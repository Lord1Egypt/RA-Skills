#!/usr/bin/env python3
"""Infoseek keys CLI —— KeyManager 全生命周期管理命令（v1.0.1 PATCH / P3）

用法:
    python scripts/infoseek_keys_cli.py add <provider> <key> [--quota N] [--persist] [--env]
    python scripts/infoseek_keys_cli.py list
    python scripts/infoseek_keys_cli.py stat [provider]
    python scripts/infoseek_keys_cli.py rotate <provider>
    python scripts/infoseek_keys_cli.py revoke <provider> [--fingerprint xxxx]
    python scripts/infoseek_keys_cli.py quota <provider> <limit>
    python scripts/infoseek_keys_cli.py persist [--file path]
    python scripts/infoseek_keys_cli.py load [--file path]
    python scripts/infoseek_keys_cli.py usage [--file path]

说明:
- 会话内注册（add）默认仅当前进程；--persist 加密落盘 ~/.infoseek/keys.enc.json
- --env 同时写入 os.environ（当前进程内对其他模块生效）
- 所有输出脱敏（key 仅显示前后 4 位）
"""
import sys
import os
import json
import argparse
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'core'))

from key_manager import KeyManager, BUILTIN_PROVIDERS, KeyManagementError

PROVIDER_NAMES = sorted(BUILTIN_PROVIDERS.keys())


def _mask(key: str) -> str:
    if not key:
        return '(empty)'
    return f'{key[:4]}***{key[-4:]}' if len(key) > 8 else '***'


def cmd_add(args) -> int:
    km = KeyManager.instance()
    km.register(args.provider, args.key, quota_limit=args.quota)
    if args.env:
        env_name = BUILTIN_PROVIDERS.get(args.provider, f'{args.provider.upper()}_API_KEY')
        os.environ[env_name] = args.key
    msg = f"已注册 {args.provider} → {_mask(args.key)}"
    if args.quota:
        msg += f"（配额 {args.quota} 次）"
    # CLI 持久化仓库语义：add 默认加密落盘（跨进程可见）
    try:
        p = km.save_keys(path=args.persist_file)
        msg += f"，已加密落盘 {p}"
    except KeyManagementError as e:
        msg += f"，⚠️ 未落盘: {e}"
    print(msg)
    return 0


def cmd_list(args) -> int:
    km = KeyManager.instance()
    stats = km.stats()
    if not stats:
        print("（无已注册 key，env 也未配置）")
        return 0
    print(f"{'provider':16s} {'source':9s} {'status':12s} {'used':>5s} {'quota':>6s} {'key':24s}")
    for provider in sorted(stats):
        for rec in stats[provider]:
            quota = rec.get('quota_limit')
            qs = str(quota) if quota is not None else '-'
            print(f"{provider:16s} {rec.get('source',''):9s} {rec.get('status',''):12s} "
                  f"{rec.get('used_count',0):5d} {qs:>6s} {rec.get('key_fingerprint',''):24s}")
    return 0


def cmd_stat(args) -> int:
    km = KeyManager.instance()
    stats = km.stats()
    targets = [args.provider] if args.provider else sorted(stats)
    for provider in targets:
        recs = stats.get(provider)
        if not recs:
            print(f"[{provider}] 未配置")
            continue
        for rec in recs:
            print(f"[{provider}] source={rec.get('source')} status={rec.get('status')} "
                  f"fail={rec.get('fail_count')} used={rec.get('used_count')} "
                  f"cooldown={rec.get('circuit_open_until', 0) > 0}")
    return 0


def cmd_rotate(args) -> int:
    km = KeyManager.instance()
    ok = km.rotate(args.provider)
    if ok:
        try:
            km.save_keys(path=getattr(args, 'persist_file', None))  # 跨进程持久
        except KeyManagementError:
            pass
    print(f"[{args.provider}] {'轮换成功（最旧 key 置后）' if ok else '无可用 key 或仅 1 个，无需轮换'}")
    return 0 if ok else 1


def cmd_revoke(args) -> int:
    km = KeyManager.instance()
    n = km.revoke(args.provider, key_fingerprint=args.fingerprint)
    if n:
        try:
            km.save_keys(path=getattr(args, 'persist_file', None))  # 跨进程持久
        except KeyManagementError:
            pass
    print(f"[{args.provider}] 已吊销 {n} 个 key"
          + (f"（指纹 {args.fingerprint}）" if args.fingerprint else "（全部）"))
    return 0


def cmd_quota(args) -> int:
    km = KeyManager.instance()
    km.set_quota(args.provider, args.limit)
    print(f"[{args.provider}] 配额上限 = {args.limit} 次（用尽自动切换/降级）")
    return 0


