#!/usr/bin/env python3
"""octo-mention 消费端查询接口

输入别名字符串 → 输出匹配的 uid / canonical_name / 置信度（含时间衰减）列表。
解决「收到消息里有个『小田』，秒查到 uid」的反向查询需求。

时间衰减：超过 decay_days 未见新证据的别名，每满 decay_days 天 ×decay_factor，
使过时称呼自然沉底。原始 confidence 不改，仅查询时计算 effective_confidence。

用法:
  python3 lookup_alias.py --db openclaw.json --alias 小田
  python3 lookup_alias.py --db openclaw.json --alias 小田 --group g1 --json
  python3 lookup_alias.py --db openclaw.json --alias 小田 --include-uncertain
"""
import argparse, json, sys
from datetime import datetime, timezone, timedelta

CN_TZ = timezone(timedelta(hours=8))
DECAY_DAYS = 30
DECAY_FACTOR = 0.9


def parse_time(s):
    if not s:
        return None
    for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
        try:
            dt = datetime.strptime(s, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=CN_TZ)
            return dt
        except ValueError:
            continue
    return None


def decayed_conf(conf, last_time, now, decay_days, decay_factor):
    lt = parse_time(last_time)
    if not lt:
        return round(conf, 3), 0
    age_days = (now - lt).total_seconds() / 86400
    if age_days <= decay_days:
        return round(conf, 3), 0
    periods = int(age_days // decay_days)
    eff = conf * (decay_factor ** periods)
    return round(eff, 3), periods


def lookup(db, alias, group=None, include_uncertain=False,
           decay_days=DECAY_DAYS, decay_factor=DECAY_FACTOR, now=None):
    now = now or datetime.now(CN_TZ)
    results = []
    for uid, p in db.get("persons", {}).items():
        lists = [("alias", p.get("aliases", []))]
        if include_uncertain:
            lists.append(("uncertain", p.get("uncertain_aliases", [])))
        for kind, al_list in lists:
            for a in al_list:
                if a.get("alias") != alias:
                    continue
                if group and group not in a.get("groups", []):
                    continue
                eff, periods = decayed_conf(
                    a.get("confidence", 0), a.get("last_evidence_time"),
                    now, decay_days, decay_factor)
                results.append({
                    "uid": uid,
                    "canonical_name": p.get("canonical_name"),
                    "member_type": p.get("member_type"),
                    "alias": alias,
                    "alias_type": a.get("alias_type"),
                    "confidence": a.get("confidence"),
                    "effective_confidence": eff,
                    "decay_periods": periods,
                    "evidence_count": a.get("evidence_count"),
                    "groups": a.get("groups", []),
                    "kind": kind,
                })
    results.sort(key=lambda r: -r["effective_confidence"])
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True)
    ap.add_argument("--alias", required=True)
    ap.add_argument("--group", default=None, help="限定在某群出现过的别名")
    ap.add_argument("--include-uncertain", action="store_true")
    ap.add_argument("--decay-days", type=int, default=DECAY_DAYS)
    ap.add_argument("--decay-factor", type=float, default=DECAY_FACTOR)
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    db = json.load(open(args.db, encoding="utf-8"))
    res = lookup(db, args.alias, args.group, args.include_uncertain,
                 args.decay_days, args.decay_factor)
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return
    if not res:
        print(f"未找到别名「{args.alias}」的匹配")
        sys.exit(1)
    print(f"别名「{args.alias}」匹配 {len(res)} 项：")
    for r in res:
        decay = f" (衰减×{args.decay_factor}^{r['decay_periods']})" if r["decay_periods"] else ""
        print(f"  {r['canonical_name']} [{r['uid']}] {r['member_type']} | "
              f"eff_conf={r['effective_confidence']}{decay} "
              f"(orig={r['confidence']}, ev={r['evidence_count']}, groups={r['groups']}, {r['kind']})")


if __name__ == "__main__":
    main()
