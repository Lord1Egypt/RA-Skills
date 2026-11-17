"""
local-rag-builder 独立模式（全链路系统）
v0.2.0

独立运行模式：检索 + LLM 调用全链路。
需要外部 LLM 服务（LM Studio / Ollama / vLLM），用户自行选择平台和模型。

LLM 接入配置（在 config 中设置）:
  - base_url: 外部服务的 API 地址
  - api_key: API 密钥（多数本地服务填 "not-needed"）
  - 各平台默认地址见 references/llm-setup.md

用法:
  python scripts/rag_standalone.py                  # 交互式 CLI
  python scripts/rag_standalone.py --query "问题"     # 单次问答
"""

import os
import sys
import re
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rag_core import get_embeddings, retrieve_context, import_documents_to_kb
from config import load_config, save_config, reset_config
from prompt_manager import load_template, save_template, reset_template, get_default_template, build_prompt
from knowledge_base_manager import list_knowledge_bases, create_knowledge_base, delete_knowledge_base

HELP_TEXT = """
可用命令:
  /help             显示此帮助
  /prompt show      显示当前 Prompt 模板
  /prompt set       设置 Prompt 模板（输入 END 结束）
  /prompt reset     重置为默认模板
  /kb list          列出所有知识库
  /kb create <name> 创建新知识库
  /kb use <name>    切换到指定知识库
  /kb delete <name> 删除知识库
  /config show      显示当前配置
  /config set <key> <value>  修改配置
  /verify-llm       验证 LLM 连接
  /llm-help         显示外部 LLM 接入指南
  /exit             退出
"""


def get_llm(base_url=None, temperature=None, max_tokens=None):
    """获取 LLM 实例（通过 OpenAI 兼容接口）"""
    from langchain_community.llms import OpenAI

    cfg = load_config()
    llm_cfg = cfg.get("llm", {})

    return OpenAI(
        base_url=base_url or llm_cfg.get("base_url", "http://localhost:1234/v1"),
        api_key=llm_cfg.get("api_key", "not-needed"),
        temperature=temperature if temperature is not None else llm_cfg.get("temperature", 0.1),
        max_tokens=max_tokens or llm_cfg.get("max_tokens", 512),
    )


def verify_llm_connection():
    """验证 LLM 连接"""
    cfg = load_config()
    llm_cfg = cfg.get("llm", {})
    base_url = llm_cfg.get("base_url", "http://localhost:1234/v1")

    import urllib.request
    try:
        req = urllib.request.Request(f"{base_url}/models")
        with urllib.request.urlopen(req, timeout=10) as resp:
            return True, "LLM 连接正常"
    except Exception as e:
        return False, f"LLM 连接失败: {e}"


def answer_question(question, kb_name="default", template=None, llm_instance=None,
                    embeddings=None, k=None, score_threshold=None):
    """完整 RAG 问答：检索 + LLM 生成"""
    retrieval = retrieve_context(
        question, kb_name=kb_name, k=k,
        score_threshold=score_threshold, embeddings=embeddings,
    )

    docs = retrieval["source_docs"]
    context = retrieval["context"]

    if not docs:
        return {
            "answer": "知识库中未找到相关信息。请先导入文档。",
            "source_docs": [],
            "context": "",
            "question": question,
        }

    prompt = build_prompt(context, question, template)

    if llm_instance is None:
        llm_instance = get_llm()

    try:
        raw_answer = llm_instance.invoke(prompt)
    except Exception as e:
        return {
            "answer": f"LLM 调用失败: {str(e)}",
            "source_docs": docs,
            "context": context,
            "question": question,
            "llm_error_detail": "请确认外部 LLM 服务正在运行。"
                                "各平台配置方式见 references/llm-setup.md 或运行 /llm-help",
        }

    clean_answer = re.sub(r"<think>.*?</think>\s*", "", raw_answer, flags=re.DOTALL).strip()

    return {
        "answer": clean_answer,
        "source_docs": docs,
        "context": context,
        "question": question,
    }


