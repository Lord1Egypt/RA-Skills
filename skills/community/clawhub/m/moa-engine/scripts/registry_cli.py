#!/usr/bin/env python3
"""
MoA 能力注册表 CLI
====================
能力画像存储 + BM25 语义匹配引擎（零外部依赖）

用法:
  python scripts/registry_cli.py match --task "..." --profiles "..." [--top-k 3] [--min-score 0.3]
  python scripts/registry_cli.py list --profiles "..." [--domain "..."]
  python scripts/registry_cli.py register --id "expert-xx" --title "..." --domains "a,b" --output "..."
  python scripts/registry_cli.py add-profile --profile-json '{...}' --output "..."
"""

import argparse
import json
import math
import re
import sys
import os
from collections import Counter
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict
from typing import List, Optional


# ============================================================
# 数据模型
# ============================================================

@dataclass
class PerformanceVector:
    proposal_depth: float = 0.5
    critique_specificity: float = 0.5
    revision_quality: float = 0.5
    synthesis_novelty: float = 0.5
    token_efficiency: float = 0.5
    adoption_rate: float = 0.5


@dataclass
class Meta:
    created_at: str = ""
    updated_at: str = ""
    source: str = "seed"  # seed | moa_run | manual | rhi_evolved
    run_count: int = 0
    tags: List[str] = field(default_factory=list)


@dataclass
class CapabilityProfile:
    id: str
    version: int = 1
    title: str = ""
    domains: List[str] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    thinking_style: str = "analytical"  # analytical | creative | critical | pragmatic | systems
    embedding: List[float] = field(default_factory=list)
    performance_vector: PerformanceVector = field(default_factory=PerformanceVector)
    meta: Meta = field(default_factory=Meta)

    @classmethod
    def from_dict(cls, d: dict) -> "CapabilityProfile":
        pv = PerformanceVector(**(d.get("performance_vector", {})))
        m = Meta(**(d.get("meta", {})))
        return cls(
            id=d["id"],
            version=d.get("version", 1),
            title=d.get("title", ""),
            domains=d.get("domains", []),
            skills=d.get("skills", []),
            thinking_style=d.get("thinking_style", "analytical"),
            embedding=d.get("embedding", []),
            performance_vector=pv,
            meta=m,
        )


@dataclass
class MatchResult:
    profile: dict
    score: float
    matched_domains: List[str]
    reason: str


@dataclass
class SignalTag:
    """MoA 执行后产生的信号标签"""
    metric: str       # proposal_depth | critique_specificity | revision_quality | synthesis_novelty | token_efficiency | adoption_rate
    score: float      # 0.0 - 1.0
    expert_id: str    # 目标专家 ID
    source: str = ""  # 信号来源（moa_run / manual / rhi）
    round: int = 0    # 产生轮次


# ============================================================
# BM25 匹配引擎
# ============================================================

