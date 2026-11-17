# PyTorch Multi-GPU Playbook

How to launch PyTorch work so that all available GPUs are actually used.

## Single training job, multiple GPUs (DDP)

Never launch multi-GPU-capable training as `python train.py`. Convert it to
DistributedDataParallel and launch with torchrun:

```bash
torchrun --standalone --nproc_per_node=8 train.py
```

Minimal code changes required in `train.py`:

```python
import torch
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data import DataLoader, DistributedSampler

def main():
    dist.init_process_group(backend="nccl")
    local_rank = int(os.environ["LOCAL_RANK"])
    torch.cuda.set_device(local_rank)

    model = build_model().to(local_rank)
    model = DDP(model, device_ids=[local_rank])

    sampler = DistributedSampler(train_dataset, shuffle=True)
    loader = DataLoader(
        train_dataset,
        batch_size=per_gpu_batch_size,  # global batch = this * world_size
        sampler=sampler,               # NOT shuffle=True together with sampler
        num_workers=num_workers_per_gpu,
        pin_memory=True,
        persistent_workers=True,
    )
    # ... standard training loop; call sampler.set_epoch(epoch) each epoch ...
```

- Set `OMP_NUM_THREADS=1` (torchrun warns and defaults sensibly, but set it
  explicitly) so each process does not spawn `nproc` intra-op threads.
- Scale learning rate with global batch size (linear scaling rule as a
  starting point, warmup helps).
- Checkpoint only from rank 0; guard logging/printing with
  `if dist.get_rank() == 0`.

## When the model does not fit on one GPU

Use FSDP (or DeepSpeed ZeRO-2/3). FSDP shards parameters/optimizer states
across GPUs:

```bash
torchrun --standalone --nproc_per_node=8 train_fsdp.py
```

Prefer `ShardingStrategy.FULL_SHARD` for the largest models,
`SHARD_GRAD_OP` when communication overhead dominates.

## Multiple independent jobs (sweeps, seeds, evals)

If you have more independent jobs than GPUs, do NOT queue them serially.
Pack one job per GPU:

```bash
CUDA_VISIBLE_DEVICES=0 python eval.py --config exp_a.yaml &
CUDA_VISIBLE_DEVICES=1 python eval.py --config exp_b.yaml &
CUDA_VISIBLE_DEVICES=2 python eval.py --config exp_c.yaml &
CUDA_VISIBLE_DEVICES=3 python eval.py --config exp_d.yaml &
wait
```

Notes:

- Always set `CUDA_VISIBLE_DEVICES` explicitly; relying on defaults causes
  two jobs to land on the same GPU.
- Run each job single-GPU (`device="cuda:0"` inside its own visible world).
- If VRAM allows (small models on A100/H100), co-locate 2+ jobs per GPU,
  but watch for compute contention: two jobs sharing one GPU can be slower
  than one at a time if both are compute-bound.

## Diagnosing an under-utilized run

| Symptom | Likely cause | Fix |
|---|---|---|
| GPU util spiky 0% <-> 100% | DataLoader starvation | raise `num_workers`, `pin_memory=True`, `persistent_workers=True` |
| GPU util ~100% but slow epoch vs expected | model too small / kernel launch overhead | larger batch, `torch.compile`, CUDA graphs, or pack more jobs per GPU |
| Only GPU 0 busy | forgot DDP, plain `python train.py` | switch to torchrun launch |
| All GPUs busy but jobs sequential | script loops configs serially | refactor to per-GPU concurrent packing (above) |
| VRAM OOM at start | batch too large / fragmentation | `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`, gradient checkpointing, smaller batch + grad accumulation |

Quick utilization check during a run:

```bash
watch -n 1 nvidia-smi
# or per-process view:
nvidia-smi pmon -s um
```