def print_llm_help():
    """打印外部 LLM 接入指南"""
    print("""
==============================
外部 LLM 服务接入指南
==============================

本 mode 需要外部 LLM 服务才能工作。以下三个方案任选其一：

--- LM Studio（图形界面，适合新手）---
1. 下载安装: https://lmstudio.ai
2. 搜索模型（如 Qwen2.5-7B-Instruct-GGUF、DeepSeek-R1-GGUF）
3. 点击 Download 下载
4. Local Inference Server -> 选择模型 -> Start Server
5. API 地址: http://localhost:1234/v1
6. 在 config 中设置: base_url = http://localhost:1234/v1

--- Ollama（命令行，适合开发者）---
1. 下载安装: https://ollama.com
2. 拉取模型: ollama pull qwen2.5:7b
            ollama pull deepseek-r1:7b
            ollama pull gemma3:7b
3. 运行: ollama serve（自动启动 API）
4. API 地址: http://localhost:11434/v1
5. 在 config 中设置: base_url = http://localhost:11434/v1

--- vLLM（生产高性能）---
1. pip install vllm
2. 启动: python -m vllm.entrypoints.openai.api_server \\
          --model Qwen/Qwen2.5-7B-Instruct --port 8000
3. API 地址: http://localhost:8000/v1
4. 在 config 中设置: base_url = http://localhost:8000/v1

设置方式:
  Web 面板: 启动 python scripts/rag_web_ui.py，在 LLM 卡片修改
  CLI: /config set llm.base_url http://localhost:1234/v1
==============================
""")