def cmd_persist(args) -> int:
    km = KeyManager.instance()
    try:
        p = km.save_keys(path=args.file)
    except KeyManagementError as e:
        print(f"[错误] {e}")
        return 1
    print(f"已加密落盘: {p}（密钥文件 {Path(str(p)).with_suffix('.key')}）")
    return 0


def cmd_load(args) -> int:
    km = KeyManager.instance()
    try:
        n = km.load_keys(path=args.file)
    except KeyManagementError as e:
        print(f"[错误] {e}")
        return 1
    print(f"已加载 {n} 个 key")
    return 0


def cmd_usage(args) -> int:
    km = KeyManager.instance()
    rep = km.usage_report(path=args.file)
    if 'error' in rep:
        print(f"[错误] {rep['error']}")
        return 1
    print(f"{'provider':16s} {'calls':>6s} {'fail':>5s} {'est_cost_usd':>14s} {'statuses'}")
    for r in rep['rows']:
        print(f"{r['provider']:16s} {r['calls']:6d} {r['fail_count']:5d} "
              f"{r['est_cost_usd']:14.6f} {','.join(r['statuses'])}")
    print(f"合计估算成本: ${rep['total_est_cost_usd']:.6f}")
    return 0


def cmd_export(args) -> int:
    """合规审计导出（v1.0.1 PATCH / 合规审计项）：
    用量/成本报表 → CSV 或 JSON 文件（供审计/报表工具消费）。
    """
    import csv as csv_mod
    km = KeyManager.instance()
    rep = km.usage_report(path=args.usage_file)
    if 'error' in rep:
        print(f"[错误] {rep['error']}")
        return 1
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fmt = args.format.lower()
    if fmt == 'csv':
        with open(out_path, 'w', newline='', encoding='utf-8') as f:
            w = csv_mod.writer(f)
            w.writerow(['provider', 'calls', 'fail_count', 'est_cost_usd', 'statuses'])
            for r in rep['rows']:
                w.writerow([r['provider'], r['calls'], r['fail_count'],
                            r['est_cost_usd'], ','.join(r['statuses'])])
            w.writerow(['TOTAL', '', '', rep['total_est_cost_usd'], ''])
    else:  # json
        out_path.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"已导出 {fmt.upper()} 审计报表 → {out_path}")
    print(f"  providers={len(rep['rows'])}  total_cost=${rep['total_est_cost_usd']:.6f}")
    return 0


def cmd_backup(args) -> int:
    """加密仓库备份（v1.0.1 B3）：导出数据文件 + 密钥文件（拷贝，非移动）。"""
    from shutil import copy2
    km = KeyManager.instance()
    try:
        p = km.save_keys(path=args.file)
    except KeyManagementError as e:
        print(f"[错误] {e}")
        return 1
    data_f = Path(p)
    key_f = Path(str(p)).with_suffix('.key')
    # 备份目录场景：把数据+密钥文件拷贝到备份位置
    backup_dir = args.backup_dir
    if backup_dir:
        bd = Path(backup_dir)
        bd.mkdir(parents=True, exist_ok=True)
        dst_data = bd / data_f.name
        dst_key = bd / key_f.name
        copy2(data_f, dst_data)
        if key_f.exists():
            copy2(key_f, dst_key)
        print(f"已备份加密仓库 → {bd}")
        print(f"  数据: {dst_data}")
        print(f"  密钥: {dst_key}（务必妥善保管，丢失将无法恢复）")
    else:
        print(f"已生成备份（数据+密钥）:")
        print(f"  数据: {data_f}")
        print(f"  密钥: {key_f}（务必妥善保管，丢失将无法恢复）")
    return 0


def cmd_restore(args) -> int:
    """从加密备份恢复（v1.0.1 B3）：load_keys 加载指定备份数据文件。"""
    km = KeyManager.instance()
    try:
        n = km.load_keys(path=args.file)
    except KeyManagementError as e:
        print(f"[错误] {e}")
        return 1
    print(f"已从备份恢复 {n} 个 key（源: {args.file}）")
    return 0


def cmd_keyring_persist(args) -> int:
    """将当前注册池写入系统 keyring（v1.0.1 B1 闭环）。"""
    km = KeyManager.instance()
    try:
        n = km.save_to_keyring(service=args.service)
    except KeyManagementError as e:
        print(f"[错误] {e}")
        return 1
    print(f"已写入系统 keyring {n} 个 key（service={args.service}）")
    return 0


