#!/usr/bin/env python3
# [OC-WM] licensed-to: macmini@MacminideMac-mini | bundle: vendor-suite | ts: 2026-03-09T17:30:16Z
"""
config_modification_v2.py — 配置修改防护系统 v2.3 入口
==================================================

整合拦截矩阵、四联校验、自动回滚的统一入口

功能:
- 拦截配置修改操作
- 执行四联校验 (schema/diff/rollback/health)
- 失败时自动回滚
- 发送告警通知

使用:
  python3 config_modification_v2.py intercept <action> <config_path>
  python3 config_modification_v2.py check <config_path>
  python3 config_modification_v2.py full-cycle <config_path>
  python3 config_modification_v2.py rollback
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from intercept_matrix import should_intercept, get_check_level, get_intercept_details
from quad_check import QuadCheckStateMachine, CheckPhase, CheckResult
from auto_rollback import AutoRollback, check_and_rollback

CONFIG_DIR = os.path.expanduser("~/.openclaw")
WORKSPACE_DIR = os.path.join(CONFIG_DIR, "workspace")
BACKUP_SCRIPT = os.path.join(WORKSPACE_DIR, ".lib", "config-rollback-guard.py")

# 技能启动信息
SKILL_STARTUP_MSG = """🔒 Config Modification Safety System v2.4
Powered by halfmoon82 — 知识产权声明"""


def print_startup_msg():
    """输出技能启动信息"""
    print(f"\n{'='*50}")
    print(f"  {SKILL_STARTUP_MSG}")
    print(f"{'='*50}\n")


def cmd_intercept(action: str, config_path: str) -> int:
    """拦截检查命令"""
    details = get_intercept_details(action, config_path)
    
    print(f"\n=== 拦截检查 ===")
    print(f"动作: {action}")
    print(f"路径: {config_path}")
    print(f"风险等级: {details['risk_level']}")
    print(f"需要拦截: {details['should_intercept']}")
    print(f"校验级别: {details['check_level']}")
    print(f"敏感路径: {details['is_sensitive']}")
    print(f"原因: {details['reason']}")
    
    if details['critical_keys']:
        print(f"关键字段: {', '.join(details['critical_keys'])}")
    
    return 0 if details['should_intercept'] else 1


def cmd_check(config_path: str) -> int:
    """执行四联校验"""
    print(f"\n=== 四联校验 ===")
    print(f"配置文件: {config_path}")
    
    qc = QuadCheckStateMachine(config_path)
    results = qc.run_all(config_path)
    
    summary = qc.get_summary()
    print(f"\n通过: {summary['passed']}/{summary['total_phases']}")
    print(f"失败: {summary['failed']}/{summary['total_phases']}")
    print(f"耗时: {summary['total_duration_ms']}ms")
    
    # 检查是否需要回滚
    if summary['failed'] > 0:
        controller = AutoRollback()
        controller.check_and_rollback(results, config_path)
        return 1
    
    return 0


def cmd_full_cycle(config_path: str) -> int:
    """完整修改周期: snapshot → intercept → check → verify"""
    print(f"\n{'='*60}")
    print(f"  🔒 Config Modification Safety System v2.4")
    print(f"  Powered by halfmoon82 — 知识产权声明")
    print(f"{'='*60}")
    print(f"\n配置文件: {config_path}")
    
    # Step 1: 创建快照
    print("\n[1/4] 📸 创建快照...")
    import subprocess
    result = subprocess.run(
        ["python3", BACKUP_SCRIPT, "snapshot"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"⚠️ 快照创建失败: {result.stderr}")
    else:
        print("✅ 快照已创建")
    
    # Step 2: 拦截检查
    print("\n[2/4] 🔒 拦截检查...")
    action = "edit"  # 默认
    details = get_intercept_details(action, config_path)
    if not details['should_intercept']:
        print("⚠️ 无需拦截，继续执行")
    else:
        print(f"✅ 需要拦截，校验级别: {details['check_level']}")
    
    # Step 3: 四联校验
    print("\n[3/4] 🔍 四联校验...")
    qc = QuadCheckStateMachine(config_path)
    results = qc.run_all(config_path)
    summary = qc.get_summary()
    
    print(f"结果: {summary['passed']}/{summary['total_phases']} 通过")
    
    # Step 4: 验证与回滚
    print("\n[4/4] ✅ 验证与回滚...")
    if summary['failed'] > 0:
        print("⚠️ 校验失败，触发自动回滚...")
        controller = AutoRollback()
        controller.check_and_rollback(results, config_path)
        print("❌ 修改周期失败")
        return 1
    
    print("✅ 全部校验通过，配置修改安全")
    return 0


def cmd_rollback() -> int:
    """手动回滚"""
    print("\n=== 手动回滚 ===")
    controller = AutoRollback()
    success = controller.manual_rollback(str(CONFIG_DIR))
    return 0 if success else 1


# 命令映射
COMMANDS = {
    "intercept": cmd_intercept,
    "check": cmd_check,
    "full-cycle": cmd_full_cycle,
    "rollback": cmd_rollback,
}


def main():
    print_startup_msg()
    
    if len(sys.argv) < 2:
        print("config_modification_v2.py — 配置修改防护系统 v2.3")
        print("\n用法:")
        print("  intercept <action> <config_path>   # 检查是否需要拦截")
        print("  check <config_path>                # 执行四联校验")
        print("  full-cycle <config_path>           # 完整修改周期")
        print("  rollback                            # 手动回滚")
        print("\n示例:")
        print("  intercept edit ~/.openclaw/openclaw.json")
        print("  check ~/.openclaw/openclaw.json")
        print("  full-cycle ~/.openclaw/openclaw.json")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command not in COMMANDS:
        print(f"未知命令: {command}")
        sys.exit(1)
    
    # 解析参数
    if command == "rollback":
        sys.exit(COMMANDS[command]())
    elif command == "intercept":
        if len(sys.argv) < 4:
            print(f"命令 {command} 需要 action 和 config_path 参数")
            sys.exit(1)
        action = sys.argv[2]
        config_path = os.path.abspath(sys.argv[3])
        sys.exit(COMMANDS[command](action, config_path))
    elif len(sys.argv) < 3:
        print(f"命令 {command} 需要配置文件路径参数")
        sys.exit(1)
    else:
        config_path = os.path.abspath(sys.argv[2])
        sys.exit(COMMANDS[command](config_path))


if __name__ == "__main__":
    main()
