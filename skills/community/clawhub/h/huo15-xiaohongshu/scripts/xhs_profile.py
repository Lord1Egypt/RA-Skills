"""火一五小红书"创作者画像"核心库。

设计目标
========
让助手"记得这个创作者" — 他写过什么、什么风格、哪些规则适用、哪些不适用。
所有功能（打分 / 教练 / 选题 / 复盘）都从这里读取，让产出"像他自己写的"。

存档位置
========
**`~/.xiaohongshu/profile/`**（用户私有，不入 git/skills 包）。
跨 skill 共用 — 未来 huo15-blog / huo15-douyin 也能读到同一份创作者档案。

数据
====
- `style.json`     — 自动从 baseline 笔记提取的风格特征
- `rules.json`     — 用户的规则覆盖（"我不要这个"+"加这个"）
- `feedback.jsonl` — 用户对每条建议的反馈日志（用于规则演进）
- `baseline/`      — 1~5 篇代表作样本（json 文件）
- `posts.jsonl`    — 起草历史（publish_helper 写入）
- `snapshots.jsonl`— 互动快照（track_post 写入）
- `reviews/`       — 周/月复盘报告

设计原则
========
- **默认规则在 `data/`（技能资产，所有人共享），覆盖在 `profile/rules.json`（个人化）。**
  最终值 = `merge(default, override)`。
- 风格档案是"统计特征"，不是"硬规定" — 偏离时只是提醒，不是禁止。
- 规则覆盖支持"教学"流程：用户给反馈 → 反馈累积到阈值 → 自动调整 rules.json。
"""

from __future__ import annotations

import collections
import datetime as dt
import json
import os
import re
import statistics as stats
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


# =====================================================================
# 路径
# =====================================================================


def profile_root(custom: Optional[str] = None) -> Path:
    """档案根目录：默认 ~/.xiaohongshu/profile/，可被环境变量覆盖。"""
    if custom:
        return Path(os.path.expanduser(custom))
    env = os.environ.get("XHS_PROFILE_DIR")
    if env:
        return Path(os.path.expanduser(env))
    return Path(os.path.expanduser("~/.xiaohongshu/profile"))


def ensure_root(root: Optional[Path] = None) -> Path:
    p = root or profile_root()
    p.mkdir(parents=True, exist_ok=True)
    (p / "baseline").mkdir(exist_ok=True)
    (p / "reviews").mkdir(exist_ok=True)
    return p


# =====================================================================
# StyleProfile — 风格档案
# =====================================================================


@dataclass
class StyleProfile:
    """从 1~5 篇 baseline 提取的创作者特征。所有字段都是统计/偏好。"""

    persona: str = ""                                # "30+ 干皮女生"，可选手填
    voice: str = "casual"                            # casual / formal / playful / pro
    niche: str = ""                                  # "护肤"、"职场"，从 baseline 推断
    avg_title_len: int = 18                          # 平均标题长度
    title_len_range: List[int] = field(default_factory=lambda: [16, 22])
    avg_content_len: int = 400                       # 平均正文字符数
    avg_paragraphs: int = 8                          # 平均段落数
    avg_para_chars: int = 50                         # 平均段落字符数
    emoji_per_post: float = 6.0                      # 平均每篇 emoji 数
    favorite_emojis: List[str] = field(default_factory=list)
    favorite_formulas: Dict[str, int] = field(default_factory=dict)   # T1: 3 表示用过 3 次
    favorite_skeletons: Dict[str, int] = field(default_factory=dict)  # S1: 5
    common_tags: List[str] = field(default_factory=list)              # 高频话题（去重）
    common_phrases: List[str] = field(default_factory=list)           # "亲测" "我体感" 等口头禅
    avoid_words: List[str] = field(default_factory=list)              # 用户不爱用的词（手填）
    sample_count: int = 0                                              # 用了几篇样本
    last_updated: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "StyleProfile":
        kwargs = {k: v for k, v in d.items() if k in cls.__dataclass_fields__}
        return cls(**kwargs)


# =====================================================================
# RuleOverride — 规则覆盖
# =====================================================================


