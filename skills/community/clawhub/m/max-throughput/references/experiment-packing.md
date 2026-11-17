# Experiment Packing on Multi-GPU Machines

How to schedule many independent runs (sweeps, seeds, ablations, evals) so
total wall-clock time is minimized.

## The decision tree

```
How many independent jobs J, how many free GPUs G?

J == 1 and code supports data parallelism
    -> DDP/torchrun across all G GPUs

J <= G
    -> one job per GPU, all launched concurrently,
       each with CUDA_VISIBLE_DEVICES pinned

J > G
    -> GPU job queue: G workers, each pulls the next job when its GPU
       frees up (see GNU parallel template below)

Any job needs > 1 GPU (single large model, no FSDP)
    -> give that job a contiguous GPU subset via CUDA_VISIBLE_DEVICES=2,3
       and DDP inside; schedule around it
```

## GNU parallel job queue (recommended for J > G)

```bash
cat > job_list.txt <<'EOF'
CUDA_VISIBLE_DEVICES=0_gpu_tag python train.py --seed 1
CUDA_VISIBLE_DEVICES=0_gpu_tag python train.py --seed 2
CUDA_VISIBLE_DEVICES=0_gpu_tag python train.py --seed 3
EOF
# replace 0_gpu_tag with per-slot GPU ids via --jobs + env, or simpler:
seq 1 32 | parallel -j 8 'CUDA_VISIBLE_DEVICES=$(( ({%} - 1) % 8 )) python train.py --seed {}'
```

`-j 8` keeps 8 jobs running; `{%}` is the job slot (1..8), so
`(slot-1) % n_gpus` pins each slot to a stable GPU. As soon as one job
finishes the next starts - no GPU ever idles waiting for a human.

Simple pure-Python scheduler equivalent:

```python
import subprocess

gpu_jobs = {gpu_index: job_queue for gpu_index in range(num_gpus)}
# pop next job per free GPU, subprocess.Popen with
# env={"CUDA_VISIBLE_DEVICES": str(gpu_index)}, reap finished, refill.
```

## VRAM-based co-location

When jobs are small relative to VRAM (e.g. 2 GB jobs on 80 GB cards),
co-locate `floor(free_vram / job_vram)` jobs per GPU. Prefer NVIDIA MPS for
true concurrent kernels:

```bash
nvidia-cuda-mps-control -d   # start MPS daemon once
```

Without MPS, processes time-slice the GPU: still better than idling, but
not additive throughput for compute-bound jobs.

## Sequencing gotchas

- Random seeds: verify each job actually differs (config, seed, data
  shard). Copy-paste launches that run the same config 8 times waste the
  whole machine.
- Shared output paths: concurrent jobs writing the same file corrupt
  results. Give each job its own `--output_dir` (include GPU/slot/seed).
- CPU side: 8 concurrent training jobs x 4 dataloader workers = 32 CPU
  workers; make sure that fits core count, else reduce num_workers.
- Checkpoint/resume: with a job queue, add per-job try/except so one crash
  does not idle its GPU; log failures for a requeue pass.

## Verify the packing worked

```bash
nvidia-smi --query-gpu=index,utilization.gpu,memory.used --format=csv -l 5
```

All G GPUs near 100% util = good. Some GPUs idle while jobs queue = the
scheduler is serial somewhere; fix the loop, do not just wait.
