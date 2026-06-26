#!/usr/bin/env python3
"""
日志验证脚本
验证执行日志文件是否符合LOG.md中定义的规范
输出结构化的验证结果供模型决策使用
"""

import json
import sys
import os
from datetime import datetime
from typing import Dict, Any, List
from collections import Counter
import re

class LogValidator:
    """日志验证器"""

    def __init__(self):
        """初始化验证器"""
        self.errors = []
        self.warnings = []
        self.rule_usage = Counter()

        # 执行规则类别
        self.rule_categories = ["CS", "RR", "TU", "RS", "EH"]

        # 必需的顶层字段
        self.required_top_fields = ["user_query", "steps", "final_result", "session_stats"]

        # session_stats必需字段
        self.required_stats_fields = ["total_steps", "tool_call_count"]

        # session_stats可选字段（如果存在则需要验证）
        self.optional_stats_fields = ["user_feedback_count", "task_tool_count"]

        # 步骤类型及其必需字段
        self.step_types = {
            "user_input": {
                "required_fields": ["step", "type", "timestamp", "content"],
                "content_fields": ["message"]
            },
            "tool_call": {
                "required_fields": ["step", "type", "timestamp", "content"],
                "content_fields": ["reasoning", "tool_name", "tool_params", "output", "success"]
            },
            "task_tool": {
                "required_fields": ["step", "type", "timestamp", "content"],
                "content_fields": ["reasoning", "tool_params", "output", "purpose"]
            },
            "user_feedback": {
                "required_fields": ["step", "type", "timestamp", "content"],
                "content_fields": ["message"]
            },
            "system_response": {
                "required_fields": ["step", "type", "timestamp", "content"],
                "content_fields": ["message"],
                "optional_content_fields": ["error", "final_result_preview"]
            }
        }

    def validate_timestamp(self, timestamp: str) -> bool:
        """
        验证时间戳格式

        Args:
            timestamp: ISO 8601格式的时间戳字符串

        Returns:
            是否为有效的时间戳
        """
        try:
            # 尝试解析ISO 8601格式
            # 支持带微秒和不带微秒的格式
            if '.' in timestamp:
                datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            else:
                datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
            return True
        except (ValueError, AttributeError):
            return False

    def validate_top_level_structure(self, log_data: Dict[str, Any]) -> bool:
        """
        验证顶层结构

        Args:
            log_data: 日志数据

        Returns:
            是否通过验证
        """
        valid = True

        # 检查必需字段
        for field in self.required_top_fields:
            if field not in log_data:
                self.errors.append(f"缺少必需的顶层字段: '{field}'")
                valid = False

        # 检查user_query类型
        if "user_query" in log_data and not isinstance(log_data["user_query"], str):
            self.errors.append(f"'user_query'必须是字符串类型，实际为: {type(log_data['user_query']).__name__}")
            valid = False

        # 检查steps类型
        if "steps" in log_data:
            if not isinstance(log_data["steps"], list):
                self.errors.append(f"'steps'必须是数组类型，实际为: {type(log_data['steps']).__name__}")
                valid = False
            elif len(log_data["steps"]) == 0:
                self.warnings.append("'steps'数组为空")

        # 检查final_result类型
        if "final_result" in log_data and not isinstance(log_data["final_result"], str):
            self.errors.append(f"'final_result'必须是字符串类型，实际为: {type(log_data['final_result']).__name__}")
            valid = False

        # 检查session_stats结构
        if "session_stats" in log_data:
            if not isinstance(log_data["session_stats"], dict):
                self.errors.append(f"'session_stats'必须是对象类型，实际为: {type(log_data['session_stats']).__name__}")
                valid = False
            else:
                stats = log_data["session_stats"]
                # 检查必需字段
                for field in self.required_stats_fields:
                    if field not in stats:
                        self.errors.append(f"'session_stats'缺少必需字段: '{field}'")
                        valid = False
                    elif not isinstance(stats.get(field), (int, float)):
                        self.errors.append(f"'session_stats.{field}'必须是数字类型")
                        valid = False

                # 检查可选字段（如果存在的话）
                for field in self.optional_stats_fields:
                    if field in stats and not isinstance(stats.get(field), (int, float)):
                        self.errors.append(f"'session_stats.{field}'必须是数字类型")
                        valid = False

        return valid

    def validate_step(self, step: Dict[str, Any], index: int) -> bool:
        """
        验证单个步骤

        Args:
            step: 步骤数据
            index: 步骤索引

        Returns:
            是否通过验证
        """
        valid = True
        step_num = step.get("step", f"[索引{index}]")

        # 检查步骤类型
        step_type = step.get("type")
        if not step_type:
            self.errors.append(f"步骤{step_num}: 缺少'type'字段")
            return False

        if step_type not in self.step_types:
            self.errors.append(f"步骤{step_num}: 未知的步骤类型 '{step_type}'")
            return False

        # 检查必需字段
        type_config = self.step_types[step_type]
        for field in type_config["required_fields"]:
            if field not in step:
                self.errors.append(f"步骤{step_num}: 缺少必需字段 '{field}'")
                valid = False

        # 验证时间戳
        if "timestamp" in step:
            if not self.validate_timestamp(step["timestamp"]):
                self.errors.append(f"步骤{step_num}: 无效的时间戳格式 '{step['timestamp']}'")
                valid = False

        # 验证content字段
        if "content" in step:
            if not isinstance(step["content"], dict):
                self.errors.append(f"步骤{step_num}: 'content'必须是对象类型")
                valid = False
            else:
                content = step["content"]
                # 检查必需的content字段
                for field in type_config["content_fields"]:
                    if field not in content:
                        self.errors.append(f"步骤{step_num}: content缺少必需字段 '{field}'")
                        valid = False

                # 特殊验证：tool_call类型
                if step_type == "tool_call":
                    valid = self.validate_tool_call(content, step_num) and valid

                # 特殊验证：task_tool类型
                if step_type == "task_tool":
                    valid = self.validate_task_tool(content, step_num) and valid

        return valid

    def validate_tool_call(self, content: Dict[str, Any], step_num: str) -> bool:
        """
        验证tool_call步骤的特殊要求

        Args:
            content: 步骤内容
            step_num: 步骤编号

        Returns:
            是否通过验证
        """
        valid = True

        # 验证reasoning字段
        reasoning = content.get("reasoning", "")
        if not reasoning:
            self.errors.append(f"步骤{step_num}: reasoning字段为空")
            valid = False

        # 验证tool_params
        if "tool_params" in content:
            if not isinstance(content["tool_params"], dict):
                self.errors.append(f"步骤{step_num}: tool_params必须是对象类型")
                valid = False

        # 验证success字段
        if "success" in content:
            if not isinstance(content["success"], bool):
                self.errors.append(f"步骤{step_num}: success必须是布尔类型")
                valid = False

        return valid

    def validate_task_tool(self, content: Dict[str, Any], step_num: str) -> bool:
        """
        验证task_tool步骤的特殊要求

        Args:
            content: 步骤内容
            step_num: 步骤编号

        Returns:
            是否通过验证
        """
        valid = True

        # 验证reasoning字段
        reasoning = content.get("reasoning", "")
        if not reasoning:
            self.errors.append(f"步骤{step_num}: reasoning字段为空")
            valid = False

        # 验证tool_params
        if "tool_params" in content:
            if not isinstance(content["tool_params"], dict):
                self.errors.append(f"步骤{step_num}: tool_params必须是对象类型")
                valid = False
            else:
                tool_params = content["tool_params"]
                # 检查必需的tool_params字段
                required_params = ["description", "prompt", "subagent_type", "model"]
                for param in required_params:
                    if param not in tool_params:
                        self.errors.append(f"步骤{step_num}: tool_params缺少必需字段 '{param}'")
                        valid = False

                # 验证subagent_type的值
                if "subagent_type" in tool_params:
                    if tool_params["subagent_type"] != "general-purpose":
                        self.warnings.append(
                            f"步骤{step_num}: subagent_type建议使用'general-purpose'，实际为'{tool_params['subagent_type']}'"
                        )

                # 验证model的值
                if "model" in tool_params:
                    if tool_params["model"] != "sonnet":
                        self.warnings.append(
                            f"步骤{step_num}: model建议使用'sonnet'，实际为'{tool_params['model']}'"
                        )

        # 验证purpose字段
        if "purpose" in content:
            valid_purposes = ["get_html_info", "selector_finding", "verification"]
            purpose = content["purpose"]
            if purpose not in valid_purposes:
                self.errors.append(
                    f"步骤{step_num}: purpose必须是{valid_purposes}之一，实际为'{purpose}'"
                )
                valid = False
        else:
            self.errors.append(f"步骤{step_num}: 缺少purpose字段")
            valid = False

        # 验证output字段
        if "output" in content:
            output = content["output"]
            if not isinstance(output, str):
                self.errors.append(f"步骤{step_num}: output必须是字符串类型")
                valid = False
            elif not output:
                self.warnings.append(f"步骤{step_num}: output字段为空")

        return valid

    def validate_step_sequence(self, steps: List[Dict[str, Any]]) -> bool:
        """
        验证步骤序列的一致性

        Args:
            steps: 步骤列表

        Returns:
            是否通过验证
        """
        valid = True

        # 检查步骤编号连续性
        expected_step = 1
        for i, step in enumerate(steps):
            step_num = step.get("step")
            if step_num:
                try:
                    actual_step = int(step_num)
                    if actual_step != expected_step:
                        self.warnings.append(f"步骤编号不连续: 期望'{expected_step}'，实际'{actual_step}'")
                    expected_step = actual_step + 1
                except ValueError:
                    self.errors.append(f"步骤编号必须是数字字符串: '{step_num}'")
                    valid = False

        # 检查时间戳递增
        timestamps = []
        for step in steps:
            if "timestamp" in step:
                try:
                    if '.' in step["timestamp"]:
                        ts = datetime.fromisoformat(step["timestamp"].replace('Z', '+00:00'))
                    else:
                        ts = datetime.strptime(step["timestamp"], "%Y-%m-%dT%H:%M:%S")
                    timestamps.append((step.get("step", "?"), ts))
                except:
                    pass

        for i in range(1, len(timestamps)):
            if timestamps[i][1] < timestamps[i-1][1]:
                self.warnings.append(
                    f"时间戳顺序异常: 步骤{timestamps[i][0]}的时间早于步骤{timestamps[i-1][0]}"
                )

        # 检查第一个步骤是否为user_input
        if steps and steps[0].get("type") != "user_input":
            self.warnings.append(f"第一个步骤应该是'user_input'类型，实际为'{steps[0].get('type')}'")

        # 检查最后一个步骤是否为system_response
        if steps and steps[-1].get("type") != "system_response":
            self.warnings.append(f"最后一个步骤通常应该是'system_response'类型，实际为'{steps[-1].get('type')}'")

        return valid

    def validate_statistics(self, log_data: Dict[str, Any]) -> bool:
        """
        验证统计数据的一致性

        Args:
            log_data: 日志数据

        Returns:
            是否通过验证
        """
        valid = True

        if "session_stats" not in log_data or "steps" not in log_data:
            return valid

        stats = log_data["session_stats"]
        steps = log_data["steps"]

        # 统计实际数据
        actual_total_steps = len(steps)
        actual_tool_calls = sum(1 for s in steps if s.get("type") == "tool_call")
        actual_task_tools = sum(1 for s in steps if s.get("type") == "task_tool")
        actual_user_feedbacks = sum(1 for s in steps if s.get("type") == "user_feedback")

        # 比较统计数据
        if stats.get("total_steps") != actual_total_steps:
            self.warnings.append(
                f"total_steps不匹配: 声明{stats.get('total_steps')}，实际{actual_total_steps}"
            )

        if stats.get("tool_call_count") != actual_tool_calls:
            self.warnings.append(
                f"tool_call_count不匹配: 声明{stats.get('tool_call_count')}，实际{actual_tool_calls}"
            )

        # 如果有task_tool_count字段，验证其正确性
        if "task_tool_count" in stats:
            if stats.get("task_tool_count") != actual_task_tools:
                self.warnings.append(
                    f"task_tool_count不匹配: 声明{stats.get('task_tool_count')}，实际{actual_task_tools}"
                )

        # 如果有user_feedback_count字段，验证其正确性
        if "user_feedback_count" in stats:
            if stats.get("user_feedback_count") != actual_user_feedbacks:
                self.warnings.append(
                    f"user_feedback_count不匹配: 声明{stats.get('user_feedback_count')}，实际{actual_user_feedbacks}"
                )

        return valid

    def validate_file(self, file_path: str) -> Dict[str, Any]:
        """
        验证日志文件

        Args:
            file_path: 日志文件路径

        Returns:
            验证结果字典
        """
        # 重置状态
        self.errors = []
        self.warnings = []
        self.rule_usage = Counter()

        # 读取文件
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                log_data = json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append(f"JSON解析错误: {e}")
            return self.get_validation_result()
        except FileNotFoundError:
            self.errors.append(f"文件不存在: {file_path}")
            return self.get_validation_result()
        except Exception as e:
            self.errors.append(f"文件读取错误: {e}")
            return self.get_validation_result()

        # 执行验证
        # 1. 验证顶层结构
        self.validate_top_level_structure(log_data)

        # 2. 验证每个步骤
        if "steps" in log_data and isinstance(log_data["steps"], list):
            for i, step in enumerate(log_data["steps"]):
                self.validate_step(step, i)

            # 3. 验证步骤序列
            self.validate_step_sequence(log_data["steps"])

        # 4. 验证统计数据
        self.validate_statistics(log_data)

        return self.get_validation_result()

    def get_validation_result(self) -> Dict[str, Any]:
        """
        获取验证结果

        Returns:
            包含验证结果的字典
        """
        return {
            "is_valid": len(self.errors) == 0,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "errors": self.errors,
            "warnings": self.warnings,
            "rule_usage": dict(self.rule_usage) if self.rule_usage else {}
        }

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python validate_log.py <日志文件路径>")
        print("\n示例: python validate_log.py workflow_log.json")
        sys.exit(1)

    # 获取文件路径
    file_path = sys.argv[1]

    # 创建验证器
    validator = LogValidator()

    # 执行验证
    result = validator.validate_file(file_path)

    # 输出JSON格式的结果
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # 返回状态码
    sys.exit(0 if result["is_valid"] else 1)

if __name__ == "__main__":
    main()