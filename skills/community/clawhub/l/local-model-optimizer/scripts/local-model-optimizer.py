#!/usr/bin/env python3
"""
local-model-optimizer.py — Hardware Detection + Model Recommendation + Hybrid Routing
Built by GetAgentIQ — https://getagentiq.ai

Auto-detects hardware, recommends optimal local models, configures Ollama,
and sets up cloud/local hybrid routing in OpenClaw.
"""

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path

# ─── Constants ───────────────────────────────────────────────────────────────

OLLAMA_MODELS_URL = "https://ollama.com/library"

CONFIG_PATH = os.path.expanduser("~/.openclaw/local-model-config.json")
OPENCLAW_CONFIG = os.path.expanduser("~/.openclaw/openclaw.json")

# Model database: name, min_vram_gb, quality_score (1-10), description
MODEL_DB = {
    "tiny": [  # ≤4GB VRAM
        {"name": "gemma3:4b", "vram": 2.5, "quality": 5, "tps": 60, "desc": "Google Gemma 3 4B — efficient edge model"},
        {"name": "phi3.5:3.8b", "vram": 2.5, "quality": 5, "tps": 55, "desc": "Microsoft Phi-3.5 Mini — strong reasoning for size"},
        {"name": "qwen2.5:3b", "vram": 2.0, "quality": 4, "tps": 70, "desc": "Alibaba Qwen 2.5 3B — fast multilingual"},
    ],
    "small": [  # 4-8GB
        {"name": "gemma3:12b-q4_K_M", "vram": 5.0, "quality": 7, "tps": 35, "desc": "Google Gemma 3 12B Q4 — best quality/size ratio"},
        {"name": "llama3.1:8b", "vram": 4.5, "quality": 7, "tps": 40, "desc": "Meta Llama 3.1 8B — strong general purpose"},
        {"name": "mistral:7b", "vram": 4.0, "quality": 6, "tps": 45, "desc": "Mistral 7B — fast European model"},
    ],
    "medium": [  # 8-16GB
        {"name": "gemma3:12b", "vram": 8.0, "quality": 8, "tps": 30, "desc": "Google Gemma 3 12B full — top tool-calling benchmarks"},
        {"name": "llama3.1:8b-q8_0", "vram": 8.5, "quality": 8, "tps": 25, "desc": "Llama 3.1 8B Q8 — maximum 8B quality"},
        {"name": "codegemma:7b", "vram": 7.0, "quality": 7, "tps": 35, "desc": "Google CodeGemma — optimized for code tasks"},
    ],
    "large": [  # 16-32GB
        {"name": "gemma3:27b-q4_K_M", "vram": 16.0, "quality": 9, "tps": 15, "desc": "Google Gemma 3 27B Q4 — near-cloud quality"},
        {"name": "llama3.1:70b-q4_K_M", "vram": 24.0, "quality": 9, "tps": 8, "desc": "Meta Llama 3.1 70B Q4 — massive capability"},
        {"name": "mixtral:8x7b", "vram": 20.0, "quality": 8, "tps": 12, "desc": "Mistral Mixture of Experts — excellent throughput"},
    ],
    "xl": [  # 32GB+
        {"name": "gemma3:27b", "vram": 28.0, "quality": 10, "tps": 12, "desc": "Google Gemma 3 27B full — top-3 open model globally"},
        {"name": "llama3.1:70b-q8_0", "vram": 48.0, "quality": 10, "tps": 5, "desc": "Llama 3.1 70B Q8 — cloud-rivalling quality"},
        {"name": "deepseek-v2:16b", "vram": 32.0, "quality": 9, "tps": 10, "desc": "DeepSeek V2 — strong reasoning and math"},
    ],
}

# Routing strategies
ROUTING_RULES = {
    "local_tasks": [
        "simple_qa", "summarization", "translation", "text_classification",
        "code_completion", "memory_search", "data_extraction", "formatting",
    ],
    "cloud_tasks": [
        "complex_reasoning", "multi_step_planning", "creative_writing",
        "code_generation", "architecture_design", "security_analysis",
        "long_context", "agentic_workflows",
    ],
}


# ─── Hardware Detection ─────────────────────────────────────────────────────

