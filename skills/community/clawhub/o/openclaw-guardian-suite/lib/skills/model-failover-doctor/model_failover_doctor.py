#!/usr/bin/env python3
# [OC-WM] licensed-to: macmini@MacminideMac-mini | bundle: vendor-suite | ts: 2026-03-09T17:30:16Z
"""
model_failover_doctor.py — OpenClaw Model Failover 诊断修复工具
版本: 1.0.0 (2026-03-05)

诊断和修复"All models failed"根因，适用于大多数 OpenClaw 部署。

根因矩阵：
  MI-1 [致命] before_agent_start 无条件返回 modelOverride/providerOverride，
              导致 Gateway 的所有 fallback 都携带同一错误 model ID（根本原因 A）
  MI-2 [增强] 缺少全局 dead model 注册表（跨 session 共享，防重复踩坑）
  P-1  [数据] pools.json 含无效 provider 前缀的模型引用
  S-1  [数据] session_model_state.json fallbackChain 缺失/过短（<=1）
  S-2  [数据] session_model_state.json fallbackChain 含无效 provider 前缀

自动修复：MI-1, P-1, S-1, S-2（MI-2 仅报告）

用法:
  python3 model_failover_doctor.py                # 诊断报告（不修改任何文件）
  python3 model_failover_doctor.py --fix          # 修复所有可自动修复的问题
  python3 model_failover_doctor.py --fix --restart # 修复后自动重启 gateway
  python3 model_failover_doctor.py --dry-run      # 预览修改内容（不写入）
"""

import json
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# ─── 路径配置（自动发现）──────────────────────────────────────────────────────

BASE          = Path.home() / '.openclaw'
WORKSPACE     = BASE / 'workspace'
LIB           = WORKSPACE / '.lib'
OPENCLAW_JSON = BASE / 'openclaw.json'
POOLS_JSON    = LIB / 'pools.json'
SESSION_STATE = LIB / 'session_model_state.json'
MESSAGE_INJECTOR = WORKSPACE / '.openclaw' / 'extensions' / 'message-injector' / 'index.ts'
BACKUP_DIR    = LIB / '.mfd_backups'

# ─── 诊断结构 ─────────────────────────────────────────────────────────────────

class Finding:
    def __init__(self, code: str, severity: str, title: str, detail: str,
                 fixable: bool = False, fix_fn=None):
        self.code     = code
        self.severity = severity   # critical / warn / info
        self.title    = title
        self.detail   = detail
        self.fixable  = fixable
        self._fix_fn  = fix_fn

    def fix(self, dry_run: bool = False) -> bool:
        if self._fix_fn:
            return bool(self._fix_fn(dry_run=dry_run))
        return False

# ─── 辅助函数 ─────────────────────────────────────────────────────────────────

def load_json(path: Path) -> Optional[dict]:
    try:
        return json.loads(path.read_text('utf-8'))
    except Exception as e:
        print(f"  ⚠️  无法读取 {path.name}: {e}")
        return None


def backup_file(path: Path) -> Path:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts  = datetime.now().strftime('%Y%m%d-%H%M%S')
    dst = BACKUP_DIR / f"{path.name}.{ts}.bak"
    shutil.copy2(path, dst)
    return dst


def get_valid_providers() -> set:
    cfg = load_json(OPENCLAW_JSON)
    if not cfg:
        return set()
    return set(cfg.get('models', {}).get('providers', {}).keys())


def get_lovbrowser_model_ids() -> list:
    """返回 lovbrowser provider 下所有 model id"""
    cfg = load_json(OPENCLAW_JSON)
    if not cfg:
        return []
    lb = 'custom-llmapi-lovbrowser-com'
    return [m['id'] for m in
            cfg.get('models', {}).get('providers', {}).get(lb, {}).get('models', [])]


# ─── MI-1：modelOverride/providerOverride 毒化检查 ───────────────────────────

