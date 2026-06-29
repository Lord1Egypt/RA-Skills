"""Docker Compose and systemd template generation for various LLM engines."""

from __future__ import annotations

import textwrap
from typing import Any

# ---------------------------------------------------------------------------
# Engine metadata
# ---------------------------------------------------------------------------

ENGINE_META: dict[str, dict[str, Any]] = {
    "ollama": {
        "name": "Ollama",
        "description": "Easy CPU/GPU LLM serving via Ollama",
        "default_port": 11434,
        "image": "ollama/ollama:latest",
    },
    "vllm": {
        "name": "vLLM",
        "description": "High-performance GPU inference engine",
        "default_port": 8000,
        "image": "vllm/vllm-openai:latest",
    },
    "llama.cpp": {
        "name": "llama.cpp",
        "description": "Lightweight CPU/GPU LLM server",
        "default_port": 8080,
        "image": "ghcr.io/ggerganov/llama.cpp:server",
    },
}

# ---------------------------------------------------------------------------
# Recommended models per engine: name, size_desc, min_vram_gb, min_ram_gb
# ---------------------------------------------------------------------------

MODEL_RECOMMENDATIONS: dict[str, list[dict[str, Any]]] = {
    "ollama": [
        {"name": "llama3.1:8b", "size": "~4.7 GB", "min_vram": 6, "min_ram": 8,
         "desc": "Meta Llama 3.1 8B – balanced general-purpose model"},
        {"name": "qwen2.5:7b", "size": "~4.4 GB", "min_vram": 6, "min_ram": 8,
         "desc": "Alibaba Qwen 2.5 7B – strong multilingual"},
        {"name": "deepseek-coder-v2:16b", "size": "~8.9 GB", "min_vram": 12, "min_ram": 16,
         "desc": "DeepSeek Coder V2 16B – code generation specialist"},
        {"name": "codestral:22b", "size": "~12 GB", "min_vram": 16, "min_ram": 20,
         "desc": "Mistral Codestral 22B – advanced code generation"},
    ],
    "vllm": [
        {"name": "meta-llama/Llama-3.1-8B-Instruct", "size": "~16 GB (FP16)", "min_vram": 18, "min_ram": 24,
         "desc": "Meta Llama 3.1 8B Instruct – balanced general-purpose"},
        {"name": "Qwen/Qwen2.5-7B-Instruct", "size": "~14 GB (FP16)", "min_vram": 16, "min_ram": 22,
         "desc": "Alibaba Qwen 2.5 7B Instruct – strong multilingual"},
        {"name": "deepseek-ai/DeepSeek-V3", "size": "~15 GB (FP16)", "min_vram": 18, "min_ram": 24,
         "desc": "DeepSeek V3 – latest MoE model"},
        {"name": "microsoft/Phi-3-mini-4k-instruct", "size": "~7 GB (FP16)", "min_vram": 10, "min_ram": 16,
         "desc": "Microsoft Phi-3 Mini – small but capable"},
    ],
    "llama.cpp": [
        {"name": "llama3.1-8b (Q4_K_M)", "size": "~5 GB", "min_vram": 0, "min_ram": 8,
         "desc": "Meta Llama 3.1 8B quantized – runs on CPU"},
        {"name": "qwen2.5-7b (Q4_K_M)", "size": "~4.5 GB", "min_vram": 0, "min_ram": 8,
         "desc": "Qwen 2.5 7B quantized – multilingual"},
        {"name": "deepseek-coder-v2-16b (Q4_K_M)", "size": "~9 GB", "min_vram": 0, "min_ram": 16,
         "desc": "DeepSeek Coder V2 quantized – code specialist"},
        {"name": "codestral-22b (Q4_K_M)", "size": "~12 GB", "min_vram": 0, "min_ram": 20,
         "desc": "Codestral 22B quantized – advanced code"},
    ],
}

# ---------------------------------------------------------------------------
# Docker Compose templates
# ---------------------------------------------------------------------------

TEMPLATES: dict[str, dict[str, Any]] = {
    "ollama": {
        "service_name": "ollama",
        "image": "ollama/ollama:latest",
        "default_port": 11434,
        "description": "Ollama – easy CPU/GPU LLM serving",
        "volumes": ["ollama_models:/root/.ollama"],
    },
    "vllm": {
        "service_name": "vllm",
        "image": "vllm/vllm-openai:latest",
        "default_port": 8000,
        "description": "vLLM – high-performance GPU inference",
        "volumes": ["~/.cache/huggingface:/root/.cache/huggingface"],
    },
    "llama.cpp": {
        "service_name": "llama.cpp",
        "image": "ghcr.io/ggerganov/llama.cpp:server",
        "default_port": 8080,
        "description": "llama.cpp – lightweight CPU/GPU server",
        "volumes": ["./models:/models"],
    },
}


