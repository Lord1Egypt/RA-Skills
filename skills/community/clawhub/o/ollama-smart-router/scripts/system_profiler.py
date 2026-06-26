#!/usr/bin/env python3
"""
System profiler - detect hardware capabilities and map to compatible Ollama models.
Prevents trying to run models that exceed available resources.
"""

import os
import re
import subprocess
import json
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

@dataclass
class SystemSpecs:
    total_ram_gb: float
    available_ram_gb: float
    gpu_vram_gb: Optional[float]
    gpu_name: Optional[str]
    cpu_cores: int
    is_gpu_available: bool
    
    def __str__(self):
        gpu_info = f"{self.gpu_name} ({self.gpu_vram_gb:.1f}GB VRAM)" if self.is_gpu_available else "No GPU"
        return f"RAM: {self.total_ram_gb:.1f}GB total / {self.available_ram_gb:.1f}GB available | {gpu_info} | CPU: {self.cpu_cores} cores"

# Model requirements: (parameters, min_vram_gb, min_ram_gb, description)
MODEL_REQUIREMENTS = {
    # Small models - run on CPU with 8GB+ RAM
    "llama3.2:1b": (1, 0, 4, "Tiny - runs on almost anything"),
    "llama3.2:3b": (3, 0, 6, "Small - runs on CPU"),
    "llama3.2": (8, 6, 10, "Standard 8B - needs GPU for speed"),
    "llama3.2:8b": (8, 6, 10, "Standard 8B - needs GPU for speed"),
    
    # Medium models - need GPU
    "llama3.1:8b": (8, 6, 10, "Llama 3.1 8B"),
    "llama3.1:70b": (70, 40, 48, "Llama 3.1 70B - needs serious GPU"),
    "qwen2.5:7b": (7, 6, 10, "Qwen2.5 7B"),
    "qwen2.5:14b": (14, 10, 16, "Qwen2.5 14B"),
    "qwen2.5:32b": (32, 20, 32, "Qwen2.5 32B"),
    "mistral:7b": (7, 6, 10, "Mistral 7B"),
    "mixtral:8x7b": (47, 28, 48, "Mixtral 8x7B - needs big GPU"),
    
    # Code models
    "codellama:7b": (7, 6, 10, "CodeLlama 7B"),
    "codellama:13b": (13, 10, 16, "CodeLlama 13B"),
    "codellama:34b": (34, 24, 40, "CodeLlama 34B - needs big GPU"),
    
    # Other popular models
    "phi4": (14, 10, 16, "Phi-4 14B"),
    "gemma2:9b": (9, 8, 12, "Gemma 2 9B"),
    "gemma2:27b": (27, 20, 32, "Gemma 2 27B"),
    "deepseek-r1:7b": (7, 6, 10, "DeepSeek R1 7B"),
    "deepseek-r1:32b": (32, 20, 32, "DeepSeek R1 32B"),
}

def detect_linux_memory() -> tuple[float, float]:
    """Detect total and available RAM on Linux."""
    try:
        with open('/proc/meminfo') as f:
            meminfo = f.read()
        
        total_match = re.search(r'MemTotal:\s+(\d+)\s+kB', meminfo)
        available_match = re.search(r'MemAvailable:\s+(\d+)\s+kB', meminfo)
        
        total_gb = int(total_match.group(1)) / 1024 / 1024 if total_match else 0
        available_gb = int(available_match.group(1)) / 1024 / 1024 if available_match else 0
        
        return total_gb, available_gb
    except Exception:
        return 0, 0

def detect_mac_memory() -> tuple[float, float]:
    """Detect memory on macOS."""
    try:
        result = subprocess.run(['sysctl', '-n', 'hw.memsize'], 
                              capture_output=True, text=True)
        total_bytes = int(result.stdout.strip())
        total_gb = total_bytes / 1024 / 1024 / 1024
        
        # macOS doesn't have easy "available" memory metric
        return total_gb, total_gb * 0.5  # Estimate 50% available
    except Exception:
        return 0, 0

