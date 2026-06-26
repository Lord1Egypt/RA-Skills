---
name: musify
description: Convert CUDA code to MUSA (Moore Threads GPU) using the musify tool. Use when migrating CUDA codebases to MUSA platform, converting CUDA kernels/APIs to MUSA equivalents, or porting NVIDIA GPU code to Moore Threads GPUs. Supports batch conversion of .cu, .cuh, .cpp, .h files with text-based API mapping.
---

# Musify - CUDA to MUSA Code Conversion

Musify converts CUDA code to MUSA (Moore Threads GPU architecture) using text-based API mapping.

## Installation

```bash
# Install dependencies
pip install ahocorapy

# musify-text should be available in MUSA toolkit
```

## Basic Usage

```bash
# Convert files in-place (CUDA -> MUSA)
musify-text --inplace -- file1.cu file2.cpp

# Convert and create new files (default)
musify-text --create -- a.cu b.cpp

# Print to stdout
musify-text -t -- file.cu
```

## Batch Conversion

```bash
# Find and convert all CUDA/C++ files in directory
musify-text --inplace -- $(find /path/to/project -name '*.cu' -o -name '*.cuh' -o -name '*.cpp' -o -name '*.h')

# Using ripgrep (recommended)
musify-text --inplace -- $(rg --files -g '*.cu' -g '*.cuh' -g '*.cpp' -g '*.h' /path/to/project)
```

## Options

| Option | Description |
|--------|-------------|
| `-t, --terminal` | Print output to stdout |
| `-c, --create` | Create new files with converted code (default) |
| `-i, --inplace` | Modify files in-place |
| `-d {c2m,m2c}` | Conversion direction: c2m (CUDA→MUSA, default), m2c (MUSA→CUDA) |
| `-m <file.json>` | Custom API mapping file (can specify multiple) |
| `--clear-mapping` | Clear default mapping, use only custom mappings |
| `-l {DEBUG,INFO,WARNING}` | Log level |

## Exclusion Markers

Prevent specific code sections from being converted:

```c
// MUSIFY_EXCL_LINE - Exclude this line
char *str = "cudaMalloc"; // MUSIFY_EXCL_LINE

// MUSIFY_EXCL_START - Start exclusion block
char *apis[] = {
    "cudaInit",
    "cudaFree"
};
// MUSIFY_EXCL_STOP - End exclusion block
```

## Common CUDA → MUSA Mappings

| CUDA | MUSA |
|------|------|
| `cuda` prefix | `musa` prefix |
| `CUDA` | `MUSA` |
| `cu` prefix (driver API) | `mu` prefix |
| `__cuda` | `__musa` |
| `cudaMalloc` | `musaMalloc` |
| `cudaFree` | `musaFree` |
| `cudaMemcpy` | `musaMemcpy` |
| `cudaLaunchKernel` | `musaLaunchKernel` |
| `__global__` | `__global__` (unchanged) |
| `__device__` | `__device__` (unchanged) |
| `__shared__` | `__shared__` (unchanged) |

## Workflow

1. **Backup code** before conversion
2. **Run musify** on target files
3. **Review changes** - text-based conversion may need manual fixes
4. **Compile with MUSA compiler** (`mcc`) to verify
5. **Test on MUSA device**

## References

- [Musify Blog Post](https://blog.mthreads.com/blog/musa/2024-05-28-使用musify对代码进行平台迁移/)
- [MUSA Documentation](https://docs.mthreads.com/)
- [Tutorial on MUSA](https://github.com/MooreThreads/tutorial_on_musa)