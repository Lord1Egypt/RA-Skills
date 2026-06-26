"""
智慧引擎 (智-Zhi)
举一反三，触类旁通

核心能力：
1. 偏好推理 — 从已知偏好推断新场景
2. 经验复用 — 过去成功/失败经验迁移
3. 模式学习 — 用户拒绝/接受的模式
4. 相似匹配 — 找相似问题及解答
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Tuple

class WisdomEngine:
    """
    智慧推理引擎
    
    "举一隅不以三隅反，则不复也" — 孔子
    
    真正的智能不只是存储，更是推理和迁移。
    """
    
    def __init__(self, data_dir: Optional[Path] = None):
        if data_dir is None:
            data_dir = Path.home() / ".mflow-memory-cn" / "wisdom"
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # 经验库：成功/失败案例
        self.experiences_file = self.data_dir / "experiences.jsonl"
        # 偏好库：用户偏好及其来源
        self.preferences_file = self.data_dir / "preferences.jsonl"
        # 拒绝模式库
        self.rejection_patterns_file = self.data_dir / "rejection_patterns.jsonl"
    
    # ========== 核心能力 ==========
    
    def learn_preference(self, user_id: str, 
                        preference: str,
                        source: str,
                        weight: float = 0.8) -> str:
        """
        学习用户偏好
        
        Args:
            user_id: 用户ID
            preference: 偏好描述（如"喜欢简洁界面"）
            source: 来源（如"直接说"、"行为推断"）
            weight: 置信权重（0-1）
            
        Returns:
            preference_id
        """
        pref_data = {
            "id": self._generate_id("pref"),
            "user_id": user_id,
            "preference": preference,
            "source": source,  # "direct" | "inferred" | "observed"
            "weight": weight,
            "examples": [],
            "confirmed_count": 0,
            "contradicted_count": 0,
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
        
        self._append_to_file(self.preferences_file, pref_data)
        return pref_data["id"]
    
    def confirm_preference(self, preference_id: str):
        """确认偏好（用户再次表现出该偏好）"""
        prefs = self._load_all_preferences()
        
        for p in prefs:
            if p["id"] == preference_id:
                p["confirmed_count"] += 1
                p["weight"] = min(1.0, p["weight"] + 0.05)  # 每次确认+0.05
                p["last_updated"] = datetime.now().isoformat()
                break
        
        self._save_all_preferences(prefs)
    
    def contradict_preference(self, preference_id: str):
        """矛盾偏好（用户表现出相反偏好）"""
        prefs = self._load_all_preferences()
        
        for p in prefs:
            if p["id"] == preference_id:
                p["contradicted_count"] += 1
                p["weight"] = max(0.1, p["weight"] - 0.15)  # 每次矛盾-0.15
                p["last_updated"] = datetime.now().isoformat()
                break
        
        self._save_all_preferences(prefs)
    
    def infer_preference(self, user_id: str, 
                        current_request: str) -> List[Dict]:
        """
        推断用户在新场景下的偏好
        
        基于历史偏好，预测当前请求的合适方案
        
        Args:
            user_id: 用户ID
            current_request: 当前请求
            
        Returns:
            推断出的偏好列表（带置信度）
        """
        prefs = self._get_user_preferences(user_id)
        
        # 关键词匹配
        inferred = []
        current_lower = current_request.lower()
        
        for pref in prefs:
            if pref["weight"] < 0.3:
                continue  # 权重太低，不采用
            
            pref_text = pref["preference"].lower()
            
            # 简单关键词匹配
            # "界面"相关
            if any(kw in current_lower for kw in ["界面", "UI", "界面", "设计"]):
                if any(kw in pref_text for kw in ["简洁", "简单", "干净", "花哨", "复杂"]):
                    inferred.append({
                        "preference": pref["preference"],
                        "weight": pref["weight"],
                        "reason": f"基于偏好'{pref['preference']}'推断"
                    })
            
            # "工具"相关
            if any(kw in current_lower for kw in ["工具", "软件", "安装", "配置"]):
                if any(kw in pref_text for kw in ["简单", "免安装", "一键", "复杂", "麻烦"]):
                    inferred.append({
                        "preference": pref["preference"],
                        "weight": pref["weight"],
                        "reason": f"基于偏好'{pref['preference']}'推断"
                    })
            
            # "时间"相关
            if any(kw in current_lower for kw in ["快速", "效率", "慢", "快"]):
                if any(kw in pref_text for kw in ["效率", "快", "慢", "简单"]):
                    inferred.append({
                        "preference": pref["preference"],
                        "weight": pref["weight"],
                        "reason": f"基于偏好'{pref['preference']}'推断"
                    })
        
        # 按权重排序
        inferred.sort(key=lambda x: x["weight"], reverse=True)
        return inferred[:5]  # 返回top5
    
    def record_experience(self, user_id: str,
                         experience_type: str,  # "success" | "failure"
                         situation: str,
                         action: str,
                         outcome: str) -> str:
        """
        记录一次经验
        
        用于未来类似场景的参考
        """
        exp_data = {
            "id": self._generate_id("exp"),
            "user_id": user_id,
            "type": experience_type,
            "situation": situation,  # 什么情况
            "action": action,        # 做了什么
            "outcome": outcome,     # 结果如何
            "use_count": 0,
            "created_at": datetime.now().isoformat()
        }
        
        self._append_to_file(self.experiences_file, exp_data)
        return exp_data["id"]
    
    def find_similar_experiences(self, user_id: str,
                                current_situation: str,
                                limit: int = 3) -> List[Dict]:
        """
        找相似经验
        
        用于类比推理
        """
        experiences = self._get_user_experiences(user_id)
        
        scored = []
        current_lower = current_situation.lower()
        
        for exp in experiences:
            situation = exp.get("situation", "").lower()
            
            # 简单相似度：共同关键词数量
            current_words = set(current_lower.split())
            situation_words = set(situation.split())
            
            common = current_words & situation_words
            if common:
                score = len(common) / max(len(current_words), len(situation_words))
                scored.append((score, exp))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        return [exp for _, exp in scored[:limit]]
    
    def learn_rejection_pattern(self, user_id: str,
                               rejection_text: str,
                               context: Optional[str] = None):
        """
        学习用户的拒绝模式
        
        记录用户拒绝某事时的典型表达，
        用于未来预判和避免
        """
        pattern_data = {
            "id": self._generate_id("rej"),
            "user_id": user_id,
            "rejection_text": rejection_text,
            "context": context,
            "count": 1,
            "created_at": datetime.now().isoformat()
        }
        
        # 检查是否已存在
        patterns = self._load_all_patterns()
        found = False
        for p in patterns:
            if p["user_id"] == user_id and p["rejection_text"] == rejection_text:
                p["count"] += 1
                found = True
                break
        
        if not found:
            patterns.append(pattern_data)
        
        self._save_all_patterns(patterns)
    
    def predict_rejection(self, user_id: str,
                         proposed_action: str) -> Tuple[bool, str]:
        """
        预测用户是否会拒绝某个提议
        
        基于历史拒绝模式
        """
        patterns = self._get_user_patterns(user_id)
        action_lower = proposed_action.lower()
        
        # 检查危险信号
        danger_signals = []
        
        for p in patterns:
            rejection = p["rejection_text"].lower()
            
            # 简单匹配
            if any(word in action_lower for word in rejection.split()[:3]):
                if p["count"] >= 2:  # 至少被拒绝2次
                    danger_signals.append(f"类似表达'{rejection}'被拒绝{p['count']}次")
        
        if danger_signals:
            return True, "; ".join(danger_signals)
        
        return False, "未发现明显拒绝风险"
    
    def get_wisdom_summary(self, user_id: str) -> Dict:
        """
        获取智慧摘要
        
        总结该用户的所有智慧学习成果
        """
        prefs = self._get_user_preferences(user_id)
        experiences = self._get_user_experiences(user_id)
        patterns = self._get_user_patterns(user_id)
        
        # 高权重偏好
        high_weight_prefs = [p for p in prefs if p["weight"] >= 0.6]
        
        # 成功经验
        success_exp = [e for e in experiences if e["type"] == "success"]
        
        # 常见拒绝
        common_rejections = sorted(patterns, key=lambda x: x["count"], reverse=True)[:5]
        
        return {
            "user_id": user_id,
            "total_preferences": len(prefs),
            "high_weight_preferences": high_weight_prefs,
            "total_experiences": len(experiences),
            "success_experiences": success_exp,
            "total_rejection_patterns": len(patterns),
            "common_rejections": common_rejections,
            "summary": self._generate_wisdom_text(user_id, high_weight_prefs, success_exp, common_rejections)
        }
    
    # ========== 私有方法 ==========
    
    def _get_user_preferences(self, user_id: str) -> List[Dict]:
        """获取用户偏好"""
        if not self.preferences_file.exists():
            return []
        
        prefs = []
        with open(self.preferences_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    p = json.loads(line)
                    if p.get("user_id") == user_id:
                        prefs.append(p)
                except:
                    continue
        return prefs
    
    def _get_user_experiences(self, user_id: str) -> List[Dict]:
        """获取用户经验"""
        if not self.experiences_file.exists():
            return []
        
        exps = []
        with open(self.experiences_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    e = json.loads(line)
                    if e.get("user_id") == user_id:
                        exps.append(e)
                except:
                    continue
        return exps
    
    def _get_user_patterns(self, user_id: str) -> List[Dict]:
        """获取用户拒绝模式"""
        patterns = self._load_all_patterns()
        return [p for p in patterns if p.get("user_id") == user_id]
    
    def _load_all_patterns(self) -> List[Dict]:
        """加载所有拒绝模式"""
        if not self.rejection_patterns_file.exists():
            return []
        
        patterns = []
        with open(self.rejection_patterns_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    patterns.append(json.loads(line))
                except:
                    continue
        return patterns
    
    def _save_all_patterns(self, patterns: List[Dict]):
        """保存所有拒绝模式"""
        with open(self.rejection_patterns_file, 'w', encoding='utf-8') as f:
            for p in patterns:
                f.write(json.dumps(p, ensure_ascii=False) + '\n')
    
    def _save_all_preferences(self, prefs: List[Dict]):
        """保存所有偏好"""
        with open(self.preferences_file, 'w', encoding='utf-8') as f:
            for p in prefs:
                f.write(json.dumps(p, ensure_ascii=False) + '\n')
    
    def _append_to_file(self, filepath: Path, data: Dict):
        """追加到文件"""
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False) + '\n')
    
    def _generate_id(self, prefix: str) -> str:
        """生成唯一ID"""
        import uuid
        return f"{prefix}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:4]}"
    
    def _generate_wisdom_text(self, user_id: str,
                             prefs: List[Dict],
                             successes: List[Dict],
                             rejections: List[Dict]) -> str:
        """生成智慧摘要文本"""
        lines = [f"=== {user_id} 的智慧档案 ==="]
        
        if prefs:
            lines.append("\n【已知偏好】（高权重）：")
            for p in prefs[:5]:
                lines.append(f"  - {p['preference']} (置信度:{p['weight']:.0%})")
        
        if successes:
            lines.append("\n【成功经验】：")
            for e in successes[:3]:
                lines.append(f"  - {e['situation'][:30]}... → {e['outcome'][:30]}...")
        
        if rejections:
            lines.append("\n【避免触发】：")
            for r in rejections:
                lines.append(f"  - 别说\"{r['rejection_text'][:20]}...\"（被拒{r['count']}次）")
        
        return "\n".join(lines)
