#!/usr/bin/env python3
"""
OpenClaw版本迁移器
处理OpenClaw不同版本间的配置迁移
"""

import json
import os
import sys
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

class OpenClawVersionMigrator:
    """OpenClaw版本迁移工具"""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or os.path.expanduser("~/.openclaw/openclaw.json")
        self.config = None
        self.current_version = None
        self.target_version = "2026.4.15"  # 最新稳定版本
        
        # 版本变更历史
        self.version_changes = {
            "2026.4.15": {
                "description": "简化memory配置，增强插件系统",
                "changes": [
                    {
                        "type": "deprecated",
                        "field": "memory.system",
                        "message": "memory.system字段已废弃",
                        "action": "remove"
                    },
                    {
                        "type": "deprecated",
                        "field": "memory.fusion_manager",
                        "message": "memory.fusion_manager字段已废弃",
                        "action": "remove"
                    },
                    {
                        "type": "deprecated",
                        "field": "memory.config",
                        "message": "memory.config字段已废弃",
                        "action": "remove"
                    },
                    {
                        "type": "deprecated",
                        "field": "memory.data_dir",
                        "message": "memory.data_dir字段已废弃",
                        "action": "remove"
                    },
                    {
                        "type": "deprecated",
                        "field": "memory.vector_store",
                        "message": "memory.vector_store字段已废弃",
                        "action": "remove"
                    },
                    {
                        "type": "deprecated",
                        "field": "memory.embedding",
                        "message": "memory.embedding字段已废弃",
                        "action": "remove"
                    },
                    {
                        "type": "deprecated",
                        "field": "memory.llm",
                        "message": "memory.llm字段已废弃",
                        "action": "remove"
                    },
                    {
                        "type": "deprecated",
                        "field": "memory.protected_paths",
                        "message": "memory.protected_paths字段已废弃",
                        "action": "remove"
                    },
                    {
                        "type": "deprecated",
                        "field": "memory.rules",
                        "message": "memory.rules字段已废弃",
                        "action": "remove"
                    },
                    {
                        "type": "deprecated",
                        "field": "memory.agent_backup",
                        "message": "memory.agent_backup字段已废弃",
                        "action": "remove"
                    },
                    {
                        "type": "new",
                        "field": "session.store",
                        "message": "新增session.store字段，推荐使用'.openclaw-memory'",
                        "action": "add",
                        "default": ".openclaw-memory"
                    },
                    {
                        "type": "new",
                        "field": "channels.feishu.dedupStore",
                        "message": "新增dedupStore字段，推荐使用'.openclaw-memory'",
                        "action": "add",
                        "default": ".openclaw-memory"
                    }
                ]
            },
            "2026.3.13": {
                "description": "改进Agent配置，增强模型路由",
                "changes": [
                    {
                        "type": "deprecated",
                        "field": "agents.defaults.concurrency",
                        "message": "agents.defaults.concurrency字段已废弃",
                        "action": "remove"
                    },
                    {
                        "type": "deprecated", 
                        "field": "bindings.match.pattern",
                        "message": "bindings.match.pattern字段已废弃",
                        "action": "remove"
                    },
                    {
                        "type": "new",
                        "field": "agents.defaults.model",
                        "message": "新增agents.defaults.model字段",
                        "action": "add",
                        "default": {"primary": "deepseek/deepseek-chat"}
                    }
                ]
            },
            "2026.2.28": {
                "description": "初始版本，基础配置结构",
                "changes": []
            }
        }
    
    def load_config(self) -> bool:
        """加载配置文件"""
        try:
            if not os.path.exists(self.config_path):
                print(f"❌ 配置文件不存在: {self.config_path}")
                return False
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            
            # 检测当前版本
            self.current_version = self.detect_version()
            return True
        except Exception as e:
            print(f"❌ 加载配置失败: {e}")
            return False
    
    def detect_version(self) -> str:
        """检测配置版本"""
        # 从meta字段获取版本
        if "meta" in self.config and "lastTouchedVersion" in self.config["meta"]:
            return self.config["meta"]["lastTouchedVersion"]
        
        # 根据配置特征推断版本
        if "memory" in self.config and "system" in self.config.get("memory", {}):
            # 有复杂的memory配置，可能是旧版本
            return "2026.3.13"
        
        # 默认返回最新版本
        return self.target_version
    
    def get_version_info(self, version: str) -> Dict:
        """获取版本信息"""
        return self.version_changes.get(version, {
            "description": "未知版本",
            "changes": []
        })
    
    def analyze_migration_needs(self) -> List[Dict]:
        """分析迁移需求"""
        if not self.current_version:
            return []
        
        needs = []
        
        # 获取从当前版本到目标版本的所有变更
        versions = list(self.version_changes.keys())
        current_index = versions.index(self.current_version) if self.current_version in versions else 0
        target_index = versions.index(self.target_version) if self.target_version in versions else len(versions) - 1
        
        if current_index < target_index:
            # 需要升级
            for i in range(current_index, target_index):
                version = versions[i + 1]  # 下一个版本
                version_info = self.get_version_info(version)
                
                for change in version_info["changes"]:
                    if change["type"] == "deprecated":
                        # 检查是否还存在废弃字段
                        if self.field_exists(change["field"]):
                            needs.append({
                                "type": "deprecated_field",
                                "version": version,
                                "field": change["field"],
                                "message": change["message"],
                                "action": change["action"]
                            })
                    elif change["type"] == "new":
                        # 检查是否缺少新字段
                        if not self.field_exists(change["field"]):
                            needs.append({
                                "type": "missing_field",
                                "version": version,
                                "field": change["field"],
                                "message": change["message"],
                                "action": change["action"],
                                "default": change.get("default")
                            })
        
        return needs
    
    def field_exists(self, field_path: str) -> bool:
        """检查字段是否存在"""
        if not self.config:
            return False
        
        parts = field_path.split('.')
        current = self.config
        
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return False
        
        return True
    
    def remove_field(self, field_path: str) -> bool:
        """删除字段"""
        if not self.config:
            return False
        
        parts = field_path.split('.')
        current = self.config
        
        # 遍历到倒数第二个部分
        for i, part in enumerate(parts[:-1]):
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return False
        
        # 删除最后一个字段
        last_part = parts[-1]
        if isinstance(current, dict) and last_part in current:
            del current[last_part]
            return True
        
        return False
    
    def add_field(self, field_path: str, default_value: Any = None) -> bool:
        """添加字段"""
        if not self.config:
            return False
        
        parts = field_path.split('.')
        current = self.config
        
        # 创建路径
        for i, part in enumerate(parts[:-1]):
            if part not in current:
                current[part] = {}
            current = current[part]
            if not isinstance(current, dict):
                # 路径冲突，无法创建
                return False
        
        # 设置字段值
        last_part = parts[-1]
        if last_part not in current:
            current[last_part] = default_value
            return True
        
        return False
    
    def migrate_to_version(self, target_version: str = None) -> Dict:
        """迁移到指定版本"""
        if target_version:
            self.target_version = target_version
        
        result = {
            "success": False,
            "current_version": self.current_version,
            "target_version": self.target_version,
            "migration_needs": [],
            "actions_taken": [],
            "errors": []
        }
        
        # 分析迁移需求
        needs = self.analyze_migration_needs()
        result["migration_needs"] = needs
        
        if not needs:
            result["success"] = True
            result["message"] = "配置已是最新版本，无需迁移"
            return result
        
        # 执行迁移
        for need in needs:
            try:
                if need["type"] == "deprecated_field" and need["action"] == "remove":
                    if self.remove_field(need["field"]):
                        result["actions_taken"].append({
                            "action": "remove",
                            "field": need["field"],
                            "message": f"已删除废弃字段: {need['field']}"
                        })
                    else:
                        result["errors"].append({
                            "error": "remove_failed",
                            "field": need["field"],
                            "message": f"删除字段失败: {need['field']}"
                        })
                
                elif need["type"] == "missing_field" and need["action"] == "add":
                    default_value = need.get("default")
                    if self.add_field(need["field"], default_value):
                        result["actions_taken"].append({
                            "action": "add",
                            "field": need["field"],
                            "value": default_value,
                            "message": f"已添加新字段: {need['field']} = {default_value}"
                        })
                    else:
                        result["errors"].append({
                            "error": "add_failed",
                            "field": need["field"],
                            "message": f"添加字段失败: {need['field']}"
                        })
            
            except Exception as e:
                result["errors"].append({
                    "error": "exception",
                    "field": need.get("field", "unknown"),
                    "message": f"迁移过程中发生异常: {str(e)}"
                })
        
        # 更新版本信息
        if "meta" not in self.config:
            self.config["meta"] = {}
        
        self.config["meta"]["lastTouchedVersion"] = self.target_version
        self.config["meta"]["lastTouchedAt"] = datetime.now().isoformat()
        self.config["meta"]["migratedFrom"] = self.current_version
        
        result["success"] = len(result["errors"]) == 0
        return result
    
    def save_config(self) -> bool:
        """保存配置文件"""
        try:
            # 创建备份
            backup_path = f"{self.config_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            import shutil
            shutil.copy2(self.config_path, backup_path)
            
            # 保存新配置
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"❌ 保存配置失败: {e}")
            return False
    
    def generate_migration_report(self, migration_result: Dict) -> str:
        """生成迁移报告"""
        report = f"""# OpenClaw配置迁移报告

## 迁移摘要
- **源版本**: {migration_result['current_version']}
- **目标版本**: {migration_result['target_version']}
- **迁移状态**: {"✅ 成功" if migration_result['success'] else "❌ 失败"}
- **迁移时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 迁移需求分析
发现 {len(migration_result['migration_needs'])} 个迁移需求:

"""
        
        for need in migration_result["migration_needs"]:
            if need["type"] == "deprecated_field":
                report += f"- ❌ **废弃字段**: {need['field']}\n"
                report += f"  - 原因: {need['message']}\n"
                report += f"  - 操作: {need['action']}\n"
            elif need["type"] == "missing_field":
                report += f"- ✅ **缺失字段**: {need['field']}\n"
                report += f"  - 原因: {need['message']}\n"
                report += f"  - 操作: {need['action']} (默认值: {need.get('default', '无')})\n"
        
        report += "\n## 执行操作\n"
        
        if migration_result["actions_taken"]:
            for action in migration_result["actions_taken"]:
                report += f"- ✅ {action['message']}\n"
        else:
            report += "- 无操作执行\n"
        
        report += "\n## 错误信息\n"
        
        if migration_result["errors"]:
            for error in migration_result["errors"]:
                report += f"- ❌ {error['message']}\n"
        else:
            report += "- 无错误\n"
        
        report += f"""
## 建议

### 迁移后检查
1. **验证配置**: 运行 `openclaw config validate` 验证新配置
2. **测试功能**: 启动Gateway测试核心功能
3. **检查插件**: 验证所有插件正常工作
4. **备份配置**: 建议保留备份文件

### 新版本特性
**{self.target_version} 版本主要改进:**
{self.get_version_info(self.target_version).get('description', '无描述')}

### 故障排除
如果迁移后出现问题:
1. 恢复备份: `cp {self.config_path}.backup.* {self.config_path}`
2. 手动修复: 根据错误信息调整配置
3. 寻求帮助: 查看OpenClaw文档或社区

---

**注意**: 迁移过程中已创建备份文件，如需恢复请使用最新的备份文件。
"""
        
        return report
    
    def display_migration_summary(self, migration_result: Dict):
        """显示迁移摘要"""
        print("╔══════════════════════════════════════════════════════════╗")
        print("║               OpenClaw版本迁移器                         ║")
        print("║              配置升级与兼容性处理                         ║")
        print("╚══════════════════════════════════════════════════════════╝")
        print()
        
        print(f"📊 迁移信息:")
        print(f"   当前版本: {migration_result['current_version']}")
        print(f"   目标版本: {migration_result['target_version']}")
        print(f"   迁移状态: {'✅ 成功' if migration_result['success'] else '❌ 失败'}")
        print()
        
        print(f"🔍 迁移需求: {len(migration_result['migration_needs'])} 个")
        for need in migration_result["migration_needs"]:
            if need["type"] == "deprecated_field":
                print(f"   ❌ {need['field']} - {need['message']}")
            elif need["type"] == "missing_field":
                print(f"   ✅ {need['field']} - {need['message']}")
        
        print()
        print(f"🛠️  执行操作: {len(migration_result['actions_taken'])} 个")
        for action in migration_result["actions_taken"]:
            print(f"   ✅ {action['message']}")
        
        print()
        if migration_result["errors"]:
            print(f"⚠️  错误: {len(migration_result['errors'])} 个")
            for error in migration_result["errors"]:
                print(f"   ❌ {error['message']}")
        else:
            print("✅ 无错误")
        
        print()
        print("💡 建议:")
        if migration_result["success"]:
            print("   1. 验证配置: openclaw config validate")
            print("   2. 重启Gateway: openclaw gateway restart")
            print("   3. 测试核心功能")
        else:
            print("   1. 检查错误信息")
            print("   2. 手动修复配置")
            print("   3. 或恢复备份文件")
        
        print()
        print(f"📁 完整报告: 已保存到迁移报告文件")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="OpenClaw版本迁移器")
    parser.add_argument("--config", help="配置文件路径", default="~/.openclaw/openclaw.json")
    parser.add_argument("--analyze", action="store_true", help="分析迁移需求")
    parser.add_argument("--migrate", action="store_true", help="执行迁移")
    parser.add_argument("--target", help="目标版本", default="2026.4.15")
    parser.add_argument("--report", help="生成迁移报告文件")
    
    args = parser.parse_args()
    
    migrator = OpenClawVersionMigrator(args.config)
    
    if not migrator.load_config():
        sys.exit(1)
    
    print(f"🔍 检测到当前版本: {migrator.current_version}")
    print(f"🎯 目标版本: {args.target}")
    
    if args.analyze:
        needs = migrator.analyze_migration_needs()
        if needs:
            print(f"⚠️  发现 {len(needs)} 个迁移需求:")
            for need in needs:
                if need["type"] == "deprecated_field":
                    print(f"   ❌ {need['field']} - {need['message']}")
                elif need["type"] == "missing_field":
                    print(f"   ✅ {need['field']} - {need['message']}")
        else:
            print("✅ 配置已是最新版本，无需迁移")
    
    elif args.migrate:
        print("🔄 开始迁移...")
        result = migrator.migrate_to_version(args.target)
        
        migrator.display_migration_summary(result)
        
        if result["success"]:
            if migrator.save_config():
                print("✅ 配置已保存")
                
                # 生成报告
                report = migrator.generate_migration_report(result)
                if args.report:
                    report_file = args.report
                else:
                    report_file = f"{migrator.config_path}.migration_report.md"
                
                with open(report_file, 'w', encoding='utf-8') as f:
                    f.write(report)
                print(f"📄 迁移报告已保存到: {report_file}")
            else:
                print("❌ 配置保存失败")
        else:
            print("❌ 迁移失败，请检查错误信息")
    
    else:
        # 默认显示分析结果
        needs = migrator.analyze_migration_needs()
        if needs:
            print(f"⚠️  发现 {len(needs)} 个迁移需求，建议执行迁移:")
            for need in needs[:5]:  # 显示前5个
                if need["type"] == "deprecated_field":
                    print(f"   ❌ {need['field']}")
                elif need["type"] == "missing_field":
                    print(f"   ✅ {need['field']}")
            
            if len(needs) > 5:
                print(f"   ... 还有 {len(needs) - 5} 个需求")
            
            print("\n💡 执行迁移命令: python3 version_migrator.py --migrate")
        else:
            print("✅ 配置已是最新版本，无需迁移")

if __name__ == "__main__":
    main()
