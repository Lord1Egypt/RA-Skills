#!/usr/bin/env python3
"""
LLM 智能分析模块
结合大语言模型对安全扫描结果进行智能分析和修复建议生成

作者：北京老李
版本：2.1.0
"""

import os
import json
from typing import Dict, List, Optional
from pathlib import Path


class LLMAnalyzer:
    """LLM 智能分析器
    
    ⚠️ 安全提示:
    - 此模块会将代码片段发送到外部 API 进行分析
    - 默认 API 端点：https://dashscope.aliyuncs.com/compatible-mode/v1
    - 敏感代码建议使用私有 API 端点或禁用 LLM 功能
    - 可通过 LLM_API_BASE 环境变量配置私有端点
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "qwen3.5-plus"):
        self.api_key = api_key or os.environ.get('LLM_API_KEY')
        self.model = model
        self.api_base = os.environ.get('LLM_API_BASE', 'https://dashscope.aliyuncs.com/compatible-mode/v1')
        
        # 安全警告
        if self.api_key:
            print(f"⚠️  LLM 分析已启用 - 代码数据将发送到：{self.api_base}")
            print(f"⚠️  敏感代码建议使用私有 API 端点或禁用 LLM 功能")
    
    def analyze_security_issue(self, issue_type: str, code_snippet: str, 
                               file_path: str, line_number: int = 0) -> Dict:
        """分析单个安全问题"""
        
        prompt = f"""你是一个 Python 安全专家。请分析以下安全问题并提供修复建议。

**问题类型**: {issue_type}
**文件路径**: {file_path}
**行号**: {line_number}
**代码片段**:
```python
{code_snippet}
```

请按以下格式回答：

## 风险分析
- 风险等级：[高/中/低]
- 可能影响：[描述可能的安全影响]
- 攻击场景：[描述可能的攻击方式]

## 修复建议
- 推荐方案：[具体的修复代码]
- 替代方案：[其他可选方案]
- 最佳实践：[相关的安全最佳实践]

## 参考资源
- [相关的 CWE 编号]
- [相关的 OWASP 条目]
- [官方文档链接]
"""
        
        # 调用 LLM API
        result = self._call_llm(prompt)
        
        return {
            'issue_type': issue_type,
            'file': file_path,
            'line': line_number,
            'code': code_snippet,
            'analysis': result,
            'risk_level': self._extract_risk_level(result)
        }
    
    def generate_privacy_report(self, scan_results: Dict) -> str:
        """生成隐私安全分析报告"""
        
        prompt = f"""你是一个隐私保护专家。请根据以下扫描结果生成隐私安全分析报告。

**扫描结果**:
{json.dumps(scan_results, indent=2, ensure_ascii=False)}

请生成隐私安全分析报告，包括：

1. 个人信息泄露风险
2. 数据处理合规性
3. 隐私保护建议
4. 相关法规参考（GDPR、个人信息保护法等）
"""
        
        return self._call_llm(prompt)
    
    def generate_data_security_report(self, scan_results: Dict) -> str:
        """生成数据安全分析报告"""
        
        prompt = f"""你是一个数据安全专家。请根据以下扫描结果生成数据安全分析报告。

**扫描结果**:
{json.dumps(scan_results, indent=2, ensure_ascii=False)}

请生成数据安全分析报告，包括：

1. 数据加密情况
2. 数据传输安全
3. 数据存储安全
4. 访问控制建议
5. 相关标准参考（等保 2.0、ISO27001 等）
"""
        
        return self._call_llm(prompt)
    
    def prioritize_issues(self, issues: List[Dict]) -> List[Dict]:
        """对问题进行优先级排序"""
        
        prompt = f"""你是一个安全专家。请对以下安全问题进行优先级排序。

**问题列表**:
{json.dumps(issues, indent=2, ensure_ascii=False)}

请按以下标准排序：
1. 风险等级（高/中/低）
2. 利用难度
3. 影响范围
4. 修复紧急程度

返回排序后的问题列表，包含优先级评分（1-10，10 为最紧急）。
"""
        
        result = self._call_llm(prompt)
        return self._parse_priority_result(result, issues)
    
    def generate_remediation_plan(self, issues: List[Dict]) -> str:
        """生成修复计划"""
        
        prompt = f"""你是一个安全顾问。请根据以下安全问题生成详细的修复计划。

**问题列表**:
{json.dumps(issues, indent=2, ensure_ascii=False)}

请生成修复计划，包括：

1. 立即修复（24 小时内）
   - 问题列表
   - 修复步骤
   - 验证方法

2. 短期修复（1 周内）
   - 问题列表
   - 修复步骤
   - 验证方法

