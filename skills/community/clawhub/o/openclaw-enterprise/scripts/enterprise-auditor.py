#!/usr/bin/env python3
"""
企业AI Agent成熟度评估工具 - Level 2
Enterprise AI Agent Maturity Assessment

功能：
- audit: 企业AI Agent成熟度评估（战略/技术/数据/组织/流程5维）
- roi: 投资ROI估算
- roadmap: 实施路线图生成

Author: OpenClaw Enterprise Team
Version: 1.0.0
"""

import sys
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict
from enum import Enum


class MaturityLevel(Enum):
    """成熟度等级"""
    LEVEL_1_INITIAL = 1  # 初始级
    LEVEL_2_DEVELOPING = 2  # 发展中
    LEVEL_3_DEFINED = 3  # 已定义
    LEVEL_4_MANAGED = 4  # 已管理
    LEVEL_5_OPTIMIZING = 5  # 优化中


@dataclass
class DimensionScore:
    """维度评分"""
    dimension: str
    score: float  # 0-100
    level: str
    strengths: List[str] = field(default_factory=list)
    gaps: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class MaturityReport:
    """成熟度报告"""
    overall_score: float
    overall_level: str
    dimensions: List[DimensionScore]
    priority_focus: List[str]
    investment_plan: Dict[str, Any]
    timeline: List[Dict[str, str]]


