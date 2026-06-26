#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
书源JSON验证工具
验证书源JSON是否符合Legado标准格式
"""

import sys
import io
import json
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class BookSourceValidator:
    """书源JSON验证器"""

    # Legado书源必需字段定义
    REQUIRED_FIELDS = {
        'bookSourceUrl': str,
        'bookSourceName': str,
        'bookSourceType': int,
        'bookSourceGroup': str,
        'enabled': bool,
        'enabledExplore': bool,
        'enabledCookieJar': bool,
        'loginUrl': str,
        'loginUi': str,
        'loginCheckJs': str,
        'concurrentRate': str,
        'header': str,
        'searchUrl': str,
        'exploreUrl': str,
        'ruleSearch': dict,
        'ruleBookInfo': dict,
        'ruleToc': dict,
        'ruleContent': dict,
        'ruleExplore': dict,
        'ruleReview': dict,
        'bookSourceComment': str,
        'variableComment': str
    }

    # ruleSearch必需字段
    RULE_SEARCH_REQUIRED = {
        'bookList': str,
        'name': str,
        'author': str,
        'kind': str,
        'wordCount': str,
        'lastChapter': str,
        'intro': str,
        'coverUrl': str,
        'bookUrl': str
    }

    # ruleToc必需字段
    RULE_TOC_REQUIRED = {
        'chapterList': str,
        'chapterName': str,
        'chapterUrl': str,
        'formatJs': str,
        'nextTocUrl': str
    }

    # ruleContent必需字段
    RULE_CONTENT_REQUIRED = {
        'content': str,
        'replaceRegex': str,
        'imageStyle': str,
        'imageDecode': str,
        'webJs': str,
        'nextContentUrl': str,
        'title': str
    }

    def __init__(self):
        self.errors = []
        self.warnings = []

    def validate_json(self, json_file):
        """
        验证书源JSON文件

        Args:
            json_file: JSON文件路径

        Returns:
            bool: 是否通过验证
        """
        print("=" * 70)
        print(f"验证书源JSON: {json_file}")
        print("=" * 70)

        # 1. 读取JSON文件
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            self.errors.append(f"文件不存在: {json_file}")
            return False
        except json.JSONDecodeError as e:
            self.errors.append(f"JSON格式错误: {e}")
            return False

        # 2. 检查是否是数组格式
        if not isinstance(data, list):
            self.errors.append(f"书源必须是数组格式，当前类型: {type(data).__name__}")
            return False

        if len(data) == 0:
            self.errors.append("书源数组为空")
            return False

        print(f"✓ 找到 {len(data)} 个书源")

        # 3. 验证书源对象
        all_valid = True
        for i, book_source in enumerate(data):
            print(f"\n--- 验证书源 {i+1}/{len(data)} ---")
            if not self.validate_book_source(book_source):
                all_valid = False

        # 4. 输出结果
        print("\n" + "=" * 70)
        print("验证结果")
        print("=" * 70)

        if self.errors:
            print(f"\n✗ 发现 {len(self.errors)} 个错误:")
            for error in self.errors:
                print(f"  - {error}")

        if self.warnings:
            print(f"\n⚠ 发现 {len(self.warnings)} 个警告:")
            for warning in self.warnings:
                print(f"  - {warning}")

        if all_valid and not self.errors:
            print("\n✓ 验证通过！书源JSON格式正确")
            return True
        else:
            print("\n✗ 验证失败！请修复上述错误")
            return False

    def validate_book_source(self, book_source):
        """验证单个书源对象"""
        if not isinstance(book_source, dict):
            self.errors.append(f"书源必须是对象类型，当前类型: {type(book_source).__name__}")
            return False

        # 检查必需字段
        for field, expected_type in self.REQUIRED_FIELDS.items():
            if field not in book_source:
                self.errors.append(f"缺少必需字段: {field}")
                continue

            actual_type = type(book_source[field])
            if not isinstance(book_source[field], expected_type):
                # 允许None值
                if book_source[field] is not None:
                    self.errors.append(
                        f"字段类型错误: {field} "
                        f"(期望: {expected_type.__name__}, 实际: {actual_type.__name__})"
                    )
                    continue

        # 验证书源名称和URL
        if book_source.get('bookSourceName'):
            print(f"  书源名称: {book_source['bookSourceName']}")
        else:
            self.errors.append("bookSourceName 不能为空")

        if book_source.get('bookSourceUrl'):
            print(f"  书源URL: {book_source['bookSourceUrl']}")
        else:
            self.errors.append("bookSourceUrl 不能为空")

        # 验证规则对象
        self.validate_rule_search(book_source.get('ruleSearch', {}))
        self.validate_rule_toc(book_source.get('ruleToc', {}))
        self.validate_rule_content(book_source.get('ruleContent', {}))

        return len(self.errors) == 0

    def validate_rule_search(self, rule_search):
        """验证搜索规则"""
        if not isinstance(rule_search, dict):
            self.errors.append(f"ruleSearch 必须是对象类型")
            return

        # bookList 和 bookUrl 是必需的
        if not rule_search.get('bookList'):
            self.errors.append("ruleSearch.bookList 不能为空")
        else:
            print(f"  bookList: {rule_search['bookList']}")

        if not rule_search.get('bookUrl'):
            self.errors.append("ruleSearch.bookUrl 不能为空")
        else:
            print(f"  bookUrl: {rule_search['bookUrl']}")

        if rule_search.get('name'):
            print(f"  name: {rule_search['name']}")

        if rule_search.get('author'):
            print(f"  author: {rule_search['author']}")

        if rule_search.get('coverUrl'):
            print(f"  coverUrl: {rule_search['coverUrl']}")

    def validate_rule_toc(self, rule_toc):
        """验证目录规则"""
        if not isinstance(rule_toc, dict):
            self.errors.append(f"ruleToc 必须是对象类型")
            return

        # chapterList, chapterName, chapterUrl 是必需的
        if not rule_toc.get('chapterList'):
            self.errors.append("ruleToc.chapterList 不能为空")

        if not rule_toc.get('chapterName'):
            self.errors.append("ruleToc.chapterName 不能为空")

        if not rule_toc.get('chapterUrl'):
            self.errors.append("ruleToc.chapterUrl 不能为空")

    def validate_rule_content(self, rule_content):
        """验证正文规则"""
        if not isinstance(rule_content, dict):
            self.errors.append(f"ruleContent 必须是对象类型")
            return

        # content 是必需的
        if not rule_content.get('content'):
            self.errors.append("ruleContent.content 不能为空")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python validate_book_source.py <book_source.json>")
        print("示例: python validate_book_source.py book_source.json")
        sys.exit(1)

    json_file = sys.argv[1]
    validator = BookSourceValidator()
    is_valid = validator.validate_json(json_file)

    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
