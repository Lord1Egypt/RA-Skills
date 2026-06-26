"""
nccl_optimizer — Detect the best NCCL configuration for distributed training.

**Linux only.** NCCL itself only supports Linux; this skill will exit cleanly
on other platforms with an explanatory message.

Workflow:
  1. OS check — abort early on non-Linux.
  2. Detect GPU info + intra-node topology (NVLink / PCIe).
  3. Check RDMA (InfiniBand / RoCE) availability via ibv_devinfo (ACTIVE state).
  4. Intra-node benchmark:
       - all_reduce_perf -g <N>  → collective bus bandwidth across all local GPUs
       - p2p_bw (if available)   → peer-to-peer bandwidth between GPU pairs
  5. Inter-node benchmark:
       - If nodes= provided in message: run mpirun all_reduce_perf across nodes
       - Otherwise: emit ready-to-run inter-node command
  6. Emit final recommended env-var block.

Usage:
  main()                           # intra-node only
  main("nodes=10.0.0.1,10.0.0.2") # also benchmarks inter-node (requires SSH + MPI)
"""

import platform
import subprocess
import re
import os
import shutil
import socket as _socket


# ---------------------------------------------------------------------------
# Platform guard — NCCL is Linux-only
# ---------------------------------------------------------------------------

def _check_platform() -> str | None:
    """Return an error string if not running on Linux, else None."""
    system = platform.system()
    if system != "Linux":
        return (
            f"⛔ **Platform not supported: {system}**\n\n"
            "NCCL only runs on **Linux**. This skill requires Linux with NVIDIA GPUs.\n\n"
            "See: https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/index.html"
        )
    return None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _run_cmd(cmd: str, timeout: int = 60) -> str:
    """Run *cmd* via shell, return stdout+stderr stripped; empty string on any failure."""
    try:
        return subprocess.check_output(
            cmd, shell=True, stderr=subprocess.STDOUT, text=True, timeout=timeout
        ).strip()
    except Exception:
        return ""


def _in_container() -> bool:
    """Heuristic: detect Docker / Kubernetes / LXC container environment."""
    # /.dockerenv file is injected by Docker runtime
    if os.path.exists("/.dockerenv"):
        return True
    # /proc/1/cgroup contains 'docker' or 'kubepods' in containers
    cgroup = _run_cmd("cat /proc/1/cgroup 2>/dev/null | head -5")
    if re.search(r"docker|kubepods|containerd|lxc", cgroup, re.I):
        return True
    return False


# ---------------------------------------------------------------------------
# GPU detection
# ---------------------------------------------------------------------------

def _detect_gpu():
    """Return (gpu_names, driver, cuda, num_gpus)."""
    out = _run_cmd("nvidia-smi --query-gpu=name,driver_version --format=csv,noheader")
    gpu_names, driver = [], ""
    if out:
        for i, line in enumerate(out.splitlines()):
            parts = [p.strip() for p in line.split(",")]
            if parts:
                gpu_names.append(parts[0])
            if i == 0 and len(parts) > 1:
                driver = parts[1]

    # CUDA version: try nvcc first, fall back to nvidia-smi header
    cuda = ""
    nvcc_out = _run_cmd("nvcc --version 2>/dev/null")
    if nvcc_out:
        m = re.search(r"release\s+([0-9.]+)", nvcc_out)
        cuda = m.group(1) if m else ""
    if not cuda:
        smi_top = _run_cmd("nvidia-smi 2>/dev/null")
        m = re.search(r"CUDA Version:\s*([0-9.]+)", smi_top)
        cuda = m.group(1) if m else "unknown"

    return gpu_names, driver, cuda, len(gpu_names)


def _detect_topology(num_gpus: int):
    """Return (has_nvlink: bool, topo_summary: str)."""
    out = _run_cmd("nvidia-smi topo -m 2>/dev/null")
    if not out:
        return False, "topology info unavailable (`nvidia-smi topo` not supported)"
    has_nvlink = bool(re.search(r"\bNV\d+\b", out))
    lines = [l for l in out.splitlines() if l.strip()]
    summary = "\n".join(lines[:min(len(lines), num_gpus + 3)])
    return has_nvlink, summary


