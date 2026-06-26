#!/usr/bin/env python3
"""octo-mention 跨群人物映射合并工具 (person-centric)

同一个 uid 在不同群里是同一个实体。本工具把某个群的分析结果(--new，单群扁平
结构，含 group_id)按 uid 合并进统一的人物映射库(--base)——同一人在所有群观测到
的称呼汇聚成一条记录，每条别名证据标注来源 group_id。

核心思想：以 uid 为全局主键跨群合并，不按群分区。

汇总文件结构 (persons.v1):
{
  "schema": "octo-mention.persons.v1",
  "version": N,
  "last_updated": "...",
  "persons": {
    "<uid>": {
      "uid", "canonical_name", "member_type",
      "owner_uid", "owner", "owns_bots",
      "seen_in_groups": ["<gid>", ...],
      "aliases": [ {alias, alias_type, confidence, evidence_count,
                    evidence:[{time,sender,text,group_id}], groups:[gid], reason} ],
      "uncertain_aliases": [...],
      "conflicts": [...]
    }
  }
}

--new 接受:
  1) 单群扁平: {"group_id":..., "members":[...]}
  2) persons 容器: {"persons": {...}}  (逐人合并)

用法:
  python3 merge_mentions.py --base openclaw.json --new round.json --out openclaw.json
"""
import argparse, json, os
from datetime import datetime, timezone, timedelta

CN_TZ = timezone(timedelta(hours=8))
MAX_EVIDENCE = 5  # 每个 alias 最多保留的证据条数（按时间取最新；evidence_count 仍记真实总数）


def now_iso():
    return datetime.now(CN_TZ).isoformat(timespec="seconds")


def ev_key(e):
    return (e.get("time", ""), e.get("sender", ""), e.get("text", ""), e.get("group_id", ""))


def confidence_from_count(n, base_conf, alias_type, n_groups):
    """证据越多、跨群使用越广，置信度越高。"""
    cap = 0.95 if alias_type == "self_declared" else 0.9
    bumped = base_conf + max(0, n - 1) * 0.03 + max(0, n_groups - 1) * 0.02
    return round(min(cap, max(base_conf, bumped)), 2)


def merge_alias_list(base_aliases, new_aliases, rejected_names=None):
    """合并别名列表。locked=True 的条目不被自动分析覆盖；rejected_names 中的词不被收录。"""
    rejected_names = set(rejected_names or [])
    by_alias = {a["alias"]: json.loads(json.dumps(a)) for a in base_aliases}
    for a in new_aliases:
        key = a["alias"]
        # 拒绝词拦截：rejected 列表中的别名不收录
        if key in rejected_names:
            continue
        if key not in by_alias:
            by_alias[key] = json.loads(json.dumps(a))
            continue
        tgt = by_alias[key]
        # locked 保护：人工锁定的条目不被自动分析覆盖
        if tgt.get("locked") and a.get("source") != "manual":
            continue
        prev_total = tgt.get("evidence_count", len(tgt.get("evidence", [])))
        seen = {ev_key(e) for e in tgt.get("evidence", [])}
        added = 0
        for e in a.get("evidence", []):
            if ev_key(e) not in seen:
                tgt.setdefault("evidence", []).append(e)
                seen.add(ev_key(e))
                added += 1
        # 增量计数：真实总数 = 原总数 + 本轮新增去重证据（不受裁剪影响）
        tgt["evidence_count"] = max(prev_total + added, a.get("evidence_count", 0), len(tgt.get("evidence", [])))
        # 证据裁剪：按 time 倒序只保留最新 MAX_EVIDENCE 条（evidence_count 仍为真实总数）
        if len(tgt.get("evidence", [])) > MAX_EVIDENCE:
            tgt["evidence"] = sorted(
                tgt["evidence"], key=lambda e: e.get("time", ""), reverse=True
            )[:MAX_EVIDENCE]
        # 合并来源群
        groups = set(tgt.get("groups", [])) | set(a.get("groups", []))
        groups |= {e.get("group_id") for e in tgt.get("evidence", []) if e.get("group_id")}
        groups.discard(None)
        tgt["groups"] = sorted(groups)
        if a.get("alias_type"):
            tgt["alias_type"] = a["alias_type"]
        if a.get("reason"):
            tgt["reason"] = a["reason"]
        base_conf = max(tgt.get("confidence", 0), a.get("confidence", 0))
        tgt["confidence"] = confidence_from_count(
            tgt["evidence_count"], base_conf, tgt.get("alias_type", ""), len(tgt["groups"]) or 1
        )
        # 记录最新证据时间（供查询时做时间衰减）
        all_times = [e.get("time", "") for e in tgt.get("evidence", [])] + [tgt.get("last_evidence_time", "")]
        tgt["last_evidence_time"] = max(t for t in all_times if t) if any(all_times) else ""
    # 为新增（未走合并分支）的 alias 补 last_evidence_time
    for a in by_alias.values():
        if "last_evidence_time" not in a:
            ts = [e.get("time", "") for e in a.get("evidence", [])]
            a["last_evidence_time"] = max(ts) if ts and any(ts) else ""
    return list(by_alias.values())


