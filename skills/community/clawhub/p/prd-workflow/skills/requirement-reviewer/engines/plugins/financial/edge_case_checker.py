#!/usr/bin/env python3
"""
边界和异常场景检查引擎 v1.0

检查 PRD 是否考虑了边界场景和异常处理
"""

import re
from typing import List, Dict


class EdgeCaseChecker:
    """边界和异常场景检查引擎"""
    
    # 边界场景分类
    EDGE_CASE_CATEGORIES = {
        "交易流程": [
            "网络中断",
            "支付失败",
            "超时",
            "并发请求",
            "数据不一致",
            "重复提交",
            "回滚",
            "交易撤销"
        ],
        "数据输入": [
            "空值",
            "null",
            "超大数据",
            "非法格式",
            "特殊字符",
            "SQL 注入",
            "XSS 攻击",
            "超长文本"
        ],
        "用户权限": [
            "未授权访问",
            "越权操作",
            "会话过期",
            "多设备登录",
            "账号冻结",
            "密码错误"
        ],
        "系统异常": [
            "服务不可用",
            "数据库连接失败",
            "第三方接口失败",
            "内存溢出",
            "磁盘空间不足",
            "CPU 过载"
        ],
        "数据展示": [
            "数据为空",
            "数据加载失败",
            "分页异常",
            "排序异常",
            "筛选无结果"
        ]
    }
    
    def check(self, prd_content: str) -> Dict:
        """
        检查边界和异常场景
        
        参数:
            prd_content: PRD 文档内容
            
        返回:
            {
                "check_type": "edge_cases",
                "score": 75,
                "issues": [...],
                "category_scores": {...}
            }
        """
        issues = []
        category_scores = {}
        
        # 检查每个类别
        for category, patterns in self.EDGE_CASE_CATEGORIES.items():
            category_result = self.check_category(prd_content, category, patterns)
            
            if category_result["issues"]:
                issues.extend(category_result["issues"])
            
            category_scores[category] = category_result["score"]
        
        # 计算总分
        total_score = sum(category_scores.values()) // len(category_scores) if category_scores else 0
        
        return {
            "check_type": "edge_cases",
            "score": total_score,
            "status": "pass" if total_score >= 80 else "warning" if total_score >= 60 else "fail",
            "issues": issues,
            "category_scores": category_scores,
            "total_categories": len(self.EDGE_CASE_CATEGORIES),
            "passed_categories": sum(1 for score in category_scores.values() if score >= 80)
        }
    
    def check_category(self, prd_content: str, category: str, patterns: List[str]) -> Dict:
        """检查单个类别的边界场景"""
        issues = []
        mentioned = []
        missing = []
        
        # 检查每个场景是否被提及
        for pattern in patterns:
            # 支持多种表述方式
            pattern_variants = [
                pattern,
                f"{pattern}处理",
                f"{pattern}异常",
                f"处理{pattern}",
                f"{pattern}场景",
                f"{pattern}情况"
            ]
            
            is_mentioned = any(variant in prd_content for variant in pattern_variants)
            
            if is_mentioned:
                mentioned.append(pattern)
            else:
                missing.append(pattern)
        
        # 如果缺失超过 50%，记录问题
        if len(missing) > len(patterns) * 0.5:
            issues.append({
                "type": "missing_edge_cases",
                "category": category,
                "severity": "medium",
                "title": f"{category}缺少边界场景考虑",
                "description": f"{category}缺少{len(missing)}个边界场景的处理说明",
                "missing_count": len(missing),
                "missing_items": missing[:5],  # 只显示前 5 个
                "mentioned_items": mentioned,
                "suggestion": f"建议补充{category}的边界场景处理，如：{', '.join(missing[:3])}"
            })
        
        # 计算类别得分
        score = int((len(mentioned) / len(patterns)) * 100) if patterns else 0
        
        return {
            "category": category,
            "score": score,
            "mentioned": mentioned,
            "missing": missing,
            "issues": issues
        }
    
    def check_exception_handling(self, prd_content: str) -> List[Dict]:
        """检查异常处理流程"""
        issues = []
        
        # 检查是否有统一的异常处理说明
        exception_keywords = [
            "异常处理",
            "错误处理",
            "容错",
            "降级",
            "重试",
            "回滚",
            "补偿"
        ]
        
        has_exception_handling = any(keyword in prd_content for keyword in exception_keywords)
        
        if not has_exception_handling:
            issues.append({
                "type": "missing_exception_handling",
                "severity": "high",
                "title": "缺少异常处理流程",
                "description": "未定义统一的异常处理机制",
                "location": "非功能需求章节",
                "suggestion": "补充异常分类、处理流程、错误提示、恢复机制等设计"
            })
        
        return issues
    
    def check_error_messages(self, prd_content: str) -> List[Dict]:
        """检查错误提示设计"""
        issues = []
        
        # 检查是否有错误提示说明
        error_keywords = [
            "错误提示",
            "提示信息",
            "错误码",
            "用户提示",
            "异常提示"
        ]
        
        has_error_messages = any(keyword in prd_content for keyword in error_keywords)
        
        if not has_error_messages:
            issues.append({
                "type": "missing_error_messages",
                "severity": "medium",
                "title": "缺少错误提示设计",
                "description": "未定义错误提示规则",
                "location": "界面设计章节",
                "suggestion": "补充错误提示文案规范、提示方式（Toast/Dialog）、错误码定义等"
            })
        
        return issues


# 测试
if __name__ == "__main__":
    # 测试用例
    test_prd = """
    # AI 养老规划助手 PRD
    
    ## 功能设计
    
    ### 交易流程
    支持网络中断后的重试机制
    支付失败时提示用户
    
    ### 数据输入
    支持空值校验
    """
    
    checker = EdgeCaseChecker()
    result = checker.check(test_prd)
    
    print("边界场景检查结果:")
    print(f"得分：{result['score']}/100")
    print(f"问题数：{len(result['issues'])}")
    print(f"类别得分：{result['category_scores']}")
    for issue in result['issues']:
        print(f"  - [{issue['severity']}] {issue['title']}: {issue['description']}")
