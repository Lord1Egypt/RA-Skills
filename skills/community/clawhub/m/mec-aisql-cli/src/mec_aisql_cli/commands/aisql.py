"""AISQL management commands for mec-aisql-cli.

This module is the primary CLI surface for AI-driven SQL lifecycle management on
the MEC (秒针) AISQL platform. It is consumed by both human operators and AI bots;
every command supports a stable ``--json`` mode so an AI agent can parse
structured output without scraping terminal text.

Module layout (command name -> function):
    gen             -> gen_sql           AI 生成 HIVE SQL
    translate       -> translate_sql     SQL -> 自然语言翻译
    create          -> create_task      创建任务记录
    perform         -> perform_task      执行任务并创建工单
    status          -> get_status       查询任务状态 (单次快照)
    watch           -> watch_status      轮询监控任务直到终态
    validate        -> validate_sql      校验 SQL 是否可执行
    agree           -> agree_agreement   签署使用协议
    check-agreement -> check_agreement    检查协议签署状态
    models          -> get_models        获取可用 AI 模型
    retry           -> retry_task        重试失败任务
    stop            -> stop_task         停止执行中任务
    list            -> list_tasks        分页查询任务列表
    detail          -> detail_task       查看任务完整详情
    sql             -> view_sql          查看任务 SQL 内容
    error           -> view_error        查看任务错误日志

Common conventions across all commands:
    - ``--url``/``-u``: override API base URL (default reads config)
    - ``--json``: emit raw JSON for AI consumption (stable, parseable structure)
    - Exit code 0 = success, 1 = failure (unless documented otherwise per command)
    - API client is built via ``_build_client`` which reads ``~/.minglue/tokens.json``
      for Bearer token; HTTP 401 responses trigger automatic token refresh.

Typical AI-driven lifecycle:
    1. ``check-agreement`` -> ``agree``        (首次使用)
    2. ``models``                               (查询可用模型)
    3. ``gen``                                  (生成 SQL)
    4. ``translate`` + ``validate``              (核对语义 + 校验合法性)
    5. ``create``                               (登记任务)
    6. ``perform`` -> ``watch``                 (执行 + 等待结果)
    7. ``retry`` / ``stop`` / ``error``         (异常处理)
"""
import json
from pathlib import Path
import time
from typing import Optional

import typer

from mec_aisql_cli.api_client import AisqlApiClient
from mec_aisql_cli.config import Config
from mec_aisql_cli.datetime_utils import validate_datetimefw
from mec_aisql_cli.output import print_result, confirm, prompt_with_default

app = typer.Typer(help="AISQL 管理命令")


# Allowed values for the --datafrom parameter of `gen` / `create`.
# These are MEC 内部数据源标识; AI 必须严格从此列表取值, 不要自行编造。
DATA_FROM_OPTIONS = ["ADM", "OTT-OM", "OTT-PMO", "TVM", "BDID-MZID", "BDID-IPV6"]


def _build_client(base_url: str = "", debug: bool = False) -> AisqlApiClient:
    """构建 AISQL API 客户端实例 (内部辅助函数, 非 CLI 命令)。

    从用户配置读取 ``base_url`` / ``timeout`` / ``max_retries``; 若 ``base_url``
    显式传入则覆盖配置。Bearer token 由 :class:`AisqlApiClient` 自行从
    ``~/.minglue/tokens.json`` 加载, 401 时自动刷新。

    Args:
        base_url: 显式 API base URL; 空字符串则读 config。
        debug: 是否开启调试日志。

    Returns:
        配置好的 :class:`AisqlApiClient` 实例。
    """
    config = Config()
    url = base_url or config.get("base_url", "https://mec.miaozhen.com/taskmng")
    timeout = config.get("timeout", 120)
    retries = config.get("max_retries", 2)
    return AisqlApiClient(base_url=url, debug=debug, timeout=timeout, max_retries=retries)


