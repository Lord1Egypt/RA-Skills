#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JUnit Test Generator - JUnit 5测试代码生成器

根据解析后的测试用例数据，生成符合Spring Boot最佳实践的JUnit 5测试代码。

作者: cherry
版本: 2.1.0
"""

import re
import os
from typing import Dict, List, Any, Optional
from datetime import datetime

from testcase_parser import TestSuite, TestCase


class JUnitTestGenerator:
    """JUnit 5测试代码生成器"""

    def __init__(self, package_name: str = "generated.tests"):
        """
        初始化生成器

        Args:
            package_name: 生成的测试类包名，默认为 "generated.tests"
        """
        self.package_name = package_name
        self.imports = set()
        self.class_body_lines = []

    def _to_pascal_case(self, text: str) -> str:
        """
        将字符串转换为PascalCase，同时移除中文字符和非ASCII字符

        Args:
            text: 输入字符串

        Returns:
            PascalCase格式的字符串
        """
        chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')
        text = chinese_pattern.sub('', text)
        words = re.split(r'[_\- ]', text)
        return ''.join(word.capitalize() for word in words if word)

    def _to_camel_case(self, text: str) -> str:
        """
        将字符串转换为camelCase

        Args:
            text: 输入字符串

        Returns:
            camelCase格式的字符串
        """
        pascal = self._to_pascal_case(text)
        if not pascal:
            return ""
        return pascal[0].lower() + pascal[1:]

    def _clean_endpoint(self, endpoint: str) -> str:
        """
        清理endpoint，移除可能的context-path

        通过检测路径段数量来判断：如果endpoint超过2个路径段，
        则认为第一个段是context-path并移除它。

        Args:
            endpoint: 原始endpoint，如 /context/api/path 或 /api/path

        Returns:
            清理后的endpoint，如 /api/path
        """
        if not endpoint:
            return endpoint

        endpoint = endpoint.strip()
        path_parts = [p for p in endpoint.split('/') if p]

        if len(path_parts) > 2:
            return '/' + '/'.join(path_parts[1:])

        return endpoint

    def _extract_class_name(self, test_suite_name: str) -> str:
        """
        从测试套件名称提取类名

        Args:
            test_suite_name: 测试套件名称

        Returns:
            PascalCase格式的类名
        """
        class_name = self._to_pascal_case(test_suite_name)
        if not class_name.endswith("Test"):
            class_name += "Test"
        return class_name

    def _extract_package_from_endpoint(self, endpoint: str) -> str:
        """
        从接口路径提取包名

        Args:
            endpoint: 接口路径，如 /api/controller/action

        Returns:
            包名，如 generated.tests.controller
        """
        match = re.search(r'/(\w+)/', endpoint)
        if match:
            return f"{self.package_name}.controller"
        return self.package_name

    def _generate_imports(self) -> List[str]:
        """生成import语句"""
        imports = [
            "package {package};",
            "",
            "import com.fasterxml.jackson.databind.ObjectMapper;",
            "import org.junit.jupiter.api.Test;",
            "import org.junit.jupiter.api.BeforeEach;",
            "import org.junit.jupiter.api.AfterEach;",
            "import org.springframework.beans.factory.annotation.Autowired;",
            "import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;",
            "import org.springframework.boot.test.context.SpringBootTest;",
            "import org.springframework.http.MediaType;",
            "import org.springframework.test.web.servlet.MockMvc;",
            "import org.springframework.test.web.servlet.MvcResult;",
            "import org.springframework.test.web.servlet.request.MockHttpServletRequestBuilder;",
            "import org.springframework.jdbc.core.JdbcTemplate;",
            "import org.slf4j.Logger;",
            "import org.slf4j.LoggerFactory;",
            "",
            "import java.util.HashMap;",
            "import java.util.Map;",
            "",
            "import static org.junit.jupiter.api.Assertions.*;",
            "import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;",
            "import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;",
            "import static org.springframework.test.web.servlet.result.MockMvcResultHandlers.print;",
        ]
        return imports

    def _generate_test_method_name(self, test_case: TestCase) -> str:
        """
        生成测试方法名

        Args:
            test_case: 测试用例对象

        Returns:
            符合规范的测试方法名
        """
        method_name = "test"

        name = test_case.name

        chinese_replacements = [
            ("正常场景", ""), ("边界场景", ""), ("异常场景", ""),
            ("成功场景", ""), ("失败场景", ""), ("错误场景", ""),
            ("查询", "Query"), ("获取", "Get"), ("新增", "Add"),
            ("删除", "Delete"), ("修改", "Update"), ("提交", "Submit"),
            ("配置", "Config"), ("设置", "Set")
        ]
        for cn, en in chinese_replacements:
            name = name.replace(cn, en)

        name = name.replace("(", "").replace(")", "").replace("-", "").replace("=", "")
        name = name.replace(",", "").replace("'", "").replace(" ", "").replace("_", "")

        clean_name = re.sub(r'[^a-zA-Z0-9]', '', name)

        method_name += clean_name

        if test_case.id:
            method_name += f"_{test_case.id.replace('-', '_')}"

        if method_name and method_name[0].isupper():
            method_name = method_name[0].lower() + method_name[1:]

        return method_name or "test"

    def _generate_request_body(self, body: Dict[str, Any]) -> str:
        """
        生成请求体构建代码

        Args:
            body: 请求体字典

        Returns:
            Java代码字符串
        """
        if not body:
            return "        Map<String, Object> requestBody = new HashMap<>();"

        lines = ["        Map<String, Object> requestBody = new HashMap<>();"]
        for key, value in body.items():
            if value is None:
                lines.append(f"        requestBody.put(\"{key}\", null);")
            elif isinstance(value, str):
                lines.append(f"        requestBody.put(\"{key}\", \"{value}\");")
            elif isinstance(value, bool):
                lines.append(f"        requestBody.put(\"{key}\", {str(value).lower()});")
            elif isinstance(value, (int, float)):
                lines.append(f"        requestBody.put(\"{key}\", {value});")
            elif isinstance(value, dict):
                import json
                dict_str = json.dumps(value, ensure_ascii=False).replace('"', '\\"')
                lines.append(f"        requestBody.put(\"{key}\", \"{dict_str}\");")
            elif isinstance(value, list):
                import json
                list_str = json.dumps(value, ensure_ascii=False).replace('"', '\\"')
                lines.append(f"        requestBody.put(\"{key}\", \"{list_str}\");")
        return "\n".join(lines)

    def _generate_json_path_assertions(self, expected_body: Optional[Dict[str, Any]], depth: int = 2) -> List[str]:
        """
        生成jsonPath断言代码

        Args:
            expected_body: 预期响应体
            depth: 嵌套深度（保留参数）

        Returns:
            断言代码列表
        """
        if not expected_body:
            return []

        lines = []

        for key, value in expected_body.items():
            if value is None:
                continue

            json_path = f"$.{key}"

            if isinstance(value, bool):
                lines.append(f"                .andExpect(jsonPath(\"{json_path}\").value({str(value).lower()}))")
            elif isinstance(value, (int, float)):
                lines.append(f"                .andExpect(jsonPath(\"{json_path}\").value({value}))")
            elif isinstance(value, str):
                lines.append(f"                .andExpect(jsonPath(\"{json_path}\").value(\"{value}\"))")

        return lines

    def _generate_sql_execution_code(self, sql_statements: List[str], phase: str) -> List[str]:
        """
        生成执行SQL的代码

        Args:
            sql_statements: SQL语句列表
            phase: 阶段标识（Setup/Teardown）

        Returns:
            SQL执行代码列表
        """
        if not sql_statements:
            return []

        lines = []
        lines.append(f"        // {phase} - SQL statements")

        for i, sql in enumerate(sql_statements):
            escaped_sql = sql.replace('"', '\\"')
            lines.append(f"        sqlStatements{phase}.add(\"{escaped_sql}\");")

        return lines

    def _generate_test_method(self, test_case: TestCase) -> str:
        """
        生成单个测试方法

        Args:
            test_case: 测试用例对象

        Returns:
            测试方法Java代码
        """
        method_name = self._generate_test_method_name(test_case)

        setup_sql = test_case.setup.mysql if test_case.setup and test_case.setup.mysql else []
        teardown_sql = test_case.teardown.mysql if test_case.teardown and test_case.teardown.mysql else []

        lines = [
            f"    /**",
            f"     * {test_case.id}: {test_case.name}",
            f"     */",
            f"    @Test",
            f"    void {method_name}() throws Exception {{",
            f"        logger.info(\"Executing test: {test_case.id} - {test_case.name}\");",
            f"",
        ]

        if setup_sql:
            lines.append("        // Setup - 准备测试数据")
            for sql in setup_sql:
                escaped_sql = sql.replace('"', '\\"')
                lines.append(f"        jdbcTemplate.execute(\"{escaped_sql}\");")
            lines.append("")

        lines.append("        // Given - 构建请求")
        lines.append(self._generate_request_body(test_case.body))
        lines.append("")

        lines.append("        // When & Then - 执行请求并验证")
        http_method = test_case.method.upper()
        endpoint = self._clean_endpoint(test_case.endpoint)

        if http_method == "GET":
            lines.append(f"        mockMvc.perform(get(\"{endpoint}\")")
        elif http_method == "POST":
            lines.append(f"        mockMvc.perform(post(\"{endpoint}\")")
        elif http_method == "PUT":
            lines.append(f"        mockMvc.perform(put(\"{endpoint}\")")
        elif http_method == "DELETE":
            lines.append(f"        mockMvc.perform(delete(\"{endpoint}\")")
        else:
            lines.append(f"        mockMvc.perform(post(\"{endpoint}\")")

        lines.append(f"                .contentType(MediaType.APPLICATION_JSON)")
        lines.append(f"                .content(objectMapper.writeValueAsString(requestBody)))")

        if test_case.expected.status:
            lines.append(f"                .andExpect(status().is{test_case.expected.status}())")

            if test_case.expected.body:
                assertions = self._generate_json_path_assertions(test_case.expected.body)
                for assertion in assertions:
                    lines.append(f"                {assertion}")

        lines.append(f"                .andDo(print());")
        lines.append("")

        if teardown_sql:
            lines.append("        // Teardown - 清理测试数据")
            for sql in teardown_sql:
                escaped_sql = sql.replace('"', '\\"')
                lines.append(f"        jdbcTemplate.execute(\"{escaped_sql}\");")
            lines.append("")

        lines.append("    }")

        return "\n".join(lines)

    def _generate_test_class_footer(self) -> str:
        """生成测试类尾部代码"""
        return ""

    def generate(self, test_suite: TestSuite) -> str:
        """
        生成完整的JUnit 5测试类代码

        Args:
            test_suite: 解析后的测试套件对象

        Returns:
            完整的Java测试类代码字符串
        """
        package_name = self._extract_package_from_endpoint(test_suite.interface_info.endpoint)
        class_name = self._extract_class_name(test_suite.name)

        lines = []

        lines.append(f"package {package_name};")
        lines.append("")
        lines.append("import com.fasterxml.jackson.databind.ObjectMapper;")
        lines.append("import org.junit.jupiter.api.Test;")
        lines.append("import org.junit.jupiter.api.BeforeEach;")
        lines.append("import org.springframework.beans.factory.annotation.Autowired;")
        lines.append("import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;")
        lines.append("import org.springframework.boot.test.context.SpringBootTest;")
        lines.append("import org.springframework.http.MediaType;")
        lines.append("import org.springframework.test.web.servlet.MockMvc;")
        lines.append("import org.springframework.test.web.servlet.MvcResult;")
        lines.append("import org.springframework.test.web.servlet.request.MockHttpServletRequestBuilder;")
        lines.append("import org.springframework.jdbc.core.JdbcTemplate;")
        lines.append("import org.slf4j.Logger;")
        lines.append("import org.slf4j.LoggerFactory;")
        lines.append("")
        lines.append("import java.util.HashMap;")
        lines.append("import java.util.Map;")
        lines.append("")
        lines.append("import static org.junit.jupiter.api.Assertions.*;")
        lines.append("import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;")
        lines.append("import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;")
        lines.append("import static org.springframework.test.web.servlet.result.MockMvcResultHandlers.print;")
        lines.append("")
        lines.append(f"/**")
        lines.append(f" * {test_suite.description}")
        lines.append(f" *")
        lines.append(f" * @Generated by JUnit Test Generator")
        lines.append(f" * @date {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f" */")
        lines.append(f"@SpringBootTest")
        lines.append(f"@AutoConfigureMockMvc")
        lines.append(f"class {class_name} {{")
        lines.append("")
        lines.append(f"    @Autowired")
        lines.append(f"    private MockMvc mockMvc;")
        lines.append("")
        lines.append(f"    @Autowired")
        lines.append(f"    private ObjectMapper objectMapper;")
        lines.append("")
        lines.append(f"    @Autowired")
        lines.append(f"    private JdbcTemplate jdbcTemplate;")
        lines.append("")
        lines.append(f"    private static final Logger logger = LoggerFactory.getLogger({class_name}.class);")
        lines.append("")

        for tc in test_suite.test_cases:
            lines.append(self._generate_test_method(tc))
            lines.append("")

        lines.append(self._generate_test_class_footer())

        lines.append(f"}}")

        return "\n".join(lines)

    def generate_service_test(self, test_suite: TestSuite) -> str:
        """
        生成服务层测试类（不使用MockMvc）

        Args:
            test_suite: 解析后的测试套件对象

        Returns:
            完整的Java服务层测试类代码字符串
        """
        package_name = f"{self.package_name}.service"
        class_name = self._extract_class_name(test_suite.name)

        lines = []

        lines.append(f"package {package_name};")
        lines.append("")
        lines.append("import org.junit.jupiter.api.Test;")
        lines.append("import org.junit.jupiter.api.BeforeEach;")
        lines.append("import org.springframework.beans.factory.annotation.Autowired;")
        lines.append("import org.springframework.boot.test.context.SpringBootTest;")
        lines.append("")
        lines.append("import static org.junit.jupiter.api.Assertions.*;")
        lines.append("")
        lines.append(f"/**")
        lines.append(f" * {test_suite.description}")
        lines.append(f" *")
        lines.append(f" * @Generated by JUnit Test Generator")
        lines.append(f" * @date {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f" */")
        lines.append(f"@SpringBootTest")
        lines.append(f"class {class_name} {{")
        lines.append("")

        for tc in test_suite.test_cases:
            method_name = self._generate_test_method_name(tc)
            lines.append(f"    /**")
            lines.append(f"     * {tc.id}: {tc.name}")
            lines.append(f"     */")
            lines.append(f"    @Test")
            lines.append(f"    void {method_name}() {{")
            lines.append(f"        // Given")
            lines.append(f"        // TODO: Prepare test data for {tc.id}")
            lines.append(f"        ")
            lines.append(f"        // When")
            lines.append(f"        // TODO: Execute service method")
            lines.append(f"        ")
            lines.append(f"        // Then")
            lines.append(f"        // TODO: Assert results")
            lines.append(f"    }}")
            lines.append("")

        lines.append(f"}}")

        return "\n".join(lines)


def main():
    """主函数 - 用于测试生成器"""
    import sys
    sys.path.insert(0, '.')

    from testcase_parser import TestCaseParser

    if len(sys.argv) < 2:
        print("用法: python jtest_generator.py <test_cases.json> [output_dir]")
        print("")
        print("参数:")
        print("  test_cases.json  - 测试用例JSON文件路径")
        print("  output_dir       - 可选，输出目录，默认为当前目录")
        print("")
        print("示例:")
        print("  python jtest_generator.py test_cases.json")
        print("  python jtest_generator.py test_cases.json src/test/java")
        sys.exit(1)

    json_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."

    parser = TestCaseParser()

    try:
        test_suite = parser.parse_file(json_file)
        print(f"解析测试套件: {test_suite.name}")
        print(f"生成JUnit 5测试代码...")

        generator = JUnitTestGenerator()
        java_code = generator.generate(test_suite)

        class_name = generator._extract_class_name(test_suite.name) + ".java"
        output_path = f"{output_dir}/{class_name}"

        os.makedirs(output_dir, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(java_code)

        print(f"生成完成: {output_path}")
        print(f"测试用例数量: {len(test_suite.test_cases)}")

    except FileNotFoundError:
        print(f"错误: 文件不存在 {json_file}")
    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    main()
