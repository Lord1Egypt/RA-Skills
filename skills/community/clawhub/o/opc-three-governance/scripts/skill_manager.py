#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三会治理系统 - 技能管理器
负责技能注册、查找、组合、执行调度
"""

import json
import re
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class SkillCategory(Enum):
    """技能分类"""
    PRIVATE_BOARD = "私董会技能"
    COUNCIL = "理事会技能"
    EXPERT_COMMITTEE = "专家委员会技能"
    COMMON = "通用技能"


@dataclass
class SkillParameter:
    """技能参数定义"""
    name: str
    description: str
    param_type: str  # string, number, boolean, array, object
    required: bool = True
    default: Any = None


@dataclass
class Skill:
    """技能定义"""
    id: str
    name: str
    category: SkillCategory
    owner_agent: str  # 所属Agent
    description: str
    trigger_conditions: List[str]  # 触发条件
    input_params: List[SkillParameter] = field(default_factory=list)
    output_format: str = ""
    reference_file: str = ""  # 知识蒸馏文件路径
    execute_func: Optional[Callable] = None
    
    def match_trigger(self, query: str) -> float:
        """计算技能与查询的匹配度"""
        query_lower = query.lower()
        score = 0.0
        
        for condition in self.trigger_conditions:
            if condition in query_lower:
                score += 1.0
        
        # 名称匹配
        if self.name.lower() in query_lower:
            score += 2.0
        
        return score
    
    def validate_input(self, params: Dict) -> tuple[bool, str]:
        """验证输入参数"""
        for param_def in self.input_params:
            if param_def.required and param_def.name not in params:
                return False, f"缺少必需参数: {param_def.name}"
            
            if param_def.name in params:
                actual_type = type(params[param_def.name]).__name__
                expected_type = param_def.param_type
                
                # 类型检查（简化版）
                type_mapping = {
                    "string": str,
                    "number": (int, float),
                    "boolean": bool,
                    "array": list,
                    "object": dict,
                }
                
                expected_python_type = type_mapping.get(expected_type)
                if expected_python_type and not isinstance(
                    params[param_def.name], expected_python_type
                ):
                    return False, f"参数 {param_def.name} 类型错误，期望 {expected_type}"
        
        return True, ""


class SkillManager:
    """技能管理器"""
    
    def __init__(self):
        self.skills: Dict[str, Skill] = {}
        self.agent_skills: Dict[str, List[str]] = {}  # Agent -> 技能ID列表
        self.category_skills: Dict[SkillCategory, List[str]] = {}
        self._register_default_skills()
    
    def _register_default_skills(self):
        """注册默认技能库"""
        
        # ========== 私董会技能 ==========
        self.register_skill(Skill(
            id="sibodahui_wangyangming_1",
            name="心贼识别Skill",
            category=SkillCategory.PRIVATE_BOARD,
            owner_agent="王阳明",
            description="识别内心私欲、杂念和偏见的方法论",
            trigger_conditions=["良知", "道德", "心贼", "私欲", "修炼", "领导力"],
            input_params=[
                SkillParameter("问题描述", "需要检验的具体问题或决定", "string"),
                SkillParameter("选项列表", "可选方案列表", "array", required=False),
            ],
            output_format="JSON",
            reference_file="references/sibodahui_9agents.md"
        ))
        
        self.register_skill(Skill(
            id="sibodahui_wangyangming_2",
            name="致良知校准Skill",
            category=SkillCategory.PRIVATE_BOARD,
            owner_agent="王阳明",
            description="用良知检验决策和行为的方法论",
            trigger_conditions=["致良知", "知行合一", "良知判断", "道德准则"],
            input_params=[
                SkillParameter("行为描述", "需要校准的行为或决定", "string"),
                SkillParameter("利益相关方", "涉及的各方", "array", required=False),
            ],
            output_format="JSON",
            reference_file="references/sibodahui_9agents.md"
        ))
        
        self.register_skill(Skill(
            id="sibodahui_zengguofan_1",
            name="日课自省Skill",
            category=SkillCategory.PRIVATE_BOARD,
            owner_agent="曾国藩",
            description="每日自我监督与改进的系统方法",
            trigger_conditions=["日课", "自省", "坚持", "习惯", "修炼"],
            input_params=[
                SkillParameter("周期", "复盘周期：日/周/月", "string"),
                SkillParameter("关注领域", "需要复盘的领域", "array"),
            ],
            output_format="JSON",
            reference_file="references/sibodahui_9agents.md"
        ))
        
        self.register_skill(Skill(
            id="sibodahui_zengguofan_2",
            name="挺经硬扛Skill",
            category=SkillCategory.PRIVATE_BOARD,
            owner_agent="曾国藩",
            description="在逆境中坚持和突破的方法论",
            trigger_conditions=["逆境", "困难", "坚持", "挺过", "困境"],
            input_params=[
                SkillParameter("困境描述", "当前面临的困难", "string"),
                SkillParameter("资源状况", "可调配的资源", "object", required=False),
            ],
            output_format="JSON",
            reference_file="references/sibodahui_9agents.md"
        ))
        
        self.register_skill(Skill(
            id="sibodahui_zengguofan_3",
            name="团队成事Skill",
            category=SkillCategory.PRIVATE_BOARD,
            owner_agent="曾国藩",
            description="打造高效团队、共同成就事业的方法论",
            trigger_conditions=["团队", "成事", "合作", "利他", "共事"],
            input_params=[
                SkillParameter("团队目标", "需要达成的目标", "string"),
                SkillParameter("团队成员", "成员特点", "array", required=False),
            ],
            output_format="JSON",
            reference_file="references/sibodahui_9agents.md"
        ))
        
        # ========== 更多私董会技能... ==========
        # 添加其他私董会成员技能...
        
        # ========== 理事会技能 ==========
        self.register_skill(Skill(
            id="lishihui_linghuchong_1",
            name="战略独孤九剑Skill",
            category=SkillCategory.COUNCIL,
            owner_agent="令狐冲",
            description="灵活应变的战略框架，无招胜有招",
            trigger_conditions=["战略", "竞争", "市场剧变", "灵活", "破局"],
            input_params=[
                SkillParameter("问题类型", "市场竞争/战略转型/组织变革/危机应对", "string"),
                SkillParameter("当前态势", "竞争格局、自身资源、核心能力描述", "string"),
                SkillParameter("约束条件", "时间、资金、人才、政策的限制", "object", required=False),
                SkillParameter("利益相关方", "股东、员工、客户、合作伙伴的诉求", "array", required=False),
            ],
            output_format="JSON",
            reference_file="references/lishihui_4agents.md"
        ))
        
        self.register_skill(Skill(
            id="lishihui_linghuchong_2",
            name="政企破壁Skill",
            category=SkillCategory.COUNCIL,
            owner_agent="令狐冲",
            description="打通政府关系、建立信任的方法论",
            trigger_conditions=["政府", "关系", "审批", "政策", "政企"],
            input_params=[
                SkillParameter("目标类型", "市场准入/政策支持/资源获取/危机化解", "string"),
                SkillParameter("对方关切", "政府部门的KPI、考核重点、风险偏好", "string"),
                SkillParameter("我方筹码", "能提供的价值", "string"),
                SkillParameter("潜在风险", "可能触发监管关注的敏感点", "string", required=False),
            ],
            output_format="JSON",
            reference_file="references/lishihui_4agents.md"
        ))
        
        self.register_skill(Skill(
            id="lishihui_zhugeliang_1",
            name="锦囊滚动规划Skill",
            category=SkillCategory.COUNCIL,
            owner_agent="诸葛亮",
            description="分层预设、随机应变的战略规划方法",
            trigger_conditions=["规划", "年度", "季度", "战略", "预案", "新业务"],
            input_params=[
                SkillParameter("规划周期", "年度/季度/月度", "string"),
                SkillParameter("战略目标", "组织的中长期战略目标", "string"),
                SkillParameter("当前资源", "人、财、物、时间的现状", "object"),
                SkillParameter("情境预设", "可能的情境假设", "array", required=False),
            ],
            output_format="JSON",
            reference_file="references/lishihui_4agents.md"
        ))
        
        self.register_skill(Skill(
            id="lishihui_zhugeliang_2",
            name="六步法督导Skill",
            category=SkillCategory.COUNCIL,
            owner_agent="诸葛亮",
            description="诊断-开方-执行-复盘的系统督导方法",
            trigger_conditions=["督导", "执行", "KPI", "遇阻", "跨部门"],
            input_params=[
                SkillParameter("问题描述", "具体的执行问题", "string"),
                SkillParameter("当前进度", "KPI完成情况", "object"),
                SkillParameter("已采取措施", "已经尝试的解决方案", "array", required=False),
            ],
            output_format="JSON",
            reference_file="references/lishihui_4agents.md"
        ))
        
        self.register_skill(Skill(
            id="lishihui_baoqingtian_1",
            name="利益回避虎头铡Skill",
            category=SkillCategory.COUNCIL,
            owner_agent="包青天",
            description="识别和回避利益冲突的方法论",
            trigger_conditions=["利益冲突", "关联交易", "回避", "合规", "审计"],
            input_params=[
                SkillParameter("决策事项", "需要做出的决策", "string"),
                SkillParameter("当事人信息", "参与决策的人员", "array"),
                SkillParameter("利益关系", "当事人与决策事项的利益关系", "array", required=False),
            ],
            output_format="JSON",
            reference_file="references/lishihui_4agents.md"
        ))
        
        self.register_skill(Skill(
            id="lishihui_baoqingtian_2",
            name="评议会铁券Skill",
            category=SkillCategory.COUNCIL,
            owner_agent="包青天",
            description="集体决策、程序公正的评议方法",
            trigger_conditions=["评议", "违规", "申诉", "争议", "处分"],
            input_params=[
                SkillParameter("事件类型", "违规/申诉/争议/处分", "string"),
                SkillParameter("当事人陈述", "当事人的说明和证据", "string"),
                SkillParameter("调查结论", "调查组的调查报告", "string"),
            ],
            output_format="JSON",
            reference_file="references/lishihui_4agents.md"
        ))
        
        self.register_skill(Skill(
            id="lishihui_huamulan_1",
            name="木兰辞对赌Skill",
            category=SkillCategory.COUNCIL,
            owner_agent="花木兰",
            description="高风险高回报的人才激励方法",
            trigger_conditions=["激励", "对赌", "保留", "绑定", "高管"],
            input_params=[
                SkillParameter("激励对象", "关键人才的背景和诉求", "object"),
                SkillParameter("业绩目标", "可量化的对赌目标", "object"),
                SkillParameter("公司资源", "能提供的资源支持", "object"),
            ],
            output_format="JSON",
            reference_file="references/lishihui_4agents.md"
        ))
        
        self.register_skill(Skill(
            id="lishihui_huamulan_2",
            name="士子点将Skill",
            category=SkillCategory.COUNCIL,
            owner_agent="花木兰",
            description="系统评估、科学决策的人才识别方法",
            trigger_conditions=["人才", "盘点", "继任", "晋升", "点将", "高潜"],
            input_params=[
                SkillParameter("盘点目的", "人才盘点/继任计划/晋升决策", "string"),
                SkillParameter("盘点范围", "部门/层级/岗位序列", "array"),
                SkillParameter("评估维度", "能力/绩效/潜力/价值观", "array", required=False),
            ],
            output_format="JSON",
            reference_file="references/lishihui_4agents.md"
        ))
        
        # ========== 专家委员会技能（示例）==========
        self.register_skill(Skill(
            id="zhuanjiaweiyuanhui_luoxiang_1",
            name="法律咨询Skill",
            category=SkillCategory.EXPERT_COMMITTEE,
            owner_agent="罗翔",
            description="法律风险识别和合规建议",
            trigger_conditions=["法律", "合规", "风险", "合同", "纠纷"],
            input_params=[
                SkillParameter("问题类型", "法律问题的类型", "string"),
                SkillParameter("事实描述", "相关事实的描述", "string"),
                SkillParameter("已有证据", "已有的证据材料", "array", required=False),
            ],
            output_format="JSON",
            reference_file="references/zhuanjiaweiyuanhui_11agents.md"
        ))
    
    def register_skill(self, skill: Skill):
        """注册技能"""
        self.skills[skill.id] = skill
        
        # 更新Agent-技能映射
        if skill.owner_agent not in self.agent_skills:
            self.agent_skills[skill.owner_agent] = []
        self.agent_skills[skill.owner_agent].append(skill.id)
        
        # 更新分类-技能映射
        if skill.category not in self.category_skills:
            self.category_skills[skill.category] = []
        self.category_skills[skill.category].append(skill.id)
    
    def find_skills(self, query: str, category: Optional[SkillCategory] = None,
                     top_k: int = 5) -> List[tuple[Skill, float]]:
        """查找匹配的技能"""
        candidates = list(self.skills.values())
        
        # 按分类过滤
        if category:
            candidates = [s for s in candidates if s.category == category]
        
        # 计算匹配度
        scored = [(s, s.match_trigger(query)) for s in candidates]
        
        # 排序
        scored.sort(key=lambda x: x[1], reverse=True)
        
        return scored[:top_k]
    
    def get_skills_by_agent(self, agent_name: str) -> List[Skill]:
        """获取Agent的所有技能"""
        skill_ids = self.agent_skills.get(agent_name, [])
        return [self.skills[sid] for sid in skill_ids if sid in self.skills]
    
    def get_skills_by_category(self, category: SkillCategory) -> List[Skill]:
        """获取分类的所有技能"""
        skill_ids = self.category_skills.get(category, [])
        return [self.skills[sid] for sid in skill_ids if sid in self.skills]
    
    def compose_skills(self, skills: List[Skill], context: Dict) -> Dict:
        """组合多个技能生成综合方案"""
        composed = {
            "参与技能": [s.name for s in skills],
            "参与Agent": list(set(s.owner_agent for s in skills)),
            "技能组合价值": self._analyze_combination_value(skills),
            "执行计划": [],
        }
        
        for skill in skills:
            composed["执行计划"].append({
                "技能": skill.name,
                "Agent": skill.owner_agent,
                "关注点": skill.description,
            })
        
        return composed
    
    def _analyze_combination_value(self, skills: List[Skill]) -> str:
        """分析技能组合的价值"""
        categories = set(s.category for s in skills)
        
        if len(categories) >= 2:
            return "跨机构协同，视角全面"
        elif len(categories) == 1:
            cat = list(categories)[0]
            if cat == SkillCategory.PRIVATE_BOARD:
                return "精神引领层洞察"
            elif cat == SkillCategory.COUNCIL:
                return "执行落地层方案"
            else:
                return "专业支撑层分析"
        else:
            return "单一技能支持"
    
    def validate_and_execute(self, skill_id: str, params: Dict) -> Dict:
        """验证并执行技能"""
        if skill_id not in self.skills:
            return {
                "success": False,
                "error": f"技能不存在: {skill_id}"
            }
        
        skill = self.skills[skill_id]
        
        # 验证参数
        valid, msg = skill.validate_input(params)
        if not valid:
            return {
                "success": False,
                "error": msg
            }
        
        # 执行技能（这里应该是实际执行逻辑）
        result = {
            "success": True,
            "skill_id": skill.id,
            "skill_name": skill.name,
            "owner_agent": skill.owner_agent,
            "output_format": skill.output_format,
            "reference_file": skill.reference_file,
            "message": f"技能 {skill.name} 执行成功，请参考 {skill.reference_file} 获取详细方法论"
        }
        
        return result
    
    def generate_skill_report(self, skills: List[Skill], 
                               problem: str) -> str:
        """生成技能应用报告"""
        report = f"""# 技能应用报告