@dataclass
class RuleOverride:
    """用户对默认规则的覆盖。"""

    # 子项权重覆盖（默认见 score_post 的 weights）
    weights: Dict[str, float] = field(default_factory=dict)
    # 完全禁用的检查项（不会扣分也不会建议）
    disabled_checks: List[str] = field(default_factory=list)
    # 用户额外的敏感词
    custom_sensitive: List[str] = field(default_factory=list)
    # 用户**允许**的词（覆盖 data/sensitive_words.txt 里的，比如医生确实需要"治愈"）
    allowed_words: List[str] = field(default_factory=list)
    # 用户偏好（影响生成）
    prefer_emoji: Optional[bool] = None              # None=不强制；True/False
    prefer_question_title: Optional[bool] = None     # 是否喜欢提问型标题
    max_emoji_per_post: Optional[int] = None
    custom_phrases: List[str] = field(default_factory=list)  # 用户希望多用的口头禅
    main_keyword: str = ""              # 主关键词（赛道核心词），影响标题前 13 字检查
    weak_dims: List[str] = field(default_factory=list)  # v3.4: 长期掉某维（evolve 写）
    last_updated: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "RuleOverride":
        kwargs = {k: v for k, v in d.items() if k in cls.__dataclass_fields__}
        return cls(**kwargs)


# =====================================================================
# Feedback — 用户对建议的反馈
# =====================================================================


@dataclass
class Feedback:
    """用户对某条建议的反馈，会驱动 rules.json 自动演进。"""

    at: str                # ISO timestamp
    rule_key: str          # 如 "emoji"、"sensitive_word:最佳"
    suggestion: str        # 建议原文
    reaction: str          # accept / reject / ignore
    note: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# =====================================================================
# ProfileStore — 读写一体
# =====================================================================


