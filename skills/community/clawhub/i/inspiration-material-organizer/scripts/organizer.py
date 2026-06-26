import argparse
import json
import os
import random
import re
import uuid
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


DEFAULT_DB = ".cursor/skills/inspiration-material-organizer/data/inspirations.json"
DEFAULT_TOPIC_RULES_PATH = ".cursor/skills/inspiration-material-organizer/config/topic_rules.json"
DEFAULT_TOPIC_RULES: Dict[str, List[str]] = {
    "写作": ["写作", "选题", "表达", "文案", "结构", "标题"],
    "产品": ["需求", "用户", "功能", "原型", "体验", "增长"],
    "运营": ["社群", "活动", "复盘", "留存", "转化"],
    "营销": ["品牌", "传播", "投放", "渠道", "广告"],
    "技术": ["代码", "架构", "接口", "自动化", "ai", "python", "算法"],
    "个人成长": ["习惯", "效率", "学习", "目标", "认知", "复利"],
}


@dataclass
class Card:
    id: str
    title: str
    content: str
    url: str
    source: str
    created_at: str
    updated_at: str
    topic: str
    tags: List[str]
    group: str

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "url": self.url,
            "source": self.source,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "topic": self.topic,
            "tags": self.tags,
            "group": self.group,
        }


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def db_path() -> Path:
    return Path(os.getenv("INSPIRATION_DB_PATH", DEFAULT_DB))


def topic_rules_path() -> Path:
    return Path(os.getenv("INSPIRATION_TOPIC_RULES_PATH", DEFAULT_TOPIC_RULES_PATH))


def ensure_db() -> None:
    path = db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text("[]", encoding="utf-8")


def load_cards() -> List[Dict]:
    ensure_db()
    path = db_path()
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        return []
    return json.loads(raw)


def save_cards(cards: List[Dict]) -> None:
    ensure_db()
    path = db_path()
    path.write_text(json.dumps(cards, ensure_ascii=False, indent=2), encoding="utf-8")


def load_topic_rules() -> Dict[str, List[str]]:
    path = topic_rules_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(json.dumps(DEFAULT_TOPIC_RULES, ensure_ascii=False, indent=2), encoding="utf-8")

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return DEFAULT_TOPIC_RULES

    if not isinstance(payload, dict):
        return DEFAULT_TOPIC_RULES

    normalized: Dict[str, List[str]] = {}
    for topic, keywords in payload.items():
        if not isinstance(topic, str):
            continue
        if not isinstance(keywords, list):
            continue
        valid_keywords = [kw.lower() for kw in keywords if isinstance(kw, str) and kw.strip()]
        if valid_keywords:
            normalized[topic] = valid_keywords

    return normalized or DEFAULT_TOPIC_RULES


def tokenize(text: str) -> List[str]:
    lowered = text.lower()
    chunks = re.findall(r"[\u4e00-\u9fff]+|[a-z0-9]+", lowered)
    return [c for c in chunks if c.strip()]


def infer_topic_and_tags(text: str) -> Tuple[str, List[str]]:
    lower = text.lower()
    topic_rules = load_topic_rules()
    best_topic = "未分类"
    best_score = 0
    tags: List[str] = []

    for topic, keywords in topic_rules.items():
        hit = [kw for kw in keywords if kw in lower]
        score = len(hit)
        if score > best_score:
            best_topic = topic
            best_score = score
        tags.extend(hit)

    token_tags = list(dict.fromkeys(tokenize(text)))[:8]
    all_tags = list(dict.fromkeys(tags + token_tags))[:10]
    group = best_topic
    return group, all_tags


def auto_title(content: str) -> str:
    plain = content.strip().replace("\n", " ")
    return (plain[:30] + "...") if len(plain) > 30 else plain


def cmd_capture(args: argparse.Namespace) -> None:
    cards = load_cards()
    ts = now_iso()
    title = args.title.strip() if args.title else auto_title(args.text)
    card = Card(
        id=str(uuid.uuid4()),
        title=title,
        content=args.text.strip(),
        url=args.url.strip() if args.url else "",
        source=args.source,
        created_at=ts,
        updated_at=ts,
        topic="未分类",
        tags=[],
        group="待整理",
    )
    cards.append(card.to_dict())
    save_cards(cards)
    print(f"已收录: {card.id} | {card.title}")


