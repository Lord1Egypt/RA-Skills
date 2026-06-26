# NVIDIA CUDA Skill Notes

This file is reference material for the `nvidia-cuda` skill. Read it when you need official grounding for a tuning choice, a code review decision, or a user-facing explanation.

## Official facts to use

### Mixed precision

- PyTorch AMP says lower precision ops such as linear layers and convolutions are often much faster in lower precision, while other ops still need FP32 range.
- Current AMP API is `torch.amp.autocast(...)` and `torch.amp.GradScaler(...)`; old `torch.cuda.amp.*` entry points are deprecated.
- PyTorch docs:
  - https://docs.pytorch.org/docs/stable/amp.html

### TF32 and FP32 matmul precision

- `torch.set_float32_matmul_precision("high" | "medium")` can significantly improve performance for FP32 matmuls on CUDA.
- It changes internal computation precision, not output dtype.
- On Ampere and later, TF32 can improve speed but may reduce accuracy for some workloads.
- PyTorch docs:
  - https://docs.pytorch.org/docs/stable/generated/torch.set_float32_matmul_precision.html
  - https://docs.pytorch.org/docs/stable/notes/numerical_accuracy.html

### CUDA env vars and allocator/debug knobs

- `PYTORCH_ALLOC_CONF`, `CUDA_LAUNCH_BLOCKING`, `CUDA_VISIBLE_DEVICES`, TF32 override knobs, cuDNN cache or workspace knobs, and NCCL non-blocking error handling are documented in one place.
- PyTorch docs:
  - https://docs.pytorch.org/docs/stable/cuda_environment_variables.html

### Data movement

- PyTorch data docs say host-to-GPU copies are much faster from pinned memory.
- `DataLoader(pin_memory=True)` automatically places fetched tensors in pinned memory.
- PyTorch docs:
  - https://docs.pytorch.org/docs/stable/data.html

### Distributed backend choice

- PyTorch distributed docs say the rule of thumb for CUDA distributed training is NCCL.
- PyTorch distributed overview says:
  - use DDP when the model fits on one GPU
  - use FSDP2 when the model cannot fit on one GPU
- PyTorch docs:
  - https://docs.pytorch.org/docs/stable/distributed.html
  - https://docs.pytorch.org/tutorials/beginner/dist_overview.html
  - https://docs.pytorch.org/tutorials/intermediate/FSDP_tutorial.html

### Activation checkpointing

- Activation checkpointing trades compute for memory.
- PyTorch recommends `use_reentrant=False`.
- PyTorch docs:
  - https://docs.pytorch.org/docs/stable/checkpoint.html

### `torch.compile`

- `torch.compile` supports modes `default`, `reduce-overhead`, `max-autotune`, and `max-autotune-no-cudagraphs`.
- `reduce-overhead` and `max-autotune` can leverage CUDA Graphs for suitable GPU paths.
- `shape_padding` exists to better align loads on GPUs, especially for tensor cores.
- PyTorch docs:
  - https://docs.pytorch.org/docs/stable/generated/torch.compile.html

### NCCL tuning and debug

- PyTorch docs recommend NCCL for CUDA and point to NVIDIA NCCL docs for the full env list.
- NCCL docs describe debug and subsystem filters such as `NCCL_DEBUG` and `NCCL_DEBUG_SUBSYS`.
- PyTorch docs:
  - https://docs.pytorch.org/docs/stable/distributed.html
- NVIDIA docs:
  - https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2265/user-guide/docs/env.html

### Profiling

- Nsight Systems is the first profiler to reach for when you need end-to-end CUDA timeline truth.
- NVIDIA docs note that heavy Unified Memory migration traffic is a performance problem and recommend manual copies from pinned host memory or peer copies instead.
- NVIDIA docs:
  - https://docs.nvidia.com/nsight-systems/UserGuide/

### Custom kernel heuristics

- CUDA best practices say:
  - threads per block should be a multiple of 32
  - 128 to 256 threads per block is a good initial range for experimentation
  - higher occupancy does not automatically mean higher performance
  - coalescing and latency hiding are core concerns
- NVIDIA docs:
  - https://docs.nvidia.com/cuda/pdf/CUDA_C_Best_Practices_Guide.pdf

### Flash attention backends and newer implementations

- PyTorch attention docs expose registration and activation for newer flash attention implementations via `register_flash_attention_impl()` and `activate_flash_attention_impl()`.
- The documented implementation identifiers include `FA3` and `FA4`.
- PyTorch attention docs also expose `list_flash_attention_impls()`, `current_flash_attention_impl()`, and `restore_flash_attention_impl()`.
- `scaled_dot_product_attention` says it will automatically choose the most optimal implementation when possible unless you override backend choice.
- PyTorch docs:
  - https://docs.pytorch.org/docs/stable/generated/torch.nn.attention.register_flash_attention_impl.html
  - https://docs.pytorch.org/docs/stable/generated/torch.nn.attention.activate_flash_attention_impl.html
  - https://docs.pytorch.org/docs/stable/nn.attention.html
  - https://docs.pytorch.org/docs/stable/generated/torch.nn.attention.sdpa_kernel.html
  - https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html

### cuDNN and Transformer Engine attention on Hopper and Blackwell

