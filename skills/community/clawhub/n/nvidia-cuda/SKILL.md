---
name: nvidia-cuda
description: Use when work targets NVIDIA GPUs for deep learning training, inference, distributed execution, CUDA/Triton kernels, or AI infra tuning. Enforces GPU-aware code conventions for PyTorch on CUDA, including dtype policy, memory movement, NCCL/DDP/FSDP choices, profiling, benchmarking, and H100/H200/B200 optimization habits.
---

# NVIDIA CUDA

Use this skill when the task involves NVIDIA GPU training or inference, multi-GPU execution, CUDA/Triton kernels, or CUDA-specific performance/debugging work.

This skill is for implementation and review, not generic theory. It should push the work toward:

- correct GPU usage first
- stable and measurable performance second
- low-risk tuning before low-level kernel work
- frontier algorithms only when the workload shape justifies them

## Hardware stance

Probe the actual machine before acting. This skill is written for modern NVIDIA Tensor Core systems and is especially opinionated for:

- H100 / Hopper
- H200
- B200 / Blackwell-class accelerators

It assumes the agent should actively choose precision, attention backends, sharding strategy, logging frequency, and dataloader settings instead of inheriting slow defaults.

## Use this skill for

- PyTorch training or inference on CUDA
- GPU memory, throughput, or latency bottlenecks
- DDP / FSDP / NCCL decisions
- CUDA env var and runtime hygiene
- Triton or custom CUDA kernel review
- benchmark and profiler setup for NVIDIA GPUs

## Do not use this skill for

- CPU-only optimization
- ROCm / AMD-specific work
- TPU / XLA-specific work
- vague "make it faster" requests without inspecting the actual GPU path first

## First-pass workflow

Before changing code, inspect the actual runtime surface:

1. Check hardware and driver: `nvidia-smi`
2. Check framework build: `python -c "import torch; print(torch.__version__, torch.version.cuda, torch.cuda.is_available())"`
3. Check device visibility and topology:
   - `CUDA_VISIBLE_DEVICES`
   - `torch.cuda.device_count()`
   - `torch.cuda.get_device_properties(i)`
4. Check whether the bottleneck is:
   - input pipeline
   - host/device transfer
   - eager Python overhead
   - kernel efficiency
   - distributed communication
   - memory pressure / fragmentation / OOM

Do not jump to kernel rewrites before ruling out bad data movement, wrong dtype, graph breaks, or poor distributed setup.

## Bundled tooling

Use the included scripts when you need deterministic probes instead of ad hoc snippets:

- `scripts/cuda_env_probe.py`: collect CUDA, PyTorch, device, and env facts
- `scripts/check_training_stack.py`: scan Python code for high-cost anti-patterns
- `scripts/benchmark_attention.py`: benchmark SDPA, flash, cuDNN, and official flash-implementation activation paths
- `scripts/training_step_benchmark.py`: benchmark a synthetic transformer training step with dtype, compile, and `.item()` logging knobs
- `scripts/dataloader_benchmark.py`: benchmark DataLoader worker, pinning, and prefetch settings
- `scripts/nccl_smoke.py`: run a minimal NCCL all-reduce smoke test under `torchrun`
- `scripts/ddp_fsdp_smoke.py`: run a one-step DDP or FSDP training smoke test under `torchrun`

Run the probe first, then benchmark or scan the real workload path.

## Planning hardware purchases

When the user wants current NVIDIA GPU recommendations, read:

- [references/latest-gpu-recommendations-2026-04.md](references/latest-gpu-recommendations-2026-04.md)
- the example configs under [examples/](examples)

Keep recommendation output scenario-based:

- cost-sensitive local prototyping
- serious workstation development
- enterprise server deployment
- single-node training
- rack-scale training or reasoning

Do not recommend by peak FLOPS alone. Weight memory, interconnect, thermals, deployment form, and software maturity.

## Reviewing Triton, CUDA, and distributed code

When the target includes Triton kernels, CUDA or C++ files, or distributed launcher code:

- use `scripts/check_training_stack.py` across the whole tree, not just Python subfolders
- treat Triton kernels as first-class review targets
- verify distributed paths with `scripts/nccl_smoke.py` or `scripts/ddp_fsdp_smoke.py` before claiming they are healthy
- benchmark flash attention implementation changes with `scripts/benchmark_attention.py --list-flash-impls` and explicit activation when available

## Non-negotiable code conventions

### High-cost anti-patterns to ban