@app.command("gen")
def gen_sql(
    comment: str = typer.Option(..., "--comment", "-c", help="需求描述"),
    models: str = typer.Option("", "--model", "-m", help="AI模型"),
    client: str = typer.Option("", "--client", help="客户名称"),
    brand: str = typer.Option("", "--brand", help="品牌名称"),
    datafrom: str = typer.Option("", "--datafrom", help="数据来源"),
    contype: str = typer.Option("", "--contype", help="分析类型"),
    datetimefw: str = typer.Option("", "--datetimefw", help="时间范围, 格式 '2026-03-01/2026-03-31' 或 '20260301-20260331'"),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON"),
    base_url: str = typer.Option("", "--url", "-u", help="API base URL"),
    debug: bool = typer.Option(False, "--debug", help="Enable debug mode"),
):
    """AI 生成 HIVE SQL 语句。

    Purpose:
        根据自然语言需求描述, 调用 AI 生成符合 HIVE SQL 语法规范的查询语句,
        并自动注入客户/品牌/数据来源/时间范围/分析类型等业务上下文。

    AI Usage:
        - 用户用自然语言描述数据查询需求, 需要生成对应 SQL 时使用
        - 在执行 ``create`` 创建任务前, 先用本命令获取候选 SQL
        - 当用户已提供完整 SQL 时不要调用本命令, 可直接 ``validate`` 或 ``create``
        - 缺失 ``--client`` / ``--brand`` / ``--datetimefw`` / ``--datafrom`` 会进入
          交互式提示, AI 调用时应一次性传齐这些参数避免阻塞

    Parameters:
        --comment, -c (str, 必填): 需求描述, 例如 "统计某品牌各渠道曝光量"
        --model, -m (str, 可选): AI 模型标识; 默认读 config.model, 再缺省为
            ``mlamp/deepseek-v4-flash``。可先用 ``models`` 命令列出可用模型。
        --client (str, 可选): 客户名称, 缺失会交互式提示
        --brand (str, 可选): 品牌名称, 缺失会交互式提示
        --datafrom (str, 可选): 数据来源, 必须取自 DATA_FROM_OPTIONS
            (ADM / OTT-OM / OTT-PMO / TVM / BDID-MZID / BDID-IPV6); 缺失会交互式选择
        --contype (str, 可选): 分析类型
        --datetimefw (str, 可选): 时间范围, 灵活格式如 "2026-03-01/2026-03-31" 或 "20260301-20260331";
            缺失会交互式提示
        --json (bool, 可选): 输出原始 JSON, 默认 False
        --url, -u (str, 可选): API base URL, 默认读 config
        --debug (bool, 可选): 启用调试日志

    Output:
        文本模式: 打印标题 + 生成的 SQL + token 用量统计
        JSON 模式结构::

            {
              "success": bool,
              "message": str,
              "data": {
                "sql": str,                  // 生成的 HIVE SQL 语句
                "prompt_tokens": int,         // 输入 token 数 (可能缺失)
                "completion_tokens": int,     // 输出 token 数 (可能缺失)
                "total_tokens": int           // 合计 token 数 (可能缺失)
              }
            }

    Exit codes:
        0: 成功生成 SQL
        1: 生成失败 (鉴权失败 / 模型错误 / 网络错误 / 必填项缺失)

    Examples:
        mec-aisql-cli aisql gen -c "统计某品牌各渠道曝光量" \\
            --client 客户A --brand 品牌B --datafrom ADM \\
            --datetimefw 2026-03-01/2026-03-31

        mec-aisql-cli aisql gen -c "..." --model mlamp/deepseek-v4-flash --json
    """
    cfg = Config()
    # 参数回退顺序: 命令行 > config 文件 > 默认值/交互提示
    models = models or cfg.get("model", "mlamp/deepseek-v4-flash")
    client = client or cfg.get("client", "")
    brand = brand or cfg.get("brand", "")
    datafrom = datafrom or cfg.get("datafrom", "")
    datetimefw = datetimefw or cfg.get("datetimefw", "")
    contype = contype or cfg.get("contype", "")

    client_api = _build_client(base_url, debug)

    # 必填业务上下文缺失时进入交互式提示 (AI 应避免走到这里, 提前传齐参数)
    if not client:
        client = typer.prompt("请输入客户名称")
    if not brand:
        brand = typer.prompt("请输入品牌名称")
    if not datetimefw:
        datetimefw = typer.prompt("请输入日期区间 (格式: 2026-03-01/2026-03-31 或 20260301-20260331)")
    # 校验 datetimefw 格式 (前端要求 ["YYYY-MM-DD","YYYY-MM-DD"] 数组)
    dt_ok, dt_result = validate_datetimefw(datetimefw)
    if not dt_ok:
        typer.echo(f"[FAIL] datetimefw 格式不合法: {dt_result}")
        typer.echo("示例: --datetimefw '2026-03-01/2026-03-31' 或 '20260301-20260331'")
        raise typer.Exit(code=1)
    if not datafrom:
        # 数据来源使用编号菜单选择, 避免用户输入非法值
        typer.echo("请选择数据来源:")
        for i, opt in enumerate(DATA_FROM_OPTIONS, 1):
            typer.echo(f"  {i}. {opt}")
        while True:
            choice = typer.prompt(f"请输入序号 (1-{len(DATA_FROM_OPTIONS)})")
            if choice.isdigit() and 1 <= int(choice) <= len(DATA_FROM_OPTIONS):
                datafrom = DATA_FROM_OPTIONS[int(choice) - 1]
                break
            typer.echo("请输入有效的序号")

    # 将业务上下文拼装为 AI 提示语, 明确要求 HIVE SQL 语法
    params_parts = []
    if client:
        params_parts.append(f"客户为「{client}」")
    if brand:
        params_parts.append(f"品牌为「{brand}」")
    if datafrom:
        params_parts.append(f"数据来源为「{datafrom}」")
    if datetimefw:
        date_parts = datetimefw.split("-")
        if len(date_parts) == 2:
            params_parts.append(f"统计日期范围为「{date_parts[0]}」至「{date_parts[1]}」")
        else:
            params_parts.append(f"统计日期为「{datetimefw}」")
    if contype:
        params_parts.append(f"分析类型为「{contype}」")

    params_text = "，".join(params_parts) if params_parts else ""
    if params_text:
        full_comment = f"{comment}。{params_text}。请基于上述业务场景和约束条件，生成符合 HIVE SQL 语法规范的查询语句。"
    else:
        full_comment = f"{comment}。请生成符合 HIVE SQL 语法规范的查询语句。"

    data = {
        "comment": full_comment,
        "models": models,
        "client": client,
        "brand": brand,
        "datafrom": datafrom,
        "datetimefw": datetimefw,
    }
    if contype:
        data["contype"] = contype

    result = client_api.gen_aisql(data)
    print_result(result, title="AI SQL 生成", as_json=json_output)


@app.command("translate")
def translate_sql(
    sql: str = typer.Option(..., "--sql", "-s", help="SQL语句"),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON"),
    base_url: str = typer.Option("", "--url", "-u", help="API base URL"),
):
    """将 SQL 语句翻译成自然语言说明。

    Purpose:
        把 HIVE SQL 反向解析为业务可读的中文描述, 便于非技术用户理解查询意图。

    AI Usage:
        - 用户拿到一段 SQL 想知道它在做什么时调用
        - 在 ``gen`` 生成 SQL 后用于向用户解释生成结果的语义
        - 用于核对 AI 生成的 SQL 是否符合用户原始需求

    Parameters:
        --sql, -s (str, 必填): 待翻译的 SQL 语句
        --json (bool, 可选): 输出原始 JSON, 默认 False
        --url, -u (str, 可选): API base URL, 默认读 config

    Output:
        文本模式: 打印翻译后的中文说明
        JSON 模式结构::

            {
              "success": bool,
              "message": str,
              "data": {
                "translation": str   // 翻译后的自然语言描述
              }
            }
        (data 字段实际结构以 API 返回为准)

    Exit codes:
        0: 翻译成功
        1: 翻译失败 (鉴权失败 / SQL 语法错误 / 网络错误)

    Examples:
        mec-aisql-cli aisql translate -s "SELECT count(*) FROM adm_log WHERE dt='20240101'"
        mec-aisql-cli aisql translate --sql "..." --json
    """
    client = _build_client(base_url)
    result = client.translate_sql({"sql": sql})
    print_result(result, title="SQL 翻译", as_json=json_output)


