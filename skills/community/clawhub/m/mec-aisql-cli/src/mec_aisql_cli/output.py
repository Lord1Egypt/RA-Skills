"""输出格式化工具模块

本模块提供统一的 CLI 输出格式化函数, 供所有命令共享。

== 设计原则 ==

所有命令的输出遵循统一格式:
  - **成功**: ``[OK] 消息`` + 数据详情
  - **失败**: ``[FAIL] [错误码] 消息``
  - **JSON 模式**: ``{"success": bool, "message": str, "data": ...}``

== 函数列表 ==

  - ``print_result()``       — 统一结果输出 (支持文本/JSON 两种模式)
  - ``confirm()``            — 交互式确认提示 (AI Bot 不应触发)
  - ``prompt_with_default()`` — 带默认值的输入提示 (AI Bot 不应触发)
"""
import json
import sys
from typing import Any, Dict, Optional

import typer


def print_result(
    result: Dict[str, Any],
    title: str = "",
    as_json: bool = False,
    success_exit: int = 0,
    failure_exit: int = 1,
    exit_on_fail: bool = True,
):
    """统一结果输出 (所有命令共用的输出入口)

    根据参数选择文本模式或 JSON 模式输出, 并在失败时设置退出码。

    Args:
        result:       API 返回的结果字典 (必须包含 success 字段)
        title:        可选的区块标题 (仅文本模式)
        as_json:      是否输出 JSON 格式 (``--json`` 模式)
        success_exit: 成功时的退出码 (默认 0)
        failure_exit: 失败时的退出码 (默认 1)
        exit_on_fail: 失败时是否自动退出 (默认 True)

    JSON 模式输出格式::

        {
          "success": true/false,
          "message": "消息",
          "data": {...},
          "error": "错误码",        // 仅失败时
          "error_message": "..."    // 仅失败时
        }

    文本模式输出格式::

        ============================================================
          标题
        ============================================================
        [OK] 操作成功
          Status:   Succeeded
          Progress: 100%
          ...

    或::

        [FAIL] [ERROR_CODE] 错误消息
    """
    is_success = result.get("success", False) or result.get("Success", False)
    data = result.get("data", {})

    # --- JSON 模式 ---
    if as_json:
        output = {
            "success": is_success,
            "message": result.get("message", result.get("Message", "")),
            "data": data,
        }
        if not is_success:
            output["error"] = result.get("code", "")
            error_msg = result.get("message", result.get("Message", ""))
            if error_msg:
                output["error_message"] = error_msg
        print(json.dumps(output, ensure_ascii=False, indent=2))
        if exit_on_fail:
            raise typer.Exit(code=success_exit if is_success else failure_exit)
        return

    # --- 文本模式: 标题 ---
    if title:
        typer.echo(f"\n{'=' * 60}")
        typer.echo(f"  {title}")
        typer.echo(f"{'=' * 60}")

    # --- 文本模式: 成功 ---
    if is_success:
        typer.echo(f"[OK] {result.get('message', result.get('Message', '操作成功'))}")
        if data:
            _print_data(data)
    # --- 文本模式: 失败 ---
    else:
        error_msg = result.get("message", result.get("Message", "操作失败"))
        error_code = result.get("code", "")
        if error_code:
            typer.echo(f"[FAIL] [{error_code}] {error_msg}")
        else:
            typer.echo(f"[FAIL] {error_msg}")

    if exit_on_fail and not is_success:
        raise typer.Exit(code=failure_exit)


