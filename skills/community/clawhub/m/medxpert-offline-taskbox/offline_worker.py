#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""断网 Worker：读本地任务箱的待办任务，逐条调本机 Ollama 跑，结果写回任务箱。

v2.4.0 新增：
- 失败重试（默认 2 次，指数退避；--retry 可调）
- --level 过滤（默认只跑 L1 本地级 + 未打标任务，--level all 跑全部）
- 防僵尸续跑（running 超过 60 分钟自动重置为 queued）
- 重试耗尽 → 任务标记 failed（带原因），不再误标 done

断网可跑——模型权重在本地，Ollama 监听 127.0.0.1:11434，不触外网。
依赖：本地已 `ollama pull` 好模型；同目录下的 local_taskbox.py。

用法：
  python offline_worker.py                          # 默认：只跑 L1 本地级任务
  python offline_worker.py --model qwen2.5:7b       # 指定模型
  python offline_worker.py --level all --retry 3    # 全部任务 + 最多重试 3 次
"""
import os
import subprocess
import sys
import time
import argparse

import local_taskbox as tb

DEFAULT_MODEL = "deepseek-r1:7b"   # 默认模型；也可用 --model 临时指定
OLLAMA_CLI = "ollama"             # 若在 PATH 外，填绝对路径
DEFAULT_RETRY = 2                 # 失败后最多重试次数（不含首次）
RUNNING_STALE_MIN = 60            # running 超过该分钟数视为僵尸，重置续跑


def run_ollama(prompt, model, retries=DEFAULT_RETRY, timeout=900):
    """调用本机 Ollama 推理，带失败重试（指数退避）。

    返回 (output, error)：output 为模型输出；error 为 None 表示成功，
    否则为最后一次失败的明确原因（重试耗尽后返回）。
    """
    last_err = ""
    for attempt in range(retries + 1):
        try:
            r = subprocess.run(
                [OLLAMA_CLI, "run", model, prompt],
                capture_output=True,
                text=True,
                encoding="utf-8",      # Windows 中文系统下 cmd 输出常为 GBK，
                errors="replace",      # 统一按 UTF-8 读取，乱码字节替换为 �，绝不崩
                timeout=timeout,
            )
            out = (r.stdout or "").strip()
            err = (r.stderr or "").strip()
            if r.returncode != 0:
                last_err = f"退出码 {r.returncode}：{err or out or '无输出'}"
            elif not out:
                last_err = f"无输出：{err or 'Ollama 未返回内容'}"
            else:
                return out, None
        except subprocess.TimeoutExpired:
            last_err = f"超时（>{timeout}s）"
        except FileNotFoundError:
            return "", "未找到 ollama 命令。请先安装 Ollama，或在脚本中把 OLLAMA_CLI 改为绝对路径。"
        except Exception as e:
            last_err = f"{e}"
        if attempt < retries:
            wait = 2 * (attempt + 1)   # 2s / 4s 退避
            print(f"  调用失败（{last_err}），{wait}s 后重试（{attempt + 1}/{retries}）")
            time.sleep(wait)
    return "", f"重试 {retries} 次仍失败：{last_err}"


def recover_stale(tasks):
    """防僵尸：把 running 超过阈值的任务重置为 queued，断电重连可续跑。"""
    from datetime import datetime
    revived = 0
    for t in tasks:
        if t["status"] != "running":
            continue
        try:
            updated = datetime.strptime(t.get("updated_at", ""), "%Y-%m-%d %H:%M:%S")
        except ValueError:
            updated = datetime.now()
        if (datetime.now() - updated).total_seconds() > RUNNING_STALE_MIN * 60:
            t["status"] = "queued"
            t["result"] = (t.get("result") or "") + "（上次运行中断，已重置待续跑）"
            t["updated_at"] = tb.now()
            revived += 1
    if revived:
        print(f"防僵尸：重置 {revived} 个中断任务为 queued")
    return revived


def main():
    p = argparse.ArgumentParser(description="断网 Worker：调本机 Ollama 处理任务箱（v2.4.0）")
    p.add_argument("--model", default=DEFAULT_MODEL,
                   help=f"Ollama 模型名（默认 {DEFAULT_MODEL}），如 qwen2.5:7b")
    p.add_argument("--level", default="L1",
                   help="只处理该级别的任务（默认 L1 = 本地级，含未打标任务；all = 全部级别）")
    p.add_argument("--retry", type=int, default=DEFAULT_RETRY,
                   help=f"失败重试次数（默认 {DEFAULT_RETRY}）")
    args = p.parse_args()
    model = args.model
    level = args.level

    try:
        tasks = tb.load()
    except SystemExit:
        return
    if not tasks:
        print("任务箱为空，退出。")
        return

    recover_stale(tasks)

    if level == "all":
        todo = [t for t in tasks if t["status"] in ("queued", "running")]
    else:
        todo = [t for t in tasks
                if t["status"] in ("queued", "running")
                and t.get("level", "L1") == level]
    if not todo:
        print(f"没有 {level} 级待办任务，退出。（可用 --level all 处理全部）")
        return
    # 排序：优先级降序，同优先级按创建时间升序
    todo.sort(key=lambda t: (-t.get("priority", 5), t.get("created_at", "")))

    for t in todo:
        print(f"== 处理 #{t['id']} [{t.get('level','L1')}]：{t['title']}（模型 {model}）")
        t["status"] = "running"
        t["updated_at"] = tb.now()
        tb.save(tasks)

        prompt = (
            f"任务：{t['title']}\n详情：{t['detail']}\n"
            f"请完成上述任务并给出结果。\n"
            f"输出格式要求：\n"
            f"1. 以「【结论】」开头，一句话给出最终结论；\n"
            f"2. 正文分点说明（每点 ≤50 字）；\n"
            f"3. 以「【下一步】」结尾，给出 1-3 条建议。\n"
            f"全程使用简体中文，总长度控制在 300 字以内。"
        )
        result, err = run_ollama(prompt, model, retries=args.retry)

        if err:
            t["status"] = "failed"
            t["result"] = f"[调用失败] {err}"
            print(f"== 失败 #{t['id']}：{err}")
        else:
            t["status"] = "done"
            t["result"] = result
            print(f"== 完成 #{t['id']}，结果长度 {len(result)}")
        t["updated_at"] = tb.now()
        tb.save(tasks)


if __name__ == "__main__":
    main()