@app.command("create")
def create_task(
    ai_task_name: str = typer.Option(..., "--task-name", "-t", help="任务名称"),
    clientid: str = typer.Option("", "--clientid", help="客户ID"),
    client: str = typer.Option(..., "--client", help="客户名称"),
    brandid: str = typer.Option("", "--brandid", help="品牌ID"),
    brand: str = typer.Option(..., "--brand", help="品牌名称"),
    datafrom: str = typer.Option(..., "--datafrom", help="数据来源"),
    contype: str = typer.Option(..., "--contype", help="分析类型"),
    datetimefw: str = typer.Option(..., "--datetimefw", help="时间范围, 格式 '2026-03-01/2026-03-31' 或 '20260301-20260331'"),
    comment: str = typer.Option(..., "--comment", help="需求描述"),
    sql: str = typer.Option(..., "--sql", help="SQL语句"),
    sccontent: Optional[str] = typer.Option(None, "--sccontent", help="自然语言描述"),
    models: Optional[str] = typer.Option(None, "--model", help="AI模型"),
    dtsaccount: Optional[str] = typer.Option(None, "--dtsaccount", help="DTS账号"),
    dtspassword: Optional[str] = typer.Option(None, "--dtspassword", help="DTS密码"),
    crow_data_path: Optional[str] = typer.Option(None, "--crow-data-path", help="人群包路径"),
    dts_path: Optional[str] = typer.Option(None, "--dts-path", help="DTS路径"),
    sale_id: Optional[str] = typer.Option(None, "--sale-id", help="销售ID"),
    excuter: Optional[str] = typer.Option(None, "--excuter", help="执行者"),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON"),
    base_url: str = typer.Option("", "--url", "-u", help="API base URL"),
):
    """创建 AISQL 任务记录 (不执行)。

    Purpose:
        将任务元数据与 SQL 内容提交到平台保存, 生成任务 ID, 但不会立即执行。
        执行需要再调用 ``perform`` 创建工单触发。

    AI Usage:
        - 用户确认 SQL 后, 将任务正式登记到平台时使用
        - 保存任务以便后续 ``perform`` / ``watch`` / ``retry`` 流程
        - 不要在用户尚未确认 SQL 时调用, 应先 ``gen`` + ``translate`` + ``validate``
        - 返回的任务 ID 是后续所有命令 (--id 参数) 的入口

    Parameters:
        --task-name, -t (str, 必填): 任务名称
        --clientid (str, 可选): 客户ID
        --client (str, 必填): 客户名称
        --brandid (str, 可选): 品牌ID
        --brand (str, 必填): 品牌名称
        --datafrom (str, 必填): 数据来源, 取值见 DATA_FROM_OPTIONS
        --contype (str, 必填): 分析类型
        --datetimefw (str, 必填): 时间范围, 灵活格式如 "2026-03-01/2026-03-31" 或 "20260301-20260331"
        --comment (str, 必填): 需求描述
        --sql (str, 必填): SQL 语句 (通常来自 ``gen`` 的输出)
        --sccontent (str, 可选): 自然语言描述
        --model (str, 可选): AI 模型标识
        --dtsaccount (str, 可选): DTS 账号 (执行 DTS 导出时需要)
        --dtspassword (str, 可选): DTS 密码
        --crow-data-path (str, 可选): 人群包路径
        --dts-path (str, 可选): DTS 路径
        --sale-id (str, 可选): 销售 ID
        --excuter (str, 可选): 执行者
        --json (bool, 可选): 输出原始 JSON, 默认 False
        --url, -u (str, 可选): API base URL

    Output:
        文本模式: 打印任务创建结果 (含新任务 ID)
        JSON 模式结构::

            {
              "success": bool,
              "message": str,
              "data": {
                "id": int,            // 新建任务 ID (后续 perform/watch 需要)
                "aiTaskName": str,
                ...
              }
            }

    Exit codes:
        0: 任务创建成功
        1: 创建失败 (鉴权失败 / 字段非法 / SQL 不合法)

    Examples:
        mec-aisql-cli aisql create -t "Q1曝光统计" --client 客户A --brand 品牌B \\
            --datafrom ADM --contype 曝光 --datetimefw 2026-03-01/2026-03-31 \\
            --comment "..." --sql "SELECT ..."

        mec-aisql-cli aisql create ... --json
    """
    client_api = _build_client(base_url)

    # 构造 payload: 必填字段直接放入, 可选项仅当非空时才加入 (避免覆盖服务端默认值)
    data = {
        "aiTaskName": ai_task_name,
        "clientid": clientid,
        "client": client,
        "brandid": brandid,
        "brand": brand,
        "datafrom": datafrom,
        "contype": contype,
        "datetimefw": datetimefw,
        "comment": comment,
        "sql": sql,
    }
    if sccontent:
        data["sccontent"] = sccontent
    if models:
        data["models"] = models
    if dtsaccount:
        data["dtsaccount"] = dtsaccount
    if dtspassword:
        data["dtspassword"] = dtspassword
    if crow_data_path:
        data["CrowDataPath"] = crow_data_path
    if dts_path:
        data["DtsPath"] = dts_path
    if sale_id:
        data["SaleId"] = sale_id
    if excuter:
        data["Excuter"] = excuter

    result = client_api.create_aisql_task(data)
    print_result(result, title="创建任务", as_json=json_output)


@app.command("perform")
def perform_task(
    id: int = typer.Option(..., "--id", help="任务ID"),
    task_id: str = typer.Option("1078", "--task-id", help="工单模板ID"),
    yes: bool = typer.Option(False, "--yes", "-y", help="跳过确认"),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON"),
    base_url: str = typer.Option("", "--url", "-u", help="API base URL"),
):
    """执行 AISQL 任务并创建工单。

    Purpose:
        触发已创建的任务实际执行: 提交 SQL 到 DMS、生成工单、开始出数流程。
        执行后任务进入异步处理状态, 需要用 ``status`` 或 ``watch`` 跟踪结果。

    AI Usage:
        - ``create`` 创建任务后, 用户确认要执行时调用
        - 默认会交互式确认, AI 调用应传 ``--yes`` 跳过确认
        - 执行后立即调用 ``watch`` 跟踪直到完成
        - 任务必须处于可执行状态 (草稿/失败重试), 已在执行的任务无法再次 perform

    Parameters:
        --id (int, 必填): 任务 ID (来自 ``create`` 的返回)
        --task-id (str, 可选): 工单模板 ID, 默认 "1078"
        --yes, -y (bool, 可选): 跳过交互式确认, AI 必备
        --json (bool, 可选): 输出原始 JSON, 默认 False
        --url, -u (str, 可选): API base URL

    Output:
        文本模式: 打印执行结果 (工单 ID / DMS 任务 ID 等)
        JSON 模式结构::

            {
              "success": bool,
              "message": str,
              "data": {
                "orderid": str,     // 工单号
                "sqldmsid": str,     // DMS 查询 ID
                "dmstaskid": str,    // DMS 任务 ID
                ...
              }
            }

    Exit codes:
        0: 工单创建成功
        1: 执行失败 (鉴权失败 / 任务不存在 / 任务状态不允许执行)
        (用户取消时不返回退出码, 直接 return)

    Examples:
        mec-aisql-cli aisql perform --id 123 --yes
        mec-aisql-cli aisql perform --id 123 --task-id 2000 --json
    """
    # 非批量、非 JSON 模式时交互式确认, 避免误触
    if not yes and not json_output:
        if not confirm(f"确认执行任务 ID={id} 并创建工单？"):
            typer.echo("已取消。")
            return

    client = _build_client(base_url)
    result = client.perform_aisql_task({"id": id, "taskId": task_id})
    print_result(result, title="执行任务", as_json=json_output)


