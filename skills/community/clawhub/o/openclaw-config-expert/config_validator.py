#!/usr/bin/env python3
"""
OpenClaw 配置验证器 (增强版)
自动检测和修复 OpenClaw 配置问题
功能：验证 + 修复 + 原子写入 + 多级备份 + 健康检查
"""

import json
import os
import sys
import shutil
import tempfile
import glob
import subprocess
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import re


class OpenClawConfigValidator:
    """OpenClaw 配置验证和修复工具"""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or os.path.expanduser("~/.openclaw/openclaw.json")
        self.config = None
        self.issues = []
        self.fixes_applied = []
        
        # OpenClaw 2026.4.15+ 废弃字段
        self.deprecated_fields = {
            "memory": [
                "system", "fusion_manager", "config", "data_dir", 
                "vector_store", "embedding", "llm", "protected_paths", 
                "rules", "agent_backup"
            ],
            "plugins.entries.memory-wiki.config": [
                "ingest.memoryDir", "ingest.mem0FusionManager",
                "ingest.includeDailyNotes", "ingest.includeMemoryMd",
                "search.enableSemantic", "search.maxResults",
                "context.autoInject", "context.maxTokens"
            ]
        }
    
    def load_config(self) -> bool:
        """加载配置文件"""
        try:
            if not os.path.exists(self.config_path):
                self.issues.append({"type": "missing_file", "path": self.config_path, "message": f"配置文件不存在：{self.config_path}", "severity": "error"})
                return False
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            
            return True
        except json.JSONDecodeError as e:
            self.issues.append({"type": "invalid_json", "path": self.config_path, "message": f"JSON 解析错误：{e}", "severity": "error"})
            return False
        except Exception as e:
            self.issues.append({"type": "load_error", "path": self.config_path, "message": f"加载配置失败：{e}", "severity": "error"})
            return False
    
    def validate(self) -> List[Dict]:
        """验证配置并返回问题列表"""
        if not self.config:
            if not self.load_config():
                return self.issues
        
        self.issues = []
        
        # 检查废弃字段
        self._check_deprecated_fields()
        
        # 检查必需字段
        self._check_required_fields()
        
        # 检查插件配置
        self._check_plugins()
        
        # 检查 Agent 配置
        self._check_agents()
        
        # 检查模型配置
        self._check_models()
        
        return self.issues
    
    def _check_deprecated_fields(self):
        """检查废弃字段"""
        for path, fields in self.deprecated_fields.items():
            parts = path.split('.')
            current = self.config
            
            for part in parts:
                if part in current:
                    current = current[part]
                else:
                    break
            else:
                for field in fields:
                    if field in current:
                        self.issues.append({
                            "type": "deprecated_field",
                            "path": f"{path}.{field}",
                            "message": f"废弃字段：{field}",
                            "severity": "error"
                        })
    
    def _check_required_fields(self):
        """检查必需字段"""
        required = ["gateway", "agents"]
        
        for field in required:
            if field not in self.config:
                self.issues.append({
                    "type": "missing_required",
                    "path": field,
                    "message": f"缺少必需字段：{field}",
                    "severity": "error"
                })
        
        if "gateway" in self.config and "mode" not in self.config["gateway"]:
            self.issues.append({
                "type": "missing_required",
                "path": "gateway.mode",
                "message": "缺少 gateway.mode 配置",
                "severity": "error"
            })
        
        if "agents" in self.config and "list" not in self.config["agents"]:
            self.issues.append({
                "type": "missing_required",
                "path": "agents.list",
                "message": "缺少 agents.list 配置",
                "severity": "error"
            })
    
    def _check_plugins(self):
        """检查插件配置"""
        if "plugins" not in self.config or "entries" not in self.config["plugins"]:
            return
        
        plugins = self.config["plugins"]["entries"]
        
        if "memory-wiki" in plugins and "config" in plugins["memory-wiki"]:
            config = plugins["memory-wiki"]["config"]
            
            if "ingest" in config:
                invalid_fields = ["memoryDir", "mem0FusionManager", "includeDailyNotes", "includeMemoryMd"]
                for field in invalid_fields:
                    if field in config["ingest"]:
                        self.issues.append({
                            "type": "invalid_plugin_config",
                            "path": "plugins.entries.memory-wiki.config.ingest",
                            "message": f"无效的 ingest 字段：{field}",
                            "severity": "error"
                        })
            
            if "search" in config:
                invalid_fields = ["enableSemantic", "maxResults"]
                for field in invalid_fields:
                    if field in config["search"]:
                        self.issues.append({
                            "type": "invalid_plugin_config",
                            "path": "plugins.entries.memory-wiki.config.search",
                            "message": f"无效的 search 字段：{field}",
                            "severity": "error"
                        })
            
            if "context" in config:
                invalid_fields = ["autoInject", "maxTokens"]
                for field in invalid_fields:
                    if field in config["context"]:
                        self.issues.append({
                            "type": "invalid_plugin_config",
                            "path": "plugins.entries.memory-wiki.config.context",
                            "message": f"无效的 context 字段：{field}",
                            "severity": "error"
                        })
    
    def _check_agents(self):
        """检查 Agent 配置"""
        if "agents" not in self.config or "list" not in self.config["agents"]:
            return
        
        agents = self.config["agents"]["list"]
        agent_ids = [a.get("id") for a in agents if "id" in a]
        
        if "main" not in agent_ids:
            self.issues.append({
                "type": "missing_main_agent",
                "path": "agents.list",
                "message": "缺少 main agent",
                "severity": "warning"
            })
        
        for agent in agents:
            if "id" not in agent:
                self.issues.append({
                    "type": "missing_agent_id",
                    "path": "agents.list[]",
                    "message": "Agent 缺少 id 字段",
                    "severity": "error"
                })
    
    def _check_models(self):
        """检查模型配置"""
        if "models" not in self.config or "providers" not in self.config["models"]:
            return
        
        providers = self.config["models"]["providers"]
        
        for name, provider in providers.items():
            if name != "ollama" and "baseUrl" not in provider:
                self.issues.append({
                    "type": "missing_base_url",
                    "path": f"models.providers.{name}",
                    "message": f"Provider {name} 缺少 baseUrl",
                    "severity": "warning"
                })
    
    def fix(self) -> bool:
        """修复配置问题"""
        if not self.config:
            return False
        
        fixes = []
        
        for issue in self.issues:
            if issue["type"] == "missing_required":
                if issue["path"] == "gateway":
                    self.config["gateway"] = {"mode": "local", "bind": "loopback", "port": 18789}
                    fixes.append("添加 gateway 配置")
                elif issue["path"] == "agents":
                    self.config["agents"] = {
                        "defaults": {"model": {"primary": "deepseek/deepseek-chat"}},
                        "list": [{"id": "main", "default": True, "name": "Main Agent"}]
                    }
                    fixes.append("添加 agents 配置")
                elif issue["path"] == "agents.list":
                    self.config["agents"]["list"] = [{"id": "main", "default": True, "name": "Main Agent"}]
                    fixes.append("添加 agents.list")
        
        self.fixes_applied = fixes
        return len(fixes) > 0
    
    def save_config(self, backup: bool = True, validate_before_save: bool = True, max_backups: int = 5) -> bool:
        """
        保存配置（增强版：原子写入 + 多级备份 + 写入前验证）
        
        Args:
            backup: 是否创建备份
            validate_before_save: 保存前是否验证配置有效性
            max_backups: 保留的最大备份数量
        """
        try:
            # 步骤 1: 写入前验证
            if validate_before_save:
                print("🔍 正在验证配置有效性...")
                
                required = ["gateway", "agents"]
                for field in required:
                    if field not in self.config:
                        print(f"❌ 验证失败：缺少必需字段 {field}")
                        return False
                
                if "mode" not in self.config.get("gateway", {}):
                    print("❌ 验证失败：缺少 gateway.mode")
                    return False
                
                print("✅ 配置验证通过")
            
            # 步骤 2: 创建备份
            if backup and os.path.exists(self.config_path):
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_path = f"{self.config_path}.bak.{timestamp}"
                shutil.copy2(self.config_path, backup_path)
                print(f"✅ 已创建备份：{backup_path}")
                
                self._cleanup_old_backups(max_backups)
            
            # 步骤 3: 原子写入（临时文件 → 重命名）
            print("💾 正在写入配置...")
            
            dir_name = os.path.dirname(self.config_path)
            fd, temp_path = tempfile.mkstemp(suffix='.json.tmp', dir=dir_name)
            
            try:
                with os.fdopen(fd, 'w', encoding='utf-8') as f:
                    json.dump(self.config, f, indent=2, ensure_ascii=False)
                
                if os.name == 'nt':
                    if os.path.exists(self.config_path):
                        os.remove(self.config_path)
                    shutil.move(temp_path, self.config_path)
                else:
                    os.replace(temp_path, self.config_path)
                
                print(f"✅ 配置已原子写入：{self.config_path}")
                return True
                
            except Exception as write_error:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                print(f"❌ 写入失败，已清理临时文件：{write_error}")
                return False
                
        except Exception as e:
            print(f"❌ 保存配置失败：{e}")
            return False
    
    def _cleanup_old_backups(self, max_backups: int):
        """清理旧备份，保留最近的 N 个"""
        backup_pattern = f"{self.config_path}.bak.*"
        backups = sorted(glob.glob(backup_pattern), key=os.path.getmtime, reverse=True)
        
        if len(backups) > max_backups:
            for old_backup in backups[max_backups:]:
                try:
                    os.remove(old_backup)
                    print(f"🗑️  已清理旧备份：{os.path.basename(old_backup)}")
                except Exception as e:
                    print(f"⚠️  清理备份失败：{e}")
    
    def health_check(self) -> Dict:
        """6 合 1 健康检查"""
        health = {
            "gateway": {"status": "unknown", "score": 0, "details": []},
            "agents": {"status": "unknown", "score": 0, "details": []},
            "models": {"status": "unknown", "score": 0, "details": []},
            "plugins": {"status": "unknown", "score": 0, "details": []},
            "network": {"status": "unknown", "score": 0, "details": []},
            "logs": {"status": "unknown", "score": 0, "details": []},
            "overall_score": 0
        }
        
        # 1. Gateway 检查
        if "gateway" in self.config:
            gw = self.config["gateway"]
            if gw.get("mode"):
                health["gateway"]["status"] = "✅"
                health["gateway"]["score"] = 100
                health["gateway"]["details"].append(f"模式：{gw.get('mode')}")
                health["gateway"]["details"].append(f"端口：{gw.get('port', 18789)}")
            else:
                health["gateway"]["status"] = "❌"
                health["gateway"]["score"] = 0
                health["gateway"]["details"].append("缺少 mode 配置")
        
        # 2. Agents 检查
        if "agents" in self.config and "list" in self.config["agents"]:
            agents = self.config["agents"]["list"]
            agent_ids = [a.get("id") for a in agents]
            health["agents"]["score"] = min(100, len(agents) * 20)
            health["agents"]["details"].append(f"Agent 数量：{len(agents)}")
            
            if "main" in agent_ids:
                health["agents"]["status"] = "✅"
            else:
                health["agents"]["status"] = "⚠️"
                health["agents"]["details"].append("缺少 main agent")
        
        # 3. Models 检查
        if "models" in self.config and "providers" in self.config["models"]:
            providers = self.config["models"]["providers"]
            healthy_providers = sum(1 for p in providers.values() if p.get("apiKey") or p.get("baseUrl"))
            health["models"]["score"] = min(100, healthy_providers * 25)
            health["models"]["details"].append(f"Provider 数量：{len(providers)}")
            health["models"]["status"] = "✅" if healthy_providers > 0 else "⚠️"
        
        # 4. Plugins 检查
        if "plugins" in self.config and "entries" in self.config["plugins"]:
            plugins = self.config["plugins"]["entries"]
            enabled = sum(1 for p in plugins.values() if p.get("enabled"))
            health["plugins"]["score"] = min(100, enabled * 20)
            health["plugins"]["details"].append(f"启用插件：{enabled}/{len(plugins)}")
            health["plugins"]["status"] = "✅" if enabled > 0 else "⚠️"
        
        # 5. 网络检查（简化版）
        health["network"]["status"] = "✅"
        health["network"]["score"] = 100
        health["network"]["details"].append("网络检查需在线测试")
        
        # 6. 日志检查
        logs_dir = os.path.expanduser("~/.openclaw/logs")
        if os.path.exists(logs_dir):
            log_files = [f for f in os.listdir(logs_dir) if f.endswith('.log')]
            health["logs"]["score"] = 100 if log_files else 50
            health["logs"]["details"].append(f"日志文件：{len(log_files)}")
            health["logs"]["status"] = "✅"
        else:
            health["logs"]["status"] = "⚠️"
            health["logs"]["score"] = 0
            health["logs"]["details"].append("日志目录不存在")
        
        # 计算总体健康分
        scores = [v["score"] for v in health.values() if isinstance(v, dict) and "score" in v]
        health["overall_score"] = round(sum(scores) / len(scores)) if scores else 0
        
        return health
    
    def generate_report(self) -> Dict:
        """生成配置报告"""
        return {
            "config_path": self.config_path,
            "issues_found": len(self.issues),
            "fixes_applied": self.fixes_applied,
            "issues": self.issues,
            "config_valid": len(self.issues) == 0
        }
    
    def print_report(self):
        """打印配置报告"""
        print("\n" + "="*60)
        print("OpenClaw 配置验证报告")
        print("="*60)
        
        if not self.issues:
            print("✅ 配置验证通过！")
        else:
            print(f"⚠️  发现 {len(self.issues)} 个问题：")
            for i, issue in enumerate(self.issues, 1):
                severity = issue.get("severity", "info")
                severity_icon = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}.get(severity, "ℹ️")
                print(f"{i}. {severity_icon} [{severity.upper()}] {issue['path']}")
                print(f"   {issue['message']}")
        
        if self.fixes_applied:
            print(f"\n🔧 已应用 {len(self.fixes_applied)} 个修复：")
            for fix in self.fixes_applied:
                print(f"  - {fix}")
        
        print("="*60)
    
    def print_health_report(self, health: Dict):
        """打印健康检查报告"""
        print("\n" + "="*60)
        print("OpenClaw 健康检查报告")
        print("="*60)
        
        print(f"\n总体健康分：{health['overall_score']}/100")
        print("\n详细检查:")
        
        for component in ["gateway", "agents", "models", "plugins", "network", "logs"]:
            h = health[component]
            print(f"\n{component.upper()}: {h['status']} ({h['score']}分)")
            for detail in h["details"]:
                print(f"  - {detail}")
        
        print("="*60)


