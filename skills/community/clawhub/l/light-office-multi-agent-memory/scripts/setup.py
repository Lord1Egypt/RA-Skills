#!/usr/bin/env python3
"""
多Agent记忆系统 - 配置向导脚本（通用版）

功能：
  交互式配置向导，帮助用户快速配置记忆系统

作者：光光教授 (光光事务所)
版本：v1.0.0
许可证：MIT
"""

import os
import sys
import json
import yaml
from pathlib import Path

# ============================================================
# 配置
# ============================================================

WORKSPACE = Path(os.environ.get("MEMORY_WORKSPACE", "/tmp/memory-workspace"))
CONFIG_DIR = WORKSPACE / "config"

# 默认配置
DEFAULT_CONFIG = {
    "memory": {
        "vector_model": "nomic-embed-text-v1.5",
        "vector_dim": 768,
        "search_mode": "rrf",
        "workspace": str(WORKSPACE)
    },
    "hooks": {
        "enabled": True,
        "count": 8
    },
    "rrf": {
        "k": 60,
        "weights": {
            "bm25": 0.2,
            "vector": 0.5,
            "graph": 0.3
        }
    },
    "llm": {
        "api_key": "",
        "api_host": "https://coding.dashscope.aliyuncs.com",
        "model": "qwen3.5-plus"
    }
}

# ============================================================
# 配置向导
# ============================================================

class ConfigWizard:
    """配置向导"""
    
    def __init__(self):
        self.config_dir = CONFIG_DIR
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / "config.yaml"
    
    def run(self):
        """运行配置向导"""
        print("=" * 60)
        print("多Agent记忆系统 - 配置向导")
        print("=" * 60)
        print()
        
        # 加载现有配置
        if self.config_file.exists():
            with open(self.config_file, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
            print(f"发现现有配置: {self.config_file}")
            overwrite = input("是否覆盖现有配置？(y/N): ").strip().lower()
            if overwrite != "y":
                print("保留现有配置")
                return config
        else:
            config = DEFAULT_CONFIG.copy()
        
        print("\n开始配置...")
        print()
        
        # 1. 工作空间配置
        print("1. 工作空间配置")
        workspace = input(f"  工作空间路径 [{config['memory']['workspace']}]: ").strip()
        if workspace:
            config["memory"]["workspace"] = workspace
        
        # 2. 向量模型配置
        print("\n2. 向量模型配置")
        vector_model = input(f"  向量模型 [{config['memory']['vector_model']}]: ").strip()
        if vector_model:
            config["memory"]["vector_model"] = vector_model
        
        vector_dim = input(f"  向量维度 [{config['memory']['vector_dim']}]: ").strip()
        if vector_dim:
            config["memory"]["vector_dim"] = int(vector_dim)
        
        # 3. 检索模式配置
        print("\n3. 检索模式配置")
        print("  可选模式: rrf, vector, bm25")
        search_mode = input(f"  检索模式 [{config['memory']['search_mode']}]: ").strip()
        if search_mode:
            config["memory"]["search_mode"] = search_mode
        
        # 4. Hook配置
        print("\n4. Hook配置")
        hooks_enabled = input(f"  启用Hook [{config['hooks']['enabled']}]: ").strip().lower()
        if hooks_enabled in ["y", "yes", "true", "1"]:
            config["hooks"]["enabled"] = True
        elif hooks_enabled in ["n", "no", "false", "0"]:
            config["hooks"]["enabled"] = False
        
        # 5. LLM配置
        print("\n5. LLM配置")
        api_key = input(f"  API Key (留空使用环境变量): ").strip()
        if api_key:
            config["llm"]["api_key"] = api_key
        
        api_host = input(f"  API Host [{config['llm']['api_host']}]: ").strip()
        if api_host:
            config["llm"]["api_host"] = api_host
        
        model = input(f"  模型 [{config['llm']['model']}]: ").strip()
        if model:
            config["llm"]["model"] = model
        
        # 保存配置
        print("\n保存配置...")
        with open(self.config_file, "w", encoding="utf-8") as f:
            yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
        
        print(f"配置已保存: {self.config_file}")
        print()
        print("=" * 60)
        print("配置完成！")
        print("=" * 60)
        
        return config


# ============================================================
# 主函数
# ============================================================

def main():
    """主函数"""
    wizard = ConfigWizard()
    config = wizard.run()
    
    print("\n当前配置:")
    print(json.dumps(config, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