@app.command("status")
def get_status(
    id: int = typer.Option(..., "--id", help="任务ID"),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON"),
    base_url: str = typer.Option("", "--url", "-u", help="API base URL"),
):
    """查询 AISQL 任务当前状态 (单次快照)。

    Purpose:
        一次性获取任务当前状态、进度、终态标志。如需持续监控请用 ``watch``。

    AI Usage:
        - 用户询问 "任务 X 怎么样了" 时调用
        - 在 ``perform`` 之后做一次状态检查
        - 需要持续轮询时改用 ``watch``, 而非循环调用本命令
        - 终态判定依据 ``data.isTerminal``, 不要用 ``agentStatus`` 字符串硬判断

    Parameters:
        --id (int, 必填): 任务 ID
        --json (bool, 可选): 输出原始 JSON, 默认 False
        --url, -u (str, 可选): API base URL

    Output:
        文本模式: 打印状态 / 进度 / 消息 / 工单 / 结果表 / 错误 / 重试次数
        JSON 模式结构::

            {
              "success": bool,
              "message": str,
              "data": {
                "id": int,
                "aiTaskName": str,
                "agentStatus": str,           // Pending/Running/Succeeded/Failed/Stopped/NeedHumanReview
                "status": str,                // 状态描述
                "progress": int,              // 0-100
                "isTerminal": bool,           // 是否终态
                "canRetry": bool,
                "canStop": bool,
                "retryCount": int,
                "maxRetryCount": int,
                "orderid": str,
                "tableName": str,            // 成功后的结果表名
                "fileRouter": str,           // 结果文件路径
                "sqlcontent": str,
                "lastErrorCode": str,
                "lastErrorMessage": str,
                "nextPollAfterSeconds": int  // 建议下次轮询间隔
              }
            }

    Exit codes:
        0: 查询成功 (无论任务本身是否成功)
        1: 查询失败 (鉴权失败 / 任务不存在 / 网络错误)

    Examples:
        mec-aisql-cli aisql status --id 123
        mec-aisql-cli aisql status --id 123 --json
    """
    client = _build_client(base_url)
    result = client.get_aisql_agent_status({"id": id})
    print_result(result, title="任务状态", as_json=json_output)


@app.command("watch")
def watch_status(
    id: int = typer.Option(..., "--id", help="任务ID"),
    interval: Optional[int] = typer.Option(None, "--interval", help="轮询间隔秒数"),
    timeout: Optional[int] = typer.Option(None, "--timeout", help="最长等待秒数"),
    json_output: bool = typer.Option(False, "--json", help="Output final JSON"),
    base_url: str = typer.Option("", "--url", "-u", help="API base URL"),
):
    """轮询监控 AISQL 任务状态直到进入终态。

    Purpose:
        周期性查询任务状态, 直到任务成功 / 失败 / 停止 / 人工复核等终态, 然后退出。
        适用于 "提交后等结果" 的长流程。

    AI Usage:
        - ``perform`` 之后等待任务跑完时调用
        - 需要阻塞式等待结果时使用, 单次状态查询请用 ``status``
        - 默认按 API 返回的 ``nextPollAfterSeconds`` 轮询; 可用 ``--interval`` 固定间隔
        - ``--json`` 模式仅在终态输出一次最终 JSON, 便于 AI 一次性解析
        - 命令会阻塞直到终态或超时, AI 调用时应设 ``--timeout`` 避免无限等待

    Parameters:
        --id (int, 必填): 任务 ID
        --interval (int, 可选): 固定轮询间隔秒数; 缺省则用 API 建议值, 再缺省 30s
        --timeout (int, 可选): 最长等待秒数, 超时即退出 (退出码 124)
        --json (bool, 可选): 仅在终态输出最终 JSON, 默认 False (持续打印进度)
        --url, -u (str, 可选): API base URL

    Output:
        文本模式: 每轮打印 ``[时间] 状态 进度% 消息``, 终态时打印结果表/文件路径
        JSON 模式结构 (仅终态输出一次)::

            {
              "success": bool,
              "message": str,
              "data": { ... 同 ``status`` 命令 ... }
            }
        超时输出::

            {
              "success": false,
              "message": "等待超时",
              "error": {"code": "AISQL_WATCH_TIMEOUT", "message": "等待任务完成超时"}
            }

    Exit codes:
        0: 任务成功 (agentStatus == "Succeeded")
        1: 任务失败 / 查询失败 / 未知终态错误
        2: 任务被停止 (agentStatus == "Stopped")
        3: 任务需要人工复核 (agentStatus == "NeedHumanReview")
        124: 等待超时 (--timeout 触发)

    Examples:
        mec-aisql-cli aisql watch --id 123
        mec-aisql-cli aisql watch --id 123 --interval 10 --timeout 3600
        mec-aisql-cli aisql watch --id 123 --json
    """
    client = _build_client(base_url)
    started_at = time.time()

    while True:
        # 超时检查优先于本次轮询, 避免无限等待
        if timeout and (time.time() - started_at) >= timeout:
            output = {
                "success": False,
                "message": "等待超时",
                "error": {"code": "AISQL_WATCH_TIMEOUT", "message": "等待任务完成超时"},
            }
            print(json.dumps(output, ensure_ascii=False, indent=2))
            raise typer.Exit(code=124)

        result = client.get_aisql_agent_status({"id": id})
        # API 调用本身失败 (非任务失败) 时直接退出码 1
        if not (result.get("success") or result.get("Success")):
            print_result(result, failure_exit=1)
            raise typer.Exit(code=1)

        data = result.get("data", {})
        status = data.get("agentStatus", "-")
        progress = data.get("progress", 0)
        message = data.get("status", "")
        is_terminal = data.get("isTerminal", False)

        # 文本模式实时输出进度行
        if not json_output:
            typer.echo(
                f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] "
                f"{status} {progress}% {message}"
            )

        if is_terminal:
            # JSON 模式只在终态输出一次完整结果
            if json_output:
                print_result(result, as_json=True, exit_on_fail=False)
            # 终态分支: 按 agentStatus 映射不同退出码
            if status == "Succeeded":
                if not json_output:
                    typer.echo(f"  结果表: {data.get('tableName', '-')}")
                    if data.get("fileRouter"):
                        typer.echo(f"  文件路径: {data['fileRouter']}")
                raise typer.Exit(code=0)
            elif status == "NeedHumanReview":
                raise typer.Exit(code=3)
            elif status == "Stopped":
                raise typer.Exit(code=2)
            else:
                error_msg = data.get("lastErrorMessage", status)
                typer.echo(f"  [FAIL] {error_msg}")
                raise typer.Exit(code=1)

        # 优先使用用户指定的 interval, 其次 API 建议, 最后默认 30s
        sleep_seconds = interval or data.get("nextPollAfterSeconds") or 30
        time.sleep(max(1, int(sleep_seconds)))