def _print_data(data: Dict[str, Any]):
    """根据数据类型选择合适的展示格式

    自动识别三种数据类型:
      1. 校验结果 (含 valid/executable 字段)
      2. SQL 生成结果 (含 sql 字段)
      3. 任务状态 (含 agentStatus/progress 字段)
      4. 其他 → JSON 格式展示
    """
    if not data:
        return

    # --- 校验结果 ---
    if "valid" in data or "executable" in data:
        typer.echo(f"  Valid:      {data.get('valid', False)}")
        typer.echo(f"  Executable: {data.get('executable', False)}")
        typer.echo(f"  Risk:       {data.get('riskLevel', '-')}")
        for issue in data.get("errors", []):
            typer.echo(f"  ERROR:  {issue.get('code')}: {issue.get('message')}")
        for issue in data.get("warnings", []):
            typer.echo(f"  WARN:   {issue.get('code')}: {issue.get('message')}")
        return

    # --- SQL 生成结果 ---
    if "sql" in data:
        typer.echo(f"\n  SQL:")
        typer.echo(f"  {'-' * 56}")
        typer.echo(f"  {data['sql']}")
        typer.echo(f"  {'-' * 56}")
        # 展示 Token 消耗 (供 AI 评估成本)
        if "prompt_tokens" in data:
            typer.echo(
                f"  Tokens: input={data.get('prompt_tokens', '-')}, "
                f"output={data.get('completion_tokens', '-')}, "
                f"total={data.get('total_tokens', '-')}"
            )
        return

    # --- 任务状态 ---
    if "agentStatus" in data or "progress" in data:
        _print_status(data)
        return

    # --- 默认: JSON 格式 ---
    typer.echo(f"\n  Details:")
    typer.echo(json.dumps(data, ensure_ascii=False, indent=4))


def _print_status(data: Dict[str, Any]):
    """格式化输出任务状态信息

    展示字段: agentStatus, progress, status, aiTaskName, orderid, tableName,
    lastErrorMessage, retryCount, nextPollAfterSeconds
    """
    status = data.get("agentStatus", "-")
    progress = data.get("progress", 0)
    message = data.get("status", "")

    typer.echo(f"  Status:   {status}")
    typer.echo(f"  Progress: {progress}%")
    if message:
        typer.echo(f"  Message:  {message}")
    if data.get("aiTaskName"):
        typer.echo(f"  Task:     {data['aiTaskName']}")
    if data.get("orderid"):
        typer.echo(f"  Order:    {data['orderid']}")
    if data.get("tableName"):
        typer.echo(f"  Table:    {data['tableName']}")
    if data.get("lastErrorMessage"):
        typer.echo(f"  Error:    {data['lastErrorMessage']}")
    if data.get("retryCount") is not None:
        typer.echo(f"  Retry:    {data['retryCount']}/{data.get('maxRetryCount', '?')}")
    # 非终态时展示下次轮询建议间隔
    if not data.get("isTerminal") and data.get("nextPollAfterSeconds"):
        typer.echo(f"  Next poll: {data['nextPollAfterSeconds']}s")


def confirm(prompt_text: str = "确认继续？", default: bool = False) -> bool:
    """交互式确认提示

    AI Bot 不应触发此函数 (Bot 模式应使用 --auto-create/--auto-perform/--yes 跳过确认)。
    交互模式下使用 ``typer.prompt`` 等待用户输入 y/n。

    Args:
        prompt_text: 提示文本
        default:     默认选择 (True 默认 Yes, False 默认 No)
    Returns:
        True 用户确认, False 用户拒绝
    """
    suffix = "[Y/n]" if default else "[y/N]"
    answer = typer.prompt(f"{prompt_text} {suffix}", default=("y" if default else "n"))
    return answer.strip().lower() in ("y", "yes")


def prompt_with_default(text: str, default: str = "") -> str:
    """带默认值的输入提示

    AI Bot 不应触发此函数 (Bot 模式所有参数必须通过命令行传入)。
    交互模式下如用户直接回车则使用默认值。

    Args:
        text:   提示文本
        default: 默认值 (如不为空则展示给用户)
    Returns:
        用户输入的值或默认值
    """
    if default:
        return typer.prompt(f"{text} (默认: {default})", default=default)
    return typer.prompt(text)
