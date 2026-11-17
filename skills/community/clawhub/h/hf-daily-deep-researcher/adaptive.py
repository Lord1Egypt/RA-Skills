#!/usr/bin/env python3
"""
Smart Paper Tracker - 自适应模块
核心功能：
1. 从用户对话自动调整关键词权重
2. 根据论文产出量自适应调整追踪频率
3. 计算论文优先级分数
4. 关键词自动扩展
"""

import json
import os
import argparse
from datetime import datetime, timedelta
from typing import List, Dict, Tuple

class AdaptiveTracker:
    def __init__(self, skill_dir: str = None):
        if skill_dir is None:
            # 从脚本位置推导，适配任意安装路径
            skill_dir = os.path.dirname(os.path.abspath(__file__))
        self.skill_dir = skill_dir
        self.config_path = os.path.join(skill_dir, "config.json")
        self.keywords_path = os.path.join(skill_dir, "keywords.json")
        self.history_path = os.path.join(skill_dir, "history", "scan_history.json")
        
        self.config = self._load_json(self.config_path, {})
        self.keywords = self._load_json(self.keywords_path, {"keywords": [], "blacklist": [], "authors": [], "institutions": []})
        self.history = self._load_json(self.history_path, [])
    
    def _load_json(self, path: str, default: dict) -> dict:
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return default
    
    def _save_json(self, path: str, data: dict):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
    
    # ============ 关键词自适应 ============
    
    def update_keywords_from_conversation(self, conversation_text: str, boost: float = 0.1) -> List[str]:
        """
        分析用户对话，自动调整关键词权重
        
        Args:
            conversation_text: 用户对话文本
            boost: 每次提及的权重增量
        
        Returns:
            被更新的关键词列表
        """
        updated = []
        text_lower = conversation_text.lower()
        
        for kw in self.keywords.get("keywords", []):
            term = kw["term"].lower()
            # 检查是否提及
            if term in text_lower or any(syn in text_lower for syn in kw.get("synonyms", [])):
                old_weight = kw["weight"]
                kw["weight"] = min(1.0, kw["weight"] + boost)
                kw["last_mentioned"] = datetime.now().isoformat()
                if kw["weight"] != old_weight:
                    updated.append(kw["term"])
        
        # 衰减未提及的关键词
        self._decay_keywords()
        
        if updated:
            self._save_json(self.keywords_path, self.keywords)
            print(f"📝 已更新 {len(updated)} 个关键词权重: {', '.join(updated)}")
        
        return updated
    
    def _decay_keywords(self, decay_rate: float = 0.02, min_weight: float = 0.1):
        """衰减长期未提及的关键词"""
        now = datetime.now()
        for kw in self.keywords.get("keywords", []):
            last = kw.get("last_mentioned")
            if last:
                last_date = datetime.fromisoformat(last)
                weeks_passed = (now - last_date).days / 7
                if weeks_passed > 1:
                    # 每周衰减
                    decay = decay_rate * weeks_passed
                    kw["weight"] = max(min_weight, kw["weight"] - decay)
    
    def add_keyword(self, term: str, weight: float = 0.7, source: str = "user") -> bool:
        """手动添加关键词"""
        existing = [k for k in self.keywords.get("keywords", []) if k["term"].lower() == term.lower()]
        if existing:
            existing[0]["weight"] = max(existing[0]["weight"], weight)
            print(f"⚠️  关键词 '{term}' 已存在，权重更新为 {existing[0]['weight']}")
        else:
            self.keywords["keywords"].append({
                "term": term,
                "weight": weight,
                "source": source,
                "added_date": datetime.now().isoformat(),
                "last_mentioned": datetime.now().isoformat(),
                "synonyms": []
            })
            print(f"✅ 已添加关键词: '{term}' (权重: {weight})")
        
        # 按权重排序
        self.keywords["keywords"].sort(key=lambda x: x["weight"], reverse=True)
        
        # 限制数量
        max_kw = self.config.get("keywords", {}).get("max_keywords", 30)
        if len(self.keywords["keywords"]) > max_kw:
            removed = self.keywords["keywords"][max_kw:]
            self.keywords["keywords"] = self.keywords["keywords"][:max_kw]
            print(f"🗑️  已移除 {len(removed)} 个低权重关键词")
        
        self._save_json(self.keywords_path, self.keywords)
        return True
    
    def expand_keywords(self, new_terms: List[str], source_term: str = None):
        """扩展关键词（添加相关词）"""
        for term in new_terms:
            self.add_keyword(term, weight=0.4, source=f"expanded_from_{source_term}" if source_term else "auto")
    
    def show_keywords(self):
        """显示当前关键词列表"""
        print("\n📊 当前关键词列表 (按权重排序):")
        print("-" * 60)
        for i, kw in enumerate(self.keywords.get("keywords", []), 1):
            bar = "█" * int(kw["weight"] * 20)
            print(f"{i:2d}. {kw['term']:30s} | {kw['weight']:.2f} | {bar}")
        print("-" * 60)
        print(f"总计: {len(self.keywords.get('keywords', []))} 个关键词")
        
        if self.keywords.get("blacklist"):
            print(f"\n🚫 黑名单: {', '.join(self.keywords['blacklist'])}")
    
    # ============ 频率自适应 ============
    
    def suggest_frequency(self) -> Tuple[str, str]:
        """
        根据历史数据建议追踪频率
        
        Returns:
            (建议频率, 原因)
        """
        if len(self.history) < 2:
            return "weekly", "历史数据不足，使用默认频率"
        
        # 计算最近几周的平均论文数
        recent = self.history[-4:]  # 最近4次扫描
        avg_papers = sum(h.get("paper_count", 0) for h in recent) / len(recent)
        
        # 检测趋势
        if len(recent) >= 2:
            trend = (recent[-1].get("paper_count", 0) - recent[-2].get("paper_count", 0)) / max(recent[-2].get("paper_count", 1), 1)
        else:
            trend = 0
        
        # 检测是否有高影响力论文
        high_impact = any(
            any(p.get("priority", 0) >= 0.8 for p in h.get("papers", []))
            for h in recent[-2:]
        )
        
        # 决策逻辑
        if avg_papers > 15 or (trend > 0.5 and avg_papers > 8):
            freq = "daily"
            reason = f"高产期: 平均 {avg_papers:.1f} 篇/周，趋势 +{trend*100:.0f}%"
        elif avg_papers > 8 or high_impact:
            freq = "every_3_days"
            reason = f"活跃期: 平均 {avg_papers:.1f} 篇/周" + (", 有高影响力论文" if high_impact else "")
        elif avg_papers < 3:
            freq = "biweekly"
            reason = f"低产期: 平均 {avg_papers:.1f} 篇/周"
        else:
            freq = "weekly"
            reason = f"平稳期: 平均 {avg_papers:.1f} 篇/周"
        
        return freq, reason
    
    def update_frequency(self, freq: str = None):
        """更新追踪频率"""
        if freq is None:
            freq, reason = self.suggest_frequency()
            print(f"🔄 建议频率: {freq} ({reason})")
        
        self.config["tracking"]["base_frequency"] = freq
        self._save_json(self.config_path, self.config)
        print(f"✅ 追踪频率已更新为: {freq}")
        
        # 计算下次扫描时间
        now = datetime.now()
        freq_map = {
            "daily": timedelta(days=1),
            "every_3_days": timedelta(days=3),
            "weekly": timedelta(weeks=1),
            "biweekly": timedelta(weeks=2)
        }
        next_scan = now + freq_map.get(freq, timedelta(weeks=1))
        self.config["tracking"]["next_scan_date"] = next_scan.isoformat()
        self._save_json(self.config_path, self.config)
        print(f"📅 下次扫描: {next_scan.strftime('%Y-%m-%d')}")
    
    # ============ 优先级计算 ============
    
    def calculate_priority(self, paper: Dict) -> float:
        """
        计算论文优先级分数
        
        Args:
            paper: 论文信息 dict，包含 title, abstract, authors 等
        
        Returns:
            优先级分数 (0-1)
        """
        scores = []
        weights = []
        
        # 1. 关键词匹配度
        text = f"{paper.get('title', '')} {paper.get('abstract', '')}".lower()
        kw_score = 0
        for kw in self.keywords.get("keywords", []):
            if kw["term"].lower() in text:
                kw_score += kw["weight"]
        kw_score = min(1.0, kw_score / 2)  # 归一化
        scores.append(kw_score)
        weights.append(0.35)
        
        # 2. 作者影响力
        author_score = 0
        paper_authors = [a.get("name", "").lower() for a in paper.get("authors", [])]
        for tracked_author in self.keywords.get("authors", []):
            if tracked_author["name"].lower() in paper_authors:
                author_score = max(author_score, tracked_author.get("weight", 0.5))
        scores.append(author_score)
        weights.append(0.15)
        
        # 3. 代码可用性
        code_score = 0.2 if paper.get("has_code") else 0
        scores.append(code_score)
        weights.append(0.1)
        
        # 4. 方法新颖性（基于标题中的信号词）
        novelty_keywords = ["novel", "new", "first", "propose", "introduce"]
        novelty_score = sum(1 for w in novelty_keywords if w in text) / len(novelty_keywords)
        scores.append(novelty_score)
        weights.append(0.1)
        
        # 5. 实验规模
        scale_signals = ["large-scale", "extensive", "comprehensive", "sota", "state-of-the-art"]
        scale_score = sum(1 for w in scale_signals if w in text) / len(scale_signals)
        scores.append(scale_score)
        weights.append(0.1)
        
        # 6. 用户项目相关性（基于当前关键词权重）
        project_keywords = self.config.get("user_profile", {}).get("current_projects", [])
        project_score = 0
        for pk in project_keywords:
            if pk.lower() in text:
                project_score += 0.3
        project_score = min(1.0, project_score)
        scores.append(project_score)
        weights.append(0.2)
        
        # 加权求和
        total_weight = sum(weights)
        priority = sum(s * w for s, w in zip(scores, weights)) / total_weight
        
        return round(min(1.0, priority), 3)
    
    def classify_priority(self, score: float) -> Tuple[str, str]:
        """根据分数分类优先级"""
        if score >= 0.8:
            return "P0", "🔴 必须读"
        elif score >= 0.6:
            return "P1", "🟠 建议读"
        elif score >= 0.4:
            return "P2", "🟡 有时间读"
        else:
            return "P3", "🟢 快速浏览"
    
    # ============ 历史记录 ============
    
    def get_scan_history(self) -> List[Dict]:
        """获取扫描历史记录"""
        return self.history
    
    def record_scan(self, paper_count: int, papers: List[Dict]):
        """记录一次扫描结果"""
        record = {
            "date": datetime.now().isoformat(),
            "paper_count": paper_count,
            "p0_count": sum(1 for p in papers if p.get("priority", 0) >= 0.8),
            "p1_count": sum(1 for p in papers if 0.6 <= p.get("priority", 0) < 0.8),
            "top_papers": [
                {"title": p.get("title", ""), "priority": p.get("priority", 0)}
                for p in sorted(papers, key=lambda x: x.get("priority", 0), reverse=True)[:5]
            ]
        }
        self.history.append(record)
        self._save_json(self.history_path, self.history[-50:])  # 保留最近50条
    
    def show_history(self, n: int = 5):
        """显示扫描历史"""
        print(f"\n📈 最近 {min(n, len(self.history))} 次扫描记录:")
        print("-" * 60)
        for h in self.history[-n:]:
            date = datetime.fromisoformat(h["date"]).strftime("%Y-%m-%d")
            print(f"{date} | 总计: {h['paper_count']:2d} | P0: {h['p0_count']} | P1: {h['p1_count']}")
            for p in h.get("top_papers", [])[:3]:
                print(f"         └─ {p['title'][:40]}... (P: {p['priority']})")
        print("-" * 60)


