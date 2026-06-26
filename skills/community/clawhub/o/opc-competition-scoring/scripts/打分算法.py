#!/usr/bin/env python3
"""
打分算法模块
胡田-OPC导师-大赛标准化打分.Skill
"""

import re
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass


@dataclass
class ScoreItem:
    """评分项"""
    name: str
    max_score: float
    actual_score: float
    keywords: List[str]
    deductions: List[str]


@dataclass
class DimensionScore:
    """维度评分"""
    name: str
    items: List[ScoreItem]
    total_score: float
    max_score: float
    
    @property
    def percentage(self) -> float:
        return (self.total_score / self.max_score * 100) if self.max_score > 0 else 0


class ScoringAlgorithm:
    """评分算法"""
    
    def __init__(self, weights: Dict[str, float] = None):
        self.weights = weights or {
            "team": 20,
            "market": 20,
            "innovation": 20,
            "business": 20,
            "legal_finance": 20
        }
        
    def calculate_score(self, content: str, structure: Dict) -> Dict[str, Any]:
        """计算总分"""
        results = {}
        
        results["team"] = self._score_team(content, structure)
        results["market"] = self._score_market(content, structure)
        results["innovation"] = self._score_innovation(content, structure)
        results["business"] = self._score_business(content, structure)
        results["legal_finance"] = self._score_legal_finance(content, structure)
        
        results["total"] = sum(r.total_score for r in results.values())
        results["details"] = {k: self._format_dimension(v) for k, v in results.items() if k != "total"}
        
        return results
    
    def _format_dimension(self, dim: DimensionScore) -> Dict:
        """格式化维度评分"""
        return {
            "name": dim.name,
            "score": dim.total_score,
            "max": dim.max_score,
            "percentage": dim.percentage,
            "items": [
                {
                    "name": item.name,
                    "score": item.actual_score,
                    "max": item.max_score,
                    "deductions": item.deductions
                }
                for item in dim.items
            ]
        }
    
    def _create_dimension(self, name: str, items: List[ScoreItem]) -> DimensionScore:
        """创建维度"""
        total = sum(item.actual_score for item in items)
        max_score = sum(item.max_score for item in items)
        return DimensionScore(name=name, items=items, total_score=total, max_score=max_score)
    
    def _score_team(self, content: str, structure: Dict) -> DimensionScore:
        """团队维度评分"""
        items = []
        
        # 创始人背景
        score, deductions = self._evaluate_founder(content)
        items.append(ScoreItem("创始人背景", 6, score, [], deductions))
        
        # 团队完整性
        score, deductions = self._evaluate_team_completeness(content)
        items.append(ScoreItem("团队完整性", 5, score, [], deductions))
        
        # 团队互补性
        score, deductions = self._evaluate_team_synergy(content)
        items.append(ScoreItem("团队互补性", 5, score, [], deductions))
        
        # 股权结构
        score, deductions = self._evaluate_equity(content)
        items.append(ScoreItem("股权结构", 4, score, [], deductions))
        
        return self._create_dimension("团队维度", items)
    
    def _evaluate_founder(self, content: str) -> Tuple[float, List[str]]:
        """评估创始人"""
        score = 0
        deductions = []
        
        # 学历
        if re.search(r"(博士|硕士|985|211|海归|名校)", content):
            score += 2
        else:
            deductions.append("学历背景描述不足")
            
        # 经验
        if re.search(r"\d+年(行业|技术|产品|运营)经验", content):
            score += 2
        elif re.search(r"(经验|经历|背景)", content):
            score += 1
            deductions.append("经验描述不够具体")
            
        # 成就
        if re.search(r"(成功|退出|收购|上市|高管|负责人)", content):
            score += 2
            
        return min(score, 6), deductions
    
    def _evaluate_team_completeness(self, content: str) -> Tuple[float, List[str]]:
        """评估团队完整性"""
        score = 0
        deductions = []
        
        roles = {
            "技术": ["技术", "CTO", "研发", "开发"],
            "产品": ["产品", "PM", "设计"],
            "市场": ["市场", "销售", "BD"],
            "运营": ["运营", "客服"]
        }
        
        found = 0
        for role, keywords in roles.items():
            if any(kw in content for kw in keywords):
                found += 1
                score += 1.5
        
        if found < 3:
            deductions.append(f"核心岗位缺失，仅覆盖{found}个岗位")
            
        if found < 2:
            score = 1
            
        return min(score, 5), deductions
    
    def _evaluate_team_synergy(self, content: str) -> Tuple[float, List[str]]:
        """评估团队互补性"""
        score = 3  # 基础分
        deductions = []
        
        # 检查互补性描述
        if re.search(r"(互补|协同|配合|资源)", content):
            score += 2
        else:
            deductions.append("团队互补性描述不足")
            
        return min(score, 5), deductions
    
    def _evaluate_equity(self, content: str) -> Tuple[float, List[str]]:
        """评估股权结构"""
        score = 0
        deductions = []
        
        if "股权" in content or "期权" in content:
            score += 1
            
        if "期权池" in content:
            score += 1
            
        # 检查股权集中度
        founder_share = re.search(r"创始人.*?(\d+)%", content)
        if founder_share:
            share = int(founder_share.group(1))
            if share > 80:
                deductions.append("创始人持股过高，可能影响团队稳定性")
                score -= 1
                
        return max(score, 0), deductions
    
    def _score_market(self, content: str, structure: Dict) -> DimensionScore:
        """市场维度评分"""
        items = []
        
        # 市场规模
        score, deductions = self._evaluate_market_size(content)
        items.append(ScoreItem("市场规模", 5, score, [], deductions))
        
        # 市场增速
        score, deductions = self._evaluate_market_growth(content)
        items.append(ScoreItem("市场增速", 4, score, [], deductions))
        
        # 痛点精准度
        score, deductions = self._evaluate_pain_point(content)
        items.append(ScoreItem("痛点精准度", 6, score, [], deductions))
        
        # 用户清晰度
        score, deductions = self._evaluate_user_clarity(content)
        items.append(ScoreItem("用户清晰度", 5, score, [], deductions))
        
        return self._create_dimension("市场维度", items)
    
    def _evaluate_market_size(self, content: str) -> Tuple[float, List[str]]:
        """评估市场规模"""
        score = 0
        deductions = []
        
        # TAM/SAM/SOM
        if re.search(r"TAM|SAM|SOM", content, re.IGNORECASE):
            score += 2
            
        # 具体数字
        if re.search(r"\d+[亿万]元", content):
            score += 2
            
        # 数据来源
        if re.search(r"(数据来源|艾瑞|罗兰贝格|IDC| Gartner)", content):
            score += 1
        else:
            deductions.append("市场规模数据来源不明确")
            
        return min(score, 5), deductions
    
    def _evaluate_market_growth(self, content: str) -> Tuple[float, List[str]]:
        """评估市场增速"""
        score = 0
        deductions = []
        
        if re.search(r"\d+%|[一二三四]成", content):
            score += 2
            
        if re.search(r"(增长|增速|趋势)", content):
            score += 2
        else:
            deductions.append("未说明市场增速")
            
        return min(score, 4), deductions
    
    def _evaluate_pain_point(self, content: str) -> Tuple[float, List[str]]:
        """评估痛点"""
        score = 0
        deductions = []
        
        if re.search(r"痛点|需求|问题", content):
            score += 2
            
        if re.search(r"(刚需|高频|迫切)", content):
            score += 2
            
        if re.search(r"(验证|访谈|调研)", content):
            score += 2
        else:
            deductions.append("痛点未经验证")
            
        return min(score, 6), deductions
    
    def _evaluate_user_clarity(self, content: str) -> Tuple[float, List[str]]:
        """评估用户清晰度"""
        score = 0
        deductions = []
        
        if re.search(r"用户画像|目标用户|画像", content):
            score += 2
            
        if re.search(r"(企业|个人|行业)", content):
            score += 1
            
        if "所有人" in content:
            deductions.append("目标用户过于宽泛")
            score -= 1
            
        if re.search(r"\d+岁|\d+人|\d+万", content):
            score += 2
            
        return max(min(score, 5), 0), deductions
    
    def _score_innovation(self, content: str, structure: Dict) -> DimensionScore:
        """创新维度评分"""
        items = []
        
        # 技术创新度
        score, deductions = self._evaluate_tech_innovation(content)
        items.append(ScoreItem("技术创新度", 6, score, [], deductions))
        
        # 模式创新度
        score, deductions = self._evaluate_business_model(content)
        items.append(ScoreItem("模式创新度", 5, score, [], deductions))
        
        # 差异化竞争力
        score, deductions = self._evaluate_differentiation(content)
        items.append(ScoreItem("差异化竞争力", 5, score, [], deductions))
        
        # 竞品对比
        score, deductions = self._evaluate_competition(content)
        items.append(ScoreItem("竞品对比", 4, score, [], deductions))
        
        return self._create_dimension("创新维度", items)
    
    def _evaluate_tech_innovation(self, content: str) -> Tuple[float, List[str]]:
        """评估技术创新"""
        score = 0
        deductions = []
        
        if re.search(r"专利|发明|软著", content):
            score += 2
            
        if re.search(r"(技术|研发|壁垒)", content):
            score += 2
            
        if re.search(r"(领先|突破|创新)", content):
            score += 2
        else:
            deductions.append("技术创新点描述不够突出")
            
        return min(score, 6), deductions
    
    def _evaluate_business_model(self, content: str) -> Tuple[float, List[str]]:
        """评估商业模式"""
        score = 0
        deductions = []
        
        if re.search(r"商业模式|盈利模式|收入来源", content):
            score += 2
            
        if re.search(r"(收费|付费|订阅|广告)", content):
            score += 2
            
        if "创新" in content:
            score += 1
        else:
            deductions.append("模式创新性描述不足")
            
        return min(score, 5), deductions
    
    def _evaluate_differentiation(self, content: str) -> Tuple[float, List[str]]:
        """评估差异化"""
        score = 3
        deductions = []
        
        if re.search(r"差异化|优势|特点", content):
            score += 2
        else:
            deductions.append("差异化描述不足")
            
        return min(score, 5), deductions
    
    def _evaluate_competition(self, content: str) -> Tuple[float, List[str]]:
        """评估竞品"""
        score = 0
        deductions = []
        
        if re.search(r"竞品|竞争|对手|对比", content):
            score += 2
        else:
            deductions.append("缺少竞品分析")
            
        if re.search(r"(优势|劣势|差异)", content):
            score += 2
            
        return min(score, 4), deductions
    
    def _score_business(self, content: str, structure: Dict) -> DimensionScore:
        """商业可行性评分"""
        items = []
        
        # 产品成熟度
        score, deductions = self._evaluate_product_maturity(content)
        items.append(ScoreItem("产品成熟度", 6, score, [], deductions))
        
        # 盈利模式
        score, deductions = self._evaluate_profit_model(content)
        items.append(ScoreItem("盈利模式", 5, score, [], deductions))
        
        # 获客路径
        score, deductions = self._evaluate_acquisition_path(content)
        items.append(ScoreItem("获客路径", 5, score, [], deductions))
        
        # 现金流规划
        score, deductions = self._evaluate_cash_flow(content)
        items.append(ScoreItem("现金流规划", 4, score, [], deductions))
        
        return self._create_dimension("商业可行性", items)
    
    def _evaluate_product_maturity(self, content: str) -> Tuple[float, List[str]]:
        """评估产品成熟度"""
        score = 0
        deductions = []
        
        if re.search(r"上线|MVP|正式版|产品", content):
            score += 2
            
        if re.search(r"\d+用户|\d+客户|付费", content):
            score += 2
            
        if re.search(r"(验证|测试|迭代)", content):
            score += 2
        else:
            deductions.append("产品验证描述不足")
            
        return min(score, 6), deductions
    
    def _evaluate_profit_model(self, content: str) -> Tuple[float, List[str]]:
        """评估盈利模式"""
        score = 0
        deductions = []
        
        if re.search(r"盈利|收入|变现", content):
            score += 2
            
        if re.search(r"(定价|收费|订阅)", content):
            score += 2
            
        if "模式" in content:
            score += 1
        else:
            deductions.append("盈利模式不够清晰")
            
        return min(score, 5), deductions
    
    def _evaluate_acquisition_path(self, content: str) -> Tuple[float, List[str]]:
        """评估获客路径"""
        score = 0
        deductions = []
        
        if re.search(r"获客|推广|渠道|获客", content):
            score += 2
            
        if re.search(r"(SEO|SEM|内容|社交)", content):
            score += 2
        else:
            deductions.append("获客策略不够具体")
            
        return min(score, 5), deductions
    
    def _evaluate_cash_flow(self, content: str) -> Tuple[float, List[str]]:
        """评估现金流"""
        score = 0
        deductions = []
        
        if re.search(r"融资|资金|预算", content):
            score += 2
            
        if re.search(r"(使用|用途|计划)", content):
            score += 2
        else:
            deductions.append("资金使用计划不够详细")
            
        return min(score, 4), deductions
    
    def _score_legal_finance(self, content: str, structure: Dict) -> DimensionScore:
        """法务财务评分"""
        items = []
        
        # 财务真实性
        score, deductions = self._evaluate_financial_truth(content)
        items.append(ScoreItem("财务真实性", 6, score, [], deductions))
        
        # 融资需求
        score, deductions = self._evaluate_funding_needs(content)
        items.append(ScoreItem("融资需求", 5, score, [], deductions))
        
        # 估值合理性
        score, deductions = self._evaluate_valuation(content)
        items.append(ScoreItem("估值合理性", 5, score, [], deductions))
        
        # 法律风险
        score, deductions = self._evaluate_legal_risk(content)
        items.append(ScoreItem("法律风险", 4, score, [], deductions))
        
        return self._create_dimension("法务财务", items)
    
    def _evaluate_financial_truth(self, content: str) -> Tuple[float, List[str]]:
        """评估财务真实性"""
        score = 0
        deductions = []
        
        if re.search(r"(收入|成本|利润|财务)", content):
            score += 2
            
        if re.search(r"\d+万|\d+亿", content):
            score += 2
            
        if re.search(r"(预测|计划|目标)", content):
            score += 2
        else:
            deductions.append("财务预测数据不足")
            
        return min(score, 6), deductions
    
    def _evaluate_funding_needs(self, content: str) -> Tuple[float, List[str]]:
        """评估融资需求"""
        score = 0
        deductions = []
        
        if re.search(r"融资|投资|轮次", content):
            score += 2
            
        if re.search(r"\d+万|\d+亿", content):
            score += 2
            
        if re.search(r"(用途|计划)", content):
            score += 1
        else:
            deductions.append("融资用途说明不足")
            
        return min(score, 5), deductions
    
    def _evaluate_valuation(self, content: str) -> Tuple[float, List[str]]:
        """评估估值"""
        score = 0
        deductions = []
        
        if "估值" in content:
            score += 2
            
        if re.search(r"(合理|对标|参考)", content):
            score += 2
        else:
            deductions.append("估值依据说明不足")
            
        return min(score, 5), deductions
    
    def _evaluate_legal_risk(self, content: str) -> Tuple[float, List[str]]:
        """评估法律风险"""
        score = 0
        deductions = []
        
        if re.search(r"(合规|资质|许可)", content):
            score += 1
            
        if re.search(r"(股权|期权|协议)", content):
            score += 1
            
        if re.search(r"(风险|控制)", content):
            score += 2
        else:
            deductions.append("风险控制意识不足")
            
        return min(score, 4), deductions