@app.command("validate")
def validate_sql(
    id: Optional[int] = typer.Option(None, "--id", help="任务ID; 传入后校验已保存的 SQL"),
    sql: Optional[str] = typer.Option(None, "--sql", help="SQL语句"),
    sql_file: Optional[Path] = typer.Option(None, "--sql-file", help="SQL文件路径"),
    datafrom: Optional[str] = typer.Option(None, "--datafrom", help="数据来源"),
    datetimefw: Optional[str] = typer.Option(None, "--datetimefw", help="时间范围"),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON"),
    base_url: str = typer.Option("", "--url", "-u", help="API base URL"),
):
    """校验 SQL 语句是否可执行。

    Purpose:
        在执行前对 SQL 做静态检查, 发现语法错误 / 风险表 / 不支持的语句等。
        支持 3 种 SQL 输入方式: ``--id`` (校验已保存任务的 SQL) / ``--sql`` / ``--sql-file``。

    AI Usage:
        - ``gen`` 生成 SQL 后, ``create`` 之前用本命令确认 SQL 合法
        - 用户粘贴一段 SQL 想知道是否能跑时使用
        - ``--id`` 传入已存在任务 ID 时校验该任务保存的 SQL
        - 注意: 校验通过 (退出码 0) 不等于 SQL 一定可执行, 需读 data.valid / data.executable

    Parameters:
        --id (int, 可选): 任务 ID; 传入后校验该任务已保存的 SQL
        --sql (str, 可选): 直接传入 SQL 语句
        --sql-file (Path, 可选): 从文件读取 SQL
        --datafrom (str, 可选): 数据来源, 参与校验上下文
        --datetimefw (str, 可选): 时间范围, 参与校验上下文
        --json (bool, 可选): 输出原始 JSON, 默认 False
        --url, -u (str, 可选): API base URL
        注意: ``--id`` / ``--sql`` / ``--sql-file`` 三者至少传一个, 否则退出码 1

    Output:
        文本模式: 打印 valid / executable / riskLevel / errors / warnings
        JSON 模式结构::

            {
              "success": bool,
              "message": str,
              "data": {
                "valid": bool,              // 语法是否合法
                "executable": bool,         // 是否可执行
                "riskLevel": str,           // 风险等级
                "errors": [{"code": str, "message": str}, ...],
                "warnings": [{"code": str, "message": str}, ...]
              }
            }

    Exit codes:
        0: 校验请求成功 (不代表 SQL 一定合法, 需看 data.valid)
        1: 校验请求失败 / 未提供 SQL 来源 / SQL 文件不存在

    Examples:
        mec-aisql-cli aisql validate --sql "SELECT count(*) FROM adm_log WHERE dt='20240101'"
        mec-aisql-cli aisql validate --sql-file ./query.sql --json
        mec-aisql-cli aisql validate --id 123
    """
    # 三种 SQL 来源至少要有一个
    if id is None and not sql and sql_file is None:
        typer.echo("必须提供 --id、--sql 或 --sql-file 中的一个。")
        raise typer.Exit(code=1)

    # --sql-file 优先级高于 --sql, 读取后覆盖 sql 变量
    if sql_file is not None:
        if not sql_file.exists():
            typer.echo(f"SQL file not found: {sql_file}")
            raise typer.Exit(code=1)
        sql = sql_file.read_text(encoding="utf-8")

    client = _build_client(base_url)
    # 仅放入非空字段, 避免覆盖服务端默认行为
    payload = {}
    if id is not None:
        payload["id"] = id
    if sql:
        payload["sql"] = sql
    if datafrom:
        payload["datafrom"] = datafrom
    if datetimefw:
        payload["datetimefw"] = datetimefw

    result = client.validate_aisql(payload)
    print_result(result, title="SQL 校验", as_json=json_output)


@app.command("agree")
def agree_agreement(
    base_url: str = typer.Option("", "--url", "-u", help="API base URL"),
    debug: bool = typer.Option(False, "--debug", help="Enable debug mode"),
):
    """签署 AISQL 使用协议。

    Purpose:
        首次使用 AISQL 服务前需要签署使用协议; 本命令触发签署流程。

    AI Usage:
        - ``check-agreement`` 显示未签署时调用
        - 用户首次使用平台、遇到 "需要先签署协议" 类错误时调用
        - 签署是一次性操作, 已签署后无需重复调用

    Parameters:
        --url, -u (str, 可选): API base URL
        --debug (bool, 可选): 启用调试日志

    Output:
        文本模式: 打印签署结果标题与消息
        JSON 模式: 本命令未提供 ``--json`` 参数, 输出始终为文本

    Exit codes:
        0: 签署成功 / 已签署
        1: 签署失败 (鉴权失败 / 网络错误)

    Examples:
        mec-aisql-cli aisql agree
        mec-aisql-cli aisql agree --debug
    """
    client = _build_client(base_url, debug)
    result = client.sign_aisql_agreement()
    print_result(result, title="签署协议")


@app.command("check-agreement")
def check_agreement(
    base_url: str = typer.Option("", "--url", "-u", help="API base URL"),
    debug: bool = typer.Option(False, "--debug", help="Enable debug mode"),
):
    """检查 AISQL 协议签署状态。

    Purpose:
        查询当前账号是否已签署 AISQL 使用协议, 用于决定是否需要调用 ``agree``。

    AI Usage:
        - 在调用 ``gen`` / ``create`` 前先检查协议状态
        - 用户遇到权限类错误时辅助诊断
        - 返回未签署时提示用户调用 ``agree``

    Parameters:
        --url, -u (str, 可选): API base URL
        --debug (bool, 可选): 启用调试日志

    Output:
        文本模式: 打印协议状态标题与消息
        JSON 模式: 本命令未提供 ``--json`` 参数, 输出始终为文本

    Exit codes:
        0: 查询成功
        1: 查询失败 (鉴权失败 / 网络错误)

    Examples:
        mec-aisql-cli aisql check-agreement
        mec-aisql-cli aisql check-agreement --debug
    """
    client = _build_client(base_url, debug)
    result = client.check_aisql_agreement()
    print_result(result, title="协议状态")


@app.command("models")
def get_models(
    base_url: str = typer.Option("", "--url", "-u", help="API base URL"),
):
    """获取可用 AI 模型列表。

    Purpose:
        列出当前账号可用的 AI 模型, 供 ``gen`` / ``create`` 的 ``--model`` 参数选择。

    AI Usage:
        - 用户问 "有哪些模型可用" 时调用
        - 在 ``gen`` 之前确认可用模型范围
        - 用户想切换模型时提供候选清单

    Parameters:
        --url, -u (str, 可选): API base URL

    Output:
        文本模式: 打印模型列表标题与详情
        JSON 模式: 本命令未提供 ``--json`` 参数, 输出始终为文本

    Exit codes:
        0: 查询成功
        1: 查询失败 (鉴权失败 / 网络错误)

    Examples:
        mec-aisql-cli aisql models
    """
    client = _build_client(base_url)
    result = client.get_aisql_models()
    print_result(result, title="AI 模型列表")