def check_mi1() -> Optional[Finding]:
    """
    检测 before_agent_start 是否无条件返回 modelOverride + providerOverride。

    症状：Gateway 尝试每个 fallback 时仍携带相同 modelOverride，
          导致 kimi-coding/k2p5 收到 model=openai/gpt-5.3-codex 等错误。
    表现："All models failed (6): ... No available channel for model <X>"
          且 6 个不同 provider 的错误 model ID 全部相同。
    """
    if not MESSAGE_INJECTOR.exists():
        return Finding('MI-1', 'info',
                       'message-injector 未找到，跳过检查',
                       f'路径: {MESSAGE_INJECTOR}')

    content = MESSAGE_INJECTOR.read_text('utf-8')

    # 已修复：有 lockModel 条件包裹
    if re.search(r'\.\.\.\s*\(\s*lockModel\s*\?[^:]+\{\s*modelOverride\s*,\s*providerOverride', content):
        return None  # good

    # 坏模式：return 块中 modelOverride 与 providerOverride 相邻出现（无条件）
    bad = re.search(
        r'modelOverride,[ \t]*\n[ \t]*providerOverride,',
        content
    )
    if not bad:
        return None  # 未发现坏模式（可能已用其他方式处理）

    return Finding(
        code='MI-1', severity='critical',
        title='before_agent_start 无条件返回 modelOverride/providerOverride（根因 A）',
        detail=(
            '问题: Gateway 进行 fallback 时，会将 before_agent_start 返回的\n'
            '      modelOverride/providerOverride 应用到所有 fallback 尝试，\n'
            '      导致 kimi-coding、zai、minimax 等 provider 都收到了错误的 model ID。\n'
            '修复: 将返回值包装在 lockModel 条件中，正常路由只依赖 sessions.patch。'
        ),
        fixable=True,
        fix_fn=_fix_mi1,
    )


def _fix_mi1(dry_run: bool = False) -> bool:
    content = MESSAGE_INJECTOR.read_text('utf-8')

    # 精确匹配：两行相邻
    pattern = re.compile(
        r'(\n([ \t]*)modelOverride,[ \t]*\n[ \t]*)providerOverride,',
        re.MULTILINE,
    )
    match = pattern.search(content)
    if not match:
        print('  ⚠️  未找到可替换的模式，请手动修复')
        return False

    indent = match.group(2)
    # 将两行合并为一个条件展开
    fixed = pattern.sub(
        f'\n{indent}...(lockModel ? {{ modelOverride, providerOverride }} : {{}}),',
        content,
        count=1,
    )

    if dry_run:
        print(f'  [DRY RUN] 将修改 {MESSAGE_INJECTOR.name}')
        print(f'  - modelOverride,')
        print(f'  - providerOverride,')
        print(f'  + ...(lockModel ? {{ modelOverride, providerOverride }} : {{}}),')
        return True

    bak = backup_file(MESSAGE_INJECTOR)
    MESSAGE_INJECTOR.write_text(fixed, 'utf-8')
    print(f'  备份: {bak.name}')
    print(f'  ✅ MI-1 已修复: {MESSAGE_INJECTOR}')
    return True


# ─── MI-2：全局 dead model 注册表缺失检查（仅报告）─────────────────────────

def check_mi2() -> Optional[Finding]:
    if not MESSAGE_INJECTOR.exists():
        return None

    content = MESSAGE_INJECTOR.read_text('utf-8')
    if 'globalDeadModels' in content:
        return None

    return Finding(
        code='MI-2', severity='warn',
        title='缺少全局 dead model 注册表（跨 session 共享）',
        detail=(
            '问题: 某模型返回 model_not_found 后，其他 session（包括子代理）\n'
            '      无法感知，会重复踩坑直到 gateway 重启。\n'
            '\n'
            '需在 message-injector/index.ts 添加：\n'
            '\n'
            '  // 在 sessionState 声明后:\n'
            '  const globalDeadModels = new Map<string, number>();\n'
            '  const DEAD_MODEL_TTL = 2 * 60 * 60 * 1000; // 2h\n'
            '\n'
            '  // 新增辅助函数（在 isFallbackWorthyError 前）:\n'
            '  function isDeadModelError(e: string) {\n'
            '    return e.includes("model_not_found") ||\n'
            '           e.includes("no available channel") ||\n'
            '           e.includes("model not found");\n'
            '  }\n'
            '  function filterDeadModels(chain: string[]) {\n'
            '    const now = Date.now();\n'
            '    return chain.filter(m => {\n'
            '      const ts = globalDeadModels.get(m);\n'
            '      return !ts || (now - ts) >= DEAD_MODEL_TTL;\n'
            '    });\n'
            '  }\n'
            '\n'
            '  // 在 agent_end 的 if (!isFallbackWorthyError(err)) return; 后:\n'
            '  if (isDeadModelError(err) && state.model) {\n'
            '    globalDeadModels.set(state.model, Date.now());\n'
            '    api.logger.warn(`semantic-router: model marked dead (2h) -> ${state.model}`);\n'
            '  }\n'
            '\n'
            '  // C-branch: const fallbackChain = filterDeadModels([targetModel, ...])\n'
            '  // B-branch: const reconcileFallbacks = filterDeadModels([currentModel, ...])'
        ),
        fixable=False,
    )


