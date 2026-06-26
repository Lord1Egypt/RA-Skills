"""
Prompt-Router Scorer

评分算法：计算 Prompt 与技能/工具的匹配度
- 多字段匹配（名称、描述、关键词）
- 加权评分
- 置信度计算
"""

from typing import Dict, List, Any
# 支持直接运行和模块导入
try:
    from .tokenizer import Tokenizer
except ImportError:
    from tokenizer import Tokenizer


class Scorer:
    """技能匹配评分器"""
    
    def __init__(self):
        self.tokenizer = Tokenizer()
        
        # 字段权重
        self.field_weights = {
            'name': 3.0,          # 名称匹配权重最高
            'description': 1.5,   # 描述次之
            'keywords': 2.0,      # 关键词权重高
            'triggers': 2.5,      # 触发词权重高
        }
    
    def score(self, tokens: set, target: Dict[str, Any]) -> float:
        """
        计算 Prompt 与目标的匹配分数
        
        Args:
            tokens: Prompt 分词集合
            target: 技能/工具元数据
            
        Returns:
            匹配分数（0-无穷，越高越匹配）
        """
        total_score = 0.0
        
        # 名称匹配
        if 'name' in target:
            name_tokens = self.tokenizer.tokenize(target['name'])
            name_score = self._calculate_field_score(tokens, name_tokens)
            total_score += name_score * self.field_weights['name']
        
        # 描述匹配
        if 'description' in target:
            desc_tokens = self.tokenizer.tokenize(target['description'])
            desc_score = self._calculate_field_score(tokens, desc_tokens)
            total_score += desc_score * self.field_weights['description']
        
        # 关键词匹配
        if 'keywords' in target:
            keyword_tokens = set()
            for kw in target['keywords']:
                keyword_tokens.update(self.tokenizer.tokenize(kw))
            keyword_score = self._calculate_field_score(tokens, keyword_tokens)
            total_score += keyword_score * self.field_weights['keywords']
        
        # 触发词匹配
        if 'triggers' in target:
            trigger_tokens = set()
            for trigger in target['triggers']:
                trigger_tokens.update(self.tokenizer.tokenize(trigger))
            trigger_score = self._calculate_field_score(tokens, trigger_tokens)
            total_score += trigger_score * self.field_weights['triggers']
        
        return total_score
    
    def _calculate_field_score(self, prompt_tokens: set, field_tokens: set) -> float:
        """
        计算单个字段的匹配分数
        
        策略：
        - triggers: 只要匹配 1 个就给高分（0.8+），每多匹配一个增加
        - 其他字段：使用 Dice 系数（更平衡）
        
        Args:
            prompt_tokens: Prompt 分词
            field_tokens: 字段分词
            
        Returns:
            匹配分数（0-1）
        """
        if not field_tokens:
            return 0.0
        
        # 计算交集
        intersection = prompt_tokens & field_tokens
        
        if not intersection:
            return 0.0
        
        # 对于 triggers 字段：只要匹配 1 个就给高分
        # 因为 triggers 是精心设计的触发词
        if len(field_tokens) <= 10:  # 短字段（如 triggers）
            # 匹配 1 个：0.7, 2 个：0.85, 3 个+：0.95
            match_count = len(intersection)
            if match_count == 1:
                return 0.7
            elif match_count == 2:
                return 0.85
            else:
                return 0.95
        
        # 对于长字段（description, keywords）：使用 Dice 系数
        # Dice = 2 * |A ∩ B| / (|A| + |B|)
        dice_score = 2 * len(intersection) / (len(prompt_tokens) + len(field_tokens))
        return min(1.0, dice_score)
    
    def calculate_confidence(self, score: float, max_possible_score: float) -> float:
        """
        计算置信度（归一化到 0-1）
        
        Args:
            score: 实际分数
            max_possible_score: 理论最高分数
            
        Returns:
            置信度（0-1）
        """
        if max_possible_score == 0:
            return 0.0
        return min(1.0, score / max_possible_score)
    
    def get_confidence_level(self, confidence: float) -> str:
        """
        将置信度转换为等级
        
        Args:
            confidence: 置信度（0-1）
            
        Returns:
            等级字符串
        """
        if confidence >= 0.8:
            return 'high'
        elif confidence >= 0.5:
            return 'medium'
        elif confidence >= 0.3:
            return 'low'
        else:
            return 'none'


# 示例用法
if __name__ == '__main__':
    scorer = Scorer()
    
    # 测试技能元数据
    skill = {
        'name': 'multi-search-engine',
        'description': 'Multi search engine integration with 17 engines',
        'keywords': ['搜索', 'search', '引擎', 'engine'],
        'triggers': ['搜索', '查找', 'search', 'find'],
    }
    
    # 测试 Prompt
    prompts = [
        "搜索 Python 教程",
        "查找资料",
        "读取文件",
        "北京天气",
    ]
    
    for prompt in prompts:
        tokens = scorer.tokenizer.tokenize(prompt)
        score = scorer.score(tokens, skill)
        confidence = scorer.calculate_confidence(score, max_possible_score=10.0)
        level = scorer.get_confidence_level(confidence)
        
        print(f"Prompt: {prompt}")
        print(f"  分词：{tokens}")
        print(f"  分数：{score:.2f}")
        print(f"  置信度：{confidence:.2f} ({level})")
        print()
