#!/usr/bin/env python3
"""
GDPR数据主体权利检查工具
版本：1.0.1
最后更新：2026年3月25日
"""

import json
import argparse
from datetime import datetime

class GDPRDataRightsChecker:
    """GDPR数据主体权利检查工具"""
    
    def __init__(self):
        self.results = {
            "check_date": datetime.now().isoformat(),
            "check_type": "GDPR_data_rights",
            "version": "1.0.1",
            "checks": []
        }
    
    def check_right_to_be_informed(self):
        """检查知情权（Articles 13-14）"""
        check = {
            "check_id": "right_to_be_informed",
            "description": "检查是否提供清晰易懂的隐私声明",
            "questions": [
                "1. 是否在数据收集时提供信息？",
                "2. 隐私声明是否包含所有必要信息？",
                "3. 信息是否以清晰易懂的语言提供？"
            ],
            "recommendations": [
                "在数据收集点提供清晰的隐私声明",
                "包含所有GDPR要求的信息",
                "使用简单明了的语言"
            ],
            "status": "PENDING"
        }
        return check
    
    def check_right_of_access(self):
        """检查访问权（Article 15）"""
        check = {
            "check_id": "right_of_access",
            "description": "检查是否提供数据访问机制",
            "questions": [
                "1. 是否有处理数据访问请求的机制？",
                "2. 是否在合理时间内提供信息？",
                "3. 是否免费提供首次数据副本？"
            ],
            "recommendations": [
                "建立标准化的访问请求处理流程",
                "确保在法定期限内响应",
                "提供电子格式的数据副本"
            ],
            "status": "PENDING"
        }
        return check
    
    def check_right_to_rectification(self):
        """检查更正权（Article 16）"""
        check = {
            "check_id": "right_to_rectification",
            "description": "检查数据更正机制",
            "questions": [
                "1. 是否有更正不准确数据的机制？",
                "2. 是否及时处理更正请求？",
                "3.是否通知数据接收方（如需要）？"
            ],
            "recommendations": [
                "建立数据验证和更正流程",
                "及时处理更正请求",
                "通知第三方数据接收方（如适用）"
            ],
            "status": "PENDING"
        }
        return check
    
    def check_right_to_erasure(self):
        """检查删除权（Article 17）"""
        check = {
            "check_id": "right_to_erasure",
            "description": "检查数据删除机制",
            "questions": [
                "1.是否有处理删除请求的机制？",
                "2.是否了解删除权的例外情况？",
                "3.是否通知第三方数据接收方（如需要）？"
            ],
            "recommendations": [
                "建立标准化的删除请求流程",
                "了解Article 17的例外情况",
                "通知第三方数据接收方（如适用）"
            ],
            "status": "PENDING"
        }
        return check
    
    def check_right_to_restriction(self):
        """检查限制处理权（Article 18）"""
        check = {
            "check_id": "right_to_restriction",
            "description": "检查限制处理机制",
            "questions": [
                "1.是否有处理限制处理请求的机制？",
                "2.是否了解可以限制处理的情况？",
                "3.是否记录限制处理请求？"
            ],
            "recommendations": [
                "建立限制处理请求流程",
                "了解可以限制处理的情况",
                "详细记录所有限制处理请求"
            ],
            "status": "PENDING"
        }
        return check
    
    def check_right_to_data_portability(self):
        """检查数据可携权（Article 20）"""
        check = {
            "check_id": "right_to_data_portability",
            "description": "检查数据可携机制",
            "questions": [
                "1. 是否有提供可携格式数据的机制？",
                "2. 是否提供结构化、常用、机器可读格式？",
                "3. 在技术可行时是否允许直接传输？"
            ],
            "recommendations": [
                "建立数据可携请求处理流程",
                "提供JSON、XML等标准格式",
                "允许技术可行的直接数据传输"
            ],
            "status": "PENDING"
        }
        return check
    
    def check_right_to_object(self):
        """检查反对权（Article 21）"""
        check = {
            "check_id": "right_to_object",
            "description": "检查反对处理机制",
            "questions": [
                "1. 是否有处理反对请求的机制？",
                "2. 是否允许反对基于合法利益的处理？",
                "3. 是否允许反对直接营销？"
            ],
            "recommendations": [
                "建立反对请求处理流程",
                "尊重数据主体反对基于合法利益处理的权利",
                "尊重数据主体反对直接营销的权利"
            ],
            "status": "PENDING"
        }
        return check
    
    def run_checks(self):
        """运行所有检查"""
        checks = [
            self.check_right_to_be_informed,
            self.check_right_of_access,
            self.check_right_to_rectification,
            self.check_right_to_erasure,
            self.check_right_to_restriction,
            self.check_right_to_data_portability,
            self.check_right_to_object
        ]
        
        for check_func in checks:
            check = check_func()
            self.results["checks"].append(check)
    
    def interactive_mode(self):
        """交互式检查模式"""
        print("="*60)
        print("GDPR数据主体权利检查工具")
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
            filename = f"gdpr_data_rights_check_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        return filename

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='GDPR数据主体权利检查工具')
    parser.add_argument('--interactive', '-i', action='store_true', help='交互式检查模式')
    parser.add_argument('--output', '-o', help='输出报告文件名')
    parser.add_argument('--list-checks', action='store_true', help='列出所有检查项')
    
    args = parser.parse_args()
    
    checker = GDPRDataRightsChecker()
    
    if args.list_checks:
        print("GDPR数据主体权利检查项:")
        print("1. 知情权 (Articles 13-14)")
        print("2. 访问权 (Article 15)")
        print("3. 更正权 (Article 16)")
        print("4. 删除权 (Article 17)")
        print("5. 限制处理权 (Article 18)")
        print("6. 数据可携权 (Article 20)")
        print("7. 反对权 (Article 21)")
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