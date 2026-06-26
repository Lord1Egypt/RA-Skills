# GPU Monitor - Ollama Real-time GPU Monitoring Skill

## Overview

This skill provides real-time GPU monitoring for local **Ollama** models. It monitors:

- GPU name and memory usage with utilization percentage (e.g., 8.5/10.0 GB = 85%)
- Model layer distribution (GPU vs CPU offloading) via Ollama server.log parsing
- Live status updates every 2 seconds

**⚠️ Framework Dependency**: This skill is specifically designed for the **Ollama framework** (https://ollama.ai).  
**📝 Log Requirement**: Requires access to Ollama's `server.log` file at a configurable path to parse model layer information.

## Features

✅ **Ollama-specific monitoring**: Automatically parses `server.log` for model info when available  
✅ **Layer distribution tracking**: Shows GPU layers, total layers, and CPU offload percentage  
✅ **Memory visualization**: Displays memory used/total with real-time utilization %  
✅ **Cross-platform**: Works on Windows/Linux/macOS with NVIDIA GPUs via nvidia-smi  
✅ **Real-time updates**: Configurable refresh interval (default: 2 seconds)  
✅ **Flexible configuration**: Specify Ollama log path via CLI `--ollama-log=PATH` or config file  
✅ **Graceful degradation**: Shows GPU metrics even without Ollama installed  

## Installation

```bash
# Via ClawHub
clawhub install gpu-monitor-skill

# Or manual clone
git clone <repository-url> ~/.openclaw/skills/gpu-monitor
```

## Usage (Local Testing)

```bash
# Basic usage - monitors local GPU
python ~/.openclaw/clawhub/gpu-monitor-skill/gpu_monitor.py --interval=3

# With Ollama log path for layer tracking
python ~/.openclaw/clawhub/gpu-monitor-skill/gpu_monitor.py \
    --ollama-log="C:\Users\zugzwang\AppData\Local\Ollama\server.log" \
    --interval=2

# Using config file (create ~/.openclaw/gpu_monitor_config.json)
{
  "update_interval_seconds": 2,
  "ollama_log_path": "/path/to/server.log",
  "quiet_mode": false
}
```

## Configuration

Create `~/.openclaw/gpu_monitor_config.json`:

```json
{
  "update_interval_seconds": 2,
  "ollama_log_path": "/path/to/Ollama/server.log",
  "quiet_mode": false
}
```

| Field | Type | Description |
|-------|------|-------------|
| `update_interval_seconds` | int | Refresh interval (default: 2) |
| `ollama_log_path` | string | Path to Ollama server.log (optional) |
| `quiet_mode` | bool | Disable banner messages |

## Output Examples

### With Ollama Layer Info

```
┌─[Update #1] 12:30:45
├─ GPU:         NVIDIA GeForce RTX 3080
├─ Memory Used: 8.5/10.0 GB (85.0%)
├─ Log Time:    [实时模式 - 无层数数据]
├─ GPU Layers:  [实时模式]
```

### With Layer Data

```
┌─[Update #1] 12:31:02
├─ GPU:         NVIDIA GeForce RTX 3080
├─ Memory Used: 7.2/10.0 GB (72.0%)
├─ Log Time:    time=2026-03-27T12:31:02+08:00
├─ GPU Layers:  32 / 33
├─ CPU Layers:  1 (3.0%)
```

### Without Ollama

```
┌─[Update #1] 12:32:15
├─ GPU:         NVIDIA GeForce RTX 3080
├─ Memory Used: 9.2/10.0 GB (92.0%)
├─ Log Time:    [实时模式 - 无层数数据]
├─ GPU Layers:  [实时模式]
```

## Prerequisites

- **Python 3.7+**
- **NVIDIA GPU** with `nvidia-smi` available (Windows/Linux/macOS)
- **(Optional)** Ollama server for layer tracking

## License

MIT License
