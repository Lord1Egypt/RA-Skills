#!/usr/bin/env python3
"""
core/freshness_cron.py — Infoseek 新鲜度 cron（v2.1.1 新增，v2.2.0 维护）

定期扫描实体元数据（共 7 步）：
1. 应用衰减（90 天半衰期）
2. 冷条目收集（>90 天未出现，待 Wikidata 验证）
3. 冷条目 Wikidata 存在性验证（网络可用时；不可达自动降级）
4. alias 生命周期扫描（v2.2.0 自动清理 stale alias）
5. 实体画像 stale 标注（v2.2.0，90 天未出现自动 stale_profile=True）
6. claim_store TTL 清理（v2.2.0 收尾，180+ 天声明 decay）
7. learned 层冷/噪声实体清理（v2.0.0 收尾，默认 dry_run 统计；近期命中实体受 active_names 保护）

CLI:
  python -m core.freshness_cron full-scan
  python -m core.freshness_cron decay
  python -m core.freshness_cron daemon --interval 7
"""

import sys
import time
from pathlib import Path
from typing import List, Dict, Optional

CORE_DIR = Path(__file__).parent
sys.path.insert(0, str(CORE_DIR))


def _dep_reg():
    """S7：外部依赖可用性统一经 dep_registry 事实层求值（懒加载，缺失回退）。"""
    try:
        import dep_registry as _dr
    except ImportError:
        from core import dep_registry as _dr  # type: ignore
    return _dr