@app.command("retry")
def retry_task(
    id: int = typer.Option(..., "--id", help="任务ID"),
    yes: bool = typer.Option(False, "--yes", "-y", help="跳过确认"),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON"),
    base_url: str = typer.Option("", "--url", "-u", help="API base URL"),
):
    """重试失败的 AISQL 任务。

    Purpose:
        对进入失败终态的任务发起重试, 重新执行 SQL 出数流程。
        受 ``maxRetryCount`` 限制, 超过上限将无法继续重试。

    AI Usage:
        - ``status`` / ``watch`` 显示任务失败时, 如 ``canRetry=true`` 则调用本命令
        - 默认交互式确认, AI 调用应传 ``--yes`` 跳过
        - 重试后应继续 ``watch`` 跟踪新一轮执行
        - 重试次数耗尽时应提示用户检查 SQL 而非继续重试

    Parameters:
        --id (int, 必填): 任务 ID
        --yes, -y (bool, 可选): 跳过交互式确认, AI 必备
        --json (bool, 可选): 输出原始 JSON, 默认 False
        --url, -u (str, 可选): API base URL

    Output:
        文本模式: 打印重试结果标题与消息
        JSON 模式结构::

            {
              "success": bool,
              "message": str,
              "data": { ... 任务最新状态 ... }
            }

    Exit codes:
        0: 重试请求已接受
        1: 重试失败 (任务不存在 / 已达最大重试次数 / 当前状态不可重试)
        (用户取消时不返回退出码, 直接 return)

    Examples:
        mec-aisql-cli aisql retry --id 123 --yes
        mec-aisql-cli aisql retry --id 123 --json
    """
    if not yes and not json_output:
        if not confirm(f"确认重试任务 ID={id}？"):
            typer.echo("已取消。")
            return

    client = _build_client(base_url)
    result = client.retry_aisql_task(id)
    print_result(result, title="重试任务", as_json=json_output)


@app.command("stop")
def stop_task(
    id: int = typer.Option(..., "--id", help="任务ID"),
    yes: bool = typer.Option(False, "--yes", "-y", help="跳过确认"),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON"),
    base_url: str = typer.Option("", "--url", "-u", help="API base URL"),
):
    """停止正在执行的 AISQL 任务。

    Purpose:
        对运行中的任务发起停止, 使任务进入 ``Stopped`` 终态。
        仅在 ``canStop=true`` 时可停止。

    AI Usage:
        - 用户明确要取消某个运行中任务时调用
        - 任务执行时间过长或方向错误时主动停止
        - 默认交互式确认, AI 调用应传 ``--yes`` 跳过
        - 停止是不可逆操作, 调用前应向用户确认

    Parameters:
        --id (int, 必填): 任务 ID
        --yes, -y (bool, 可选): 跳过交互式确认, AI 必备
        --json (bool, 可选): 输出原始 JSON, 默认 False
        --url, -u (str, 可选): API base URL

    Output:
        文本模式: 打印停止结果标题与消息
        JSON 模式结构::

            {
              "success": bool,
              "message": str,
              "data": { ... 任务最新状态 ... }
            }

    Exit codes:
        0: 停止请求已接受
        1: 停止失败 (任务不存在 / 当前状态不可停止 / 网络错误)
        (用户取消时不返回退出码, 直接 return)

    Examples:
        mec-aisql-cli aisql stop --id 123 --yes
        mec-aisql-cli aisql stop --id 123 --json
    """
    if not yes and not json_output:
        if not confirm(f"确认停止任务 ID={id}？"):
            typer.echo("已取消。")
            return

    client = _build_client(base_url)
    result = client.stop_aisql_task(id)
    print_result(result, title="停止任务", as_json=json_output)


# --------------- List / Detail / SQL / Error ---------------

# 任务列表用的 isdosql 状态码 -> 中文描述映射 (与 watch 的 agentStatus 不同体系)
_STATUS_MAP = {
    0: "草稿/待执行",
    1: "执行中",
    2: "结果就绪",
    3: "导出中",
    4: "已完成",
    5: "失败",
}


