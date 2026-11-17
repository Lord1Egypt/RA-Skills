#!/usr/bin/env python3
"""mcp_tools_keys.py — Infoseek MCP Key 管理工具（G11 拆分 v1.0.1）"""
import sys
from typing import Any, Dict

from mcp_tools_common import INFOSEEK_ROOT


# ══ 以下函数由 G11 拆分脚本从 infoseek_mcp_server.py 提取（v1.0.1）══

def tool_manage_keys(args: Dict) -> Dict:
    """v1.0.1 PATCH: Key 生命周期管理（list / stat / rotate / revoke）

    所有输出脱敏（仅指纹），不暴露明文 key。
    """
    import sys
    sys.path.insert(0, str(INFOSEEK_ROOT / 'core'))
    try:
        from key_manager import KeyManager
    except ImportError:
        return {"error": "key_manager 模块未找到"}

    action = args.get('action', '')
    provider = args.get('provider', '')
    fingerprint = args.get('fingerprint', '')
    km = KeyManager.instance()
    # 尝试加载持久化仓库（跨进程）
    try:
        km.load_keys()
    except Exception:
        pass

    if action == 'list':
        stats = km.stats()
        rows = []
        for p in sorted(stats):
            for rec in stats[p]:
                rows.append({
                    'provider': p, 'source': rec.get('source'), 'status': rec.get('status'),
                    'used': rec.get('used_count'), 'quota': rec.get('quota_limit'),
                    'fail': rec.get('fail_count'), 'fingerprint': rec.get('key_fingerprint'),
                })
        return {'count': len(rows), 'keys': rows, 'masked': True}

    if action == 'stat':
        if not provider:
            return {"error": "stat 需要 provider 参数"}
        stats = km.stats()
        recs = stats.get(provider, [])
        return {'provider': provider, 'keys': recs, 'masked': True}

    if action == 'rotate':
        if not provider:
            return {"error": "rotate 需要 provider 参数"}
        ok = km.rotate(provider)
        try:
            km.save_keys()
        except Exception:
            pass
        return {'provider': provider, 'rotated': ok}

    if action == 'revoke':
        if not provider:
            return {"error": "revoke 需要 provider 参数"}
        n = km.revoke(provider, key_fingerprint=fingerprint or None)
        try:
            km.save_keys()
        except Exception:
            pass
        return {'provider': provider, 'revoked': n}

    return {"error": f"未知 action: {action}（支持 list/stat/rotate/revoke）"}


def tool_key_usage(args: Dict) -> Dict:
    """v1.0.1 PATCH: Key 用量/成本报表（基于 key_usage.json）"""
    import sys
    sys.path.insert(0, str(INFOSEEK_ROOT / 'core'))
    try:
        from key_manager import KeyManager
    except ImportError:
        return {"error": "key_manager 模块未找到"}
    rep = KeyManager.instance().usage_report()
    if 'error' in rep:
        return rep
    return {'rows': rep['rows'], 'total_est_cost_usd': rep['total_est_cost_usd'],
            'source': rep['source']}

