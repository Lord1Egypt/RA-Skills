#!/usr/bin/env python3
"""
本地大模型图书馆 - 快速起步脚本 v1.29.1
依赖:
  - Ollama 已安装并运行 (localhost:11434)
  - Python 库: requests (安装: pip install requests)
用法:
  python quickstart.py doctor        # 一键环境自检（推荐先跑这个，问题+解法一次说清）
  python quickstart.py init          # 初始化图书馆目录
  python quickstart.py setup         # 一键部署（检测 Ollama + git init + 拉模型）
  python quickstart.py summarize     # 批量摘要
  python quickstart.py ask "问题"    # 提问
  python quickstart.py health        # 知识库健康检查
  python quickstart.py scan          # 脱敏扫描（手机号/身份证/邮箱/公司名）
  python quickstart.py check         # 检查 Ollama 状态
"""

import os
import sys
import json
import time
import shutil
import platform
from datetime import datetime

try:
    import requests
except ImportError:
    print("[错误] 缺少 Python 依赖库 requests")
    print("       请先安装: pip install requests")
    print("       (或使用: python -m pip install requests)")
    sys.exit(1)

OLLAMA_BASE = os.environ.get("OLLAMA_BASE", "http://localhost:11434")
OLLAMA_URL = f"{OLLAMA_BASE}/api/generate"
MODEL = os.environ.get("LLM_MODEL", "qwen2.5:3b")
LIBRARY_DIR = os.environ.get("LIBRARY_DIR", "my-library")
CHUNK_SIZE = 2000
MAX_RETRIES = 3
OLLAMA_TIMEOUT = 5


def request_with_retry(method, url, **kwargs):
    """带自动重试的 Ollama 请求封装（R 维度：网络抖动自动恢复）。

    - 连接失败、超时、HTTP 4xx/5xx 都会自动重试，最多 3 次（指数退避）
    - 每次失败报「人话」而非堆栈：用户知道发生了什么、该怎么处理
    - 全部重试失败返回 None，由调用方决定跳过还是提示
    """
    last_err = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.request(
                method, url,
                timeout=kwargs.pop("timeout", 300),
                **kwargs
            )
            if resp.status_code == 404:
                last_err = "模型不存在（请先拉取模型: ollama pull qwen2.5:3b）"
            elif resp.status_code == 500:
                last_err = "Ollama 服务异常（试试: ollama stop 后重新 ollama serve）"
            elif resp.status_code >= 400:
                last_err = f"HTTP {resp.status_code}: {resp.text[:120]}"
            else:
                return resp
        except requests.exceptions.ConnectionError:
            last_err = "Ollama 连不上（服务没启动？先运行: ollama serve）"
        except requests.exceptions.Timeout:
            last_err = "请求超时（模型正在加载或电脑繁忙）"
        except Exception as e:
            last_err = f"请求出错: {e}"
        if attempt < MAX_RETRIES:
            wait = attempt * 2
            print(f"    [重试 {attempt}/{MAX_RETRIES}] {last_err}，{wait}秒后重试…")
            time.sleep(wait)
    print(f"    [失败] {last_err}")
    return None


def check_ollama():
    """检查 Ollama 是否在线（带超时与异常分类）"""
    try:
        resp = requests.get(f"{OLLAMA_BASE}/api/tags", timeout=OLLAMA_TIMEOUT)
        if resp.status_code != 200:
            print(f"[!] Ollama 返回异常状态码: {resp.status_code}")
            return False
        models = [m["name"] for m in resp.json().get("models", [])]
        if not models:
            print("[!] Ollama 在线但没有已安装的模型")
            print("    请运行: ollama pull qwen2.5:3b")
            return False
        print(f"[OK] Ollama 在线，可用模型: {', '.join(models)}")
        if MODEL not in " ".join(models):
            print(f"[!] 当前设定模型 {MODEL} 未安装，请运行: ollama pull {MODEL}")
            return False
        return True
    except requests.exceptions.ConnectionError:
        print("[!] Ollama 连不上——先启动服务: ollama serve（Windows 装完需重启终端）")
        return False
    except requests.exceptions.Timeout:
        print("[!] 连 Ollama 超时，等几秒再试（模型可能正在加载）")
        return False
    except Exception as e:
        print(f"[!] 检查 Ollama 时出错: {e}")
        return False