def main():
    parser = argparse.ArgumentParser(description="Smart Paper Tracker - 自适应模块")
    parser.add_argument("--show-keywords", action="store_true", help="显示当前关键词")
    parser.add_argument("--add-keyword", type=str, help="添加关键词")
    parser.add_argument("--weight", type=float, default=0.7, help="关键词权重")
    parser.add_argument("--suggest-frequency", action="store_true", help="建议追踪频率")
    parser.add_argument("--update-frequency", type=str, help="更新追踪频率")
    parser.add_argument("--show-history", action="store_true", help="显示扫描历史")
    parser.add_argument("--analyze-conversation", type=str, help="分析对话文本并更新关键词")
    
    args = parser.parse_args()
    
    tracker = AdaptiveTracker()
    
    if args.show_keywords:
        tracker.show_keywords()
    elif args.add_keyword:
        tracker.add_keyword(args.add_keyword, args.weight)
        tracker.show_keywords()
    elif args.suggest_frequency:
        freq, reason = tracker.suggest_frequency()
        print(f"建议频率: {freq}")
        print(f"原因: {reason}")
    elif args.update_frequency:
        tracker.update_frequency(args.update_frequency)
    elif args.show_history:
        tracker.show_history()
    elif args.analyze_conversation:
        updated = tracker.update_keywords_from_conversation(args.analyze_conversation)
        if updated:
            print(f"从对话中更新了 {len(updated)} 个关键词")
        else:
            print("对话中未发现新的关键词提及")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
