# jetson-cuda

NVIDIA Jetson CUDA 工具集。提供 CUDA 版本查询、GPU 设备信息等功能。

## 功能

- CUDA 版本查询 (nvcc --version)
- GPU 设备信息 (nvidia-smi)
- CUDA 库路径

## 使用方法

```bash
# 查看 CUDA 信息
jetson-cuda info

# 检查 nvcc
which nvcc
nvcc --version
```

## 依赖

- CUDA Toolkit
- nvidia-smi

## 环境要求

- NVIDIA Jetson (AGX Orin, Xavier, Nano, etc.)
- CUDA 11.x or 12.x
