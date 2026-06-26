#!/usr/bin/env python3
"""
DRG查询工具 - 基于CHS-DRG2.0完整版
用法: python drg_lookup_tool.py <icd|adrg|drg|mdc> [编码]
示例:
  python drg_lookup_tool.py icd I21.0
  python drg_lookup_tool.py adrg FF9
  python drg_lookup_tool.py drg FR21
  python drg_lookup_tool.py mdc
"""
import json, sys

DATA = "/workspace/skills/ICD-Coding/data"

def load():
    with open(f"{DATA}/drg_weight.json", encoding="utf-8") as f:
        w = json.load(f)
    with open(f"{DATA}/drg_icd_map.json", encoding="utf-8") as f:
        m = json.load(f)
    return w, m

def q_icd(code):
    w, m = load()
    r = []
    up = code.upper()
    # exact
    if up in m["icd_to_mdc"]:
        e = m["icd_to_mdc"][up]
        mdc_id = e["mdc"]; adrg = e["adrg"]
        mdc_n = w["mdc_names"].get(mdc_id, {}).get("name", mdc_id)
        adrg_n = w["adrg_names"].get(adrg, adrg)
        drgs = w["adrg_to_drg"].get(adrg, [])
        lines = []
        for d in drgs:
            wt = d.get("weight", "")
            lr = " ⚠️低风险" if d.get("low_risk") else ""
            wts = f" | 权重:{wt}" if wt else ""
            lines.append(f"    {d['code']} {d['name']}{wts}{lr}")
        r.append(f"【精确】ICD: {up} {e['name']}\n  → MDC: {mdc_id} {mdc_n}\n  → ADRG: {adrg} {adrg_n}\n  → DRG:\n" + ("\n".join(lines) if lines else "    （无细分组）"))
    # prefix
    pre = up[:4]
    for icd, e in m["icd_to_mdc"].items():
        if icd.startswith(pre) and icd != up and len(r) < 6:
            mdc_id = e["mdc"]; adrg = e["adrg"]
            mdc_n = w["mdc_names"].get(mdc_id, {}).get("name", mdc_id)
            adrg_n = w["adrg_names"].get(adrg, adrg)
            drgs = w["adrg_to_drg"].get(adrg, [])[:3]
            lines = [f"    {d['code']} {d['name']}" for d in drgs]
            r.append(f"【前缀匹配】ICD: {icd} {e['name']}\n  → MDC: {mdc_id} {mdc_n}\n  → ADRG: {adrg} {adrg_n}\n  → DRG样例:\n" + "\n".join(lines))
    return r

def q_adrg(code):
    w, m = load()
    up = code.upper()
    if up in w["adrg_names"]:
        adrg_n = w["adrg_names"][up]
        drgs = w["adrg_to_drg"].get(up, [])
        lines = []
        for d in drgs:
            wt = d.get("weight", "")
            lr = " ⚠️低风险" if d.get("low_risk") else ""
            wts = f" | 权重:{wt}" if wt else ""
            lines.append(f"    {d['code']} {d['name']}{wts}{lr}")
        return [f"【ADRG→DRG】ADRG: {up} {adrg_n}\n  共{len(drgs)}个DRG细分组:\n" + "\n".join(lines)] if lines else [f"【ADRG→DRG】ADRG: {up} {adrg_n}\n  （无DRG细分组数据）"]
    # fuzzy
    fuzzy = []
    for k, v in w["adrg_names"].items():
        if up in k or up in v:
            drgs2 = w["adrg_to_drg"].get(k, [])
            if drgs2:
                lines2 = [f"    {d['code']} {d['name']}" for d in drgs2[:3]]
                fuzzy.append(f"【模糊】ADRG: {k} {v}\n  → DRG样例:\n" + "\n".join(lines2))
    return fuzzy[:5]

def q_drg(code):
    w, m = load()
    up = code.upper()
    wt = w["weight_by_code"].get(up, "")
    # find name via adrg mapping
    nm = None
    for adrg, drgs in w["adrg_to_drg"].items():
        for d in drgs:
            if d["code"] == up:
                nm = d["name"]
                break
    if wt or nm:
        return [f"【DRG权重】{up} {nm or ''}\n  权重: {wt or '待确认'}"]
    return []

def q_mdc():
    w, m = load()
    lines = ["【MDC分类】26个主要诊断大类:"]
    for k in sorted(w["mdc_names"].keys()):
        v = w["mdc_names"][k]
        lines.append(f"  {k} {v['name']}（含{v.get('adrg_count',0)}个ADRG）")
    return ["\n".join(lines)]

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == "help":
        print(__doc__)
        sys.exit(0)
    mode = sys.argv[1].lower()
    query = sys.argv[2] if len(sys.argv) > 2 else ""
    fn = {"icd": q_icd, "adrg": q_adrg, "drg": q_drg, "mdc": q_mdc}.get(mode)
    if not fn:
        print("未知模式:", mode)
    else:
        res = fn(query) if query else fn()
        if not res:
            print(f"未找到: {query}")
        else:
            for r in res:
                print(r)
                print()
