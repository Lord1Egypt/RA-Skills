#!/usr/bin/env bash
# Inspect local compute resources (Linux/macOS) and recommend a parallel plan.
# Lightweight alternative to inspect_resources.py for headless training boxes.

set -euo pipefail

line() { printf '%s\n' "--------------------------------------------------------------"; }

logical_cores() {
    if command -v nproc >/dev/null 2>&1; then
        nproc
    else
        sysctl -n hw.ncpu
    fi
}

physical_cores() {
    if command -v lscpu >/dev/null 2>&1; then
        lscpu | awk '/^Core\(s\) per socket/ {c=$4} /^Socket\(s\)/ {s=$2} END {print c*s}'
    else
        sysctl -n hw.physicalcpu
    fi
}

ram_info() {
    if command -v free >/dev/null 2>&1; then
        free -h | awk 'NR<=2'
    else
        echo "total: $(( $(sysctl -n hw.memsize) / 1024 / 1024 / 1024 )) GB"
    fi
}

echo "=============================================================="
echo "RESOURCE REPORT"
echo "=============================================================="
echo "OS:      $(uname -srm)"
echo "CPU:     $(lscpu 2>/dev/null | awk -F': +' '/Model name/ {print $2; exit}' || sysctl -n machdep.cpu.brand_string 2>/dev/null || echo unknown)"
echo "Cores:   $(physical_cores) physical / $(logical_cores) logical"
echo "RAM:"
ram_info | sed 's/^/  /'

if command -v nvidia-smi >/dev/null 2>&1; then
    echo "GPUs:"
    nvidia-smi --query-gpu=index,name,memory.total,memory.free,utilization.gpu \
        --format=csv,noheader | sed 's/^/  /'
    free_gpus=$(nvidia-smi --query-gpu=index,memory.free --format=csv,noheader,nounits \
        | awk -F', ' '$2 > 1024 {printf "%s ", $1}')
    gpu_count=$(echo $free_gpus | wc -w)
else
    echo "GPUs:    (nvidia-smi not found)"
    free_gpus=""
    gpu_count=0
fi

workers=$(( $(logical_cores) * 3 / 4 ))
[ "$workers" -lt 1 ] && workers=1

line
echo "RECOMMENDED EXECUTION PLAN"
line
echo "CPU workers (build/pytest/proc): $workers"
if [ "$gpu_count" -gt 1 ]; then
    echo "Free GPUs:                       $free_gpus"
    echo "Multi-GPU launch:                torchrun --standalone \\"
    echo "                                     --nproc_per_node=$gpu_count train.py"
elif [ "$gpu_count" -eq 1 ]; then
    echo "Free GPUs:                       $free_gpus"
else
    echo "Free GPUs:                       none"
fi
echo "DataLoader num_workers per GPU:  $(( $(logical_cores) / (gpu_count > 0 ? gpu_count : 1) )) (cap at 8)"
echo "Multi-process jobs:              export OMP_NUM_THREADS=1 per worker"
echo "=============================================================="
