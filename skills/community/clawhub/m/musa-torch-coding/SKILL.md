---
name: musa-torch-coding
description: Transcribe audio via OpenAI Audio Transcriptions API (Whisper).
homepage: https://platform.openai.com/docs/guides/speech-to-text
metadata:
  {
    "openclaw":
      {
        "emoji": "☁️",
        "requires": { "bins": ["curl"], "env": ["OPENAI_API_KEY"] },
        "primaryEnv": "OPENAI_API_KEY",
      },
  }
---
# MUSA Torch Coding

Guide for generating PyTorch code that runs on Moore Threads (摩尔线程) MUSA GPUs using torch_musa.

## Overview

MUSA (Metaverse Unified System Architecture) is Moore Threads' GPU computing platform. This skill helps generate code that:

- Runs on Moore Threads GPUs via `torch_musa`
- Converts CUDA code to MUSA-compatible code
- Sets up proper environments (conda v1.2/v1.3)
- Follows MUSA best practices

## Key Differences: CUDA vs MUSA


| CUDA                           | MUSA                           |
| ------------------------------ | ------------------------------ |
| `torch.cuda`                   | `torch.musa`                   |
| `torch.device("cuda")`         | `torch.device("musa")`         |
| `torch.cuda.is_available()`    | `torch.musa.is_available()`    |
| `backend='nccl'`               | `backend='mccl'`               |
| `torch.cuda.device_count()`    | `torch.musa.device_count()`    |
| `torch.cuda.get_device_name()` | `torch.musa.get_device_name()` |

## Environment Setup

### ⚠️ Important: MUSA Uses Pre-configured Conda Environments

**DO NOT install PyTorch, vLLM, or related packages manually.** MUSA environments are **custom-built** and include:

- MUSA-specific PyTorch builds (not compatible with standard PyTorch)
- MUSA-customized vLLM versions
- MUSA drivers and SDK integration

Installing standard packages from PyPI will break the environment.

### Conda Environment (v1.2/v1.3)

MUSA provides pre-configured conda environments. Common environment names:

- `v1.2` - MUSA SDK v1.2 environment
- `v1.3` - MUSA SDK v1.3 environment (newer)

```bash
# List available MUSA environments
conda env list | grep -E "(v1\.2|v1\.3|musa)"

# Activate the appropriate environment
conda activate v1.2  # or v1.3

# Verify MUSA availability
python -c "import torch_musa; import torch; print(torch.musa.is_available())"
```

### Environment Detection & Setup

If no MUSA conda environment is detected:

1. **Check if MUSA is installed:**

   ```bash
   which musaInfo  # Should show musaInfo path
   ls /usr/local/musa/  # MUSA SDK location
   ```
2. **If MUSA is not set up:**

   - **Use the `musa-env-setup` skill** for complete environment installation
   - The skill covers SDK installation, conda setup, and vLLM-MUSA configuration
3. **Common conda environment locations:**

   - `/opt/conda/envs/`
   - `~/conda/envs/`
   - `/usr/local/conda/envs/`

### Key Environment Variables


| Variable                       | Purpose                   |
| ------------------------------ | ------------------------- |
| `MUSA_VISIBLE_DEVICES=0,1,2,3` | Control visible GPU IDs   |
| `MUSA_LAUNCH_BLOCKING=1`       | Synchronous kernel launch |
| `MUDNN_LOG_LEVEL=INFO`         | Enable MUDNN logging      |
| `TORCH_SHOW_CPP_STACKTRACES=1` | Show C++ stack traces     |

## Code Generation Rules

When generating PyTorch code for MUSA:

1. **Always import torch_musa**

   ```python
   import torch_musa  # Must import before using torch.musa
   ```
2. **Use torch.device("musa")**

   ```python
   device = torch.device("musa") if torch.musa.is_available() else torch.device("cpu")
   tensor = torch.tensor([1.0, 2.0], device=device)
   ```
3. **Use 'mccl' for distributed training**

   ```python
   dist.init_process_group(backend='mccl', ...)
   ```
4. **Mixed precision (AMP) is supported**

   ```python
   from torch.cuda.amp import autocast, GradScaler  # Same API
   ```
5. **TensorCore optimization available**

   - Set `torch.backends.musa.matmul.allow_tf32 = True` for TensorFloat32

## Model Templates

For common model types, see templates in `references/`:

- `reference.md` - Complete MUSA API reference

## Common Tasks

### Check GPU Availability

```python
import torch
import torch_musa

print(f"MUSA available: {torch.musa.is_available()}")
print(f"Device count: {torch.musa.device_count()}")
print(f"Device name: {torch.musa.get_device_name(0)}")
```

### Training Loop Pattern

```python
import torch_musa

# Device setup
device = torch.device("musa") if torch.musa.is_available() else torch.device("cpu")

# Model and data to device
model = model.to(device)
inputs = inputs.to(device)

# Training (same as CUDA)
optimizer.zero_grad()
outputs = model(inputs)
loss = criterion(outputs, targets)
loss.backward()
optimizer.step()
```

### Distributed Training (DDP)

```python
import torch.distributed as dist
import torch_musa

# Initialize with mccl backend
dist.init_process_group(backend='mccl', rank=rank, world_size=world_size)

# Create process group on MUSA
torch.cuda.set_device(local_rank)  # torch_musa extends torch.cuda API
```

## Code Conversion

When converting existing CUDA code to MUSA:

1. Add `import torch_musa` at the top
2. Replace `cuda` with `musa` in device strings
3. Replace `nccl` with `mccl` for distributed backend
4. Keep all other PyTorch API calls unchanged

## Troubleshooting

- **Device not found**: Ensure user is in `render` group: `sudo usermod -aG render $(whoami)`
- **Library not found**: Check `LD_LIBRARY_PATH` includes `/usr/local/musa/lib/`
- **Build issues**: Clean and rebuild: `python setup.py clean && bash build.sh`
- **Docker issues**: Use `--env MTHREADS_VISIBLE_DEVICES=all`

## Reference

For detailed API reference and examples, see [references/reference.md](references/reference.md).
