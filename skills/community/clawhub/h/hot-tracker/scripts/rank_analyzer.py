#!/usr/bin/env python3
"""Cross-platform hot-topic analyzer with noise reduction and neutral ranking."""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


SUPPORTED_PLATFORMS = ["wx", "xhs", "dy", "weibo", "zhihu", "bilibili", "kuaishou"]

PLATFORM_QUALITY = {
    "wx": 1.00,
    "xhs": 0.95,
    "dy": 0.95,
    "weibo": 0.95,
    "zhihu": 0.90,
    "bilibili": 0.90,
    "kuaishou": 0.88,
}

PLATFORM_LABELS = {
    "wx": "微信公众号",
    "xhs": "小红书",
    "dy": "抖音",
    "weibo": "微博",
    "zhihu": "知乎",
    "bilibili": "B站",
    "kuaishou": "快手",
}

STOPWORDS = {
    "热搜",
    "热点",
    "热榜",
    "最新",
    "今天",
    "今日",
    "刚刚",
    "视频",
    "话题",
    "网友",
    "内容",
    "平台",
    "事件",
    "最新消息",
}

PROMO_KEYWORDS = {
    "抽奖",
    "福利",
    "领券",
    "优惠",
    "促销",
    "返利",
    "私信",
    "加微",
    "加vx",
    "进群",
    "合作",
    "招商",
    "代理",
    "带货",
    "购买",
}

LOW_INFO_KEYWORDS = {
    "笑死",
    "绝了",
    "绷不住",
    "震惊",
    "速看",
    "快看",
    "太离谱了",
}

ABSOLUTE_WORDS = {
    "最强",
    "第一",
    "绝对",
    "一定",
    "无敌",
    "顶级",
    "封神",
}


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def safe_float(value: Any) -> float:
    try:
        if value is None:
            return 0.0
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def now_local() -> datetime:
    return datetime.now().astimezone()


def percentile_scores(values: Sequence[float]) -> List[float]:
    if not values:
        return []
    if len(values) == 1:
        return [1.0]

    indexed = sorted(enumerate(values), key=lambda pair: pair[1])
    scores = [0.0] * len(values)
    start = 0

    while start < len(indexed):
        end = start
        while end + 1 < len(indexed) and indexed[end + 1][1] == indexed[start][1]:
            end += 1
        avg_rank = (start + end) / 2
        score = avg_rank / (len(indexed) - 1)
        for i in range(start, end + 1):
            scores[indexed[i][0]] = score
        start = end + 1

    return scores