def cmd_keyring_load(args) -> int:
    """从系统 keyring 恢复 key（v1.0.1 B1 闭环）。"""
    km = KeyManager.instance()
    try:
        n = km.load_from_keyring(service=args.service)
    except KeyManagementError as e:
        print(f"[错误] {e}")
        return 1
    print(f"已从系统 keyring 恢复 {n} 个 key（service={args.service}）")
    return 0


# ── 引擎全生命周期管理（v1.0.1 评估升级 P2）──
def cmd_engine_status(args) -> int:
    """查看各搜索引擎健康/配额/认证状态（engine_lifecycle）。"""
    try:
        from engine_lifecycle import get_lifecycle
    except ImportError:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from engine_lifecycle import get_lifecycle
    lc = get_lifecycle()
    st = lc.status()
    if not st:
        print("（暂无引擎状态记录；首次搜索后开始累计）")
        return 0
    print(f"{'引擎':<16}{'状态':<10}{'失败':<6}{'最后错误':<12}{'配额':<8}{'认证':<8}{'API漂移'}")
    print("-" * 78)
    for name, s in sorted(st.items()):
        disabled = lc.is_disabled(name)
        if disabled:
            state = "禁用"
        elif s["fail_count"] > 0:
            state = f"降权({s['fail_count']})"
        else:
            state = "正常"
        quota = "耗尽" if s.get("quota_exhausted") else "-"
        auth = "损坏" if s.get("auth_broken") else "-"
        drift = "⚠变更" if s.get("api_changed") else "-"
        print(f"{name:<16}{state:<10}{s['fail_count']:<6}{s['last_error']:<12}{quota:<8}{auth:<8}{drift}")
    return 0


def cmd_engine_reset(args) -> int:
    """重置引擎健康/配额/认证状态（可选 --engine 单引擎）。"""
    try:
        from engine_lifecycle import get_lifecycle
    except ImportError:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from engine_lifecycle import get_lifecycle
    lc = get_lifecycle()
    lc.reset(name=args.engine)
    print(f"已重置引擎状态{'：' + args.engine if args.engine else '（全部）'}")
    return 0


def cmd_engine_reconcile(args) -> int:
    """新鲜度对账（P3）：自动清零到重置时刻的配额标记 / 冷却期满的认证标记。"""
    try:
        from engine_lifecycle import get_lifecycle
    except ImportError:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from engine_lifecycle import get_lifecycle
    lc = get_lifecycle()
    if args.engine:
        changed = 1 if lc.reconcile(args.engine) else 0
        print(f"已对账引擎 {args.engine}：{'状态已更新' if changed else '无需变更'}")
    else:
        changed = lc.reconcile_all()
        print(f"全量对账完成：{changed} 个引擎状态已自动恢复")
    return 0


def cmd_engine_probe(args) -> int:
    """存活探测（P3）：对账全部引擎并报告恢复项（实弹探测在 _call_engine 内 lazy 触发）。"""
    try:
        from engine_lifecycle import get_lifecycle
    except ImportError:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from engine_lifecycle import get_lifecycle
    lc = get_lifecycle()
    changed = lc.reconcile_all()
    st = lc.status()
    if not st:
        print("（暂无引擎状态记录；首次搜索后开始累计）")
        return 0
    print(f"存活探测完成：{changed} 个引擎经对账自动恢复")
    print(f"{'引擎':<16}{'状态':<10}{'配额重置':<14}{'API漂移':<10}{'上次对账':<14}")
    print("-" * 70)
    for name, s in sorted(st.items()):
        disabled = lc.is_disabled(name)
        state = "禁用" if disabled else ("降权" if s["fail_count"] > 0 else "正常")
        rat = s.get("quota_reset_at", 0)
        quota = "—" if not s.get("quota_exhausted") else (
            "已过期" if rat and time.time() >= rat else "待重置")
        drift = "⚠变更" if s.get("api_changed") else "—"
        lr = s.get("last_reconcile", 0)
        lr_s = time.strftime("%m-%d %H:%M", time.localtime(lr)) if lr else "—"
        print(f"{name:<16}{state:<10}{quota:<14}{drift:<10}{lr_s:<14}")
    return 0


