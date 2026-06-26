#!/usr/bin/env python3
"""
OPC Skill互引推荐引擎
调用方式: python recommend.py <current_skill> [top_k] [user_id]
示例: python recommend.py 技术尽调 3 user123
"""
import json
import random
import sys
from datetime import datetime
from typing import List, Tuple, Dict

class OPCRecommendationEngine:
    """OPC导师Skill互引推荐引擎"""
    
    def __init__(self, network_path: str = None):
        if network_path is None:
            import os
            # 尝试多个可能路径
            possible_paths = [
                os.path.join(os.path.dirname(__file__), 'skill_network.json'),
                os.path.join(os.path.dirname(__file__), '..', 'skill_network.json'),
                'skill_network.json'
            ]
            for p in possible_paths:
                if os.path.exists(p):
                    network_path = p
                    break
            if network_path is None:
                raise FileNotFoundError("skill_network.json not found")
        
        with open(network_path, 'r', encoding='utf-8') as f:
            self.network = json.load(f)
        
        self.config = self.network["algorithm_config"]
        self.weights = self.config["weights"]
        
    def _calc_tag_similarity(self, skill_a: str, skill_b: str) -> float:
        """计算两个Skill之间的标签重叠度"""
        tags_a = self.network["skills"][skill_a]["tags"]
        tags_b = self.network["skills"][skill_b]["tags"]
        
        # Domain匹配权重: 2.0
        domain_overlap = len(set(tags_a["domain"]) & set(tags_b["domain"])) * 2.0
        
        # Stage匹配权重: 1.5
        stage_overlap = len(set(tags_a["stage"]) & set(tags_b["stage"])) * 1.5
        
        # Triggers匹配权重: 1.0
        trigger_overlap = len(set(tags_a["triggers"]) & set(tags_b["triggers"])) * 1.0
        
        # 归一化
        max_possible = 10.0
        return min((domain_overlap + stage_overlap + trigger_overlap) / max_possible, 1.0)
    
    def _get_fixed_score(self, current: str, target: str) -> float:
        """获取固定关联权重"""
        fixed_refs = self.network["skills"][current]["fixed_refs"]
        for ref in fixed_refs:
            if ref["skill"] == target:
                return ref["weight"]
        return 0.0
    
    def _random_factor(self, target: str, user_id: str) -> float:
        """随机因子（基于用户ID的确定性随机）"""
        seed = hash(user_id + target + str(datetime.now().date())) % (2**32)
        random.seed(seed)
        return random.uniform(
            self.config["recommendation_rules"]["min_random_score"],
            self.config["recommendation_rules"]["max_random_score"]
        )
    
    def recommend(self, current_skill: str, user_id: str = "default", 
                  top_k: int = 3) -> List[Tuple[str, float, Dict]]:
        """
        推荐引擎主函数
        返回: [(skill_name, score, skill_info), ...]
        """
        if current_skill not in self.network["skills"]:
            print(f"⚠️ Skill '{current_skill}' 不在网络中")
            print(f"可用Skill: {list(self.network['skills'].keys())}")
            return []
        
        all_skills = [s for s in self.network["skills"].keys() if s != current_skill]
        results = []
        
        for skill in all_skills:
            # 1. 固定关联得分
            fixed = self._get_fixed_score(current_skill, skill) * self.weights["fixed_ref"]
            
            # 2. 标签相似度得分
            tag_sim = self._calc_tag_similarity(current_skill, skill) * self.weights["tag_similarity"]
            
            # 3. 随机因子得分
            rand = self._random_factor(skill, user_id) * self.weights["random_factor"]
            
            # 4. 最终得分
            total_score = fixed + tag_sim + rand
            
            # 5. 弱关联补充（如果没有固定关联但标签匹配）
            if fixed == 0 and tag_sim > 0.3:
                total_score += tag_sim * 0.5
            
            results.append((skill, total_score, self.network["skills"][skill]))
        
        # 排序并返回TopK
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]
    
    def format_qa_recommendation(self, current_skill: str, user_id: str = "default") -> str:
        """格式化Q&A场景的Follow-up推荐"""
        recs = self.recommend(current_skill, user_id, top_k=3)
        
        if not recs:
            return ""
        
        lines = ["👇 **你可能还想了解**\n"]
        
        for i, (skill, score, info) in enumerate(recs, 1):
            if score >= 0.7:
                emoji, prefix = "🔥", "你可能还想"
            elif score >= 0.4:
                emoji, prefix = "💡", "顺带可以"
            else:
                emoji, prefix = "✨", "要不要试试"
            
            trigger = info["tags"]["triggers"][0] if info["tags"]["triggers"] else info["description"]
            lines.append(f"{i}. {emoji} {prefix}：{trigger} → **{skill}**")
        
        lines.append('\n*回复编号直接进入对应Skill，或说"换一批"刷新*')
        return "\n".join(lines)
    
    def format_document_recommendation(self, current_skill: str, user_id: str = "default") -> str:
        """格式化文档末尾的推荐模块"""
        recs = self.recommend(current_skill, user_id, top_k=3)
        
        if not recs:
            return ""
        
        lines = [
            "\n---\n",
            "💡 **OPC能力联动推荐**\n",
            f"*已完成：{current_skill}*\n\n"
        ]
        
        for i, (skill, score, info) in enumerate(recs, 1):
            pricing = info.get("pricing", "free")
            pricing_str = "免费" if pricing == "free" else f"¥{pricing.split('_')[1]}/次"
            
            if score >= 0.7:
                ref_type = "🔥 **【强关联】**"
            elif score >= 0.4:
                ref_type = "💡 **【关联】**"
            else:
                ref_type = "✨ **【探索】**"
            
            # 获取推荐原因
            reason = ""
            fixed_refs = self.network["skills"][current_skill].get("fixed_refs", [])
            for ref in fixed_refs:
                if ref["skill"] == skill:
                    reason = ref["reason"]
                    break
            if not reason:
                reason = info["description"]
            
            lines.append(f"{i}. {ref_type} **{skill}** — {reason}（{pricing_str}）")
        
        lines.append("\n*由OPC推荐引擎驱动 v1.0*")
        return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("=" * 50)
        print("OPC Skill互引推荐引擎")
        print("=" * 50)
        print("\n用法: python recommend.py <current_skill> [top_k] [user_id]")
        print("\n示例:")
        print("  python recommend.py 技术尽调")
        print("  python recommend.py 技术尽调 3")
        print("  python recommend.py 技术尽调 3 user123")
        print("\n可用Skill列表:")
        
        # 加载网络显示可用Skill
        try:
            engine = OPCRecommendationEngine()
            for i, skill in enumerate(engine.network["skills"].keys(), 1):
                print(f"  {i}. {skill}")
        except Exception as e:
            print(f"  无法加载skill_network.json: {e}")
        
        print()
        sys.exit(1)
    
    current = sys.argv[1]
    top_k = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    user_id = sys.argv[3] if len(sys.argv) > 3 else "cli_user"
    
    try:
        engine = OPCRecommendationEngine()
        
        print("=" * 60)
        print(f"OPC推荐引擎 - 当前Skill: {current}")
        print(f"用户ID: {user_id} | TopK: {top_k}")
        print("=" * 60)
        
        print("\n" + "=" * 60)
        print("📱 Q&A场景推荐（Follow-up）")
        print("=" * 60)
        print(engine.format_qa_recommendation(current, user_id))
        
        print("\n" + "=" * 60)
        print("📄 文档场景推荐（Report Footer）")
        print("=" * 60)
        print(engine.format_document_recommendation(current, user_id))
        
        print("\n" + "=" * 60)
        print("🔍 详细推荐信息")
        print("=" * 60)
        recs = engine.recommend(current, user_id, top_k)
        for i, (skill, score, info) in enumerate(recs, 1):
            print(f"\n{i}. {skill}")
            print(f"   得分: {score:.3f}")
            print(f"   定价: {info.get('pricing', 'free')}")
            print(f"   描述: {info['description']}")
            print(f"   标签: {info['tags']['domain']}")
            
    except FileNotFoundError as e:
        print(f"❌ 错误: {e}")
        print("请确保skill_network.json文件存在")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