def run_interactive():
    """交互式 RAG 对话（独立模式）"""
    cfg = load_config()
    active_kb = cfg.get("kb", {}).get("active_kb", "default")

    print("=" * 50)
    print("  local-rag-builder 独立模式")
    print("=" * 50)

    # 验证 LLM 连接
    llm_ok, llm_msg = verify_llm_connection()
    print(f"  [{chr(10003) if llm_ok else '!'}] {llm_msg}")
    if not llm_ok:
        print("  输入 /llm-help 查看外部 LLM 接入指南")
    else:
        print("  [i] LLM 已就绪")

    # 检查嵌入模型
    try:
        embeddings = get_embeddings()
        print(f"  [{chr(10003)}] 嵌入模型就绪")
    except ValueError as e:
        print(f"  [!] {e}")
        print("  请先运行: python scripts/embedding_model_manager.py --interactive")
        embeddings = None

    print(f"  当前知识库: {active_kb}")
    print(f"  输入 /help 查看命令，直接输入问题开始问答")
    print("=" * 50)

    llm = get_llm() if llm_ok else None

    while True:
        try:
            user_input = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n退出。")
            break

        if not user_input:
            continue

        if user_input.startswith("/"):
            parts = user_input.split(maxsplit=2)
            cmd = parts[0].lower()

            if cmd == "/exit":
                print("退出。")
                break

            elif cmd == "/help":
                print(HELP_TEXT)

            elif cmd == "/llm-help":
                print_llm_help()

            elif cmd == "/prompt":
                sub = parts[1].lower() if len(parts) > 1 else ""
                if sub == "show":
                    print(f"\n当前 Prompt 模板:\n{'-' * 40}\n{load_template()}\n{'-' * 40}")
                elif sub == "set":
                    print("请输入新模板（输入 END 单独一行结束）：")
                    lines = []
                    while True:
                        try:
                            line = input()
                            if line.strip() == "END":
                                break
                            lines.append(line)
                        except EOFError:
                            break
                    content = "\n".join(lines)
                    if content.strip():
                        save_template(content)
                        print(f"[OK] 模板已保存 ({len(content)} 字符)")
                    else:
                        print("[!] 模板为空，未保存")
                elif sub == "reset":
                    print("[OK] 已重置为默认模板")
                else:
                    print("用法: /prompt show|set|reset")

            elif cmd == "/kb":
                sub = parts[1].lower() if len(parts) > 1 else ""
                if sub == "list":
                    kbs = list_knowledge_bases()
                    for name, info in kbs.items():
                        print(f"  {name}: {info.get('description', '')} [{info.get('doc_count', 0)} 文档]")
                elif sub == "create" and len(parts) > 2:
                    ok, msg = create_knowledge_base(parts[2])
                    print(f"[{'OK' if ok else '!'}] {msg}")
                elif sub == "use" and len(parts) > 2:
                    cfg = load_config()
                    if "kb" not in cfg:
                        cfg["kb"] = {}
                    cfg["kb"]["active_kb"] = parts[2]
                    save_config(cfg)
                    print(f"[OK] 已切换到知识库 '{parts[2]}'")
                    active_kb = parts[2]
                elif sub == "delete" and len(parts) > 2:
                    ok, msg = delete_knowledge_base(parts[2])
                    print(f"[{'OK' if ok else '!'}] {msg}")
                else:
                    print("用法: /kb list|create <name>|use <name>|delete <name>")

            elif cmd == "/config":
                sub = parts[1].lower() if len(parts) > 1 else ""
                if sub == "show":
                    print(json.dumps(load_config(), ensure_ascii=False, indent=2))
                elif sub == "set" and len(parts) > 3:
                    key_path = parts[2].split(".")
                    value = parts[3]
                    try:
                        value = int(value)
                    except ValueError:
                        try:
                            value = float(value)
                        except ValueError:
                            if value.lower() in ("true", "false"):
                                value = value.lower() == "true"
                    try:
                        cfg = load_config()
                        target = cfg
                        for k in key_path[:-1]:
                            if k not in target:
                                target[k] = {}
                            target = target[k]
                        target[key_path[-1]] = value
                        save_config(cfg)
                        print(f"[OK] 已设置 {parts[2]} = {value}")
                    except Exception as e:
                        print(f"[!] 设置失败: {e}")
                else:
                    print("用法: /config show|set <key> <value>")

            elif cmd == "/verify-llm":
                ok, msg = verify_llm_connection()
                print(f"[{'OK' if ok else '!'}] {msg}")
                if ok:
                    llm = get_llm()

            else:
                print(f"未知命令: {cmd}。输入 /help 查看可用命令")
        else:
            # 问答
            if embeddings is None:
                print("[!] 嵌入模型未加载，请先通过 /model 配置")
                continue
            if llm is None:
                print("[!] LLM 未连接。输入 /llm-help 查看接入指南，或 /verify-llm 重试")
                continue

            try:
                print("  思考中...")
                result = answer_question(user_input, kb_name=active_kb,
                                         embeddings=embeddings, llm_instance=llm)
                print(f"\n{result['answer']}")
                if result.get("source_docs"):
                    print(f"\n--- 引用片段 ({len(result['source_docs'])} 个) ---")
                    for i, doc in enumerate(result["source_docs"]):
                        content = doc.get("content", "")[:120] if isinstance(doc, dict) else str(doc)[:120]
                        print(f"  [{i + 1}] {content}...")
            except Exception as e:
                print(f"[!] 错误: {e}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="local-rag-builder 独立模式（检索 + LLM 全链路）")
    parser.add_argument("--query", type=str, help="单次问答，完成后退出")
    parser.add_argument("--kb", type=str, help="初始知识库")
    parser.add_argument("--k", type=int, help="检索文档数")
    parser.add_argument("--threshold", type=float, help="相似度阈值")
    parser.add_argument("--json", action="store_true", help="单次问答输出 JSON")
    parser.add_argument("--import-file", type=str, dest="import_file", help="导入文件到知识库")
    parser.add_argument("--verify-llm", action="store_true", help="验证 LLM 连接")
    parser.add_argument("--llm-help", action="store_true", help="显示外部 LLM 接入指南")

    args = parser.parse_args()

    if args.kb:
        cfg = load_config()
        cfg["kb"]["active_kb"] = args.kb
        save_config(cfg)

    if args.verify_llm:
        ok, msg = verify_llm_connection()
        print(f"[{'OK' if ok else '!'}] {msg}")
        sys.exit(0)

    if args.llm_help:
        print_llm_help()
        sys.exit(0)

    if args.import_file:
        if not os.path.exists(args.import_file):
            print(f"[!] 文件不存在: {args.import_file}")
            sys.exit(1)
        try:
            embeddings = get_embeddings()
            result = import_documents_to_kb(args.import_file, args.kb, embeddings)
            if args.json:
                print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
            else:
                status = "OK" if result["success"] else "!"
                print(f"[{status}] {result['message']}")
                print(f"  切分块数: {result['chunks_count']}")
        except Exception as e:
            print(f"[!] 导入失败: {e}")
            sys.exit(1)
        sys.exit(0)

    if args.query:
        try:
            embeddings = get_embeddings()
            llm = get_llm()
            result = answer_question(args.query, kb_name=args.kb,
                                     embeddings=embeddings, llm_instance=llm,
                                     k=args.k, score_threshold=args.threshold)
            if args.json:
                print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
            else:
                print(f"\n{result['answer']}")
        except Exception as e:
            print(f"[!] 错误: {e}")
            sys.exit(1)
        sys.exit(0)

    run_interactive()