# ─── P-1：pools.json 无效 provider 引用 ─────────────────────────────────────

def check_p1() -> Optional[Finding]:
    if not POOLS_JSON.exists():
        return None

    pools = load_json(POOLS_JSON)
    if not pools:
        return None

    valid = get_valid_providers()
    if not valid:
        return None  # 无法验证，跳过

    bad = []
    for pool_name, pool_data in pools.items():
        if pool_name == 'version' or not isinstance(pool_data, dict):
            continue
        for field in ['primary', 'fallback_1', 'fallback_2', 'fallback_3', 'fallback_4']:
            val = pool_data.get(field, '')
            if not val or '/' not in val:
                continue
            provider = val.split('/')[0]
            if provider not in valid:
                bad.append((pool_name, field, val, provider))

    if not bad:
        return None

    lines = [f'  {pool}.{field}: "{val}" (provider="{prov}" 不存在)'
             for pool, field, val, prov in bad]
    return Finding(
        code='P-1', severity='critical',
        title=f'pools.json 含 {len(bad)} 处无效 provider 引用',
        detail='\n'.join(lines) + f'\n  有效 providers: {sorted(valid)}',
        fixable=True,
        fix_fn=lambda dry_run=False: _fix_p1(bad, dry_run),
    )


def _fix_p1(bad_entries: list, dry_run: bool = False) -> bool:
    pools    = load_json(POOLS_JSON)
    lb       = 'custom-llmapi-lovbrowser-com'
    lb_ids   = get_lovbrowser_model_ids()
    valid    = get_valid_providers()
    changed  = False

    for pool_name, field, val, prov in bad_entries:
        model_path = val[len(prov) + 1:]   # 去掉 "bad-provider/" 前缀

        # 1) 精确匹配 lovbrowser 模型 ID
        new_val = None
        for mid in lb_ids:
            if model_path == mid or model_path.endswith(mid.split('/')[-1]):
                new_val = f'{lb}/{mid}'
                break

        # 2) 尝试其他 valid provider（精确 provider/model 拆分）
        if new_val is None:
            for vp in valid:
                if model_path.startswith(vp + '/'):
                    new_val = model_path  # model_path IS already provider/model
                    break

        # 3) 最后兜底：挂到 lovbrowser
        if new_val is None:
            new_val = f'{lb}/{model_path}'

        if dry_run:
            print(f'  [DRY RUN] {pool_name}.{field}: "{val}" → "{new_val}"')
        else:
            pools[pool_name][field] = new_val
            print(f'  修复: {pool_name}.{field}: "{val}" → "{new_val}"')
        changed = True

    if changed and not dry_run:
        bak = backup_file(POOLS_JSON)
        POOLS_JSON.write_text(json.dumps(pools, indent=4, ensure_ascii=False), 'utf-8')
        print(f'  备份: {bak.name}')
        print(f'  ✅ P-1 已修复: {POOLS_JSON}')

    return changed


# ─── S-1 / S-2：session_model_state.json 完整性检查 ─────────────────────────

