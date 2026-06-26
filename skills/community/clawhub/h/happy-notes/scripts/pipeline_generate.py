#!/usr/bin/env python3
"""Pipeline: 对已有知识库直接提交创作任务

用法:
  python3 scripts/pipeline_generate.py --kb "AI论文集" --output-type PDF
  python3 scripts/pipeline_generate.py --kb "竞品分析" --output-type PPT --preset "卡通" --query "对比分析"
  python3 scripts/pipeline_generate.py --kb-id "xxx" --output-type PODCAST --poll-creation

适用场景: 知识库已有内容，用户直接说"帮我做个PPT""生成一份报告"，不涉及上传或搜索前置步骤。
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from iflow_common import (
    log, find_kb, submit_creation, poll_creation, output,
    validate_output_type, validate_preset,
)


def main():
    parser = argparse.ArgumentParser(description="对已有知识库直接提交创作任务")
    parser.add_argument("--kb", default="", help="知识库名称")
    parser.add_argument("--kb-id", default="", help="知识库 ID")
    parser.add_argument("--output-type", default="PDF", help="生成类型: PDF/DOCX/MARKDOWN/PPT/XMIND/PODCAST/VIDEO")
    parser.add_argument("--query", default="", help="创作要求")
    parser.add_argument("--preset", default="", help="PPT 风格: 商务/卡通（仅 PPT 有效）")
    parser.add_argument("--poll-creation", action="store_true", help="轮询等待创作完成")
    args = parser.parse_args()

    # 参数校验
    args.output_type = validate_output_type(args.output_type)
    validate_preset(args.preset, args.output_type)

    kb_id = find_kb(args.kb or None, args.kb_id or None)
    log(f"知识库 ID: {kb_id}")

    # 提交创作任务
    creation_id = submit_creation(
        kb_id,
        output_type=args.output_type,
        query=args.query or None,
        preset=args.preset or None,
    )

    result = {
        "collectionId": kb_id,
        "creationId": creation_id,
        "creationStatus": "submitted" if creation_id else "failed",
    }

    if creation_id and args.poll_creation:
        status = poll_creation(kb_id, creation_id)
        result["creationStatus"] = status

    output(result)


if __name__ == "__main__":
    main()