class BM25Matcher:
    """零依赖 BM25 匹配引擎"""

    def __init__(self, profiles: List[CapabilityProfile]):
        self.profiles = profiles
        self._build_index()

    def _tokenize(self, text: str) -> List[str]:
        """中文 + 英文分词；中文用 2-gram 改善匹配质量"""
        text = text.lower()
        tokens = []
        # 英文/数字 token
        for eng in re.findall(r'[a-zA-Z0-9]+', text):
            tokens.append(eng)
        # 中文：切分为 2-gram 字符块
        chinese_parts = re.findall(r'[\u4e00-\u9fff]+', text)
        for part in chinese_parts:
            if len(part) <= 2:
                tokens.append(part)
            else:
                for i in range(len(part) - 1):
                    tokens.append(part[i:i+2])
        return tokens

    def _build_index(self):
        """构建文档索引"""
        self.doc_ids = []
        self.documents = []
        self.doc_domains = []
        self.doc_titles = []

        for p in self.profiles:
            doc_text = f"{p.title} {' '.join(p.domains)} {' '.join(p.skills)}"
            self.doc_ids.append(p.id)
            self.documents.append(self._tokenize(doc_text))
            self.doc_domains.append(p.domains)
            self.doc_titles.append(p.title)

        # 计算 IDF
        self.N = len(self.documents)
        self.df = Counter()
        for doc in self.documents:
            for token in set(doc):
                self.df[token] += 1

        self.idf = {}
        for token, freq in self.df.items():
            self.idf[token] = math.log((self.N - freq + 0.5) / (freq + 0.5) + 1.0)

        # 文档长度统计
        self.doc_lengths = [len(doc) for doc in self.documents]
        self.avg_doc_len = sum(self.doc_lengths) / max(len(self.doc_lengths), 1)

    def _score_bm25(self, query_tokens: List[str], doc_idx: int, k1=1.5, b=0.75) -> float:
        """计算单文档 BM25 得分"""
        doc = self.documents[doc_idx]
        doc_len = self.doc_lengths[doc_idx]
        doc_tf = Counter(doc)

        score = 0.0
        for token in query_tokens:
            if token not in self.idf:
                continue
            tf = doc_tf.get(token, 0)
            if tf == 0:
                continue
            idf_val = self.idf[token]
            numerator = tf * (k1 + 1)
            denominator = tf + k1 * (1 - b + b * doc_len / self.avg_doc_len)
            score += idf_val * numerator / denominator

        return score

    def match(self, task_text: str, top_k: int = 3, min_score: float = 0.3,
              required_domains: Optional[List[str]] = None,
              excluded_ids: Optional[List[str]] = None) -> List[MatchResult]:
        """匹配最合适的专家"""
        query_tokens = self._tokenize(task_text)
        if not query_tokens:
            return []

        excluded = set(excluded_ids or [])
        scores = []

        for i in range(self.N):
            if self.doc_ids[i] in excluded:
                continue
            score = self._score_bm25(query_tokens, i)
            if score < min_score:
                continue

            # 计算领域匹配
            matched = []
            if required_domains:
                req_set = set(d.lower() for d in required_domains)
                prof_set = set(d.lower() for d in self.doc_domains[i])
                matched = list(req_set & prof_set)
                # 有领域要求时，无匹配则降权
                if not matched:
                    score *= 0.5

            scores.append((score, i, matched))

        # 按得分排序
        scores.sort(key=lambda x: -x[0])

        # 构建结果
        results = []
        for score, idx, matched in scores[:top_k]:
            p = self.profiles[idx]
            reason_parts = []
            if matched:
                reason_parts.append(f"领域匹配: {', '.join(matched)}")
            if p.domains:
                reason_parts.append(f"领域覆盖: {', '.join(p.domains[:3])}")
            if p.skills:
                reason_parts.append(f"技能: {', '.join(p.skills[:3])}")
            reason = "; ".join(reason_parts) if reason_parts else f"综合匹配度 {score:.2f}"

            results.append(MatchResult(
                profile=asdict(p),
                score=round(score, 4),
                matched_domains=matched,
                reason=reason,
            ))

        return results


# ============================================================
# 能力注册表
# ============================================================

