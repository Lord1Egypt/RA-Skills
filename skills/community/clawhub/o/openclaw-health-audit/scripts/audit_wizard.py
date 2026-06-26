#!/usr/bin/env python3
# [OC-WM] licensed-to: macmini@MacminideMac-mini | bundle: vendor-suite | ts: 2026-03-09T17:30:16Z
"""
audit_wizard.py — openclaw-health-audit 安装向导
版本: 1.0.0 (2026-03-05)

自动测量当前文件大小，生成个性化 config.json，可选注册 48h Cron Job。

用法:
  python3 audit_wizard.py
"""

import json
import os
import sys
import uuid
from pathlib import Path
from datetime import datetime

SKILL_DIR = Path(__file__).parent.parent
CONFIG_FILE = SKILL_DIR / 'config' / 'config.json'
BASE = Path.home() / '.openclaw'
WORKSPACE = BASE / 'workspace'
AGENTS_DIR = BASE / 'agents'
CRON_JOBS = BASE / 'cron' / 'jobs.json'

KNOWN_PROMPT_FILES = ['SOUL.md', 'TOOLS.md', 'AGENTS.md']
KNOWN_SUBAGENTS = ['pm', 'architect', 'backend', 'frontend', 'qa', 'devops', 'code-artisan']

EXPENSIVE_MODELS = ['claude-opus', 'claude-opus-4', 'opus-4.6', 'opus-4-5']
DEFAULT_CHEAP_MODEL = 'custom-llmapi-lovbrowser-com/google/gemini-2.5-flash'

def hr():
    print('─' * 50)

def ask(prompt: str, default: str = '') -> str:
    suffix = f' [{default}]' if default else ''
    try:
        answer = input(f'{prompt}{suffix}: ').strip()
        return answer if answer else default
    except (EOFError, KeyboardInterrupt):
        print()
        return default

def ask_yn(prompt: str, default: bool = True) -> bool:
    suffix = ' [Y/n]' if default else ' [y/N]'
    try:
        answer = input(f'{prompt}{suffix}: ').strip().lower()
        if not answer:
            return default
        return answer in ('y', 'yes')
    except (EOFError, KeyboardInterrupt):
        print()
        return default

def measure_prompt_files() -> dict:
    """测量 workspace 下的主要 prompt 文件大小，计算 warn/alert 阈值"""
    results = {}
    print('\n📊 扫描 workspace prompt 文件...')
    for filename in KNOWN_PROMPT_FILES:
        path = WORKSPACE / filename
        if path.exists():
            size = path.stat().st_size
            warn = int(size * 1.1)
            alert = int(size * 1.4)
            results[filename] = {'warn': warn, 'alert': alert}
            print(f'   {filename}: {size}B → warn={warn}B ({warn//1024}KB), alert={alert}B ({alert//1024}KB)')
        else:
            # 文件不存在时使用合理默认值
            defaults = {
                'SOUL.md':   {'warn': 6144,  'alert': 8192},
                'TOOLS.md':  {'warn': 6144,  'alert': 7500},
                'AGENTS.md': {'warn': 12288, 'alert': 14336},
            }
            results[filename] = defaults.get(filename, {'warn': 6144, 'alert': 8192})
            print(f'   {filename}: 文件不存在，使用默认阈值')
    return results

def detect_subagents() -> list:
    """检测实际安装的子代理"""
    found = []
    if not AGENTS_DIR.exists():
        return KNOWN_SUBAGENTS  # fallback
    for agent in KNOWN_SUBAGENTS:
        if (AGENTS_DIR / agent).exists():
            found.append(agent)
    # 还检测 AGENTS_DIR 下未在 KNOWN_SUBAGENTS 中的目录
    for d in AGENTS_DIR.iterdir():
        if d.is_dir() and d.name not in KNOWN_SUBAGENTS and d.name not in ('main',):
            found.append(d.name)
    return found

def measure_subagent_souls(subagents: list) -> dict:
    """测量子代理 SOUL.md 大小，计算阈值"""
    sizes = []
    print('\n📊 扫描子代理 SOUL.md...')
    for agent in subagents:
        soul_path = AGENTS_DIR / agent / 'workspace' / 'SOUL.md'
        if soul_path.exists():
            size = soul_path.stat().st_size
            sizes.append(size)
            print(f'   {agent}/SOUL.md: {size}B')
    if sizes:
        max_size = max(sizes)
        warn = int(max_size * 1.1)
        alert = int(max_size * 1.4)
    else:
        warn, alert = 3072, 4096
    print(f'   → 子代理阈值: warn={warn}B, alert={alert}B')
    return {'warn': warn, 'alert': alert}

def detect_semantic_router() -> bool:
    """检测是否安装了 semantic-router skill"""
    sr_path = WORKSPACE / 'skills' / 'semantic-router'
    injector_path = WORKSPACE / '.openclaw' / 'extensions' / 'message-injector' / 'index.ts'
    return sr_path.exists() or injector_path.exists()

def detect_message_injector_path() -> str:
    default = str(WORKSPACE / '.openclaw' / 'extensions' / 'message-injector' / 'index.ts')
    return default

