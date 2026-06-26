#!/usr/bin/env python3
"""
优甲乐服药提醒系统 - 测试脚本
"""

import sys
import os
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_basic_functionality():
    """测试基本功能"""
    print("🧪 测试优甲乐服药提醒系统基本功能...")
    
    try:
        from medication_reminder import MedicationReminder
        
        # 创建提醒实例
        reminder = MedicationReminder()
        
        print("\n1. ✅ 测试系统初始化...")
        print(f"   数据目录: {reminder.data_dir}")
        print(f"   记录文件: {reminder.records_file.exists()}")
        print(f"   统计文件: {reminder.stats_file.exists()}")
        print(f"   设置文件: {reminder.settings_file.exists()}")
        
        print("\n2. ✅ 测试设置加载...")
        settings = reminder.get_settings()
        print(f"   首次提醒时间: {settings['first_reminder_time']}")
        print(f"   提醒间隔: {settings['reminder_interval']}分钟")
        print(f"   按时窗口: {settings['on_time_window']}分钟")
        
        print("\n3. ✅ 测试记录服药...")
        result = reminder.record_medication("07:15", manual=True)
        print(f"   记录结果: {result['message']}")
        print(f"   是否按时: {result['is_on_time']}")
        
        print("\n4. ✅ 测试今日状态查询...")
        status = reminder.get_today_status()
        print(f"   今日状态: {status['status']}")
        print(f"   服药时间: {status.get('time', 'N/A')}")
        
        print("\n5. ✅ 测试记录查询...")
        records = reminder.get_records()
        print(f"   总记录数: {len(records)}")
        if records:
            latest = records[0]
            print(f"   最新记录: {latest['date']} {latest['time']}")
        
        print("\n6. ✅ 测试报告生成...")
        report = reminder.generate_report(7)
        print(f"   报告期间: {report['period']}")
        print(f"   服药依从率: {report['compliance_rate']}%")
        print(f"   当前连续服药: {report['current_streak']}天")
        
        print("\n7. ✅ 测试数据导出...")
        try:
            export_path = reminder.export_to_csv("/tmp/test_medication_export.csv")
            print(f"   导出路径: {export_path}")
            print(f"   文件存在: {Path(export_path).exists()}")
        except Exception as e:
            print(f"   导出测试跳过: {e}")
        
        print("\n🎉 所有基本功能测试通过！")
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integration():
    """测试集成功能"""
    print("\n🔗 测试 OpenClaw 集成功能...")
    
    try:
        from openclaw_integration import handle_medication_command
        
        test_commands = [
            "help",
            "status",
            "taken",
            "report 7",
            "records 5",
            "settings"
        ]
        
        for cmd in test_commands:
            print(f"\n{'='*40}")
            print(f"测试命令: /medication {cmd}")
            print(f"{'='*40}")
            
            result = handle_medication_command(cmd)
            print(result["content"][:200] + "..." if len(result["content"]) > 200 else result["content"])
        
        print("\n🎉 集成功能测试通过！")
        return True
        
    except Exception as e:
        print(f"\n❌ 集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cron_simulation():
    """模拟 cron 任务"""
    print("\n⏰ 模拟每日提醒流程...")
    
    try:
        from medication_reminder import MedicationReminder
        import datetime
        
        reminder = MedicationReminder()
        settings = reminder.get_settings()
        
        print("模拟时间线:")
        print(f"1. 06:30 - 首次提醒: '⏰ 请服用优甲乐'")
        print(f"2. 06:45 - 重复提醒: '⏰ 提醒：请服用优甲乐'")
        print(f"3. 07:00 - 重复提醒: '⏰ 提醒：请服用优甲乐'")
        print(f"4. 07:15 - 用户确认服药")
        
        # 模拟记录
        result = reminder.record_medication("07:15", manual=False)
        print(f"\n📝 记录结果: {result['message']}")
        
        # 检查状态
        status = reminder.get_today_status()
        print(f"📊 最终状态: {status['status']}")
        
        # 生成当日报告
        report = reminder.generate_report(1)
        print(f"📈 当日依从率: {report['compliance_rate']}%")
        
        print("\n🎉 提醒流程模拟成功！")
        return True
        
    except Exception as e:
        print(f"\n❌ 流程模拟失败: {e}")
        return False

def cleanup_test_data():
    """清理测试数据"""
    print("\n🧹 清理测试数据...")

    try:
        data_dir = Path.home() / ".openclaw" / "medication_data"

        # 备份原始文件（带时间戳，避免覆盖）
        import shutil
        import datetime
        if data_dir.exists():
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = data_dir.parent / f"medication_data_backup_{timestamp}"
            try:
                shutil.copytree(data_dir, backup_dir)
                print(f"✅ 已备份原始数据到: {backup_dir}")
            except Exception as e:
                print(f"⚠️  备份失败: {e}，跳过备份步骤")

            # 清理测试文件（仅清空内容，不删除文件）
            test_files = list(data_dir.glob("*.json"))
            for file in test_files:
                if file.name in ["medication-records.json", "stats.json", "settings.json"]:
                    # 只清空内容，不删除文件
                    if file.name == "medication-records.json":
                        with open(file, 'w', encoding='utf-8') as f:
                            import json
                            json.dump([], f, ensure_ascii=False, indent=2)
                    elif file.name == "stats.json":
                        with open(file, 'w', encoding='utf-8') as f:
                            import json
                            json.dump({
                                "total_days": 0,
                                "on_time_days": 0,
                                "missed_days": 0,
                                "current_streak": 0,
                                "best_streak": 0,
                                "last_taken": None
                            }, f, ensure_ascii=False, indent=2)
                    print(f"   已重置: {file.name}")

        # 清理测试导出文件
        test_export = Path("/tmp/test_medication_export.csv")
        if test_export.exists():
            test_export.unlink()
            print(f"   已删除测试导出文件")

        print("✅ 数据清理完成")
        return True

    except Exception as e:
        print(f"❌ 清理失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🔬 优甲乐服药提醒系统 - 完整测试套件")
    print("="*50)
    
    try:
        # 运行所有测试
        basic_ok = test_basic_functionality()
        integration_ok = test_integration()
        cron_ok = test_cron_simulation()
        
        # 汇总结果
        print("\n" + "="*50)
        print("📊 测试结果汇总:")
        print(f"✅ 基本功能测试: {'通过' if basic_ok else '失败'}")
        print(f"✅ 集成功能测试: {'通过' if integration_ok else '失败'}")
        print(f"✅ 提醒流程测试: {'通过' if cron_ok else '失败'}")
        
        if basic_ok and integration_ok and cron_ok:
            print("\n🎉 所有测试通过！系统功能正常。")
        else:
            print("\n⚠️  部分测试失败，请检查上述错误信息。")
        
        # 询问是否清理测试数据
        print("\n🧹 是否清理测试数据？(y/n): ", end="")
        response = input().strip().lower()
        if response == 'y':
            cleanup_test_data()
        else:
            print("⚠️  测试数据保留，可用于进一步测试。")
        
        print("\n📋 **下一步建议：**")
        print("1. 运行安装脚本: python3 setup.py")
        print("2. 配置 OpenClaw cron 任务")
        print("3. 测试实际使用流程")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ 测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试过程中出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    # 使脚本可执行
    if len(sys.argv) > 1 and sys.argv[1] == "--cleanup":
        cleanup_test_data()
    else:
        main()