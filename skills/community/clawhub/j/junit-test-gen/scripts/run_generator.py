#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JUnit Test Generator - 入口脚本

一键执行测试用例JSON解析、测试类生成和文件输出。

用法:
    python run_generator.py <test_cases.json> [output_dir]

示例:
    python run_generator.py test_cases_querySmartControlModeConfig.json
    python run_generator.py test_cases_xxx.json src/test/java

作者: MiniMax Agent
版本: 1.0.0
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from testcase_parser import TestCaseParser
from jtest_generator import JUnitTestGenerator


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python run_generator.py <test_cases.json> [output_dir]")
        print("")
        print("参数:")
        print("  test_cases.json  - 测试用例JSON文件路径")
        print("  output_dir       - 可选，输出目录，默认为 src/test/java")
        print("")
        print("示例:")
        print("  python run_generator.py test_cases_querySmartControlModeConfig.json")
        print("  python run_generator.py test_cases_xxx.json src/test/java")
        sys.exit(1)

    json_file = sys.argv[1]
    output_base = sys.argv[2] if len(sys.argv) > 2 else "src/test/java"

    print("=" * 60)
    print("JUnit Test Generator")
    print("=" * 60)

    if not os.path.exists(json_file):
        print(f"错误: 文件不存在 {json_file}")
        sys.exit(1)

    print(f"\n[1/3] 解析测试用例JSON: {json_file}")
    parser = TestCaseParser()
    try:
        test_suite = parser.parse_file(json_file)
    except FileNotFoundError:
        print(f"错误: 文件不存在 {json_file}")
        sys.exit(1)
    except Exception as e:
        print(f"错误: JSON解析失败 {e}")
        sys.exit(1)

    print(f"  测试套件: {test_suite.name}")
    print(f"  描述: {test_suite.description}")
    print(f"  接口: {test_suite.interface_info.method} {test_suite.interface_info.endpoint}")
    print(f"  测试用例数量: {len(test_suite.test_cases)}")

    summary = parser.get_summary()
    print(f"\n  摘要统计:")
    print(f"    正常场景: {summary.get('normal_cases', 0)}")
    print(f"    边界条件: {summary.get('boundary_cases', 0)}")
    print(f"    异常情况: {summary.get('error_cases', 0)}")

    errors = parser.validate()
    if errors:
        print(f"\n  验证错误:")
        for err in errors:
            print(f"    - {err}")

    print(f"\n[2/3] 生成JUnit 5测试类")
    generator = JUnitTestGenerator()
    java_code = generator.generate(test_suite)

    class_name = generator._extract_class_name(test_suite.name) + ".java"
    package_name = generator._extract_package_from_endpoint(test_suite.interface_info.endpoint)
    output_dir = os.path.join(output_base, package_name.replace('.', '/'))

    print(f"  包名: {package_name}")
    print(f"  类名: {class_name}")
    print(f"  输出目录: {output_dir}")

    os.makedirs(output_dir, exist_ok=True)

    print(f"\n[3/3] 写入测试类文件")
    output_path = os.path.join(output_dir, class_name)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(java_code)

    test_method_count = java_code.count('@Test')

    print(f"\n" + "=" * 60)
    print("生成完成!")
    print("=" * 60)
    print(f"  测试类文件: {output_path}")
    print(f"  测试方法数量: {test_method_count}")

    test_class_name = generator._extract_class_name(test_suite.name)
    print(f"\n下一步: 执行Maven测试")
    print("-" * 60)
    print(f"  mvn test -Dtest={test_class_name} -Dspring.profiles.active=test")
    print("=" * 60)


if __name__ == "__main__":
    main()