3. 长期改进（1 个月内）
   - 改进建议
   - 实施计划
   - 验收标准

4. 持续监控
   - 监控指标
   - 告警规则
   - 响应流程
"""
        
        return self._call_llm(prompt)
    
    def _call_llm(self, prompt: str) -> str:
        """调用 LLM API"""
        
        if not self.api_key:
            return self._fallback_analysis(prompt)
        
        try:
            import requests
            
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'model': self.model,
                'messages': [
                    {'role': 'system', 'content': '你是一个专业的 Python 安全专家和隐私保护顾问。'},
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.3,
                'max_tokens': 2000
            }
            
            response = requests.post(
                f'{self.api_base}/chat/completions',
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                print(f"⚠️ LLM API 调用失败：{response.status_code}")
                return self._fallback_analysis(prompt)
                
        except Exception as e:
            print(f"⚠️ LLM 调用异常：{e}")
            return self._fallback_analysis(prompt)
    
    def _fallback_analysis(self, prompt: str) -> str:
        """降级分析（无 LLM 时）"""
        
        # 基于规则的简单分析
        if '风险分析' in prompt:
            return """## 风险分析
- 风险等级：中
- 可能影响：可能导致安全风险
- 攻击场景：攻击者可能利用此漏洞

## 修复建议
- 推荐方案：参考相关安全最佳实践进行修复
- 替代方案：使用安全库替代
- 最佳实践：遵循 OWASP 安全指南

## 参考资源
- CWE: 参考相关 CWE 编号
- OWASP: https://owasp.org/
"""
        elif '隐私' in prompt:
            return """# 隐私安全分析报告

## 个人信息保护
- 建议加密存储个人数据
- 实施访问控制
- 定期审计数据使用

## 合规建议
- 遵循《个人信息保护法》
- 参考 GDPR 要求
- 实施隐私设计原则
"""
        elif '数据安全' in prompt:
            return """# 数据安全分析报告

## 加密建议
- 传输使用 TLS 1.3
- 存储使用 AES-256
- 密钥使用 KMS 管理

## 访问控制
- 实施最小权限原则
- 多因素认证
- 定期审计权限
"""
        else:
            return "建议参考相关安全最佳实践进行修复。"
    
    def _extract_risk_level(self, analysis: str) -> str:
        """从分析结果中提取风险等级"""
        if '高' in analysis or 'High' in analysis:
            return 'high'
        elif '中' in analysis or 'Medium' in analysis:
            return 'medium'
        else:
            return 'low'
    
    def _parse_priority_result(self, result: str, issues: List[Dict]) -> List[Dict]:
        """解析优先级排序结果"""
        # 简单实现，实际应解析 LLM 返回
        for i, issue in enumerate(issues):
            issue['priority'] = len(issues) - i  # 简单倒序
        return issues


class PrivacyChecker:
    """隐私安全检查器"""
    
    def __init__(self):
        self.privacy_patterns = {
            '身份证号': r'\d{17}[\dXx]|\d{15}',
            '手机号': r'1[3-9]\d{9}',
            '邮箱': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            '银行卡': r'\d{16}|\d{19}',
            '密码': r'(?i)(password|passwd|pwd|secret)\s*[=:]\s*[\'"][^\'"]+[\'"]',
            'API 密钥': r'(?i)(api_key|apikey|token|access_token)\s*[=:]\s*[\'"][^\'"]+[\'"]',
            'AWS 密钥': r'AKIA[0-9A-Z]{16}',
            'GitHub Token': r'gh[pousr]_[A-Za-z0-9_]{36,}',
        }
    
    def check_file(self, file_path: Path) -> List[Dict]:
        """检查文件中的隐私信息"""
        issues = []
        
        try:
            content = file_path.read_text()
            lines = content.split('\n')
            
            for pattern_name, pattern in self.privacy_patterns.items():
                import re
                for i, line in enumerate(lines, 1):
                    matches = re.findall(pattern, line)
                    if matches:
                        # 排除示例文件和测试文件
                        if 'example' in str(file_path).lower() or 'test' in str(file_path).lower():
                            continue
                        
                        issues.append({
                            'type': 'privacy_leak',
                            'subtype': pattern_name,
                            'file': str(file_path),
                            'line': i,
                            'content': line.strip()[:100],  # 只保留前 100 字符
                            'severity': 'high' if pattern_name in ['密码', 'API 密钥', 'AWS 密钥'] else 'medium'
                        })
        except Exception as e:
            pass
        
        return issues
    
    def generate_report(self, issues: List[Dict]) -> str:
        """生成隐私检查报告"""
        
        report = """# 隐私安全检查报告

## 检查摘要

