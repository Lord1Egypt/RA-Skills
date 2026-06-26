#!/usr/bin/env python3
"""
OpenClaw配置专家 - 主入口脚本
整合配置验证、Agent优化、模型路由、插件管理、版本迁移等功能
"""

import os
import sys
import json
import argparse
from datetime import datetime

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="OpenClaw配置专家系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s validate           # 验证配置
  %(prog)s fix                # 修复配置问题
  %(prog)s optimize-agents    # 优化Agent配置
  %(prog)s check-plugins      # 检查插件状态
  %(prog)s migrate            # 版本迁移
  %(prog)s wizard             # 交互式配置向导
  %(prog)s report             # 生成配置报告
        """
    )
    
    parser.add_argument("command", nargs="?", help="执行命令")
    parser.add_argument("--config", help="配置文件路径", default="~/.openclaw/openclaw.json")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    parser.add_argument("--output", help="输出文件路径")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    config_path = os.path.expanduser(args.config)
    
    print("╔══════════════════════════════════════════════════════════╗")
    print("║               OpenClaw配置专家系统                       ║")
    print("║              智能配置管理与优化                           ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()
    
    # 根据命令执行相应功能
    if args.command == "validate":
        from config_validator import OpenClawConfigValidator
        validator = OpenClawConfigValidator(config_path)
        if validator.load_config():
            issues = validator.validate()
            if issues:
                print(f"⚠️  发现 {len(issues)} 个配置问题:")
                for issue in issues:
                    print(f"   {issue['type'].upper()}: {issue['message']}")
                    if args.verbose and 'details' in issue:
                        print(f"     详情: {issue['details']}")
            else:
                print("✅ 配置验证通过，无问题")
        else:
            print("❌ 加载配置失败")
    
    elif args.command == "fix":
        from config_validator import OpenClawConfigValidator
        validator = OpenClawConfigValidator(config_path)
        if validator.load_config():
            fixed = validator.fix_common_issues()
            if fixed:
                print(f"✅ 修复了 {len(fixed)} 个问题:")
                for fix in fixed:
                    print(f"   ✅ {fix['message']}")
                
                if validator.save_config():
                    print("✅ 配置已保存")
                else:
                    print("❌ 配置保存失败")
            else:
                print("✅ 无需修复，配置正常")
        else:
            print("❌ 加载配置失败")
    
    elif args.command == "optimize-agents":
        from agent_optimizer import OpenClawAgentOptimizer
        optimizer = OpenClawAgentOptimizer(config_path)
        if optimizer.load_config():
            optimizations = optimizer.optimize_agents()
            if optimizations:
                print(f"🎯 提供了 {len(optimizations)} 个优化建议:")
                for opt in optimizations:
                    print(f"   💡 {opt['message']}")
                    if 'action' in opt:
                        print(f"      操作: {opt['action']}")
            else:
                print("✅ Agent配置已优化，无需调整")
        else:
            print("❌ 加载配置失败")
    
    elif args.command == "check-plugins":
        from plugin_manager import OpenClawPluginManager
        manager = OpenClawPluginManager(config_path)
        if manager.load_config():
            report = manager.generate_plugin_report()
            manager.display_report(report)
        else:
            print("❌ 加载配置失败")
    
    elif args.command == "migrate":
        from version_migrator import OpenClawVersionMigrator
        migrator = OpenClawVersionMigrator(config_path)
        if migrator.load_config():
            result = migrator.migrate_to_version()
            migrator.display_migration_summary(result)
            
            if result["success"]:
                if migrator.save_config():
                    print("✅ 配置已保存")
                else:
                    print("❌ 配置保存失败")
        else:
            print("❌ 加载配置失败")
    
    elif args.command == "wizard":
        print("🚧 交互式配置向导正在开发中...")
        print()
        print("💡 当前可用的替代方案:")
        print("   1. 使用模板: 查看 config_templates/ 目录")
        print("   2. 验证配置: openclaw-config-expert validate")
        print("   3. 优化Agent: openclaw-config-expert optimize-agents")
    
    elif args.command == "report":
        print("📊 生成配置报告中...")
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "config_path": config_path,
            "sections": []
        }
        
        # 验证报告
        try:
            from config_validator import OpenClawConfigValidator
            validator = OpenClawConfigValidator(config_path)
            if validator.load_config():
                issues = validator.validate()
                report["sections"].append({
                    "name": "配置验证",
                    "issues": len(issues),
                    "status": "✅ 通过" if not issues else f"⚠️ {len(issues)}个问题"
                })
        except:
            report["sections"].append({
                "name": "配置验证",
                "status": "❌ 失败"
            })
        
        # 插件报告
        try:
            from plugin_manager import OpenClawPluginManager
            manager = OpenClawPluginManager(config_path)
            if manager.load_config():
                plugin_report = manager.generate_plugin_report()
                report["sections"].append({
                    "name": "插件管理",
                    "enabled_plugins": plugin_report["enabled_plugins"],
                    "total_plugins": plugin_report["total_plugins"],
                    "status": f"✅ {plugin_report['enabled_plugins']}/{plugin_report['total_plugins']}启用"
                })
        except:
            report["sections"].append({
                "name": "插件管理",
                "status": "❌ 失败"
            })
        
        # 版本报告
        try:
            from version_migrator import OpenClawVersionMigrator
            migrator = OpenClawVersionMigrator(config_path)
            if migrator.load_config():
                needs = migrator.analyze_migration_needs()
                report["sections"].append({
                    "name": "版本兼容",
                    "current_version": migrator.current_version,
                    "migration_needs": len(needs),
                    "status": "✅ 最新" if not needs else f"⚠️ {len(needs)}个迁移需求"
                })
        except:
            report["sections"].append({
                "name": "版本兼容",
                "status": "❌ 失败"
            })
        
        # 显示报告
        print()
        print("📋 配置报告摘要:")
        for section in report["sections"]:
            print(f"   {section['name']}: {section['status']}")
        
        # 保存报告
        if args.output:
            output_path = args.output
        else:
            output_path = f"{config_path}.report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📄 完整报告已保存到: {output_path}")
    
    elif args.command == "list-templates":
        templates_dir = os.path.join(os.path.dirname(__file__), "config_templates")
        if os.path.exists(templates_dir):
            print("📁 可用配置模板:")
            for file in sorted(os.listdir(templates_dir)):
                if file.endswith(".json"):
                    template_path = os.path.join(templates_dir, file)
                    try:
                        with open(template_path, 'r', encoding='utf-8') as f:
                            template = json.load(f)
                            description = template.get("description", "无描述")
                            print(f"   📄 {file}: {description}")
                    except:
                        print(f"   📄 {file}: (无法读取)")
        else:
            print("❌ 模板目录不存在")
    
    elif args.command == "apply-template":
        if len(sys.argv) < 3:
            print("❌ 请指定模板名称")
            print("   用法: openclaw-config-expert apply-template <template_name>")
            print("   示例: openclaw-config-expert apply-template standard")
            return
        
        template_name = sys.argv[2]
        template_file = f"{template_name}.json"
        template_path = os.path.join(os.path.dirname(__file__), "config_templates", template_file)
        
        if not os.path.exists(template_path):
            print(f"❌ 模板不存在: {template_file}")
            print("   可用模板:")
            templates_dir = os.path.join(os.path.dirname(__file__), "config_templates")
            for file in sorted(os.listdir(templates_dir)):
                if file.endswith(".json"):
                    print(f"   - {file.replace('.json', '')}")
            return
        
        # 备份当前配置
        backup_path = f"{config_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        import shutil
        if os.path.exists(config_path):
            shutil.copy2(config_path, backup_path)
            print(f"✅ 已备份当前配置到: {backup_path}")
        
        # 应用模板
        try:
            shutil.copy2(template_path, config_path)
            print(f"✅ 已应用模板: {template_name}")
            print(f"📄 新配置: {config_path}")
            
            # 显示模板信息
            with open(template_path, 'r', encoding='utf-8') as f:
                template = json.load(f)
                description = template.get("description", "无描述")
                print(f"📝 模板描述: {description}")
        except Exception as e:
            print(f"❌ 应用模板失败: {e}")
    
    else:
        print(f"❌ 未知命令: {args.command}")
        print()
        print("可用命令:")
        print("  validate          验证配置")
        print("  fix               修复配置问题")
        print("  optimize-agents   优化Agent配置")
        print("  check-plugins     检查插件状态")
        print("  migrate           版本迁移")
        print("  wizard            交互式配置向导")
        print("  report            生成配置报告")
        print("  list-templates    列出可用模板")
        print("  apply-template    应用配置模板")
    
    print()
    print("💡 更多帮助: python3 openclaw_config_expert.py --help")

if __name__ == "__main__":
    main()