"""
Prompt-Router Core

核心路由引擎：
- 加载技能元数据
- 路由 Prompt 到最佳匹配技能
- 支持置信度阈值和 LLM 降级
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

# 支持直接运行和模块导入
try:
    from .tokenizer import Tokenizer
    from .scorer import Scorer
except ImportError:
    from tokenizer import Tokenizer
    from scorer import Scorer


@dataclass
class RouteResult:
    """路由结果"""
    match: Optional[Dict[str, Any]]  # 匹配的技能/工具
    score: float                      # 匹配分数
    confidence: float                 # 置信度 (0-1)
    confidence_level: str             # 置信度等级 (high/medium/low/none)
    all_matches: List[Dict]          # 所有匹配（用于调试）
    
    def to_dict(self) -> Dict:
        return asdict(self)


class PromptRouter:
    """Prompt 路由器"""
    
    def __init__(
        self,
        skills_dir: str = None,
        confidence_threshold: float = 0.6,
        high_confidence_threshold: float = 0.8,
    ):
        """
        初始化路由器
        
        Args:
            skills_dir: 技能目录路径
            confidence_threshold: 置信度阈值（低于此值降级到 LLM）
            high_confidence_threshold: 高置信度阈值（高于此值直接调用）
        """
        self.skills_dir = Path(skills_dir) if skills_dir else None
        self.confidence_threshold = confidence_threshold
        self.high_confidence_threshold = high_confidence_threshold
        
        self.tokenizer = Tokenizer()
        self.scorer = Scorer()
        
        self._targets = []  # 路由目标列表
        self._loaded = False
    
    def load_skills(self, skills_dir: str = None) -> int:
        """
        从目录加载技能元数据
        
        Args:
            skills_dir: 技能目录路径
            
        Returns:
            加载的技能数量
        """
        if skills_dir:
            self.skills_dir = Path(skills_dir)
        
        if not self.skills_dir or not self.skills_dir.exists():
            raise FileNotFoundError(f"Skills directory not found: {self.skills_dir}")
        
        self._targets = []
        
        # 遍历所有技能目录
        for skill_dir in self.skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue
            
            # 跳过隐藏目录和特殊目录
            if skill_dir.name.startswith('.') or skill_dir.name in ['tests', 'data', 'references']:
                continue
            
            # 读取 SKILL.md
            skill_md = skill_dir / 'SKILL.md'
            if not skill_md.exists():
                continue
            
            try:
                meta = self._parse_skill_md(skill_md.read_text(encoding='utf-8'))
                if meta:
                    meta['_path'] = str(skill_dir)
                    self._targets.append(meta)
            except Exception as e:
                print(f"Warning: Failed to parse {skill_md}: {e}")
        
        self._loaded = True
        return len(self._targets)
    
    def _parse_skill_md(self, content: str) -> Optional[Dict]:
        """
        解析 SKILL.md 提取元数据
        
        Args:
            content: SKILL.md 内容
            
        Returns:
            元数据字典
        """
        meta = {}
        lines = content.split('\n')
        
        # 解析 YAML frontmatter
        in_frontmatter = False
        for line in lines:
            stripped = line.strip()
            if stripped == '---':
                if not in_frontmatter:
                    in_frontmatter = True
                    continue
                else:
                    break
            
            if in_frontmatter and ':' in line:
                # 正确处理 YAML 格式
                colon_idx = line.index(':')
                key = line[:colon_idx].strip()
                value = line[colon_idx+1:].strip()
                
                # 去除引号
                value = value.strip('"\'')
                
                if key == 'name':
                    meta['name'] = value
                elif key == 'description':
                    meta['description'] = value
                elif key in ('triggers', 'trigger'):
                    # 解析触发词列表（支持中英文逗号）
                    if ',' in value or '，' in value:
                        # 先将中文逗号替换为英文逗号
                        value = value.replace('，', ',')
                        triggers = [t.strip().strip('"\'') for t in value.split(',') if t.strip()]
                    else:
                        triggers = [value.strip()]
                    meta['triggers'] = triggers
                elif key == 'keywords':
                    # 解析关键词列表（支持中英文逗号）
                    if ',' in value or '，' in value:
                        # 先将中文逗号替换为英文逗号
                        value = value.replace('，', ',')
                        keywords = [k.strip().strip('"\'') for k in value.split(',') if k.strip()]
                    else:
                        keywords = [value.strip()]
                    meta['keywords'] = keywords
        
        # 必须有 name 字段
        if 'name' not in meta:
            return None
        
        # 从描述提取关键词（如果没有显式定义）
        if 'keywords' not in meta:
            meta['keywords'] = []
        
        # 从描述提取触发词（如果没有显式定义）
        if 'triggers' not in meta and 'description' in meta:
            # 简单提取：使用描述中的词汇
            meta['triggers'] = []
        
        return meta
    
    def route(self, prompt: str, limit: int = 3) -> RouteResult:
        """
        路由 Prompt 到最佳匹配技能
        
        Args:
            prompt: 用户输入
            limit: 返回最大匹配数
            
        Returns:
            路由结果
        """
        if not self._loaded:
            raise RuntimeError("Skills not loaded. Call load_skills() first.")
        
        # 分词
        tokens = self.tokenizer.tokenize(prompt)
        
        if not tokens:
            return RouteResult(
                match=None,
                score=0.0,
                confidence=0.0,
                confidence_level='none',
                all_matches=[]
            )
        
        # 评分所有目标
        all_matches = []
        for target in self._targets:
            score = self.scorer.score(tokens, target)
            if score > 0:
                # 计算理论最高分（基于技能字段 token 数）
                # 每个字段最高得分为 1.0 * weight，总共有 4 个字段
                max_score = sum(self.scorer.field_weights.values())  # 3.0+1.5+2.0+2.5 = 9.0
                confidence = self.scorer.calculate_confidence(score, max_score)
                
                all_matches.append({
                    'target': target,
                    'score': score,
                    'confidence': confidence,
                })
        
        # 排序
        all_matches.sort(key=lambda x: -x['score'])
        
        # 限制数量
        all_matches = all_matches[:limit]
        
        # 选择最佳匹配
        if not all_matches:
            return RouteResult(
                match=None,
                score=0.0,
                confidence=0.0,
                confidence_level='none',
                all_matches=[]
            )
        
        best = all_matches[0]
        confidence_level = self.scorer.get_confidence_level(best['confidence'])
        
        # 决定是否匹配
        if best['confidence'] < self.confidence_threshold:
            # 低于阈值，不匹配
            return RouteResult(
                match=None,
                score=best['score'],
                confidence=best['confidence'],
                confidence_level='low',
                all_matches=all_matches
            )
        
        return RouteResult(
            match=best['target'],
            score=best['score'],
            confidence=best['confidence'],
            confidence_level=confidence_level,
            all_matches=all_matches
        )
    
    def should_invoke_skill(self, result: RouteResult) -> bool:
        """
        判断是否应该调用技能
        
        Args:
            result: 路由结果
            
        Returns:
            True 如果应该调用技能
        """
        return result.match is not None and result.confidence >= self.confidence_threshold
    
    def should_fallback_to_llm(self, result: RouteResult) -> bool:
        """
        判断是否应该降级到 LLM
        
        Args:
            result: 路由结果
            
        Returns:
            True 如果应该降级
        """
        return result.match is None or result.confidence < self.confidence_threshold
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            'total_targets': len(self._targets),
            'loaded': self._loaded,
            'confidence_threshold': self.confidence_threshold,
            'high_confidence_threshold': self.high_confidence_threshold,
        }


# 示例用法
if __name__ == '__main__':
    # 创建路由器
    router = PromptRouter(
        skills_dir='C:/Users/User/.openclaw/workspace/skills',
        confidence_threshold=0.3  # 降低阈值测试
    )
    
    # 加载技能
    count = router.load_skills()
    print(f"加载了 {count} 个技能")
    print()
    
    # 调试：显示加载的技能
    print("已加载技能:")
    for target in router._targets[:5]:  # 显示前 5 个
        print(f"  - {target['name']}: {target.get('description', '')[:50]}...")
    print()
    
    # 测试路由
    test_prompts = [
        "搜索 Python 教程",
        "读取 config.json 文件",
        "北京今天天气怎么样",
        "帮我写一篇文章",
        "打开浏览器访问 GitHub",
    ]
    
    for prompt in test_prompts:
        # 调试：显示分词
        tokens = router.tokenizer.tokenize(prompt)
        print(f"Prompt: {prompt}")
        print(f"  分词：{tokens}")
        
        result = router.route(prompt)
        print(f"  匹配：{result.match['name'] if result.match else 'None'}")
        print(f"  分数：{result.score:.2f}")
        print(f"  置信度：{result.confidence:.2f} ({result.confidence_level})")
        print(f"  调用技能：{router.should_invoke_skill(result)}")
        
        # 显示所有匹配
        if result.all_matches:
            print(f"  所有匹配:")
            for m in result.all_matches[:3]:
                print(f"    - {m['target']['name']}: score={m['score']:.2f}, conf={m['confidence']:.2f}")
        print()
