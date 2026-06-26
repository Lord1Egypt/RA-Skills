#!/usr/bin/env python3
"""
GDPR跨境传输合规检查工具
版本：1.0.1
最后更新：2026年3月25日
"""

import json
import argparse
from datetime import datetime

class GDPRCrossBorderChecker:
    """GDPR跨境传输合规检查工具"""
    
    def __init__(self):
        self.results = {
            "check_date": datetime.now().isoformat(),
            "check_type": "GDPR_cross_border",
            "version": "1.0.1",
            "checks": []
        }
    
    def check_adequacy_decision(self):
        """检查充分性决定（Article 45）"""
        check = {
            "check_id": "adequacy_decision",
            "description": "检查是否向充分性决定国家传输数据",
            "questions": [
                "1. 您是否向欧盟委员会认可的国家传输数据？",
                "2. 您是否了解当前的充分性决定列表？",
                "3. 您是否定期检查充分性决定更新？"
            ],
            "recommendations": [
                "查阅欧盟委员会充分性决定列表",
                "仅向充分性决定国家传输数据",
                "定期检查充分性决定更新"
            ],
            "status": "PENDING"
        }
        return check
    
    def check_appropriate_safeguards(self):
        """检查适当保障措施（Article 46）"""
        check = {
            "check_id": "appropriate_safeguards",
            "description": "检查是否使用适当保障措施",
            "questions": [
                "1. 您是否使用标准合同条款（SCCs）？",
                "2. 您是否使用约束性公司规则（BCRs）？",
                "3. 您是否使用行为准则或认证？"
            ],
            "recommendations": [
                "使用最新的标准合同条款（SCCs）",
                "考虑实施约束性公司规则（BCRs）",
                "探索行业行为准则和认证"
            ],
            "status": "PENDING"
        }
        return check
    
    def check_standard_contractual_clauses(self):
        """检查标准合同条款（SCCs）"""
        check = {
            "check_id": "standard_contractual_clauses",
            "description": "检查标准合同条款的使用",
            "questions": [
                "1. 您是否使用最新版本的SCCs？",
                "2. 您的SCCs是否包含所有必要模块？",
                "3. 您是否进行SCCs补充评估？"
            ],
            "recommendations": [
                "使用欧盟委员会最新SCCs版本",
                "根据传输关系选择适当模块",
                "进行必要的补充评估"
            ],
            "status": "PENDING"
        }
        return check
    
    def check_binding_corporate_rules(self):
        """检查约束性公司规则（BCRs）"""
        check = {
            "check_id": "binding_corporate_rules",
            "description": "检查BCRs的适用性",
            "questions": [
                "1. 您的企业集团是否考虑使用BCRs？",
                "2. 您是否了解BCRs的审批流程？",
                "3. 您是否有资源实施BCRs？"
            ],
            "recommendations": [
                "评估BCRs对集团企业的适用性",
                "了解国家监管机构的审批要求",
                "准备必要的资源和文件"
            ],
            "status": "PENDING"
        }
        return check
    
    def check_derogations(self):
        """检查例外情况（Article 49）"""
        check = {
            "check_id": "derogations",
            "description": "检查是否适用例外情况",
            "questions": [
                "1. 您是否基于明确同意进行传输？",
                "2. 您是否因合同履行需要传输？",
                "3. 您是否因重大公共利益传输？"
            ],
            "recommendations": [
                "仅在例外情况下使用Article 49",
                "确保例外情况适用且记录充分",
                "定期审查例外情况的使用"
            ],
            "status": "PENDING"
        }
        return check
    
    def check_third_country_recipients(self):
        """检查第三国接收方"""
        check = {
            "check_id": "third_country_recipients",
            "description": "检查第三国接收方的合规性",
            "questions": [
                "1. 您是否评估接收方数据保护水平？",
                "2. 您是否与接收方签订适当合同？",
                "3. 您是否监控接收方的合规性？"
            ],
            "recommendations": [
                "评估接收方国家的数据保护法律",
                "签订包含必要保护条款的合同",
                "建立接收方合规监控机制"
            ],
            "status": "PENDING"
        }
        return check
    
    def check_data_transfer_impact_assessment(self):
        """检查数据传输影响评估"""
        check = {
            "check_id": "data_transfer_impact_assessment",
            "description": "检查是否进行数据传输影响评估",
            "questions": [
                "1. 您是否进行数据传输影响评估？",
                "2. 您是否评估接收国法律环境？",
                "3. 您是否实施额外保护措施？"
            ],
            "recommendations": [
                "对高风险传输进行影响评估",
                "评估接收国法律和实践环境",
                "实施必要的额外保护措施"
            ],
            "status": "PENDING"
        }
        return check
    
    def run_checks(self):
        """运行所有检查"""
        checks = [
            self.check_adequacy_decision,
            self.check_appropriate_safeguards,
            self.check_standard_contractual_clauses,
            self.check_binding_corporate_rules,
            self.check_derogations,
            self.check_third_country_recipients,
            self.check_data_transfer_impact_assessment
        ]
        
        for check_func in checks:
            check = check_func()
            self.results["checks"].append(check)
    
    def interactive_mode(self):
        """交互式检查模式"""
        print("="*60)
        print("GDPR跨境传输合规检查工具")
        print("="*60)
        
        for check in self.results["checks"]:
            print(f"\n📋 检查项: {check['description']}")
            print("问题:")
            for question in check['questions']:
                print(f"  {question}")
            
            response = input("\n您的回答（简要描述当前状况）: ")
            check["user_response"] = response
            check["status"] = "COMPLETED"
    
    def save_report(self, filename=None):
        """保存检查报告"""
        if not filename:
            filename = f"gdpr_cross_border_check_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        return filename

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='GDPR跨境传输合规检查工具')
    parser.add_argument('--interactive', '-i', action='store_true', help='交互式检查模式')
    parser.add_argument('--output', '-o', help='输出报告文件名')
    parser.add_argument('--list-checks', action='store_true', help='列出所有检查项')
    
    args = parser.parse_args()
    
    checker = GDPRCrossBorderChecker()
    
    if args.list_checks:
        print("GDPR跨境传输合规检查项:")
        print("1. 充分性决定 (Article 45)")
        print("2. 适当保障措施 (Article 46)")
        print("3. 标准合同条款 (SCCs)")
        print("4. 约束性公司规则 (BCRs)")
        print("5. 例外情况 (Article 49)")
        print("6. 第三国接收方评估")
        print("7. 数据传输影响评估")
        return
    
    if args.interactive:
        checker.run_checks()
        checker.interactive_mode()
    else:
        checker.run_checks()
    
    report = checker.save_report(args.output)
    
    print(f"\n✅ 检查完成！报告已保存到: {report}")
    print("="*60)

if __name__ == "__main__":
    main()