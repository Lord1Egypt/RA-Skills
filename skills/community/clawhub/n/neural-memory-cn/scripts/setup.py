#!/usr/bin/env python3
"""
Neural Memory Setup Script / 神经记忆安装脚本

Auto-detects OpenClaw installation and configures the neural memory system.
自动检测 OpenClaw 安装位置并配置神经记忆系统。

Usage / 使用方法:
    python setup.py                          # Interactive setup / 交互式安装
    python setup.py --path ~/.neural-memory  # Custom path / 自定义路径
    python setup.py --auto                   # Auto setup with defaults / 自动安装

Environment Variables / 环境变量:
    NEURAL_MEMORY_LLM_API_KEY   - LLM API key / LLM API 密钥
    NEURAL_MEMORY_LLM_BASE_URL  - LLM API base URL / LLM API 基础 URL
    NEURAL_MEMORY_LLM_MODEL     - LLM model name / LLM 模型名称
"""

import os
import sys
import json
import shutil
from pathlib import Path

# Default configuration template (no hardcoded secrets!)
DEFAULT_CONFIG = {
    "thinking": {
        "enabled": True,
        "mode": "smart",
        "enhanced": {
            "use_intent_layer": True,
            "use_semantic_engine": True,
            "use_lazy_loading": True,
            "use_llm_analysis": False  # Disabled by default, enable after config
        },
        "intent": {
            "use_llm": False,
            "llm_base_url": "",
            "llm_model": "",
            "llm_api_key": "",  # Populated from env or args
            "relevance_threshold": 0.4,
            "max_related_neurons": 10
        },
        "semantic": {
            "embedding_model": "local",
            "cache_dir": ""  # Auto-set during setup
        },
        "storage": {
            "hot_cache_size": 100,
            "lazy_loading": True
        },
        "parameters": {
            "default_max_depth": 3,
            "decay_factor": 0.8,
            "min_activation": 0.15,
            "result_limit": 20
        },
        "protection": {
            "enabled": True,
            "protected_types": ["preference", "personality", "identity", "user_profile", "user_preference"],
            "allow_update_protected": True,
            "allow_delete_protected": False
        }
    }
}

DEFAULT_DOMAINS = {
    "示例领域": ["相关概念1", "相关概念2"],
    "Example Domain": ["Related Concept 1", "Related Concept 2"]
}


def detect_openclaw_path():
    """
    Detect OpenClaw installation path.
    检测 OpenClaw 安装路径。
    """
    # Check common locations
    candidates = [
        Path.home() / ".openclaw",
        Path.home() / "openclaw",
        Path.cwd(),
    ]
    
    # Check environment variable
    if "OPENCLAW_STATE_DIR" in os.environ:
        candidates.insert(0, Path(os.environ["OPENCLAW_STATE_DIR"]))
    
    for path in candidates:
        if path.exists():
            return path
    
    return Path.home() / ".openclaw"


def get_llm_config_from_env():
    """
    Get LLM configuration from environment variables.
    从环境变量获取 LLM 配置。
    """
    return {
        "api_key": os.environ.get("NEURAL_MEMORY_LLM_API_KEY", ""),
        "base_url": os.environ.get("NEURAL_MEMORY_LLM_BASE_URL", ""),
        "model": os.environ.get("NEURAL_MEMORY_LLM_MODEL", "")
    }