def doctor():
    """一键环境自检：问题在哪、怎么修，一次说清（R 维度核心）"""
    print("=" * 56)
    print("本地大模型图书馆 · 环境自检 (doctor)")
    print("=" * 56)
    issues = 0

    ver = platform.python_version()
    major = int(ver.split(".")[0])
    print(f"\n[1/5] Python 版本: {ver}  " + ("✓" if major >= 3 else "✗ 需要 Python 3+，请先安装"))
    if major < 3:
        issues += 1

    print(f"[2/5] requests 库: ✓ 已安装 (v{requests.__version__})")

    try:
        resp = requests.get(f"{OLLAMA_BASE}/api/tags", timeout=OLLAMA_TIMEOUT)
        if resp.status_code == 200:
            models = [m["name"] for m in resp.json().get("models", [])]
            print(f"[3/5] Ollama 服务: ✓ 在线（已装 {len(models)} 个模型）")
            if models:
                print(f"      已装模型: {', '.join(models[:8])}")
            if MODEL not in " ".join(models):
                print(f"      ⚠ 目标模型 {MODEL} 未安装 → 运行: ollama pull {MODEL}")
                issues += 1
            else:
                print(f"      目标模型 {MODEL}: ✓ 已就绪")
        else:
            print(f"[3/5] Ollama 服务: ✗ 返回 HTTP {resp.status_code}（先运行: ollama serve）")
            issues += 1
    except requests.exceptions.ConnectionError:
        print("[3/5] Ollama 服务: ✗ 连不上（先运行: ollama serve；Windows 装完 Ollama 需重启终端）")
        issues += 1
    except requests.exceptions.Timeout:
        print("[3/5] Ollama 服务: ✗ 超时（模型加载中？等几秒再试）")
        issues += 1

    try:
        usage = shutil.disk_usage(".")
        free_gb = usage.free / (1024 ** 3)
        if free_gb >= 5:
            print(f"[4/5] 磁盘空间: ✓ 剩余 {free_gb:.1f} GB（3B 模型约需 2-3GB）")
        else:
            print(f"[4/5] 磁盘空间: ✗ 仅剩 {free_gb:.1f} GB，建议 ≥5GB（3B 模型约需 2-3GB）")
            issues += 1
    except Exception as e:
        print(f"[4/5] 磁盘空间: ⚠ 检查失败 ({e})")

    if os.path.isdir(LIBRARY_DIR):
        print(f"[5/5] 知识库目录 '{LIBRARY_DIR}/': ✓ 已存在")
    else:
        print(f"[5/5] 知识库目录 '{LIBRARY_DIR}/': ⚠ 未初始化 → 运行: python quickstart.py init")
        issues += 1

    print("\n" + "=" * 56)
    if issues == 0:
        print("自检通过 ✓ 环境就绪，可以开始用了！")
        print("下一步: python quickstart.py init && python quickstart.py summarize")
    else:
        print(f"共 {issues} 项需处理，按上方提示修复后重跑 doctor 复检。")
        print("（80% 的问题是 Ollama 没启动，先试: ollama serve）")
    print("=" * 56)
    return issues == 0