def check_session_issues() -> list[Finding]:
    findings = []
    if not SESSION_STATE.exists():
        return findings

    sessions = load_json(SESSION_STATE)
    if not sessions:
        return findings

    valid  = get_valid_providers()
    pools  = load_json(POOLS_JSON) or {}

    # S-1: fallbackChain 缺失/过短
    s1_keys = [
        k for k, v in sessions.items()
        if not v.get('fallbackChain') or len(v['fallbackChain']) <= 1
    ]
    if s1_keys:
        findings.append(Finding(
            code='S-1', severity='critical',
            title=f'session fallbackChain 缺失/过短: {len(s1_keys)} 个',
            detail=('\n'.join(f'  - {k[:72]}' for k in s1_keys) +
                    '\n  影响: agent_end runtime fallback 无法推进（chain 只有 1 个元素）'),
            fixable=True,
            fix_fn=lambda dry_run=False: _fix_s1(s1_keys, sessions, pools, dry_run),
        ))

    # S-2: 无效 provider 前缀
    if valid:
        s2 = []
        for k, v in sessions.items():
            for entry in v.get('fallbackChain', []):
                if isinstance(entry, str) and '/' in entry:
                    prov = entry.split('/')[0]
                    if prov not in valid:
                        s2.append((k, entry, prov))
        if s2:
            detail_lines = [f'  [{k[:40]}] "{e}" (provider="{p}")'
                            for k, e, p in s2]
            findings.append(Finding(
                code='S-2', severity='critical',
                title=f'session fallbackChain 含无效 provider: {len(s2)} 处',
                detail=('\n'.join(detail_lines) +
                        '\n  影响: Gateway 路由到不存在的 provider → 503 model_not_found'),
                fixable=True,
                fix_fn=lambda dry_run=False: _fix_s2(s2, sessions, dry_run),
            ))

    return findings


def _build_fallback_chain(pool_name: str, current_model: str, pools: dict) -> list:
    """基于 pools.json 为给定 pool 构建合理的 fallbackChain"""
    pool  = pools.get(pool_name, {})
    chain = []
    if current_model:
        chain.append(current_model)
    for field in ['primary', 'fallback_1', 'fallback_2', 'fallback_3', 'fallback_4']:
        m = pool.get(field, '')
        if m and m not in chain:
            chain.append(m)

    # 兜底：Intelligence 池的常见配置
    if len(chain) <= 1:
        chain = [
            'custom-llmapi-lovbrowser-com/anthropic/claude-sonnet-4.6',
            'custom-llmapi-lovbrowser-com/anthropic/claude-opus-4.6',
            'custom-llmapi-lovbrowser-com/openai/gpt-5.3-codex',
            'kimi-coding/k2p5',
            'zai/glm-5',
        ]
    return chain


def _fix_s1(s1_keys: list, sessions: dict, pools: dict, dry_run: bool = False) -> bool:
    for key in s1_keys:
        state = sessions[key]
        chain = _build_fallback_chain(state.get('pool', 'Intelligence'),
                                      state.get('model', ''), pools)
        if dry_run:
            print(f'  [DRY RUN] {key[:64]}: 添加 fallbackChain ({len(chain)} 个模型)')
        else:
            state['fallbackChain'] = chain
            state.setdefault('fallbackIndex', 0)

    if not dry_run:
        bak = backup_file(SESSION_STATE)
        SESSION_STATE.write_text(json.dumps(sessions, indent=2, ensure_ascii=False), 'utf-8')
        print(f'  备份: {bak.name}')
        print(f'  ✅ S-1 已修复: {len(s1_keys)} 个 session')
    return True


