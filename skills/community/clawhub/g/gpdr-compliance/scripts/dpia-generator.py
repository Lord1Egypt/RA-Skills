#!/usr/bin/env python3
"""
GDPR数据保护影响评估(DPIA)生成器
版本：1.0.1
最后更新：2026年3月25日
"""

import json
import argparse
from datetime import datetime

class DPIAGenerator:
    """GDPR数据保护影响评估(DPIA)生成器"""
    
    def __init__(self):
        self.template = {
            "dpia_id": "",
            "creation_date": "",
            "processing_description": "",
            "processing_purpose": "",
            "processing_categories": [],
            "data_subjects": [],
            "retention_period": "",
            "legal_basis": "",
            "data_transfers": [],
            "risk_assessment": {
                "likelihood": "",
                "impact": "",
                "overall_risk": ""
            },
            "mitigation_measures": [],
            "residual_risk": "",
            "dpo_consultation": {
                "required": False,
                "consulted": False,
                "recommendations": []
            },
            "authority_consultation": {
                "required": False,
                "consulted": False,
                "outcome": ""
            },
            "conclusion": {
                "can_proceed": False,
                "conditions": []
            },
            "approval": {
                "approved_by": "",
                "approval_date": "",
                "conditions": []
            }
        }
    
    def create_basic_template(self):
        """创建基本DPIA模板"""
        return {
            "title": "GDPR数据保护影响评估报告",
            "version": "1.0",
            "creation_date": datetime.now().isoformat(),
            "dpo_name": "",
            "assessor_name": "",
            "sections": {
                "processing_description": {
                    "title": "1. 数据处理活动描述",
                    "purpose": "处理目的",
                    "categories": ["个人数据类型"],
                    "scope": "处理范围"
                },
                "necessity_test": {
                    "title": "2. 必要性和成比例性测试",
                    "questions": [
                        "此处理是否为合法利益所必需？",
                        "是否有其他方法实现相同目的但影响更小？",
                        "处理范围是否适当限制？"
                    ]
                },
                "risk_assessment": {
                    "title": "3. 风险评估",
                    "data_subject_risks": ["对数据主体的潜在风险"],
                    "organization_risks": ["对组织的潜在风险"],
                    "likelihood": "高/中/低",
                    "severity": "严重/高/中/低"
                },
                "mitigation_measures": {
                    "title": "4. 缓解措施",
                    "measures": ["具体缓解措施"],
                    "effectiveness": "效果评估"
                },
                "dpo_consultation": {
                    "title": "5. 数据保护官(DPO)咨询",
                    "required": False,
                    "consulted": False,
                    "recommendations": []
                },
                "authority_consultation": {
                    "title": "6. 监管机构咨询",
                    "required": False,
                    "consulted": False,
                    "outcome": ""
                },
                "conclusion": {
                    "title": "7. 结论",
                    "can_proceed": False,
                    "conditions": ["继续条件"]
                }
            }
        }
    
    def automated_decision_dpia(self):
        """创建自动化决策DPIA模板"""
        return {
            "title": "GDPR自动化决策系统DPIA",
            "description": "自动化决策系统的数据保护影响评估",
            "legal_basis": "Article 22 - 自动化决策",
            "processing_details": {
                "decision_logic": "决策逻辑说明",
                "data_categories": ["使用的数据类别"],
                "decision_outcomes": ["可能的决策结果"]
            },
            "rights_guarantees": {
                "human_intervention": "人工干预机制",
                "right_to_object": "反对权行使",
                "right_to_explanation": "决策解释权"
            },
            "risk_assessment": {
                "risks_to_rights": ["对数据主体权利的风险"],
                "mitigation": ["风险缓解措施"]
            }
        }
    
    def save_template(self, template, filename=None):
        """保存模板到文件"""
        if not filename:
            filename = f"dpia_template_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(template, f, ensure_ascii=False, indent=2)
        
        return filename
    
    def interactive_mode(self):
        """交互式DPIA生成"""
        print("="*60)
        print("GDPR数据保护影响评估(DPIA)生成器")
        print("="*60)
        print("本工具帮助您创建GDPR DPIA报告模板。")
        print()
        
        template = self.create_basic_template()
        
        # 收集基本信息
        print("=== 基本信息 ===")
        template["sections"]["processing_description"]["purpose"] = input("处理目的: ")
        template["assessor_name"] = input("评估人姓名: ")
        template["dpo_name"] = input("DPO姓名（如适用）: ")
        
        print("\n=== 风险评估 ===")
        template["sections"]["risk_assessment"]["likelihood"] = input("风险可能性（高/中/低）: ")
        template["sections"]["risk_assessment"]["severity"] = input("风险严重程度（严重/高/中/低）: ")
        
        print("\n=== 结论 ===")
        can_proceed = input("是否可以继续处理？(y/n): ").lower() == 'y'
        template["sections"]["conclusion"]["can_proceed"] = can_proceed
        
        if can_proceed:
            conditions = input("继续条件（多个条件用逗号分隔）: ")
            template["sections"]["conclusion"]["conditions"] = [c.strip() for c in conditions.split(",")]
        
        return template

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='GDPR数据保护影响评估(DPIA)生成器')
    parser.add_argument('--interactive', '-i', action='store_true', help='交互式DPIA生成')
    parser.add_argument('--purpose', help='处理目的（快速生成）')
    parser.add_argument('--output', '-o', help='输出文件名')
    parser.add_argument('--type', choices=['basic', 'automated'], default='basic', help='DPIA类型')
    
    args = parser.parse_args()
    
    generator = DPIAGenerator()
    
    if args.interactive:
        print("开始交互式DPIA生成...")
        template = generator.interactive_mode()
    else:
        if args.purpose:
            print(f"生成针对'{args.purpose}'的DPIA模板...")
            template = generator.create_basic_template()
            template["sections"]["processing_description"]["purpose"] = args.purpose
        else:
            print("生成基本DPIA模板...")
            template = generator.create_basic_template()
    
    # 保存模板
    output_file = generator.save_template(template, args.output)
    
    print(f"\n✅ DPIA模板已生成: {output_file}")
    print("="*60)
    print("下一步建议：")
    print("1. 根据实际情况完善DPIA模板")
    print("2. 进行详细的风险评估")
    print("3. 咨询DPO（如适用）")
    print("4. 如需要，咨询监管机构")
    print("5. 记录DPIA结果和缓解措施")
    print("="*60)

if __name__ == "__main__":
    main()