# ---------------------------------------------------------------------------
# RDMA detection
# ---------------------------------------------------------------------------

def _rdma_available():
    """Return (available: bool, active_devices: list[str]).
    Considers a device active only when its port state is PORT_ACTIVE.
    """
    out = _run_cmd("ibv_devinfo 2>/dev/null")
    if not out:
        return False, []
    active_devs, current_dev = [], None
    for line in out.splitlines():
        dev_m = re.match(r"^hca_id:\s*(\S+)", line)
        if dev_m:
            current_dev = dev_m.group(1)
        if re.search(r"state:\s*(PORT_ACTIVE|4\b)", line) and current_dev:
            if current_dev not in active_devs:
                active_devs.append(current_dev)
    return bool(active_devs), active_devs


def _rdma_gid_index():
    """Detect RoCEv2 GID index via show_gids; default to 3."""
    out = _run_cmd("show_gids 2>/dev/null")
    if out:
        m = re.search(r"(\d+)\s+\S+\s+\S+\s+ROCEv2", out)
        if m:
            return m.group(1)
    # Fallback: parse ibv_devinfo -v for GID entries
    out2 = _run_cmd("ibv_devinfo -v 2>/dev/null")
    if out2:
        m = re.search(r"GID\[(\d+)\].*:.*:.*:.*fe80", out2, re.I)
        if m:
            return m.group(1)
    return "3"


# ---------------------------------------------------------------------------
# nccl-tests binary discovery
# ---------------------------------------------------------------------------

_NCCL_SEARCH_DIRS = [
    "/usr/local/nccl-tests/build",
    os.path.expanduser("~/nccl-tests/build"),
    "./nccl-tests/build",
    "/opt/nccl-tests/build",
]


def _find_binary(name: str) -> str | None:
    """Find an nccl-tests binary in PATH or common install locations."""
    found = shutil.which(name)
    if found:
        return found
    for d in _NCCL_SEARCH_DIRS:
        p = os.path.join(d, name)
        if os.path.isfile(p) and os.access(p, os.X_OK):
            return p
    return None


# ---------------------------------------------------------------------------
# Bandwidth parsing
# ---------------------------------------------------------------------------

def _parse_bandwidth(output: str) -> float:
    """Extract average bus bandwidth (GB/s) from nccl-tests output."""
    # Primary: summary line "# Avg bus bandwidth    : 127.9"
    m = re.search(r"Avg bus bandwidth\s*[:\-]+\s*([0-9.]+)", output)
    if m:
        return float(m.group(1))
    # Fallback: last busbw column in data rows
    # Format: size count type redop root time algbw busbw #wrong ...
    values = re.findall(r"^\s*\d+\s+\d+\s+\S+\s+\S+\s+\S+\s+[0-9.]+\s+[0-9.]+\s+([0-9.]+)", output, re.M)
    return float(values[-1]) if values else 0.0


def _parse_p2p_bandwidth(output: str) -> float:
    """Extract max unidirectional bandwidth from p2p_bw output (GB/s)."""
    values = re.findall(r"^\s*\d+\s+\d+\s+([0-9.]+)\s*$", output, re.M)
    if values:
        return max(float(v) for v in values)
    m = re.search(r"([0-9.]+)\s*GB/s", output)
    return float(m.group(1)) if m else 0.0


# ---------------------------------------------------------------------------
# Network interface detection (Linux-aware, container-safe)
# ---------------------------------------------------------------------------

