---
name: nccl_optimizer
description: >
  Detect the optimal NCCL configuration for distributed GPU training on this machine.
  Checks GPU topology (NVLink/PCIe), whether RDMA (InfiniBand / RoCE) is available,
  benchmarks intra-node collective bandwidth and peer-to-peer GPU bandwidth,
  and optionally benchmarks inter-node bandwidth via MPI.
  Use when: setting up multi-GPU or multi-node training, diagnosing slow collective
  communication, or tuning NCCL for a new cluster node.
---

# NCCL Optimizer

Finds the best NCCL communication configuration for distributed training with clear
separation of **intra-node** and **inter-node** bandwidth metrics.

## What it does

1. **GPU topology** — `nvidia-smi topo -m` to detect NVLink vs PCIe.
2. **RDMA check** — `ibv_devinfo` PORT_ACTIVE state for InfiniBand/RoCE.
   - ✅ RDMA → emit recommended `NCCL_IB_*` env-vars.
   - ❌ No RDMA → socket benchmark sweep.
3. **Intra-node all-reduce** — sweeps `NCCL_SOCKET_IFNAME` × `NCCL_NET_GDR_LEVEL` ×
   `NCCL_IB_TIMEOUT`, runs `all_reduce_perf -g <N>`, picks best bus bandwidth.
4. **Intra-node P2P** — `p2p_bw` for GPU↔GPU pair bandwidth (if available).
5. **Inter-node benchmark** — if `nodes=` passed, runs MPI `all_reduce_perf` across nodes;
   otherwise emits a ready-to-run command.

## Prerequisites

| Tool | Purpose | Install |
|------|---------|---------|
| `nvidia-smi` | GPU info + topology | NVIDIA driver |
| `ibv_devinfo` | RDMA detection | `apt install ibverbs-utils` |
| `all_reduce_perf` | Collective benchmark | See below |
| `p2p_bw` | Peer-to-peer benchmark | Same nccl-tests build |
| `mpirun` | Inter-node benchmark | `apt install openmpi-bin` |

### Build nccl-tests

```bash
git clone https://github.com/NVIDIA/nccl-tests.git
cd nccl-tests
# For V100 (sm_70), A100 (sm_80), A800 (sm_80), H100 (sm_90):
make -j$(nproc) CUDA_HOME=/usr/local/cuda \
  NVCC_GENCODE="-gencode=arch=compute_80,code=sm_80"
export PATH=$PWD/build:$PATH
```

## Usage

```bash
# Intra-node only
openclaw skill run nccl_optimizer

# Include inter-node benchmark (requires passwordless SSH + MPI)
openclaw skill run nccl_optimizer "nodes=10.0.0.1,10.0.0.2"
```

## Metrics explained

| Metric | What it measures |
|--------|-----------------|
| All-reduce bus BW (intra) | Collective throughput across local GPUs — relevant for single-node training |
| P2P bandwidth | GPU↔GPU direct copy speed (NVLink ≫ PCIe) |
| All-reduce bus BW (inter) | Collective throughput across nodes — bottleneck for multi-node training |

## Notes

- Bus bandwidth normalises for GPU count: `(N-1)/N × data / time`. Compare at same N.
- Multi-node training is almost always bottlenecked by inter-node bandwidth, not intra-node.
- RDMA (InfiniBand/RoCE) typically gives 10-100× better inter-node bandwidth than TCP.
