#!/usr/bin/env python3
# [OC-WM] licensed-to: macmini@MacminideMac-mini | bundle: vendor-suite | ts: 2026-03-09T17:30:16Z
"""
health_monitor.py — OpenClaw 48h 健康监控脚本
版本: 1.4.0 (2026-03-06)

用法:
  python3 health_monitor.py --report       # 生成报告，输出到 stdout（供 agent 发送 Telegram）
  python3 health_monitor.py --dry-run      # 同 --report，标注 [DRY RUN]
  python3 health_monitor.py --fix "1,3"   # 执行第 1、3 项问题的修复
  python3 health_monitor.py --list-fixes   # 列出所有可执行的修复命令（不执行）

监控范围（Layer 1-3）：
  A. System Prompt 体积漂移（Layer 1）
  B. Cron Job 合规性（Layer 2）
  C. 孤儿 Session 检测（Layer 2）
  D. Token 消耗趋势（Layer 3，参考）
  E. 缓存配置完整性（Layer 2）—— PATCH_CACHE_TTL=30min + extractSkillKey 机制（M1/M3）
  F. Session 状态完整性（Layer 2）—— fallbackChain 缺失/过短（F1）+ 无效 provider 前缀（F2）
  G. 代码完整性（Layer 2）—— FIX-0/1/2/3/4 合规检查（G1-G8）（2026-03-06）
     G7: extractStableRoutingParts 函数存在（Option C 路由标签，2026-03-06 续）
     G8: isChannelSession 排除 :subagent:（subagent 双重输出修复，2026-03-06 续）
"""

import json
import os
import re
import sys
import time
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ─── 路径常量 ────────────────────────────────────────────────────────────────

BASE = Path.home() / '.openclaw'
WORKSPACE = BASE / 'workspace'
LIB = WORKSPACE / '.lib'
MEMORY = WORKSPACE / 'memory'
AGENTS_DIR = BASE / 'agents'
CRON_JOBS = BASE / 'cron' / 'jobs.json'
SESSION_STATE = LIB / 'session_model_state.json'
REPORT_FILE = LIB / 'health_report_latest.md'
OPENCLAW_JSON = BASE / 'openclaw.json'

# ─── 阈值配置 ────────────────────────────────────────────────────────────────

# 修复后基线 (2026-03-05): SOUL.md=5.7KB, TOOLS.md=5.4KB, AGENTS.md=11KB, subagent=2.3-3.1KB
# warn = 修复后基线 × 1.1（允许10%增长）; alert = 修复后基线 × 1.4
PROMPT_THRESHOLDS = {
    'SOUL.md':   {'warn': 6 * 1024,      'alert': 8 * 1024},
    'TOOLS.md':  {'warn': 6 * 1024,      'alert': 7500},
    'AGENTS.md': {'warn': 12 * 1024,     'alert': 14 * 1024},
}

SUBAGENT_SOUL_THRESHOLDS = {'warn': 3 * 1024, 'alert': 4 * 1024}
SUBAGENT_NAMES = ['pm', 'architect', 'backend', 'frontend', 'qa', 'devops', 'code-artisan']

TOKEN_THRESHOLDS = {'warn': 30_000_000, 'alert': 60_000_000}
SESSION_STALE_DAYS = 7
EXPENSIVE_MODELS = {'claude-opus', 'claude-opus-4', 'opus-4.6', 'opus-4-5'}

# Category E: 缓存配置完整性（2026-03-05 M1/M3 引入）
MESSAGE_INJECTOR = WORKSPACE / '.openclaw' / 'extensions' / 'message-injector' / 'index.ts'
# M3: PATCH_CACHE_TTL 应为 30min (1800000ms)，旧值 5min (300000ms) 会告警
PATCH_CACHE_TTL_EXPECTED = 30 * 60 * 1000   # 1800000
PATCH_CACHE_TTL_BAD      = 5  * 60 * 1000   # 300000（旧默认值）
# M1: extractSkillKey 函数应存在（FIX-0 后替代 extractDeclKey）
EXTRACT_SKILL_KEY_SIGNATURE = 'function extractSkillKey('
# Category G: 代码完整性（2026-03-06 FIX-0/3/4 引入）
POOLS_JSON = LIB / 'pools.json'

# ─── 数据结构 ────────────────────────────────────────────────────────────────

