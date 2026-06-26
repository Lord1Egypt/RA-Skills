#!/usr/bin/env python3
"""
AI 内容检查器 v1.0

⚠️ DEPRECATED - 此文件已废弃
============================
新架构不再使用此文件进行 AI 检查。

新架构流程：
1. get_tasks_cli.py 提取检查任务（纯逻辑）
2. review_module.js 使用 aiExecutor 调用 AI（OpenClaw架构）

此文件保留作为备份参考。

原功能：
- 构建检查 Prompt
- 调用 AI 进行内容理解 ❌（改为 aiExecutor）
- 解析检查结果
- 生成结构化问题列表
"""

import json
import os
import requests
from typing import List, Dict, Optional
from dataclasses import dataclass

from .check_items import CHECK_ITEMS, CheckItem, Priority
from .section_matcher import CheckTask


@dataclass
class ContentIssue:
    """内容问题"""
    check_item: CheckItem      # 检查项
    section_title: str         # 章节标题
    issue_description: str     # 问题描述
    suggestion: str            # 修补建议
    original_text: str         # 原文引用
    priority: Priority         # 优先级


class AIContentChecker:
    """AI 内容检查器"""

    # AI 检查 Prompt 模板
    CHECK_PROMPT_TEMPLATE = """你是一个专业的软件需求文档评审专家。请检查以下内容是否符合"{check_name}"的要求。

## 检查项说明
- 名称：{check_name}
- 描述：{check_description}
- 检查要点：
{check_points}

## 良好示例
{example_good}

## 不良示例
{example_bad}

## 待检查内容
章节：{section_title}
内容：
```
{content}
```

## 检查要求
1. 仔细阅读内容，判断是否符合检查项要求
2. 如果存在问题，请明确指出问题所在
3. 给出具体的修补建议
4. 引用原文中有问题的部分

## 输出格式（JSON）
```json
{{
    "passed": true/false,
    "issues": [
        {{
            "description": "问题描述",
            "suggestion": "修补建议",
            "original_text": "原文引用"
        }}
    ]
}}
```

请直接输出 JSON，不要有其他内容。"""

    def __init__(self, api_config: Dict = None):
        """
        初始化

        参数:
            api_config: API 配置
                - api_key: API密钥
                - base_url: API地址
                - model: 模型名称
        """
        self.api_config = api_config or self._load_config()

    def _load_config(self) -> Dict:
        """加载 API 配置"""
        # 尝试从环境变量加载
        config = {
            "api_key": os.getenv("OPENAI_API_KEY", ""),
            "base_url": os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
            "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        }

        # 尝试从配置文件加载
        config_path = os.path.expanduser("~/.openclaw/workspace/skills/prd-workflow/config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    file_config = json.load(f)
                    config.update(file_config)
            except:
                pass

        return config

    def check_task(self, task: CheckTask) -> List[ContentIssue]:
        """
        执行单个检查任务

        参数:
            task: 检查任务

        返回:
            问题列表
        """
        # 构建 Prompt
        prompt = self._build_prompt(task)

        # 调用 AI
        response = self._call_ai(prompt)

        # 解析结果
        issues = self._parse_response(response, task)

        return issues

    def check_all(self, tasks: List[CheckTask]) -> List[ContentIssue]:
        """
        执行所有检查任务

        参数:
            tasks: 检查任务列表

        返回:
            所有问题列表
        """
        import sys
        all_issues = []

        for i, task in enumerate(tasks):
            print(f"   检查 [{i+1}/{len(tasks)}]: {task.check_item.name}...", file=sys.stderr)
            issues = self.check_task(task)
            all_issues.extend(issues)

        return all_issues

    def _build_prompt(self, task: CheckTask) -> str:
        """构建检查 Prompt"""
        check_item = task.check_item

        # 格式化检查要点
        check_points = "\n".join([f"  - {p}" for p in check_item.check_points])

        prompt = self.CHECK_PROMPT_TEMPLATE.format(
            check_name=check_item.name,
            check_description=check_item.description,
            check_points=check_points,
            example_good=check_item.example_good,
            example_bad=check_item.example_bad,
            section_title=task.section.title if task.section else "全文",
            content=task.content[:3000] if len(task.content) > 3000 else task.content  # 限制长度
        )

        return prompt

    def _call_ai(self, prompt: str) -> str:
        """调用 AI API"""
        if not self.api_config.get("api_key"):
            # 模拟返回（无 API 时）
            return '{"passed": true, "issues": []}'

        try:
            headers = {
                "Authorization": f"Bearer {self.api_config['api_key']}",
                "Content-Type": "application/json"
            }

            data = {
                "model": self.api_config.get("model", "gpt-4o-mini"),
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 1000
            }

            response = requests.post(
                f"{self.api_config['base_url']}/chat/completions",
                headers=headers,
                json=data,
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                print(f"   ⚠️ API 调用失败: {response.status_code}")
                return '{"passed": true, "issues": []}'

        except Exception as e:
            print(f"   ⚠️ API 调用异常: {e}")
            return '{"passed": true, "issues": []}'

    def _parse_response(self, response: str, task: CheckTask) -> List[ContentIssue]:
        """解析 AI 返回结果"""
        issues = []

        try:
            # 提取 JSON
            json_match = response
            if "```json" in response:
                json_match = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                json_match = response.split("```")[1].split("```")[0]

            result = json.loads(json_match.strip())

            if not result.get("passed", True):
                for issue_data in result.get("issues", []):
                    issues.append(ContentIssue(
                        check_item=task.check_item,
                        section_title=task.section.title if task.section else "全文",
                        issue_description=issue_data.get("description", ""),
                        suggestion=issue_data.get("suggestion", ""),
                        original_text=issue_data.get("original_text", ""),
                        priority=task.check_item.priority
                    ))

        except json.JSONDecodeError as e:
            print(f"   ⚠️ JSON 解析失败: {e}")
        except Exception as e:
            print(f"   ⚠️ 结果解析异常: {e}")

        return issues

    def generate_fix(self, issue: ContentIssue, user_instruction: str = None) -> str:
        """
        生成修补内容

        参数:
            issue: 内容问题
            user_instruction: 用户指令（可选）

        返回:
            修补内容
        """
        prompt = f"""你是一个专业的软件需求文档编写专家。请根据以下问题生成修补内容。

## 问题描述
- 检查项：{issue.check_item.name}
- 章节：{issue.section_title}
- 问题：{issue.issue_description}
- 建议：{issue.suggestion}

## 原文
{issue.original_text}

## 用户要求
{user_instruction if user_instruction else "请自动生成合适的修补内容"}

## 输出要求
1. 直接输出修补后的内容（不要包含原文）
2. 保持专业、准确、完整
3. 使用 Markdown 格式

请直接输出修补内容："""

        response = self._call_ai(prompt)
        return response


if __name__ == "__main__":
    # 测试用例
    from .section_matcher import SectionMatcher

    test_prd = """
## 业务流程
用户点击下单按钮，系统处理下单请求。

## 功能 1：下单功能
输入：金额
输出：订单号

## 验收标准
功能正常
"""

    # 创建检查器
    checker = AIContentChecker()
    matcher = SectionMatcher()

    # 获取检查任务
    tasks = matcher.get_all_tasks(test_prd)

    print(f"共 {len(tasks)} 个检查任务")

    # 执行检查
    issues = checker.check_all(tasks)

    print(f"\n发现 {len(issues)} 个问题")
    for issue in issues:
        print(f"  - [{issue.priority.value}] {issue.check_item.name}: {issue.issue_description}")