Treat the following as red flags in reviews and optimization work:

1. keeping transformer training or inference in full FP32 by default on Tensor Core GPUs
2. refusing to try `torch.compile` on stable hot paths
3. staying on a generic default SDPA path on H200/B200 when newer flash-backed implementations or cuDNN/TE attention backends are available and benchmarkable
4. reaching for activation checkpointing before FSDP / ZeRO-style sharding when the real problem is replicated params, grads, or optimizer state
5. calling `.item()` every step for logging and metrics
6. leaving DataLoader workers, pinning, prefetching, and persistent workers untuned until GPU starvation shows up

If several of these exist at once, assume the GPU is underfed until proven otherwise.

### 1. Dtype policy

- On H100 / Hopper, prefer `bfloat16` for training and inference unless there is a measured or correctness-driven reason not to.
- On H200 / B200-class systems, treat BF16 or FP8-capable paths as the default starting point for deep learning workloads.
- Full FP32 by default is a correctness mode, not a performance baseline.
- Use `float16` only when a dependency or model explicitly benefits from it.
- If using `float16` training, use `torch.amp.GradScaler("cuda")`.
- For mixed precision, use the current API:
  - `torch.amp.autocast("cuda", dtype=...)`
  - not deprecated `torch.cuda.amp.*`

### 2. FP32 fallback policy

- If the model is nominally FP32 but does not require strict IEEE-style matmul precision, prefer enabling faster matmul paths with `torch.set_float32_matmul_precision("high")`.
- Disable TF32 only for reproducibility or numerics investigations.
- Never silently mix "strict numerics" and "fast numerics" requirements in the same change. State the choice.

### 3. Device movement rules

- Keep tensors on device across the hot path.
- Move data in batches, not item-by-item.
- Use `pin_memory=True` in `DataLoader` when feeding CUDA.
- Use `tensor.to("cuda", non_blocking=True)` or equivalent only when the source is pinned or already async-safe.
- Avoid CPU round-trips in the training or inference loop.

### 4. Avoid accidental synchronization

Inside hot loops, avoid or justify:

- `.item()`
- `.cpu()`
- `.numpy()`
- `print(cuda_tensor)`
- timing without `torch.cuda.synchronize()`

These often force host synchronization and distort both throughput and profiling.

### 5. Benchmarking rules

- Warm up before measuring.
- Use CUDA events or a framework benchmark harness, not bare wall clock alone.
- Synchronize before reading timings.
- Record batch size, dtype, sequence/image shape, compile state, and number of warmup / measured iterations.
- For throughput and latency claims, include the exact command or code path used.

### 6. `torch.compile` rules

- Reach correctness first in eager mode.
- Then apply `torch.compile` to stable hot paths.
- Do not reject `torch.compile` categorically for CUDA models. Benchmark it.
- Prefer:
  - `mode="default"` for general speedups
  - `mode="reduce-overhead"` for small-batch / latency-sensitive CUDA paths with stable shapes
  - `mode="max-autotune"` when compile overhead is acceptable and the path is hot enough
- If shapes are unstable, be explicit about `dynamic=True` or accept recompiles intentionally.
- Use `TORCH_LOGS=perf_hints` or `TORCH_LOGS=dynamic` when diagnosing graph breaks or overspecialization.

### 6.1 Attention kernel policy

- For transformer attention, prefer native `scaled_dot_product_attention` and PyTorch attention backends before custom kernels.
- Use PyTorch SDPA / FlashAttention backends as the default fast path on CUDA.
- On H200 / B200-class systems, do not assume the default shipped SDPA backend is the best available path. Check whether FA3 / FA4 implementations are registered and benchmark them.
- Where Transformer Engine or cuDNN attention backends are available, benchmark them against the default path on Hopper/Blackwell instead of assuming SDPA wins.
- If masks or score transforms are unusual, consider `torch.nn.attention.flex_attention` only after confirming SDPA cannot express the workload cleanly.
- For variable-length packed batches, prefer varlen / packed attention paths rather than padding to worst-case sequence length.
- Do not keep a hand-rolled eager attention implementation in a hot path if SDPA, TE attention, or TensorRT-LLM fused attention can replace it.

### 6.2 CUDA Graphs policy

- Use CUDA Graphs only for repeated, shape-stable hot paths where CPU launch overhead is material.
- Graph capture is a strong fit for:
  - small-batch inference
  - fixed-shape decode loops
  - stable training microbatches