def _socket_interfaces() -> list:
    """Return non-loopback, non-virtual interfaces with carrier (link-up).

    Uses /sys/class/net when available (standard Linux), falls back to
    `ip link show` (works in most containers), then `ifconfig`.
    Excludes loopback, docker bridges, virbr*, and veth interfaces.
    """
    _EXCLUDE = re.compile(r"^(lo|docker|virbr|veth|br-|tunl|dummy)")

    ifaces = []

    # Method 1: sysfs (standard Linux, may not be mounted in all containers)
    if os.path.isdir("/sys/class/net"):
        try:
            ifaces = [i for i in os.listdir("/sys/class/net") if not _EXCLUDE.match(i)]
        except OSError:
            pass

    # Method 2: ip link show (works in containers without sysfs)
    if not ifaces:
        ip_out = _run_cmd("ip link show 2>/dev/null")
        ifaces = re.findall(r"^\d+:\s+(\S+):", ip_out, re.M)
        ifaces = [i.rstrip(":@") for i in ifaces if not _EXCLUDE.match(i)]

    # Method 3: ifconfig (older systems)
    if not ifaces:
        ifc_out = _run_cmd("ifconfig -a 2>/dev/null")
        ifaces = re.findall(r"^(\S+)\s+Link|^(\S+):\s+flags", ifc_out, re.M)
        ifaces = [a or b for a, b in ifaces if not _EXCLUDE.match(a or b)]

    if not ifaces:
        return ["eth0"]  # last-resort default

    # Filter to link-up interfaces
    active = []
    for iface in ifaces:
        # sysfs carrier file
        carrier_path = f"/sys/class/net/{iface}/carrier"
        if os.path.exists(carrier_path):
            carrier = _run_cmd(f"cat {carrier_path} 2>/dev/null")
            if carrier == "1":
                active.append(iface)
        else:
            # ip link operstate
            state = _run_cmd(f"cat /sys/class/net/{iface}/operstate 2>/dev/null")
            if state in ("up", "unknown"):
                active.append(iface)

    return (active or ifaces)[:3]


# ---------------------------------------------------------------------------
# Intra-node benchmarks
# ---------------------------------------------------------------------------

def _run_intranode_allreduce(binary: str, env: dict, num_gpus: int) -> tuple:
    """Run all_reduce_perf across all local GPUs. Returns (bw, raw_output)."""
    env_str = "NCCL_DEBUG=WARN " + " ".join(f"{k}={v}" for k, v in env.items())
    cmd = f"{env_str} {binary} -b 8M -e 4G -f 2 -g {max(1, num_gpus)} 2>&1"
    out = _run_cmd(cmd, timeout=180)
    return _parse_bandwidth(out), out


def _run_p2p_bw(p2p_binary: str, num_gpus: int) -> float:
    """Run p2p_bw between all GPU pairs. Returns max observed GB/s."""
    cmd = f"NCCL_DEBUG=WARN {p2p_binary} -b 1G -e 4G -f 2 -g {max(1, num_gpus)} 2>&1"
    out = _run_cmd(cmd, timeout=120)
    return _parse_p2p_bandwidth(out)


def _optimize_socket_intranode(binary: str, num_gpus: int) -> tuple:
    """Sweep socket configs, return (best_env, best_bw).

    Search space:
      NCCL_SOCKET_IFNAME  : top-3 active interfaces
      NCCL_NET_GDR_LEVEL  : 0, 2
      NCCL_IB_TIMEOUT     : 22, 30
    """
    interfaces = _socket_interfaces()
    best_env, best_bw = None, -1.0
    for iface in interfaces:
        for gdr_level in ("0", "2"):
            for ib_timeout in ("22", "30"):
                env = {
                    "NCCL_SOCKET_IFNAME": iface,
                    "NCCL_IB_DISABLE": "1",
                    "NCCL_NET_GDR_LEVEL": gdr_level,
                    "NCCL_IB_TIMEOUT": ib_timeout,
                }
                bw, _ = _run_intranode_allreduce(binary, env, num_gpus)
                if bw > best_bw:
                    best_bw = bw
                    best_env = dict(env)
    return best_env, best_bw


# ---------------------------------------------------------------------------
# Inter-node benchmarks
# ---------------------------------------------------------------------------

def _find_mpirun() -> str | None:
    for name in ("mpirun", "orterun", "mpiexec"):
        p = shutil.which(name)
        if p:
            return p
    return None


