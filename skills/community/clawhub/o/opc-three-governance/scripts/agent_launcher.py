#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三会治理系统 - Agent启动器
负责问题分类、Agent匹配、主执行流程控制
"""

import json
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class Institution(Enum):
    """机构枚举"""
    PRIVATE_BOARD = "私董会"      # 精神领袖层
    COUNCIL = "理事会"           # 执行中枢层
    EXPERT_COMMITTEE = "专家委员会"  # 专业支撑层


class ProblemType(Enum):
    """问题类型枚举"""
    STRATEGY = "战略决策"
    OPERATION = "运营管理"
    RISK_CONTROL = "风险控制"
    TALENT = "人才发展"
    VALUE_CONFLICT = "价值观冲突"
    PRODUCT = "产品决策"
    INNOVATION = "创新突破"
    ADVERSITY = "逆境应对"
    CONCEPT = "概念澄清"
    PROFESSIONAL = "专业咨询"


@dataclass
class Agent:
    """Agent定义"""
    name: str
    institution: Institution
    skills: List[str]
    keywords: List[str]
    description: str = ""
    
    def match_score(self, problem: str, problem_type: ProblemType) -> float:
        """计算Agent与问题的匹配分数"""
        score = 0.0
        
        # 关键词匹配
        for kw in self.keywords:
            if kw in problem:
                score += 2.0
        
        # 问题类型匹配
        type_mapping = {
            ProblemType.STRATEGY: ["战略", "方向", "规划", "决策"],
            ProblemType.OPERATION: ["执行", "运营", "管理", "落地"],
            ProblemType.RISK_CONTROL: ["风险", "合规", "审计", "控制"],
            ProblemType.TALENT: ["人才", "团队", "组织", "招聘"],
            ProblemType.VALUE_CONFLICT: ["道德", "价值", "原则", "良知"],
            ProblemType.PRODUCT: ["产品", "设计", "体验", "用户"],
            ProblemType.INNOVATION: ["创新", "颠覆", "突破", "第一性"],
            ProblemType.ADVERSITY: ["困境", "逆境", "危机", "压力"],
            ProblemType.CONCEPT: ["概念", "定义", "本质", "澄清"],
            ProblemType.PROFESSIONAL: ["专业", "咨询", "分析", "建议"],
        }
        
        for kw in type_mapping.get(problem_type, []):
            if kw in problem:
                score += 1.0
        
        return score


@dataclass
class AgentRegistry:
    """Agent注册表"""
    agents: List[Agent] = field(default_factory=list)
    
    def register(self, agent: Agent):
        """注册Agent"""
        self.agents.append(agent)
    
    def find_best_match(self, problem: str, problem_type: ProblemType, 
                        institution: Optional[Institution] = None,
                        top_k: int = 3) -> List[Tuple[Agent, float]]:
        """查找最佳匹配的Agent"""
        candidates = self.agents
        
        # 按机构过滤
        if institution:
            candidates = [a for a in candidates if a.institution == institution]
        
        # 计算匹配分数
        scored = [(a, a.match_score(problem, problem_type)) for a in candidates]
        
        # 排序并返回top_k
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]


class GovernanceSystem:
    """三会治理系统主类"""
    
    def __init__(self):
        self.registry = AgentRegistry()
        self._register_agents()
    
    def _register_agents(self):
        """注册所有Agent"""
        
        # ========== 私董会9位Agent ==========
        private_board_agents = [
            Agent(
                name="王阳明",
                institution=Institution.PRIVATE_BOARD,
                skills=["心贼识别Skill", "致良知校准Skill"],
                keywords=["良知", "道德", "心学", "知行合一", "修炼", "领导力"],
                description="心学宗师，破心中贼，致良知"
            ),
            Agent(
                name="曾国藩",
                institution=Institution.PRIVATE_BOARD,
                skills=["日课自省Skill", "挺经硬扛Skill", "团队成事Skill"],
                keywords=["坚持", "长期", "团队", "成事", "拙诚", "日课"],
                description="治世能臣，拙诚有恒"
            ),
            Agent(
                name="范仲淹",
                institution=Institution.PRIVATE_BOARD,
                skills=["公忠破贼Skill", "庙堂江湖视角切换Skill"],
                keywords=["公益", "公义", "先忧后乐", "责任", "民生"],
                description="天下为先，宁鸣而死"
            ),
            Agent(
                name="苏格拉底",
                institution=Institution.PRIVATE_BOARD,
                skills=["诘问产婆术Skill", "概念澄清Skill"],
                keywords=["追问", "真理", "认识自己", "逻辑", "本质"],
                description="诘问大师，认识你自己"
            ),
            Agent(
                name="维特根斯坦",
                institution=Institution.PRIVATE_BOARD,
                skills=["语言界限勘察Skill", "践言冲突扫描Skill"],
                keywords=["语言", "概念", "边界", "清晰", "分析"],
                description="语言哲学家，划定边界"
            ),
            Agent(
                name="张小龙",
                institution=Institution.PRIVATE_BOARD,
                skills=["极简主义暴力Skill", "情感化设计Skill"],
                keywords=["产品", "极简", "用户", "体验", "简单"],
                description="产品宗师，极简主义"
            ),
            Agent(
                name="马斯克",
                institution=Institution.PRIVATE_BOARD,
                skills=["物理定律拆解Skill", "十倍目标倒逼Skill"],
                keywords=["第一性", "创新", "颠覆", "突破", "物理"],
                description="第一性思维者，颠覆式创新"
            ),
            Agent(
                name="任正非",
                institution=Institution.PRIVATE_BOARD,
                skills=["深淘滩低作堰Skill", "灰度管理Skill"],
                keywords=["灰度", "熵减", "管理", "妥协", "平衡"],
                description="熵减大师，灰度哲学"
            ),
            Agent(
                name="苏轼",
                institution=Institution.PRIVATE_BOARD,
                skills=["时空降维Skill", "审美救赎Skill"],
                keywords=["逆境", "心态", "豁达", "超越", "心安"],
                description="逆境诗人，此心安处"
            ),
        ]
        
        # ========== 理事会4位Agent ==========
        council_agents = [
            Agent(
                name="令狐冲",
                institution=Institution.COUNCIL,
                skills=["战略独孤九剑Skill", "政企破壁Skill"],
                keywords=["战略", "架构", "灵活", "信任", "政府", "关系"],
                description="理事长，战略架构师"
            ),
            Agent(
                name="诸葛亮",
                institution=Institution.COUNCIL,
                skills=["锦囊滚动规划Skill", "六步法督导Skill"],
                keywords=["规划", "执行", "落地", "督导", "制度", "流程"],
                description="常务副理事长，战略落地总工程师"
            ),
            Agent(
                name="包青天",
                institution=Institution.COUNCIL,
                skills=["利益回避虎头铡Skill", "评议会铁券Skill"],
                keywords=["合规", "审计", "利益冲突", "程序", "公正", "透明"],
                description="审计与合规理事，程序正义守门人"
            ),
            Agent(
                name="花木兰",
                institution=Institution.COUNCIL,
                skills=["木兰辞对赌Skill", "士子点将Skill"],
                keywords=["人才", "激励", "培养", "点将", "梯队", "对赌"],
                description="CHO/组织生态理事，组织引擎与人才官"
            ),
        ]
        
        # ========== 专家委员会11位Agent ==========
        expert_committee_agents = [
            # 战略宏观组
            Agent(
                name="凯文凯利",
                institution=Institution.EXPERT_COMMITTEE,
                skills=["科技预言Skill", "趋势洞察Skill"],
                keywords=["趋势", "科技", "未来", "预言", "网络", "生态"],
                description="科技预言家，未来学家"
            ),
            Agent(
                name="吴晓波",
                institution=Institution.EXPERT_COMMITTEE,
                skills=["财经观察Skill", "品牌叙事Skill"],
                keywords=["财经", "品牌", "商业史", "传播", "产业"],
                description="财经观察家，品牌传播专家"
            ),
            # 商业运营组
            Agent(
                name="刘润",
                institution=Institution.EXPERT_COMMITTEE,
                skills=["商业逻辑拆解Skill", "运营优化Skill"],
                keywords=["商业", "运营", "效率", "模式", "增长"],
                description="商业顾问，运营优化专家"
            ),
            Agent(
                name="宫玉振",
                institution=Institution.EXPERT_COMMITTEE,
                skills=["战略思维Skill", "领导力培养Skill"],
                keywords=["战略", "竞争", "军事", "领导力", "孙子兵法"],
                description="军事战略家，领导力专家"
            ),
            Agent(
                name="李叫兽",
                institution=Institution.EXPERT_COMMITTEE,
                skills=["营销策略Skill", "品牌定位Skill"],
                keywords=["营销", "品牌", "定位", "用户洞察", "内容"],
                description="营销专家，品牌定位专家"
            ),
            Agent(
                name="金枪大叔",
                institution=Institution.EXPERT_COMMITTEE,
                skills=["创意策划Skill", "文案创作Skill"],
                keywords=["创意", "广告", "文案", "传播", "叙事"],
                description="创意大师，文案创作大师"
            ),
            # 技术实现组
            Agent(
                name="安德鲁吴",
                institution=Institution.EXPERT_COMMITTEE,
                skills=["技术架构Skill", "产品设计Skill"],
                keywords=["技术", "架构", "AI", "产品", "工程"],
                description="技术架构专家，AI专家"
            ),
            Agent(
                name="詹姆斯戴森",
                institution=Institution.EXPERT_COMMITTEE,
                skills=["产品创新Skill", "工业设计Skill"],
                keywords=["创新", "设计", "产品", "工程", "制造"],
                description="创新工程师，工业设计大师"
            ),
            # 风控感知组
            Agent(
                name="罗翔",
                institution=Institution.EXPERT_COMMITTEE,
                skills=["法律咨询Skill", "合规审查Skill"],
                keywords=["法律", "合规", "风险", "法治", "程序"],
                description="法学家，法律咨询专家"
            ),
            Agent(
                name="东东枪",
                institution=Institution.EXPERT_COMMITTEE,
                skills=["内容创作Skill", "危机公关Skill"],
                keywords=["内容", "品牌", "公关", "传播", "叙事"],
                description="内容专家，危机公关专家"
            ),
            Agent(
                name="原研哉",
                institution=Institution.EXPERT_COMMITTEE,
                skills=["品牌设计Skill", "视觉传达Skill"],
                keywords=["设计", "视觉", "品牌", "美学", "用户体验"],
                description="设计师，视觉传达大师"
            ),
        ]
        
        # 注册所有Agent
        for agent in (private_board_agents + council_agents + expert_committee_agents):
            self.registry.register(agent)
    
    def classify_problem(self, problem: str) -> ProblemType:
        """问题分类"""
        problem_lower = problem.lower()
        
        type_rules = {
            ProblemType.STRATEGY: ["战略", "方向", "规划", "决策", "布局"],
            ProblemType.OPERATION: ["执行", "运营", "管理", "落地", "实施"],
            ProblemType.RISK_CONTROL: ["风险", "合规", "审计", "控制", "安全"],
            ProblemType.TALENT: ["人才", "团队", "组织", "招聘", "培养", "激励"],
            ProblemType.VALUE_CONFLICT: ["道德", "价值", "原则", "良知", "对错"],
            ProblemType.PRODUCT: ["产品", "设计", "体验", "用户", "功能"],
            ProblemType.INNOVATION: ["创新", "颠覆", "突破", "第一性", "改革"],
            ProblemType.ADVERSITY: ["困境", "逆境", "危机", "压力", "困难"],
            ProblemType.CONCEPT: ["概念", "定义", "本质", "澄清", "理解"],
            ProblemType.PROFESSIONAL: ["专业", "咨询", "分析", "建议", "方案"],
        }
        
        scores = {}
        for ptype, keywords in type_rules.items():
            score = sum(1 for kw in keywords if kw in problem_lower)
            scores[ptype] = score
        
        if max(scores.values()) == 0:
            return ProblemType.PROFESSIONAL
        
        return max(scores, key=scores.get)
    
    def determine_institution(self, problem_type: ProblemType) -> List[Institution]:
        """确定需要的机构"""
        # 问题类型到机构的映射
        mapping = {
            ProblemType.STRATEGY: [Institution.COUNCIL, Institution.PRIVATE_BOARD, Institution.EXPERT_COMMITTEE],
            ProblemType.OPERATION: [Institution.COUNCIL, Institution.EXPERT_COMMITTEE],
            ProblemType.RISK_CONTROL: [Institution.COUNCIL, Institution.EXPERT_COMMITTEE],
            ProblemType.TALENT: [Institution.COUNCIL, Institution.EXPERT_COMMITTEE],
            ProblemType.VALUE_CONFLICT: [Institution.PRIVATE_BOARD],
            ProblemType.PRODUCT: [Institution.PRIVATE_BOARD, Institution.EXPERT_COMMITTEE],
            ProblemType.INNOVATION: [Institution.PRIVATE_BOARD, Institution.EXPERT_COMMITTEE],
            ProblemType.ADVERSITY: [Institution.PRIVATE_BOARD],
            ProblemType.CONCEPT: [Institution.PRIVATE_BOARD],
            ProblemType.PROFESSIONAL: [Institution.EXPERT_COMMITTEE],
        }
        
        return mapping.get(problem_type, [Institution.EXPERT_COMMITTEE])
    
    def match_agents(self, problem: str, problem_type: ProblemType,
                      institutions: List[Institution]) -> Dict[Institution, List[Tuple[Agent, float]]]:
        """匹配Agent"""
        result = {}
        
        for inst in institutions:
            matches = self.registry.find_best_match(
                problem, problem_type, institution=inst, top_k=3
            )
            if matches:
                result[inst] = matches
        
        return result
    
    def execute(self, problem: str, background: str = "", 
                urgency: str = "中") -> Dict:
        """主执行流程"""
        
        # Step 1: 问题分类
        problem_type = self.classify_problem(problem)
        
        # Step 2: 确定需要的机构
        institutions = self.determine_institution(problem_type)
        
        # Step 3: Agent匹配
        agent_matches = self.match_agents(problem, problem_type, institutions)
        
        # Step 4: 生成执行计划
        execution_plan = self._generate_execution_plan(
            problem, problem_type, agent_matches, background, urgency
        )
        
        return {
            "问题分类": problem_type.value,
            "涉及机构": [inst.value for inst in institutions],
            "Agent匹配": {
                inst.value: [(a.name, score) for a, score in matches]
                for inst, matches in agent_matches.items()
            },
            "执行计划": execution_plan
        }
    
    def _generate_execution_plan(self, problem: str, problem_type: ProblemType,
                                  agent_matches: Dict, background: str,
                                  urgency: str) -> Dict:
        """生成执行计划"""
        
        plan = {
            "问题描述": problem,
            "背景信息": background,
            "紧急程度": urgency,
            "阶段": []
        }
        
        # 私董会视角（如果涉及）
        if Institution.PRIVATE_BOARD in agent_matches:
            pb_agents = agent_matches[Institution.PRIVATE_BOARD]
            plan["阶段"].append({
                "阶段名称": "私董会：价值观与方向审视",
                "参与Agent": [a.name for a, _ in pb_agents],
                "核心Skill": list(set(skill for a, _ in pb_agents for skill in a.skills)),
                "关注点": "价值观、方向、精神支柱"
            })
        
        # 理事会视角（如果涉及）
        if Institution.COUNCIL in agent_matches:
            council_agents = agent_matches[Institution.COUNCIL]
            plan["阶段"].append({
                "阶段名称": "理事会：战略决策与执行规划",
                "参与Agent": [a.name for a, _ in council_agents],
                "核心Skill": list(set(skill for a, _ in council_agents for skill in a.skills)),
                "关注点": "战略落地、执行方案、资源配置"
            })
        
        # 专家委员会视角（如果涉及）
        if Institution.EXPERT_COMMITTEE in agent_matches:
            ec_agents = agent_matches[Institution.EXPERT_COMMITTEE]
            plan["阶段"].append({
                "阶段名称": "专家委员会：专业分析与支撑",
                "参与Agent": [a.name for a, _ in ec_agents],
                "核心Skill": list(set(skill for a, _ in ec_agents for skill in a.skills)),
                "关注点": "专业咨询、深度分析、风险评估"
            })
        
        return plan


def main():
    """测试函数"""
    system = GovernanceSystem()
    
    # 测试用例
    test_cases = [
        {
            "problem": "公司面临重大战略转型，是继续深耕主业还是开拓新市场？",
            "background": "主业增长放缓，新市场有潜力但风险较大",
            "urgency": "高"
        },
        {
            "problem": "核心高管要离职，如何挽留并做好继任规划？",
            "background": "该高管掌握核心技术和人脉，离职会影响业务连续性",
            "urgency": "高"
        },
        {
            "problem": "产品设计如何做到既简单又有竞争力？",
            "background": "竞品功能越来越多，用户反馈产品太复杂",
            "urgency": "中"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"测试案例 {i}")
        print(f"{'='*60}")
        result = system.execute(
            problem=case["problem"],
            background=case["background"],
            urgency=case["urgency"]
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