class FreshnessCron:
    """v2.1.1 新鲜度扫描器"""

    def __init__(self, scan_interval_days: int = 7):
        self.interval_days = scan_interval_days

    def run_full_scan(self) -> dict:
        """完整扫描：衰减 + 冷条目验证 + alias 生命周期（v2.2.1）"""
        from entity_tracker import EntityTracker
        from wikidata_sync import WikidataSync

        # 1) 衰减
        decay_stats = EntityTracker().apply_decay()

        # 2) 冷条目
        stale = EntityTracker().get_stale_entities(threshold_days=90)

        # 3) Wikidata 验证（如网络可用）
        wikidata_available = False
        verified, marked_stale = [], []

        if stale:
            try:
                sync = WikidataSync()
                for ent in stale:
                    # Wikidata 验证（网络可用时）
                    name = ent['name']
                    if sync.verify_existence(name):
                        verified.append(name)
                    else:
                        marked_stale.append(name)
                wikidata_available = True
            except Exception as e:
                wikidata_available = False
        # 实体持久层现状（v2.0.0 校正，取代 v1.2.x 旧注释）：entities.py 已有双层
        # 持久层——learn_entity → entities_learned.json（动态回流），EntityTracker →
        # entities_state.json（hit/last_seen/衰减，跨进程）。静态词典仍不被改写，
        # 故 last_verified_at 验证结果以统计字段返回；冷条目清理见下方第 7 步。

        # 4) v2.2.1: alias 生命周期扫描（自动清理 stale alias）
        alias_stats = {'active': 0, 'downgraded': 0, 'stale': 0, 'cleaned': 0}
        try:
            from entity_aliases import EntityAliases
            mgr = EntityAliases()
            lifecycle = mgr.get_lifecycle_stats()
            alias_stats['active'] = lifecycle['stats']['active_count']
            alias_stats['downgraded'] = lifecycle['stats']['downgraded_count']
            alias_stats['stale'] = lifecycle['stats']['stale_count']
            if alias_stats['stale'] > 0:
                clean_result = mgr.clean_stale_aliases(auto_delete=True)
                alias_stats['cleaned'] = clean_result.get('cleaned', 0)
        except Exception:
            pass  # alias 扫描失败不阻断主流程

        # 5) v2.4.0: 实体画像 stale 标注（90 天未出现即标 stale_profile）
        profile_stats = {'scanned': 0, 'marked_stale': 0, 'kept_active': 0}
        try:
            from entity_profile import EntityProfile
            import datetime as _dt
            profiler = EntityProfile()
            profiles = profiler.load()
            today = _dt.date.today()
            updated = False
            for ent_name, p in profiles.items():
                profile_stats['scanned'] += 1
                last_seen = p.get('last_seen')
                stale_flag = False
                if last_seen:
                    try:
                        d = _dt.date.fromisoformat(last_seen)
                        if (today - d).days > 90:
                            stale_flag = True
                    except Exception:
                        pass
                if stale_flag:
                    p['stale_profile'] = True
                    p['stale_marked_at'] = today.isoformat()
                    profile_stats['marked_stale'] += 1
                    updated = True
                else:
                    profile_stats['kept_active'] += 1
                    # 清理已恢复的 stale 标记
                    if p.get('stale_profile'):
                        p.pop('stale_profile', None)
                        p.pop('stale_marked_at', None)
                        updated = True
            if updated:
                profiler.save(profiles)
        except Exception:
            pass

        # 6) v2.4.0: claim_store TTL 清理（release 180+ 天声明）
        claim_decay_stats = {}
        try:
            from claim_store import ClaimStore
            store = ClaimStore()
            claim_decay_stats = store.decay()  # TTL=180
        except Exception:
            pass

        # 7) v2.0.0: learned 层冷/噪声实体清理（实体持久层生命周期收尾）
        # 默认 dry_run 只统计候选不删除（安全）；env INFOSEEK_LEARNED_PRUNE_APPLY=1
        # 才真正原子落盘。近期仍命中（出现在 stale 列表之外）的冷条目受 active_names 保护。
        learned_prune_stats = {'candidates': 0, 'pruned': 0, 'remaining': 0,
                               'dry_run': True, 'applied': False}
        try:
            from entities import prune_learned_entities, get_learned_entities
            # 真实 active_names：全部 learned 实体名 − 当期 stale 名 → 近期仍命中者受保护，
            # 避免空集合放行把所有冷条目一律判候选（D-1 安全收口，R1-a）。
            _all = {e.get('name', '').lower() for e in get_learned_entities(force=True)}
            _stale = {e.get('name', '').lower() for e in stale}
            _active = _all - _stale
            _pr = prune_learned_entities(
                max_age_days=180, min_confidence=0.3,
                active_names=_active, dry_run=True)
            learned_prune_stats = {
                'candidates': len(_pr.get('candidates', [])),
                'pruned': _pr.get('pruned', 0),
                'remaining': _pr.get('remaining', 0),
                'dry_run': _pr.get('dry_run', True),
                'applied': _pr.get('applied', False),
            }
        except Exception:
            pass

        return {
            'decayed_count': decay_stats.get('decayed_count', 0),
            'total_reduction': decay_stats.get('total_reduction', 0),
            'stale_count': len(stale),
            'wikidata_verified': len(verified),
            'wikidata_marked_stale': len(marked_stale),
            'wikidata_available': wikidata_available,
            'alias_active': alias_stats['active'],
            'alias_downgraded': alias_stats['downgraded'],
            'alias_stale': alias_stats['stale'],
            'alias_stale_cleaned': alias_stats['cleaned'],
            # v2.4.0 新增字段
            'profile_scanned': profile_stats['scanned'],
            'profile_marked_stale': profile_stats['marked_stale'],
            'profile_kept_active': profile_stats['kept_active'],
            'claim_decay': claim_decay_stats,
            # v2.0.0 learned 层冷清理统计（默认 dry_run）
            'learned_prune_candidates': learned_prune_stats['candidates'],
            'learned_pruned': learned_prune_stats['pruned'],
            'learned_prune_applied': learned_prune_stats.get('applied', False),
            'scan_time': 'cron',
        }

    def run_incremental_decay(self) -> dict:
        """轻量级：仅衰减（每日可调用）"""
        from entity_tracker import EntityTracker
        return EntityTracker().apply_decay()

    async def run_full_scan_async(self) -> dict:
        """v2.6.3 PATCH: 异步版 freshness_cron

        把 4 个 IO/CPU 步骤并发：
        - decay（CPU 计算）
        - wikidata 验证（网络）
        - alias 生命周期（IO + 计算）
        - profile stale 标注（IO）
        - claim_store TTL decay（IO）

        注：v2.5.4 同步版是 6 步骤串行（~966ms 沙箱，~2-5s 含 wikidata 超时），
        异步版预期降到 ~500ms 沙箱。
        """
        import asyncio
        loop = asyncio.get_event_loop()

        # 步骤 1+2+3+4+5+6 并发
        async def _decay():
            from entity_tracker import EntityTracker
            return await loop.run_in_executor(None, EntityTracker().apply_decay)

        async def _stale_entities():
            from entity_tracker import EntityTracker
            return await loop.run_in_executor(None, EntityTracker().get_stale_entities, 90)

        async def _alias_lifecycle():
            from entity_aliases import EntityAliases
            try:
                mgr = EntityAliases()
                lc = mgr.get_lifecycle_stats()
                stats = {'active': lc['stats']['active_count'],
                        'downgraded': lc['stats']['downgraded_count'],
                        'stale': lc['stats']['stale_count']}
                if stats['stale'] > 0:
                    clean_result = mgr.clean_stale_aliases(auto_delete=True)
                    stats['cleaned'] = clean_result.get('cleaned', 0)
                else:
                    stats['cleaned'] = 0
                return stats
            except Exception:
                return {}

        async def _profile_stale():
            try:
                from entity_profile import EntityProfile
                import datetime as _dt
                profiler = EntityProfile()
                profiles = profiler.load()
                today = _dt.date.today()
                stats = {'scanned': 0, 'marked_stale': 0, 'kept_active': 0}
                updated = False
                for ent_name, p in profiles.items():
                    stats['scanned'] += 1
                    last_seen = p.get('last_seen')
                    stale_flag = False
                    if last_seen:
                        try:
                            d = _dt.date.fromisoformat(last_seen)
                            if (today - d).days > 90:
                                stale_flag = True
                        except Exception:
                            pass
                    if stale_flag:
                        p['stale_profile'] = True
                        p['stale_marked_at'] = today.isoformat()
                        stats['marked_stale'] += 1
                        updated = True
                    else:
                        stats['kept_active'] += 1
                        if p.get('stale_profile'):
                            p.pop('stale_profile', None)
                            p.pop('stale_marked_at', None)
                            updated = True
                if updated:
                    profiler.save(profiles)
                return stats
            except Exception:
                return {}

        async def _claim_decay():
            try:
                from claim_store import ClaimStore
                store = ClaimStore()
                return store.decay()
            except Exception:
                return {}

        # 阶段 1：decay + stale 列表并发
        decay_stats, stale = await asyncio.gather(
            _decay(), _stale_entities(),
        )

        # 阶段 2：剩余步骤并发（wikidata 依赖 stale 结果）
        async def _wikidata_with_stale():
            try:
                if not stale:
                    return [], True
                from wikidata_sync import WikidataSync
                sync = WikidataSync()
                results = []
                for ent in stale:
                    name = ent.get('name', '')
                    if name:
                        verified = await sync.verify_existence_async(name)
                        results.append({'name': name, 'verified': verified})
                wikidata_available = True
                verified_names = [r['name'] for r in results if r['verified']]
                marked = [r['name'] for r in results if not r['verified']]
                return (verified_names, marked, wikidata_available), True
            except Exception:
                return ([], [], False), True
            finally:
                pass

        async def _profile_with_stale():
            try:
                from entity_profile import EntityProfile
                import datetime as _dt
                profiler = EntityProfile()
                profiles = profiler.load()
                today = _dt.date.today()
                stats = {'scanned': 0, 'marked_stale': 0, 'kept_active': 0}
                updated = False
                for ent_name, p in profiles.items():
                    stats['scanned'] += 1
                    last_seen = p.get('last_seen')
                    stale_flag = False
                    if last_seen:
                        try:
                            d = _dt.date.fromisoformat(last_seen)
                            if (today - d).days > 90:
                                stale_flag = True
                        except Exception:
                            pass
                    if stale_flag:
                        p['stale_profile'] = True
                        p['stale_marked_at'] = today.isoformat()
                        stats['marked_stale'] += 1
                        updated = True
                    else:
                        stats['kept_active'] += 1
                        if p.get('stale_profile'):
                            p.pop('stale_profile', None)
                            p.pop('stale_marked_at', None)
                            updated = True
                if updated:
                    profiler.save(profiles)
                return stats
            except Exception:
                return {}

        # 并发：alias + profile + claim + wikidata
        alias_res, profile_res, claim_decay_res, wikidata_res = await asyncio.gather(
            _alias_lifecycle(),
            _profile_with_stale(),
            _claim_decay(),
            _wikidata_with_stale(),
        )

        # 解析 wikidata 结果
        if isinstance(wikidata_res, tuple) and len(wikidata_res) == 2:
            wikidata_data = wikidata_res[0]
            wikidata_available = isinstance(wikidata_data, list)
            if wikidata_available:
                verified_names = [r['name'] for r in wikidata_data if r['verified']]
                marked_names = [r['name'] for r in wikidata_data if not r['verified']]
            else:
                verified_names = []
                marked_names = []
        else:
            wikidata_available = False
            verified_names = []
            marked_names = []

        return {
            'decayed_count': decay_stats.get('decayed_count', 0),
            'total_reduction': decay_stats.get('total_reduction', 0),
            'stale_count': len(stale),
            'wikidata_verified': len(verified_names),
            'wikidata_marked_stale': len(marked_names),
            'wikidata_available': wikidata_available,
            'alias_active': alias_res.get('active', 0),
            'alias_downgraded': alias_res.get('downgraded', 0),
            'alias_stale': alias_res.get('stale', 0),
            'alias_stale_cleaned': alias_res.get('cleaned', 0),
            'profile_scanned': profile_res.get('scanned', 0),
            'profile_marked_stale': profile_res.get('marked_stale', 0),
            'profile_kept_active': profile_res.get('kept_active', 0),
            'claim_decay': claim_decay_res if isinstance(claim_decay_res, dict) else {},
            'scan_time': 'async_cron_v273',
        }

    def start_scheduler(self, interval_days: Optional[int] = None):
        """启动后台调度器（间隔天数扫描一次）。

        S7：schedule 为可选外部依赖，可用性经 dep_registry 统一求值；
        缺失时给出明确安装指引（避免裸 import 报模糊 ModuleNotFoundError）。
        """
        dr = _dep_reg()
        if not dr.is_available("schedule"):
            dr.require("schedule")  # 抛带 install_hint 的依赖缺失错误
        import schedule
        interval = interval_days or self.interval_days

        schedule.every(interval).days.do(self.run_full_scan)
        print(f"[freshness_cron] 调度器启动，间隔 {interval} 天")

        while True:
            schedule.run_pending()
            time.sleep(3600)  # 1h 检查一次


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m core.freshness_cron [full-scan | decay | daemon]")
        sys.exit(1)

    cmd = sys.argv[1]
    cron = FreshnessCron()

    if cmd == 'full-scan':
        import json
        result = cron.run_full_scan()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif cmd == 'decay':
        result = cron.run_incremental_decay()
        print(f"衰减: {result}")
    elif cmd == 'daemon':
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        cron.start_scheduler(interval)
    else:
        print(f"未知命令: {cmd}")


if __name__ == '__main__':
    main()