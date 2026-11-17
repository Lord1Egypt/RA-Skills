# Platform interpretation notes

Use these notes after collecting a report. Keep observations separate from conclusions, especially when the process runs inside a container or scheduler allocation.

## Resource layers

Reason about resources in this order:

1. **Node hardware**: components physically installed in, or exposed to, the host operating system.
2. **Process visibility**: CPUs, memory, devices, and files visible inside the current namespace, VM, container, or remote session.
3. **Allocation limits**: cgroup, Kubernetes, Slurm, or runtime constraints applied to the current workload.
4. **Driver and toolkit**: whether the operating system can use the device and whether development tools are installed.
5. **Framework readiness**: whether the current Python environment can initialize the accelerator.

Do not collapse these layers into a single “available” claim.

## Kubernetes, containers, and schedulers

The collector reads local cgroup files and selected environment variables; it does not contact the Kubernetes API.

- `effective_cpu_cores` is the minimum of the process-visible CPU count, cpuset size, and CPU quota when those values exist. A fractional quota is meaningful.
- `effective_memory_bytes` is bounded by `memory.max` on cgroup v2 or `memory.limit_in_bytes` on cgroup v1. `/proc/meminfo` can still describe the node rather than the pod.
- Kubernetes **requests** are scheduling hints and are not generally discoverable from inside a pod. Report them only when the workload explicitly exposes them through the Downward API or the user provides the manifest.
- A Kubernetes GPU limit commonly appears as devices exposed by the container runtime. Reconcile `CUDA_VISIBLE_DEVICES` or `NVIDIA_VISIBLE_DEVICES` with `nvidia-smi -L` and the capacity query.
- NVIDIA MIG instances are allocations, not full physical GPUs. Preserve the distinction between an H100 GPU and an H100 MIG slice.
- GPU memory free and utilization are point-in-time observations. They do not prove exclusive ownership; time-slicing, MPS, or other workloads can share a device.
- A missing `kubectl` result is irrelevant inside a pod. Do not request cluster credentials merely to identify local resources.
- For Slurm, selected allocation variables describe scheduler intent. Reconcile them with cgroup and visible-device evidence before stating usable capacity.

## NVIDIA desktop and data-center GPUs

Use the NVIDIA probes as separate evidence:

- `nvidia-smi -L` identifies devices visible to the current process and shows MIG layout when available.
- The capacity query reports GPU model, driver, total/free/used memory, utilization, and PCI location.
- The CUDA level printed by `nvidia-smi` belongs to driver compatibility. It is not proof that the matching CUDA toolkit is installed.
- `nvcc --version` describes the CUDA toolkit selected on `PATH`; Python wheels can bundle a different CUDA runtime.
- A successful framework probe is stronger evidence for the current environment than driver or toolkit presence alone.

## NVIDIA Jetson

Jetson uses an integrated GPU and a Jetson Linux software stack. Desktop assumptions do not always apply.

- Identify the board from device tree and the Jetson Linux/L4T release from `/etc/nv_tegra_release`.
- Treat the absence of `nvidia-smi` as normal on many Jetson configurations.
- Use `tegrastats` for a short live telemetry sample and `nvpmodel -q` for the selected power profile.
- Do not infer an exact JetPack release from memory when compatibility matters; verify the current NVIDIA mapping.
- For deep Jetson health, memory, runtime, and inference diagnostics, prefer NVIDIA's specialized open-source [`jetson-device-skills`](https://github.com/NVIDIA-AI-IOT/jetson-device-skills) when it is installed. This skill provides the portable inventory layer.

## Raspberry Pi and compatible SBCs

- Prefer `/sys/firmware/devicetree/base/model` for the marketed board model.
- Preserve Raspberry Pi revision data but redact the serial number before sharing.
- `vcgencmd get_throttled` reports current and historical under-voltage or throttling flags. A nonzero historical flag does not prove the condition is active now.
- `vcgencmd measure_temp` is only a point-in-time SoC reading.
- Clones and other ARM SBCs may expose different device-tree, firmware, NPU, and thermal interfaces. Report an unsupported probe as unknown rather than identifying the board by architecture alone.

## AMD, Intel, and Apple accelerators

- For AMD, distinguish the kernel driver, ROCm installation, agents reported by `rocminfo`, and framework HIP support.
- For Intel, `xpu-smi`, OpenCL, and Vulkan expose different runtime layers; one succeeding does not imply the others work.
- On Apple Silicon, the integrated GPU and unified memory do not map directly to dedicated VRAM. Use `system_profiler` for hardware identity and test Metal support in the actual framework when needed.

## Virtualization and passthrough

A guest or container can only report hardware exposed through its boundary. PCI passthrough, virtual GPUs, WSL, and remote development containers may hide the physical host or present a virtual device. State which boundary the report describes.

## Sharing reports

Default redaction removes common host and device identifiers, but no automatic filter is perfect. Before publishing a report, review mount paths, custom device names, firmware strings, command errors, and third-party tool output for organization-specific information.