def init_library():
    """初始化图书馆目录结构（幂等：重复运行不产生副作用）"""
    dirs = [
        "01-法规",
        "02-产品",
        "03-标准",
        "04-学习笔记",
        "05-运营",
        "06-模板",
    ]
    for d in dirs:
        path = os.path.join(LIBRARY_DIR, d)
        os.makedirs(path, exist_ok=True)
        print(f"  [创建] {path}/")

    index_path = os.path.join(LIBRARY_DIR, "00-index.md")
    if not os.path.exists(index_path):
        with open(index_path, "w", encoding="utf-8") as f:
            f.write("# 知识库索引\n\n")
            f.write(f"> 最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            f.write("| 文件 | 分类 | 摘要 | 更新日期 |\n")
            f.write("|------|------|------|----------|\n")
        print(f"  [创建] {index_path}")

    changelog = os.path.join(LIBRARY_DIR, "changelog.md")
    if not os.path.exists(changelog):
        with open(changelog, "w", encoding="utf-8") as f:
            f.write("# 变更日志\n\n")
            f.write(f"- {datetime.now().strftime('%Y-%m-%d')}: 图书馆初始化\n")
        print(f"  [创建] {changelog}")

    print(f"\n[完成] 图书馆已初始化: {LIBRARY_DIR}/")
    print("下一步: 把你的文档（.md/.txt）放到对应目录，然后运行 summarize")


def summarize_file(filepath):
    """让本地模型给单个文件做摘要（容错：空文件/非 UTF-8/读取失败都跳过不崩）"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        print(f"    [跳过] {filepath} 不是 UTF-8 文本（二进制文件？只处理 .md/.txt）")
        return "[跳过: 非文本文件]"
    except OSError as e:
        print(f"    [跳过] {filepath} 读取失败: {e}")
        return "[跳过: 读取失败]"

    if not content.strip():
        print(f"    [跳过] {filepath} 是空文件")
        return "[跳过: 空文件]"

    if len(content) <= CHUNK_SIZE:
        chunks = [content]
    else:
        chunks = [content[i:i + CHUNK_SIZE] for i in range(0, len(content), CHUNK_SIZE)]

    summaries = []
    for i, chunk in enumerate(chunks):
        print(f"    分块 {i + 1}/{len(chunks)}...", end="", flush=True)
        resp = request_with_retry("POST", OLLAMA_URL, json={
            "model": MODEL,
            "prompt": f"请用中文给以下内容做摘要，提取关键信息，200字以内：\n\n{chunk}",
            "stream": False
        }, timeout=300)
        if resp is None:
            print(" 失败")
            summaries.append(f"[摘要失败: 模型未响应，请用 doctor 检查环境]")
        else:
            summary = resp.json().get("response", "[摘要失败]")
            summaries.append(summary)
            print(" OK")

    return "\n\n".join(summaries)


def batch_summarize():
    """批量给知识库所有文件做摘要，更新索引"""
    if not check_ollama():
        return

    print(f"\n开始批量摘要 (模型: {MODEL})\n")

    index_lines = [
        "# 知识库索引\n",
        f"> 最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n",
        "| 文件 | 分类 | 摘要 | 更新日期 |",
        "|------|------|------|----------|",
    ]
    count = 0

    for root, dirs, files in os.walk(LIBRARY_DIR):
        for fname in sorted(files):
            if not fname.endswith((".md", ".txt")) or fname.startswith("00-index"):
                continue
            filepath = os.path.join(root, fname)
            rel_path = os.path.relpath(filepath, LIBRARY_DIR)
            category = os.path.relpath(root, LIBRARY_DIR)

            print(f"  处理: {rel_path}")
            summary = summarize_file(filepath)
            summary_oneline = summary.replace("\n", " ")[:100]
            index_lines.append(f"| {fname} | {category} | {summary_oneline} | {datetime.now().strftime('%Y-%m-%d')} |")
            count += 1

    if count == 0:
        print("[!] 没有找到 .md/.txt 文件——先把文档放进知识库目录，再跑 summarize。")
        return

    index_path = os.path.join(LIBRARY_DIR, "00-index.md")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("\n".join(index_lines) + "\n")

    print(f"\n[完成] 已处理 {count} 个文件，索引已更新: {index_path}")


def ask_library(question):
    """基于知识库回答问题（容错：空库明确提示，不空转）"""
    if not check_ollama():
        return

    context = ""
    for root, dirs, files in os.walk(LIBRARY_DIR):
        for fname in files:
            if fname.endswith((".md", ".txt")):
                filepath = os.path.join(root, fname)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                except (UnicodeDecodeError, OSError):
                    continue
                context += f"\n--- {fname} ---\n{content}\n"

    if not context.strip():
        print("[!] 知识库为空或没有可读的 .md/.txt 文件——先运行 init 建库、放入文档，再提问。")
        return

    max_context = 6000
    if len(context) > max_context:
        context = context[:max_context]
        print(f"[!] 知识库较大，已截断到 {max_context} 字符。建议升级到 RAG 方案。")

    prompt = f"""根据以下知识库内容回答问题。
要求：
1. 仅基于知识库内容回答，不要编造
2. 如果知识库中没有相关信息，明确说"知识库中未找到相关信息"
3. 回答时标注信息来源（文件名）

知识库：
{context}

问题：{question}
"""

    print(f"\n提问: {question}")
    print(f"模型: {MODEL}")
    print(f"知识库上下文: {len(context)} 字符\n")
    print("-" * 60)

    resp = request_with_retry("POST", OLLAMA_URL, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }, timeout=600)
    if resp is None:
        print("[回答失败] 模型未响应，请用 doctor 检查环境后重试。")
    else:
        print(resp.json().get("response", "[回答失败]"))

    print("-" * 60)


def health_check():
    """知识库健康检查（含磁盘空间）"""
    print(f"\n知识库健康检查: {LIBRARY_DIR}/\n")

    issues = []
    stats = {"files": 0, "total_size": 0, "categories": set(), "empty_files": 0}

    for root, dirs, files in os.walk(LIBRARY_DIR):
        if ".git" in root:
            continue
        for fname in files:
            if fname.endswith((".md", ".txt")):
                filepath = os.path.join(root, fname)
                size = os.path.getsize(filepath)
                stats["files"] += 1
                stats["total_size"] += size
                stats["categories"].add(os.path.relpath(root, LIBRARY_DIR))

                if size < 50:
                    stats["empty_files"] += 1
                    issues.append(f"  [!] 空文件: {fname}")

                with open(filepath, "r", encoding="utf-8") as f:
                    head = f.read(200)
                if "---" not in head[:10]:
                    issues.append(f"  [!] 缺少元信息头: {fname}")

    print(f"文件总数: {stats['files']}")
    print(f"总大小: {stats['total_size'] / 1024:.1f} KB")
    print(f"分类数: {len(stats['categories'])}")
    print(f"空文件: {stats['empty_files']}")

    index_path = os.path.join(LIBRARY_DIR, "00-index.md")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            index_content = f.read()
        indexed = index_content.count("|") - 2
        print(f"索引文件: 存在 (约 {indexed} 条)")
    else:
        issues.append("  [!] 索引文件不存在，请运行 summarize")
        print("索引文件: 不存在")

    git_dir = os.path.join(LIBRARY_DIR, ".git")
    if os.path.exists(git_dir):
        print("版本管理: Git 已初始化")
    else:
        issues.append("  [!] 未启用 Git 版本管理，建议运行: cd my-library && git init")
        print("版本管理: 未启用")

    try:
        usage = shutil.disk_usage(".")
        print(f"磁盘剩余: {usage.free / (1024 ** 3):.1f} GB")
    except Exception as e:
        print(f"磁盘检查失败: {e}")

    if issues:
        print(f"\n发现 {len(issues)} 个问题:")
        for issue in issues:
            print(issue)
    else:
        print("\n[OK] 一切正常!")


def scan_sensitive():
    """脱敏扫描：找出知识库里可能泄露的手机号/身份证/邮箱/公司名"""
    patterns = [
        ("手机号", r"1[3-9]\d{9}"),
        ("身份证", r"\d{17}[\dXx]"),
        ("邮箱", r"[\w.+-]+@[\w-]+\.[\w.]+"),
        ("QQ号", r"(?<!\d)[1-9]\d{5,10}(?!\d)"),
    ]
    print(f"\n脱敏扫描: {LIBRARY_DIR}/\n")
    hits = 0
    for root, dirs, files in os.walk(LIBRARY_DIR):
        if ".git" in root:
            continue
        for fname in files:
            if not fname.endswith((".md", ".txt")):
                continue
            filepath = os.path.join(root, fname)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
            except (UnicodeDecodeError, OSError):
                continue
            for label, pat in patterns:
                import re
                for m in re.finditer(pat, content):
                    line_no = content[:m.start()].count("\n") + 1
                    print(f"  [命中] {label} {os.path.join(root, fname)}:{line_no}  →  {m.group(0)}")
                    hits += 1
    if hits == 0:
        print("[OK] 未发现敏感信息 ✓")
    else:
        print(f"\n共 {hits} 处命中，请逐条确认后脱敏（可手动替换或删除）。")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1]

    if cmd == "doctor":
        doctor()
    elif cmd == "init":
        init_library()
    elif cmd == "setup":
        if check_ollama():
            init_library()
            if not os.path.isdir(os.path.join(LIBRARY_DIR, ".git")):
                try:
                    import subprocess
                    subprocess.run(["git", "init", LIBRARY_DIR], check=True)
                    print("[OK] Git 已初始化（版本管理就绪）")
                except Exception as e:
                    print(f"[!] Git 初始化失败（可手动: cd {LIBRARY_DIR} && git init）: {e}")
    elif cmd == "summarize":
        batch_summarize()
    elif cmd == "ask":
        if len(sys.argv) < 3:
            print("用法: python quickstart.py ask \"你的问题\"")
            return
        ask_library(sys.argv[2])
    elif cmd == "health":
        health_check()
    elif cmd == "scan":
        scan_sensitive()
    elif cmd == "check":
        check_ollama()
    else:
        print(f"未知命令: {cmd}")
        print(__doc__)


if __name__ == "__main__":
    main()