@app.command("list")
def list_tasks(
    page: int = typer.Option(1, "--page", "-p", help="页码 (默认1)"),
    page_size: int = typer.Option(20, "--page-size", "-s", help="每页条数 (默认20, 最大100)"),
    status: int = typer.Option(0, "--status", help="状态过滤: 0=全部, 1=草稿, 2=执行中, 3=已完成, 4=失败"),
    client: str = typer.Option("", "--client", help="客户名称 (模糊匹配)"),
    brand: str = typer.Option("", "--brand", help="品牌名称 (模糊匹配)"),
    keyword: str = typer.Option("", "--keyword", "-k", help="关键词 (任务名/需求)"),
    date_from: str = typer.Option("", "--date-from", help="创建开始日期 (yyyy-MM-dd)"),
    date_to: str = typer.Option("", "--date-to", help="创建结束日期 (yyyy-MM-dd)"),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON"),
    base_url: str = typer.Option("", "--url", "-u", help="API base URL"),
):
    """分页查询任务列表 (支持筛选)。

    Purpose:
        列出当前账号可见的 AISQL 任务, 支持按状态 / 客户 / 品牌 / 关键词 / 日期筛选。

    AI Usage:
        - 用户问 "我有哪些任务" 时调用
        - 需要按客户/品牌/状态定位某个任务时使用 (拿到 ID 后再 ``detail``)
        - 默认第 1 页 20 条; 翻页用 ``--page``, 加大每页量用 ``--page-size``
        - 注意: --status 这里用的是 isdosql 编码体系, 与 watch 的 agentStatus 不同

    Parameters:
        --page, -p (int, 可选): 页码, 默认 1
        --page-size, -s (int, 可选): 每页条数, 默认 20, 最大 100
        --status (int, 可选): 状态过滤: 0=全部, 1=草稿, 2=执行中, 3=已完成, 4=失败
        --client (str, 可选): 客户名称 (模糊匹配)
        --brand (str, 可选): 品牌名称 (模糊匹配)
        --keyword, -k (str, 可选): 关键词 (匹配任务名 / 需求描述)
        --date-from (str, 可选): 创建开始日期 yyyy-MM-dd
        --date-to (str, 可选): 创建结束日期 yyyy-MM-dd
        --json (bool, 可选): 输出原始 JSON, 默认 False
        --url, -u (str, 可选): API base URL

    Output:
        文本模式: 表格化打印每条任务的 ID/任务名/客户/品牌/状态/工单号/结果表/创建时间
        JSON 模式结构::

            {
              "success": bool,
              "message": str,
              "data": {
                "page": int,
                "pageSize": int,
                "total": int,
                "totalPages": int,
                "items": [
                  {
                    "id": int,
                    "aiTaskName": str,
                    "client": str,
                    "brand": str,
                    "isdosql": int,       // 0/1/2/3/4/5, 见 _STATUS_MAP
                    "orderid": str,
                    "tableName": str,
                    "comment": str,
                    "createTime": str
                  },
                  ...
                ]
              }
            }

    Exit codes:
        0: 查询成功 (即使 items 为空)
        1: 查询失败 (鉴权失败 / 网络错误)

    Examples:
        mec-aisql-cli aisql list
        mec-aisql-cli aisql list --status 2 --page 2
        mec-aisql-cli aisql list --client 客户A --keyword 曝光 --json
    """
    client_api = _build_client(base_url)
    # 只把非空/非默认筛选条件加入查询参数, 避免覆盖服务端默认行为
    params: dict = {"page": page, "pageSize": page_size}
    if status:
        params["status"] = status
    if client:
        params["client"] = client
    if brand:
        params["brand"] = brand
    if keyword:
        params["keyword"] = keyword
    if date_from:
        params["dateFrom"] = date_from
    if date_to:
        params["dateTo"] = date_to

    result = client_api.list_aisql_tasks(params)
    success = result.get("success") or result.get("Success")
    data = result.get("data", {}) if success else {}

    if json_output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        raise typer.Exit(code=0 if success else 1)

    if not success:
        print_result(result, title="任务列表", as_json=False)
        return

    items = data.get("items", [])
    total = data.get("total", 0)
    total_pages = data.get("totalPages", 0)

    typer.echo(f"\n{'=' * 80}")
    typer.echo(f"  任务列表 (第 {data.get('page', 1)}/{total_pages} 页, 共 {total} 条)")
    typer.echo(f"{'=' * 80}")

    if not items:
        typer.echo("  没有找到匹配的任务。")
        return

    # 逐条打印任务概要, isdosql 状态码翻译为中文
    for item in items:
        isdosql = item.get("isdosql", 0)
        status_text = _STATUS_MAP.get(isdosql, str(isdosql))
        task_name = item.get("aiTaskName") or item.get("comment", "")[:30]
        create_time = (item.get("createTime") or "")[:19].replace("T", " ")
        typer.echo(f"\n  ID: {item.get('id')}")
        typer.echo(f"  任务名: {task_name}")
        typer.echo(f"  客户:   {item.get('client', '-')}")
        typer.echo(f"  品牌:   {item.get('brand', '-')}")
        typer.echo(f"  状态:   {status_text}")
        if item.get("orderid"):
            typer.echo(f"  工单号: {item['orderid']}")
        if item.get("tableName"):
            typer.echo(f"  结果表: {item['tableName']}")
        typer.echo(f"  创建:   {create_time}")


@app.command("detail")
def detail_task(
    id: int = typer.Option(..., "--id", help="任务ID"),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON"),
    base_url: str = typer.Option("", "--url", "-u", help="API base URL"),
):
    """查看任务完整详情 (全字段)。

    Purpose:
        展示任务所有关键字段, 包括状态/进度/工单/DMS/结果表/SQL/错误/重试等。
        比 ``status`` 输出更详细, 适合排查问题或对账。

    AI Usage:
        - 用户问 "任务 X 的详细信息" 时调用
        - 排查任务失败原因时配合 ``error`` 一起看
        - 需要拿到完整 SQL 内容时可改用 ``sql`` 命令 (本命令 SQL 截断到 500 字符)
        - 复用 agent status 接口, 与 ``status`` / ``error`` / ``sql`` 同源

    Parameters:
        --id (int, 必填): 任务 ID
        --json (bool, 可选): 输出原始 JSON, 默认 False
        --url, -u (str, 可选): API base URL

    Output:
        文本模式: 按 ``label: value`` 行打印全部字段 (空值字段不显示,
            长字段截断到 120 字符)
        JSON 模式结构 (与 ``status`` 一致, 完整 ``data`` 对象)::

            {
              "success": bool,
              "message": str,
              "data": {
                "id": int, "aiTaskId": str, "aiTaskName": str,
                "agentStatus": str, "status": str, "progress": int,
                "isTerminal": bool, "canRetry": bool, "canStop": bool,
                "retryCount": int, "maxRetryCount": int,
                "orderid": str, "sqldmsid": str, "dmstaskid": str, "dmscxtaskid": str,
                "tableName": str, "fileRouter": str, "sqlcontent": str,
                "createTime": str, "orderdate": str, "sqlcondate": str, "dmstasktime": str,
                "lastErrorCode": str, "lastErrorMessage": str,
                "nextPollAfterSeconds": int
              }
            }

    Exit codes:
        0: 查询成功
        1: 查询失败 (鉴权失败 / 任务不存在 / 网络错误)

    Examples:
        mec-aisql-cli aisql detail --id 123
        mec-aisql-cli aisql detail --id 123 --json
    """
    client = _build_client(base_url)
    result = client.get_aisql_agent_status({"id": id})
    success = result.get("success") or result.get("Success")
    data = result.get("data", {}) if success else {}

    if json_output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        raise typer.Exit(code=0 if success else 1)

    if not success:
        print_result(result, title="任务详情", as_json=False)
        return

    typer.echo(f"\n{'=' * 60}")
    typer.echo(f"  任务详情 (ID: {id})")
    typer.echo(f"{'=' * 60}")

    # 字段名 -> API 字段的有序展示列表, 便于人工阅读
    rows = [
        ("任务ID", data.get("id", "")),
        ("AI任务ID", data.get("aiTaskId", "")),
        ("任务名称", data.get("aiTaskName", "")),
        ("Agent状态", data.get("agentStatus", "")),
        ("状态描述", data.get("status", "")),
        ("进度", f"{data.get('progress', 0)}%"),
        ("是否终态", str(data.get("isTerminal", False))),
        ("可重试", str(data.get("canRetry", False))),
        ("可停止", str(data.get("canStop", False))),
        ("重试次数", f"{data.get('retryCount', 0)}/{data.get('maxRetryCount', 2)}"),
        ("工单ID", data.get("orderid", "")),
        ("DMS查询ID", data.get("sqldmsid", "")),
        ("DMS任务ID", data.get("dmstaskid", "")),
        ("DMS导出ID", data.get("dmscxtaskid", "")),
        ("结果表名", data.get("tableName", "")),
        ("结果文件", data.get("fileRouter", "")),
        ("SQL内容", (data.get("sqlcontent", "") or "")[:500]),
        ("创建时间", str(data.get("createTime", ""))[:19].replace("T", " ")),
        ("工单时间", str(data.get("orderdate", ""))[:19].replace("T", " ")),
        ("执行时间", str(data.get("sqlcondate", ""))[:19].replace("T", " ")),
        ("出数时间", str(data.get("dmstasktime", ""))[:19].replace("T", " ")),
        ("最后错误码", data.get("lastErrorCode", "")),
        ("最后错误信息", data.get("lastErrorMessage", "")),
        ("下次轮询", f"{data.get('nextPollAfterSeconds', 30)}秒后"),
    ]
    # 仅展示非空字段; 过长字段截断到 120 字符
    for label, value in rows:
        if value and value != "None" and value != "":
            display = str(value)
            if len(display) > 120:
                display = display[:120] + "..."
            typer.echo(f"  {label:12s}: {display}")