def cmd_capability_status(args) -> int:
    """能力注册表状态（T8/B2 审计 UX）：声明启用 / env 闸 / consent 授权 / 综合生效 / 降级链。"""
    try:
        from core import capability_registry as cr
    except ImportError:
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from core import capability_registry as cr
    cr.reload()
    caps = cr.list_capabilities()
    if not caps:
        print("（注册表为空）")
        return 0
    hdr = f"{'能力':<20}{'kind':<26}{'声明':<6}{'env闸':<8}{'consent':<9}{'生效':<6}降级链"
    print(hdr)
    print("-" * 100)
    for c in sorted(caps, key=lambda x: (x.get("kind", ""), x.get("name", ""))):
        name = c.get("name", "")
        kind = c.get("kind", "")
        declared = "ON" if c.get("enabled") else "off"
        env_v = os.environ.get(c.get("env_var") or f"INFOSEEK_ENABLE_{name.upper()}", "")
        env_s = "set" if env_v else "-"
        cons = "✓" if cr.consent_granted(name) else ("✗" if c.get("requires_consent") else "-")
        eff = "ON" if cr.is_effective_enabled(name) else "-"
        chain = "→".join(cr.degrade_chain(name))
        print(f"{name:<20}{kind:<26}{declared:<6}{env_s:<8}{cons:<9}{eff:<6}{chain}")
    print("-" * 100)
    cl = cr.consent_log_path()
    print(f"consent.log: {cl or '(不可用)'}")
    return 0