def generate_compose(
    engine: str,
    model_name: str,
    gpu: bool = True,
    port: int | None = None,
) -> str:
    """Generate a docker-compose.yml as a YAML string.

    Parameters
    ----------
    engine : str
        One of ``ollama``, ``vllm``, ``llama.cpp``.
    model_name : str
        Model identifier passed to the engine.
    gpu : bool
        Request GPU acceleration (ignored for engines that always need it).
    port : int or None
        Override port; ``None`` uses the engine default.

    Returns
    -------
    str
        Valid YAML content.
    """
    if engine not in TEMPLATES:
        raise ValueError(f"Unknown engine '{engine}'. Choose from: {', '.join(TEMPLATES)}")

    tpl = TEMPLATES[engine]
    svc = tpl["service_name"]
    image = tpl["image"]
    default_port = tpl["default_port"]
    listen_port = port if port is not None else default_port

    # Build ports mapping
    compose_port = f'"{listen_port}:{default_port}"'

    lines: list[str] = []
    lines.append(f'# Generated by llm-deploy-helper v1.0.0')
    lines.append(f'# Engine: {engine} ({tpl["description"]})')
    lines.append(f'# Model: {model_name}')
    lines.append(f'# GPU: {"enabled" if gpu else "disabled"}')
    lines.append("")
    lines.append("services:")
    lines.append(f"  {svc}:")
    lines.append(f"    image: {image}")
    lines.append(f"    container_name: {svc}-server")
    lines.append("    ports:")
    lines.append(f"      - {compose_port}")

    # Volumes
    lines.append("    volumes:")
    for vol in tpl["volumes"]:
        lines.append(f"      - {vol}")

    # Engine-specific configuration
    if engine == "ollama":
        lines.append("    restart: unless-stopped")
        if gpu:
            lines.append("    deploy:")
            lines.append("      resources:")
            lines.append("        reservations:")
            lines.append("          devices:")
            lines.append("            - driver: nvidia")
            lines.append("              count: 1")
            lines.append("              capabilities: [gpu]")
        lines.append("    environment:")
        lines.append(f'      - OLLAMA_KEEP_ALIVE=24h')

    elif engine == "vllm":
        lines.append('    command: ["--model", "MODEL_PLACEHOLDER", "--gpu-memory-utilization", "0.90"]')
        lines.append("    restart: unless-stopped")
        lines.append("    deploy:")
        lines.append("      resources:")
        lines.append("        reservations:")
        lines.append("          devices:")
        lines.append("            - driver: nvidia")
        lines.append("              count: 1")
        lines.append("              capabilities: [gpu]")
        lines.append("    environment:")
        lines.append("      - HF_TOKEN=${HF_TOKEN:-}")
        lines.append("      - NVIDIA_VISIBLE_DEVICES=all")

    elif engine == "llama.cpp":
        lines.append(f'    command: ["-m", "/models/MODEL_PLACEHOLDER", "--host", "0.0.0.0", "--port", "{default_port}"]')
        lines.append("    restart: unless-stopped")
        if gpu:
            lines.append("    deploy:")
            lines.append("      resources:")
            lines.append("        reservations:")
            lines.append("          devices:")
            lines.append("            - driver: nvidia")
            lines.append("              count: 1")
            lines.append("              capabilities: [gpu]")

    # Named volumes for ollama
    if engine == "ollama":
        lines.append("")
        lines.append("volumes:")
        lines.append("  ollama_models:")

    # Substitute model placeholder
    content = "\n".join(lines)
    content = content.replace("MODEL_PLACEHOLDER", model_name)

    return content


def generate_systemd(engine: str, model_name: str) -> str:
    """Generate a systemd unit file for the given engine.

    Parameters
    ----------
    engine : str
        One of ``ollama``, ``vllm``, ``llama.cpp``.
    model_name : str
        Model identifier.

    Returns
    -------
    str
        systemd unit file content.
    """
    if engine not in TEMPLATES:
        raise ValueError(f"Unknown engine '{engine}'. Choose from: {', '.join(TEMPLATES)}")

    tpl = TEMPLATES[engine]
    image = tpl["image"]
    default_port = tpl["default_port"]
    svc = tpl["service_name"]

    # Build docker run command
    if engine == "ollama":
        exec_line = (
            f'/usr/bin/docker run --rm --name {svc}-server '
            f'-p {default_port}:11434 '
            f'-v ollama_models:/root/.ollama '
            f'--restart unless-stopped '
            f'{image}'
        )
    elif engine == "vllm":
        exec_line = (
            f'/usr/bin/docker run --rm --name {svc}-server '
            f'-p {default_port}:8000 '
            f'-v ~/.cache/huggingface:/root/.cache/huggingface '
            f'--gpus all '
            f'-e HF_TOKEN=${{HF_TOKEN:-}} '
            f'--restart unless-stopped '
            f'{image} '
            f'--model {model_name} --gpu-memory-utilization 0.90'
        )
    elif engine == "llama.cpp":
        exec_line = (
            f'/usr/bin/docker run --rm --name {svc}-server '
            f'-p {default_port}:8080 '
            f'-v ./models:/models '
            f'--restart unless-stopped '
            f'{image} '
            f'-m /models/{model_name} --host 0.0.0.0 --port 8080'
        )

    unit = textwrap.dedent(f"""\
    [Unit]
    Description={svc.capitalize()} LLM Server ({model_name})
    After=docker.service network-online.target
    Requires=docker.service

    [Service]
    Type=simple
    ExecStartPre=-/usr/bin/docker stop {svc}-server 2>/dev/null
    ExecStartPre=-/usr/bin/docker rm {svc}-server 2>/dev/null
    ExecStart={exec_line}
    ExecStop=/usr/bin/docker stop {svc}-server
    Restart=on-failure
    RestartSec=10
    TimeoutStartSec=300

    [Install]
    WantedBy=multi-user.target
    """)

    return unit.strip()