## 问题背景
{problem}

## 匹配的技能

"""
        
        for skill in skills:
            report += f"""
### {skill.name}
- **所属Agent**: {skill.owner_agent}
- **所属分类**: {skill.category.value}
- **技能描述**: {skill.description}
- **触发条件**: {', '.join(skill.trigger_conditions)}
- **参考文件**: {skill.reference_file}
"""
        
        report += """
## 使用建议

1. 优先使用排名靠前的技能
2. 同一Agent的技能可以组合使用
3. 跨机构技能组合可以获得更全面的视角
4. 详细方法论请参考对应的知识蒸馏文件

---
*报告生成时间: 2024*
"""
        
        return report
    
    def list_all_skills(self) -> Dict:
        """列出所有技能"""
        result = {}
        for category in SkillCategory:
            skills = self.get_skills_by_category(category)
            if skills:
                result[category.value] = [
                    {
                        "id": s.id,
                        "name": s.name,
                        "owner": s.owner_agent,
                        "description": s.description
                    }
                    for s in skills
                ]
        return result


def main():
    """测试函数"""
    manager = SkillManager()
    
    # 测试查询
    test_queries = [
        "战略决策遇到竞争压力怎么办",
        "如何挽留核心人才",
        "产品设计太复杂怎么简化",
        "遇到法律纠纷怎么处理",
    ]
    
    print("=" * 60)
    print("技能管理器测试")
    print("=" * 60)
    
    for query in test_queries:
        print(f"\n查询: {query}")
        results = manager.find_skills(query, top_k=3)
        print("匹配技能:")
        for skill, score in results:
            if score > 0:
                print(f"  - [{score:.1f}] {skill.name} ({skill.owner_agent})")
    
    print("\n" + "=" * 60)
    print("所有技能列表")
    print("=" * 60)
    all_skills = manager.list_all_skills()
    print(json.dumps(all_skills, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