def cmd_audit_report(args) -> int:
    """归因/取证审计报表（T8/B2）：聚合 audit.log，含取证降级统计。"""
    try:
        from core.state_dir import audit_log_path
    except ImportError:
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from core.state_dir import audit_log_path
    from collections import Counter
    p = audit_log_path()
    if not os.path.exists(p):
        print(f"（审计日志不存在: {p}）")
        return 0
    lines = open(p, encoding="utf-8").read().splitlines()
    ident = [l for l in lines if "[identity_attribution]" in l]
    foren = [l for l in lines if "[account_forensics]" in l]
    other = [l for l in lines if l and "[identity_attribution]" not in l
             and "[account_forensics]" not in l]
    print("=" * 72)
    print("Infoseek 合规审计报表（T8）")
    print("=" * 72)
    print(f"审计总行数: {len(lines)} | 身份归因: {len(ident)} | 账号取证: {len(foren)} | 其他: {len(other)}")
    deg = Counter()
    for l in ident:
        if "skipped-no-consent" in l:
            deg["skipped_no_consent"] += 1
        elif "skipped-disabled" in l:
            deg["skipped_disabled"] += 1
        elif "manual_review" in l and "gap" in l:
            deg["manual_review_gap"] += 1
        elif "exhausted" in l:
            deg["capability_exhausted"] += 1
        else:
            deg["ok_or_other"] += 1
    fdeg = Counter()
    for l in foren:
        if "insufficient" in l or "降级" in l:
            fdeg["降级/不足"] += 1
        else:
            fdeg["深度取证完成"] += 1
    print("\n[身份归因] 降级分布:")
    for k, v in deg.most_common():
        print(f"  {k:<24}{v}")
    print("\n[账号取证] 通道统计:")
    for k, v in (fdeg.most_common() or [("（无记录）", 0)]):
        print(f"  {k:<24}{v}")
    if args.json:
        import json
        print(json.dumps({"total": len(lines), "identity": len(ident), "forensics": len(foren),
                          "identity_degradation": dict(deg), "forensics_stats": dict(fdeg)},
                         ensure_ascii=False, indent=1))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description='infoseek keys —— KeyManager 生命周期管理 CLI')
    sub = ap.add_subparsers(dest='cmd', required=True)

    p_add = sub.add_parser('add', help='注册 key 并加密落盘（跨进程持久）')
    p_add.add_argument('provider', choices=PROVIDER_NAMES, help='provider 名')
    p_add.add_argument('key', help='API key 明文')
    p_add.add_argument('--quota', type=int, default=None, help='配额上限（次）')
    p_add.add_argument('--persist-file', default=None, help='加密数据文件（默认 ~/.infoseek/keys.enc.json）')
    p_add.add_argument('--env', action='store_true', help='同时写入 os.environ')
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser('list', help='列出全部 key（脱敏）')
    p_list.set_defaults(func=cmd_list)

    p_stat = sub.add_parser('stat', help='查看健康/用量状态')
    p_stat.add_argument('provider', nargs='?', default=None, help='指定 provider（默认全部）')
    p_stat.set_defaults(func=cmd_stat)

    p_rot = sub.add_parser('rotate', help='轮换（最旧 key 置后）')
    p_rot.add_argument('provider', choices=PROVIDER_NAMES)
    p_rot.add_argument('--persist-file', default=None)
    p_rot.set_defaults(func=cmd_rotate)

    p_rev = sub.add_parser('revoke', help='吊销 key')
    p_rev.add_argument('provider', choices=PROVIDER_NAMES)
    p_rev.add_argument('--fingerprint', default=None, help='key 指纹（后 4+ 位，默认吊销全部）')
    p_rev.add_argument('--persist-file', default=None)
    p_rev.set_defaults(func=cmd_revoke)

    p_quota = sub.add_parser('quota', help='设置配额上限')
    p_quota.add_argument('provider', choices=PROVIDER_NAMES)
    p_quota.add_argument('limit', type=int)
    p_quota.set_defaults(func=cmd_quota)

    p_persist = sub.add_parser('persist', help='加密落盘当前注册 key')
    p_persist.add_argument('--file', default=None, help='数据文件路径（默认 ~/.infoseek/keys.enc.json）')
    p_persist.set_defaults(func=cmd_persist)

    p_load = sub.add_parser('load', help='从加密文件加载 key')
    p_load.add_argument('--file', default=None)
    p_load.set_defaults(func=cmd_load)

    p_usage = sub.add_parser('usage', help='用量/成本报表')
    p_usage.add_argument('--file', default=None, help='key_usage.json 路径')
    p_usage.set_defaults(func=cmd_usage)

    p_export = sub.add_parser('export', help='导出用量/成本审计报表（CSV/JSON）')
    p_export.add_argument('output', help='输出文件路径（如 audit.csv / audit.json）')
    p_export.add_argument('--format', choices=['csv', 'json'], default='csv', help='格式（默认 csv）')
    p_export.add_argument('--usage-file', default=None, help='key_usage.json 路径')
    p_export.set_defaults(func=cmd_export)

    p_backup = sub.add_parser('backup', help='加密仓库备份（数据 + 密钥文件）')
    p_backup.add_argument('--file', default=None, help='数据文件路径（默认 ~/.infoseek/keys.enc.json）')
    p_backup.add_argument('--backup-dir', default=None, help='备份目录（将拷贝数据+密钥到该目录）')
    p_backup.set_defaults(func=cmd_backup)

    p_restore = sub.add_parser('restore', help='从加密备份恢复 key')
    p_restore.add_argument('file', help='备份数据文件路径')
    p_restore.set_defaults(func=cmd_restore)

    p_kr_p = sub.add_parser('keyring-persist', help='写入系统 keyring（Windows 凭据管理器 / macOS Keychain）')
    p_kr_p.add_argument('--service', default='infoseek', help='keyring service 名（默认 infoseek）')
    p_kr_p.set_defaults(func=cmd_keyring_persist)

    p_kr_l = sub.add_parser('keyring-load', help='从系统 keyring 恢复 key')
    p_kr_l.add_argument('--service', default='infoseek', help='keyring service 名（默认 infoseek）')
    p_kr_l.set_defaults(func=cmd_keyring_load)

    p_eng_st = sub.add_parser('engine-status', help='查看搜索引擎健康/配额/认证状态')
    p_eng_st.set_defaults(func=cmd_engine_status)

    p_eng_rst = sub.add_parser('engine-reset', help='重置引擎健康/配额/认证状态')
    p_eng_rst.add_argument('--engine', default=None, help='仅重置指定引擎（默认全部）')
    p_eng_rst.set_defaults(func=cmd_engine_reset)

    p_eng_rec = sub.add_parser('engine-reconcile', help='新鲜度对账（自动恢复过期的配额/认证禁用）')
    p_eng_rec.add_argument('--engine', default=None, help='仅对账指定引擎（默认全部）')
    p_eng_rec.set_defaults(func=cmd_engine_reconcile)

    p_eng_prb = sub.add_parser('engine-probe', help='存活探测（对账全部引擎并报告恢复项）')
    p_eng_prb.set_defaults(func=cmd_engine_probe)

    p_cap = sub.add_parser('capability-status', help='能力注册表状态（T8：声明/env/consent/生效/降级链）')
    p_cap.set_defaults(func=cmd_capability_status)

    p_aud = sub.add_parser('audit-report', help='合规审计报表（T8：身份归因 + 账号取证降级统计）')
    p_aud.add_argument('--json', action='store_true', help='JSON 输出')
    p_aud.set_defaults(func=cmd_audit_report)

    args = ap.parse_args()
    # CLI 持久化仓库语义：启动时自动加载加密仓库（若存在），
    # 使 add/list/stat/rotate/revoke 跨进程共享同一 key 仓库
    if args.cmd in ('add', 'list', 'stat', 'rotate', 'revoke', 'quota', 'usage', 'export', 'backup', 'keyring-persist', 'keyring-load'):
        try:
            KeyManager.instance().load_keys(path=getattr(args, 'persist_file', None))
        except (KeyManagementError, TypeError):
            try:
                KeyManager.instance().load_keys()
            except KeyManagementError:
                pass  # 仓库损坏/密钥不匹配时静默降级（env 仍可用）
        except Exception:
            pass
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