def register_cron_job(model: str) -> str:
    """注册 48h 健康检查 Cron Job，返回 Job ID"""
    if not CRON_JOBS.exists():
        print(f'   ⚠️  Cron Job 文件不存在：{CRON_JOBS}，跳过注册')
        return ''

    with open(CRON_JOBS) as f:
        jobs_data = json.load(f)

    # 判断格式
    is_list = isinstance(jobs_data, list)
    jobs = jobs_data if is_list else jobs_data.get('jobs', list(jobs_data.values()))

    # 检查是否已有 health-monitor cron
    for job in jobs:
        if 'health' in job.get('name', '').lower() and 'monitor' in job.get('name', '').lower():
            print(f'   ℹ️  已存在健康监控 Cron Job: {job.get("id", "")} ({job.get("name", "")})')
            return job.get('id', '')

    job_id = str(uuid.uuid4())
    skill_dir = str(SKILL_DIR)
    new_job = {
        "id": job_id,
        "name": "48h-health-monitor",
        "schedule": "0 2 */2 * *",
        "sessionKey": None,
        "status": "active",
        "payload": {
            "kind": "agentTurn",
            "model": model,
            "timeoutSeconds": 120,
            "prompt": (
                f"执行系统健康检查：python3 {skill_dir}/scripts/health_monitor.py --report\n\n"
                "将输出结果通过 Telegram 发送给用户。若有问题，等待用户回复后按指令执行修复。\n"
                "修复命令格式：python3 {skill_dir}/scripts/health_monitor.py --fix <编号或 all>"
            ).replace('{skill_dir}', skill_dir)
        }
    }

    if is_list:
        jobs_data.append(new_job)
    else:
        jobs_data[job_id] = new_job

    with open(CRON_JOBS, 'w') as f:
        json.dump(jobs_data, f, indent=2, ensure_ascii=False)

    print(f'   ✅ 已注册 Cron Job: {job_id} (每 48h 凌晨 2:00)')
    return job_id

def main():
    print('\n╔══════════════════════════════════════════════════════╗')
    print('║      openclaw-health-audit 安装向导 v1.0.0          ║')
    print('╚══════════════════════════════════════════════════════╝')
    print(f'\n工作目录: {WORKSPACE}')
    print(f'配置输出: {CONFIG_FILE}')
    hr()

    # Step 1: 测量 prompt 文件
    prompt_files = measure_prompt_files()

    # Step 2: 检测子代理
    print('\n📊 检测已安装的子代理...')
    subagents = detect_subagents()
    print(f'   发现 {len(subagents)} 个子代理: {", ".join(subagents)}')
    subagent_soul = measure_subagent_souls(subagents)

    # Step 3: 检测 semantic-router
    hr()
    has_sr = detect_semantic_router()
    enable_cache_check = False
    injector_path = detect_message_injector_path()

    if has_sr:
        print('\n🔍 检测到 semantic-router / message-injector')
        enable_cache_check = ask_yn(
            '   是否启用 Category E（缓存配置完整性检测，需要 M1/M3 补丁）',
            default=False
        )
    else:
        print('\n🔍 未检测到 semantic-router，Category E 禁用')

    # Step 4: Token 阈值确认
    hr()
    print('\n⚙️  Token 消耗阈值（日均）:')
    warn_m = int(ask('   warn 阈值（百万 tokens）', '30'))
    alert_m = int(ask('   alert 阈值（百万 tokens）', '60'))

    # Step 5: 其他设置
    stale_days = int(ask('\n   Session 过期天数', '7'))

    # Step 6: 生成 config.json
    hr()
    config = {
        "version": "1.0",
        "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "generated_by": "audit_wizard.py",
        "prompt_files": prompt_files,
        "subagent_soul": subagent_soul,
        "subagents": {"list": subagents},
        "token_thresholds": {"warn": warn_m * 1_000_000, "alert": alert_m * 1_000_000},
        "session_stale_days": stale_days,
        "expensive_models": {"list": EXPENSIVE_MODELS},
        "checks": {
            "prompt_drift": True,
            "cron_jobs": True,
            "orphan_sessions": True,
            "token_trend": True,
            "cache_config": enable_cache_check
        },
        "cache_config": {
            "message_injector_path": injector_path,
            "expected_ttl_ms": 1_800_000,
            "expected_ttl_label": "30 minutes",
            "bad_ttl_ms": 300_000,
            "check_extract_decl_key": True
        }
    }

    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print(f'\n✅ 配置已写入: {CONFIG_FILE}')

    # Step 7: 可选注册 Cron Job
    hr()
    if ask_yn('\n是否注册 48h 定期健康检查 Cron Job', default=True):
        model = ask('   使用模型', DEFAULT_CHEAP_MODEL)
        register_cron_job(model)
    else:
        skill_dir = str(SKILL_DIR)
        print(f'\n   手动注册命令参考（加入 {CRON_JOBS}）:')
        print(json.dumps({
            "id": "<uuid>",
            "name": "48h-health-monitor",
            "schedule": "0 2 */2 * *",
            "sessionKey": None,
            "payload": {
                "kind": "agentTurn",
                "model": DEFAULT_CHEAP_MODEL,
                "timeoutSeconds": 120,
                "prompt": f"python3 {skill_dir}/scripts/health_monitor.py --report"
            }
        }, indent=2, ensure_ascii=False))

    # Step 8: 首次 dry-run 验证
    hr()
    if ask_yn('\n是否运行首次干跑验证（--dry-run）', default=True):
        print()
        monitor_path = SKILL_DIR / 'scripts' / 'health_monitor.py'
        import subprocess
        result = subprocess.run(
            [sys.executable, str(monitor_path), '--dry-run'],
            capture_output=False
        )
        hr()
        if result.returncode <= 1:
            print('\n✅ 向导完成！健康监控已就绪。')
        else:
            print('\n⚠️  检测到告警，请查看上方报告并按需修复。')
    else:
        hr()
        print('\n✅ 向导完成！')
        monitor_path = SKILL_DIR / 'scripts' / 'health_monitor.py'
        print(f'手动验证命令：python3 {monitor_path} --dry-run')

if __name__ == '__main__':
    main()