def merge_person(base_p, new_p):
    out = json.loads(json.dumps(base_p))
    # canonical_name 跨群变更追踪：旧名不同于新名时存入 previous_names，不静默覆盖
    new_name = new_p.get("canonical_name")
    old_name = out.get("canonical_name")
    if new_name and old_name and new_name != old_name:
        prev = out.get("previous_names", [])
        new_gid = (new_p.get("seen_in_groups") or [None])[0]
        if not any(pn.get("name") == old_name for pn in prev):
            prev.append({"name": old_name, "group_id": new_gid,
                         "last_seen": new_p.get("analyzed_at") or now_iso()})
        out["previous_names"] = prev
    # 权威字段：new 覆盖（来自最新 API）
    for f in ("canonical_name", "member_type", "owner", "owner_uid", "owns_bots"):
        if new_p.get(f) not in (None, ""):
            out[f] = new_p[f]
    # 合并观测到的群
    sg = set(out.get("seen_in_groups", [])) | set(new_p.get("seen_in_groups", []))
    out["seen_in_groups"] = sorted(sg)
    # 收集 rejected_aliases 名单，自动分析不得收录这些词
    rejected_names = {r.get("alias") for r in base_p.get("rejected_aliases", []) if r.get("alias")}
    out["aliases"] = merge_alias_list(base_p.get("aliases", []), new_p.get("aliases", []), rejected_names)
    out["uncertain_aliases"] = merge_alias_list(
        base_p.get("uncertain_aliases", []), new_p.get("uncertain_aliases", []), rejected_names
    )
    # 保留 rejected_aliases（人工标记的拒绝词）
    out["rejected_aliases"] = base_p.get("rejected_aliases", [])
    seen = {json.dumps(c, sort_keys=True, ensure_ascii=False) for c in base_p.get("conflicts", [])}
    out["conflicts"] = list(base_p.get("conflicts", []))
    for c in new_p.get("conflicts", []):
        k = json.dumps(c, sort_keys=True, ensure_ascii=False)
        if k not in seen:
            out["conflicts"].append(c)
            seen.add(k)
    return out


def flat_group_to_persons(new):
    """把单群扁平结构(members[])转成 persons 字典，证据打 group_id 标签。"""
    gid = new.get("group_id")
    if not gid:
        raise SystemExit("--new 缺少 group_id，无法标注来源群")
    persons = {}
    for m in new.get("members", []):
        uid = m["uid"]
        def tag(al_list):
            out = []
            for a in al_list:
                a2 = json.loads(json.dumps(a))
                for e in a2.get("evidence", []):
                    e.setdefault("group_id", gid)
                a2["groups"] = sorted(set(a2.get("groups", [])) | {gid})
                ts = [e.get("time", "") for e in a2.get("evidence", [])]
                a2["last_evidence_time"] = max(ts) if ts and any(ts) else ""
                out.append(a2)
            return out
        conflicts = []
        for c in m.get("conflicts", []):
            c2 = json.loads(json.dumps(c)); c2.setdefault("group_id", gid)
            conflicts.append(c2)
        p = {
            "uid": uid,
            "canonical_name": m.get("canonical_name") or m.get("member"),
            "member_type": m.get("member_type"),
            "seen_in_groups": [gid],
            "aliases": tag(m.get("aliases", [])),
            "uncertain_aliases": tag(m.get("uncertain_aliases", [])),
            "conflicts": conflicts,
        }
        for k in ("owner_uid", "owner", "owns_bots"):
            if m.get(k) not in (None, ""):
                p[k] = m[k]
        persons[uid] = p
    return persons


def normalize_new(new):
    if "persons" in new:
        return new["persons"]
    return flat_group_to_persons(new)


def merge(base, new):
    if not base:
        base = {"schema": "octo-mention.persons.v1", "version": 0, "persons": {}}
    new_persons = normalize_new(new)
    persons = dict(base.get("persons", {}))
    for uid, np_ in new_persons.items():
        persons[uid] = merge_person(persons[uid], np_) if uid in persons else np_
    return {
        "schema": "octo-mention.persons.v1",
        "version": base.get("version", 0) + 1,
        "last_updated": now_iso(),
        "persons": persons,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--new", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    base = None
    if os.path.exists(args.base) and os.path.getsize(args.base) > 0:
        base = json.load(open(args.base, encoding="utf-8"))
    new = json.load(open(args.new, encoding="utf-8"))

    out = merge(base, new)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    json.dump(out, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"merged -> {args.out} | version={out['version']} persons={len(out['persons'])}")


if __name__ == "__main__":
    main()
