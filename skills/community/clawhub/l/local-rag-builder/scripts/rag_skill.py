"""
local-rag-builder 技能接口模块
v0.2.0

纯技能模式：只检索，不调用 LLM。
- 无 LLM 依赖（不 import langchain_community.llms）
- 无交互式 CLI
- 所有输出为结构化 JSON，供任何智能体（xxxx 等）消费
- prompt 模板在输出中被正确填充，智能体直接使用即可

用法:
  python scripts/rag_skill.py --query "问题" --kb default [--template "模板"] [--json]
"""

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rag_core import get_embeddings, format_skill_output, import_documents_to_kb
from knowledge_base_manager import list_knowledge_bases, get_kb_stats
from prompt_manager import load_template


def run_query(question, kb="default", k=None, threshold=None, template=None, json_output=False):
    """单次检索查询"""
    try:
        embeddings = get_embeddings()
        result = format_skill_output(
            question, kb_name=kb, k=k,
            score_threshold=threshold,
            embeddings=embeddings,
            template=template,
        )
        if json_output:
            print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
        else:
            _print_human(result)
        return 0
    except ValueError as e:
        _print_error(f"配置错误: {e}", json_output)
        return 1
    except Exception as e:
        _print_error(f"检索失败: {e}", json_output)
        return 1


def run_import(file_path, kb="default", json_output=False):
    """导入文件到知识库"""
    if not os.path.exists(file_path):
        _print_error(f"文件不存在: {file_path}", json_output)
        return 1
    try:
        embeddings = get_embeddings()
        result = import_documents_to_kb(file_path, kb, embeddings)
        if json_output:
            print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
        else:
            status = "OK" if result["success"] else "!"
            print(f"[{status}] {result['message']}")
            print(f"  切分块数: {result['chunks_count']}")
            print(f"  来源: {result['source']}")
        return 0
    except Exception as e:
        _print_error(f"导入失败: {e}", json_output)
        return 1


def run_kb_list(json_output=False):
    """列出知识库"""
    kbs = list_knowledge_bases()
    stats = get_kb_stats()
    if json_output:
        output = {"knowledge_bases": kbs, "statistics": stats}
        print(json.dumps(output, ensure_ascii=False, indent=2, default=str))
    else:
        print(f"知识库 ({len(kbs)} 个):")
        for name, info in kbs.items():
            print(f"  {name}: {info.get('description', '')} [{info.get('doc_count', 0)} 文档]")
        print(f"\n总文档块: {stats.get('total_docs', 0)}")
    return 0


def _print_human(result):
    """人类可读输出"""
    print(f"问题: {result['question']}")
    print(f"知识库: {result['kb']}")
    print(f"检索片段: {result['source_count']} 个")
    print()
    if result["has_context"]:
        print("=" * 50)
        print("检索到的上下文:")
        print("=" * 50)
        print(result["context"])
        print()
        print("=" * 50)
        print("完整的 Prompt（已填充）:")
        print("=" * 50)
        print(result["prompt"])
    else:
        print("知识库中未找到相关信息。")


def _print_error(msg, json_output):
    if json_output:
        print(json.dumps({"error": msg, "success": False}, ensure_ascii=False))
    else:
        print(f"[!] {msg}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="local-rag-builder 技能接口（纯检索，不调用 LLM）")
    parser.add_argument("--query", type=str, help="检索问题")
    parser.add_argument("--kb", type=str, default="default", help="知识库名称")
    parser.add_argument("--k", type=int, help="返回片段数")
    parser.add_argument("--threshold", type=float, help="相似度阈值 (0-1)")
    parser.add_argument("--template", type=str, help="自定义 prompt 模板（含 {context} {question}）")
    parser.add_argument("--import-file", type=str, dest="import_file", help="导入文件到知识库")
    parser.add_argument("--kb-list", action="store_true", help="列出知识库")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")

    args = parser.parse_args()

    if args.import_file:
        sys.exit(run_import(args.import_file, args.kb, args.json))

    if args.kb_list:
        sys.exit(run_kb_list(args.json))

    if args.query:
        sys.exit(run_query(args.query, args.kb, args.k, args.threshold, args.template, args.json))

    parser.print_help()
    sys.exit(1)
