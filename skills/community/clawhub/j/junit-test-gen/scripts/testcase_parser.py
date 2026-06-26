#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JUnit Test Generator - 测试用例JSON解析器

用于解析Test Case Generator生成的JSON格式测试用例文件。

作者: MiniMax Agent
版本: 1.0.0
"""

import json
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict


@dataclass
class InterfaceInfo:
    """接口信息"""
    endpoint: str = ""
    method: str = "POST"
    content_type: str = "application/json"
    function: str = ""


@dataclass
class RequestDto:
    """请求DTO信息"""
    fields: Dict[str, str] = field(default_factory=dict)


@dataclass
class SetupConfig:
    """前置条件配置"""
    mysql: List[str] = field(default_factory=list)
    redis: Dict[str, str] = field(default_factory=dict)


@dataclass
class ExpectedResult:
    """预期结果"""
    status: int = 200
    body: Optional[Dict[str, Any]] = None


@dataclass
class TestCase:
    """测试用例"""
    id: str = ""
    name: str = ""
    endpoint: str = ""
    method: str = "POST"
    headers: Dict[str, str] = field(default_factory=dict)
    body: Dict[str, Any] = field(default_factory=dict)
    setup: SetupConfig = field(default_factory=SetupConfig)
    expected: ExpectedResult = field(default_factory=ExpectedResult)
    teardown: SetupConfig = field(default_factory=SetupConfig)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TestCase':
        """从字典创建TestCase对象"""
        setup_data = data.get('setup', {})
        teardown_data = data.get('teardown', {})
        expected_data = data.get('expected', {})

        return cls(
            id=data.get('id', ''),
            name=data.get('name', ''),
            endpoint=data.get('endpoint', ''),
            method=data.get('method', 'POST'),
            headers=data.get('headers', {}),
            body=data.get('body', {}),
            setup=SetupConfig(
                mysql=setup_data.get('mysql', []),
                redis=setup_data.get('redis', {})
            ),
            expected=ExpectedResult(
                status=expected_data.get('status', 200),
                body=expected_data.get('body')
            ),
            teardown=SetupConfig(
                mysql=teardown_data.get('mysql', []),
                redis=teardown_data.get('redis', {})
            )
        )


@dataclass
class TestSuite:
    """测试套件"""
    name: str = ""
    description: str = ""
    interface_info: InterfaceInfo = field(default_factory=InterfaceInfo)
    request_dto: RequestDto = field(default_factory=RequestDto)
    mysql_data: Dict[str, Any] = field(default_factory=dict)
    test_cases: List[TestCase] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TestSuite':
        """从字典创建TestSuite对象"""
        interface_info_data = data.get('interface_info', {})
        request_dto_data = data.get('request_dto', {})

        test_cases = []
        for tc_data in data.get('test_cases', []):
            test_cases.append(TestCase.from_dict(tc_data))

        return cls(
            name=data.get('test_suite', ''),
            description=data.get('description', ''),
            interface_info=InterfaceInfo(
                endpoint=interface_info_data.get('endpoint', ''),
                method=interface_info_data.get('method', 'POST'),
                content_type=interface_info_data.get('content_type', 'application/json'),
                function=interface_info_data.get('function', '')
            ),
            request_dto=RequestDto(fields=request_dto_data),
            mysql_data=data.get('mysql_data', {}),
            test_cases=test_cases
        )


class TestCaseParser:
    """测试用例JSON解析器"""

    def __init__(self):
        """初始化解析器"""
        self.current_suite: Optional[TestSuite] = None
        self.test_cases: List[TestCase] = []

    def parse_file(self, file_path: str) -> TestSuite:
        """
        解析测试用例JSON文件

        Args:
            file_path: JSON文件路径

        Returns:
            TestSuite对象

        Raises:
            FileNotFoundError: 文件不存在
            json.JSONDecodeError: JSON解析失败
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.current_suite = TestSuite.from_dict(data)
        self.test_cases = self.current_suite.test_cases

        return self.current_suite

    def parse_string(self, json_str: str) -> TestSuite:
        """
        解析JSON字符串

        Args:
            json_str: JSON字符串

        Returns:
            TestSuite对象
        """
        data = json.loads(json_str)
        self.current_suite = TestSuite.from_dict(data)
        self.test_cases = self.current_suite.test_cases
        return self.current_suite

    def get_test_case(self, test_id: str) -> Optional[TestCase]:
        """
        根据ID获取测试用例

        Args:
            test_id: 测试用例ID

        Returns:
            TestCase对象，不存在返回None
        """
        for tc in self.test_cases:
            if tc.id == test_id:
                return tc
        return None

    def get_test_cases_by_type(self, test_type: str) -> List[TestCase]:
        """
        根据类型获取测试用例

        Args:
            test_type: 测试类型 (normal/boundary/error)

        Returns:
            符合条件的测试用例列表
        """
        if test_type == "normal":
            return [tc for tc in self.test_cases if "正常" in tc.name or "成功" in tc.name]
        elif test_type == "boundary":
            return [tc for tc in self.test_cases if "边界" in tc.name]
        elif test_type == "error":
            return [tc for tc in self.test_cases if "异常" in tc.name or "失败" in tc.name]
        return self.test_cases

    def get_summary(self) -> Dict[str, Any]:
        """
        获取测试套件摘要信息

        Returns:
            包含统计信息的字典
        """
        if not self.current_suite:
            return {}

        normal_count = len([tc for tc in self.test_cases if "正常" in tc.name or "成功" in tc.name])
        boundary_count = len([tc for tc in self.test_cases if "边界" in tc.name])
        error_count = len([tc for tc in self.test_cases if "异常" in tc.name or "失败" in tc.name])

        return {
            "test_suite_name": self.current_suite.name,
            "description": self.current_suite.description,
            "interface": self.current_suite.interface_info.endpoint,
            "total_cases": len(self.test_cases),
            "normal_cases": normal_count,
            "boundary_cases": boundary_count,
            "error_cases": error_count,
            "request_dto_fields": list(self.current_suite.request_dto.fields.keys())
        }

    def validate(self) -> List[str]:
        """
        验证测试用例的完整性

        Returns:
            错误列表，空表示验证通过
        """
        errors = []

        if not self.current_suite:
            errors.append("未加载任何测试套件")
            return errors

        if not self.current_suite.name:
            errors.append("测试套件名称为空")

        if not self.current_suite.interface_info.endpoint:
            errors.append("接口路径为空")

        for tc in self.test_cases:
            if not tc.id:
                errors.append(f"测试用例缺少ID")
            if not tc.name:
                errors.append(f"测试用例 {tc.id} 缺少名称")
            if not tc.body:
                errors.append(f"测试用例 {tc.id} 缺少请求体")

        return errors


def main():
    """主函数 - 用于测试解析器"""
    import sys

    if len(sys.argv) < 2:
        print("用法: python testcase_parser.py <test_cases.json>")
        sys.exit(1)

    parser = TestCaseParser()

    try:
        suite = parser.parse_file(sys.argv[1])
        print(f"解析成功: {suite.name}")
        print(f"描述: {suite.description}")
        print(f"接口: {suite.interface_info.method} {suite.interface_info.endpoint}")
        print(f"测试用例数量: {len(suite.test_cases)}")

        summary = parser.get_summary()
        print(f"\n摘要统计:")
        print(f"  正常场景: {summary.get('normal_cases', 0)}")
        print(f"  边界条件: {summary.get('boundary_cases', 0)}")
        print(f"  异常情况: {summary.get('error_cases', 0)}")

        errors = parser.validate()
        if errors:
            print(f"\n验证错误:")
            for err in errors:
                print(f"  - {err}")
        else:
            print(f"\n验证通过!")

    except FileNotFoundError:
        print(f"错误: 文件不存在 {sys.argv[1]}")
    except json.JSONDecodeError as e:
        print(f"错误: JSON解析失败 {e}")


if __name__ == "__main__":
    main()