def _run_internode_allreduce(binary: str, mpirun: str, nodes: list,
                              gpus_per_node: int, best_env: dict) -> tuple:
    """Run all_reduce_perf across multiple nodes via MPI. Returns (bw, raw_output)."""
    host_str = ",".join(f"{n}:{gpus_per_node}" for n in nodes)
    total_ranks = len(nodes) * gpus_per_node
    env_args = " ".join(f"-x {k}={v}" for k, v in best_env.items())
    cmd = (
        f"{mpirun} -np {total_ranks} -H {host_str} "
        f"-x NCCL_DEBUG=WARN {env_args} "
        f"{binary} -b 8M -e 4G -f 2 -g 1 2>&1"
    )
    out = _run_cmd(cmd, timeout=300)
    return _parse_bandwidth(out), out


def _parse_nodes(message: str) -> list:
    """Extract node list from 'nodes=10.0.0.1,10.0.0.2' or 'hosts=a,b'."""
    m = re.search(r"(?:nodes?|hosts?)=([^\s]+)", message, re.I)
    if m:
        return [n.strip() for n in m.group(1).split(",") if n.strip()]
    return []


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def _generate_report(message: str = "") -> str:
    # ── Platform guard ────────────────────────────────────────────────────
    err = _check_platform()
    if err:
        return err

    lines = ["# NCCL Optimizer Report\n"]
    local_hostname = _socket.gethostname()
    is_container = _in_container()

    # ── Environment info ──────────────────────────────────────────────────
    lines.append(f"**Host:** `{local_hostname}`")
    if is_container:
        lines.append("⚠️  **Container environment detected** — interface names may differ from host; "
                      "ensure NCCL can reach peer containers/nodes via the expected interface.\n")

    # ── GPU info ──────────────────────────────────────────────────────────
    gpu_names, driver, cuda, num_gpus = _detect_gpu()
    if gpu_names:
        lines.append(f"**GPUs detected ({num_gpus}):** {', '.join(set(gpu_names))}")
        lines.append(f"**Driver:** {driver}  |  **CUDA:** {cuda}\n")
    else:
        lines.append("⚠️  No NVIDIA GPU info found (`nvidia-smi` missing or no GPU present).\n")
        num_gpus = 1

    # ── Topology ──────────────────────────────────────────────────────────
    has_nvlink, topo_summary = _detect_topology(num_gpus)
    lines.append("## Intra-node GPU Topology\n")
    if has_nvlink:
        lines.append("✅ **NVLink detected** — GPUs can communicate at NVLink speeds.\n")
    else:
        lines.append("ℹ️  **No NVLink** — GPU↔GPU traffic goes over PCIe.\n")
    lines.append("```")
    lines.append(topo_summary)
    lines.append("```\n")

    # ── RDMA check ────────────────────────────────────────────────────────
    rdma_ok, active_devs = _rdma_available()
    best_env: dict = {}

    if rdma_ok:
        lines.append("## ✅ RDMA Available\n")
        lines.append(f"Active InfiniBand/RoCE devices: **{', '.join(active_devs)}**\n")
        gid_idx = _rdma_gid_index()
        hca = active_devs[0]
        best_env = {
            "NCCL_IB_HCA": hca,
            "NCCL_IB_GID_INDEX": gid_idx,
            "NCCL_IB_DISABLE": "0",
            "NCCL_IB_TC": "106",
            "NCCL_IB_RETRY_CNT": "7",
            "NCCL_IB_TIMEOUT": "22",
            "NCCL_NET_GDR_LEVEL": "2",
        }
        lines.append("### Recommended NCCL env-vars (RDMA mode)\n")
        lines.append("```bash")
        for k, v in best_env.items():
            lines.append(f"export {k}={v}")
        lines.append("export NCCL_DEBUG=WARN")
        lines.append("```\n")
        lines.append("> Verify GID index with `show_gids` (RoCEv2 → usually index 3).")

    else:
        lines.append("## ℹ️  No RDMA — Socket mode\n")
        lines.append("No active InfiniBand/RoCE device detected. Falling back to TCP sockets.\n")

        binary = _find_binary("all_reduce_perf")
        if binary is None:
            lines.append("⚠️  `all_reduce_perf` not found. Build nccl-tests first:\n")
            lines.append("```bash")
            lines.append("git clone https://github.com/NVIDIA/nccl-tests.git && cd nccl-tests")
            lines.append("# Adjust arch flag: V100=sm_70, A100/A800=sm_80, H100=sm_90")
            lines.append("make -j$(nproc) CUDA_HOME=/usr/local/cuda \\")
            lines.append("  NVCC_GENCODE=\"-gencode=arch=compute_80,code=sm_80\"")
            lines.append("export PATH=$PWD/build:$PATH")
            lines.append("```\n")
        else:
            lines.append(f"Benchmark binary: `{binary}`\n")

            # ── Intra-node sweep ──────────────────────────────────────────
            lines.append("## Intra-node Benchmark\n")
            lines.append(f"> Measures **all-reduce collective bus bandwidth** across all {num_gpus} local GPUs.")
            lines.append("> Relevant for **single-node multi-GPU** training.\n")
            lines.append("Running parameter sweep (may take several minutes)…\n")

            env, bw = _optimize_socket_intranode(binary, num_gpus)

            if env and bw > 0:
                best_env = env
                lines.append(f"### ✅ Best intra-node config — **{bw:.1f} GB/s bus bandwidth**\n")
                lines.append("```bash")
                for k, v in env.items():
                    lines.append(f"export {k}={v}")
                lines.append("export NCCL_SOCKET_NTHREADS=4")
                lines.append("export NCCL_NSOCKS_PERTHREAD=4")
                lines.append("export NCCL_BUFFSIZE=8388608")
                lines.append("export NCCL_DEBUG=WARN")
                lines.append("```\n")
            else:
                # Benchmark failed — diagnose and provide fallback
                iface = (_socket_interfaces() or ["eth0"])[0]
                best_env = {
                    "NCCL_SOCKET_IFNAME": iface,
                    "NCCL_IB_DISABLE": "1",
                    "NCCL_NET_GDR_LEVEL": "2",
                    "NCCL_IB_TIMEOUT": "22",
                }
                lines.append("⚠️  Benchmark produced no results. Common causes on Linux:\n")
                lines.append("- **CUDA arch mismatch** — rebuild with correct `NVCC_GENCODE` for your GPU:")
                lines.append("  ```bash")
                lines.append("  # V100: sm_70 | A100/A800: sm_80 | H100: sm_90")
                lines.append("  make -j$(nproc) CUDA_HOME=/usr/local/cuda \\")
                lines.append("    NVCC_GENCODE=\"-gencode=arch=compute_80,code=sm_80\"")
                lines.append("  ```")
                lines.append("- **GPU not accessible** — check `nvidia-smi` and driver status")
                lines.append("- **Container without GPU passthrough** — verify `--gpus all` flag\n")
                lines.append("**Fallback config (untuned):**")
                lines.append("```bash")
                for k, v in best_env.items():
                    lines.append(f"export {k}={v}")
                lines.append("export NCCL_SOCKET_NTHREADS=4")
                lines.append("export NCCL_NSOCKS_PERTHREAD=4")
                lines.append("export NCCL_BUFFSIZE=8388608")
                lines.append("export NCCL_DEBUG=WARN")
                lines.append("```\n")

            # ── P2P bandwidth ─────────────────────────────────────────────
            p2p_binary = _find_binary("p2p_bw")
            if p2p_binary and num_gpus >= 2:
                p2p_bw = _run_p2p_bw(p2p_binary, num_gpus)
                if p2p_bw > 0:
                    lines.append(f"**Intra-node GPU peer-to-peer bandwidth:** {p2p_bw:.1f} GB/s  ")
                    lines.append("_(point-to-point, not collective; NVLink typically 600+ GB/s, PCIe ~32 GB/s)_\n")

    # ── Inter-node benchmark ──────────────────────────────────────────────
    lines.append("## Inter-node Benchmark\n")
    lines.append("> Measures **network bandwidth between nodes**. The primary bottleneck for multi-node training.\n")

    peer_nodes = _parse_nodes(message)
    mpirun = _find_mpirun()
    binary = _find_binary("all_reduce_perf")

    if peer_nodes and binary and mpirun:
        all_nodes = [local_hostname] + [n for n in peer_nodes if n != local_hostname]
        lines.append(f"Running inter-node benchmark across: `{', '.join(all_nodes)}`\n")
        internode_bw, internode_out = _run_internode_allreduce(
            binary, mpirun, all_nodes, num_gpus, best_env
        )
        if internode_bw > 0:
            lines.append(f"### ✅ Inter-node all-reduce bus bandwidth: **{internode_bw:.1f} GB/s**")
            lines.append(f"_{len(all_nodes)} nodes × {num_gpus} GPUs = {len(all_nodes)*num_gpus} total GPUs_\n")
        else:
            lines.append("⚠️  Inter-node benchmark produced no readings.\n")
            lines.append("Checklist:")
            lines.append("- Passwordless SSH between all nodes (same user)")
            lines.append("- `all_reduce_perf` at same path on all nodes")
            lines.append("- MPI hostfile / firewall allows traffic on MPI ports\n")
            lines.append("```")
            lines.append(internode_out[:800] if internode_out else "(no output)")
            lines.append("```\n")
    else:
        env_x_args = " \\\n  ".join(f"-x {k}={v}" for k, v in best_env.items())
        lines.append("To benchmark inter-node bandwidth, run on one node:\n")
        lines.append("```bash")
        lines.append("# Replace NODE1, NODE2 etc. with actual hostnames/IPs")
        if not mpirun:
            lines.append("# Install MPI first:  apt install openmpi-bin  (Debian/Ubuntu)")
            lines.append("#                     yum install openmpi       (RHEL/CentOS)")
        lines.append(f"mpirun -np $((NNODES * {num_gpus})) -H NODE1:{num_gpus},NODE2:{num_gpus} \\")
        if env_x_args:
            lines.append(f"  {env_x_args} \\")
        lines.append("  -x NCCL_DEBUG=WARN \\")
        binary_path = binary or "/path/to/nccl-tests/build/all_reduce_perf"
        lines.append(f"  {binary_path} -b 8M -e 4G -f 2 -g 1")
        lines.append("```\n")
        lines.append("Or let this skill run it automatically:")
        lines.append("```")
        lines.append('openclaw skill run nccl_optimizer "nodes=10.0.0.1,10.0.0.2"')
        lines.append("```\n")

    # ── Metric explanation ────────────────────────────────────────────────
    lines.append("---\n")
    lines.append("## Understanding the metrics\n")
    lines.append("| Metric | What it measures | Relevant for |")
    lines.append("|--------|-----------------|--------------|")
    lines.append("| **All-reduce bus BW** (intra-node) | Collective throughput across local GPUs | Single-node multi-GPU |")
    lines.append("| **P2P bandwidth** | Direct GPU↔GPU copy (NVLink / PCIe) | Pipeline parallelism, ZeRO |")
    lines.append("| **All-reduce bus BW** (inter-node) | Collective throughput across nodes | Multi-node training |")
    lines.append("")
    lines.append("> **Bus BW vs raw link speed:** all-reduce with N GPUs transfers `(N-1)/N × data` per GPU.")
    lines.append("> Bus bandwidth normalises for this — valid for comparing across different GPU counts.\n")
    lines.append("## General tuning tips\n")
    lines.append("- `NCCL_DEBUG=INFO` — diagnose hangs / connection errors")
    lines.append("- `NCCL_BUFFSIZE=8388608` — larger buffers improve large-message throughput")
    lines.append("- `NCCL_SOCKET_NTHREADS=4` + `NCCL_NSOCKS_PERTHREAD=4` — more threads for TCP mode")
    lines.append("- Multi-node: set `MASTER_ADDR` / `MASTER_PORT`, or use `torchrun --rdzv_backend=c10d`")
    lines.append("- In containers: mount `/dev/infiniband` and run with `--privileged` or `--cap-add IPC_LOCK` for RDMA")

    return "\n".join(lines)


def main(message: str = "") -> str:
    """Skill entry point. Returns a Markdown-formatted report."""
    return _generate_report(message)


if __name__ == "__main__":
    import sys
    print(main(" ".join(sys.argv[1:])))
