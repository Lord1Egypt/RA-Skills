#!/usr/bin/env python3
"""
Entity Extractor — 实体关系提取器。

从子结构正文中自动提取实体-关系三元组，增量更新 entity_tracker。
写入 write-sub 管道的第 4 步（非阻断，仅 INFO/WARN）。

数据模型：
  entity_tracker.entities[i] = {
    "id": "ent_001",
    "type": "character|object|location|organization|data",
    "name": "实用擒拿格斗术",
    "attributes": {"status": "active", "owner": "林铁生", "origin": "老贾贩卖,30信用点"},
    "first_chapter": "L01", "first_sub": "S01",
    "last_chapter": "L01", "last_sub": "S01"
  }
  entity_tracker.relations[i] = {
    "id": "rel_001",
    "from_entity": "ent_001",   # 实体 id（非角色名）
    "predicate": "贩卖",
    "to_entity": "ent_002",
    "detail": "30信用点",
    "chapter": "L01", "sub": "S01"
  }
"""
import json, sys, re
from pathlib import Path

# ── 实体类型关键词（提取时参考） ──
LOCATION_SUFFIX = ["巷", "街", "路", "区", "市", "城", "楼", "大厦", "厂", "院", "铺", "摊", "场"]
ORGANIZATION_SUFFIX = ["公司", "集团", "协会", "会", "组织", "联盟", "厂", "社", "所", "院", "局", "处"]
STATUS_CHANGE_TRIGGERS = {
    "摧毁": "destroyed", "损坏": "damaged", "烧毁": "destroyed",
    "修复": "repaired", "重建": "rebuilt", "关闭": "closed",
    "开启": "open", "建立": "active", "成立": "active",
    "出售": "sold", "购买": "owned", "送给": "given",
    "抢夺": "stolen", "丢失": "lost", "死亡": "dead",
    "负伤": "injured", "受伤": "injured", "昏迷": "unconscious",
    "苏醒": "active", "恢复": "active",
}
STATUS_DEGRADING = {"destroyed", "damaged", "closed", "lost", "dead", "injured", "unconscious", "sold", "stolen", "given"}

# ── 关系谓词模式 ──
REL_PATTERNS = [
    (r"(把|将)\s*(.{1,8})\s*(交给|递给|卖给|送给|还给)", "转移"),
    (r"(在|位于|来到|前往|离开)\s*(.{1,8})(?:巷|街|路|区|市|楼|厂|铺|场)", "位于"),
    (r"是\s*.{0,4}(?:的|一位|一名)\s*(?:员工|成员|头目|领导|首领)", "归属"),
    (r"领导\s*.{1,8}(?:组织|团体|联盟|会)", "领导"),
    (r"装有|配备|携带|持有|拥有|带着\s*.{1,8}", "拥有"),
    (r"来自\s*.{1,8}(?:公司|集团|组织|协会)", "来自"),
]


def _make_entity_id(existing: list) -> str:
    """生成自增实体 ID"""
    max_id = 0
    for e in existing:
        m = re.match(r'ent_(\d+)', e.get("id", ""))
        if m:
            max_id = max(max_id, int(m.group(1)))
    return f"ent_{max_id + 1:03d}"


def _make_relation_id(existing: list) -> str:
    """生成自增关系 ID"""
    max_id = 0
    for r in existing:
        m = re.match(r'rel_(\d+)', r.get("id", ""))
        if m:
            max_id = max(max_id, int(m.group(1)))
    return f"rel_{max_id + 1:03d}"


def _entity_name_matches(name: str, text: str) -> bool:
    """宽松匹配：多字实体名只要在文本中出现即可"""
    return name in text


def _extract_noun_entities(text: str) -> list:
    """
    从正文中提取疑似实体的名词短语。
    抽取规则：
    - 引用号内的内容（「」《》""''）
    - "把/从/到/在/和/的"后跟随的2-4字中文词
    - 以地点/组织后缀结尾的词
    """
    candidates = set()
    # 引号内的内容
    for m in re.finditer(r'[「《"\'][^」》"\']{2,8}[」》"\']', text):
        candidates.add(m.group()[1:-1])
    # 以地点后缀结尾的词
    for m in re.finditer(r'[\u4e00-\u9fff]{2,6}(?:巷|街|路|区|市|楼|厂|铺|场|院|社|所)', text):
        candidates.add(m.group())
    # 以组织后缀结尾的词
    for m in re.finditer(r'[\u4e00-\u9fff]{2,8}(?:公司|集团|协会|联盟|组织)', text):
        candidates.add(m.group())
    # 连续3-6字的中文名词（非句首，非人称代词）
    for m in re.finditer(r'(?<=[的把在被和与到对从给向关于])([\u4e00-\u9fff]{2,6})(?=[，。；：！？\s])', text):
        candidates.add(m.group(1))
    return list(candidates)