- cuDNN frontend documents unified SDPA based on the FlashAttention-2 algorithm.
- cuDNN attention support matrix includes Hopper and Blackwell paths, with fp8, fp16, and bf16 support depending on phase and architecture.
- Transformer Engine docs state both its flash-attention backend and cuDNN attention backend are flash-algorithm based.
- Transformer Engine docs also note cuDNN attention had 20-50% advantages on Hopper in their benchmarks for a number of common model configurations.
- NVIDIA docs:
  - https://docs.nvidia.com/deeplearning/cudnn/frontend/latest/operations/Attention.html
  - https://docs.nvidia.com/deeplearning/transformer-engine-releases/release-2.4/user-guide/examples/attention/attention.html

### Variable-length attention

- PyTorch attention docs include a `varlen` module for variable-length attention using Flash Attention.
- PyTorch docs:
  - https://docs.pytorch.org/docs/main/nn.attention.varlen.html

### Reproducibility

- cuDNN docs state bitwise reproducibility is not guaranteed across architectures.
- NVIDIA docs:
  - https://docs.nvidia.com/deeplearning/cudnn/backend/v9.13.0/developer/misc.html

### TensorRT inference note

- TensorRT best practices separate engine build from runtime profiling and recommend profiling inference rather than the build phase.
- NVIDIA docs:
  - https://docs.nvidia.com/deeplearning/tensorrt/latest/performance/best-practices.html

### TensorRT-LLM serving algorithms

- TensorRT-LLM documents paged context attention as useful for large input lengths and safe to benchmark as an opt-in build flag.
- TensorRT-LLM docs describe speculative decoding as a family of techniques that can reduce average per-token latency when the GPU is underutilized at small batch sizes.
- TensorRT-LLM docs cover in-flight batching and scheduler runtime options separately from build-time attention choices.
- NVIDIA docs:
  - https://nvidia.github.io/TensorRT-LLM/performance/performance-tuning-guide/useful-build-time-flags.html
  - https://nvidia.github.io/TensorRT-LLM/advanced/speculative-decoding.html
  - https://nvidia.github.io/TensorRT-LLM/performance/performance-tuning-guide/useful-runtime-flags.html

### Distributed optimizer and large-model sharding

- Megatron Core distributed optimizer docs describe memory savings from sharding optimizer state across data parallel ranks.
- Megatron Core parallelism docs recommend sequence parallelism with tensor parallelism and position context parallelism as the lever for long sequences.
- Megatron Core docs also expose expert parallelism for MoE and FSDP-style sharding strategies.
- NVIDIA docs:
  - https://docs.nvidia.com/megatron-core/developer-guide/0.15.0/api-guide/dist_optimizer.html
  - https://docs.nvidia.com/megatron-core/developer-guide/0.16.0/user-guide/parallelism-guide.html
  - https://docs.nvidia.com/megatron-core/developer-guide/latest/user-guide/features/custom_fsdp.html

### DDP, FSDP, and torchrun smoke guidance

- `torchrun` is the official launcher for single-node and multi-node distributed training and sets `LOCAL_RANK`, `RANK`, and related env vars for the script.
- PyTorch docs explicitly recommend NCCL for best GPU training performance.
- DDP docs state `DistributedDataParallel` is significantly faster than `torch.nn.DataParallel` for single-node multi-GPU data parallel training.
- DDP docs require the process group to be initialized before constructing `DistributedDataParallel`.
- DDP docs use `device_ids=[local_rank]` and `output_device=local_rank` for the one-GPU-per-process training pattern.
- FSDP docs say to wrap the module first and create the optimizer after wrapping.
- FSDP docs show the canonical wrapping pattern with `FullyShardedDataParallel`.
- PyTorch docs:
  - https://docs.pytorch.org/docs/stable/elastic/run.html
  - https://docs.pytorch.org/docs/stable/generated/torch.nn.parallel.DistributedDataParallel.html
  - https://docs.pytorch.org/docs/stable/fsdp.html

### Triton review guidance

- Triton is the official language and compiler for productively writing custom DNN compute kernels on modern GPUs.
- Triton tutorials explicitly recommend validating and benchmarking custom ops against native reference implementations.
- Triton docs expose compiler hints and debug ops such as `multiple_of`, `max_contiguous`, `device_print`, and `device_assert`, which are useful review surfaces.
- Triton debugging docs recommend `TRITON_INTERPRET=1` for CPU-interpreter debugging, with caveats around `bfloat16` and indirect memory access.
- NVIDIA Compute Sanitizer is the official NVIDIA correctness tool for CUDA kernels and recommends running `memcheck` first before `racecheck` or `synccheck`.
- Triton docs:
  - https://triton-lang.org/main/index.html
  - https://triton-lang.org/main/getting-started/tutorials/01-vector-add.html
  - https://triton-lang.org/main/python-api/triton.language.html
  - https://triton-lang.org/main/programming-guide/chapter-3/debugging.html
  - https://triton-lang.org/main/python-api/generated/triton.testing.assert_close.html
  - https://triton-lang.org/main/python-api/generated/triton.testing.do_bench.html
- NVIDIA docs:
  - https://docs.nvidia.com/compute-sanitizer/ComputeSanitizer/index.html
