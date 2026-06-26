#!/usr/bin/env python3
"""
GDPR报告格式化工具
提供GDPR合规报告的格式化功能
"""

import json
import datetime
from typing import Dict, List, Any, Optional, Union
from enum import Enum


class ReportFormat(Enum):
    """报告格式枚举"""
    JSON = "json"
    MARKDOWN = "markdown"
    HTML = "html"
    PLAIN_TEXT = "plain_text"
    CSV = "csv"


class RiskLevel(Enum):
    """风险等级枚举"""
    LOW = "低风险"
    MEDIUM = "中等风险"
    HIGH = "高风险"
    CRITICAL = "严重风险"


class GDPRReportFormatter:
    """GDPR报告格式化器"""
    
    def __init__(self):
        self.templates = {
            "compliance_check": self._get_compliance_check_template(),
            "risk_assessment": self._get_risk_assessment_template(),
            "dpia_summary": self._get_dpia_summary_template(),
            "data_breach": self._get_data_breach_template(),
            "cross_border_transfer": self._get_cross_border_template()
        }
    
    def _get_compliance_check_template(self) -> Dict[str, Any]:
        """获取合规检查报告模板"""
        return {
            "metadata": {
                "report_type": "GDPR合规检查报告",
                "version": "1.0",
                "generated_date": "",
                "company_name": "",
                "assessment_date": ""
            },
            "summary": {
                "overall_score": 0,
                "compliance_level": "",
                "total_checks": 0,
                "passed_checks": 0,
                "failed_checks": 0,
                "warnings": 0
            },
            "checks": {
                "legal_basis": {
                    "description": "合法性基础检查",
                    "status": "",
                    "details": [],
                    "recommendations": []
                },
                "data_subject_rights": {
                    "description": "数据主体权利检查",
                    "status": "",
                    "details": [],
                    "recommendations": []
                },
                "data_security": {
                    "description": "数据安全措施检查",
                    "status": "",
                    "details": [],
                    "recommendations": []
                },
                "dpo_requirements": {
                    "description": "DPO要求检查",
                    "status": "",
                    "details": [],
                    "recommendations": []
                },
                "dpia_requirements": {
                    "description": "DPIA要求检查",
                    "status": "",
                    "details": [],
                    "recommendations": []
                },
                "data_breach": {
                    "description": "数据泄露通知要求检查",
                    "status": "",
                    "details": [],
                    "recommendations": []
                },
                "cross_border_transfer": {
                    "description": "跨境传输要求检查",
                    "status": "",
                    "details": [],
                    "recommendations": []
                }
            },
            "recommendations": {
                "immediate": [],
                "short_term": [],
                "long_term": []
            },
            "next_steps": []
        }
    
    def _get_risk_assessment_template(self) -> Dict[str, Any]:
        """获取风险评估报告模板"""
        return {
            "metadata": {
                "report_type": "GDPR风险评估报告",
                "version": "1.0",
                "generated_date": "",
                "company_name": "",
                "assessment_date": ""
            },
            "risk_matrix": {
                "likelihood": {
                    "rare": "罕见 (每年少于1次)",
                    "unlikely": "不太可能 (每年1-3次)",
                    "possible": "可能 (每年4-12次)",
                    "likely": "很可能 (每月1-3次)",
                    "certain": "几乎确定 (每周1次或更频繁)"
                },
                "impact": {
                    "insignificant": "可忽略 (对业务无影响)",
                    "minor": "轻微 (有限业务影响)",
                    "moderate": "中等 (明显业务影响)",
                    "major": "重大 (严重业务影响)",
                    "catastrophic": "灾难性 (业务中断)"
                }
            },
            "identified_risks": [],
            "risk_assessment": {
                "high_risks": [],
                "medium_risks": [],
                "low_risks": []
            },
            "risk_treatment": {
                "avoid": [],
                "reduce": [],
                "transfer": [],
                "accept": []
            },
            "risk_owners": [],
            "monitoring_plan": []
        }
    
    def _get_dpia_summary_template(self) -> Dict[str, Any]:
        """获取DPIA摘要报告模板"""
        return {
            "metadata": {
                "report_type": "数据保护影响评估(DPIA)摘要",
                "version": "1.0",
                "generated_date": "",
                "project_name": "",
                "assessment_date": ""
            },
            "project_overview": {
                "description": "",
                "purpose": "",
                "legal_basis": "",
                "data_categories": [],
                "data_sources": [],
                "data_recipients": []
            },
            "risk_assessment": {
                "identified_risks": [],
                "risk_level": "",
                "justification": ""
            },
            "proposed_measures": {
                "technical": [],
                "organizational": [],
                "contractual": []
            },
            "consultation": {
                "dpo_consulted": False,
                "dpo_opinion": "",
                "supervisory_consulted": False,
                "supervisory_opinion": ""
            },
            "conclusion": {
                "approved": False,
                "approver": "",
                "approval_date": "",
                "conditions": []
            }
        }
    
    def _get_data_breach_template(self) -> Dict[str, Any]:
        """获取数据泄露报告模板"""
        return {
            "metadata": {
                "report_type": "数据泄露报告",
                "version": "1.0",
                "generated_date": "",
                "breach_id": "",
                "notification_date": ""
            },
            "breach_details": {
                "discovery_time": "",
                "occurrence_time": "",
                "duration": "",
                "type": "",
                "cause": "",
                "affected_data_categories": [],
                "estimated_affected_individuals": 0
            },
            "impact_assessment": {
                "data_subject_impact": "",
                "business_impact": "",
                "regulatory_impact": "",
                "reputation_impact": ""
            },
            "response_actions": {
                "immediate": [],
                "technical": [],
                "organizational": [],
                "communication": []
            },
            "notification": {
                "supervisory_notified": False,
                "supervisory_notification_time": "",
                "data_subjects_notified": False,
                "data_subjects_notification_time": "",
                "notification_method": ""
            },
            "preventive_measures": {
                "short_term": [],
                "long_term": []
            },
            "lessons_learned": []
        }
    
    def _get_cross_border_template(self) -> Dict[str, Any]:
        """获取跨境传输报告模板"""
        return {
            "metadata": {
                "report_type": "跨境数据传输评估报告",
                "version": "1.0",
                "generated_date": "",
                "assessment_date": ""
            },
            "transfer_details": {
                "source_country": "",
                "destination_country": "",
                "data_categories": [],
                "purpose": "",
                "duration": "",
                "recipients": []
            },
            "legal_assessment": {
                "adequacy_decision": False,
                "transfer_mechanism": "",
                "mechanism_details": "",
                "additional_safeguards": []
            },
            "risk_assessment": {
                "country_risk": "",
                "data_protection_level": "",
                "enforcement_risk": "",
                "overall_risk": ""
            },
            "compliance_check": {
                "sccs_compliant": False,
                "bcrs_compliant": False,
                "supplementary_measures": False,
                "documentation_complete": False
            },
            "recommendations": {
                "approval": "",
                "conditions": [],
                "monitoring": []
            }
        }
    
    def format_compliance_report(self, data: Dict[str, Any], 
                               format: ReportFormat = ReportFormat.JSON) -> Union[str, Dict[str, Any]]:
        """
        格式化合规检查报告
        
        Args:
            data: 报告数据
            format: 输出格式
            
        Returns:
            格式化后的报告
        """
        template = self._get_compliance_check_template()
        
        # 合并数据
        report = self._merge_data(template, data)
        
        # 添加生成日期
        report["metadata"]["generated_date"] = datetime.datetime.now().isoformat()
        
        # 计算总分
        if "summary" in data:
            report["summary"] = data["summary"]
        else:
            report["summary"] = self._calculate_compliance_score(report["checks"])
        
        return self._format_output(report, format)
    
    def format_risk_report(self, data: Dict[str, Any],
                          format: ReportFormat = ReportFormat.JSON) -> Union[str, Dict[str, Any]]:
        """
        格式化风险评估报告
        
        Args:
            data: 报告数据
            format: 输出格式
            
        Returns:
            格式化后的报告
        """
        template = self._get_risk_assessment_template()
        
        # 合并数据
        report = self._merge_data(template, data)
        
        # 添加生成日期
        report["metadata"]["generated_date"] = datetime.datetime.now().isoformat()
        
        # 分类风险
        if "identified_risks" in data:
            report = self._categorize_risks(report, data["identified_risks"])
        
        return self._format_output(report, format)
    
    def format_dpia_summary(self, data: Dict[str, Any],
                           format: ReportFormat = ReportFormat.JSON) -> Union[str, Dict[str, Any]]:
        """
        格式化DPIA摘要报告
        
        Args:
            data: 报告数据
            format: 输出格式
            
        Returns:
            格式化后的报告
        """
        template = self._get_dpia_summary_template()
        
        # 合并数据
        report = self._merge_data(template, data)
        
        # 添加生成日期
        report["metadata"]["generated_date"] = datetime.datetime.now().isoformat()
        
        return self._format_output(report, format)
    
    def _merge_data(self, template: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """合并模板和数据"""
        import copy
        
        result = copy.deepcopy(template)
        
        def recursive_merge(target: Dict[str, Any], source: Dict[str, Any]) -> None:
            for key, value in source.items():
                if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                    recursive_merge(target[key], value)
                else:
                    target[key] = value
        
        recursive_merge(result, data)
        return result
    
    def _calculate_compliance_score(self, checks: Dict[str, Any]) -> Dict[str, Any]:
        """计算合规分数"""
        total_checks = len(checks)
        passed_checks = 0
        failed_checks = 0
        warnings = 0
        
        for check_name, check_data in checks.items():
            status = check_data.get("status", "").lower()
            
            if status == "passed":
                passed_checks += 1
            elif status == "failed":
                failed_checks += 1
            elif status == "warning":
                warnings += 1
        
        overall_score = int((passed_checks / total_checks) * 100) if total_checks > 0 else 0
        
        # 确定合规等级
        if overall_score >= 90:
            compliance_level = "优秀"
        elif overall_score >= 70:
            compliance_level = "良好"
        elif overall_score >= 50:
            compliance_level = "一般"
        else:
            compliance_level = "需要改进"
        
        return {
            "overall_score": overall_score,
            "compliance_level": compliance_level,
            "total_checks": total_checks,
            "passed_checks": passed_checks,
            "failed_checks": failed_checks,
            "warnings": warnings
        }
    
    def _categorize_risks(self, report: Dict[str, Any], risks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分类风险"""
        for risk in risks:
            risk_level = risk.get("level", "").lower()
            
            if risk_level in ["high", "critical"]:
                report["risk_assessment"]["high_risks"].append(risk)
            elif risk_level == "medium":
                report["risk_assessment"]["medium_risks"].append(risk)
            else:
                report["risk_assessment"]["low_risks"].append(risk)
        
        return report
    
    def _format_output(self, data: Dict[str, Any], format: ReportFormat) -> Union[str, Dict[str, Any]]:
        """格式化输出"""
        if format == ReportFormat.JSON:
            return data
        
        elif format == ReportFormat.MARKDOWN:
            return self._convert_to_markdown(data)
        
        elif format == ReportFormat.HTML:
            return self._convert_to_html(data)
        
        elif format == ReportFormat.PLAIN_TEXT:
            return self._convert_to_text(data)
        
        elif format == ReportFormat.CSV:
            return self._convert_to_csv(data)
        
        else:
            raise ValueError(f"不支持的格式: {format}")
    
    def _convert_to_markdown(self, data: Dict[str, Any]) -> str:
        """转换为Markdown格式"""
        # 简化实现，实际应该更完整
        import json
        return f"```json\n{json.dumps(data, ensure_ascii=False, indent=2)}\n```"
    
    def _convert_to_html(self, data: Dict[str, Any]) -> str:
        """转换为HTML格式"""
        # 简化实现
        import json
        return f"<pre>{json.dumps(data, ensure_ascii=False, indent=2)}</pre>"
    
    def _convert_to_text(self, data: Dict[str, Any]) -> str:
        """转换为纯文本格式"""
        # 简化实现
        import json
        return json.dumps(data, ensure_ascii=False, indent=2)
    
    def _convert_to_csv(self, data: Dict[str, Any]) -> str:
        """转换为CSV格式"""
        # 简化实现
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # 只处理简单数据结构
        if "checks" in data:
            writer.writerow(["检查项目", "状态", "描述"])
            for check_name, check_data in data["checks"].items():
                writer.writerow([
                    check_data.get("description", check_name),
                    check_data.get("status", ""),
                    "; ".join(check_data.get("details", []))
                ])
        
        return output.getvalue()


def main():
    """测试函数"""
    formatter = GDPRReportFormatter()
    
    # 测试合规报告
    print("测试合规报告格式化:")
    
    compliance_data = {
        "metadata": {
            "company_name": "示例公司",
            "assessment_date": "2024-01-15"
        },
        "checks": {
            "legal_basis": {
                "status": "passed",
                "details": ["合法性基础明确"],
                "recommendations": []
            },
            "data_subject_rights": {
                "status": "warning",
                "details": ["部分权利实现不完整"],
                "recommendations": ["完善数据主体权利实现机制"]
            }
        }
    }
    
    try:
        # JSON格式
        json_report = formatter.format_compliance_report(compliance_data, ReportFormat.JSON)
        print("✅ JSON格式报告生成成功")
        print(f"报告类型: {json_report['metadata']['report_type']}")
        
        # Markdown格式
        md_report = formatter.format_compliance_report(compliance_data, ReportFormat.MARKDOWN)
        print(f"✅ Markdown格式报告长度: {len(md_report)} 字符")
        
        # 测试风险评估报告
        print("\n测试风险评估报告格式化:")
        
        risk_data = {
            "metadata": {
                "company_name": "示例公司"
            },
            "identified_risks": [
                {"name": "数据泄露风险", "level": "high", "description": "缺乏加密措施"},
                {"name": "合规风险", "level": "medium", "description": "文档不完整"}
            ]
        }
        
        risk_report = formatter.format_risk_report(risk_data, ReportFormat.JSON)
        print("✅ 风险评估报告生成成功")
        print(f"高风险数量: {len(risk_report['risk_assessment']['high_risks'])}")
        print(f"中等风险数量: {len(risk_report['risk_assessment']['medium_risks'])}")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")


if __name__ == "__main__":
    main()