@dataclass
class Issue:
    idx: int            # 显示编号（从 1 开始）
    category: str       # A / B / C / D
    severity: str       # warn / alert
    title: str
    detail: str
    fix_cmd: Optional[str] = None      # 可直接执行的命令
    fix_description: Optional[str] = None


# ─── 监控检查 ────────────────────────────────────────────────────────────────

def check_prompt_drift() -> list[Issue]:
    """A: 检查主 workspace 和子代理 SOUL.md 体积漂移"""
    issues = []

    # 主 workspace 文件
    for filename, thresholds in PROMPT_THRESHOLDS.items():
        path = WORKSPACE / filename
        if not path.exists():
            continue
        size = path.stat().st_size
        warn, alert = thresholds['warn'], thresholds['alert']
        if size > alert:
            sev = 'alert'
            emoji = '🔴'
        elif size > warn:
            sev = 'warn'
            emoji = '🟡'
        else:
            continue
        issues.append(Issue(
            idx=0, category='A', severity=sev,
            title=f'{filename} 体积漂移: {size // 1024}KB ({size}B)',
            detail=f'阈值: warn={warn // 1024}KB, alert={alert // 1024}KB\n'
                   f'原因: 可能有新内容被写入常驻 prompt\n'
                   f'建议: 将超出部分移至 memory/LESSONS/ 或对应 Skill 文件',
            fix_description=f'手动审查 {filename}，将非核心内容移至 memory/LESSONS/lessons.md',
        ))

    # 子代理 SOUL.md
    oversized = []
    for agent in SUBAGENT_NAMES:
        soul_path = AGENTS_DIR / agent / 'workspace' / 'SOUL.md'
        if not soul_path.exists():
            continue
        size = soul_path.stat().st_size
        warn = SUBAGENT_SOUL_THRESHOLDS['warn']
        alert = SUBAGENT_SOUL_THRESHOLDS['alert']
        if size > alert:
            oversized.append((agent, size, 'alert'))
        elif size > warn:
            oversized.append((agent, size, 'warn'))

    if oversized:
        names = ', '.join(f'{a}({s}B)' for a, s, _ in oversized)
        max_sev = 'alert' if any(s == 'alert' for _, _, s in oversized) else 'warn'
        issues.append(Issue(
            idx=0, category='A', severity=max_sev,
            title=f'子代理 SOUL.md 超限: {len(oversized)} 个',
            detail=f'超限代理: {names}\n'
                   f'阈值: warn={SUBAGENT_SOUL_THRESHOLDS["warn"]}B, alert={SUBAGENT_SOUL_THRESHOLDS["alert"]}B\n'
                   f'建议: 删除 SOUL.md 中的模型配置表、历史教训等非核心内容',
            fix_description='删除各子代理 SOUL.md 中的 Model Fallback Order 表和历史教训',
        ))

    return issues


def check_cron_jobs() -> list[Issue]:
    """B: 检查 Cron Job 合规性"""
    issues = []
    if not CRON_JOBS.exists():
        return issues

    with open(CRON_JOBS) as f:
        jobs_data = json.load(f)

    jobs = jobs_data if isinstance(jobs_data, list) else jobs_data.get('jobs', list(jobs_data.values()))

    violations = []
    for job in jobs:
        if job.get('status') == 'disabled':
            continue
        payload = job.get('payload', {})
        if payload.get('kind') != 'agentTurn':
            continue

        jid = job.get('id', 'unknown')
        name = job.get('name', jid)[:50]
        problems = []

        if job.get('sessionKey') is not None:
            problems.append('sessionKey 非 null（污染主会话）')

        if 'timeoutSeconds' not in payload:
            problems.append('缺少 timeoutSeconds（可能挂起）')

        model = payload.get('model', '')
        if any(em in model.lower() for em in EXPENSIVE_MODELS):
            problems.append(f'使用高成本模型: {model}')

        if problems:
            violations.append((jid, name, problems))

    if violations:
        detail_lines = []
        fix_lines = []
        for jid, name, problems in violations:
            detail_lines.append(f'- [{jid[:8]}...] {name}: {", ".join(problems)}')
            fix_lines.append(
                f'python3 -c "import json; f=open(\'{CRON_JOBS}\'); '
                f'jobs=json.load(f); f.close(); '
                f'# edit job {jid[:8]}"'
            )

        issues.append(Issue(
            idx=0, category='B', severity='alert' if len(violations) > 2 else 'warn',
            title=f'Cron Job 违规: {len(violations)} 个',
            detail='\n'.join(detail_lines) + '\n建议: 设置 sessionKey=null, timeoutSeconds≤120, 使用 gemini-2.5-flash',
            fix_cmd=None,
            fix_description=f'修复 {len(violations)} 个违规 Job: sessionKey=null, timeoutSeconds=120, model=gemini-2.5-flash',
        ))

    return issues