def normalize_title(title: str) -> str:
    text = (title or "").strip().lower()
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"#[^#]+#", " ", text)
    text = re.sub(r"[@#【】\[\]\(\)\{\}\-_=+|\\/:;,.!?！？，。、“”‘’·~`]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_tokens(text: str) -> List[str]:
    normalized = normalize_title(text)
    tokens: List[str] = []

    for token in re.findall(r"[a-z0-9]+|[\u4e00-\u9fff]{2,}", normalized):
        if token in STOPWORDS:
            continue
        if re.fullmatch(r"[\u4e00-\u9fff]{2,}", token):
            tokens.append(token)
            if len(token) > 4:
                tokens.extend(token[i : i + 2] for i in range(len(token) - 1))
        else:
            tokens.append(token)

    return [token for token in tokens if token and token not in STOPWORDS]


def jaccard_similarity(left: Iterable[str], right: Iterable[str]) -> float:
    left_set = set(left)
    right_set = set(right)
    if not left_set or not right_set:
        return 0.0
    inter = len(left_set & right_set)
    union = len(left_set | right_set)
    return inter / union if union else 0.0


def title_similarity(title_a: str, title_b: str) -> float:
    norm_a = normalize_title(title_a)
    norm_b = normalize_title(title_b)
    if not norm_a or not norm_b:
        return 0.0
    if norm_a == norm_b:
        return 1.0
    if norm_a in norm_b or norm_b in norm_a:
        return 0.82
    return jaccard_similarity(extract_tokens(norm_a), extract_tokens(norm_b))


def parse_publish_time(value: Any) -> Optional[datetime]:
    if value is None or value == "":
        return None

    try:
        if isinstance(value, (int, float)):
            return datetime.fromtimestamp(float(value), tz=timezone.utc).astimezone()

        text = str(value).strip()
        text = text.replace("Z", "+00:00")
        if re.fullmatch(r"\d{10,13}", text):
            ts = float(text)
            if len(text) == 13:
                ts /= 1000
            return datetime.fromtimestamp(ts, tz=timezone.utc).astimezone()
        return datetime.fromisoformat(text).astimezone()
    except ValueError:
        return None


def hours_since_publish(value: Any) -> float:
    publish_time = parse_publish_time(value)
    if publish_time is None:
        return 72.0
    return max(0.0, (now_local() - publish_time).total_seconds() / 3600)


def noise_flags(item: Dict[str, Any]) -> List[str]:
    text = f"{item.get('title', '')} {item.get('content', '')}".lower()
    flags: List[str] = []

    if item.get("has_ad") or item.get("is_ad"):
        flags.append("promo")
    if any(keyword in text for keyword in PROMO_KEYWORDS):
        flags.append("lead_gen")
    if any(keyword in text for keyword in LOW_INFO_KEYWORDS):
        flags.append("low_information")
    if any(keyword in text for keyword in ABSOLUTE_WORDS):
        flags.append("sensational")

    title = str(item.get("title", "")).strip()
    if len(title) < 6:
        flags.append("short_title")

    punctuation_hits = len(re.findall(r"[!！?？]{2,}", title))
    if punctuation_hits > 0:
        flags.append("shouty_title")

    spam_score = safe_float(item.get("spam_score"))
    if spam_score >= 0.6:
        flags.append("spam_like")

    return sorted(set(flags))


def calculate_noise_penalty(item: Dict[str, Any]) -> float:
    flags = noise_flags(item)
    penalty = 0.0

    weight_map = {
        "promo": 0.35,
        "lead_gen": 0.22,
        "low_information": 0.16,
        "sensational": 0.14,
        "short_title": 0.08,
        "shouty_title": 0.08,
        "spam_like": 0.32,
    }

    for flag in flags:
        penalty += weight_map.get(flag, 0.0)

    if item.get("is_repost") and not item.get("source_attributed"):
        penalty += 0.18

    return clamp(penalty)


def freshness_score(item: Dict[str, Any]) -> float:
    hours = hours_since_publish(item.get("publish_time"))
    realtime = max(0.0, 1 - hours / 24)

    delta_signal = (
        safe_float(item.get("delta_1h")) / 1000 * 0.5
        + safe_float(item.get("delta_3h")) / 5000 * 0.3
        + safe_float(item.get("delta_6h")) / 10000 * 0.2
    )
    velocity = clamp(delta_signal)

    topic_type = item.get("topic_type") or "general"
    lifecycle_map = {
        "breaking": 6,
        "news": 12,
        "entertainment": 24,
        "tech": 48,
        "general": 24,
    }
    typical_life = lifecycle_map.get(topic_type, 24)
    decay = clamp(max(0.0, typical_life - hours) / typical_life)

    return clamp(realtime * 0.45 + velocity * 0.35 + decay * 0.20)


def estimate_emotion(item: Dict[str, Any], comment_value: float, forwarding_value: float) -> float:
    direct = safe_float(item.get("emotion_intensity"))
    if direct > 0:
        return clamp(direct)

    positive = safe_float(item.get("positive_count"))
    negative = safe_float(item.get("negative_count"))
    neutral = safe_float(item.get("neutral_count"))
    total = positive + negative + neutral
    if total > 0:
        return clamp((positive + negative) / total)

    density = comment_value / max(1.0, forwarding_value + 1.0)
    return clamp(0.35 + min(0.45, math.log1p(comment_value + forwarding_value) / 12) + min(0.20, density / 40))


def estimate_opposition(item: Dict[str, Any], comment_value: float) -> float:
    direct = max(safe_float(item.get("opposition_score")), safe_float(item.get("controversy_score")))
    if direct > 0:
        return clamp(direct)

    support = safe_float(item.get("support_count"))
    oppose = safe_float(item.get("oppose_count"))
    if support > 0 and oppose > 0:
        balance = min(support, oppose) / max(support, oppose)
        volume = clamp(math.log1p(support + oppose) / 10)
        return clamp(balance * 0.7 + volume * 0.3)

    positive = safe_float(item.get("positive_count"))
    negative = safe_float(item.get("negative_count"))
    if positive > 0 and negative > 0:
        balance = min(positive, negative) / max(positive, negative)
        volume = clamp(math.log1p(positive + negative) / 10)
        return clamp(balance * 0.65 + volume * 0.35)

    return clamp(min(0.6, math.log1p(comment_value) / 12))


@dataclass
class UnifiedItem:
    raw: Dict[str, Any]
    platform: str
    title: str
    url: str
    publish_time: Any
    discussion_raw: float
    propagation_raw: float
    forwarding_raw: float
    emotion_raw: float
    opposition_raw: float
    freshness_raw: float
    noise_penalty: float
    noise_flags: List[str]


class TopicRankAnalyzer:
    def __init__(self, window: str = "24h", top_n: int = 10):
        self.window = window
        self.top_n = top_n

    def load_data(self, file_path: str) -> Dict[str, List[Dict[str, Any]]]:
        with open(file_path, "r", encoding="utf-8") as handle:
            data = json.load(handle)

        platform_data: Dict[str, List[Dict[str, Any]]] = {platform: [] for platform in SUPPORTED_PLATFORMS}

        if isinstance(data, list):
            for item in data:
                platform = str(item.get("platform", "")).strip()
                if platform in platform_data:
                    platform_data[platform].append(item)
            return platform_data

        if not isinstance(data, dict):
            raise ValueError("Input JSON must be a list or a dict keyed by platform.")

        for platform in SUPPORTED_PLATFORMS:
            rows = data.get(platform, [])
            if isinstance(rows, list):
                platform_data[platform] = rows

        return platform_data

    def unify_items(self, platform_data: Dict[str, List[Dict[str, Any]]]) -> List[UnifiedItem]:
        unified: List[UnifiedItem] = []

        for platform, rows in platform_data.items():
            for row in rows:
                normalized = dict(row)
                normalized["platform"] = platform
                normalized["author"] = row.get("author") or row.get("account") or row.get("nickname") or ""
                normalized["author_id"] = row.get("author_id") or row.get("account_id") or ""
                title = str(row.get("title", "")).strip()
                url = str(row.get("url", "")).strip()

                discussion = (
                    safe_float(row.get("comment"))
                    + safe_float(row.get("comment_count"))
                    + safe_float(row.get("reply_count"))
                    + safe_float(row.get("qa_count"))
                )
                propagation = (
                    safe_float(row.get("view"))
                    + safe_float(row.get("read"))
                    + safe_float(row.get("reads"))
                    + safe_float(row.get("exposure"))
                    + safe_float(row.get("delta_1h")) * 8
                    + safe_float(row.get("delta_3h")) * 3
                    + safe_float(row.get("delta_6h")) * 1.5
                )
                forwarding = (
                    safe_float(row.get("share"))
                    + safe_float(row.get("forward"))
                    + safe_float(row.get("repost"))
                    + safe_float(row.get("save"))
                    + safe_float(row.get("fav"))
                    + safe_float(row.get("favorite"))
                )

                noise_pen = calculate_noise_penalty(normalized)

                unified.append(
                    UnifiedItem(
                        raw=normalized,
                        platform=platform,
                        title=title,
                        url=url,
                        publish_time=row.get("publish_time"),
                        discussion_raw=discussion,
                        propagation_raw=propagation,
                        forwarding_raw=forwarding,
                        emotion_raw=estimate_emotion(normalized, discussion, forwarding),
                        opposition_raw=estimate_opposition(normalized, discussion),
                        freshness_raw=freshness_score(normalized),
                        noise_penalty=noise_pen,
                        noise_flags=noise_flags(normalized),
                    )
                )

        return unified

    def score_items(self, items: List[UnifiedItem]) -> List[Dict[str, Any]]:
        if not items:
            return []

        discussion_scores = percentile_scores([item.discussion_raw for item in items])
        propagation_scores = percentile_scores([item.propagation_raw for item in items])
        forwarding_scores = percentile_scores([item.forwarding_raw for item in items])

        scored: List[Dict[str, Any]] = []

        for index, item in enumerate(items):
            platform_quality = PLATFORM_QUALITY.get(item.platform, 0.9)
            bias_guard = clamp(0.55 + platform_quality * 0.25 + (1 - item.noise_penalty) * 0.20)

            base_score = (
                discussion_scores[index] * 0.26
                + propagation_scores[index] * 0.24
                + forwarding_scores[index] * 0.18
                + item.freshness_raw * 0.12
                + item.emotion_raw * 0.10
                + item.opposition_raw * 0.10
            )
            overall = base_score * bias_guard * (1 - item.noise_penalty * 0.75)

            scored.append(
                {
                    **item.raw,
                    "platform": item.platform,
                    "title": item.title,
                    "url": item.url,
                    "discussion_score": discussion_scores[index],
                    "propagation_score": propagation_scores[index],
                    "forwarding_score": forwarding_scores[index],
                    "emotion_score": item.emotion_raw,
                    "opposition_score": item.opposition_raw,
                    "conflict_score": item.opposition_raw,
                    "freshness_score": item.freshness_raw,
                    "noise_penalty": item.noise_penalty,
                    "noise_flags": item.noise_flags,
                    "bias_guard_score": bias_guard,
                    "item_score": clamp(overall),
                    "title_tokens": extract_tokens(item.title),
                }
            )

        return scored

    def cluster_items(self, items: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
        clusters: List[List[Dict[str, Any]]] = []

        for item in sorted(items, key=lambda current: current["item_score"], reverse=True):
            matched_cluster: Optional[List[Dict[str, Any]]] = None

            for cluster in clusters:
                if self._same_topic(item, cluster):
                    matched_cluster = cluster
                    break

            if matched_cluster is None:
                clusters.append([item])
            else:
                matched_cluster.append(item)

        return clusters

    def _same_topic(self, item: Dict[str, Any], cluster: List[Dict[str, Any]]) -> bool:
        event_id = item.get("event_id")
        if event_id and any(event_id == member.get("event_id") for member in cluster):
            return True

        for member in cluster[:5]:
            if title_similarity(item.get("title", ""), member.get("title", "")) >= 0.38:
                return True

        item_tokens = set(item.get("title_tokens", []))
        if not item_tokens:
            return False

        cluster_tokens = set()
        for member in cluster[:5]:
            cluster_tokens.update(member.get("title_tokens", []))

        return jaccard_similarity(item_tokens, cluster_tokens) >= 0.36

    def aggregate_clusters(self, clusters: List[List[Dict[str, Any]]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        top_topics: List[Dict[str, Any]] = []
        filtered_noise: List[Dict[str, Any]] = []

        for cluster_index, cluster in enumerate(clusters, start=1):
            avg_noise = sum(item["noise_penalty"] for item in cluster) / len(cluster)
            if avg_noise >= 0.70:
                filtered_noise.append(
                    {
                        "title": cluster[0].get("title", ""),
                        "platform": cluster[0].get("platform", ""),
                        "noise_penalty": round(avg_noise, 3),
                        "noise_flags": sorted({flag for item in cluster for flag in item.get("noise_flags", [])}),
                    }
                )
                continue

            platforms = sorted({item["platform"] for item in cluster})
            platform_count = len(platforms)
            coverage_boost = clamp(platform_count / 4)
            evidence_count = len(cluster)
            bias_guard = clamp(
                min(1.0, 0.45 + coverage_boost * 0.30 + min(1.0, evidence_count / 8) * 0.25)
                * (1 - avg_noise * 0.2)
            )

            discussion = sum(item["discussion_score"] for item in cluster) / len(cluster)
            propagation = sum(item["propagation_score"] for item in cluster) / len(cluster)
            forwarding = sum(item["forwarding_score"] for item in cluster) / len(cluster)
            emotion = sum(item["emotion_score"] for item in cluster) / len(cluster)
            opposition = sum(item["opposition_score"] for item in cluster) / len(cluster)
            freshness = sum(item["freshness_score"] for item in cluster) / len(cluster)
            item_score = sum(item["item_score"] for item in cluster) / len(cluster)

            overall = clamp(
                item_score * (0.82 + coverage_boost * 0.18) * (0.90 + bias_guard * 0.10) * (1 - avg_noise * 0.50)
            )

            representative_titles = self._representative_titles(cluster)
            neutral_topic = self._neutral_topic_name(cluster, representative_titles)
            why_hot = self._build_hot_reason(platform_count, discussion, propagation, forwarding, freshness, opposition)
            noise_note = self._build_noise_note(avg_noise, cluster)
            neutrality_note = self._build_neutrality_note(platform_count, opposition, avg_noise)
            confidence = clamp(0.45 + coverage_boost * 0.25 + min(1.0, evidence_count / 10) * 0.20 + bias_guard * 0.10)

            top_topics.append(
                {
                    "rank": 0,
                    "topic_id": f"topic_{cluster_index:03d}",
                    "neutral_topic": neutral_topic,
                    "representative_titles": representative_titles,
                    "overall_score": round(overall * 100, 1),
                    "discussion_score": round(discussion * 100, 1),
                    "propagation_score": round(propagation * 100, 1),
                    "forwarding_score": round(forwarding * 100, 1),
                    "emotion_score": round(emotion * 100, 1),
                    "opposition_score": round(opposition * 100, 1),
                    "conflict_score": round(opposition * 100, 1),
                    "freshness_score": round(freshness * 100, 1),
                    "noise_penalty": round(avg_noise, 3),
                    "bias_guard_score": round(bias_guard, 3),
                    "confidence": round(confidence, 3),
                    "platform_count": platform_count,
                    "item_count": evidence_count,
                    "platforms": platforms,
                    "why_hot": why_hot,
                    "noise_note": noise_note,
                    "neutrality_note": neutrality_note,
                    "evidence": self._build_evidence(cluster),
                }
            )

        top_topics.sort(key=lambda topic: topic["overall_score"], reverse=True)

        for rank, topic in enumerate(top_topics[: self.top_n], start=1):
            topic["rank"] = rank

        return top_topics[: self.top_n], filtered_noise

    def _representative_titles(self, cluster: List[Dict[str, Any]]) -> List[str]:
        seen = set()
        titles: List[str] = []
        for item in sorted(cluster, key=lambda current: current["item_score"], reverse=True):
            title = item.get("title", "").strip()
            normalized = normalize_title(title)
            if title and normalized not in seen:
                seen.add(normalized)
                titles.append(title)
            if len(titles) >= 3:
                break
        return titles

    def _neutral_topic_name(self, cluster: List[Dict[str, Any]], titles: List[str]) -> str:
        token_counter: Counter[str] = Counter()
        for item in cluster:
            token_counter.update(token for token in item.get("title_tokens", []) if token not in STOPWORDS)

        common_tokens = [token for token, count in token_counter.most_common(4) if count >= 2 and len(token) >= 2]
        if common_tokens:
            return " / ".join(common_tokens[:3])

        if titles:
            neutral = re.sub(r"[!?！？]+", "", titles[0]).strip()
            return neutral[:40]

        return "未命名热点"

    def _build_hot_reason(
        self,
        platform_count: int,
        discussion: float,
        propagation: float,
        forwarding: float,
        freshness: float,
        opposition: float,
    ) -> str:
        fragments = []
        if platform_count >= 4:
            fragments.append("多平台同步上升")
        if discussion >= 0.75:
            fragments.append("讨论密度高")
        if propagation >= 0.75:
            fragments.append("传播范围大")
        if forwarding >= 0.70:
            fragments.append("转发意愿强")
        if freshness >= 0.70:
            fragments.append("仍处于热度窗口")
        if opposition >= 0.65:
            fragments.append("存在明显观点对冲")
        return "，".join(fragments) if fragments else "多个热度指标均处于中上水平。"

    def _build_noise_note(self, avg_noise: float, cluster: List[Dict[str, Any]]) -> str:
        flags = sorted({flag for item in cluster for flag in item.get("noise_flags", [])})
        if avg_noise < 0.20:
            return "噪音较低，未发现明显广告或引流主导。"
        if not flags:
            return "存在一定噪音，已在排序时做降权。"
        return f"已对 {', '.join(flags)} 做去噪降权。"

    def _build_neutrality_note(self, platform_count: int, opposition: float, avg_noise: float) -> str:
        if platform_count == 1:
            return "结果主要来自单一平台，已降低置信度，不能直接视为全网共识。"
        if opposition >= 0.65:
            return "该话题争议较强，结果只表示热度与分化程度，不表示任何立场。"
        if avg_noise >= 0.30:
            return "该话题含一定噪音，结果已做客观性修正。"
        return "结果仅表示话题热度，不表示价值判断或立场推荐。"

    def _build_evidence(self, cluster: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        evidence: List[Dict[str, Any]] = []
        used_platforms = set()
        for item in sorted(cluster, key=lambda current: current["item_score"], reverse=True):
            platform = item.get("platform", "")
            if platform in used_platforms:
                continue
            used_platforms.add(platform)
            evidence.append(
                {
                    "platform": platform,
                    "platform_label": PLATFORM_LABELS.get(platform, platform),
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "publish_time": item.get("publish_time"),
                }
            )
            if len(evidence) >= 5:
                break
        return evidence

    def build_report(
        self,
        platform_data: Dict[str, List[Dict[str, Any]]],
        top_topics: List[Dict[str, Any]],
        filtered_noise: List[Dict[str, Any]],
        query: Optional[str] = None,
    ) -> Dict[str, Any]:
        total_items = sum(len(rows) for rows in platform_data.values())
        platforms_covered = [platform for platform, rows in platform_data.items() if rows]

        return {
            "run_meta": {
                "ts": now_local().strftime("%Y-%m-%d %H:%M"),
                "window": self.window,
                "top_n_requested": self.top_n,
                "top_n_returned": len(top_topics),
                "mode": "objective-hot-topic-scan",
                "query": query,
                "platforms_covered": platforms_covered,
                "total_input_items": total_items,
            },
            "ranking_basis": {
                "discussion_weight": 0.26,
                "propagation_weight": 0.24,
                "forwarding_weight": 0.18,
                "freshness_weight": 0.12,
                "emotion_weight": 0.10,
                "opposition_weight": 0.10,
                "noise_penalty_applied": True,
                "bias_guard_applied": True,
            },
            "top_topics": top_topics,
            "filtered_noise": filtered_noise,
            "summary": {
                "platform_topic_count": {platform: len(rows) for platform, rows in platform_data.items() if rows},
                "top_topic_names": [topic["neutral_topic"] for topic in top_topics[:3]],
                "noise_filtered_count": len(filtered_noise),
            },
        }


def main() -> None:
    parser = argparse.ArgumentParser(description="Cross-platform hot-topic analyzer")
    parser.add_argument("--all-data", required=True, help="Path to input JSON")
    parser.add_argument("--output", required=True, help="Path to output JSON")
    parser.add_argument("--window", default="24h", help="Time window label")
    parser.add_argument("--top-n", type=int, default=10, help="Number of top topics to return")
    parser.add_argument("--query", default=None, help="Optional user query for metadata")

    args = parser.parse_args()

    analyzer = TopicRankAnalyzer(window=args.window, top_n=args.top_n)
    platform_data = analyzer.load_data(args.all_data)
    unified_items = analyzer.unify_items(platform_data)
    if not unified_items:
        raise SystemExit("No valid items found in input.")

    scored_items = analyzer.score_items(unified_items)
    clusters = analyzer.cluster_items(scored_items)
    top_topics, filtered_noise = analyzer.aggregate_clusters(clusters)
    report = analyzer.build_report(platform_data, top_topics, filtered_noise, query=args.query)

    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2)

    print(f"Analyzed {sum(len(rows) for rows in platform_data.values())} items.")
    print(f"Returned {len(top_topics)} top topics and filtered {len(filtered_noise)} noisy clusters.")
    print(f"Saved report to {args.output}")


if __name__ == "__main__":
    main()