def _fix_s2(s2_entries: list, sessions: dict, dry_run: bool = False) -> bool:
    lb      = 'custom-llmapi-lovbrowser-com'
    lb_ids  = get_lovbrowser_model_ids()
    # 建立替换映射
    fix_map: dict[str, str] = {}
    for _, entry, prov in s2_entries:
        if entry in fix_map:
            continue
        model_path = entry[len(prov) + 1:]
        new_entry  = None
        # 匹配 lovbrowser 模型
        for mid in lb_ids:
            if model_path == mid or model_path.endswith(mid.split('/')[-1]):
                new_entry = f'{lb}/{mid}'
                break
        if new_entry is None:
            new_entry = f'{lb}/{model_path}'
        fix_map[entry] = new_entry
        if dry_run:
            print(f'  [DRY RUN] "{entry}" → "{new_entry}"')

    if not dry_run:
        affected = set(k for k, _, _ in s2_entries)
        for key in affected:
            state = sessions[key]
            state['fallbackChain'] = [
                fix_map.get(e, e) for e in state.get('fallbackChain', [])
            ]
        bak = backup_file(SESSION_STATE)
        SESSION_STATE.write_text(json.dumps(sessions, indent=2, ensure_ascii=False), 'utf-8')
        print(f'  备份: {bak.name}')
        print(f'  ✅ S-2 已修复: {len(fix_map)} 处引用')
    return True


# ─── 汇总 & 报告 ─────────────────────────────────────────────────────────────

def run_all_checks() -> list[Finding]:
    findings: list[Finding] = []
    for fn in [check_mi1, check_mi2]:
        f = fn()
        if f:
            findings.append(f)
    findings.extend(check_session_issues())
    p1 = check_p1()
    if p1:
        findings.append(p1)
    return findings


SEV_ICON = {'critical': '🔴', 'warn': '🟡', 'info': 'ℹ️'}


def print_report(findings: list[Finding]) -> None:
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    print(f'\n🩺 OpenClaw Model Failover Doctor — {now}\n{"─" * 48}')

    if not findings:
        print('✅ 未发现问题，模型 Failover 配置正常。\n'
              '   覆盖: MI-1 / MI-2 / P-1 / S-1 / S-2')
        return

    critical = sum(1 for f in findings if f.severity == 'critical')
    warn     = sum(1 for f in findings if f.severity == 'warn')
    print(f'发现 {len(findings)} 个问题  🔴 致命: {critical}  🟡 警告: {warn}\n')

    for i, f in enumerate(findings, 1):
        icon    = SEV_ICON.get(f.severity, '•')
        fix_tag = '✏️ 可自动修复' if f.fixable else '🖐 需手动处理'
        print(f'{icon} [{i}] [{f.code}] {f.title}  {fix_tag}')
        for line in f.detail.strip().split('\n'):
            print(f'     {line}')
        print()


# ─── 主程序 ──────────────────────────────────────────────────────────────────

def main() -> None:
    args    = set(sys.argv[1:])
    do_fix  = '--fix' in args
    restart = '--restart' in args
    dry_run = '--dry-run' in args
    if dry_run:
        do_fix = True

    findings = run_all_checks()
    print_report(findings)

    if not findings:
        sys.exit(0)

    if not do_fix:
        fixable = sum(1 for f in findings if f.fixable)
        if fixable:
            script = Path(__file__).name
            print(f'💊 运行以下命令自动修复 {fixable} 个问题:')
            print(f'   python3 {script} --fix --restart\n')
        sys.exit(2 if any(f.severity == 'critical' for f in findings) else 1)

    # ── 执行修复 ──────────────────────────────────────────────────────────────
    label = '[DRY RUN] ' if dry_run else ''
    fixable = [f for f in findings if f.fixable]
    print(f'\n{label}执行修复 ({len(fixable)} 项可自动修复)...\n{"─" * 40}')

    any_fixed = False
    for f in fixable:
        print(f'▶ [{f.code}] {f.title}')
        if f.fix(dry_run=dry_run):
            any_fixed = True
        print()

    manual = [f for f in findings if not f.fixable]
    if manual:
        print('⚠️  以下问题需手动处理:')
        for f in manual:
            print(f'\n  [{f.code}] {f.title}')
            for line in f.detail.strip().split('\n'):
                print(f'  {line}')
        print()

    if any_fixed and not dry_run:
        if restart:
            print('🔄 重启 gateway...')
            r = subprocess.run(['openclaw', 'gateway', 'restart'],
                               capture_output=True, text=True)
            print((r.stdout or r.stderr).strip())
        else:
            print('💡 修复已完成，请执行: openclaw gateway restart')


if __name__ == '__main__':
    main()
