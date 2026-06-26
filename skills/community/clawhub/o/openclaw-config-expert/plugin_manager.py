#!/usr/bin/env python3
"""
OpenClaw插件管理器
管理插件的启用、禁用、配置验证和依赖检查
"""

import json
import os
import sys
from typing import Dict, List, Any, Optional, Set
import re

class OpenClawPluginManager:
    """OpenClaw插件管理工具"""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or os.path.expanduser("~/.openclaw/openclaw.json")
        self.config = None
        self.plugins_config = {}
        
        # 已知插件列表
        self.known_plugins = {
            "feishu": "飞书集成",
            "kimi-claw": "Kimi Claw连接器",
            "kimi-search": "Kimi搜索",
            "wecom-openclaw-plugin": "企业微信插件",
            "openclaw-lark": "Lark/飞书插件",
            "openclaw-weixin": "微信插件",
            "dingtalk-connector": "钉钉连接器",
            "weibo-openclaw-plugin": "微博插件",
            "qwen-portal-auth": "千问门户认证",
            "memory-core": "记忆核心",
            "multi-search-engine": "多搜索引擎",
            "imap-smtp-email": "邮件客户端",
            "himalaya": "Himalaya邮件",
            "smart-router": "智能路由",
            "excel-xlsx": "Excel处理",
            "financial-calculator": "金融计算器",
            "humanizer": "文本人性化",
            "ontology": "本体知识图谱"
        }
        
        # 插件依赖关系
        self.plugin_dependencies = {
            "feishu": [],
            "kimi-claw": [],
            "kimi-search": ["kimi-claw"],
            "wecom-openclaw-plugin": [],
            "openclaw-lark": [],
            "openclaw-weixin": [],
            "dingtalk-connector": [],
            "weibo-openclaw-plugin": [],
            "qwen-portal-auth": [],
            "memory-core": [],
            "multi-search-engine": [],
            "imap-smtp-email": [],
            "himalaya": ["imap-smtp-email"],
            "smart-router": [],
            "excel-xlsx": [],
            "financial-calculator": [],
            "humanizer": [],
            "ontology": ["memory-core"]
        }
        
        # 插件冲突
        self.plugin_conflicts = {
            "feishu": ["openclaw-lark"],  # 飞书和Lark可能有冲突
            "openclaw-lark": ["feishu"],
            "wecom-openclaw-plugin": [],
            "openclaw-weixin": []
        }
    
    def load_config(self) -> bool:
        """加载配置文件"""
        try:
            if not os.path.exists(self.config_path):
                print(f"❌ 配置文件不存在: {self.config_path}")
                return False
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            
            # 提取插件配置
            self.plugins_config = self.config.get("plugins", {}).get("entries", {})
            return True
        except Exception as e:
            print(f"❌ 加载配置失败: {e}")
            return False
    
    def get_enabled_plugins(self) -> Dict[str, Dict]:
        """获取已启用的插件"""
        enabled_plugins = {}
        
        for plugin_id, plugin_config in self.plugins_config.items():
            if plugin_config.get("enabled", False):
                enabled_plugins[plugin_id] = {
                    "config": plugin_config,
                    "name": self.known_plugins.get(plugin_id, plugin_id),
                    "description": self.get_plugin_description(plugin_id)
                }
        
        return enabled_plugins
    
    def get_plugin_description(self, plugin_id: str) -> str:
        """获取插件描述"""
        descriptions = {
            "feishu": "飞书办公套件集成，支持消息、日历、文档等",
            "kimi-claw": "Kimi Claw AI助手连接器",
            "kimi-search": "Kimi智能搜索功能",
            "wecom-openclaw-plugin": "企业微信工作台集成",
            "openclaw-lark": "Lark/飞书国际版集成",
            "openclaw-weixin": "微信个人号集成",
            "dingtalk-connector": "钉钉工作台连接器",
            "weibo-openclaw-plugin": "微博社交平台集成",
            "qwen-portal-auth": "千问模型门户认证",
            "memory-core": "核心记忆系统",
            "multi-search-engine": "多搜索引擎聚合",
            "imap-smtp-email": "IMAP/SMTP邮件客户端",
            "himalaya": "Himalaya命令行邮件工具",
            "smart-router": "智能模型路由系统",
            "excel-xlsx": "Excel文件处理工具",
            "financial-calculator": "金融计算器",
            "humanizer": "AI文本人性化工具",
            "ontology": "本体知识图谱系统"
        }
        return descriptions.get(plugin_id, "未知插件")
    
    def check_dependencies(self, plugin_id: str) -> List[str]:
        """检查插件依赖"""
        missing_deps = []
        
        if plugin_id in self.plugin_dependencies:
            deps = self.plugin_dependencies[plugin_id]
            for dep in deps:
                if dep not in self.plugins_config or not self.plugins_config.get(dep, {}).get("enabled", False):
                    missing_deps.append(dep)
        
        return missing_deps
    
    def check_conflicts(self, plugin_id: str) -> List[str]:
        """检查插件冲突"""
        conflicts = []
        
        if plugin_id in self.plugin_conflicts:
            conflict_list = self.plugin_conflicts[plugin_id]
            for conflict_id in conflict_list:
                if conflict_id in self.plugins_config and self.plugins_config.get(conflict_id, {}).get("enabled", False):
                    conflicts.append(conflict_id)
        
        return conflicts
    
    def validate_plugin_config(self, plugin_id: str, plugin_config: Dict) -> List[Dict]:
        """验证插件配置"""
        issues = []
        
        # 检查必要配置字段
        required_configs = {
            "feishu": ["appId", "appSecret"],
            "kimi-claw": ["config.bridge.token"],
            "wecom-openclaw-plugin": ["corpId", "secret"],
            "openclaw-lark": ["appId", "appSecret"],
            "dingtalk-connector": ["appKey", "appSecret"]
        }
        
        if plugin_id in required_configs:
            for required_field in required_configs[plugin_id]:
                # 支持嵌套字段检查
                value = plugin_config
                for field in required_field.split('.'):
                    if isinstance(value, dict):
                        value = value.get(field)
                    else:
                        value = None
                        break
                
                if not value:
                    issues.append({
                        "type": "missing_config",
                        "field": required_field,
                        "message": f"插件 {plugin_id} 缺少必要配置: {required_field}"
                    })
        
        # 检查配置格式
        if plugin_id == "feishu" and plugin_config.get("enabled", False):
            app_id = plugin_config.get("appId", "")
            app_secret = plugin_config.get("appSecret", "")
            
            if not app_id.startswith("cli_"):
                issues.append({
                    "type": "invalid_format",
                    "field": "appId",
                    "message": "飞书appId应以'cli_'开头"
                })
            
            if len(app_secret) < 20:
                issues.append({
                    "type": "invalid_format",
                    "field": "appSecret",
                    "message": "飞书appSecret过短，可能无效"
                })
        
        return issues
    
    def enable_plugin(self, plugin_id: str, config: Dict = None) -> Dict:
        """启用插件"""
        result = {
            "success": False,
            "plugin_id": plugin_id,
            "issues": [],
            "warnings": [],
            "actions_taken": []
        }
        
        # 检查插件是否已知
        if plugin_id not in self.known_plugins:
            result["issues"].append({
                "type": "unknown_plugin",
                "message": f"未知插件: {plugin_id}"
            })
            return result
        
        # 检查依赖
        missing_deps = self.check_dependencies(plugin_id)
        if missing_deps:
            result["issues"].append({
                "type": "missing_dependencies",
                "message": f"缺少依赖插件: {', '.join(missing_deps)}",
                "dependencies": missing_deps
            })
        
        # 检查冲突
        conflicts = self.check_conflicts(plugin_id)
        if conflicts:
            result["warnings"].append({
                "type": "plugin_conflict",
                "message": f"与以下插件可能存在冲突: {', '.join(conflicts)}",
                "conflicts": conflicts
            })
        
        # 验证配置
        plugin_config = config or {"enabled": True}
        config_issues = self.validate_plugin_config(plugin_id, plugin_config)
        result["issues"].extend(config_issues)
        
        # 如果没有问题，启用插件
        if not result["issues"]:
            if "plugins" not in self.config:
                self.config["plugins"] = {"entries": {}}
            
            if "entries" not in self.config["plugins"]:
                self.config["plugins"]["entries"] = {}
            
            self.config["plugins"]["entries"][plugin_id] = plugin_config
            result["actions_taken"].append(f"已启用插件: {plugin_id}")
            result["success"] = True
        
        return result
    
    def disable_plugin(self, plugin_id: str) -> Dict:
        """禁用插件"""
        result = {
            "success": False,
            "plugin_id": plugin_id,
            "actions_taken": []
        }
        
        if plugin_id in self.plugins_config:
            # 检查是否有其他插件依赖此插件
            dependent_plugins = []
            for other_id, deps in self.plugin_dependencies.items():
                if plugin_id in deps and other_id in self.plugins_config and self.plugins_config[other_id].get("enabled", False):
                    dependent_plugins.append(other_id)
            
            if dependent_plugins:
                result["success"] = False
                result["issues"] = [{
                    "type": "has_dependents",
                    "message": f"以下插件依赖此插件: {', '.join(dependent_plugins)}",
                    "dependents": dependent_plugins
                }]
            else:
                # 禁用插件
                if plugin_id in self.config.get("plugins", {}).get("entries", {}):
                    self.config["plugins"]["entries"][plugin_id]["enabled"] = False
                    result["actions_taken"].append(f"已禁用插件: {plugin_id}")
                    result["success"] = True
        else:
            result["issues"] = [{
                "type": "plugin_not_found",
                "message": f"插件未找到: {plugin_id}"
            }]
        
        return result
    
    def generate_plugin_report(self) -> Dict:
        """生成插件报告"""
        enabled_plugins = self.get_enabled_plugins()
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_plugins": len(self.plugins_config),
            "enabled_plugins": len(enabled_plugins),
            "disabled_plugins": len(self.plugins_config) - len(enabled_plugins),
            "plugins": []
        }
        
        for plugin_id, plugin_config in self.plugins_config.items():
            plugin_info = {
                "id": plugin_id,
                "name": self.known_plugins.get(plugin_id, plugin_id),
                "enabled": plugin_config.get("enabled", False),
                "description": self.get_plugin_description(plugin_id),
                "dependencies": self.plugin_dependencies.get(plugin_id, []),
                "conflicts": self.plugin_conflicts.get(plugin_id, []),
                "issues": self.validate_plugin_config(plugin_id, plugin_config)
            }
            
            # 检查依赖状态
            missing_deps = self.check_dependencies(plugin_id)
            if missing_deps:
                plugin_info["dependency_issues"] = {
                    "missing": missing_deps,
                    "message": f"缺少依赖: {', '.join(missing_deps)}"
                }
            
            # 检查冲突
            conflicts = self.check_conflicts(plugin_id)
            if conflicts:
                plugin_info["conflict_issues"] = {
                    "conflicts": conflicts,
                    "message": f"与以下插件冲突: {', '.join(conflicts)}"
                }
            
            report["plugins"].append(plugin_info)
        
        return report
    
    def save_config(self) -> bool:
        """保存配置文件"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ 保存配置失败: {e}")
            return False
    
    def display_report(self, report: Dict = None):
        """显示插件报告"""
        if not report:
            report = self.generate_plugin_report()
        
        print("╔══════════════════════════════════════════════════════════╗")
        print("║                 OpenClaw插件管理器                       ║")
        print("║                插件状态与配置分析                         ║")
        print("╚══════════════════════════════════════════════════════════╝")
        print()
        
        print(f"📊 插件统计:")
        print(f"   总插件数: {report['total_plugins']}")
        print(f"   已启用: {report['enabled_plugins']} 🟢")
        print(f"   未启用: {report['disabled_plugins']} ⚫")
        print()
        
        print("🔌 已启用插件:")
        for plugin in report["plugins"]:
            if plugin["enabled"]:
                status = "🟢" if not plugin.get("issues") and not plugin.get("dependency_issues") else "🟡"
                print(f"   {status} {plugin['name']} ({plugin['id']})")
                
                if plugin.get("issues"):
                    print(f"      ⚠️ 配置问题: {len(plugin['issues'])}个")
                
                if plugin.get("dependency_issues"):
                    print(f"      ⚠️ 依赖问题: {plugin['dependency_issues']['message']}")
        
        print()
        print("⚫ 未启用插件:")
        for plugin in report["plugins"]:
            if not plugin["enabled"]:
                print(f"   ⚫ {plugin['name']} ({plugin['id']})")
        
        print()
        print("💡 建议:")
        
        # 生成建议
        suggestions = []
        
        # 检查配置问题
        config_issues = sum(len(p.get("issues", [])) for p in report["plugins"] if p["enabled"])
        if config_issues > 0:
            suggestions.append(f"修复 {config_issues} 个插件配置问题")
        
        # 检查依赖问题
        dep_issues = sum(1 for p in report["plugins"] if p.get("dependency_issues") and p["enabled"])
        if dep_issues > 0:
            suggestions.append(f"解决 {dep_issues} 个插件依赖问题")
        
        # 检查冲突
        conflict_issues = sum(1 for p in report["plugins"] if p.get("conflict_issues") and p["enabled"])
        if conflict_issues > 0:
            suggestions.append(f"处理 {conflict_issues} 个插件冲突")
        
        if not suggestions:
            suggestions.append("插件配置良好，无需操作")
        
        for suggestion in suggestions:
            print(f"   • {suggestion}")
        
        print()
        print(f"⏰ 报告时间: {report['timestamp']}")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="OpenClaw插件管理器")
    parser.add_argument("--config", help="配置文件路径", default="~/.openclaw/openclaw.json")
    parser.add_argument("--report", action="store_true", help="生成插件报告")
    parser.add_argument("--enable", help="启用指定插件")
    parser.add_argument("--disable", help="禁用指定插件")
    parser.add_argument("--list", action="store_true", help="列出所有插件")
    
    args = parser.parse_args()
    
    manager = OpenClawPluginManager(args.config)
    
    if not manager.load_config():
        sys.exit(1)
    
    if args.report:
        report = manager.generate_plugin_report()
        manager.display_report(report)
    
    elif args.enable:
        result = manager.enable_plugin(args.enable)
        if result["success"]:
            print(f"✅ 成功启用插件: {args.enable}")
            if manager.save_config():
                print("✅ 配置已保存")
            else:
                print("❌ 配置保存失败")
        else:
            print(f"❌ 启用插件失败: {args.enable}")
            for issue in result.get("issues", []):
                print(f"   ⚠️ {issue['message']}")
    
    elif args.disable:
        result = manager.disable_plugin(args.disable)
        if result["success"]:
            print(f"✅ 成功禁用插件: {args.disable}")
            if manager.save_config():
                print("✅ 配置已保存")
            else:
                print("❌ 配置保存失败")
        else:
            print(f"❌ 禁用插件失败: {args.disable}")
            for issue in result.get("issues", []):
                print(f"   ⚠️ {issue['message']}")
    
    elif args.list:
        enabled_plugins = manager.get_enabled_plugins()
        print("📋 插件列表:")
        print(f"已启用 ({len(enabled_plugins)}):")
        for plugin_id, plugin_info in enabled_plugins.items():
            print(f"  🟢 {plugin_info['name']} ({plugin_id})")
        
        all_plugins = set(manager.known_plugins.keys())
        disabled_plugins = all_plugins - set(enabled_plugins.keys())
        print(f"\n未启用 ({len(disabled_plugins)}):")
        for plugin_id in sorted(disabled_plugins):
            print(f"  ⚫ {manager.known_plugins[plugin_id]} ({plugin_id})")
    
    else:
        # 默认显示报告
        report = manager.generate_plugin_report()
        manager.display_report(report)

if __name__ == "__main__":
    main()