class EnterpriseAuditor:
    """企业AI Agent成熟度评估器"""
    
    DIMENSIONS = [
        "战略规划",    # 战略维度
        "技术架构",    # 技术维度
        "数据治理",    # 数据维度
        "组织能力",    # 组织维度
        "流程优化"     # 流程维度
    ]
    
    DIMENSION_WEIGHTS = {
        "战略规划": 0.25,
        "技术架构": 0.25,
        "数据治理": 0.20,
        "组织能力": 0.15,
        "流程优化": 0.15
    }
    
    def __init__(self):
        self.current_report: Optional[MaturityReport] = None
    
    def assess_dimension(self, dimension: str, responses: Dict[str, int]) -> DimensionScore:
        """
        评估单个维度
        
        Args:
            dimension: 维度名称
            responses: 用户响应字典，键为问题ID，值为评分(1-5)
        
        Returns:
            维度评分结果
        """
        if not responses:
            return DimensionScore(
                dimension=dimension,
                score=0,
                level="未评估",
                strengths=[],
                gaps=[],
                recommendations=[]
            )
        
        # 计算基础分数
        avg_score = sum(responses.values()) / len(responses)
        normalized_score = (avg_score / 5) * 100
        
        # 确定成熟度等级
        if normalized_score < 20:
            level = "LEVEL_1_INITIAL"
            level_cn = "初始级"
        elif normalized_score < 40:
            level = "LEVEL_2_DEVELOPING"
            level_cn = "发展中"
        elif normalized_score < 60:
            level = "LEVEL_3_DEFINED"
            level_cn = "已定义"
        elif normalized_score < 80:
            level = "LEVEL_4_MANAGED"
            level_cn = "已管理"
        else:
            level = "LEVEL_5_OPTIMIZING"
            level_cn = "优化中"
        
        # 生成优势和差距分析
        strengths = self._generate_strengths(dimension, responses)
        gaps = self._generate_gaps(dimension, responses)
        recommendations = self._generate_recommendations(dimension, normalized_score)
        
        return DimensionScore(
            dimension=dimension,
            score=round(normalized_score, 1),
            level=level_cn,
            strengths=strengths,
            gaps=gaps,
            recommendations=recommendations
        )
    
    def _generate_strengths(self, dimension: str, responses: Dict) -> List[str]:
        """生成优势分析"""
        strengths = []
        high_score_items = [(k, v) for k, v in responses.items() if v >= 4]
        
        if len(high_score_items) >= 3:
            strengths.append(f"在{len(high_score_items)}个关键指标上表现优秀")
        
        dimension_strengths = {
            "战略规划": ["明确的AI应用愿景", "高层支持到位", "有明确的KPI体系"],
            "技术架构": ["基础架构完善", "API集成能力强", "安全性设计良好"],
            "数据治理": ["数据质量管理体系健全", "有数据标准规范", "隐私保护措施完善"],
            "组织能力": ["团队技能储备充足", "有专业AI团队", "培训体系完善"],
            "流程优化": ["流程文档完善", "有标准化操作流程", "持续改进机制建立"]
        }
        
        strengths.extend(dimension_strengths.get(dimension, [])[:2])
        return strengths[:5]
    
    def _generate_gaps(self, dimension: str, responses: Dict) -> List[str]:
        """生成差距分析"""
        gaps = []
        low_score_items = [(k, v) for k, v in responses.items() if v <= 2]
        
        if len(low_score_items) >= 2:
            gaps.append(f"存在{len(low_score_items)}个关键指标待改进")
        
        dimension_gaps = {
            "战略规划": ["缺乏长期AI规划", "ROI衡量体系不完善", "战略与执行脱节"],
            "技术架构": ["系统集成能力不足", "技术债务累积", "扩展性受限"],
            "数据治理": ["数据孤岛问题", "数据质量不稳定", "数据安全风险"],
            "组织能力": ["专业人才短缺", "跨部门协作不畅", "变革阻力大"],
            "流程优化": ["流程标准化程度低", "缺乏关注机制", "改进周期长"]
        }
        
        gaps.extend(dimension_gaps.get(dimension, [])[:2])
        return gaps[:5]
    
    def _generate_recommendations(self, dimension: str, score: float) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        if score < 40:
            recommendations.append(f"【紧急】优先建立{dimension}基础能力")
            recommendations.append("建议引入外部顾问进行现状诊断")
            recommendations.append("制定90天快速改进计划")
        elif score < 60:
            recommendations.append(f"加强{dimension}体系建设")
            recommendations.append("参考行业最佳实践进行优化")
            recommendations.append("建立定期评估机制")
        elif score < 80:
            recommendations.append(f"深化{dimension}能力建设")
            recommendations.append("推动创新试点项目")
            recommendations.append("建立标杆案例推广机制")
        else:
            recommendations.append("持续优化领先实践")
            recommendations.append("探索前沿技术应用")
            recommendations.append("对外分享成功经验")
        
        return recommendations
    
    def calculate_overall_score(self, dimension_scores: List[DimensionScore]) -> float:
        """计算综合评分"""
        total_score = 0
        for ds in dimension_scores:
            weight = self.DIMENSION_WEIGHTS.get(ds.dimension, 0.2)
            total_score += ds.score * weight
        return round(total_score, 1)
    
    def determine_overall_level(self, score: float) -> str:
        """确定综合成熟度等级"""
        if score < 20:
            return "L1-初始级（探索期）"
        elif score < 40:
            return "L2-发展中（试点期）"
        elif score < 60:
            return "L3-已定义（推广期）"
        elif score < 80:
            return "L4-已管理（成熟期）"
        else:
            return "L5-优化中（领先期）"
    
    def audit(self, company_data: Dict[str, Any]) -> MaturityReport:
        """
        执行完整成熟度评估
        
        Args:
            company_data: 企业数据，包含各维度评估响应
        
        Returns:
            完整的成熟度评估报告
        """
        dimension_scores = []
        
        # 评估各维度
        for dimension in self.DIMENSIONS:
            responses = company_data.get(dimension, {})
            ds = self.assess_dimension(dimension, responses)
            dimension_scores.append(ds)
        
        # 计算综合评分
        overall_score = self.calculate_overall_score(dimension_scores)
        overall_level = self.determine_overall_level(overall_score)
        
        # 确定优先关注领域
        priority_focus = self._determine_priority_focus(dimension_scores)
        
        # 生成投资计划
        investment_plan = self._generate_investment_plan(overall_score, dimension_scores)
        
        # 生成实施路线图
        timeline = self._generate_timeline(overall_score)
        
        self.current_report = MaturityReport(
            overall_score=overall_score,
            overall_level=overall_level,
            dimensions=dimension_scores,
            priority_focus=priority_focus,
            investment_plan=investment_plan,
            timeline=timeline
        )
        
        return self.current_report
    
    def _determine_priority_focus(self, dimension_scores: List[DimensionScore]) -> List[str]:
        """确定优先关注领域"""
        sorted_dims = sorted(dimension_scores, key=lambda x: x.score)
        priority = []
        
        for dim in sorted_dims[:3]:
            priority.append(f"{dim.dimension}({dim.score}分)")
        
        return priority
    
    def _generate_investment_plan(self, overall_score: float, 
                                   dimension_scores: List[DimensionScore]) -> Dict[str, Any]:
        """生成投资计划"""
        base_investment = 100  # 万元
        
        if overall_score < 40:
            multiplier = 2.0
        elif overall_score < 60:
            multiplier = 1.5
        elif overall_score < 80:
            multiplier = 1.2
        else:
            multiplier = 1.0
        
        total_investment = base_investment * multiplier
        
        investment_breakdown = {}
        for ds in dimension_scores:
            if ds.score < 50:
                weight = 0.3
            elif ds.score < 70:
                weight = 0.2
            else:
                weight = 0.1
            investment_breakdown[ds.dimension] = {
                "占比": f"{weight*100:.0f}%",
                "建议投资额(万元)": round(total_investment * weight, 1)
            }
        
        return {
            "总投资估算(万元)": round(total_investment, 1),
            "投资周期": "12个月",
            "投资重点": investment_breakdown,
            "预期收益": "效率提升20-40%，成本降低15-30%"
        }
    
    def _generate_timeline(self, overall_score: float) -> List[Dict[str, str]]:
        """生成实施路线图"""
        if overall_score < 40:
            phases = [
                {"阶段": "第一阶段(1-3月)", "重点": "基础设施建设", "里程碑": "完成现状诊断和基础架构搭建"},
                {"阶段": "第二阶段(4-6月)", "重点": "核心能力建设", "里程碑": "至少3个Agent上线运行"},
                {"阶段": "第三阶段(7-9月)", "重点": "规模化推广", "里程碑": "覆盖核心业务场景"},
                {"阶段": "第四阶段(10-12月)", "重点": "优化迭代", "里程碑": "建立持续优化机制"}
            ]
        elif overall_score < 60:
            phases = [
                {"阶段": "第一阶段(1-2月)", "重点": "能力补强", "里程碑": "识别并补强关键短板"},
                {"阶段": "第二阶段(3-5月)", "重点": "深化应用", "里程碑": "Agent集群协同工作"},
                {"阶段": "第三阶段(6-9月)", "重点": "全面推广", "里程碑": "80%业务覆盖"},
                {"阶段": "第四阶段(10-12月)", "重点": "优化升级", "里程碑": "达到L4成熟度"}
            ]
        else:
            phases = [
                {"阶段": "第一阶段(1-3月)", "重点": "精细化运营", "里程碑": "建立量化指标体系"},
                {"阶段": "第二阶段(4-6月)", "重点": "创新探索", "里程碑": "2个创新试点"},
                {"阶段": "第三阶段(7-12月)", "重点": "行业引领", "里程碑": "形成最佳实践"}
            ]
        
        return phases
    
    def estimate_roi(self, investment_amount: float, 
                     expected_improvement: float) -> Dict[str, Any]:
        """
        估算投资ROI
        
        Args:
            investment_amount: 投资金额（万元）
            expected_improvement: 预期效率提升比例（0-1）
        
        Returns:
            ROI估算结果
        """
        # 假设年收入基数为1000万元
        base_revenue = 1000
        additional_revenue = base_revenue * expected_improvement
        
        # 计算ROI
        net_benefit = additional_revenue - investment_amount
        roi = (net_benefit / investment_amount) * 100 if investment_amount > 0 else 0
        
        payback_months = (investment_amount / (additional_revenue / 12)) if additional_revenue > 0 else 0
        
        return {
            "投资金额(万元)": investment_amount,
            "预期年收入增量(万元)": round(additional_revenue, 1),
            "净收益(万元)": round(net_benefit, 1),
            "投资回报率(%)": round(roi, 1),
            "投资回收期(月)": round(payback_months, 1),
            "建议": "ROI>100%建议投资，回收期<12个月风险可控" if roi > 100 and payback_months < 12 else "需进一步评估"
        }
    
    def generate_roadmap(self, target_level: str) -> List[Dict[str, Any]]:
        """
        生成实施路线图
        
        Args:
            target_level: 目标成熟度等级
        
        Returns:
            实施路线图
        """
        level_map = {
            "L1": 20, "L2": 40, "L3": 60, "L4": 80, "L5": 100
        }
        
        target_score = level_map.get(target_level, 60)
        
        if self.current_report:
            current_score = self.current_report.overall_score
        else:
            current_score = 50
        
        gap = target_score - current_score
        
        if gap <= 0:
            return [{
                "message": "已达到目标等级，建议关注持续优化",
                "actions": ["建立关注体系", "定期评估复盘", "持续迭代改进"]
            }]
        
        # 根据差距确定路线
        roadmap = []
        
        if gap > 30:
            roadmap.append({
                "阶段": "基础建设期",
                "时长": "3-6个月",
                "重点": ["完善基础设施", "建立数据体系", "组建专业团队"],
                "产出": "具备基本的Agent运行能力"
            })
        
        if gap > 15:
            roadmap.append({
                "阶段": "能力提升期",
                "时长": "6-12个月",
                "重点": ["深化应用场景", "优化业务流程", "建立治理体系"],
                "产出": "核心业务场景Agent化"
            })
        
        roadmap.append({
            "阶段": "优化成熟期",
            "时长": "12-18个月",
            "重点": ["规模化应用", "持续迭代优化", "行业标杆打造"],
            "产出": "达到目标成熟度等级"
        })
        
        return roadmap
    
    def format_report(self, report: MaturityReport) -> str:
        """格式化输出报告"""
        output = []
        output.append("=" * 60)
        output.append("企业AI Agent成熟度评估报告")
        output.append("=" * 60)
        output.append(f"\n【综合评分】{report.overall_score}分")
        output.append(f"【成熟度等级】{report.overall_level}")
        output.append(f"\n【优先关注领域】")
        for p in report.priority_focus:
            output.append(f"  • {p}")
        
        output.append(f"\n【各维度评分】")
        for dim in report.dimensions:
            output.append(f"\n  ▶ {dim.dimension} ({dim.score}分 - {dim.level})")
            if dim.strengths:
                output.append("    优势:")
                for s in dim.strengths[:3]:
                    output.append(f"      ✓ {s}")
            if dim.gaps:
                output.append("    差距:")
                for g in dim.gaps[:3]:
                    output.append(f"      ✗ {g}")
            if dim.recommendations:
                output.append("    建议:")
                for r in dim.recommendations[:2]:
                    output.append(f"      → {r}")
        
        output.append(f"\n【投资计划】")
        ip = report.investment_plan
        output.append(f"  总投资估算: {ip['总投资估算(万元)']}万元")
        output.append(f"  投资周期: {ip['投资周期']}")
        output.append(f"  预期收益: {ip['预期收益']}")
        
        output.append(f"\n【实施路线图】")
        for phase in report.timeline:
            output.append(f"\n  {phase['阶段']}")
            output.append(f"    重点: {phase['重点']}")
            output.append(f"    里程碑: {phase['里程碑']}")
        
        output.append("\n" + "=" * 60)
        return "\n".join(output)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python enterprise-auditor.py <command> [args]")
        print("命令:")
        print("  audit   - 执行成熟度评估")
        print("  roi     - 估算投资ROI")
        print("  roadmap - 生成实施路线图")
        return
    
    command = sys.argv[1]
    auditor = EnterpriseAuditor()
    
    if command == "audit":
        # 模拟评估数据
        sample_data = {
            "战略规划": {"q1": 3, "q2": 2, "q3": 4, "q4": 3, "q5": 2},
            "技术架构": {"q1": 4, "q2": 3, "q3": 4, "q4": 3, "q5": 4},
            "数据治理": {"q1": 2, "q2": 3, "q3": 2, "q4": 3, "q5": 2},
            "组织能力": {"q1": 3, "q2": 3, "q3": 4, "q4": 3, "q5": 3},
            "流程优化": {"q1": 2, "q2": 3, "q3": 3, "q4": 2, "q5": 3}
        }
        
        report = auditor.audit(sample_data)
        print(auditor.format_report(report))
        
    elif command == "roi":
        investment = float(sys.argv[2]) if len(sys.argv) > 2 else 100
        improvement = float(sys.argv[3]) if len(sys.argv) > 3 else 0.2
        
        result = auditor.estimate_roi(investment, improvement)
        print("=" * 40)
        print("投资ROI估算")
        print("=" * 40)
        for k, v in result.items():
            print(f"{k}: {v}")
        
    elif command == "roadmap":
        target = sys.argv[2] if len(sys.argv) > 2 else "L4"
        roadmap = auditor.generate_roadmap(target)
        print("=" * 40)
        print(f"实施路线图 (目标: {target})")
        print("=" * 40)
        for phase in roadmap:
            print(json.dumps(phase, ensure_ascii=False, indent=2))
    else:
        print(f"未知命令: {command}")


if __name__ == "__main__":
    main()