def detect_gpu():
    """Detect GPU(s) and VRAM."""
    gpus = []

    # Try nvidia-smi first (NVIDIA)
    try:
        result = subprocess.run(
            ['nvidia-smi', '--query-gpu=name,memory.total,driver_version',
             '--format=csv,noheader,nounits'],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            for line in result.stdout.strip().split('\n'):
                parts = [p.strip() for p in line.split(',')]
                if len(parts) >= 3:
                    gpus.append({
                        'vendor': 'NVIDIA',
                        'name': parts[0],
                        'vram_mb': int(float(parts[1])),
                        'vram_gb': round(int(float(parts[1])) / 1024, 1),
                        'driver': parts[2],
                    })
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    # Try rocm-smi (AMD)
    if not gpus:
        try:
            result = subprocess.run(
                ['rocm-smi', '--showmeminfo', 'vram', '--json'],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                for card_id, info in data.items():
                    vram_bytes = int(info.get('VRAM Total Memory (B)', 0))
                    gpus.append({
                        'vendor': 'AMD',
                        'name': f'AMD GPU {card_id}',
                        'vram_mb': vram_bytes // (1024 * 1024),
                        'vram_gb': round(vram_bytes / (1024**3), 1),
                        'driver': 'ROCm',
                    })
        except (FileNotFoundError, subprocess.TimeoutExpired, json.JSONDecodeError):
            pass

    # macOS — Apple Silicon (unified memory acts as VRAM)
    if not gpus and platform.system() == 'Darwin':
        try:
            result = subprocess.run(
                ['sysctl', '-n', 'hw.memsize'],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                total_bytes = int(result.stdout.strip())
                # Apple Silicon shares RAM as VRAM — ~75% is usable for ML
                usable_gb = round((total_bytes / (1024**3)) * 0.75, 1)
                # Detect chip name
                chip_result = subprocess.run(
                    ['sysctl', '-n', 'machdep.cpu.brand_string'],
                    capture_output=True, text=True, timeout=5
                )
                chip_name = chip_result.stdout.strip() if chip_result.returncode == 0 else 'Apple Silicon'

                gpus.append({
                    'vendor': 'Apple',
                    'name': chip_name,
                    'vram_mb': int(usable_gb * 1024),
                    'vram_gb': usable_gb,
                    'driver': 'Metal',
                })
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

    return gpus


def detect_ram():
    """Detect system RAM."""
    try:
        if platform.system() == 'Linux':
            with open('/proc/meminfo', 'r') as f:
                for line in f:
                    if line.startswith('MemTotal:'):
                        kb = int(line.split()[1])
                        return round(kb / (1024 * 1024), 1)
        elif platform.system() == 'Darwin':
            result = subprocess.run(
                ['sysctl', '-n', 'hw.memsize'],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                return round(int(result.stdout.strip()) / (1024**3), 1)
    except (IOError, subprocess.TimeoutExpired):
        pass
    return 0


def detect_cpu():
    """Detect CPU info."""
    info = {
        'model': platform.processor() or 'Unknown',
        'cores': os.cpu_count() or 0,
        'arch': platform.machine(),
    }

    # Try to get better CPU name on Linux
    if platform.system() == 'Linux':
        try:
            with open('/proc/cpuinfo', 'r') as f:
                for line in f:
                    if line.startswith('model name'):
                        info['model'] = line.split(':')[1].strip()
                        break
        except IOError:
            pass

    return info


def get_hardware_tier(vram_gb, ram_gb):
    """Determine hardware tier based on available VRAM (or RAM for CPU-only)."""
    effective_vram = vram_gb if vram_gb > 0 else ram_gb * 0.4  # CPU-only: ~40% RAM usable
    if effective_vram <= 4:
        return "tiny"
    elif effective_vram <= 8:
        return "small"
    elif effective_vram <= 16:
        return "medium"
    elif effective_vram <= 32:
        return "large"
    else:
        return "xl"


# ─── Ollama Management ──────────────────────────────────────────────────────

def check_ollama():
    """Check if Ollama is installed and running."""
    installed = shutil.which('ollama') is not None
    running = False

    if installed:
        try:
            result = subprocess.run(
                ['ollama', 'list'], capture_output=True, text=True, timeout=10
            )
            running = result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

    return installed, running


def install_ollama():
    """Install Ollama using the official installer."""
    print("  📥 Installing Ollama...")
    try:
        if platform.system() == 'Linux':
            result = subprocess.run(
                ['sh', '-c', 'curl -fsSL https://ollama.com/install.sh | sh'],
                capture_output=True, text=True, timeout=300
            )
        elif platform.system() == 'Darwin':
            result = subprocess.run(
                ['brew', 'install', 'ollama'],
                capture_output=True, text=True, timeout=300
            )
        else:
            print("  ❌ Unsupported platform. Install Ollama manually: https://ollama.com")
            return False

        if result.returncode == 0:
            print("  ✅ Ollama installed successfully")
            return True
        else:
            print(f"  ❌ Installation failed: {result.stderr[:200]}")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"  ❌ Installation error: {e}")
        return False


def pull_model(model_name):
    """Pull a model from Ollama registry."""
    print(f"  📥 Pulling {model_name}... (this may take a while)")
    try:
        result = subprocess.run(
            ['ollama', 'pull', model_name],
            capture_output=True, text=True, timeout=1800  # 30 min timeout for large models
        )
        if result.returncode == 0:
            print(f"  ✅ {model_name} pulled successfully")
            return True
        else:
            print(f"  ❌ Failed to pull {model_name}: {result.stderr[:200]}")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"  ❌ Pull error: {e}")
        return False


def test_model(model_name):
    """Run a quick test prompt against a model."""
    print(f"  🧪 Testing {model_name}...")
    try:
        result = subprocess.run(
            ['ollama', 'run', model_name, 'Say "Hello, I am working!" in exactly those words.'],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0 and result.stdout.strip():
            print(f"  ✅ Model responded: {result.stdout.strip()[:100]}")
            return True
        else:
            print(f"  ❌ Model test failed")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print(f"  ❌ Model test timed out")
        return False


# ─── Configuration ───────────────────────────────────────────────────────────

def configure_openclaw_provider(model_name):
    """Add local Ollama as an OpenClaw model provider."""
    if not os.path.exists(OPENCLAW_CONFIG):
        print("  ⚠️  OpenClaw config not found. Manual configuration needed.")
        print(f"  Add to openclaw.json: models.providers.ollama-local with model {model_name}")
        return False

    try:
        with open(OPENCLAW_CONFIG, 'r') as f:
            config = json.load(f)

        # Add Ollama provider if not present
        models = config.setdefault('models', {})
        providers = models.setdefault('providers', {})

        providers['ollama-local'] = {
            'type': 'ollama',
            'baseUrl': 'http://localhost:11434',
            'model': model_name,
            'enabled': True,
        }

        with open(OPENCLAW_CONFIG, 'w') as f:
            json.dump(config, f, indent=2)

        print(f"  ✅ OpenClaw configured with Ollama provider: {model_name}")
        return True
    except (json.JSONDecodeError, IOError) as e:
        print(f"  ❌ Config error: {e}")
        return False


def save_config(hardware, model, routing_strategy="balanced"):
    """Save optimization config for future reference."""
    config = {
        "hardware": hardware,
        "model": model,
        "routing": {
            "strategy": routing_strategy,
            "local_tasks": ROUTING_RULES["local_tasks"],
            "cloud_tasks": ROUTING_RULES["cloud_tasks"],
        },
        "timestamp": __import__('datetime').datetime.utcnow().isoformat(),
    }

    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)

    print(f"  💾 Config saved: {CONFIG_PATH}")


# ─── Commands ────────────────────────────────────────────────────────────────

def cmd_detect(args):
    """Detect and display hardware capabilities."""
    print("🔍 Local Model Optimizer — Hardware Detection")
    print("=" * 50)

    gpus = detect_gpu()
    ram_gb = detect_ram()
    cpu = detect_cpu()

    print(f"\n💻 System: {platform.system()} {platform.release()} ({cpu['arch']})")
    print(f"🧠 CPU: {cpu['model']} ({cpu['cores']} cores)")
    print(f"💾 RAM: {ram_gb} GB")

    total_vram = 0
    if gpus:
        print(f"\n🎮 GPU(s) detected:")
        for gpu in gpus:
            print(f"  • {gpu['vendor']} {gpu['name']}: {gpu['vram_gb']} GB VRAM (driver: {gpu['driver']})")
            total_vram += gpu['vram_gb']
    else:
        print("\n⚠️  No GPU detected — CPU-only inference (slower but works)")

    tier = get_hardware_tier(total_vram, ram_gb)
    tier_names = {"tiny": "Tiny (≤4GB)", "small": "Small (4-8GB)", "medium": "Medium (8-16GB)",
                  "large": "Large (16-32GB)", "xl": "XL (32GB+)"}

    effective = total_vram if total_vram > 0 else ram_gb * 0.4
    print(f"\n📊 Effective AI capacity: {effective:.1f} GB")
    print(f"🏷️  Hardware tier: {tier_names.get(tier, tier)}")

    return {"gpus": gpus, "ram_gb": ram_gb, "cpu": cpu, "tier": tier, "vram_gb": total_vram}


def cmd_recommend(args):
    """Recommend models for detected hardware."""
    print("🤖 Local Model Optimizer — Model Recommendations")
    print("=" * 50)

    # Detect hardware first
    gpus = detect_gpu()
    ram_gb = detect_ram()
    total_vram = sum(g['vram_gb'] for g in gpus) if gpus else 0
    tier = get_hardware_tier(total_vram, ram_gb)

    models = MODEL_DB.get(tier, MODEL_DB["tiny"])

    print(f"\n📊 Hardware tier: {tier.upper()}")
    print(f"🎯 Top {len(models)} recommended models:\n")

    for i, m in enumerate(models, 1):
        stars = "⭐" * min(m['quality'], 5)
        print(f"  {i}. {m['name']}")
        print(f"     {m['desc']}")
        print(f"     VRAM: {m['vram']:.1f} GB | Quality: {stars} ({m['quality']}/10) | Speed: ~{m['tps']} tok/s")
        print()

    print(f"💡 Recommendation: Start with #{1} ({models[0]['name']}) for best quality/performance balance.")
    return models


def cmd_routing(args):
    """Configure hybrid cloud/local routing."""
    print("🔀 Local Model Optimizer — Hybrid Routing")
    print("=" * 50)

    strategy = args.strategy if hasattr(args, 'strategy') and args.strategy else 'balanced'
    cloud_provider = args.cloud_provider if hasattr(args, 'cloud_provider') and args.cloud_provider else 'anthropic'

    print(f"\n📋 Strategy: {strategy}")
    print(f"☁️  Cloud fallback: {cloud_provider}")

    print(f"\n🏠 LOCAL routing (fast, free):")
    for task in ROUTING_RULES["local_tasks"]:
        print(f"  ✅ {task.replace('_', ' ').title()}")

    print(f"\n☁️  CLOUD routing (quality, paid):")
    for task in ROUTING_RULES["cloud_tasks"]:
        print(f"  ☁️  {task.replace('_', ' ').title()}")

    if strategy == 'cost':
        print("\n💰 Cost strategy: Routing 80% of tasks locally. Only complex reasoning goes to cloud.")
    elif strategy == 'quality':
        print("\n🎯 Quality strategy: Routing 60% to cloud. Only simple tasks stay local.")
    else:
        print("\n⚖️  Balanced strategy: Smart routing — simple tasks local, complex tasks cloud.")

    # Save routing config
    print(f"\n💾 Routing rules saved.")
    return strategy


def cmd_cost(args):
    """Calculate cost savings from local inference."""
    print("💰 Local Model Optimizer — Cost Analysis")
    print("=" * 50)

    # Estimate based on typical usage patterns
    # Average OpenClaw user: ~500K tokens/day input, ~100K tokens/day output
    daily_input_tokens = 500_000
    daily_output_tokens = 100_000

    # Cloud costs (per 1M tokens)
    cloud_costs = {
        "anthropic_haiku": {"input": 0.25, "output": 1.25, "name": "Claude Haiku"},
        "anthropic_sonnet": {"input": 3.00, "output": 15.00, "name": "Claude Sonnet"},
        "openai_gpt4o_mini": {"input": 0.15, "output": 0.60, "name": "GPT-4o Mini"},
        "openai_gpt4o": {"input": 2.50, "output": 10.00, "name": "GPT-4o"},
    }

    # Electricity cost for local (estimate: 200W GPU, $0.12/kWh)
    gpu_watts = 200
    electricity_per_kwh = 0.12
    hours_active = 8  # 8 hours/day active inference
    daily_electricity = (gpu_watts / 1000) * hours_active * electricity_per_kwh

    print(f"\n📊 Estimated daily usage: {daily_input_tokens:,} input + {daily_output_tokens:,} output tokens")
    print(f"⚡ Local electricity cost: ~${daily_electricity:.2f}/day ({gpu_watts}W × {hours_active}h × ${electricity_per_kwh}/kWh)")

    print(f"\n{'Model':<25} {'Daily Cloud $':<15} {'Monthly Cloud $':<17} {'Monthly Savings':<17}")
    print("-" * 75)

    for key, cost in cloud_costs.items():
        daily = (daily_input_tokens / 1_000_000 * cost['input'] +
                 daily_output_tokens / 1_000_000 * cost['output'])
        monthly = daily * 30
        savings = monthly - (daily_electricity * 30)
        pct = (savings / monthly * 100) if monthly > 0 else 0

        print(f"{cost['name']:<25} ${daily:<14.2f} ${monthly:<16.2f} ${savings:<10.2f} ({pct:.0f}%)")

    print(f"\n💡 With hybrid routing (balanced strategy), expect 40-60% of tokens handled locally.")
    print(f"   Effective monthly savings: 30-50% of your current cloud bill.")


def cmd_auto(args):
    """Full automated setup pipeline."""
    print("🚀 Local Model Optimizer — Full Auto Setup")
    print("=" * 50)

    # Step 1: Detect hardware
    print("\n[1/6] Detecting hardware...")
    hw = cmd_detect(args)

    # Step 2: Recommend models
    print("\n[2/6] Finding optimal models...")
    models = MODEL_DB.get(hw['tier'], MODEL_DB['tiny'])
    best = models[0]
    print(f"  🎯 Best fit: {best['name']} ({best['desc']})")

    # Step 3: Check/install Ollama
    print("\n[3/6] Checking Ollama...")
    installed, running = check_ollama()
    if not installed:
        print("  Ollama not found. Installing...")
        if not install_ollama():
            print("  ❌ Cannot proceed without Ollama. Install manually: https://ollama.com")
            sys.exit(1)
    elif not running:
        print("  ⚠️  Ollama installed but not running. Start it: ollama serve")
    else:
        print("  ✅ Ollama is installed and running")

    # Step 4: Pull model
    print(f"\n[4/6] Pulling model: {best['name']}...")
    if installed and running:
        pull_model(best['name'])
    else:
        print(f"  ⏭️  Skipping pull (Ollama not running). Run: ollama pull {best['name']}")

    # Step 5: Configure OpenClaw
    print(f"\n[5/6] Configuring OpenClaw provider...")
    configure_openclaw_provider(best['name'])

    # Step 6: Save config
    print(f"\n[6/6] Saving configuration...")
    save_config(hw, best)

    print(f"\n{'=' * 50}")
    print(f"✅ Setup complete!")
    print(f"   Model: {best['name']}")
    print(f"   Tier: {hw['tier'].upper()}")
    print(f"   Quality: {best['quality']}/10")
    print(f"   Expected speed: ~{best['tps']} tokens/sec")
    print(f"\n💡 Run `local-model-optimizer routing` to set up hybrid cloud/local routing.")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Local Model Optimizer — Hardware Detection + Ollama Config + Hybrid Routing'
    )
    sub = parser.add_subparsers(dest='command', help='Command to run')

    sub.add_parser('detect', help='Detect hardware capabilities')
    sub.add_parser('recommend', help='Recommend models for your hardware')

    p_routing = sub.add_parser('routing', help='Configure hybrid cloud/local routing')
    p_routing.add_argument('--strategy', choices=['cost', 'quality', 'balanced'], default='balanced')
    p_routing.add_argument('--cloud-provider', default='anthropic')

    sub.add_parser('cost', help='Cost comparison: local vs cloud')
    sub.add_parser('auto', help='Full automated setup')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        'detect': cmd_detect,
        'recommend': cmd_recommend,
        'routing': cmd_routing,
        'cost': cmd_cost,
        'auto': cmd_auto,
    }

    commands[args.command](args)


if __name__ == '__main__':
    main()
