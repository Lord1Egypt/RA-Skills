#!/usr/bin/env python3
"""
Token Optimizer - Scheduled Task Handler
定时任务处理器 - 自动执行 Token 优化

用法：
  python3 scheduled-optimizer.py [analyze|compress|suggest|auto]

定时任务配置：
  - 每天早上 8 点：分析 token 使用
  - 每周日凌晨 3 点：压缩旧记忆
  - 每周一早上 8 点：生成优化建议
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR.parent / "config" / "token-optimizer-schedule.json"
OPTIMIZER_SCRIPT = SCRIPT_DIR / "token-optimizer.py"
LOG_FILE = SCRIPT_DIR.parent / "logs" / "optimizer-schedule.log"

class Colors:
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[0;36m'
    RED = '\033[0;31m'
    NC = '\033[0m'
    BOLD = '\033[1m'

def log_info(msg): print(f"{Colors.BLUE}[INFO]{Colors.NC} {msg}")
def log_success(msg): print(f"{Colors.GREEN}[SUCCESS]{Colors.NC} {msg}")
def log_warning(msg): print(f"{Colors.YELLOW}[WARNING]{Colors.NC} {msg}")
def log_error(msg): print(f"{Colors.RED}[ERROR]{Colors.NC} {msg}")

def load_config() -> dict:
    """加载配置文件"""
    if not CONFIG_FILE.exists():
        log_error(f"配置文件不存在：{CONFIG_FILE}")
        return {
            "enabled": False,
            "schedule": {},
            "settings": {
                "keep_days": 30,
                "auto_compress": True,
                "notify_on_savings": True,
                "min_savings_tokens": 500
            }
        }
    
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_config(config: dict):
    """保存配置文件"""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def run_optimizer(mode: str) -> dict:
    """运行优化器"""
    args = ['python3', str(OPTIMIZER_SCRIPT)]
    
    if mode == 'analyze':
        args.append('--analyze')
    elif mode == 'compress':
        config = load_config()
        days = config['settings'].get('keep_days', 30)
        args.extend(['--compress', '--days', str(days)])
    elif mode == 'suggest':
        args.append('--suggest')
    elif mode == 'auto':
        args.append('--full')
    else:
        log_error(f"未知模式：{mode}")
        return {'success': False}
    
    try:
        result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=300)
        return {
            'success': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr
        }
    except subprocess.TimeoutExpired:
        log_error("优化器执行超时")
        return {'success': False, 'error': 'timeout'}
    except Exception as e:
        log_error(f"执行失败：{e}")
        return {'success': False, 'error': str(e)}

def log_execution(mode: str, result: dict):
    """记录执行日志"""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().isoformat()
    log_entry = {
        'timestamp': timestamp,
        'mode': mode,
        'success': result.get('success', False),
        'error': result.get('error', result.get('stderr', ''))
    }
    
    # 追加到日志文件
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"\n--- {timestamp} ---\n")
        f.write(f"Mode: {mode}\n")
        f.write(f"Success: {log_entry['success']}\n")
        if result.get('stdout'):
            f.write(f"Output:\n{result['stdout'][:1000]}\n")
        if result.get('error'):
            f.write(f"Error: {result['error']}\n")

def update_stats(mode: str, result: dict):
    """更新统计信息"""
    config = load_config()
    
    timestamp = datetime.now().isoformat()
    
    if mode == 'analyze':
        config['stats']['last_analyze'] = timestamp
    elif mode == 'compress':
        config['stats']['last_compress'] = timestamp
        # 估算节省的 token（简化处理）
        if result.get('success'):
            # 从输出中解析节省的 token 数
            output = result.get('stdout', '')
            if '节省字符:' in output:
                # 简单估算
                config['stats']['total_saved_tokens'] = config['stats'].get('total_saved_tokens', 0) + 1000
    
    save_config(config)

def show_status():
    """显示定时任务状态"""
    config = load_config()
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}📅 Token Optimizer 定时任务状态{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.NC}\n")
    
    enabled = config.get('enabled', False)
    print(f"定时任务：{'✅ 已启用' if enabled else '❌ 已禁用'}\n")
    
    schedule = config.get('schedule', {})
    print(f"{'任务':<15} {'Cron 表达式':<20} {'说明':<25}")
    print(f"{'-'*60}")
    print(f"{'分析':<15} {schedule.get('analyze', 'N/A'):<20} 每天早上 8 点")
    print(f"{'压缩':<15} {schedule.get('compress', 'N/A'):<20} 每周日凌晨 3 点")
    print(f"{'建议':<15} {schedule.get('suggest', 'N/A'):<20} 每周一早上 8 点")
    print()
    
    settings = config.get('settings', {})
    print(f"设置:")
    print(f"  - 保留天数：{settings.get('keep_days', 30)} 天")
    print(f"  - 自动压缩：{'是' if settings.get('auto_compress', True) else '否'}")
    print(f"  - 节省通知：{'是' if settings.get('notify_on_savings', True) else '否'}")
    print(f"  - 最小节省：{settings.get('min_savings_tokens', 500)} tokens")
    print()
    
    stats = config.get('stats', {})
    print(f"统计:")
    print(f"  - 最后分析：{stats.get('last_analyze', '从未')}")
    print(f"  - 最后压缩：{stats.get('last_compress', '从未')}")
    print(f"  - 累计节省：{stats.get('total_saved_tokens', 0):,} tokens")
    print()

def enable_scheduling():
    """启用定时任务"""
    config = load_config()
    config['enabled'] = True
    save_config(config)
    log_success("定时任务已启用")
    
    print(f"\n{Colors.YELLOW}⚠️  注意：{Colors.NC}")
    print("需要在 OpenClaw 中配置定时任务，或使用系统 crontab：")
    print(f"\n添加到 crontab (crontab -e):")
    print(f"# Token Optimizer 定时任务")
    print(f"0 8 * * * cd ~/.openclaw/workspace && python3 skills/memory-enhancer/scripts/scheduled-optimizer.py analyze")
    print(f"0 3 * * 0 cd ~/.openclaw/workspace && python3 skills/memory-enhancer/scripts/scheduled-optimizer.py compress")
    print(f"0 8 * * 1 cd ~/.openclaw/workspace && python3 skills/memory-enhancer/scripts/scheduled-optimizer.py suggest")
    print()

def disable_scheduling():
    """禁用定时任务"""
    config = load_config()
    config['enabled'] = False
    save_config(config)
    log_success("定时任务已禁用")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Token Optimizer 定时任务处理器')
    parser.add_argument('mode', nargs='?', choices=['analyze', 'compress', 'suggest', 'auto', 'status', 'enable', 'disable'], 
                       default='auto', help='执行模式')
    
    args = parser.parse_args()
    
    if args.mode == 'status':
        show_status()
        return
    elif args.mode == 'enable':
        enable_scheduling()
        return
    elif args.mode == 'disable':
        disable_scheduling()
        return
    
    # 检查是否启用
    config = load_config()
    if not config.get('enabled', False):
        log_warning("定时任务未启用，运行：python3 scheduled-optimizer.py enable")
        print(f"\n{Colors.YELLOW}💡 提示：{Colors.NC}")
        print("首次使用请先启用定时任务：")
        print(f"  python3 scheduled-optimizer.py enable")
        print(f"\n或直接执行优化：")
        print(f"  python3 scheduled-optimizer.py {args.mode}")
        print()
        return
    
    log_info(f"开始执行定时任务：{args.mode}")
    result = run_optimizer(args.mode)
    
    if result.get('success'):
        log_success(f"任务执行成功：{args.mode}")
        log_execution(args.mode, result)
        update_stats(args.mode, result)
        
        # 显示输出
        if result.get('stdout'):
            print(result['stdout'])
    else:
        log_error(f"任务执行失败：{result.get('error', '未知错误')}")
        log_execution(args.mode, result)
        sys.exit(1)

if __name__ == "__main__":
    main()
