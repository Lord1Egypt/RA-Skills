#!/usr/bin/env python3
"""验证 .docx 文件结构"""

import argparse
import os
import sys
import re
import zipfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

REQUIRED_FILES = ["word/document.xml", "[Content_Types].xml", "word/_rels/document.xml.rels"]
PLACEHOLDER_RE = re.compile(r"\{\{[^}]+\}\}")


def validate(filepath: str) -> dict:
    """验证 .docx 文件结构，返回详细结果"""
    result = {
        "valid": True,
        "issues": [],
        "warnings": [],
        "stats": {},
    }

    # 1. File exists
    if not os.path.exists(filepath):
        result["valid"] = False
        result["issues"].append(f"文件不存在: {filepath}")
        return result

    # 2. File size
    size = os.path.getsize(filepath)
    result["stats"]["file_size"] = size
    if size < 50 * 1024:  # < 50KB
        result["warnings"].append("文件大小异常（< 50KB）")
    elif size > 50 * 1024 * 1024:  # > 50MB
        result["warnings"].append("文件过大（> 50MB）")

    # 3. ZIP structure
    if not zipfile.is_zipfile(filepath):
        result["valid"] = False
        result["issues"].append("不是有效的 ZIP 文件")
        return result

    # 3. ZIP structure + 4-8. All zip reads inside the same context
    try:
        with zipfile.ZipFile(filepath) as z:
            names = z.namelist()

            for req in REQUIRED_FILES:
                if req not in names:
                    result["valid"] = False
                    result["issues"].append(f"缺少必需文件: {req}")

            # 4. XML parsable
            from lxml import etree
            for xml_file in ["word/document.xml"]:
                if xml_file in names:
                    try:
                        content = z.read(xml_file)
                        etree.fromstring(content)
                    except etree.XMLSyntaxError as e:
                        result["valid"] = False
                        result["issues"].append(f"XML 解析错误 ({xml_file}): {e}")

            # 5. Paragraph count
            try:
                doc_xml = z.read("word/document.xml").decode("utf-8")
                para_count = doc_xml.count("</w:p>")
                table_count = doc_xml.count("</w:tbl>")
                result["stats"]["paragraph_count"] = para_count
                result["stats"]["table_count"] = table_count
                if para_count == 0:
                    result["warnings"].append("文档中没有段落")
            except Exception:
                pass

            # 6. Unreplaced placeholders
            try:
                doc_xml = z.read("word/document.xml").decode("utf-8")
                placeholders = PLACEHOLDER_RE.findall(doc_xml)
                if placeholders:
                    result["warnings"].append(f"发现未替换的占位符: {', '.join(set(placeholders))}")
            except Exception:
                pass

            # 7. Style existence check (basic)
            try:
                if "word/styles.xml" in names:
                    styles_xml = z.read("word/styles.xml").decode("utf-8")
                    style_count = styles_xml.count("w:style ")
                    result["stats"]["style_count"] = style_count
            except Exception:
                pass

            # 8. Media file consistency
            try:
                rels = z.read("word/_rels/document.xml.rels").decode("utf-8")
                rel_names = re.findall(r'Target="([^"]+)"', rels)
                media_targets = [t for t in rel_names if "media" in t]
                for target in media_targets:
                    full_path = f"word/{target}"
                    if full_path not in names:
                        result["warnings"].append(f"媒体文件引用存在但不在 ZIP 中: {target}")
            except Exception:
                pass

    except Exception as e:
        result["valid"] = False
        result["issues"].append(f"ZIP 文件损坏: {e}")
        return result

    return result


def main():
    parser = argparse.ArgumentParser(description="验证 .docx 文件结构")
    parser.add_argument("file", help=".docx 文件路径")

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"错误: 文件不存在: {args.file}", file=sys.stderr)
        sys.exit(1)

    result = validate(args.file)

    if result["valid"]:
        print("✓ 文件结构有效")
    else:
        print("✗ 文件结构无效")
        for issue in result["issues"]:
            print(f"  错误: {issue}")

    if result["warnings"]:
        print("警告:")
        for warn in result["warnings"]:
            print(f"  ⚠ {warn}")

    if result["stats"]:
        print("统计:")
        for key, val in result["stats"].items():
            print(f"  {key}: {val}")

    if not result["valid"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
