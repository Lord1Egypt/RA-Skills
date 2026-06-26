#!/bin/bash
echo "=== CUDA Info ==="
nvcc --version 2>/dev/null || echo "CUDA not found"
nvidia-smi 2>/dev/null || echo "nvidia-smi not found"