class CapabilityRegistry:
    """能力注册表 —— 管理专家画像的增删改查与匹配"""

    def __init__(self, path: Optional[str] = None):
        self.path = path
        self.profiles: List[CapabilityProfile] = []
        self.matcher: Optional[BM25Matcher] = None
        if path and os.path.exists(path):
            self.load()

    def load(self, path: Optional[str] = None) -> "CapabilityRegistry":
        """从 JSON 文件加载"""
        load_path = path or self.path
        if not load_path:
            raise ValueError("No path specified")
        with open(load_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.profiles = [CapabilityProfile.from_dict(p) for p in data.get("profiles", [])]
        self.matcher = BM25Matcher(self.profiles)
        self.path = load_path
        return self

    def persist(self, path: Optional[str] = None) -> None:
        """持久化到 JSON 文件"""
        save_path = path or self.path
        if not save_path:
            raise ValueError("No path specified")
        data = {
            "version": "1.0",
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "profile_count": len(self.profiles),
            "profiles": [asdict(p) for p in self.profiles],
        }
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def register(self, profile: CapabilityProfile) -> None:
        """注册新专家"""
        # 检查是否已存在
        for i, p in enumerate(self.profiles):
            if p.id == profile.id:
                profile.version = p.version + 1
                self.profiles[i] = profile
                break
        else:
            self.profiles.append(profile)
        # 重建索引
        self.matcher = BM25Matcher(self.profiles)

    def unregister(self, expert_id: str) -> bool:
        """注销专家"""
        before = len(self.profiles)
        self.profiles = [p for p in self.profiles if p.id != expert_id]
        if len(self.profiles) < before:
            self.matcher = BM25Matcher(self.profiles)
            return True
        return False

    def get(self, expert_id: str) -> Optional[CapabilityProfile]:
        """按 ID 查询"""
        for p in self.profiles:
            if p.id == expert_id:
                return p
        return None

    def list_all(self, domain: Optional[str] = None) -> List[CapabilityProfile]:
        """列出所有专家（可按领域过滤）"""
        if domain:
            d = domain.lower()
            return [p for p in self.profiles if d in [x.lower() for x in p.domains]]
        return self.profiles

    def match(self, task_text: str, top_k: int = 3, min_score: float = 0.3,
              required_domains: Optional[List[str]] = None,
              excluded_ids: Optional[List[str]] = None) -> List[MatchResult]:
        """语义匹配专家"""
        if not self.matcher:
            raise ValueError("Registry not loaded. Call load() first.")
        return self.matcher.match(task_text, top_k, min_score, required_domains, excluded_ids)

    def update_from_signals(self, signals: List[SignalTag], alpha: float = 0.3) -> dict:
        """根据信号标签更新专家 performance_vector（EMA 加权）

        alpha: 新信号的权重 (0-1)，越大历史衰减越快。默认 0.3（新信号占 30%）
        """
        updates = {}
        for sig in signals:
            expert = self.get(sig.expert_id)
            if not expert:
                updates[sig.expert_id] = {"status": "skipped", "reason": "expert not found"}
                continue

            metric = sig.metric
            if not hasattr(expert.performance_vector, metric):
                updates[sig.expert_id] = {"status": "skipped", "reason": f"unknown metric: {metric}"}
                continue

            # EMA 更新
            old_val = getattr(expert.performance_vector, metric)
            new_val = round(alpha * sig.score + (1 - alpha) * old_val, 4)
            setattr(expert.performance_vector, metric, new_val)

            # 更新元数据
            expert.version += 1
            expert.meta.run_count += 1
            expert.meta.updated_at = datetime.now(timezone.utc).isoformat()
            if sig.source:
                expert.meta.source = sig.source

            if sig.expert_id not in updates:
                updates[sig.expert_id] = {"status": "updated", "metrics": {}}
            updates[sig.expert_id]["metrics"][metric] = {
                "old": old_val,
                "new": new_val,
                "signal": sig.score,
            }

        # 重建索引
        if updates:
            self.matcher = BM25Matcher(self.profiles)

        return updates

    def stats(self) -> dict:
        """注册表统计"""
        domain_count = Counter()
        style_count = Counter()
        for p in self.profiles:
            for d in p.domains:
                domain_count[d] += 1
            style_count[p.thinking_style] += 1
        return {
            "total_profiles": len(self.profiles),
            "domain_distribution": dict(domain_count.most_common()),
            "thinking_style_distribution": dict(style_count.most_common()),
            "avg_skills_per_profile": round(sum(len(p.skills) for p in self.profiles) / max(len(self.profiles), 1), 1),
        }


# ============================================================
# CLI 入口
# ============================================================

def cmd_match(args):
    """match 子命令"""
    registry = CapabilityRegistry(args.profiles)
    results = registry.match(
        task_text=args.task,
        top_k=args.top_k,
        min_score=args.min_score,
        required_domains=args.domains.split(",") if args.domains else None,
        excluded_ids=args.exclude.split(",") if args.exclude else None,
    )
    output = {
        "task": args.task,
        "top_k": args.top_k,
        "min_score": args.min_score,
        "matches": [
            {
                "profile": r.profile,
                "score": r.score,
                "matched_domains": r.matched_domains,
                "reason": r.reason,
            }
            for r in results
        ],
        "total_matches": len(results),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_list(args):
    """list 子命令"""
    registry = CapabilityRegistry(args.profiles)
    profiles = registry.list_all(domain=args.domain)
    output = {
        "total": len(profiles),
        "domain_filter": args.domain,
        "profiles": [
            {
                "id": p.id,
                "title": p.title,
                "domains": p.domains,
                "skills": p.skills[:5],
                "thinking_style": p.thinking_style,
                "version": p.version,
                "run_count": p.meta.run_count,
            }
            for p in profiles
        ],
        "stats": registry.stats(),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_register(args):
    """register 子命令"""
    now = datetime.now(timezone.utc).isoformat()
    profile = CapabilityProfile(
        id=args.id,
        title=args.title,
        domains=[d.strip() for d in args.domains.split(",") if d.strip()],
        skills=[s.strip() for s in args.skills.split(",") if s.strip()] if args.skills else [],
        thinking_style=args.style,
        embedding=[],
        performance_vector=PerformanceVector(),
        meta=Meta(created_at=now, updated_at=now, source="manual"),
    )
    registry = CapabilityRegistry(args.output)
    registry.register(profile)
    registry.persist()
    print(json.dumps({"status": "ok", "id": profile.id, "version": profile.version}, ensure_ascii=False))


def cmd_add_profile(args):
    """add-profile 子命令 —— 从 JSON 字符串添加"""
    profile_dict = json.loads(args.profile_json)
    profile = CapabilityProfile.from_dict(profile_dict)
    registry = CapabilityRegistry(args.output)
    registry.register(profile)
    registry.persist()
    print(json.dumps({"status": "ok", "id": profile.id, "version": profile.version}, ensure_ascii=False))


def cmd_update(args):
    """update 子命令 —— 从信号标签更新专家 performance_vector"""
    with open(args.signals, "r", encoding="utf-8") as f:
        raw = json.load(f)

    signals = [SignalTag(**s) for s in raw]
    registry = CapabilityRegistry(args.profiles)
    results = registry.update_from_signals(signals, alpha=args.alpha)
    registry.persist()

    output = {
        "total_signals": len(signals),
        "experts_updated": sum(1 for v in results.values() if v["status"] == "updated"),
        "experts_skipped": sum(1 for v in results.values() if v["status"] == "skipped"),
        "updates": results,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_stats(args):
    """stats 子命令"""
    registry = CapabilityRegistry(args.profiles)
    stats = registry.stats()
    print(json.dumps(stats, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="MoA 能力注册表 —— 专家画像存储与 BM25 语义匹配引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 匹配专家
  python scripts/registry_cli.py match --task "设计高并发消息队列" --profiles references/capability-profiles.json --top-k 3

  # 列出所有专家
  python scripts/registry_cli.py list --profiles references/capability-profiles.json

  # 按领域过滤
  python scripts/registry_cli.py list --profiles references/capability-profiles.json --domain security

  # 注册新专家
  python scripts/registry_cli.py register --id "expert-ai-arch" --title "AI架构师" --domains "ai,ml,architecture" --skills "transformer,模型部署,推理优化" --style analytical --output references/capability-profiles.json

  # 从信号标签更新 performance_vector
  python scripts/registry_cli.py update --signals signals.json --profiles references/capability-profiles.json --alpha 0.3

  # 查看统计
  python scripts/registry_cli.py stats --profiles references/capability-profiles.json
        """
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # match
    p_match = subparsers.add_parser("match", help="语义匹配专家")
    p_match.add_argument("--task", required=True, help="子任务描述")
    p_match.add_argument("--profiles", required=True, help="专家画像 JSON 文件路径")
    p_match.add_argument("--top-k", type=int, default=3, help="返回 Top-K 结果 (默认 3)")
    p_match.add_argument("--min-score", type=float, default=0.3, help="最低匹配得分 (默认 0.3)")
    p_match.add_argument("--domains", help="必须覆盖的领域（逗号分隔）")
    p_match.add_argument("--exclude", help="排除的专家 ID（逗号分隔）")

    # list
    p_list = subparsers.add_parser("list", help="列出专家")
    p_list.add_argument("--profiles", required=True, help="专家画像 JSON 文件路径")
    p_list.add_argument("--domain", help="按领域过滤")

    # register
    p_reg = subparsers.add_parser("register", help="注册新专家")
    p_reg.add_argument("--id", required=True, help="专家唯一 ID")
    p_reg.add_argument("--title", required=True, help="显示头衔")
    p_reg.add_argument("--domains", required=True, help="领域列表（逗号分隔）")
    p_reg.add_argument("--skills", help="技能列表（逗号分隔）")
    p_reg.add_argument("--style", default="analytical", choices=["analytical", "creative", "critical", "pragmatic", "systems"], help="思维风格")
    p_reg.add_argument("--output", required=True, help="输出 JSON 文件路径")

    # add-profile
    p_add = subparsers.add_parser("add-profile", help="从 JSON 添加专家")
    p_add.add_argument("--profile-json", required=True, help="专家画像 JSON 字符串")
    p_add.add_argument("--output", required=True, help="输出 JSON 文件路径")

    # stats
    p_stats = subparsers.add_parser("stats", help="注册表统计")
    p_stats.add_argument("--profiles", required=True, help="专家画像 JSON 文件路径")

    # update
    p_update = subparsers.add_parser("update", help="根据信号标签更新专家 performance_vector")
    p_update.add_argument("--signals", required=True, help="信号标签 JSON 文件路径")
    p_update.add_argument("--profiles", required=True, help="专家画像 JSON 文件路径")
    p_update.add_argument("--alpha", type=float, default=0.3, help="EMA 平滑系数 (默认 0.3)")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    cmd_map = {
        "match": cmd_match,
        "list": cmd_list,
        "register": cmd_register,
        "add-profile": cmd_add_profile,
        "update": cmd_update,
        "stats": cmd_stats,
    }
    cmd_map[args.command](args)


if __name__ == "__main__":
    main()