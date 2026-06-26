#!/usr/bin/env python3
"""
OpenClaw 配置验证脚本
验证 openclaw.json 的正确性
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any

# 配置路径
OPENCLAW_CONFIG = Path.home() / ".openclaw" / "openclaw.json"

# 必需字段
REQUIRED_FIELDS = {
    "gateway": ["mode", "bind", "port", "auth"],
    "agents": ["defaults", "list"],
    "models": ["providers"],
    "tools": [],
}

# 推荐的 agent
RECOMMENDED_AGENTS = ["main", "hermes"]

# 有效的模型提供商
VALID_PROVIDERS = ["qwen", "deepseek", "ollama", "modelstudio"]


class ConfigValidator:
    """OpenClaw 配置验证器"""
    
    def __init__(self, config_path: Path = OPENCLAW_CONFIG):
        self.config_path = config_path
        self.config = None
        self.errors = []
        self.warnings = []
        self.suggestions = []
    
    def load_config(self) -> bool:
        """加载配置文件"""
        if not self.config_path.exists():
            self.errors.append(f"配置文件不存在：{self.config_path}")
            return False
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            return True
        except json.JSONDecodeError as e:
            self.errors.append(f"JSON 格式错误：{e}")
            return False
    
    def validate_structure(self) -> bool:
        """验证基本结构"""
        for field, subfields in REQUIRED_FIELDS.items():
            if field not in self.config:
                self.errors.append(f"缺少必需字段：{field}")
                continue
            
            for subfield in subfields:
                if subfield not in self.config[field]:
                    self.warnings.append(f"缺少推荐字段：{field}.{subfield}")
        
        return len(self.errors) == 0
    
    def validate_agents(self) -> bool:
        """验证 Agent 配置"""
        agents = self.config.get("agents", {}).get("list", [])
        
        # 检查必需 agent
        agent_ids = [a.get("id") for a in agents]
        for required in RECOMMENDED_AGENTS:
            if required not in agent_ids:
                self.warnings.append(f"缺少推荐 agent: {required}")
        
        # 检查 agent 配置
        for agent in agents:
            agent_id = agent.get("id", "unknown")
            
            # 检查 model 字段
            if "model" not in agent and "model" not in agent.get("defaults", {}):
                self.warnings.append(f"Agent {agent_id} 缺少 model 配置")
            
            # 检查 subagents 配置
            subagents = agent.get("subagents", {})
            if "allowAgents" in subagents:
                for sub in subagents["allowAgents"]:
                    if sub not in agent_ids:
                        self.suggestions.append(
                            f"Agent {agent_id} 的 subagent '{sub}' 不存在于 agent 列表"
                        )
        
        return True
    
    def validate_models(self) -> bool:
        """验证模型配置"""
        providers = self.config.get("models", {}).get("providers", {})
        
        for provider_name, provider_config in providers.items():
            if provider_name not in VALID_PROVIDERS:
                self.suggestions.append(f"未知模型提供商：{provider_name}")
            
            # 检查 baseUrl
            if "baseUrl" not in provider_config and provider_name != "ollama":
                self.warnings.append(f"提供商 {provider_name} 缺少 baseUrl")
            
            # 检查 models 列表
            models = provider_config.get("models", [])
            if not models:
                self.warnings.append(f"提供商 {provider_name} 没有配置任何模型")
        
        return True
    
    def validate_tools(self) -> bool:
        """验证工具配置"""
        tools = self.config.get("tools", {})
        
        # 检查 agentToAgent
        a2a = tools.get("agentToAgent", {})
        if a2a.get("enabled"):
            allow_list = a2a.get("allow", [])
            agent_ids = [a.get("id") for a in self.config.get("agents", {}).get("list", [])]
            
            for agent in allow_list:
                if agent not in agent_ids:
                    self.suggestions.append(
                        f"agentToAgent 允许列表中的 '{agent}' 不存在"
                    )
        
        return True
    
    def validate_security(self) -> bool:
        """验证安全配置"""
        # 检查 gateway auth
        gateway = self.config.get("gateway", {})
        auth = gateway.get("auth", {})
        
        if auth.get("mode") == "none":
            self.warnings.append("Gateway 认证模式为 none，建议设置为 token")
        
        # 检查 feishu groupPolicy
        channels = self.config.get("channels", {})
        feishu = channels.get("feishu", {})
        
        if feishu.get("groupPolicy") == "open":
            self.warnings.append("Feishu 群策略为 open，建议设置为 allowlist")
        
        return True
    
    def validate(self) -> Dict[str, Any]:
        """执行完整验证"""
        print("=" * 60)
        print("  OpenClaw 配置验证")
        print("=" * 60)
        print()
        
        # 加载配置
        print("📄 加载配置文件...")
        if not self.load_config():
            return {"valid": False, "errors": self.errors}
        print(f"✓ 配置文件：{self.config_path}")
        print()
        
        # 执行验证
        print("🔍 验证配置结构...")
        self.validate_structure()
        
        print("🔍 验证 Agent 配置...")
        self.validate_agents()
        
        print("🔍 验证模型配置...")
        self.validate_models()
        
        print("🔍 验证工具配置...")
        self.validate_tools()
        
        print("🔍 验证安全配置...")
        self.validate_security()
        
        print()
        print("=" * 60)
        print("  验证结果")
        print("=" * 60)
        print()
        
        # 输出结果
        if self.errors:
            print(f"❌ 错误 ({len(self.errors)}):")
            for error in self.errors:
                print(f"   - {error}")
            print()
        
        if self.warnings:
            print(f"⚠️  警告 ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   - {warning}")
            print()
        
        if self.suggestions:
            print(f"💡 建议 ({len(self.suggestions)}):")
            for suggestion in self.suggestions:
                print(f"   - {suggestion}")
            print()
        
        if not self.errors and not self.warnings and not self.suggestions:
            print("✅ 配置完美！没有发现任何问题。")
            print()
        
        # 总结
        valid = len(self.errors) == 0
        print(f"状态：{'✅ 通过' if valid else '❌ 失败'}")
        print(f"错误：{len(self.errors)} | 警告：{len(self.warnings)} | 建议：{len(self.suggestions)}")
        print("=" * 60)
        
        return {
            "valid": valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "suggestions": self.suggestions
        }


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="OpenClaw 配置验证工具")
    parser.add_argument("--config", type=str, default=str(OPENCLAW_CONFIG),
                       help="配置文件路径")
    parser.add_argument("--json", action="store_true",
                       help="输出 JSON 格式结果")
    
    args = parser.parse_args()
    
    validator = ConfigValidator(Path(args.config))
    result = validator.validate()
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0 if result["valid"] else 1)
    
    sys.exit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