def detect_gpu() -> tuple[Optional[float], Optional[str]]:
    """Detect GPU and VRAM. Returns (vram_gb, gpu_name)."""
    vram_gb = None
    gpu_name = None
    
    # Try nvidia-smi for NVIDIA GPUs
    try:
        result = subprocess.run(
            ['nvidia-smi', '--query-gpu=name,memory.total', '--format=csv,noheader'],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            line = result.stdout.strip().split('\n')[0]
            parts = line.split(',')
            if len(parts) >= 2:
                gpu_name = parts[0].strip()
                # Parse memory like "8192 MiB" or "8 GB"
                mem_str = parts[1].strip()
                if 'MiB' in mem_str:
                    vram_gb = int(re.search(r'(\d+)', mem_str).group(1)) / 1024
                elif 'GB' in mem_str or 'GiB' in mem_str:
                    vram_gb = float(re.search(r'([\d.]+)', mem_str).group(1))
                return vram_gb, gpu_name
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    # Try rocm-smi for AMD GPUs
    try:
        result = subprocess.run(
            ['rocm-smi', '--showproductname', '--showmeminfo', 'vram'],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and 'AMD' in result.stdout:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if 'AMD' in line or 'Radeon' in line:
                    gpu_name = line.strip()
                if 'VRAM' in line or 'Total Memory' in line:
                    match = re.search(r'(\d+)\s*MB', line)
                    if match:
                        vram_gb = int(match.group(1)) / 1024
                        return vram_gb, gpu_name
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    # Check for Apple Silicon GPU
    try:
        result = subprocess.run(['sysctl', '-n', 'hw.model'], 
                              capture_output=True, text=True)
        if 'Mac' in result.stdout:
            # Check if it's Apple Silicon (M1/M2/M3)
            chip_result = subprocess.run(['sysctl', '-n', 'machdep.cpu.brand_string'],
                                        capture_output=True, text=True)
            if 'Apple' in chip_result.stdout:
                gpu_name = chip_result.stdout.strip()
                # Unified memory - use system RAM
                total_ram, _ = detect_mac_memory()
                vram_gb = total_ram * 0.8  # Can use most of unified memory
                return vram_gb, gpu_name
    except Exception:
        pass
    
    return vram_gb, gpu_name

def detect_cpu_cores() -> int:
    """Detect number of CPU cores."""
    try:
        return os.cpu_count() or 4
    except:
        return 4

def get_system_specs() -> SystemSpecs:
    """Get complete system specifications."""
    # Detect OS and get memory
    if os.path.exists('/proc/meminfo'):
        total_ram, available_ram = detect_linux_memory()
    elif os.uname().sysname == 'Darwin':
        total_ram, available_ram = detect_mac_memory()
    else:
        total_ram, available_ram = 8, 4  # Default assumption
    
    vram, gpu_name = detect_gpu()
    cpu_cores = detect_cpu_cores()
    
    return SystemSpecs(
        total_ram_gb=total_ram,
        available_ram_gb=available_ram,
        gpu_vram_gb=vram,
        gpu_name=gpu_name,
        cpu_cores=cpu_cores,
        is_gpu_available=vram is not None and vram > 0
    )

def get_compatible_models(specs: SystemSpecs) -> dict[str, dict]:
    """
    Get models compatible with system specs.
    Returns dict of {model_name: requirements}
    """
    compatible = {}
    
    for model, (params, min_vram, min_ram, description) in MODEL_REQUIREMENTS.items():
        # Check if system can handle this model
        if specs.is_gpu_available:
            # With GPU: check VRAM
            if specs.gpu_vram_gb and specs.gpu_vram_gb >= min_vram:
                compatible[model] = {
                    "params": params,
                    "min_vram": min_vram,
                    "description": description,
                    "will_run": "fast_gpu"
                }
            elif specs.total_ram_gb >= min_ram * 1.5:  # Can run offloaded to RAM
                compatible[model] = {
                    "params": params,
                    "min_vram": min_vram,
                    "description": description,
                    "will_run": "slow_ram"
                }
        else:
            # CPU only: check RAM
            if specs.total_ram_gb >= min_ram:
                compatible[model] = {
                    "params": params,
                    "min_vram": min_vram,
                    "description": description,
                    "will_run": "slow_cpu"
                }
    
    return compatible

def get_recommended_tiers(specs: SystemSpecs) -> dict[str, list[str]]:
    """
    Get model recommendations by tier for the system.
    """
    compatible = get_compatible_models(specs)
    
    tiers = {
        "lightweight": [],    # 1-3B params, very fast
        "balanced": [],       # 7-9B params, good quality/speed
        "capable": [],        # 14-32B params, high quality
        "max_quality": []     # 70B+, best quality if available
    }
    
    for model, info in compatible.items():
        params = info["params"]
        speed = info["will_run"]
        
        if params <= 3:
            tiers["lightweight"].append(f"{model} ({speed})")
        elif params <= 9:
            tiers["balanced"].append(f"{model} ({speed})")
        elif params <= 32:
            tiers["capable"].append(f"{model} ({speed})")
        else:
            tiers["max_quality"].append(f"{model} ({speed})")
    
    return tiers

def main():
    print("Scanning system...")
    print("-" * 50)
    
    specs = get_system_specs()
    print(f"Detected: {specs}")
    print("-" * 50)
    
    # Get compatible models
    compatible = get_compatible_models(specs)
    
    print(f"\nCompatible models ({len(compatible)} found):")
    print("-" * 50)
    
    tiers = get_recommended_tiers(specs)
    
    for tier_name, models in tiers.items():
        if models:
            print(f"\n{tier_name.upper()}:")
            for model in sorted(models):
                print(f"  - {model}")
    
    # Recommendations for router config
    print("\n" + "=" * 50)
    print("RECOMMENDED ROUTER CONFIG:")
    print("=" * 50)
    
    if tiers["balanced"]:
        # Pick first balanced model for local
        local_model = tiers["balanced"][0].split()[0]
    elif tiers["lightweight"]:
        local_model = tiers["lightweight"][0].split()[0]
    else:
        local_model = "llama3.2:1b"  # Fallback
    
    print(f"""
local:
  model: "{local_model}"
  base_url: "http://localhost:11434"

cloud:
  model: "qwen2.5:14b"  # Configure your remote Ollama here
  base_url: "http://YOUR-SERVER:11434"
""")
    
    # Save system profile
    profile_path = Path(__file__).parent.parent / "config" / "system_profile.json"
    profile_path.parent.mkdir(parents=True, exist_ok=True)
    
    profile = {
        "specs": {
            "total_ram_gb": specs.total_ram_gb,
            "available_ram_gb": specs.available_ram_gb,
            "gpu_vram_gb": specs.gpu_vram_gb,
            "gpu_name": specs.gpu_name,
            "cpu_cores": specs.cpu_cores,
            "is_gpu_available": specs.is_gpu_available
        },
        "compatible_models": list(compatible.keys()),
        "recommended_local": local_model
    }
    
    with open(profile_path, 'w') as f:
        json.dump(profile, f, indent=2)
    
    print(f"\nProfile saved to: {profile_path}")

if __name__ == '__main__':
    main()