@app.command("sql")
def view_sql(
    id: int = typer.Option(..., "--id", help="任务ID"),
    save: str = typer.Option("", "--save", help="保存到文件路径"),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON"),
    base_url: str = typer.Option("", "--url", "-u", help="API base URL"),
):
    """查看任务的 SQL 内容。

    Purpose:
        取出任务保存的完整 SQL 语句, 可保存到文件或直接打印。
        与 ``detail`` 不同, 本命令只输出 SQL 本身, 不附带其他字段。

    AI Usage:
        - 用户问 "任务 X 的 SQL 是什么" 时调用
        - 需要把 SQL 保存到本地文件做版本管理时用 ``--save``
        - ``detail`` 中 SQL 被截断到 500 字符, 本命令返回完整 SQL
        - 复用 agent status 接口, 仅提取 sqlcontent 字段

    Parameters:
        --id (int, 必填): 任务 ID
        --save (str, 可选): 保存到该路径, UTF-8 编码; 不传则打印到终端
        --json (bool, 可选): 输出原始 JSON, 默认 False
        --url, -u (str, 可选): API base URL

    Output:
        文本模式: 打印 SQL 完整内容
        JSON 模式结构 (本命令自定义, 非原始 API 响应)::

            {
              "success": true,
              "id": int,
              "sql": str   // 完整 SQL 内容
            }

    Exit codes:
        0: 查询成功 / SQL 已保存
        1: 查询失败 (鉴权失败 / 任务不存在)
        (任务无 SQL 内容时不返回退出码, 打印提示后 return)

    Examples:
        mec-aisql-cli aisql sql --id 123
        mec-aisql-cli aisql sql --id 123 --save ./task_123.sql
        mec-aisql-cli aisql sql --id 123 --json
    """
    client = _build_client(base_url)
    # 复用 agent status 接口, 仅提取 sqlcontent 字段
    result = client.get_aisql_agent_status({"id": id})
    success = result.get("success") or result.get("Success")
    data = result.get("data", {}) if success else {}

    if not success:
        print_result(result, title="SQL 查看", as_json=False)
        return

    sql_content = data.get("sqlcontent", "") or ""
    if not sql_content:
        typer.echo("该任务暂无 SQL 内容。")
        return

    if json_output:
        # JSON 模式自定义输出结构, 便于 AI 直接取 sql 字段
        print(json.dumps({"success": True, "id": id, "sql": sql_content}, ensure_ascii=False, indent=2))
        raise typer.Exit(code=0)

    if save:
        from pathlib import Path
        Path(save).write_text(sql_content, encoding="utf-8")
        typer.echo(f"SQL 已保存到: {save}")
    else:
        typer.echo(f"\n{'=' * 60}")
        typer.echo(f"  SQL 内容 (任务 ID: {id})")
        typer.echo(f"{'=' * 60}")
        typer.echo(sql_content)


@app.command("error")
def view_error(
    id: int = typer.Option(..., "--id", help="任务ID"),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON"),
    base_url: str = typer.Option("", "--url", "-u", help="API base URL"),
):
    """查看任务的错误日志。

    Purpose:
        提取并集中展示任务的错误信息: 错误码、错误消息、执行 SQL、重试次数等,
        便于排查任务失败原因。

    AI Usage:
        - ``status`` / ``watch`` 显示任务失败时调用
        - 用户问 "任务 X 为什么失败了" 时调用
        - 排查重试多次仍失败的任务时配合 ``detail`` 一起看
        - 复用 agent status 接口, 集中提取错误相关字段

    Parameters:
        --id (int, 必填): 任务 ID
        --json (bool, 可选): 输出原始 JSON (完整 API 响应), 默认 False
        --url, -u (str, 可选): API base URL

    Output:
        文本模式: 打印 Agent状态/错误码/错误信息/重试次数/执行SQL (截断到 300 字符)
        JSON 模式结构 (与 ``status`` 一致, 输出完整 ``result``)::

            {
              "success": bool,
              "message": str,
              "data": {
                "agentStatus": str,
                "lastErrorCode": str,
                "lastErrorMessage": str,
                "sqlcontent": str,
                "retryCount": int,
                "maxRetryCount": int,
                ...
              }
            }

    Exit codes:
        0: 查询成功 (无论任务本身是否有错误)
        1: 查询失败 (鉴权失败 / 任务不存在 / 网络错误)

    Examples:
        mec-aisql-cli aisql error --id 123
        mec-aisql-cli aisql error --id 123 --json
    """
    client = _build_client(base_url)
    # 复用 agent status 接口, 集中提取错误相关字段
    result = client.get_aisql_agent_status({"id": id})
    success = result.get("success") or result.get("Success")
    data = result.get("data", {}) if success else {}

    if json_output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        raise typer.Exit(code=0 if success else 1)

    if not success:
        print_result(result, title="错误日志", as_json=False)
        return

    agent_status = data.get("agentStatus", "")
    error_code = data.get("lastErrorCode", "")
    error_msg = data.get("lastErrorMessage", "")
    sql_content = data.get("sqlcontent", "") or ""
    retry_count = data.get("retryCount", 0)
    max_retry = data.get("maxRetryCount", 2)

    typer.echo(f"\n{'=' * 60}")
    typer.echo(f"  错误日志 (任务 ID: {id})")
    typer.echo(f"{'=' * 60}")
    typer.echo(f"  Agent状态:  {agent_status}")
    typer.echo(f"  错误码:     {error_code or '(无)'}")
    typer.echo(f"  错误信息:   {error_msg or '(无)'}")
    typer.echo(f"  重试次数:   {retry_count}/{max_retry}")
    # 仅当 SQL 内容有效时才打印, 过滤占位错误信息 "AI SQL任务执行失败"
    if sql_content and sql_content != "AI SQL任务执行失败":
        typer.echo(f"  执行SQL:   {sql_content[:300]}...")
    if not error_code and not error_msg:
        typer.echo("\n  该任务暂无错误信息。")
