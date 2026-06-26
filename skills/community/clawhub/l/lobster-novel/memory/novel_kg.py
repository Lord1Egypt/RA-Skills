#!/usr/bin/env python3
"""
lobster-novel: Novel Knowledge Graph — auto-extraction from chapter text.
Inspired by 马良写作 知识图谱 system.

Maintains a JSONL graph of entities (characters, items, locations, events)
and their relationships, extracted from chapter text.

Format: JSONL with 'op' operations:
  {"op": "upsert", "id": "...", "type": "character", "label": "...", "props": {}}
  {"op": "relate", "from": "...", "rel": "...", "to": "...", "chapter": 1}
"""
import re, json
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from collections import defaultdict


@dataclass
class KGEntity:
    id: str
    type: str  # character / location / item / event / concept
    label: str
    properties: Dict = field(default_factory=dict)
    first_seen: int = 0
    last_seen: int = 0


@dataclass
class KGRelation:
    source: str
    target: str
    relation: str
    chapter: int = 0
    context: str = ""


class NovelKG:
    """Lightweight novel knowledge graph using JSONL format.
    Two files: entities.jsonl + relations.jsonl for easy querying.
    """

    def __init__(self, project_dir: Path):
        self.dir = Path(project_dir) / "knowledge_graph"
        self.dir.mkdir(parents=True, exist_ok=True)
        self.entities_file = self.dir / "entities.jsonl"
        self.relations_file = self.dir / "relations.jsonl"
        self._entities: Dict[str, KGEntity] = {}
        self._relations: List[KGRelation] = []
        self._load()

    def _load(self):
        if self.entities_file.exists():
            for line in self.entities_file.read_text().strip().split("\n"):
                if line:
                    d = json.loads(line)
                    self._entities[d["id"]] = KGEntity(**d)
        if self.relations_file.exists():
            for line in self.relations_file.read_text().strip().split("\n"):
                if line:
                    d = json.loads(line)
                    self._relations.append(KGRelation(**d))

    def save(self):
        with open(self.entities_file, "w", encoding="utf-8") as f:
            for e in self._entities.values():
                f.write(json.dumps({
                    "id": e.id, "type": e.type, "label": e.label,
                    "properties": e.properties,
                    "first_seen": e.first_seen, "last_seen": e.last_seen,
                }, ensure_ascii=False) + "\n")
        with open(self.relations_file, "w", encoding="utf-8") as f:
            for r in self._relations:
                f.write(json.dumps({
                    "source": r.source, "target": r.target,
                    "relation": r.relation, "chapter": r.chapter,
                    "context": r.context[:100],
                }, ensure_ascii=False) + "\n")

    def upsert_entity(self, eid: str, etype: str, label: str,
                       props: Dict = None, chapter: int = 0):
        if eid in self._entities:
            ent = self._entities[eid]
            ent.last_seen = max(ent.last_seen, chapter)
            if props:
                ent.properties.update(props)
        else:
            self._entities[eid] = KGEntity(
                id=eid, type=etype, label=label,
                properties=props or {},
                first_seen=chapter, last_seen=chapter,
            )

    def add_relation(self, source: str, target: str, relation: str,
                      chapter: int = 0, context: str = ""):
        self._relations.append(KGRelation(
            source=source, target=target, relation=relation,
            chapter=chapter, context=context[:100],
        ))

    def query_entity(self, eid: str) -> Optional[KGEntity]:
        return self._entities.get(eid)

    def query_relations(self, entity_id: str) -> List[KGRelation]:
        return [r for r in self._relations
                if r.source == entity_id or r.target == entity_id]

    def get_contradictions(self) -> List[str]:
        """Find potential contradictions in the KG."""
        issues = []
        # Character in two places at same time
        char_locations = defaultdict(list)
        for r in self._relations:
            if r.relation == "at":
                char_locations[r.source].append((r.target, r.chapter))
        for char, locs in char_locations.items():
            prev_loc, prev_ch = "", 0
            for loc, ch in locs:
                if prev_loc and prev_loc != loc and ch == prev_ch:
                    issues.append(f"'{char}' at both '{prev_loc}' and '{loc}' in ch{ch}")
                prev_loc, prev_ch = loc, ch
        return issues

    def summary(self) -> str:
        by_type = defaultdict(int)
        for e in self._entities.values():
            by_type[e.type] += 1
        lines = [
            f"Knowledge Graph Summary:",
            f"  Entities: {len(self._entities)} | Relations: {len(self._relations)}",
        ]
        for t, c in sorted(by_type.items()):
            lines.append(f"    {t}: {c}")
        contradict = self.get_contradictions()
        if contradict:
            lines.append(f"  ⚠️ {len(contradict)} potential contradictions")
        return "\n".join(lines)

    # ── Auto-extraction from text ─────────────────────────────

    def extract_from_chapter(self, text: str, chapter: int) -> int:
        """Auto-extract entities and relations from chapter text.
        Returns count of new relations added.
        """
        count = 0

        # Extract character names from bible (pre-registered)
        from bible import BibleManager
        bm = BibleManager(self.dir.parent)
        for name, char in bm.bible.characters.items():
            if name in text:
                self.upsert_entity(
                    f"char_{name}", "character", name,
                    {"role": char.role}, chapter)

        # Extract location names (capitalized or repeated mention)
        location_candidates = re.findall(
            r'(?:在|到|去|往|从|位于)([\u4e00-\u9fff]{2,6}(?:城|镇|村|山|河|海|湖|宫|殿|府|楼|塔|谷|林|原|岛|国|域|界|大陆))', text)
        for loc in set(location_candidates):
            eid = f"loc_{loc}"
            self.upsert_entity(eid, "location", loc, chapter=chapter)
            # Find which characters are at this location
            for name, char in bm.bible.characters.items():
                if name in text and name in text[:text.find(loc) + 100]:
                    self.add_relation(f"char_{name}", eid, "at",
                                      chapter=chapter,
                                      context=text[text.find(loc):text.find(loc) + 40])
                    count += 1

        # Extract item ownership
        item_pattern = re.findall(
            r'([\u4e00-\u9fff]{2,4})的([\u4e00-\u9fff]{2,4}(?:剑|刀|枪|棍|棒|书|笔|戒|链|玉|珠|瓶|鼎|钟|琴|图|令|符|石))', text)
        for owner, item in set(item_pattern):
            item_id = f"item_{item}"
            owner_id = f"char_{owner}" if owner in bm.bible.characters else f"entity_{owner}"
            self.upsert_entity(item_id, "item", item, chapter=chapter)
            self.upsert_entity(owner_id, "character", owner, chapter=chapter)
            self.add_relation(owner_id, item_id, "owns", chapter=chapter)
            count += 1

        # Relation extraction: "X[verb]Y"
        relation_verbs = [
            (r'([\u4e00-\u9fff]{2,4})是([\u4e00-\u9fff]{2,4})的(父亲|母亲|兄弟|姐妹|儿子|女儿|朋友|敌人|徒弟|师父|师兄|师姐|师弟|师妹)', "family"),
            (r'([\u4e00-\u9fff]{2,4})爱[上]?了?([\u4e00-\u9fff]{2,4})', "loves"),
            (r'([\u4e00-\u9fff]{2,4})恨([\u4e00-\u9fff]{2,4})', "hates"),
            (r'([\u4e00-\u9fff]{2,4})帮[助]?([\u4e00-\u9fff]{2,4})', "helps"),
            (r'([\u4e00-\u9fff]{2,4})杀[死]?了?([\u4e00-\u9fff]{2,4})', "kills"),
            (r'([\u4e00-\u9fff]{2,4})打[败]?([\u4e00-\u9fff]{2,4})', "defeats"),
        ]
        for pat, rel in relation_verbs:
            matches = re.findall(pat, text)
            for sub, obj in set(matches):
                sub_id = f"char_{sub}" if sub in bm.bible.characters else f"entity_{sub}"
                obj_id = f"char_{obj}" if obj in bm.bible.characters else f"entity_{obj}"
                self.upsert_entity(sub_id, "character", sub, chapter=chapter)
                self.upsert_entity(obj_id, "character", obj, chapter=chapter)
                self.add_relation(sub_id, obj_id, rel, chapter=chapter,
                                  context=f"{sub}{rel}{obj}")
                count += 1

        self.save()
        return count


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="novel knowledge graph")
    parser.add_argument("--dir", default="./my-novel")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status", help="show KG summary")
    p_extract = sub.add_parser("extract", help="extract from chapter file")
    p_extract.add_argument("chapter", type=int)
    p_extract.add_argument("file", help="chapter md file")

    args = parser.parse_args()
    kg = NovelKG(Path(args.dir))

    if args.cmd == "status":
        print(kg.summary())
        contradicts = kg.get_contradictions()
        if contradicts:
            print("\n⚠️ Contradictions:")
            for c in contradicts:
                print(f"  - {c}")
    elif args.cmd == "extract":
        text = Path(args.file).read_text(encoding="utf-8")
        count = kg.extract_from_chapter(text, args.chapter)
        print(f"Extracted {count} relations from ch{args.chapter}")
        print(kg.summary())