def check_orphan_sessions() -> list[Issue]:
    """C: 检查孤儿 Session（超过 7 天无活动的 cron session）"""
    issues = []
    if not SESSION_STATE.exists():
        return issues

    with open(SESSION_STATE) as f:
        sessions = json.load(f)

    now_ms = int(time.time() * 1000)
    stale_ms = SESSION_STALE_DAYS * 24 * 3600 * 1000

    stale = []
    for key, state in sessions.items():
        ts = state.get('lastPatchedAt', state.get('updatedAt', 0))
        if ts and (now_ms - ts) > stale_ms:
            age_days = (now_ms - ts) / (24 * 3600 * 1000)
            stale.append((key, age_days))

    if stale:
        names = '\n'.join(f'- {k[:60]} ({d:.1f}天前)' for k, d in stale)
        issues.append(Issue(
            idx=0, category='C', severity='warn',
            title=f'过期 Session: {len(stale)} 个（>{SESSION_STALE_DAYS}天无活动）',
            detail=names + f'\n建议: 从 session_model_state.json 清除这些 key',
            fix_description=f'清除 {len(stale)} 个过期 session key',
        ))

    return issues


def check_token_trend() -> list[Issue]:
    """D: 检查 Token 消耗趋势（读取最近2天的 memory 文件或调用 usage API）"""
    issues = []

    # 尝试调用 openclaw gateway usage-cost --json
    try:
        result = subprocess.run(
            ['openclaw', 'gateway', 'usage-cost', '--json', '--days', '2'],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            daily = data.get('daily', [])
            for day_data in daily:
                date = day_data.get('date', '')
                total = day_data.get('totalTokens', 0)
                cost = day_data.get('totalCost', 0)
                if total > TOKEN_THRESHOLDS['alert']:
                    sev = 'alert'
                    icon = '🔴'
                elif total > TOKEN_THRESHOLDS['warn']:
                    sev = 'warn'
                    icon = '🟡'
                else:
                    continue
                issues.append(Issue(
                    idx=0, category='D', severity=sev,
                    title=f'{icon} Token 消耗异常 {date}: {total / 1_000_000:.1f}M tokens / ${cost:.2f}',
                    detail=f'阈值: warn={TOKEN_THRESHOLDS["warn"] // 1_000_000}M, alert={TOKEN_THRESHOLDS["alert"] // 1_000_000}M\n'
                           f'建议: 检查是否有失控的 cron job 或长会话未压缩',
                    fix_description='检查 cron job 模型配置，使用 /compact 压缩长会话',
                ))
    except Exception:
        pass  # 无法获取则跳过，不影响其他检查

    return issues


def check_cache_config() -> list[Issue]:
    """E: 检查 message-injector/index.ts 缓存配置完整性（M1/M3）"""
    issues = []
    if not MESSAGE_INJECTOR.exists():
        return issues

    content = MESSAGE_INJECTOR.read_text(encoding='utf-8')

    # E1: PATCH_CACHE_TTL 检查
    # 检测是否存在旧值 5 * 60 * 1000 = 300000
    bad_ttl_patterns = [
        '5 * 60 * 1000',
        '300000',
    ]
    found_bad = False
    found_line = ''
    for line in content.splitlines():
        if 'PATCH_CACHE_TTL' in line:
            for pat in bad_ttl_patterns:
                if pat in line:
                    found_bad = True
                    found_line = line.strip()
                    break
            break  # 只看第一个 PATCH_CACHE_TTL 行

    if found_bad:
        issues.append(Issue(
            idx=0, category='E', severity='alert',
            title='PATCH_CACHE_TTL 已回退至旧值（5 分钟）',
            detail=f'发现行: {found_line}\n'
                   f'期望: 30 * 60 * 1000 (1800000ms = 30 分钟)\n'
                   f'影响: B 分支每 5 分钟触发一次不必要的 sessions.patch，LLM prompt cache 失效\n'
                   f'文件: {MESSAGE_INJECTOR}',
            fix_description=f'手动编辑 message-injector/index.ts：将 PATCH_CACHE_TTL 改为 30 * 60 * 1000',
        ))

    # E2: extractSkillKey 函数存在性检查（M1，FIX-0 后从 extractDeclKey 更名）
    if EXTRACT_SKILL_KEY_SIGNATURE not in content:
        issues.append(Issue(
            idx=0, category='E', severity='warn',
            title='M1 prependContext 稳定性机制缺失（extractSkillKey 未找到）',
            detail=f'未找到函数签名: {EXTRACT_SKILL_KEY_SIGNATURE}\n'
                   f'影响: 技能激活时 prependContext 每次不同，技能对话 cache 无法命中\n'
                   f'文件: {MESSAGE_INJECTOR}',
            fix_description='重新应用 M1/FIX-0 补丁：在 message-injector/index.ts 添加 extractSkillKey() 函数',
        ))

    return issues


def check_code_integrity() -> list[Issue]:
    """G: 检查 message-injector/index.ts 代码完整性（FIX-0/3/4 合规，2026-03-06 引入）"""
    issues = []
    if not MESSAGE_INJECTOR.exists():
        return issues

    content = MESSAGE_INJECTOR.read_text(encoding='utf-8')

    # G1: declarationPrepend 不应出现在 prependContext 数组中（FIX-0）
    bad_decl_pattern = re.search(r'const prependContext\s*=\s*\[([^\]]*declarationPrepend[^\]]*)\]', content)
    if bad_decl_pattern:
        issues.append(Issue(
            idx=0, category='G', severity='alert',
            title='G1 - declarationPrepend 仍混入 prependContext（FIX-0 未生效）',
            detail=f'发现行: {bad_decl_pattern.group(0)[:100]}\n'
                   f'影响: 每条消息前缀含易变声明字符串，对话历史 cache 100% miss\n'
                   f'修复: 从 prependContext 数组中移除 declarationPrepend\n'
                   f'文件: {MESSAGE_INJECTOR}',
            fix_description='手动编辑 index.ts: 从 prependContext 数组移除 declarationPrepend',
        ))

    # G2: extractSkillKey 函数应存在（FIX-0）
    if 'function extractSkillKey(' not in content:
        issues.append(Issue(
            idx=0, category='G', severity='alert',
            title='G2 - extractSkillKey 函数缺失（FIX-0 未生效）',
            detail=f'文件: {MESSAGE_INJECTOR}\n'
                   f'影响: M1 skill-key 缓存不可用，技能激活时每轮 prependContext 不稳定',
            fix_description='手动编辑 index.ts: 添加 extractSkillKey() 函数',
        ))

    # G3: POOL_PRIMARY.Highspeed 与 pools.json Highspeed primary 一致（FIX-3）
    try:
        if POOLS_JSON.exists():
            pools_data = json.loads(POOLS_JSON.read_text(encoding='utf-8'))
            pools_hs_primary = pools_data.get('Highspeed', {}).get('primary', '')
            # Extract POOL_PRIMARY Highspeed from index.ts
            m = re.search(r'Highspeed\s*:\s*"([^"]+)"', content)
            ts_hs_primary = m.group(1) if m else ''
            if pools_hs_primary and ts_hs_primary and pools_hs_primary != ts_hs_primary:
                issues.append(Issue(
                    idx=0, category='G', severity='warn',
                    title=f'G3 - POOL_PRIMARY.Highspeed 与 pools.json 不一致',
                    detail=f'index.ts: {ts_hs_primary}\n'
                           f'pools.json: {pools_hs_primary}\n'
                           f'影响: 解锁时 index.ts 路由错误 primary 模型',
                    fix_description='手动对齐 index.ts POOL_PRIMARY.Highspeed 与 pools.json Highspeed.primary',
                ))
    except Exception:
        pass

    # G4: main agent fallback 链不含 claude-haiku-4.5（FIX-1）
    try:
        if OPENCLAW_JSON.exists():
            config = json.loads(OPENCLAW_JSON.read_text(encoding='utf-8'))
            main_agent = next((a for a in config.get('agents', {}).get('list', []) if a.get('id') == 'main'), None)
            if main_agent:
                fallbacks = main_agent.get('model', {}).get('fallbacks', [])
                haiku_entries = [f for f in fallbacks if 'claude-haiku-4.5' in f]
                if haiku_entries:
                    issues.append(Issue(
                        idx=0, category='G', severity='alert',
                        title=f'G4 - main agent fallback 链含 claude-haiku-4.5（在 lovbrowser 不可用）',
                        detail=f'条目: {haiku_entries}\n'
                               f'影响: sonnet 失败后每次无效尝试，产生 1604+ 次 No available channel 错误',
                        fix_description='手动删除 openclaw.json main.model.fallbacks 中的 claude-haiku-4.5 条目',
                    ))
    except Exception:
        pass

    # G5: pools.json 高速池/人文池 primary 不含 gemini-3-*（FIX-2）
    try:
        if POOLS_JSON.exists():
            pools_data = json.loads(POOLS_JSON.read_text(encoding='utf-8'))
            dead_pools = []
            for pool_name in ['Highspeed', 'Humanities']:
                prim = pools_data.get(pool_name, {}).get('primary', '')
                if re.search(r'gemini-3-', prim):
                    dead_pools.append(f'{pool_name}: {prim}')
            if dead_pools:
                issues.append(Issue(
                    idx=0, category='G', severity='alert',
                    title=f'G5 - pools.json 含不可用 gemini-3-* primary: {len(dead_pools)} 处',
                    detail='\n'.join(dead_pools) + '\n影响: 每次请求该池都触发 fallback，浪费 ~1.5M tokens/天',
                    fix_description='手动将 pools.json 高速池/人文池 primary 改为 gemini-2.5-flash/gemini-2.5-pro',
                ))
    except Exception:
        pass

    # G6: lockModel 时 hook return 不含 modelOverride（FIX-4）
    # 检测 return 块中 lockModel ? { modelOverride ... } 模式
    lock_override_pattern = re.search(r'lockModel\s*\?\s*\{\s*modelOverride', content)
    if lock_override_pattern:
        issues.append(Issue(
            idx=0, category='G', severity='alert',
            title='G6 - lockModel 时仍返回 modelOverride（FIX-4 未生效）',
            detail=f'发现模式: {lock_override_pattern.group(0)}\n'
                   f'影响: lockModel 时 modelOverride 毒化全部 fallback，导致 All models failed\n'
                   f'文件: {MESSAGE_INJECTOR}',
            fix_description='手动编辑 index.ts: 从 return 中移除 modelOverride/providerOverride',
        ))

    # G7: extractStableRoutingParts 函数存在（Option C，2026-03-06 续）
    if 'function extractStableRoutingParts(' not in content:
        issues.append(Issue(
            idx=0, category='G', severity='alert',
            title='G7 - extractStableRoutingParts 函数缺失（Option C 路由标签未生效）',
            detail=f'文件: {MESSAGE_INJECTOR}\n'
                   f'影响: 渠道会话无法生成路由标签 prependContext，LLM 不输出声明\n'
                   f'该函数负责从 declarationText 提取 pool/model/sessionType（延续/新对话）',
            fix_description='手动编辑 index.ts: 添加 extractStableRoutingParts() 函数',
        ))

    # G8: isChannelSession 使用正则白名单（whitelist 修复，2026-03-06 续）
    # 检测 isChannelSession 定义是否使用精确的 discord|telegram 白名单正则
    ics_match = re.search(r'const isChannelSession\s*=\s*([^\n;]+)', content)
    if ics_match:
        ics_expr = ics_match.group(1)
        if 'discord|telegram' not in ics_expr or 'test(sessionKey)' not in ics_expr:
            issues.append(Issue(
                idx=0, category='G', severity='warn',
                title='G8 - isChannelSession 未使用白名单正则（agent:main:main 双重输出风险）',
                detail=f'当前表达式: {ics_expr.strip()}\n'
                       f'影响: agent:main:main 等后台 session 也会注入 routingInstruction，\n'
                       f'导致路由标签在 Discord/Telegram 回复中出现两遍\n'
                       f'期望: /^agent:main:(discord|telegram):/.test(sessionKey)\n'
                       f'文件: {MESSAGE_INJECTOR}',
                fix_description='手动编辑 index.ts: isChannelSession = /^agent:main:(discord|telegram):/.test(sessionKey)',
            ))

    return issues


def check_session_integrity() -> list[Issue]:
    """F: 检查 session_model_state.json 中的 fallbackChain 完整性"""
    issues = []
    if not SESSION_STATE.exists():
        return issues

    # Load valid provider names from openclaw.json
    valid_providers: set[str] = set()
    if OPENCLAW_JSON.exists():
        try:
            with open(OPENCLAW_JSON) as f:
                config = json.load(f)
            valid_providers = set(config.get('models', {}).get('providers', {}).keys())
        except Exception:
            pass

    with open(SESSION_STATE) as f:
        sessions = json.load(f)

    f1_sessions = []  # fallbackChain 缺失或长度 ≤ 1
    f2_entries = []   # fallbackChain 含无效 provider 前缀

    for key, state in sessions.items():
        chain = state.get('fallbackChain')

        # F1: missing or too short
        if not chain or len(chain) <= 1:
            f1_sessions.append(key)

        # F2: invalid provider prefix in chain entries
        if chain:
            for entry in chain:
                if not isinstance(entry, str) or '/' not in entry:
                    continue
                provider = entry.split('/')[0]
                if valid_providers and provider not in valid_providers:
                    f2_entries.append((key, entry, provider))

    if f1_sessions:
        names = '\n'.join(f'- {k[:70]}' for k in f1_sessions)
        issues.append(Issue(
            idx=0, category='F', severity='alert',
            title=f'F1 - fallbackChain 缺失/过短: {len(f1_sessions)} 个 session',
            detail=names + '\n影响: runtime fallback 永远无法推进（chain.length=1 时 agent_end 无法切换模型）\n'
                          '建议: 补充完整 fallbackChain（参考 pools.json 模型列表）',
            fix_description=f'为 {len(f1_sessions)} 个 session 补充默认 fallbackChain（Intelligence 池）',
        ))

    if f2_entries:
        detail_lines = [f'- [{k[:40]}] {entry} (provider={prov})' for k, entry, prov in f2_entries]
        issues.append(Issue(
            idx=0, category='F', severity='alert',
            title=f'F2 - fallbackChain 含无效 provider 引用: {len(f2_entries)} 处',
            detail='\n'.join(detail_lines) + '\n影响: gateway 路由到不存在的 provider，导致 503 model_not_found\n'
                                             '建议: 替换为有效的 provider/model 引用',
            fix_description=f'替换 {len(f2_entries)} 处无效 provider 引用',
        ))

    return issues


# ─── 报告生成 ────────────────────────────────────────────────────────────────

def collect_all_issues() -> list[Issue]:
    all_issues = []
    all_issues.extend(check_prompt_drift())
    all_issues.extend(check_cron_jobs())
    all_issues.extend(check_orphan_sessions())
    all_issues.extend(check_token_trend())
    all_issues.extend(check_cache_config())
    all_issues.extend(check_code_integrity())
    all_issues.extend(check_session_integrity())

    # 分配编号
    for i, issue in enumerate(all_issues, start=1):
        issue.idx = i

    return all_issues


def format_report(issues: list[Issue], dry_run: bool = False) -> str:
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    prefix = '[DRY RUN] ' if dry_run else ''

    ok_count = 7 - len(set(i.category for i in issues))  # 7个类别，减去有问题的
    alert_count = sum(1 for i in issues if i.severity == 'alert')
    warn_count = sum(1 for i in issues if i.severity == 'warn')

    lines = [
        f'{prefix}🔍 OpenClaw 48h 健康报告 ({now})',
        '',
    ]

    if not issues:
        lines += [
            '✅ 全部正常，无需操作',
            '',
            '监控范围：Prompt 体积 / Cron Job / Session / Token 趋势 / 缓存配置 / 代码完整性 / Session 完整性',
        ]
        return '\n'.join(lines)

    status_parts = []
    if alert_count:
        status_parts.append(f'🔴 告警: {alert_count}')
    if warn_count:
        status_parts.append(f'🟡 警告: {warn_count}')
    if ok_count > 0:
        status_parts.append(f'✅ 正常类别: {ok_count}/4')
    lines.append(' | '.join(status_parts))
    lines.append('')
    lines.append('问题清单:')

    for issue in issues:
        sev_icon = '🔴' if issue.severity == 'alert' else '🟡'
        lines.append(f'\n{sev_icon} [{issue.idx}] [{issue.category}] {issue.title}')
        for detail_line in issue.detail.split('\n'):
            lines.append(f'   {detail_line}')
        if issue.fix_description:
            lines.append(f'   💊 修复: {issue.fix_description}')

    lines += [
        '',
        '─' * 40,
        '回复以下内容执行修复（发给主代理）:',
        f'• "health fix all" — 执行全部 ({len(issues)} 项)',
    ]

    if len(issues) > 1:
        idx_str = ' '.join(str(i.idx) for i in issues)
        lines.append(f'• "health fix {idx_str}" — 选择执行')

    lines.append('• "health skip" — 本次忽略')

    return '\n'.join(lines)


def execute_fix(issues: list[Issue], selected_indices: list[int], dry_run: bool = False):
    """执行选定问题的修复"""
    selected = [i for i in issues if i.idx in selected_indices]
    if not selected:
        print('未找到匹配的问题编号')
        return

    for issue in selected:
        print(f'\n▶ 修复 [{issue.idx}] {issue.title}')

        # Category B: Cron Job violations
        if issue.category == 'B':
            if dry_run:
                print('  [DRY RUN] 将修复违规 Cron Job')
            else:
                _fix_cron_jobs()

        # Category C: Orphan sessions
        elif issue.category == 'C':
            if dry_run:
                print('  [DRY RUN] 将清理过期 Session')
            else:
                _fix_orphan_sessions()

        # Category F: Session integrity
        elif issue.category == 'F':
            if dry_run:
                print('  [DRY RUN] 将修复 Session fallbackChain 完整性问题')
            else:
                _fix_session_integrity()

        # Category A/D/E: manual fixes needed
        else:
            print(f'  ⚠️  需要手动处理: {issue.fix_description}')

    print('\n修复完成。建议重启 gateway: openclaw gateway restart')


def _fix_cron_jobs():
    """修复 Cron Job 违规"""
    with open(CRON_JOBS) as f:
        jobs_data = json.load(f)

    jobs = jobs_data if isinstance(jobs_data, list) else jobs_data.get('jobs', list(jobs_data.values()))
    fixed = 0

    for job in jobs:
        if job.get('status') == 'disabled':
            continue
        payload = job.get('payload', {})
        if payload.get('kind') != 'agentTurn':
            continue

        changed = False
        if job.get('sessionKey') is not None:
            job['sessionKey'] = None
            changed = True
        if 'timeoutSeconds' not in payload:
            payload['timeoutSeconds'] = 120
            changed = True
        model = payload.get('model', '')
        if any(em in model.lower() for em in EXPENSIVE_MODELS):
            payload['model'] = 'custom-llmapi-lovbrowser-com/google/gemini-2.5-flash'
            changed = True

        if changed:
            job['payload'] = payload
            fixed += 1

    with open(CRON_JOBS, 'w') as f:
        json.dump(jobs_data, f, indent=2, ensure_ascii=False)

    print(f'  ✅ 修复了 {fixed} 个 Cron Job')


def _fix_orphan_sessions():
    """清理过期 Session"""
    with open(SESSION_STATE) as f:
        sessions = json.load(f)

    now_ms = int(time.time() * 1000)
    stale_ms = SESSION_STALE_DAYS * 24 * 3600 * 1000

    keys_to_remove = [
        k for k, v in sessions.items()
        if (ts := v.get('lastPatchedAt', v.get('updatedAt', 0))) and (now_ms - ts) > stale_ms
    ]

    for k in keys_to_remove:
        del sessions[k]

    with open(SESSION_STATE, 'w') as f:
        json.dump(sessions, f, indent=2, ensure_ascii=False)

    print(f'  ✅ 清理了 {len(keys_to_remove)} 个过期 Session: {keys_to_remove}')


def _fix_session_integrity():
    """修复 Session fallbackChain 完整性问题（F1 + F2）"""
    with open(SESSION_STATE) as f:
        sessions = json.load(f)

    # Load valid providers from openclaw.json for F2 check
    valid_providers: set[str] = set()
    if OPENCLAW_JSON.exists():
        try:
            with open(OPENCLAW_JSON) as f2:
                config = json.load(f2)
            valid_providers = set(config.get('models', {}).get('providers', {}).keys())
        except Exception:
            pass

    # Default fallbackChain for Intelligence pool sessions (most common)
    DEFAULT_INTELLIGENCE_CHAIN = [
        "custom-llmapi-lovbrowser-com/anthropic/claude-sonnet-4.6",
        "custom-llmapi-lovbrowser-com/anthropic/claude-opus-4.6",
        "custom-llmapi-lovbrowser-com/openai/gpt-5.3-codex",
        "kimi-coding/k2p5",
        "zai/glm-5",
    ]

    fixed_f1 = 0
    fixed_f2 = 0

    for key, state in sessions.items():
        chain = state.get('fallbackChain')

        # F1: supplement missing/short fallbackChain
        if not chain or len(chain) <= 1:
            # Use pool-appropriate chain; fallback to Intelligence chain
            pool = state.get('pool', 'Intelligence')
            state['fallbackChain'] = DEFAULT_INTELLIGENCE_CHAIN[:]
            if 'model' in state and state['model'] not in state['fallbackChain']:
                state['fallbackChain'].insert(0, state['model'])
            state.setdefault('fallbackIndex', 0)
            fixed_f1 += 1
            continue  # F2 check will be done on next run after F1 fix

        # F2: replace invalid provider prefixes
        if valid_providers:
            new_chain = []
            changed = False
            for entry in chain:
                if isinstance(entry, str) and '/' in entry:
                    provider = entry.split('/')[0]
                    if provider not in valid_providers:
                        # Replace with lovbrowser-proxied version using model path from entry
                        model_path = entry[len(provider) + 1:]
                        # Handle openai-codex/gpt-5.3-codex -> openai/gpt-5.3-codex via lovbrowser
                        if 'gpt-5.3-codex' in model_path:
                            new_entry = f"custom-llmapi-lovbrowser-com/openai/gpt-5.3-codex"
                        else:
                            new_entry = f"custom-llmapi-lovbrowser-com/{model_path}"
                        new_chain.append(new_entry)
                        changed = True
                        fixed_f2 += 1
                    else:
                        new_chain.append(entry)
                else:
                    new_chain.append(entry)
            if changed:
                state['fallbackChain'] = new_chain

    with open(SESSION_STATE, 'w') as f:
        json.dump(sessions, f, indent=2, ensure_ascii=False)

    print(f'  ✅ F1 修复了 {fixed_f1} 个缺失 fallbackChain 的 session')
    print(f'  ✅ F2 替换了 {fixed_f2} 处无效 provider 引用')


# ─── 主程序 ──────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]

    dry_run = '--dry-run' in args
    do_report = '--report' in args or dry_run
    fix_arg = None
    fix_all = False

    for i, arg in enumerate(args):
        if arg == '--fix' and i + 1 < len(args):
            fix_arg = args[i + 1]
        if arg == 'all' and i > 0 and args[i-1] == '--fix':
            fix_all = True
    if 'all' in args and '--fix' in args:
        fix_all = True

    list_fixes = '--list-fixes' in args

    issues = collect_all_issues()

    should_report = do_report or (not fix_arg and not list_fixes)
    if should_report:
        report = format_report(issues, dry_run=dry_run)
        print(report)
        REPORT_FILE.write_text(report)

    if list_fixes:
        print('\n可执行的修复命令:')
        for issue in issues:
            if issue.fix_cmd:
                print(f'  [{issue.idx}] {issue.fix_cmd}')
            elif issue.fix_description:
                print(f'  [{issue.idx}] (手动) {issue.fix_description}')

    if fix_arg or fix_all:
        if fix_all:
            selected = [i.idx for i in issues]
        else:
            selected = [int(x.strip()) for x in re.split(r'[,\s]+', fix_arg) if x.strip().isdigit()]
        execute_fix(issues, selected, dry_run=dry_run)

    # Exit code: 0 = all clear, 1 = warnings, 2 = alerts
    if any(i.severity == 'alert' for i in issues):
        sys.exit(2)
    elif issues:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