"""
        
        if not issues:
            report += "✅ 未发现明显的隐私信息泄露\n"
        else:
            report += f"❌ 发现 {len(issues)} 个隐私信息泄露风险\n\n"
            
            # 按类型分组
            by_type = {}
            for issue in issues:
                subtype = issue['subtype']
                if subtype not in by_type:
                    by_type[subtype] = []
                by_type[subtype].append(issue)
            
            report += "## 问题详情\n\n"
            for subtype, type_issues in by_type.items():
                report += f"### {subtype} ({len(type_issues)} 个)\n\n"
                for issue in type_issues[:5]:  # 只显示前 5 个
                    report += f"- **文件**: {issue['file']}:{issue['line']}\n"
                    report += f"  ```\n  {issue['content']}\n  ```\n\n"
            
            if len(issues) > 5:
                report += f"... 还有 {len(issues) - 5} 个问题，请查看完整报告\n\n"
        
        report += """
## 修复建议

### 立即修复
1. 删除代码中的敏感信息
2. 使用环境变量或配置管理系统
3. 轮换已泄露的密钥

### 长期改进
1. 实施密钥管理系统（KMS）
2. 使用预提交钩子检测敏感信息
3. 定期进行安全审计

## 参考标准
- 《中华人民共和国个人信息保护法》
- GDPR（通用数据保护条例）
- ISO/IEC 29100 隐私框架
"""
        
        return report


class DataSecurityChecker:
    """数据安全检查器"""
    
    def __init__(self):
        self.data_security_checks = {
            '数据库密码硬编码': r'(?i)(mysql|postgres|mongodb|redis).*:\/\/.*:.*@',
            '弱加密算法': r'(?i)(DES|MD5|SHA1|RC4)',
            '不安全随机数': r'(?i)random\.(randint|choice|random)',
            '明文传输': r'http:\/\/(?!localhost|127\.0\.0\.1)',
            'SQL 注入': r'execute\s*\([^)]*%|execute\s*\(.*\.format|execute\s*\(.*\+',
        }
    
    def check_file(self, file_path: Path) -> List[Dict]:
        """检查文件的数据安全问题"""
        issues = []
        
        try:
            content = file_path.read_text()
            lines = content.split('\n')
            
            for check_name, pattern in self.data_security_checks.items():
                import re
                for i, line in enumerate(lines, 1):
                    if re.search(pattern, line):
                        issues.append({
                            'type': 'data_security',
                            'subtype': check_name,
                            'file': str(file_path),
                            'line': i,
                            'content': line.strip()[:100],
                            'severity': 'high' if check_name in ['数据库密码硬编码', '弱加密算法'] else 'medium'
                        })
        except Exception as e:
            pass
        
        return issues
    
    def generate_report(self, issues: List[Dict]) -> str:
        """生成数据安全检查报告"""
        
        report = """# 数据安全检查报告

## 检查摘要

"""
        
        if not issues:
            report += "✅ 未发现明显的数据安全问题\n"
        else:
            report += f"❌ 发现 {len(issues)} 个数据安全风险\n\n"
            
            # 按严重程度分组
            high_issues = [i for i in issues if i['severity'] == 'high']
            medium_issues = [i for i in issues if i['severity'] == 'medium']
            
            if high_issues:
                report += f"### 🔴 高风险 ({len(high_issues)} 个)\n\n"
                for issue in high_issues[:5]:
                    report += f"- **{issue['subtype']}**: {issue['file']}:{issue['line']}\n"
                report += "\n"
            
            if medium_issues:
                report += f"### 🟡 中风险 ({len(medium_issues)} 个)\n\n"
                for issue in medium_issues[:5]:
                    report += f"- **{issue['subtype']}**: {issue['file']}:{issue['line']}\n"
                report += "\n"
        
        report += """
## 修复建议

### 数据加密
- ✅ 传输加密：使用 HTTPS/TLS 1.3
- ✅ 存储加密：使用 AES-256
- ✅ 密钥管理：使用 KMS 或 HSM

### 访问控制
- ✅ 最小权限原则
- ✅ 多因素认证
- ✅ 定期审计权限

### 数据保护
- ✅ 数据分类分级
- ✅ 敏感数据脱敏
- ✅ 数据备份和恢复

## 参考标准
- 网络安全等级保护 2.0
- ISO/IEC 27001 信息安全管理体系
- GB/T 35273-2020 个人信息安全规范
"""
        
        return report


if __name__ == '__main__':
    # 测试
    print("LLM 智能分析模块测试")
    
    analyzer = LLMAnalyzer()
    privacy_checker = PrivacyChecker()
    data_security_checker = DataSecurityChecker()
    
    print("✅ 模块加载成功")