def _detect_status_changes(text: str) -> list:
    """
    检测正文中的状态变更关键词。
    返回 [(实体名, 新状态, 触发词), ...] 列表。
    """
    changes = []
    for trigger_word, new_status in STATUS_CHANGE_TRIGGERS.items():
        if trigger_word in text:
            # 尝试向前提取被作用的对象（触发词前最多8个字）
            pattern = rf'(.{{1,8}}){trigger_word}'
            for m in re.finditer(pattern, text):
                target = m.group(1).strip()
                # 去掉标点和常见介词
                target = re.sub(r'^[的把将被由从给向对与和了]', '', target)
                target = re.sub(r'[的，。；：！？、\s]+$', '', target)
                if target and len(target) >= 2 and len(target) <= 8:
                    changes.append((target, new_status, trigger_word))
    return changes


def _classify_type(name: str) -> str:
    """根据名称猜测实体类型"""
    if any(name.endswith(s) for s in LOCATION_SUFFIX):
        return "location"
    if any(name.endswith(s) for s in ORGANIZATION_SUFFIX):
        return "organization"
    if re.match(r'^[\d.]+%?$', name):
        return "data"
    return "object"


def extract(state_path: str, chapter: str, sub_key: str, content: str):
    """
    主入口：从子结构正文提取实体关系，增量合并到 entity_tracker。
    不阻断流程（POISON 级别输出仅为 INFO），但有冲突时输出 WARN。
    """
    sp = Path(state_path)
    if not sp.exists():
        print(f"[entity-extract] state_path 不存在: {state_path}")
        return

    data = json.loads(sp.read_text(encoding="utf-8-sig"))
    tracker = data.setdefault("entity_tracker", {"entities": [], "relations": []})
    existing_entities = tracker.get("entities", [])
    existing_relations = tracker.get("relations", [])
    known_chars = {c.get("name", "") for c in data.get("characters", [])}
    # ── 别名集：角色的别名也视为已知实体名，不重复创建 ──
    char_aliases = {}
    for c in data.get("characters", []):
        aliases = c.get("aliases", [])
        if isinstance(aliases, list):
            for a in aliases:
                known_chars.add(a)  # 别名加入已知名
                char_aliases[a] = c.get("name", "")  # 记录别名→真名映射
    known_entity_names = {e["name"] for e in existing_entities}
    known_entity_by_name = {e["name"]: e for e in existing_entities}

    new_count = 0
    conflict_count = 0
    relation_count = 0

    # ── 1. 检测状态变更 ──
    status_changes = _detect_status_changes(content)
    for target_name, new_status, trigger in status_changes:
        # 尝试匹配已有实体
        matched = False
        for e in existing_entities:
            if _entity_name_matches(e["name"], content) and e["name"] in target_name or target_name in e["name"]:
                old_status = e.get("attributes", {}).get("status", "active")
                if old_status != new_status:
                    # 回溯：看看是否已是该状态的实体
                    if new_status in STATUS_DEGRADING and new_status == old_status:
                        continue  # 已标记，不重复
                    e.setdefault("attributes", {})["status"] = new_status
                    e["last_chapter"] = chapter
                    e["last_sub"] = sub_key
                    print(f"  [entity-extract] [INFO] 实体状态变更: {e['name']}: {old_status}→{new_status} ({trigger})")
                    if new_status in STATUS_DEGRADING and old_status not in STATUS_DEGRADING:
                        print(f"    → 状态降级，后续章节使用该实体时需注意")
                    matched = True
                break
        if not matched:
            # 未匹配到已有实体 → 新建
            ent_type = _classify_type(target_name)
            eid = _make_entity_id(existing_entities)
            existing_entities.append({
                "id": eid,
                "type": ent_type,
                "name": target_name,
                "attributes": {"status": new_status},
                "first_chapter": chapter, "first_sub": sub_key,
                "last_chapter": chapter, "last_sub": sub_key
            })
            known_entity_names.add(target_name)
            known_entity_by_name[target_name] = existing_entities[-1]
            new_count += 1
            print(f"  [entity-extract] [INFO] 新实体: {eid} ({ent_type})「{target_name}」状态={new_status}")

    # ── 2. 提取新的实体名 ──
    candidates = _extract_noun_entities(content)
    for cand in candidates:
        if cand in known_entity_names or cand in known_chars:
            continue
        # 子串匹配（防包裹式命名重复）
        already_tracked = False
        for e in existing_entities:
            if cand in e["name"] or e["name"] in cand:
                already_tracked = True
                break
        if already_tracked:
            continue
        # 新建实体
        ent_type = _classify_type(cand)
        eid = _make_entity_id(existing_entities)
        existing_entities.append({
            "id": eid,
            "type": ent_type,
            "name": cand,
            "attributes": {},
            "first_chapter": chapter, "first_sub": sub_key,
            "last_chapter": chapter, "last_sub": sub_key
        })
        known_entity_names.add(cand)
        known_entity_by_name[cand] = existing_entities[-1]
        new_count += 1
        print(f"  [entity-extract] [INFO] 新实体: {eid} ({ent_type})「{cand}」")

    # ── 3. 更新已有实体的 last_chapter/last_sub（含别名匹配） ──
    for e in existing_entities:
        ename = e["name"]
        if ename in content:
            e["last_chapter"] = chapter
            e["last_sub"] = sub_key
        else:
            # 检查该实体的别名是否出现在内容中
            for c in data.get("characters", []):
                if c.get("name") == ename:
                    for alias in c.get("aliases", []):
                        if alias in content:
                            e["last_chapter"] = chapter
                            e["last_sub"] = sub_key
                            break
                    break

    # ── 4. 冲突检测：检查实体在本章被提及但状态不匹配 ──
    existing_entities_in_content = [e for e in existing_entities if e["name"] in content]
    for e in existing_entities_in_content:
        attr = e.get("attributes", {})
        status = attr.get("status", "")
        if status in STATUS_DEGRADING:
            # 实体是降级状态，但本章提及它时可能是正常使用的→看位置
            # 简单的启发式：如果正文同时包含"修复/重建"等恢复词，不算冲突
            recovery_words = ["修复", "重建", "修好", "重新", "恢复"]
            has_recovery = any(w in content for w in recovery_words)
            if not has_recovery and e["last_chapter"] != chapter:
                # 上次降级后未恢复，本次仍在用但不恢复—可能是矛盾
                print(f"  [entity-extract] [WARN] 实体状态矛盾: {e['name']}({e['id']}) 状态=「{status}」但本章仍在使用")
                conflict_count += 1

    # ── 5. 简单关系提取 ──
    for pattern, default_pred in REL_PATTERNS:
        for m in re.finditer(pattern, content):
            # 提取关系两端的实体名
            matched_entities = []
            for e in existing_entities:
                if e["name"] in m.group():
                    matched_entities.append(e)
            for char_name in known_chars:
                if char_name in m.group():
                    # 找到或创建一个角色实体
                    e = known_entity_by_name.get(char_name)
                    if not e:
                        eid = _make_entity_id(existing_entities)
                        e = {"id": eid, "type": "character", "name": char_name,
                             "attributes": {}, "first_chapter": chapter, "first_sub": sub_key,
                             "last_chapter": chapter, "last_sub": sub_key}
                        existing_entities.append(e)
                        known_entity_by_name[char_name] = e
                    if e not in matched_entities:
                        matched_entities.append(e)
            if len(matched_entities) >= 2:
                # 检查是否已有类似关系
                already_exists = False
                for r in existing_relations:
                    if (r.get("predicate") == default_pred and
                        any(re.search(re.escape(rm["name"]), content) for rm in matched_entities if rm["name"] in content)):
                        already_exists = True
                        break
                if not already_exists:
                    rid = _make_relation_id(existing_relations)
                    existing_relations.append({
                        "id": rid,
                        "from_entity": matched_entities[0]["id"],
                        "predicate": default_pred,
                        "to_entity": matched_entities[1]["id"] if len(matched_entities) > 1 else "",
                        "detail": m.group(),
                        "chapter": chapter, "sub": sub_key
                    })
                    relation_count += 1
                    print(f"  [entity-extract] [INFO] 新关系: {rid} {matched_entities[0]['name']}→{default_pred}→{matched_entities[1]['name'] if len(matched_entities) > 1 else '?'}")

    # ── 写入 entity_tracker ──
    tracker["entities"] = existing_entities
    tracker["relations"] = existing_relations
    data["entity_tracker"] = tracker
    sp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    # ── 总结 ──
    parts = []
    if new_count:
        parts.append(f"新增 {new_count} 实体")
    if relation_count:
        parts.append(f"新增 {relation_count} 关系")
    if conflict_count:
        parts.append(f"[WARN] {conflict_count} 个状态矛盾")
    if parts:
        print(f"  [entity-extract] 总结: {'; '.join(parts)}")
    else:
        print(f"  [entity-extract] [OK] 无新实体或变更")
    print(f"  [entity-extract] 当前: {len(existing_entities)} 实体, {len(existing_relations)} 关系")


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("用法: python novel_entity_extractor.py <state_path> <chapter> <sub_key> <content_file>")
        print("  content_file: 子结构内容文件路径（如 chapters/L01/S01.txt）")
        print("  或传 - 从 stdin 读取")
        sys.exit(1)

    state_path = sys.argv[1]
    chapter = sys.argv[2]
    sub_key = sys.argv[3]
    content_src = sys.argv[4]

    if content_src == "-":
        content = sys.stdin.read()
    else:
        content = Path(content_src).read_text(encoding="utf-8-sig")

    if not content.strip():
        print(f"[entity-extract] [WARN] 内容为空，跳过提取")
        sys.exit(0)

    extract(state_path, chapter, sub_key, content)