- Do not graph workloads with live shape churn, `.item()` sync points, or allocator churn in the captured region.
- Prefer graphing after eager correctness and after compile/engine selection are already settled.

### 7. Distributed rules

- Use NCCL for distributed CUDA training.
- Use DDP when the model fits on one GPU and you mainly need data parallel scale-out.
- Use FSDP2 when the model does not fit on one GPU or optimizer state dominates memory.
- When tensor parallelism is enabled, sequence parallelism is the default companion unless a framework limitation blocks it.
- For long-context transformer training, consider context parallelism before blindly increasing tensor parallel degree.
- For MoE, use expert parallelism instead of replicating all experts everywhere.
- For large-scale runs, consider a distributed optimizer before inventing custom sharding logic.
- Use `torchrun` and one process per GPU.
- Set the current CUDA device from rank/local-rank early and only once.
- Do not tune NCCL environment variables by superstition. Change them only after evidence.

### 8. Memory rules

- Prefer algorithmic memory wins before allocator tweaks:
  - BF16
  - FSDP / sharding
  - distributed optimizer
  - smaller activation footprints
  - sequence or batch shaping
  - activation checkpointing
- When the memory problem is replicated model state, prioritize FSDP / ZeRO-2 / ZeRO-3 style sharding before gradient checkpointing.
- Use checkpointing when activation memory is the real limiter, not as a substitute for state sharding.
- If activation checkpointing is needed, prefer `use_reentrant=False` unless there is a specific reason otherwise.
- Treat allocator and workspace env vars as debugging/tuning levers, not first-line fixes.

### 9. Profiling rules

- Start with Nsight Systems for timeline truth:
  - CPU launch gaps
  - H2D / D2H copies
  - stream overlap
  - NCCL overlap and stalls
  - Unified Memory migrations
- Move to Nsight Compute only after isolating the hot kernels.
- For PyTorch-level attribution, use the profiler only if you need operator names or stack grouping.

## Frontier algorithm ladder

Use this section when the user explicitly wants leading-edge optimization or when the baseline is already healthy.

Do not apply all of these at once. Climb the ladder in order and keep a benchmark after each step.

### A. Hopper and Blackwell transformer path

For H100/H200/B200-class transformer workloads, the default advanced path is:

1. BF16 baseline
2. native SDPA / FlashAttention fast path
3. `torch.compile`
4. CUDA Graphs if shapes stabilize
5. Transformer Engine FP8 if:
   - the model is transformer-dominated
   - BF16 numerics are already validated
   - there is an accuracy gate

FP8 is not a blanket default. It is a targeted transformer optimization with strict measurement.

### B. Large-model training algorithms

For models that are too large, too long-context, or too communication-heavy, consider:

- FSDP2 / Megatron FSDP for parameter, grad, and optimizer sharding
- distributed optimizer for optimizer-state memory pressure
- tensor parallelism for large hidden dimensions
- sequence parallelism when TP is enabled
- context parallelism for long sequences
- pipeline parallelism for very deep models
- expert parallelism for MoE
- activation checkpointing when the above is still insufficient

Selection heuristics:

- if the model barely misses single-GPU fit: start with FSDP2
- if hidden dimensions are very large: add TP
- if sequence length is the actual problem: prefer CP over just raising TP
- if the model is MoE: use EP rather than replicating experts
- if optimizer state dominates: distributed optimizer or FSDP shard first

### C. LLM inference algorithms

For autoregressive serving, the advanced inference ladder is:

1. fused attention path
2. paged KV cache / paged context handling
3. continuous or inflight batching
4. chunked prefill / context chunking for large prompts
5. CUDA Graphs for stable decode loops
6. speculative decoding when low-batch latency matters and acceptance rate is healthy
7. FP8 or weight-focused quantization only after accuracy validation

Strong fits:

- paged context / chunked prefill: long prompts and mixed request sizes
- speculative decoding: low-batch underutilized serving
- inflight fused batching: multi-request serving with scheduler pressure
- FP8 serving: Hopper/Blackwell inference paths with validated quality

### D. Quantization policy

- On Hopper and newer, prefer BF16 first, FP8 second, INT8/INT4 only when memory or throughput targets require it.
- For training or finetuning quantized targets, prefer QAT or recipe-backed flows over ad hoc fake-quant code.
- For serving, keep a clear boundary between:
  - engine build or calibration
  - runtime benchmarking
  - accuracy evaluation

Do not merge a quantization change without an explicit quality gate.

## Training optimization playbook

When optimizing training code, prefer this order:

