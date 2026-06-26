#!/usr/bin/env python3
"""
run_quality_check.py - 产品分析文档质量检查工具

用法:
    python3 run_quality_check.py <markdown_file> [--type flow|arch|prd|tracking|all]

文档类型说明:
    flow     - 业务流程分析报告
    arch     - 功能架构设计
    prd      - 完整 PRD 文档
    tracking - 埋点方案设计
    all      - 通用检查（不指定文档类型时默认）

功能:
    对最终输出的 Markdown 文档进行结构和内容质量检查。
    检查项包括：
    1. 文档是否包含必要的章节标题
    2. 是否包含 Mermaid 图表
    3. 是否包含优先级标注（flow/arch/prd）
    4. 是否包含异常场景分析（flow/prd）
    5. 表格格式是否正确
"""

import sys
import re
from pathlib import Path


# 各文档类型必要章节关键词
FLOW_REQUIRED_SECTIONS = [
    "需求概述",
    "业务流程",
    "异常",
]

ARCH_REQUIRED_SECTIONS = [
    "功能架构",
    "功能模块",
    "迭代",
]

PRD_REQUIRED_SECTIONS = [
    "产品概述",
    "用户分析",
    "功能需求",
    "业务流程",
    "非功能需求",
    "数据需求",
    "实施计划",
    "风险",
]

TRACKING_REQUIRED_SECTIONS = [
    "埋点概述",
    "页面埋点",
    "事件埋点",
    "转化漏斗",
    "测试",
]

DOC_TYPE_MAP = {
    "flow": FLOW_REQUIRED_SECTIONS,
    "arch": ARCH_REQUIRED_SECTIONS,
    "prd": PRD_REQUIRED_SECTIONS,
    "tracking": TRACKING_REQUIRED_SECTIONS,
}


def check_sections(content: str, required_keywords: list[str]) -> list[str]:
    """检查文档是否包含必要的章节（通过关键词匹配标题行）。"""
    issues = []
    headings = re.findall(r"^#{1,4}\s+(.+)$", content, re.MULTILINE)
    heading_text = " ".join(headings).lower()

    for keyword in required_keywords:
        if keyword.lower() not in heading_text and keyword not in content:
            issues.append(f"  缺少关键章节或内容: 未找到包含 '{keyword}' 的标题。")
    return issues


def check_mermaid(content: str) -> list[str]:
    """检查文档是否包含至少一个 Mermaid 图表。"""
    blocks = re.findall(r"```mermaid", content)
    if not blocks:
        return ["  文档中未包含任何 Mermaid 图表。产品分析文档应至少包含一个流程图或架构图。"]
    return []


def check_priority_labels(content: str) -> list[str]:
    """检查文档是否包含优先级标注。"""
    priority_pattern = re.compile(r"P[0-3]", re.IGNORECASE)
    if not priority_pattern.search(content):
        return ["  文档中未发现优先级标注 (如 P0, P1, P2)。建议为功能或异常添加优先级。"]
    return []


def check_tables(content: str) -> list[str]:
    """检查文档是否包含表格，并进行基础格式验证。"""
    table_rows = re.findall(r"^\|.*\|$", content, re.MULTILINE)
    if len(table_rows) < 2:
        return ["  文档中未包含有效的 Markdown 表格。建议使用表格组织结构化信息。"]
    return []


def check_exceptions(content: str) -> list[str]:
    """检查文档是否包含异常场景分析。"""
    exception_keywords = ["异常", "错误", "失败", "超时", "处理策略"]
    found = sum(1 for kw in exception_keywords if kw in content)
    if found < 2:
        return ["  文档中异常场景分析不足。建议至少识别并描述 2–3 个关键异常场景。"]
    return []


def check_tracking_specific(content: str) -> list[str]:
    """埋点文档专项检查。"""
    issues = []
    tracking_keywords = ["事件名称", "参数", "触发时机"]
    found = sum(1 for kw in tracking_keywords if kw in content)
    if found < 2:
        issues.append("  埋点文档缺少关键字段：建议包含「事件名称」「参数」「触发时机」等字段定义。")
    return issues


def check_prd_specific(content: str) -> list[str]:
    """PRD 文档专项检查。"""
    issues = []
    # 检查用户故事
    if "作为" not in content and "用户故事" not in content:
        issues.append("  PRD 文档建议包含用户故事（「作为[角色]，我想要...」格式）。")
    # 检查验收标准
    if "验收标准" not in content and "acceptance" not in content.lower():
        issues.append("  PRD 文档建议为核心功能包含验收标准。")
    return issues


def auto_detect_type(filepath: Path) -> str:
    """根据文件名自动检测文档类型。"""
    name = filepath.stem.lower()
    if "业务流程" in name or "flow" in name:
        return "flow"
    if "功能架构" in name or "arch" in name:
        return "arch"
    if "prd" in name or "需求文档" in name:
        return "prd"
    if "埋点" in name or "tracking" in name:
        return "tracking"
    return "all"


def main():
    if len(sys.argv) < 2:
        print("用法: python3 run_quality_check.py <markdown_file> [--type flow|arch|prd|tracking|all]")
        sys.exit(1)

    filepath = Path(sys.argv[1])
    if not filepath.exists():
        print(f"错误: 文件不存在 - {filepath}")
        sys.exit(1)

    # 确定文档类型
    doc_type = "all"
    if "--type" in sys.argv:
        type_idx = sys.argv.index("--type") + 1
        if type_idx < len(sys.argv):
            doc_type = sys.argv[type_idx]
            if doc_type not in ("flow", "arch", "prd", "tracking", "all"):
                print(f"错误: 不支持的文档类型 '{doc_type}'。支持: flow | arch | prd | tracking | all")
                sys.exit(1)
    else:
        # 根据文件名自动检测
        detected = auto_detect_type(filepath)
        if detected != "all":
            doc_type = detected
            print(f"自动检测文档类型: {doc_type}（可用 --type 参数手动指定）")

    print(f"正在检查文件: {filepath.name}")
    print(f"检查类型: {doc_type}")
    print("-" * 40)

    try:
        content = filepath.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            content = filepath.read_text(encoding="gbk")
            print("⚠️  检测到非 UTF-8 编码，已使用 GBK 编码读取。")
        except Exception as e:
            print(f"错误: 无法读取文件 - {e}")
            sys.exit(1)

    all_issues = []

    # 通用检查（所有类型）
    all_issues.extend(check_mermaid(content))
    all_issues.extend(check_tables(content))

    # 按文档类型执行专项检查
    if doc_type in DOC_TYPE_MAP:
        all_issues.extend(check_sections(content, DOC_TYPE_MAP[doc_type]))

    if doc_type in ("flow", "prd", "all"):
        all_issues.extend(check_priority_labels(content))
        all_issues.extend(check_exceptions(content))

    if doc_type == "arch":
        all_issues.extend(check_priority_labels(content))

    if doc_type == "prd":
        all_issues.extend(check_prd_specific(content))

    if doc_type == "tracking":
        all_issues.extend(check_tracking_specific(content))

    if doc_type == "all":
        # 通用：检查是否有基本优先级标注
        all_issues.extend(check_priority_labels(content))

    # 输出结果
    if all_issues:
        print(f"\n⚠️  发现 {len(all_issues)} 个质量问题:\n")
        for issue in all_issues:
            print(issue)
        print(f"\n请根据以上建议完善文档后重新检查。")
        sys.exit(1)
    else:
        print(f"\n✅ 质量检查通过！文档 '{filepath.name}' 满足所有检查项。")
        sys.exit(0)


if __name__ == "__main__":
    main()