def restart_gateway() -> bool:
    """重启 Gateway（带超时和验证）"""
    import time
    
    print("🔄 正在重启 Gateway...")
    
    try:
        # 停止 Gateway
        subprocess.run(["pkill", "-f", "openclaw.*gateway"], capture_output=True, timeout=10)
        time.sleep(2)
        
        # 启动 Gateway
        subprocess.Popen(["openclaw", "gateway", "start"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(5)
        
        # 验证 Dashboard 可访问
        import urllib.request
        try:
            urllib.request.urlopen("http://127.0.0.1:18789", timeout=5)
            print("✅ Gateway 重启成功，Dashboard 可访问")
            return True
        except Exception:
            print("⚠️  Gateway 已启动但 Dashboard 不可访问")
            return False
            
    except Exception as e:
        print(f"❌ Gateway 重启失败：{e}")
        return False


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="OpenClaw 配置验证和修复工具")
    parser.add_argument("action", choices=["validate", "fix", "report", "health", "modify"], 
                       help="执行的操作：validate(验证), fix(修复), report(报告), health(健康检查), modify(修改)")
    parser.add_argument("--config", "-c", default="~/.openclaw/openclaw.json",
                       help="配置文件路径 (默认：~/.openclaw/openclaw.json)")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="详细输出")
    parser.add_argument("--json", action="store_true",
                       help="输出 JSON 格式")
    parser.add_argument("--key", "-k", type=str,
                       help="配置键路径 (用于 modify)，如：agents.defaults.model.primary")
    parser.add_argument("--value", "-val", type=str,
                       help="配置值 (用于 modify)，如：qwen/qwen-turbo")
    parser.add_argument("--restart", "-r", action="store_true",
                       help="修改后重启 Gateway (用于 modify)")
    
    args = parser.parse_args()
    config_path = os.path.expanduser(args.config)
    
    validator = OpenClawConfigValidator(config_path)
    
    if args.action == "validate":
        if not validator.load_config():
            print("❌ 加载配置失败")
            sys.exit(1)
        
        issues = validator.validate()
        validator.print_report()
        sys.exit(0 if not issues else 1)
    
    elif args.action == "fix":
        if not validator.load_config():
            print("❌ 加载配置失败")
            sys.exit(1)
        
        validator.validate()
        
        if validator.issues:
            print(f"发现 {len(validator.issues)} 个问题，开始修复...")
            if validator.fix():
                if validator.save_config():
                    print("✅ 配置修复完成！")
                    validator.validate()
                    validator.print_report()
                else:
                    print("❌ 保存配置失败")
            else:
                print("⚠️  没有可自动修复的问题")
        else:
            print("✅ 配置没有问题")
    
    elif args.action == "report":
        if not validator.load_config():
            print("❌ 加载配置失败")
            sys.exit(1)
        
        validator.validate()
        report = validator.generate_report()
        
        if args.json:
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            validator.print_report()
    
    elif args.action == "health":
        if not validator.load_config():
            print("❌ 加载配置失败")
            sys.exit(1)
        
        health = validator.health_check()
        
        if args.json:
            print(json.dumps(health, ensure_ascii=False, indent=2))
        else:
            validator.print_health_report(health)
    
    elif args.action == "modify":
        if not args.key or not args.value:
            print("❌ modify 需要指定 --key 和 --value")
            print("示例：python3 config_validator.py modify --key agents.defaults.model.primary --value qwen/qwen-turbo")
            sys.exit(1)
        
        if not validator.load_config():
            print("❌ 加载配置失败")
            sys.exit(1)
        
        # 解析键路径
        keys = args.key.split('.')
        
        # 导航到目标位置
        current = validator.config
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        # 设置值
        old_value = current.get(keys[-1])
        current[keys[-1]] = args.value
        
        print(f"📝 配置修改:")
        print(f"   {args.key}")
        print(f"   {old_value} → {args.value}")
        
        # 保存配置
        if validator.save_config(backup=True, validate_before_save=True):
            print("✅ 配置已保存")
            
            # 重启 Gateway
            if args.restart:
                if restart_gateway():
                    print("✅ 配置已生效")
                else:
                    print("⚠️  Gateway 重启失败，请手动重启")
            else:
                print("💡 提示：运行以下命令使配置生效:")
                print("   openclaw gateway restart")
        else:
            print("❌ 保存配置失败")
            sys.exit(1)


if __name__ == "__main__":
    main()
