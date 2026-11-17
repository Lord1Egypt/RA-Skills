# Profiling Playbook: Find the REAL Bottleneck

Tuning without profiling is guessing. Work down this ladder and stop at the
first level that explains the symptom - each level is cheaper than the next.

## Level 0: Utilization triage (30 seconds)

While the job runs in its steady phase:

```bash
python scripts/quick_triage.py --duration 60
```

Read the GPU utilization PATTERN, not just the average:

| Pattern | Meaning |
|---|---|
| Flat 90-100% | compute-bound; job is healthy, tune efficiency (level 3) |
| Sawtooth 0% <-> 100% | GPU repeatedly waits for data: input pipeline starvation |
| Flat < 30% with high CPU | decode/tokenize eating cores: data pipeline CPU-bound |
| Flat < 30% with low CPU | job too small for the GPU, I/O blocked, or serialized host code |
| One GPU busy, rest idle | no DDP / no packing - a launch problem, not a perf problem |

## Level 1: Isolate the data pipeline (2 minutes)

Measure dataloader-only throughput and compare with the training loop's
consumption rate (batch_size x steps/s from logs):

```python
import time

def benchmark_dataloader(loader, batches: int = 200) -> float:
    iterator = iter(loader)
    next(iterator)  # warm-up: workers spin up, caches fill
    start = time.perf_counter()
    for _ in range(batches):
        next(iterator)
    elapsed = time.perf_counter() - start
    items_per_sec = batches * loader.batch_size / elapsed
    print(f"dataloader-only: {items_per_sec:.0f} items/s")
    return items_per_sec
```

Interpretation:

- dataloader-only >= ~1.3x consumption -> data pipeline is fine; look at GPU
  efficiency instead (level 3).
- dataloader-only < consumption -> confirmed input starvation. Tune workers
  (tuning-playbook.md) or pre-encode.
- dataloader-only fast but training still starves -> the bottleneck is in
  the training step itself: per-step `.item()`/`print(tensor)` syncs,
  CPU-side metrics, `non_blocking` misuse.

## Step-time decomposition (drop into any training loop)

```python
import time

data_total = compute_total = 0.0
for epoch in range(epochs):
    for batch in loader:
        torch.cuda.synchronize()
        step_start = time.perf_counter()
        batch = batch.to("cuda", non_blocking=True)
        torch.cuda.synchronize()
        data_total += time.perf_counter() - step_start

        compute_start = time.perf_counter()
        loss = train_step(batch)
        torch.cuda.synchronize()
        compute_total += time.perf_counter() - compute_start

print(f"data wait: {data_total:.1f}s   compute: {compute_total:.1f}s   "
      f"ratio: {data_total / (data_total + compute_total):.0%}")
```

data ratio > 20% = the pipeline is stealing a fifth of your wall clock.

## Level 2: Python-level sampling with py-spy (5 minutes)

Finds WHERE the CPU time goes (decode? tokenization? numpy copies? GIL
contention?) without modifying code:

```bash
pip install py-spy
py-spy top --pid <TRAINING_PID>            # live hotspot view
py-spy record -o profile.svg --pid <TRAINING_PID> -d 60   # flame graph
```

Typical findings and their fixes:

| Hot frame | Fix |
|---|---|
| `PIL/Image.decode`, `cv2.imread`, jpeglib | pre-encode to raw tensors, or DALI/FFCV |
| `tokenizer(...)`, `pack_dataset` | pre-tokenize once, memory-map the cache |
| albumentations / torchvision transforms | fewer/cheaper augs, GPU-side augs (Kornia), or fold into pre-encode |
| `torch.Tensor.item()`, `.cpu()`, `print(tensor)` | remove per-step syncs; log every N steps |
| `cv2.setNumThreads` absent -> workers thrash | `cv2.setNumThreads(0)` in dataset `__init__` |
| main-process work between steps | move metric computation off the hot path |

## Level 3: Op/kernel-level with torch.profiler

```python
from torch.profiler import profile, ProfilerActivity

with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA]) as prof:
    for _ in range(20):
        train_step(batch)
prof.export_chrome_trace("trace.json")     # open in chrome://tracing
print(prof.key_averages().table(sort_by="cuda_time_total", row_limit=15))
```

What the trace tells you:

| Signature | Cause | Fix |
|---|---|---|
| wide gaps between kernel clusters | host-side work / dataloader on the hot path | workers, pin_memory, remove syncs |
| hundreds of tiny kernels, launch-bound | model too small per op | bigger batch, `torch.compile` (fusion), CUDA graphs |
| long `Memcpy HtoD` blocks | pageable host memory | `pin_memory=True`, `non_blocking=True` |
| one kernel = 100% of GPU time | that op IS the model; check its efficiency | AMP, fused impl, kernel-specific tuning |
| `cudaStreamSynchronize` frequently | hidden syncs (metrics, asserts, `.item()`) | remove from hot path |

## Level 4: System-level

- Disk I/O: `iostat -x 1` (Linux) / Task Manager (Windows). Read throughput
  pinned at disk limit -> cache locally on NVMe, use sharded/tar formats
  (WebDataset), or pre-encode.
- CUDA kernels: `nsys profile python train.py` (Nsight Systems) for the
  timeline; `ncu` (Nsight Compute) for a single kernel's efficiency.
- PCIe/NVLink transfers: `nvidia-smi dmon -s t` during training; heavy DtoH
  traffic means something is being pulled back to host per-step.

## Discipline

- Measure the STEADY state; skip warm-up (first iterations compile caches,
  spin up workers).
- Report medians/means over >= 50 steps, not single iterations.
- Change one knob, re-measure, keep or revert. Two changes at once tell you
  nothing if the result is ambiguous.
- Stop tuning when a change buys < 5% - your remaining time is better spent
  on the next bottleneck or the next experiment.