class CrossValidator:
    """交叉验证器"""
    
    def validate(self, content: str, scores: Dict) -> List[Dict]:
        """验证一致性"""
        issues = []
        
        # 数据一致性检查
        issues.extend(self._check_number_consistency(content))
        
        # 时间线检查
        issues.extend(self._check_timeline(content))
        
        # 逻辑检查
        issues.extend(self._check_logic(content))
        
        return issues
    
    def _check_number_consistency(self, content: str) -> List[Dict]:
        """检查数字一致性"""
        issues = []
        
        # 提取所有数字
        numbers = re.findall(r"\d+[亿万]元|\d+%|\d+用户|\d+客户", content)
        
        # 检查是否有重复但不同的数字描述同一事物
        # 简化检查：查找可能的矛盾
        if "500亿" in content and "300亿" in content:
            if "市场规模" in content:
                issues.append({
                    "type": "数据矛盾",
                    "severity": "high",
                    "description": "市场规模在不同位置出现不同数值",
                    "suggestion": "核实并统一市场规模数据"
                })
                
        return issues
    
    def _check_timeline(self, content: str) -> List[Dict]:
        """检查时间线"""
        issues = []
        
        # 提取年份
        years = re.findall(r"20\d{2}", content)
        years = list(set(years))
        
        if len(years) > 1 and sorted(years) != years:
            issues.append({
                "type": "时间线问题",
                "severity": "medium",
                "description": f"时间顺序可能有问题: {years}",
                "suggestion": "检查各事件的时间顺序"
            })
            
        return issues
    
    def _check_logic(self, content: str) -> List[Dict]:
        """检查逻辑"""
        issues = []
        
        # 检查明显矛盾
        if "已有10万用户" in content and "从0开始获客" in content:
            issues.append({
                "type": "逻辑矛盾",
                "severity": "high",
                "description": "声称已有用户但计划从0获客",
                "suggestion": "澄清用户数据和获客计划"
            })
            
        return issues