1. Ensure correct device placement and eliminate CPU fallbacks
2. Fix input pipeline:
   - `pin_memory=True`
   - enough workers
   - `persistent_workers=True` when the workload is steady and worker startup cost matters
   - tuned `prefetch_factor`
   - no CPU-heavy transforms inside the critical path unless justified
3. Set precision policy:
   - BF16 first on Hopper
   - BF16 / FP8-capable path first on H200/B200
   - FP16 only with explicit reason
4. Remove accidental syncs and per-step Python overhead
5. Try `torch.compile`
6. If this is transformer-heavy, move attention to SDPA / FlashAttention / TE attention fast paths
7. Scale to DDP or FSDP2 if single-GPU utilization or model size requires it
8. Add TP + SP, CP, PP, or EP only according to the actual bottleneck
9. Add activation checkpointing if memory still blocks batch size
10. For Hopper/Blackwell transformer stacks, evaluate Transformer Engine FP8 behind an accuracy gate
11. Profile and only then consider Triton or custom CUDA work

## Inference optimization playbook

When optimizing inference code:

1. Use `model.eval()` and `torch.no_grad()` / `torch.inference_mode()`
2. Pick dtype deliberately:
   - BF16 or FP16 on Hopper when numerically acceptable
   - TF32-enabled FP32 if accuracy must stay near FP32 but pure FP32 is too slow
3. Move attention and decode loops onto fused kernels or native SDPA paths
4. Stabilize shapes if possible
5. Apply `torch.compile` or engine compilation only after correctness baselines
6. For LLM serving, evaluate paged KV / paged context and inflight batching early
7. Use CUDA Graphs only for repeated, fixed-shape paths where launch overhead matters
8. If low-batch latency dominates, evaluate speculative decoding with acceptance-rate tracking
9. Benchmark after warmup, with synchronization
10. If using TensorRT or TensorRT-LLM, profile runtime separately from engine build

## Multi-GPU and NCCL playbook

Baseline expectations:

- launch with `torchrun`
- backend `nccl`
- one process per GPU
- clear `MASTER_ADDR`, `MASTER_PORT`, `RANK`, `WORLD_SIZE`, `LOCAL_RANK`

Parallelism heuristics:

- `DP` first for ordinary scale-out
- `FSDP2` when full replication is too expensive
- `FSDP / ZeRO-2 / ZeRO-3` before checkpointing when optimizer, grad, or param state replication is the memory bottleneck
- `TP + SP` for large transformer blocks
- `CP` for long-context models
- `PP` for deep stacks that still do not fit
- `EP` for MoE
- combine only what the bottleneck requires

Debugging rules:

- First-line NCCL debug:
  - `NCCL_DEBUG=INFO`
  - `NCCL_DEBUG_SUBSYS=COLL,GRAPH` when debugging hangs or topology issues
- If interface auto-detection is wrong, set `NCCL_SOCKET_IFNAME`
- Use `TORCH_NCCL_USE_COMM_NONBLOCKING=1` when you specifically want non-blocking NCCL error handling

Do not hardcode socket or thread tuning variables unless profiling or production evidence shows the default topology tuning is wrong.

## Custom CUDA / Triton kernel rules

Only drop to Triton or CUDA when operator fusion, layout cleanup, `torch.compile`, or library kernels are not enough.

For custom kernels:

- favor coalesced global memory access
- treat shared memory as a tool, not a reflex
- watch register pressure; occupancy is a means, not the target
- use block sizes that are multiples of 32
- start experiments around `128` to `256` threads per block unless the kernel shape clearly suggests otherwise
- avoid giant one-block-per-SM thinking; multiple resident blocks often help latency hiding
- measure spills, occupancy, achieved bandwidth, and kernel time before and after changes

Do not claim a kernel is faster because occupancy increased. Show end-to-end or kernel-level timing.

## Transformer Engine and FP8 rules

Use Transformer Engine when all of these are true:

- the workload is transformer-dominated
- the target GPUs are Hopper/Ada/Blackwell-class
- BF16 baseline is already correct
- you can run an accuracy gate

Rules:

- wrap only the forward pass in TE FP8 autocast
- use recipe-backed scaling, not home-grown FP8 metadata logic
- start with delayed scaling or hybrid FP8 recipes
- keep optimizer and master-weight behavior explicit
- if FP8 helps throughput but destabilizes training, fall back to BF16 instead of layering hacks

Prefer TE modules or established framework integration over custom FP8 plumbing.