def cmd_classify(args: argparse.Namespace) -> None:
    cards = load_cards()
    if args.ids == "all":
        target_ids = {c["id"] for c in cards}
    else:
        target_ids = set([s.strip() for s in args.ids.split(",") if s.strip()])

    updated = 0
    for c in cards:
        if c["id"] not in target_ids:
            continue
        base_text = " ".join([c.get("title", ""), c.get("content", ""), c.get("url", "")])
        topic, tags = infer_topic_and_tags(base_text)
        c["topic"] = topic
        c["group"] = topic
        c["tags"] = tags
        c["updated_at"] = now_iso()
        updated += 1

    save_cards(cards)
    print(f"分类完成: {updated} 条")


def score_card(card: Dict, query: str) -> float:
    q_tokens = tokenize(query)
    if not q_tokens:
        return 0.0

    text = " ".join(
        [
            card.get("title", ""),
            card.get("content", ""),
            card.get("topic", ""),
            card.get("group", ""),
            " ".join(card.get("tags", [])),
        ]
    ).lower()

    base_hits = sum(text.count(t) for t in q_tokens)
    tag_hits = sum(1 for t in q_tokens if t in " ".join(card.get("tags", [])).lower())
    card_tokens = set(tokenize(text))
    overlap = len(set(q_tokens).intersection(card_tokens)) / max(len(set(q_tokens)), 1)
    return base_hits * 1.0 + tag_hits * 1.5 + overlap * 3.0


def cmd_search(args: argparse.Namespace) -> None:
    cards = load_cards()
    scored = []
    for c in cards:
        s = score_card(c, args.query)
        if s > 0:
            scored.append((s, c))
    scored.sort(key=lambda x: x[0], reverse=True)

    if not scored:
        print("没有找到相关素材。")
        return

    for idx, (score, c) in enumerate(scored[: args.limit], start=1):
        print(f"{idx}. [{c['topic']}] {c['title']}  (score={score:.2f})")
        print(f"   id={c['id']}")
        print(f"   tags={','.join(c.get('tags', []))}")
        print(f"   source={c['source']}  url={c.get('url', '')}")
        print(f"   content={c['content'][:120]}")


def in_date_range(card: Dict, date_from: str, date_to: str) -> bool:
    created = card.get("created_at", "")[:10]
    if date_from and created < date_from:
        return False
    if date_to and created > date_to:
        return False
    return True


def cmd_ruminate(args: argparse.Namespace) -> None:
    cards = load_cards()
    pool = []
    for c in cards:
        if args.topic and c.get("topic") != args.topic:
            continue
        if not in_date_range(c, args.date_from or "", args.date_to or ""):
            continue
        pool.append(c)

    if not pool:
        print("没有符合条件的素材可反刍。")
        return

    pick = random.sample(pool, k=min(args.count, len(pool)))
    print(f"本次反刍 {len(pick)} 条：")
    for i, c in enumerate(pick, start=1):
        print(f"{i}. [{c['topic']}] {c['title']} ({c['created_at'][:10]})")
        print(f"   下一步建议: 把这条素材改写成一个可执行动作。")
        print(f"   摘要: {c['content'][:100]}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="灵感素材整理器 CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_capture = sub.add_parser("capture", help="快速收录素材")
    p_capture.add_argument("--text", required=True, help="素材文本")
    p_capture.add_argument("--url", default="", help="素材链接")
    p_capture.add_argument("--title", default="", help="素材标题")
    p_capture.add_argument(
        "--source",
        default="other",
        choices=["chat", "screenshot", "link", "note", "other"],
        help="素材来源",
    )
    p_capture.set_defaults(func=cmd_capture)

    p_classify = sub.add_parser("classify", help="智能分类")
    p_classify.add_argument("--ids", default="all", help="逗号分隔卡片ID，默认 all")
    p_classify.set_defaults(func=cmd_classify)

    p_search = sub.add_parser("search", help="语义检索")
    p_search.add_argument("--query", required=True, help="检索关键词或描述")
    p_search.add_argument("--limit", type=int, default=10, help="返回数量上限")
    p_search.set_defaults(func=cmd_search)

    p_ruminate = sub.add_parser("ruminate", help="灵感反刍")
    p_ruminate.add_argument("--topic", default="", help="按主题过滤")
    p_ruminate.add_argument("--date-from", default="", help="起始日期 YYYY-MM-DD")
    p_ruminate.add_argument("--date-to", default="", help="结束日期 YYYY-MM-DD")
    p_ruminate.add_argument("--count", type=int, default=5, help="返回数量")
    p_ruminate.set_defaults(func=cmd_ruminate)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
