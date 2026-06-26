# GPU Monitor Skill

Real-time GPU monitoring tool that works across platforms.

## Features

- ✅ Real-time GPU memory usage tracking
- ✅ Ollama model layer distribution (GPU/CPU)
- ✅ Cross-platform compatibility
- ✅ Configurable update interval
- ✅ Clean terminal output with tree-like formatting

## Quick Start

```bash
# Auto-start on launch
clawhub gpu-monitor --auto-start

# Manual run
clawhub gpu-monitor --interval=2
```

## Output Example

```
┌─[Update #1] 12:17:23
├─ GPU:         NVIDIA GeForce RTX 3080
├─ Memory Used: 8.5/10.0 GB (85.0%)
├─ Log Time:    [实时模式 - 无层数数据]
├─ GPU Layers:  [实时模式]
```

## Dependencies

- Python 3.7+
- `nvidia-smi` (NVIDIA GPUs)
- Optional: Ollama server for layer tracking

## License

MIT
