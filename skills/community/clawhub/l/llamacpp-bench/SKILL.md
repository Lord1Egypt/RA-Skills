---
name: llamacpp-bench
description: Run llama.cpp benchmarks on GGUF models to measure prompt processing (pp) and token generation (tg) performance. Use when the user wants to benchmark LLM models, compare model performance, test inference speed, or run llama-bench on GGUF files. Supports Vulkan, CUDA, ROCm, and CPU backends.
---

# llamacpp-bench

Run standardized benchmarks on GGUF models using llama.cpp's `llama-bench` tool.

## Quick Start

```bash
# Basic benchmark
llama-bench -m model.gguf -p 512,1024,2048 -n 128,256 -ngl 99

# With specific backend
LLAMA_BACKEND=vulkan llama-bench -m model.gguf -p 512,1024,2048 -n 128,256 -ngl 99
```

## Benchmark Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `-m` | Model path (GGUF file) | required |
| `-p` | Prompt sizes to test | 512 |
| `-n` | Generation lengths to test | 128 |
| `-ngl` | GPU layers to offload | 99 |
| `-t` | CPU threads | auto |
| `-dev` | Device selection | auto |

## Standard Test Suite

For consistent comparisons across models, use:

```bash
-p 512,1024,2048 -n 128,256 -ngl 99
```

This tests:
- **Prompt processing**: 512, 1024, 2048 tokens
- **Token generation**: 128, 256 tokens

## Interpreting Results

| Metric | Meaning | Good Performance |
|--------|---------|------------------|
| `pp512` | Prompt processing speed at 512 tokens | >1000 t/s |
| `pp1024` | Prompt processing speed at 1024 tokens | >1000 t/s |
| `pp2048` | Prompt processing speed at 2048 tokens | >1000 t/s |
| `tg128` | Token generation speed (128 tokens) | >50 t/s |
| `tg256` | Token generation speed (256 tokens) | >50 t/s |

## Backend Selection

llama-bench auto-detects available backends. Priority order:
1. CUDA (NVIDIA GPUs)
2. ROCm (AMD GPUs)
3. Vulkan (cross-platform GPU)
4. CPU (fallback)

To force a backend, set environment variable or check build:
```bash
# Check available backends
llama-bench --help | grep -i "backend\|cuda\|rocm\|vulkan"
```

## Batch Benchmarking

Use the provided script for benchmarking multiple models:

```bash
./scripts/benchmark_models.sh /path/to/models/*.gguf
```

## Saving Results

Output can be redirected to a file:
```bash
llama-bench -m model.gguf -p 512,1024,2048 -n 128,256 -ngl 99 > results.txt
```

Or use the benchmark script which auto-saves to timestamped files.

## Common Issues

1. **Out of memory**: Reduce `-ngl` (GPU layers) or test smaller prompt sizes
2. **Slow CPU performance**: Ensure `-t` matches CPU core count
3. **Backend not found**: Check llama.cpp was built with the desired backend

## Building / Updating llama.cpp

### Check Current Version

```bash
./scripts/build_llamacpp.sh -v
```

Shows:
- Current Git commit and branch
- Build date
- Whether behind upstream
- Available backends

### Build or Update

```bash
# Interactive mode (prompts for backend selection)
./scripts/build_llamacpp.sh -u

# Specify backend directly
./scripts/build_llamacpp.sh -u -b vulkan   # Vulkan (AMD/Intel GPUs)
./scripts/build_llamacpp.sh -u -b cuda     # CUDA (NVIDIA GPUs)
./scripts/build_llamacpp.sh -u -b rocm     # ROCm (AMD GPUs)
./scripts/build_llamacpp.sh -u -b cpu      # CPU only

# Clean rebuild
./scripts/build_llamacpp.sh -c -b vulkan

# Custom build directory
./scripts/build_llamacpp.sh -u -b cuda -d /custom/path
```

### Build Options

| Flag | Description |
|------|-------------|
| `-v` | Show version info and exit |
| `-u` | Update to latest from GitHub |
| `-c` | Clean build (remove existing) |
| `-b` | Backend: vulkan, cuda, rocm, cpu |
| `-d` | Build directory path |
| `-j` | Parallel jobs (default: CPU count) |

## Finding llama-bench

The benchmark script auto-detects llama-bench in these locations:
- `/DATA/Benchmark/llama.cpp/build/bin/llama-bench`
- `~/Repo/llama.cpp/build/bin/llama-bench`
- `~/lab/build/bin/llama-bench`

If not found, it will search your home directory or you can build it using the script above.