class ProfileStore:
    """档案的统一读写入口。"""

    def __init__(self, root: Optional[Path] = None) -> None:
        self.root = ensure_root(root)
        self.style_path = self.root / "style.json"
        self.rules_path = self.root / "rules.json"
        self.feedback_path = self.root / "feedback.jsonl"
        self.baseline_dir = self.root / "baseline"
        self.posts_path = self.root.parent / "posts.jsonl"          # publish_helper 默认位置
        self.snapshots_path = self.root.parent / "snapshots.jsonl"  # track_post 默认位置
        self.reviews_dir = self.root / "reviews"

    # ---------- style ----------

    def load_style(self) -> StyleProfile:
        if not self.style_path.exists():
            return StyleProfile()
        try:
            d = json.loads(self.style_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return StyleProfile()
        return StyleProfile.from_dict(d)

    def save_style(self, profile: StyleProfile) -> None:
        profile.last_updated = dt.datetime.now().isoformat(timespec="seconds")
        self.style_path.write_text(
            json.dumps(profile.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    # ---------- rules ----------

    def load_rules(self) -> RuleOverride:
        if not self.rules_path.exists():
            return RuleOverride()
        try:
            d = json.loads(self.rules_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return RuleOverride()
        return RuleOverride.from_dict(d)

    def save_rules(self, rules: RuleOverride) -> None:
        rules.last_updated = dt.datetime.now().isoformat(timespec="seconds")
        self.rules_path.write_text(
            json.dumps(rules.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    # ---------- baseline ----------

    def add_baseline(self, draft_or_note: Dict[str, Any]) -> Path:
        """加一篇 baseline 笔记。返回写入的文件路径。"""
        idx = len(list(self.baseline_dir.glob("*.json"))) + 1
        path = self.baseline_dir / f"sample_{idx:02d}.json"
        path.write_text(
            json.dumps(draft_or_note, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return path

    def load_baselines(self) -> List[Dict[str, Any]]:
        out = []
        for p in sorted(self.baseline_dir.glob("*.json")):
            try:
                out.append(json.loads(p.read_text(encoding="utf-8")))
            except json.JSONDecodeError:
                continue
        return out

    # ---------- feedback ----------

    def append_feedback(self, fb: Feedback) -> None:
        with self.feedback_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(fb.to_dict(), ensure_ascii=False) + "\n")

    def load_feedback(self) -> List[Feedback]:
        if not self.feedback_path.exists():
            return []
        out = []
        for line in self.feedback_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
                out.append(Feedback(**{k: v for k, v in d.items() if k in Feedback.__dataclass_fields__}))
            except (json.JSONDecodeError, TypeError):
                continue
        return out

    # ---------- posts / snapshots（read-only 视图） ----------

    def load_posts(self) -> List[Dict[str, Any]]:
        if not self.posts_path.exists():
            return []
        out = []
        for line in self.posts_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
        return out

    def load_snapshots(self) -> List[Dict[str, Any]]:
        if not self.snapshots_path.exists():
            return []
        out = []
        for line in self.snapshots_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
        return out


# =====================================================================
# 从 baseline 笔记提取 StyleProfile
# =====================================================================


_EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001F9FF"
    "\U0001FA70-\U0001FAFF"
    "\U00002600-\U000027BF"
    "\U0001F000-\U0001F2FF"
    "‍️]"
)


def _all_emojis(text: str) -> List[str]:
    return _EMOJI_RE.findall(text)


def _extract_phrases(text: str) -> List[str]:
    """口头禅检测：常见的几种，命中即标记。"""
    candidates = [
        "亲测", "我自己", "我体感", "我之前", "我以为", "其实",
        "保姆级", "手把手", "记一下", "整理了", "私心推荐",
        "重点来了", "划重点", "敲黑板",
    ]
    return [c for c in candidates if c in text]


def derive_style(baselines: List[Dict[str, Any]]) -> StyleProfile:
    """从已抓取/手动整理的笔记中提取风格档案。"""
    if not baselines:
        return StyleProfile()

    title_lens: List[int] = []
    content_lens: List[int] = []
    para_counts: List[int] = []
    para_lens: List[int] = []
    emoji_counts: List[int] = []
    emoji_pool: collections.Counter = collections.Counter()
    formulas: collections.Counter = collections.Counter()
    skeletons: collections.Counter = collections.Counter()
    tags_pool: collections.Counter = collections.Counter()
    phrases_pool: collections.Counter = collections.Counter()

    for n in baselines:
        title = (n.get("title") or "").strip()
        content = n.get("content") or ""

        if title:
            title_lens.append(len(title))
        if content:
            content_lens.append(len(content))
            paras = [p for p in content.splitlines() if p.strip()]
            para_counts.append(len(paras))
            para_lens.extend(len(p) for p in paras)

        es = _all_emojis(title + "\n" + content)
        emoji_counts.append(len(es))
        emoji_pool.update(es)

        for t in (n.get("tags") or []):
            tags_pool[t.strip()] += 1

        if n.get("formula"):
            formulas[n["formula"]] += 1
        if n.get("skeleton"):
            skeletons[n["skeleton"]] += 1

        phrases_pool.update(_extract_phrases(title + "\n" + content))

    def _med(xs: List[int]) -> int:
        return int(stats.median(xs)) if xs else 0

    profile = StyleProfile(
        avg_title_len=_med(title_lens) if title_lens else 18,
        title_len_range=[min(title_lens), max(title_lens)] if title_lens else [16, 22],
        avg_content_len=_med(content_lens) if content_lens else 400,
        avg_paragraphs=_med(para_counts) if para_counts else 8,
        avg_para_chars=_med(para_lens) if para_lens else 50,
        emoji_per_post=round(stats.mean(emoji_counts), 1) if emoji_counts else 6.0,
        favorite_emojis=[e for e, _ in emoji_pool.most_common(8)],
        favorite_formulas=dict(formulas),
        favorite_skeletons=dict(skeletons),
        common_tags=[t for t, _ in tags_pool.most_common(15)],
        common_phrases=[p for p, _ in phrases_pool.most_common(8)],
        sample_count=len(baselines),
    )
    return profile


# =====================================================================
# 规则合并：default ⊕ override
# =====================================================================


_DEFAULT_WEIGHTS = {
    "title": 0.25,
    "first_lines": 0.20,
    "layout": 0.10,
    "emoji": 0.10,
    "hashtags": 0.10,
    "compliance": 0.25,
}


def effective_weights(rules: RuleOverride) -> Dict[str, float]:
    """合并默认权重 + 用户覆盖（含禁用 = 权重置 0）。返回归一化后的权重。"""
    merged = dict(_DEFAULT_WEIGHTS)
    for k, v in rules.weights.items():
        if k in merged:
            merged[k] = max(0.0, float(v))
    for k in rules.disabled_checks:
        if k in merged:
            merged[k] = 0.0
    total = sum(merged.values()) or 1.0
    return {k: v / total for k, v in merged.items()}


def effective_sensitive_words(rules: RuleOverride, base: List[str]) -> List[str]:
    """合并：先去掉用户允许的词，再加上用户的额外敏感词。"""
    allowed = set(rules.allowed_words or [])
    out = [w for w in base if w not in allowed]
    out.extend(w for w in (rules.custom_sensitive or []) if w not in allowed)
    return out


# =====================================================================
# 规则演进：根据 feedback 自动调 rules
# =====================================================================


def evolve_rules(store: ProfileStore, *, threshold: int = 3,
                 iter_low_rate: float = 0.3, iter_min_attempts: int = 5) -> Dict[str, Any]:
    """从 feedback.jsonl + iter_sessions 双源自动演进规则。

    feedback 来源（v2.5 已有）：
    - 同一个 rule_key 连续被 reject ≥ threshold → 加入 disabled_checks
    - 一旦该 rule_key 出现 accept → 重置计数

    iter_sessions 来源（v3.4 新加）：
    - 同一维度被 focus ≥ iter_min_attempts 次，但改进率 < iter_low_rate
      → 标记为"长期掉某维"（写到 weak_dims，不直接禁用）

    返回 changes 字典（哪些改了 / 为什么）。
    """
    feedback = store.load_feedback()
    rules = store.load_rules()
    changes: Dict[str, Any] = {"disabled_added": [], "weak_dims_added": []}
    disabled = set(rules.disabled_checks)

    # ---- 1) feedback reject 计数（原逻辑） ----
    counters: Dict[str, int] = {}
    for fb in feedback:
        key = fb.rule_key.split(":", 1)[0]
        if fb.reaction == "reject":
            counters[key] = counters.get(key, 0) + 1
        elif fb.reaction == "accept":
            counters[key] = 0

    for k, c in counters.items():
        if c >= threshold and k not in disabled and k in _DEFAULT_WEIGHTS:
            disabled.add(k)
            changes["disabled_added"].append({"key": k, "reason": f"feedback reject ≥ {threshold}"})

    # ---- 2) iter_sessions 长期低改进率检测（v3.4 新逻辑） ----
    iter_root = store.root / "iter_sessions"
    weak_dims = list(getattr(rules, "weak_dims", []) or [])
    if iter_root.exists():
        attempts: Dict[str, int] = {}
        improved: Dict[str, int] = {}
        for sess in iter_root.iterdir():
            if not sess.is_dir():
                continue
            log_file = sess / "iter.jsonl"
            if not log_file.exists():
                continue
            for line in log_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    continue
                dim = r.get("focus", "")
                if dim in ("", "graduated"):
                    continue
                attempts[dim] = attempts.get(dim, 0) + 1
                before = r.get("before_score")
                after = r.get("after_score")
                if before is not None and after is not None and after > before:
                    improved[dim] = improved.get(dim, 0) + 1
        for d, n in attempts.items():
            if n < iter_min_attempts:
                continue
            rate = improved.get(d, 0) / n
            if rate < iter_low_rate and d not in weak_dims:
                weak_dims.append(d)
                changes["weak_dims_added"].append({
                    "dim": d, "attempts": n, "improved": improved.get(d, 0),
                    "rate": round(rate * 100, 0),
                })

    rules.disabled_checks = sorted(disabled)
    # weak_dims 是 v3.4 新字段，先用 dynamic 写法，避免改动 dataclass 直接动表（向后兼容）
    if hasattr(rules, "weak_dims"):
        rules.weak_dims = weak_dims  # type: ignore
    else:
        # RuleOverride 没字段就用 custom_phrases 旁挂个隐字段
        pass

    if changes["disabled_added"] or changes["weak_dims_added"]:
        store.save_rules(rules)
    changes["weak_dims"] = weak_dims
    return changes