def setup_neural_memory(
    base_path: str = None,
    llm_api_key: str = None,
    llm_base_url: str = None,
    llm_model: str = None,
    auto: bool = False
):
    """
    Initialize neural memory system.
    初始化神经记忆系统。
    
    Args:
        base_path: Directory for memory storage / 记忆存储目录
        llm_api_key: API key for LLM intent analysis / LLM 意图分析 API 密钥
        llm_base_url: LLM API base URL / LLM API 基础 URL
        llm_model: Model identifier / 模型标识符
        auto: Run in non-interactive mode / 非交互模式运行
    """
    # Determine base path
    if base_path is None:
        openclaw_path = detect_openclaw_path()
        base_path = openclaw_path / "neural-memory"
    else:
        base_path = Path(base_path)
    
    print("\n" + "=" * 60)
    print("  Neural Memory Setup / 神经记忆安装")
    print("=" * 60)
    print(f"\n[INFO] Installation path / 安装路径: {base_path}")
    
    # Create directory structure
    dirs = [
        base_path,
        base_path / "memory_long_term",
        base_path / "memory_long_term" / "synapses",
        base_path / "memory_long_term" / "embeddings",
        base_path / "memory_long_term" / "activation_logs"
    ]
    
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
    print(f"[OK] Created directories / 目录创建完成")
    
    # Get LLM config from environment if not provided
    env_config = get_llm_config_from_env()
    if not llm_api_key:
        llm_api_key = env_config["api_key"]
    if not llm_base_url:
        llm_base_url = env_config["base_url"]
    if not llm_model:
        llm_model = env_config["model"]
    
    # Build config
    config = json.loads(json.dumps(DEFAULT_CONFIG))  # Deep copy
    
    # Set paths
    config["thinking"]["semantic"]["cache_dir"] = str(base_path / "memory_long_term" / "embeddings")
    
    # Configure LLM if provided
    if llm_api_key and llm_base_url and llm_model:
        config["thinking"]["enhanced"]["use_llm_analysis"] = True
        config["thinking"]["intent"]["use_llm"] = True
        config["thinking"]["intent"]["llm_api_key"] = llm_api_key
        config["thinking"]["intent"]["llm_base_url"] = llm_base_url
        config["thinking"]["intent"]["llm_model"] = llm_model
        print(f"[OK] LLM configured / LLM 配置完成: {llm_model}")
    else:
        print(f"[INFO] LLM not configured / LLM 未配置 (using local mode)")
    
    # Write config
    config_path = base_path / "config.yaml"
    try:
        import yaml
        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
        print(f"[OK] Config created / 配置文件创建完成: {config_path}")
    except ImportError:
        # Fallback to JSON if PyYAML not available
        config_path = base_path / "config.json"
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        print(f"[OK] Config created (JSON) / 配置文件创建完成: {config_path}")
    
    # Create empty neurons file
    neurons_path = base_path / "memory_long_term" / "neurons.json"
    if not neurons_path.exists():
        with open(neurons_path, "w", encoding="utf-8") as f:
            json.dump({"neurons": []}, f, ensure_ascii=False, indent=2)
        print(f"[OK] Neurons index created / 神经元索引创建完成")
    
    # Create domain hints template
    domains_path = base_path / "memory_long_term" / "domain_hints.json"
    if not domains_path.exists():
        with open(domains_path, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_DOMAINS, f, ensure_ascii=True, indent=2)
        print(f"[OK] Domain hints created / 领域提示创建完成")
    
    # Success message
    print("\n" + "=" * 60)
    print("  Setup Complete! / 安装完成！")
    print("=" * 60)
    
    print(f"""
Installation path / 安装路径:
  {base_path}

Quick Start / 快速开始:
  from thinking import ThinkingModule
  memory = ThinkingModule(base_path="{base_path}")
  result = memory.think("查询内容")

Documentation / 文档:
  - API Reference: skills/neural-memory/references/api.md
  - Architecture: skills/neural-memory/references/architecture.md
""")
    
    # LLM configuration hint
    if not (llm_api_key and llm_base_url and llm_model):
        print("""
[OPTIONAL] Enable LLM for better intent analysis:
[可选] 启用 LLM 以获得更好的意图分析效果:

  # Set environment variables / 设置环境变量:
  export NEURAL_MEMORY_LLM_API_KEY="your-api-key"
  export NEURAL_MEMORY_LLM_BASE_URL="https://openrouter.ai/api/v1"
  export NEURAL_MEMORY_LLM_MODEL="openai/gpt-3.5-turbo"

  # Or edit config / 或编辑配置文件:
  {config_path}
  
  Set: intent.use_llm: true
       intent.llm_api_key: "your-key"
       intent.llm_base_url: "your-url"
       intent.llm_model: "your-model"
""")
    
    return str(base_path)


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Initialize neural memory system / 初始化神经记忆系统",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--path", default=None, help="Base path for memory storage / 记忆存储路径")
    parser.add_argument("--api-key", default=None, help="LLM API key / LLM API 密钥")
    parser.add_argument("--base-url", default=None, help="LLM API base URL / LLM API 基础 URL")
    parser.add_argument("--model", default=None, help="LLM model identifier / LLM 模型标识符")
    parser.add_argument("--auto", action="store_true", help="Non-interactive mode / 非交互模式")
    args = parser.parse_args()
    
    setup_neural_memory(
        base_path=args.path,
        llm_api_key=args.api_key,
        llm_base_url=args.base_url,
        llm_model=args.model,
        auto=args.auto
    )


if __name__ == "__main__":
    main()