## Attention and sequence-shape rules

For long-sequence transformer work:

- prefer fused attention over matmul-softmax-matmul Python compositions
- on H200/B200, actively test newer flash attention implementations when available instead of passively staying with the default SDPA stack
- prefer grouped or multi-query attention-aware fast paths when the model architecture already uses GQA or MQA
- prefer context parallelism and packed or varlen attention before wasting memory on blanket padding
- if custom masking is the only blocker, test FlexAttention before writing a new CUDA kernel

For decoder serving:

- KV cache layout is part of the algorithm, not just a storage detail
- paged KV and chunked context handling are first-class optimization choices
- scheduler choice affects TTFT and ITL, so benchmark serving algorithms at the scheduler level, not only kernel level

## Logging and metric collection rules

- Do not call `.item()` every step for loss curves, metric dashboards, or debug prints.
- Aggregate metrics on device and synchronize periodically:
  - every `N` steps
  - end of an accumulation window
  - end of an evaluation window
- If exact per-step host-visible metrics are required for debugging, state that this is a debug-only mode.
- Prefer batched reductions and detached device-side buffers over step-wise host sync.

## Data pipeline and prefetch rules

For CUDA training jobs, always inspect the input path before blaming kernels.

Required checks:

- `num_workers`
- `pin_memory`
- `persistent_workers`
- `prefetch_factor`
- CPU decode, tokenize, or augment cost
- storage throughput and remote filesystem latency

Rules:

- If GPU utilization dips between steps, inspect the dataloader before touching kernels.
- Tune `prefetch_factor` and worker count together; more workers without enough prefetch often just moves the bottleneck.
- Keep host preprocessing out of the critical path when possible.
- For very fast H100/H200/B200 training loops, assume untuned input pipelines are guilty until measurements say otherwise.

## Reproducibility and numerics rules

- Be explicit when a change trades accuracy for speed.
- cuDNN determinism is not guaranteed across architectures.
- Across devices or architectures, do not promise bitwise-identical outputs.
- If NaNs or Infs appear:
  - check data first
  - check loss scaling or dtype policy
  - check reduced-precision reductions
  - inspect unstable linalg paths

## Environment variable policy

Allowed as targeted tools, not blanket defaults:

- `CUDA_VISIBLE_DEVICES`
- `CUDA_LAUNCH_BLOCKING=1` for debugging only
- `PYTORCH_ALLOC_CONF`
- `TORCH_CUDNN_V8_API_LRU_CACHE_LIMIT`
- `TORCH_ALLOW_TF32_CUBLAS_OVERRIDE`
- `TORCH_NCCL_USE_COMM_NONBLOCKING=1`
- `NCCL_DEBUG`
- `NCCL_DEBUG_SUBSYS`
- `NCCL_SOCKET_IFNAME`

If you set an env var in code, config, or docs, explain:

1. why it is needed
2. whether it is for debugging, correctness, or performance
3. when it should be removed

## Review checklist

When reviewing or generating code in this domain, check for:

- tensors bouncing between CPU and GPU
- missing `pin_memory=True` on CUDA dataloaders
- missing `non_blocking=True` on pinned copies
- missing `persistent_workers=True` or untuned `prefetch_factor` on steady-state training jobs
- deprecated AMP API usage
- full FP32 training or inference on Hopper/Blackwell with no numerics justification
- FP16 used by default on Hopper with no reason
- no BF16 or FP8 path evaluation on H200/B200-class hardware
- no warmup in benchmarks
- no synchronize around timing
- `.item()` / `.cpu()` / `.numpy()` inside the step loop
- distributed code using non-NCCL backend for CUDA
- DDP used where model clearly does not fit, instead of FSDP2
- activation checkpointing used to paper over what should be FSDP or ZeRO sharding
- TP enabled without SP where the framework expects SP
- long-context workloads scaled by TP alone when CP is the better lever
- transformer stack on Hopper staying on unfused attention with no reason
- transformer stack on H200/B200 never testing newer flash attention implementations
- speculative decoding added with no acceptance-rate measurement
- quantization merged with no quality gate
- FP8 added without recipe-backed scaling or accuracy validation
- custom kernel work started before simpler wins were exhausted

## Output contract

When using this skill, report in this order:

1. runtime facts
2. bottleneck hypothesis
3. chosen optimization order
4. changes made
5. verification evidence
6. remaining risks

If you need deeper justification or exact source-backed tuning notes, read [references/official-notes.md](references/official-notes.md).
