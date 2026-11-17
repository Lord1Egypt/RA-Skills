#!/usr/bin/env python3
"""Deterministic name and address checker using speaker, wording, and target."""
import json, sys

def edit_distance_at_most_one(left, right):
    """Return whether two names differ by one insertion, deletion, or substitution."""
    if left == right:
        return True
    if abs(len(left) - len(right)) > 1:
        return False
    if len(left) > len(right):
        left, right = right, left
    i = j = edits = 0
    while i < len(left) and j < len(right):
        if left[i] == right[j]:
            i += 1; j += 1
        else:
            edits += 1
            if edits > 1:
                return False
            if len(left) == len(right):
                i += 1; j += 1
            else:
                j += 1
    edits += (len(left) - i) + (len(right) - j)
    return edits <= 1

def main(path):
    data = json.load(open(path, encoding="utf-8"))
    people = {p["id"]: p for p in data["people"] if isinstance(p.get("id"), str) and p["id"].strip()}
    variants = {}
    for p in people.values():
        for name in [p["name"], *p.get("aliases", [])]:
            variants.setdefault(name, []).append(p["id"])
    approved = {}
    for r in data.get("rules", []):
        approved[(r.get("speaker"), r.get("address"), r.get("target"))] = r
    findings = []
    for x in data["mentions"]:
        token, anchor, speaker, target = x["token"], x["anchor"], x.get("speaker"), x.get("target")
        ids = variants.get(token, [])
        if x.get("kind") == "address":
            if not speaker:
                findings.append([anchor, token, "待确认", "缺少说话人 ID", "补充说话人 ID 后再核对；保留原文"])
            elif speaker not in people:
                findings.append([anchor, token, "待确认", f"说话人 ID {speaker} 不在角色表中", "补充有效角色资料；保留原文"])
            elif not target:
                if len(ids) > 1:
                    findings.append([anchor, token, "待确认", "同名或同别名归属多个角色，且缺少称呼对象 ID，无法区分", "补充角色 ID 或可区分的上下文后再核对；保留原文"])
                else:
                    findings.append([anchor, token, "待确认", "缺少称呼对象 ID", "确认称呼对象后再核对；保留原文"])
            elif target not in people:
                findings.append([anchor, token, "待确认", f"称呼对象 ID {target} 不在角色表中", "补充有效角色资料；保留原文"])
            else:
                # Once speaker and target are both valid, an absent exact
                # triple is a decidable wrong address. Missing identity data
                # and unresolvable duplicate names were handled above.
                triple_approved = (speaker, token, target) in approved
                if not triple_approved:
                    # A target outside every registered owner is decisive even
                    # when the written form belongs to multiple people.  The
                    # ambiguity is about which owner it denotes, not whether it
                    # can denote this explicitly supplied target.
                    if ids and target not in ids:
                        owners = "、".join(people[owner]["name"] for owner in ids)
                        actual = people[target]["name"]
                        reason = f"称呼“{token}”已登记归属{owners}，此处对象为{actual}，不属于任何已登记归属；不存在该说话人、称呼和对象三者同时匹配的批准规则"
                        suggestion = f"仅核对此处：对象既为{actual}，请改用其已批准称呼或确认对象；不得全局替换“{token}”"
                        findings.append([anchor, token, "错称", reason, suggestion])
                    else:
                        reason = "说话人和对象明确，但该称呼关系未获批准"
                        suggestion = "核对该处称呼并请作者确认可用称呼；确认前保留原文，不猜测替换"
                        findings.append([anchor, token, "错称", reason, suggestion])
        elif not ids:
            # Only flag a likely typo when the target is explicit and exactly
            # one registered name is one character away.
            near = [(name, owner) for name, owners in variants.items() for owner in owners if edit_distance_at_most_one(token, name)]
            target_candidates = {(name, owner) for name, owner in near if owner == target}
            if target in people and len(target_candidates) == 1:
                corrected = next(iter(target_candidates))[0]
                findings.append([anchor, token, "错称", f"该写法未登记，且与对象 {target} 的已确认姓名变体“{corrected}”仅差一字", f"仅此处核对并将错拼“{token}”改为已确认写法“{corrected}”；不得全局替换"])
            else:
                findings.append([anchor, token, "待确认", "姓名或别名没有明确归属", "补充姓名/别名归属或确认对象；保留原文"])
        elif target and target not in people:
            findings.append([anchor, token, "待确认", f"对象 ID {target} 不在角色表中", "补充有效角色资料；保留原文"])
        elif target and target in ids:
            pass  # Explicit stable ID resolves a duplicate written name.
        elif target and target not in ids:
            findings.append([anchor, token, "错称", "实名或别名归属与该处对象不一致", f"仅此处核对对象 {target}；不得全局替换"])
        elif len(ids) > 1:
            findings.append([anchor, token, "待确认", "同名人物无法区分，且此处没有匹配的角色 ID", "补充角色 ID 或可区分的上下文后再核对；保留原文"])
    print(json.dumps({"variants": variants, "findings": findings}, ensure_ascii=False, indent=2))

if __name__ == "__main__": main(sys.argv[1])
