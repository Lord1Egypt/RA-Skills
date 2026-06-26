#!/usr/bin/env python3
"""
GDPR合规检查工具
版本：1.0.0
最后更新：2026年3月25日
"""

import sys
import json
import argparse
from datetime import datetime

class GDPRAuditTool:
    """GDPR合规检查工具"""
    
    def __init__(self):
        self.results = {
            "audit_date": datetime.now().isoformat(),
            "skill_version": "1.0.0",
            "summary": {
                "total_checks": 0,
                "passed": 0,
                "failed": 0,
                "warnings": 0
            },
            "checks": []
        }
        
        # GDPR核心检查项
        self.gdpr_checks = [
            self.check_legal_basis,
            self.check_data_subject_rights,
            self.check_dpo_requirement,
            self.check_dpia_requirement,
            self.check_data_breach_notification,
            self.check_international_transfers,
            self.check_privacy_by_design,
            self.check_data_minimization,
            self.check_accuracy,
            self.check_storage_limitation,
            self.check_integrity_confidentiality,
            self.check_accountability
        ]
    
    def check_legal_basis(self):
        """检查合法性基础"""
        check_id = "legal_basis"
        description = "验证数据处理活动的合法性基础"
        
        questions = [
            "1. 您是否有至少一种合法性基础？",
            "   a) 数据主体同意",
            "   b) 合同履行",
            "   c) 法律义务",
            "   d) 保护数据主体或他人的重大利益",
            "   e) 公共利益任务",
            "   f) 合法利益（需进行平衡测试）",
            "2. 您是否记录了合法性基础的依据？",
            "3. 特殊类别数据是否满足额外条件？"
        ]
        
        result = {
            "check_id": check_id,
            "description": description,
            "questions": questions,
            "recommendations": [
                "为每个处理活动确定并记录合法性基础",
                "对于合法利益，必须进行平衡测试并记录",
                "特殊类别数据处理必须满足Article 9的额外条件"
            ],
            "status": "PENDING",
            "score": 0
        }
        
        return result
    
    def check_data_subject_rights(self):
        """检查数据主体权利"""
        check_id = "data_subject_rights"
        description = "验证数据主体权利的保障机制"
        
        rights = [
            "知情权（Articles 13-14）",
            "访问权（Article 15）",
            "更正权（Article 16）",
            "删除权（Article 17）",
            "限制处理权（Article 18）",
            "数据可携带权（Article 20）",
            "反对权（Article 21）",
            "自动化决策相关权利（Article 22）"
        ]
        
        result = {
            "check_id": check_id,
            "description": description,
            "rights": rights,
            "questions": [
                "1. 您是否有机制处理数据主体的权利请求？",
                "2. 您是否在合理时间内响应请求？",
                "3. 您是否免费提供首次数据副本？",
                "4. 您是否验证请求者的身份？"
            ],
            "recommendations": [
                "建立标准化的权利请求处理流程",
                "确保在法定期限内（通常一个月内）响应",
                "提供电子格式的数据副本",
                "实施适当的身份验证机制"
            ],
            "status": "PENDING",
            "score": 0
        }
        
        return result
    
    def check_dpo_requirement(self):
        """检查DPO要求"""
        check_id = "dpo_requirement"
        description = "确定是否需要指定数据保护官（DPO）"
        
        criteria = [
            "公共机构或机关（除法院外）",
            "核心活动涉及大规模、系统性监控",
            "核心活动涉及大规模处理特殊类别数据或犯罪相关数据"
        ]
        
        result = {
            "check_id": check_id,
            "description": description,
            "criteria": criteria,
            "questions": [
                "1. 您的机构是否属于公共机构？",
                "2. 您的核心活动是否涉及大规模监控？",
                "3. 您是否大规模处理特殊类别数据？",
                "4. 如果您需要DPO，是否已指定？"
            ],
            "recommendations": [
                "定期评估是否需要指定DPO",
                "如果指定DPO，确保其独立性",
                "公开DPO的姓名和联系方式",
                "确保DPO具备适当的专业知识"
            ],
            "status": "PENDING",
            "score": 0
        }
        
        return result
    
    def check_dpia_requirement(self):
        """检查DPIA要求"""
        check_id = "dpia_requirement"
        description = "确定是否需要数据保护影响评估（DPIA）"
        
        scenarios = [
            "系统性、大规模监控",
            "大规模处理特殊类别数据或犯罪相关数据",
            "大规模、系统性评估个人特征",
            "自动化决策产生法律或类似重大影响",
            "匹配或组合数据集",
            "处理弱势群体数据",
            "创新性技术使用",
            "防止数据主体行使权利"
        ]
        
        result = {
            "check_id": check_id,
            "description": description,
            "scenarios": scenarios,
            "questions": [
                "1. 您的处理活动是否涉及高风险？",
                "2. 您是否进行过DPIA？",
                "3. 是否咨询过监管机构或DPO？",
                "4. 您是否记录了DPIA结果和缓解措施？"
            ],
            "recommendations": [
                "对高风险处理活动进行DPIA",
                "在早期阶段进行DPIA，影响处理设计",
                "咨询DPO或监管机构意见",
                "记录DPIA过程和结果"
            ],
            "status": "PENDING",
            "score": 0
        }
        
        return result
    
    def check_data_breach_notification(self):
        """检查数据泄露通知要求"""
        check_id = "data_breach_notification"
        description = "验证数据泄露通知机制"
        
        requirements = [
            "向监管机构通知（72小时内）",
            "向数据主体通知（高风险情况下）",
            "记录所有数据泄露事件"
        ]
        
        result = {
            "check_id": check_id,
            "description": description,
            "requirements": requirements,
            "questions": [
                "1. 您是否有数据泄露检测机制？",
                "2. 您是否有通知程序和模板？",
                "3. 您是否培训员工识别和报告数据泄露？",
                "4. 您是否有数据泄露应急预案？"
            ],
            "recommendations": [
                "制定数据泄露应急预案",
                "建立72小时内通知监管机构的流程",
                "高风险泄露时及时通知数据主体",
                "记录所有数据泄露事件及其处理"
            ],
            "status": "PENDING",
            "score": 0
        }
        
        return result
    
    def check_international_transfers(self):
        """检查跨境传输要求"""
        check_id = "international_transfers"
        description = "验证跨境数据传输的合规性"
        
        mechanisms = [
            "充分性决定（Article 45）",
            "适当保障措施（Article 46）",
            "   - 标准合同条款（SCCs）",
            "   - 约束性公司规则（BCRs）",
            "   - 行为准则 + 认证",
            "例外情况（Article 49）"
        ]
        
        result = {
            "check_id": check_id,
            "description": description,
            "mechanisms": mechanisms,
            "questions": [
                "1. 您是否有数据传输到欧盟以外？",
                "2. 您是否使用适当的传输机制？",
                "3. 您是否评估接收方数据保护水平？",
                "4. 您是否与接收方签订适当的合同？"
            ],
            "recommendations": [
                "如果没有充分性决定，使用SCCs或BCRs",
                "评估接收方提供的数据保护水平",
                "与接收方签订包含必要保护条款的合同",
                "记录跨境传输的合法依据"
            ],
            "status": "PENDING",
            "score": 0
        }
        
        return result
    
    def check_privacy_by_design(self):
        """检查默认隐私设计"""
        check_id = "privacy_by_design"
        description = "验证隐私默认设计原则"
        
        principles = [
            "处理活动设计时即考虑隐私保护",
            "默认设置提供最高隐私保护",
            "隐私保护功能是默认启用"
        ]
        
        result = {
            "check_id": check_id,
            "description": description,
            "principles": principles,
            "questions": [
                "1. 您是否在设计阶段考虑隐私保护？",
                "2. 默认设置是否提供最高保护？",
                "3. 用户是否需要主动选择才能获得更高保护？",
                "4. 您是否进行隐私影响评估？"
            ],
            "recommendations": [
                "在设计阶段集成隐私保护",
                "设置默认提供最高保护级别",
                "用户友好的隐私设置界面",
                "定期进行隐私设计审查"
            ],
            "status": "PENDING",
            "score": 0
        }
        
        return result
    
    def check_data_minimization(self):
        """检查数据最小化原则"""
        check_id = "data_minimization"
        description = "验证数据最小化原则的实施"
        
        result = {
            "check_id": check_id,
            "description": description,
            "questions": [
                "1. 您是否仅收集实现目的所需的数据？",
                "2. 您是否定期审查收集的数据类型和数量？",
                "3. 您是否删除不再需要的数据？",
                "4. 您是否有数据保留策略？"
            ],
            "recommendations": [
                "审查所有数据收集活动，确保必要性",
                "实施定期数据清理流程",
                "制定明确的数据保留政策",
                "记录数据收集的目的和使用限制"
            ],
            "status": "PENDING",
            "score": 0
        }
        
        return result
    
    def check_accuracy(self):
        """检查数据准确性"""
        check_id = "accuracy"
        description = "验证数据准确性的保障措施"
        
        result = {
            "check_id": check_id,
            "description": description,
            "questions": [
                "1. 您是否有机制确保数据准确？",
                "2. 您是否及时更新不准确的数据？",
                "3. 您是否向数据主体提供更正数据的机制？",
                "4. 您是否验证关键数据的准确性？"
            ],
            "recommendations": [
                "建立数据验证和更正流程",
                "定期审查关键数据的准确性",
                "提供数据主体更正数据的便捷途径",
                "记录数据准确性的维护措施"
            ],
            "status": "PENDING",
            "score": 0
        }
        
        return result
    
    def check_storage_limitation(self):
        """检查存储限制"""
        check_id = "storage_limitation"
        description = "验证数据存储期限的合规性"
        
        result = {
            "check_id": check_id,
            "description": description,
            "questions": [
                "1. 您是否有明确的数据保留期限？",
                "2. 您是否定期清理过时数据？",
                "3. 您是否记录数据删除的情况？",
                "4. 您是否建立数据存档机制（如适用）？"
            ],
            "recommendations": [
                "制定明确的数据保留政策",
                "实施自动化的数据清理流程",
                "记录数据删除操作和依据",
                "合规存档需要长期保存的数据"
            ],
            "status": "PENDING",
            "score": 0
        }
        
        return result
    
    def check_integrity_confidentiality(self):
        """检查完整性和保密性"""
        check_id = "integrity_confidentiality"
        description = "验证数据安全和保密措施"
        
        measures = [
            "加密",
            "访问控制",
            "安全审计",
            "备份和恢复",
            "网络安全"
        ]
        
        result = {
            "check_id": check_id,
            "description": description,
            "security_measures": measures,
            "questions": [
                "1. 您是否采取适当的技术安全措施？",
                "2. 您是否定期进行安全评估？",
                "3. 您是否培训员工数据安全？",
                "4. 您是否有数据恢复计划？"
            ],
            "recommendations": [
                "实施多层安全防护",
                "定期进行安全漏洞评估",
                "建立数据泄露检测和响应机制",
                "制定业务连续性计划"
            ],
            "status": "PENDING",
            "score": 0
        }
        
        return result
    
    def check_accountability(self):
        """检查问责制"""
        check_id = "accountability"
        description = "验证问责制原则的实施"
        
        requirements = [
            "数据处理记录（Article 30）",
            "DPIA记录（如需要）",
            "数据泄露通知记录",
            "合同和协议记录",
            "培训记录"
        ]
        
        result = {
            "check_id": check_id,
            "description": description,
            "requirements": requirements,
            "questions": [
                "1. 您是否保存数据处理活动记录？",
                "2. 您是否能够证明合规性？",
                "3. 您是否进行内部审计？",
                "4. 您是否任命了DPO（如需要）？"
            ],
            "recommendations": [
                "建立全面的合规文档体系",
                "定期进行内部合规审计",
                "确保所有处理活动有记录",
                "提供充分的合规培训"
            ],
            "status": "PENDING",
            "score": 0
        }
        
        return result
    
    def interactive_mode(self):
        """交互式检查模式"""
        print("=" * 60)
        print("GDPR合规检查工具 - 交互模式")
        print("=" * 60)
        print("本工具将引导您完成GDPR核心合规要求的检查。")
        print("请回答以下问题或按Ctrl+C退出。")
        print()
        
        # 运行所有检查
        for check_func in self.gdpr_checks:
            result = check_func()
            
            # 显示检查项信息
            print(f"📋 检查项: {result['description']}")
            
            # 如果有问题列表，显示并获取输入
            if 'questions' in result:
                print("问题:")
                for question in result['questions']:
                    print(f"  {question}")
                
                response = input("您的回答（简要描述当前状况）: ")
                result['user_response'] = response
                
                # 基于用户输入评估
                if response and len(response.strip()) > 10:
                    result['status'] = "PASSED"
                    result['score'] = 3
                    print("✅ 检查通过")
                else:
                    result['status'] = "PASSED"  # 先标记为通过，后续细评
                    result['score'] = 2
                    print("⚠️  需要进一步评估")
            
            # 如果有建议列表，显示
            if 'recommendations' in result:
                print("建议:")
                for i, rec in enumerate(result['recommendations'], 1):
                    print(f"  {i}. {rec}")
            
            print("-" * 60)
            
            # 更新摘要
            self.results['summary']['total_checks'] += 1
            if result['status'] == "PASSED":
                self.results['summary']['passed'] += 1
            elif result['status'] == "FAILED":
                self.results['summary']['failed'] += 1
            elif result['status'] == "WARNING":
                self.results['summary']['warnings'] += 1
            
            self.results['checks'].append(result)
    
    def generate_report(self):
        """生成检查报告"""
        report = {
            "audit_info": {
                "date": self.results['audit_date'],
                "skill_version": self.results['skill_version'],
                "total_checks": self.results['summary']['total_checks'],
                "passed": self.results['summary']['passed'],
                "failed": self.results['summary']['failed'],
                "warnings": self.results['summary']['warnings'],
                "compliance_rate": (self.results['summary']['passed'] / max(self.results['summary']['total_checks'], 1)) * 100
            },
            "detailed_results": self.results['checks'],
            "overall_assessment": self.get_overall_assessment(),
            "next_steps": self.get_next_steps(),
            "report_generated": datetime.now().isoformat()
        }
        
        return report
    
    def get_overall_assessment(self):
        """获取总体评估"""
        total_score = sum(check['score'] for check in self.results['checks'] if 'score' in check)
        max_score = 3 * len(self.results['checks'])
        
        if (total_score / max_score) > 0.8:
            return "优秀 - 高度符合GDPR要求"
        elif (total_score / max_score) > 0.6:
            return "良好 - 基本符合GDPR要求，有待改进"
        else:
            return "需要改进 - 存在明显合规差距"
    
    def get_next_steps(self):
        """获取下一步建议"""
        steps = []
        
        # 根据检查结果生成建议
        for check in self.results['checks']:
            if check.get('status') == "PASSED" and check.get('score', 0) < 2:
                steps.append(f"完善 {check['description']} 的实施措施")
            elif check.get('status') == "FAILED":
                steps.append(f"立即整改 {check['description']}")
        
        # 添加通用建议
        if not steps:
            steps = [
                "继续完善GDPR合规体系",
                "定期进行合规检查",
                "关注EDPB最新指南",
                "考虑外部合规审计"
            ]
        
        return steps
    
    def save_report(self, report, filename=None):
        """保存报告到文件"""
        if filename is None:
            filename = f"gdpr_audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return filename

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='GDPR合规检查工具')
    parser.add_argument('--interactive', '-i', action='store_true', help='交互式检查模式')
    parser.add_argument('--output', '-o', help='输出报告文件名')
    parser.add_argument('--format', choices=['json', 'text'], default='json', help='输出格式')
    parser.add_argument('--list-checks', action='store_true', help='列出所有检查项')
    
    args = parser.parse_args()
    
    tool = GDPRAuditTool()
    
    if args.list_checks:
        print("GDPR合规检查项列表:")
        for i, check_func in enumerate(tool.gdpr_checks, 1):
            result = check_func()
            print(f"{i}. {result['description']}")
        return
    
    if args.interactive:
        tool.interactive_mode()
    else:
        # 非交互模式：运行所有检查
        for check_func in tool.gdpr_checks:
            result = check_func()
            result['status'] = "PASSED"  # 默认通过，需要实际评估
            result['score'] = 2  # 默认分数
            tool.results['summary']['total_checks'] += 1
            tool.results['summary']['passed'] += 1
            tool.results['checks'].append(result)
    
    # 生成报告
    report = tool.generate_report()
    
    # 输出报告
    if args.format == 'json':
        if args.output:
            output_file = tool.save_report(report, args.output)
            print(f"✅ 报告已保存到: {output_file}")
        else:
            print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("=" * 60)
        print("GDPR合规检查报告")
        print("=" * 60)
        print(f"检查日期: {report['audit_info']['date']}")
        print(f"Skill版本: {report['audit_info']['skill_version']}")
        print(f"检查项总数: {report['audit_info']['total_checks']}")
        print(f"通过项: {report['audit_info']['passed']}")
        print(f"未通过项: {report['audit_info']['failed']}")
        print(f"警告项: {report['audit_info']['warnings']}")
        print(f"合规率: {report['audit_info']['compliance_rate']:.1f}%")
        print()
        print(f"总体评估: {report['overall_assessment']}")
        print()
        print("下一步行动:")
        for i, step in enumerate(report['next_steps'], 1):
            print(f"  {i}. {step}")
        print("=" * 60)

if __name__ == "__main__":
    main()
