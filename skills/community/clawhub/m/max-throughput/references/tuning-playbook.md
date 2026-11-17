# Tuning Playbook: Knobs That Actually Help

Prerequisites: run the profiling ladder first (`references/profiling.md`).
Every section below is keyed to a bottleneck class - do not apply knobs
blindly, and change ONE at a time.

Universal measurement snippet (throughput = the only tuning metric):

```python
import time, torch

def measure_items_per_sec(train_step, batch_size: int, warmup: int = 10, measured: int = 50) -> float:
    for _ in range(warmup):
        train_step()
    torch.cuda.synchronize()
    start = time.perf_counter()
    for _ in range(measured):
        train_step()
    torch.cuda.synchronize()
    return measured * batch_size / (time.perf_counter() - start)
```

## 1. Batch size (bottleneck: compute-bound or under-occupied)

Find the VRAM ceiling by doubling, then binary-search between the last fit
and first OOM; report peak memory as you go:

```python
for batch_size in [32, 64, 128, 256, 512]:
    try:
        torch.cuda.reset_peak_memory_stats()
        loss = train_a_few_steps(batch_size)   # 3-5 steps, with backward
        peak_gib = torch.cuda.max_memory_allocated() / 2**30
        print(f"batch={batch_size}: fits, peak {peak_gib:.1f} GiB")
    except torch.cuda.OutOfMemoryError:
        torch.cuda.empty_cache()
        print(f"batch={batch_size}: OOM")
        break
```

Then sweep throughput (`measure_items_per_sec`) over the feasible sizes and
pick the knee - typically the largest size whose items/s gain is > 5%.
Beyond the knee, larger batches waste VRAM and can hurt convergence.

Gotchas:

- Scale LR with global batch (linear rule as starting point) and add
  ~500-2000 warmup steps, or the speedup comes with a loss regression.
- BatchNorm prefers larger batches; very large batches can hurt
  small-dataset generalization - validate, don't just benchmark.
- Need a big global batch but VRAM-bound? Gradient accumulation:

```python
loss = loss / accumulation_steps
loss.backward()
if (step + 1) % accumulation_steps == 0:
    optimizer.step()
    optimizer.zero_grad(set_to_none=True)
```

## 2. DataLoader workers (bottleneck: input-pipeline starvation)

Method: benchmark the loader ALONE (profiling.md level 1), then:

- Start at 4-8 workers per GPU for heavy decode (JPEG/video),
  2-4 for light pipelines. Never exceed CPU cores / total GPUs.
- Sweep `[4, 8, 16]` and keep the point where dataloader-only throughput
  exceeds consumption by ~30% with the fewest workers. Diminishing returns
  or rising per-batch latency = stop.
- `cv2.setNumThreads(0)` inside dataset `__init__` - OpenCV's internal
  thread pool fights the DataLoader worker pool.
- Windows: `num_workers > 0` requires the training entry point guarded by
  `if __name__ == "__main__":`, and workers use spawn (slower startup) -
  `persistent_workers=True` matters even more there.

```python
DataLoader(
    dataset,
    batch_size=batch_size,
    num_workers=8,               # from the sweep above
    pin_memory=True,             # enables async H2D copy
    persistent_workers=True,     # no respawn every epoch
    prefetch_factor=4,           # default 2; raise if GPU still stalls
)
# and in the loop:
batch = batch.to("cuda", non_blocking=True)
```

## 3. Pre-encode / pre-tokenize (bottleneck: decode that workers can't absorb)

Do it when BOTH hold (from profiling):

1. dataloader-only throughput < consumption even at high `num_workers`;
2. py-spy shows decode/tokenize/augmentation hot frames.

Recipes by data type:

- Text/LLM: pre-tokenize the corpus ONCE, save packed uint16/int32 id
  shards (e.g. `np.memmap`), and memory-map at train time. This is standard
  practice - nobody tokenizes per-step at scale.
- Images: one-time pass that decodes + resizes to the training resolution
  and stores uint8 arrays (or WebDataset/FFCV shards). Decode of a raw
  array is ~10x cheaper than JPEG. Random crops/flips stay online (cheap);
  only the EXPENSIVE part (full-size JPEG decode, EXIF, giant resize) moves
  offline.
- Video: pre-extract per-clip frame tensors at target resolution/FPS.
- Audio: pre-compute spectrograms/waveform resamples.

Trade-offs to state explicitly before converting:

- Disk: expect 2-5x the raw size for uint8 tensors at training resolution.
- One-time conversion cost - run it with `parallel -j$(nproc)` (CPU
  playbook), and make it resumable (skip existing outputs).
- Augmentation flexibility: anything folded into the pre-encode is frozen;
  keep stochastic augs online and cheap.

## 4. Compute efficiency knobs (bottleneck: GPU-bound, util already ~100%)

Ordered by effort-to-payoff:

```python
torch.backends.cuda.matmul.allow_tf32 = True      # free on Ampere+
torch.backends.cudnn.benchmark = True             # fixed input sizes
model.to(memory_format=torch.channels_last)       # CNNs, often 10-30%
optimizer = torch.optim.AdamW(..., fused=True)    # fused optimizer step

scaler = torch.amp.GradScaler()                   # bf16 needs no scaler
with torch.autocast("cuda", dtype=torch.bfloat16):
    loss = model(batch)
# new-style:
model = torch.compile(model)                      # fusion, big for small models
```

Rough expectations: TF32 free, bf16 autocast 1.5-3x on tensor-core GPUs,
`torch.compile` 1.2-2x (best for many small ops), channels_last 1.1-1.4x
for CNNs. Measure each separately; some combinations conflict.

## 5. VRAM-bound knobs

- Gradient accumulation (see 1) - decouple global batch from micro-batch.
- `torch.utils.checkpoint` on the transformer/CNN blocks: ~30% VRAM saved
  for ~20-30% compute overhead - only when it unlocks a bigger batch.
- `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` for fragmentation OOM.
- Free cached tensors between phases (`optimizer.zero_grad(set_to_none=True)`).

## 6. When to stop

Re-measure after every single change. Stop when:

- the last change bought < 5% wall-clock, OR
- GPU util is sustained >= 90-95% and data wait ratio < 5%, OR
- you are about to break correctness/semantics for single-digit gains.

Then spend the remaining effort on launching MORE concurrent work instead
(`references/experiment-packing.md`) - utilization beats micro-optimization.
