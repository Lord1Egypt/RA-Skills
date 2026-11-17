"""End-to-end AI SQL Agent workflow.

模块用途 (Purpose)
-------------------
本模块实现 AI SQL Agent 的完整工作流编排，包含 7 个阶段:
    Phase 1: gen      —— 调用 AI 大模型生成 HIVE SQL 语句
    Phase 2: guard    —— SQL 类型守卫，确保仅放行统计类查询 (COUNT/SUM/AVG/GROUP BY 等)
    Phase 3: validate —— 提交后端校验 SQL 语法与可执行性
    Phase 4: create   —— 创建持久化任务并保存 SQL
    Phase 5: perform  —— 触发任务执行（创建工单）
    Phase 6: watch    —— 轮询监控任务状态直至终态
    Phase 7: result   —— 查询最终执行结果（结果表、文件路径、DMS ID 等）

两种入口
--------
- run_agent(): 交互式完整流程，允许人工确认与重试，适用于 CLI 人工操作。
- run_bot():   全自动 Bot 流程，无任何交互提示，仅放行统计类 SQL，返回结构化 JSON。

AI 使用提示 (AI Usage)
-----------------------
- AI Bot 自动化场景优先调用 run_bot()，以获取可直接解析的 JSON 结果。
- run_agent() 包含 typer.prompt / typer.confirm，不适合无人值守调用。
- Bot 模式下 SQL 类型守卫为强制阻断：非统计类 SQL 自动重试或直接拒绝。
"""
import json
import time
from typing import Any, Dict, Optional

import typer

from mec_aisql_cli.api_client import AisqlApiClient
from mec_aisql_cli.config import Config
from mec_aisql_cli.datetime_utils import validate_datetimefw
from mec_aisql_cli.output import confirm, print_result
from mec_aisql_cli.sql_guard import check_sql_type, format_guard_result, GuardResult


DATA_FROM_OPTIONS = ["ADM", "OTT-OM", "OTT-PMO", "TVM", "BDID-MZID", "BDID-IPV6"]


class RunResult:
    """Holds the result of a run phase."""
    def __init__(self, success: bool = False, data: Optional[Dict] = None, error: str = ""):
        self.success = success
        self.data = data or {}
        self.error = error

    @property
    def sql(self) -> str:
        return self.data.get("sql", "")

    @property
    def task_id(self) -> int:
        return self.data.get("id", 0)


def build_client(debug: bool = False, config: Optional[Config] = None) -> AisqlApiClient:
    """Build API client from config or defaults."""
    if config:
        kwargs = config.as_api_kwargs()
        kwargs["debug"] = debug
        return AisqlApiClient(**kwargs)
    return AisqlApiClient(debug=debug)


# ============================================================
# Phase 1: Generate SQL via AI
# ============================================================
def phase_gen(
    client: AisqlApiClient,
    comment: str,
    model: str,
    client_name: str,
    brand: str,
    datafrom: str,
    contype: Optional[str],
    datetimefw: str,
    debug: bool = False,
) -> RunResult:
    """Phase 1: 调用 AI 大模型生成 HIVE SQL 语句。

    将 comment 与业务参数（客户/品牌/数据来源/日期/分析类型）拼接为完整提示，
    调用 client.gen_aisql 提交后端 AI 服务，返回生成的 SQL 与 token 使用统计。
    """
    typer.echo("\n>>> [1/7] AI 生成 SQL...")

    params_parts = []
    if client_name:
        params_parts.append(f"客户为「{client_name}」")
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
    full_comment = (
        f"{comment}。{params_text}。"
        f"请基于上述业务场景和约束条件，生成符合 HIVE SQL 语法规范的查询语句。"
    ) if params_text else (
        f"{comment}。请生成符合 HIVE SQL 语法规范的查询语句。"
    )

    data = {
        "comment": full_comment,
        "models": model,
        "client": client_name,
        "brand": brand,
        "datafrom": datafrom,
        "datetimefw": datetimefw,
    }
    if contype:
        data["contype"] = contype

    result = client.gen_aisql(data)
    if not (result.get("success") or result.get("Success")):
        return RunResult(error=f"生成失败: {result.get('message', result.get('Message', ''))}")

    sql = result.get("data", {}).get("sql", "")
    if not sql:
        return RunResult(error="生成的 SQL 为空")

    tokens = result.get("data", {})
    typer.echo(f"  Tokens: input={tokens.get('prompt_tokens', '?')}, "
               f"output={tokens.get('completion_tokens', '?')}, "
               f"total={tokens.get('total_tokens', '?')}")
    typer.echo(f"  SQL: {sql[:120]}{'...' if len(sql) > 120 else ''}")

    return RunResult(success=True, data={"sql": sql, **tokens})


# ============================================================
# Phase 2: SQL Type Guard — only statistical queries allowed
# ============================================================
def phase_guard(sql: str, bot_mode: bool = False) -> GuardResult:
    """Phase 2: SQL 类型守卫 — 检测 SQL 是否为统计类查询。

    守卫逻辑 (Guard logic)
    -----------------------
    - 调用 check_sql_type(sql) 解析 SQL 语句，识别其类型（statistical/detail/dml 等）。
    - 统计类查询 (含 COUNT/SUM/AVG/MIN/MAX/GROUP BY) 视为 allowed=True，允许放行。
    - 非统计类查询 (明细 SELECT、DELETE/UPDATE/INSERT 等) 视为 allowed=False。
    - bot_mode=True 时：守卫未通过会触发上层 run_bot 自动重试重新生成 SQL。
    - bot_mode=False 时：仅向用户提示风险，决定权交给交互式确认。

    参数
    -----
    sql : str
        待检查的 SQL 文本。
    bot_mode : bool
        是否为 Bot 自动化模式（影响日志输出与上层重试行为）。

    返回
    -----
    GuardResult: 包含 allowed、sql_type、reason、aggregate_functions 字段。
    """
    if bot_mode:
        typer.echo("\n>>> [2/7] SQL 类型守卫 (Bot 模式)...")
    else:
        typer.echo("\n>>> [2/7] SQL 类型守卫...")

    # SQL 类型检测：解析 SQL 文本，识别是否包含聚合函数 / GROUP BY 等统计特征
    result = check_sql_type(sql)
    typer.echo(format_guard_result(result))

    # Bot 模式下守卫未通过：打印阻断原因，供调用方诊断
    if not result.allowed and bot_mode:
        typer.echo(f"\n[BLOCKED] Bot 自动化已阻断非统计类 SQL")
        typer.echo(f"  类型: {result.sql_type}")
        typer.echo(f"  原因: {result.reason}")

    return result


# ============================================================
# Phase 3: Validate SQL via backend
# ============================================================
def phase_validate(
    client: AisqlApiClient,
    sql: str,
    datafrom: str,
    datetimefw: str,
    debug: bool = False,
) -> RunResult:
    """Phase 3: 提交后端校验 SQL 语法与可执行性。

    调用 client.validate_aisql 提交 SQL 至后端，后端返回 valid / executable 标志位
    及 errors / warnings 列表。仅在 valid 与 executable 同时为 True 时通过。
    """
    typer.echo("\n>>> [3/7] SQL 校验...")

    payload = {"sql": sql}
    if datafrom:
        payload["datafrom"] = datafrom
    if datetimefw:
        payload["datetimefw"] = datetimefw

    result = client.validate_aisql(payload)
    if not (result.get("success") or result.get("Success")):
        return RunResult(error=f"校验请求失败: {result.get('message', result.get('Message', ''))}")

    validation = result.get("data", {})
    is_valid = validation.get("valid", False)
    is_executable = validation.get("executable", False)

    if not is_valid or not is_executable:
        errors = validation.get("errors", [])
        warnings = validation.get("warnings", [])
        error_text = "\n".join(f"  - {e.get('code')}: {e.get('message')}" for e in errors)
        warn_text = "\n".join(f"  - {w.get('code')}: {w.get('message')}" for w in warnings)
        msg_parts = ["SQL 校验未通过"]
        if error_text:
            msg_parts.append(f"Errors:\n{error_text}")
        if warn_text:
            msg_parts.append(f"Warnings:\n{warn_text}")
        return RunResult(
            success=False,
            error="\n".join(msg_parts),
            data={"validation": validation, "sql": sql},
        )

    if warnings := validation.get("warnings", []):
        typer.echo("  校验通过，存在提示:")
        for w in warnings:
            typer.echo(f"  WARN: {w.get('code')}: {w.get('message')}")

    typer.echo("  校验通过")
    return RunResult(success=True, data={"sql": sql, "validation": validation})


# ============================================================
# Phase 4: Create task
# ============================================================
def phase_create(
    client: AisqlApiClient,
    task_name: str,
    sql: str,
    comment: str,
    client_name: str,
    brand: str,
    datafrom: str,
    contype: str,
    datetimefw: str,
    clientid: str = "",
    brandid: str = "",
    saleid: str = "",
    dtsaccount: str = "",
    dtspass: str = "",
    sccontent: Optional[str] = None,
    model: Optional[str] = None,
) -> RunResult:
    """Phase 4: 创建持久化任务并保存 SQL。

    调用 client.create_aisql_task 提交任务元数据（名称/客户/品牌/数据来源/SQL 等），
    后端返回任务 ID。后续 perform/watch 阶段依赖此 ID。

    saleid / dtsaccount / dtspass 来自 brand 查找, 创建工单(perform)时为必填字段。
    """
    typer.echo("\n>>> [4/7] 创建任务...")

    data = {
        "aiTaskName": task_name,
        "clientid": clientid,
        "client": client_name,
        "brandid": brandid,
        "brand": brand,
        "datafrom": datafrom,
        "contype": contype,
        "datetimefw": datetimefw,
        "comment": comment,
        "sql": sql,
        "SaleId": saleid,
        "dtsaccount": dtsaccount,
        "dtspassword": dtspass,
    }
    if sccontent:
        data["sccontent"] = sccontent
    if model:
        data["models"] = model

    result = client.create_aisql_task(data)
    if not (result.get("success") or result.get("Success")):
        return RunResult(error=f"创建失败: {result.get('message', result.get('Message', ''))}")

    task_data = result.get("data", {})
    task_id = task_data.get("id", 0)
    typer.echo(f"  任务创建成功, ID: {task_id}")

    return RunResult(success=True, data={"id": task_id, **task_data})


# ============================================================
# Phase 5: Execute task (create work order)
# ============================================================
def phase_perform(
    client: AisqlApiClient,
    task_id: int,
    task_template_id: str = "1078",
) -> RunResult:
    """Phase 5: 触发任务执行（创建工单）。

    调用 client.perform_aisql_task 提交任务 ID 与工单模板 ID，
    后端据此创建执行工单并启动 SQL 运行流程。
    """
    typer.echo("\n>>> [5/7] 执行任务（创建工单）...")

    result = client.perform_aisql_task({"id": task_id, "taskId": task_template_id})
    if not (result.get("success") or result.get("Success")):
        return RunResult(error=f"执行失败: {result.get('message', result.get('Message', ''))}")

    typer.echo("  工单创建成功")
    return RunResult(success=True, data=result.get("data", {}))


# ============================================================
# Phase 6: Watch task until completion
# ============================================================
def phase_watch(
    client: AisqlApiClient,
    task_id: int,
    interval: Optional[int] = None,
    timeout: Optional[int] = None,
) -> RunResult:
    """Phase 6: 监控循环 — 轮询任务状态直至终态或超时。

    以 while 循环调用 client.get_aisql_agent_status 拉取任务最新状态：
    - 命中 timeout 时返回 "等待超时" 失败。
    - 命中 isTerminal 且 status=Succeeded 时返回成功，附带 tableName/fileRouter。
    - 命中 isTerminal 但非成功时返回失败，附带 lastErrorMessage。
    - 非终态时按 interval / nextPollAfterSeconds / 30 秒休眠后再次轮询。
    """
    typer.echo("\n>>> [6/7] 监控任务进度...")

    started_at = time.time()
    last_status = None

    # 监控循环（Watch loop）：持续轮询后端任务状态直至终态或超时。
    while True:
        # 超时检查：达到 timeout 秒数后立即返回失败
        if timeout and (time.time() - started_at) >= timeout:
            return RunResult(
                success=False,
                error="等待超时",
                data={"agentStatus": last_status},
            )

        # 拉取最新任务状态：agentStatus、progress、message、isTerminal
        result = client.get_aisql_agent_status({"id": task_id})
        if not (result.get("success") or result.get("Success")):
            return RunResult(error=f"查询状态失败: {result.get('message', result.get('Message', ''))}")

        data = result.get("data", {})
        status = data.get("agentStatus", "-")
        progress = data.get("progress", 0)
        message = data.get("status", "")
        is_terminal = data.get("isTerminal", False)

        # 仅在状态变化时打印日志，避免刷屏
        if status != last_status:
            typer.echo(f"  [{time.strftime('%H:%M:%S')}] {status} {progress}% {message}")
            last_status = status

        # 终态判定：is_terminal=True 表示任务到达终态（成功或失败）
        if is_terminal:
            if status == "Succeeded":
                # 成功终态：返回结果数据（表名、文件路径等）
                typer.echo(f"  任务完成! Table: {data.get('tableName', '-')}, "
                          f"File: {data.get('fileRouter', '-') or '-'}")
                return RunResult(success=True, data=data)
            else:
                # 失败终态：携带 lastErrorMessage 返回失败
                error_msg = data.get("lastErrorMessage", status)
                return RunResult(
                    success=False,
                    error=f"任务未成功 ({status}): {error_msg}",
                    data=data,
                )

        # 非终态：休眠后再次轮询。优先使用 interval，其次后端建议的 nextPollAfterSeconds，默认 30 秒
        sleep_seconds = interval or data.get("nextPollAfterSeconds") or 30
        time.sleep(max(1, int(sleep_seconds)))


# ============================================================
# Phase 7: Query execution result
# ============================================================
def phase_result(client: AisqlApiClient, task_id: int) -> RunResult:
    """Phase 7: 查询最终执行结果。

    再次调用 client.get_aisql_agent_status 拉取任务终态数据，
    仅当 status=Succeeded 时返回结果表名、文件路径、DMS 查询/导出 ID 等结果字段。
    """
    typer.echo("\n>>> [7/7] 查询执行结果...")

    result = client.get_aisql_agent_status({"id": task_id})
    if not (result.get("success") or result.get("Success")):
        return RunResult(error=f"查询失败: {result.get('message', result.get('Message', ''))}")

    data = result.get("data", {})
    status = data.get("agentStatus", "-")

    if status != "Succeeded":
        return RunResult(
            success=False,
            error=f"任务尚未完成 (当前状态: {status})，无法查询结果",
            data=data,
        )

    typer.echo(f"  任务状态: {status}")
    typer.echo(f"  进度: {data.get('progress', 100)}%")

    if data.get("tableName"):
        typer.echo(f"  结果表名: {data['tableName']}")
    if data.get("fileRouter"):
        typer.echo(f"  结果文件: {data['fileRouter']}")
    if data.get("sqldmsid"):
        typer.echo(f"  DMS 查询ID: {data['sqldmsid']}")
    if data.get("dmstaskid"):
        typer.echo(f"  DMS 导出ID: {data['dmstaskid']}")
    if data.get("orderid"):
        typer.echo(f"  工单ID: {data['orderid']}")
    if data.get("sqlcontent"):
        typer.echo(f"  执行SQL: {data['sqlcontent'][:200]}...")

    return RunResult(success=True, data=data)


# ============================================================
# Full agent flow (interactive)
# ============================================================
def run_agent(
    comment: str,
    client_name: Optional[str],
    brand: Optional[str],
    datafrom: Optional[str],
    contype: Optional[str],
    datetimefw: Optional[str],
    model: str,
    task_name: Optional[str],
    auto_create: bool,
    auto_perform: bool,
    watch_after: bool,
    watch_timeout: int,
    no_confirm: bool,
    base_url: str,
    debug: bool,
):
    """运行 AI SQL Agent 完整工作流（交互式模式，7 阶段）。

    用途 (Purpose)
    --------------
    执行端到端的 AI SQL Agent 流程：从自然语言业务描述生成 HIVE SQL，
    经类型守卫、后端校验、任务创建、工单触发、进度监控，直至取回执行结果。
    交互模式下，缺失的参数会通过 typer.prompt 询问用户，关键节点支持 typer.confirm 二次确认。

    AI 调用时机 (AI Usage)
    -----------------------
    - 仅适合 CLI 人工操作场景；包含 typer.prompt / typer.confirm 交互。
    - AI Bot 自动化场景请改用 run_bot()，避免被交互式 prompt 阻塞。
    - 若 AI 必须通过子进程执行 CLI 命令并完整流转所有阶段，可调用本函数，
      但需预先提供全部必填参数并设置 no_confirm=True 以跳过交互提示。

    参数 (Parameters)
    -----------------
    comment : str
        业务需求自然语言描述（必填），AI 据此生成 SQL。
    client_name : Optional[str]
        客户名称，缺失时交互式询问。
    brand : Optional[str]
        品牌名称，缺失时交互式询问。
    datafrom : Optional[str]
        数据来源标识，可选值见 DATA_FROM_OPTIONS（ADM/OTT-OM/OTT-PMO/TVM/BDID-MZID/BDID-IPV6）。
    contype : Optional[str]
        分析类型，可选参数。
    datetimefw : str
        统计日期或日期区间，格式如 "20260301" 或 "20260301-20260331"。
    model : str
        AI 模型标识，默认从 config 读取 (mlamp/deepseek-v4-flash)。
    task_name : Optional[str]
        任务名称，缺省时按 comment 前 30 字符自动生成。
    auto_create : bool
        True=跳过创建任务前的确认；False=需要用户确认。
    auto_perform : bool
        True=跳过执行任务前的确认；False=需要用户确认。
    watch_after : bool
        True=执行后进入监控循环直至终态；False=仅提交任务后退出。
    watch_timeout : int
        监控循环超时秒数，默认 1800 秒。
    no_confirm : bool
        True=跳过所有 typer.confirm 二次确认；False=按需确认。
    base_url : str
        后端服务地址，默认从 config 读取 (https://mec.miaozhen.com/taskmng)。
    debug : bool
        是否开启调试日志。

    返回值 (Returns)
    ----------------
    无显式返回值。流程中各分支行为：
    - 成功完成：函数自然结束（无 return）。
    - 用户取消（如拒绝继续执行非统计类 SQL）：直接 return。
    - 任意 Phase 失败：raise typer.Exit(code=1)，进程退出码为 1。

    错误码 (Error codes)
    ---------------------
    本函数通过 typer.Exit(code=1) 表示失败，具体失败原因通过 typer.echo 输出。
    失败可能原因：
    - Phase 1 生成失败/SQL 为空
    - Phase 3 校验未通过且用户拒绝重新生成或重试后仍未通过
    - Phase 4 创建任务失败
    - Phase 5 执行任务（创建工单）失败
    - Phase 6 监控超时或任务进入非成功终态

    流程步骤 (Flow steps)
    ----------------------
    1. Phase 1 (gen)      : 调用 phase_gen 让 AI 生成 SQL。
    2. Phase 2 (guard)    : 调用 phase_guard 做 SQL 类型守卫，非统计类提示用户。
    3. Phase 3 (validate) : 调用 phase_validate 提交后端校验；失败时支持重新生成重试。
    4. Phase 4 (create)   : 调用 phase_create 持久化任务并保存 SQL。
    5. Phase 5 (perform)  : 调用 phase_perform 触发任务执行（创建工单）。
    6. Phase 6 (watch)     : 调用 phase_watch 轮询任务状态直至终态。
    7. Phase 7 (result)   : watch 成功后通过 watch_result 直接拿到结果数据（合并到 Phase 6）。
    """
    config = Config()

    model = model or config.get("model", "mlamp/deepseek-v4-flash")
    client_name = client_name or config.get("client", "")
    brand = brand or config.get("brand", "")
    datafrom = datafrom or config.get("datafrom", "")
    contype = contype or config.get("contype", "")
    datetimefw = datetimefw or config.get("datetimefw", "")
    base_url = base_url or config.get("base_url", "https://mec.miaozhen.com/taskmng")

    client = build_client(debug, config)
    task_name = task_name or f"AI SQL - {comment[:30]}"

    # Interactive prompts for missing required fields
    if not client_name:
        client_name = typer.prompt("请输入客户名称")
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
        typer.echo("请选择数据来源:")
        for i, opt in enumerate(DATA_FROM_OPTIONS, 1):
            typer.echo(f"  {i}. {opt}")
        while True:
            choice = typer.prompt(f"请输入序号 (1-{len(DATA_FROM_OPTIONS)})")
            if choice.isdigit() and 1 <= int(choice) <= len(DATA_FROM_OPTIONS):
                datafrom = DATA_FROM_OPTIONS[int(choice) - 1]
                break
            typer.echo("请输入有效的序号")

    # ============================================================
    # Phase 1 START: Generate SQL via AI
    # ============================================================
    gen_result = phase_gen(client, comment, model, client_name, brand, datafrom, contype, datetimefw, debug)
    if not gen_result.success:
        typer.echo(f"\n[ERROR] {gen_result.error}")
        raise typer.Exit(code=1)

    # ============================================================
    # Phase 2 START: SQL Type Guard (interactive — warn only)
    # ============================================================
    # SQL 类型守卫：检测 SQL 是否为统计类查询。
    # 交互模式下非统计类不强制阻断，仅向用户提示风险并要求确认。
    # bot_mode=False 表示提示但不阻断，决定权交给用户。
    guard_result = phase_guard(gen_result.sql, bot_mode=False)
    if not guard_result.allowed:
        # 守卫未通过：非统计类 SQL（如 SELECT *、DELETE、UPDATE 等）
        typer.echo(f"\n[WARN] SQL 类型守卫提示: {guard_result.reason}")
        typer.echo("  非 Bot 模式下仍可继续，但请注意安全风险。")
        if not no_confirm:
            # 用户需手动确认是否继续执行非统计类 SQL
            if not confirm("是否继续执行非统计类 SQL？"):
                typer.echo("已取消。")
                return

    # ============================================================
    # Phase 3 START: Validate SQL via backend
    # ============================================================
    # 后端校验：检查 SQL 语法、可执行性，并返回 errors / warnings 列表。
    validate_result = phase_validate(client, gen_result.sql, datafrom, datetimefw, debug)
    if not validate_result.success:
        typer.echo(f"\n[ERROR] {validate_result.error}")
        if not no_confirm:
            # 重试/重新生成逻辑：校验失败后允许用户选择是否重新生成 SQL。
            # 重新生成后必须重新执行 Phase 2 守卫与 Phase 3 校验，确保新 SQL 合规。
            retry = typer.confirm("是否重新生成 SQL？", default=False)
            if retry:
                # 重新调用 Phase 1 生成 SQL
                gen_result = phase_gen(client, comment, model, client_name, brand, datafrom, contype, datetimefw, debug)
                if gen_result.success:
                    # 重新生成成功后必须重新守卫 + 重新校验
                    guard_result = phase_guard(gen_result.sql, bot_mode=False)
                    validate_result = phase_validate(client, gen_result.sql, datafrom, datetimefw, debug)
                    if not validate_result.success:
                        # 重试后校验仍未通过，结束流程
                        typer.echo(f"\n[ERROR] 重新生成后校验仍未通过: {validate_result.error}")
                        raise typer.Exit(code=1)
                else:
                    # 重新生成本身失败
                    typer.echo(f"\n[ERROR] 重新生成失败: {gen_result.error}")
                    raise typer.Exit(code=1)
            else:
                # 用户拒绝重试，直接退出
                raise typer.Exit(code=1)
        else:
            # no_confirm 模式下不提供重试机会，直接失败
            raise typer.Exit(code=1)

    typer.echo(f"\nSQL 校验通过:")
    typer.echo(f"  {gen_result.sql}")

    # ============================================================
    # Phase 4 START: Create task
    # ============================================================
    if not auto_create and not no_confirm:
        if not confirm("是否创建任务并保存 SQL？"):
            typer.echo("\n仅生成 SQL，退出。")
            return

    # Pre-flight: 按名查 clientid / brandid (创建任务 + 工单必需)
    typer.echo("\n>>> 按客户名查找 clientid...")
    cli_lookup = client.lookup_client_by_name(client_name)
    if not (cli_lookup.get("success") or cli_lookup.get("Success")):
        typer.echo(f"[ERROR] 未找到客户「{client_name}」: {cli_lookup.get('message', '')}")
        raise typer.Exit(code=1)
    clientid = cli_lookup["data"]["clientid"]
    typer.echo(f"  clientid = {clientid}")

    typer.echo(">>> 按品牌名查找 brandid...")
    brand_lookup = client.lookup_brand_by_name(brand, clientid)
    if not (brand_lookup.get("success") or brand_lookup.get("Success")):
        typer.echo(f"[ERROR] 未找到品牌「{brand}」: {brand_lookup.get('message', '')}")
        raise typer.Exit(code=1)
    brand_data = brand_lookup["data"]
    brandid = brand_data["brandid"]
    saleid = brand_data.get("saleid", "")
    dtsaccount = brand_data.get("dtsaccount", "")
    dtspass = brand_data.get("dtspass", "")
    typer.echo(f"  brandid = {brandid}")
    typer.echo(f"  saleid = {saleid or '(空)'}, dtsaccount = {dtsaccount or '(空)'}")

    create_result = phase_create(
        client, task_name, gen_result.sql, comment,
        client_name, brand, datafrom, contype or "-", datetimefw,
        clientid=clientid, brandid=brandid,
        saleid=saleid, dtsaccount=dtsaccount, dtspass=dtspass,
    )
    if not create_result.success:
        typer.echo(f"\n[ERROR] {create_result.error}")
        raise typer.Exit(code=1)

    task_id = create_result.task_id

    # ============================================================
    # Phase 5 START: Perform task (create work order)
    # ============================================================
    if not auto_perform and not no_confirm:
        if not confirm(f"是否执行任务 (ID: {task_id}) 并创建工单？"):
            typer.echo(f"\n任务已创建 (ID: {task_id})，未执行。")
            typer.echo(f"稍后可运行: mec-aisql aisql perform --id {task_id}")
            return

    perform_result = phase_perform(client, task_id)
    if not perform_result.success:
        typer.echo(f"\n[ERROR] {perform_result.error}")
        raise typer.Exit(code=1)

    # ============================================================
    # Phase 6 START: Watch task until completion (interactive mode)
    # ============================================================
    if not watch_after:
        typer.echo(f"\n任务已提交执行 (ID: {task_id})")
        typer.echo(f"监控进度: mec-aisql aisql watch --id {task_id}")
        return

    watch_result = phase_watch(client, task_id, timeout=watch_timeout)
    if watch_result.success:
        typer.echo(f"\n[SUCCESS] 任务执行完成!")
        if watch_result.data.get("tableName"):
            typer.echo(f"  结果表: {watch_result.data['tableName']}")
        if watch_result.data.get("fileRouter"):
            typer.echo(f"  文件路径: {watch_result.data['fileRouter']}")
    else:
        typer.echo(f"\n[ERROR] 任务执行未成功: {watch_result.error}")
        raise typer.Exit(code=1)


# ============================================================
# Bot mode: non-interactive, statistical-only, fully automated
# ============================================================
def run_bot(
    comment: str,
    client_name: str,
    brand: str,
    datafrom: str,
    datetimefw: str,
    contype: str = "",
    model: str = "",
    task_name: str = "",
    clientid: str = "",
    brandid: str = "",
    saleid: str = "",
    dtsaccount: str = "",
    dtspass: str = "",
    watch_timeout: int = 1800,
    max_regen_attempts: int = 2,
    base_url: str = "",
    debug: bool = False,
) -> Dict[str, Any]:
    """运行全自动 Bot 工作流（无交互，统计类 SQL 强制守卫）。

    用途 (Purpose)
    --------------
    无人值守地完成 AI SQL Agent 完整 7 阶段流程：生成 → 类型守卫 → 校验 →
    创建任务 → 触发工单 → 监控进度 → 返回结果。
    全过程无任何 typer.prompt / typer.confirm，所有参数必须由调用方显式提供。
    SQL 类型守卫为强制阻断：非统计类 SQL 会自动重试，仍不通过则返回 SQL_TYPE_BLOCKED。

    AI 调用时机 (AI Usage)
    -----------------------
    - AI Bot 自动化场景应优先调用本函数，以获取可直接解析的 JSON 结果。
    - 所有参数必须显式传入；缺失必填参数会立即返回 MISSING_PARAMS 错误。
    - 若 SQL 类型多次重试仍不通过，应提示用户调整业务描述 (comment) 后重试。
    - 调用前请确保已登录（client.is_authenticated()），否则返回 NOT_AUTHENTICATED。

    参数 (Parameters)
    -----------------
    comment : str
        业务需求自然语言描述（必填），AI 据此生成 SQL。建议描述清晰、聚焦统计目标。
    client_name : str
        客户名称（必填）。
    brand : str
        品牌名称（必填）。
    datafrom : str
        数据来源标识（必填），可选值：ADM/OTT-OM/OTT-PMO/TVM/BDID-MZID/BDID-IPV6。
    datetimefw : str
        统计日期或日期区间（必填），格式如 "20260301" 或 "20260301-20260331"。
    contype : str, optional
        分析类型，默认空字符串。
    model : str, optional
        AI 模型标识，默认从 config 读取 (mlamp/deepseek-v4-flash)。
    task_name : str, optional
        任务名称，缺省时按 "Bot SQL - {comment 前 30 字符}" 自动生成。
    watch_timeout : int, optional
        监控循环超时秒数，默认 1800 秒（30 分钟）。
    max_regen_attempts : int, optional
        SQL 类型守卫失败后最大重试重新生成次数，默认 2 次。
    base_url : str, optional
        后端服务地址，默认从 config 读取 (https://mec.miaozhen.com/taskmng)。
    debug : bool, optional
        是否开启调试日志，默认 False。

    返回值 (Returns)
    ----------------
    Dict[str, Any]，结构化 JSON 结果，分两种情况：

    成功 (success=True)：
        {
            "success": True,
            "task_id": int,                  # 任务 ID
            "sql": str,                      # 最终执行的 SQL 文本
            "sql_type": str,                 # SQL 类型 (statistical 等)
            "aggregate_functions": list[str],# 检测到的聚合函数列表
            "status": str,                   # 任务终态 (Succeeded)
            "table_name": str,               # 结果表名
            "file_router": str,              # 结果文件路径
            "order_id": str,                 # 工单 ID
            "dms_query_id": str,             # DMS 查询 ID (sqldmsid)
            "dms_export_id": str,            # DMS 导出 ID (dmstaskid)
        }

    失败 (success=False)：返回结构包含 error、message 字段，并尽可能附带上下文：
        {
            "success": False,
            "error": "<ERROR_CODE>",
            "message": str,
            # 以下字段视 error 类型而定：
            "sql_type": str,                # SQL_TYPE_BLOCKED 时附带
            "reason": str,                  # SQL_TYPE_BLOCKED 时附带
            "sql": str,                     # SQL_TYPE_BLOCKED 时附带
            "task_id": int,                 # PERFORM_FAILED / WATCH_FAILED 时附带
            "status": str,                  # WATCH_FAILED 时附带 (任务终态)
        }

    错误码 (Error codes)
    ---------------------
    本函数返回的 error 字段可能取值：
    - "MISSING_PARAMS"     : 必填参数缺失（client/brand/datafrom/datetimefw）。
    - "NOT_AUTHENTICATED" : Bot 未登录，需先执行 login。
    - "GEN_FAILED"         : Phase 1 AI 生成 SQL 失败。
    - "SQL_TYPE_BLOCKED"   : Phase 2 SQL 类型守卫阻断（非统计类，重试 max_regen_attempts 次仍未通过）。
    - "VALIDATION_FAILED"  : Phase 3 后端校验未通过（重试 1 次仍失败）。
    - "CREATE_FAILED"      : Phase 4 创建任务失败。
    - "PERFORM_FAILED"     : Phase 5 执行任务（创建工单）失败。
    - "WATCH_FAILED"       : Phase 6 监控超时或任务进入非成功终态。

    流程步骤 (Flow steps)
    ----------------------
    1. 参数校验：检查必填参数与登录态。
    2. Phase 1 (gen)      : 调用 phase_gen 生成 SQL，失败返回 GEN_FAILED。
    3. Phase 2 (guard)    : 调用 phase_guard 严格守卫；非统计类自动重试重新生成最多 max_regen_attempts 次，
                            仍不通过返回 SQL_TYPE_BLOCKED。
    4. Phase 3 (validate) : 调用 phase_validate 校验 SQL；失败时重试 1 次重新生成，仍不通过返回 VALIDATION_FAILED。
    5. Phase 4 (create)   : 调用 phase_create 持久化任务，失败返回 CREATE_FAILED。
    6. Phase 5 (perform)  : 调用 phase_perform 触发工单，失败返回 PERFORM_FAILED。
    7. Phase 6 (watch)    : 调用 phase_watch 轮询监控直至终态，超时或非成功终态返回 WATCH_FAILED。
    8. Phase 7 (result)   : 直接复用 watch_result.data，组装成功结果 JSON 返回。
    """
    config = Config()

    model = model or config.get("model", "mlamp/deepseek-v4-flash")
    client_name = client_name or config.get("client", "")
    brand = brand or config.get("brand", "")
    datafrom = datafrom or config.get("datafrom", "")
    datetimefw = datetimefw or config.get("datetimefw", "")
    contype = contype or config.get("contype", "")
    base_url = base_url or config.get("base_url", "https://mec.miaozhen.com/taskmng")

    client = build_client(debug, config)
    task_name = task_name or f"Bot SQL - {comment[:30]}"

    # Validate required parameters
    missing = []
    if not client_name:
        missing.append("client")
    if not brand:
        missing.append("brand")
    if not datafrom:
        missing.append("datafrom")
    if not datetimefw:
        missing.append("datetimefw")
    if missing:
        return {
            "success": False,
            "error": "MISSING_PARAMS",
            "message": f"Bot 模式缺少必要参数: {', '.join(missing)}",
        }

    # 校验 datetimefw 格式 (前端要求 ["YYYY-MM-DD","YYYY-MM-DD"] 数组)
    # 输入支持灵活格式, 不合法则在此早期失败, 避免任务创建后前端渲染异常
    dt_ok, dt_result = validate_datetimefw(datetimefw)
    if not dt_ok:
        return {
            "success": False,
            "error": "INVALID_DATETIMEFW",
            "message": f"datetimefw 格式不合法: {dt_result}, "
            f"示例: --datetimefw '2026-03-01/2026-03-31' 或 '20260301-20260331'",
        }

    # Check authentication
    if not client.is_authenticated():
        return {
            "success": False,
            "error": "NOT_AUTHENTICATED",
            "message": "Bot 未登录，请先执行 login",
        }

    # ============================================================
    # Pre-flight: 按名查 clientid / brandid (创建任务必需)
    # ============================================================
    # 创建 AISQL 任务需要 32 位 hash 形式的 clientid / brandid。
    # 若调用方未显式传入, 则通过 Ml_Client / Ml_Brand 分页接口按名称自动查找。
    if not clientid:
        typer.echo("\n>>> [0/7] 按客户名查找 clientid...")
        cli_lookup = client.lookup_client_by_name(client_name)
        if not (cli_lookup.get("success") or cli_lookup.get("Success")):
            return {
                "success": False,
                "error": "LOOKUP_FAILED",
                "message": f"未找到客户「{client_name}」: {cli_lookup.get('message', '')}",
            }
        clientid = cli_lookup["data"]["clientid"]
        typer.echo(f"  clientid = {clientid}")

    if not brandid:
        typer.echo(">>> [0/7] 按品牌名查找 brandid...")
        brand_lookup = client.lookup_brand_by_name(brand, clientid)
        if not (brand_lookup.get("success") or brand_lookup.get("Success")):
            return {
                "success": False,
                "error": "LOOKUP_FAILED",
                "message": f"未找到品牌「{brand}」: {brand_lookup.get('message', '')}",
            }
        brand_data = brand_lookup["data"]
        brandid = brand_data["brandid"]
        # brand 实体带 saleid/dtsaccount/dtspass, 创建工单(perform)时为必填字段
        saleid = saleid or brand_data.get("saleid", "")
        dtsaccount = dtsaccount or brand_data.get("dtsaccount", "")
        dtspass = dtspass or brand_data.get("dtspass", "")
        typer.echo(f"  brandid = {brandid}")
        typer.echo(f"  saleid = {saleid or '(空)'}, dtsaccount = {dtsaccount or '(空)'}")

    # ============================================================
    # Phase 1 START: Generate SQL via AI
    # ============================================================
    gen_result = phase_gen(client, comment, model, client_name, brand, datafrom, contype, datetimefw, debug)
    if not gen_result.success:
        return {"success": False, "error": "GEN_FAILED", "message": gen_result.error}

    # ============================================================
    # Phase 2 START: SQL Type Guard (strict — block non-statistical)
    # ============================================================
    # 强制类型守卫：Bot 模式下只允许统计类 SQL（含聚合函数/GROUP BY）通过。
    # 非统计类 SQL 会自动重新生成并重新守卫，最多重试 max_regen_attempts 次。
    guard_result = phase_guard(gen_result.sql, bot_mode=True)
    if not guard_result.allowed:
        # 重试/重新生成逻辑：守卫失败后注入"统计类强调"提示，让 AI 重新生成更合规的 SQL。
        for attempt in range(max_regen_attempts):
            typer.echo(f"\n  [Bot] 尝试重新生成 (attempt {attempt + 1}/{max_regen_attempts})...")
            # 在 comment 中追加统计类强调：要求聚合函数或 GROUP BY 子句
            statistical_comment = (
                f"{comment}。请注意：生成的SQL必须是统计类查询，"
                f"必须包含聚合函数(COUNT/SUM/AVG等)或GROUP BY子句，"
                f"用于数据统计而非明细查询。"
            )
            # 使用强调后的 comment 重新调用 Phase 1 生成 SQL
            gen_result = phase_gen(
                client, statistical_comment, model, client_name, brand, datafrom, contype, datetimefw, debug
            )
            if not gen_result.success:
                # 重新生成本身失败，继续下一次重试
                continue

            # 重新执行守卫检查
            guard_result = phase_guard(gen_result.sql, bot_mode=True)
            if guard_result.allowed:
                # 守卫通过，跳出重试循环
                break

        if not guard_result.allowed:
            # 重试次数耗尽仍未通过：返回 SQL_TYPE_BLOCKED 错误，附带 SQL 上下文供调用方诊断
            return {
                "success": False,
                "error": "SQL_TYPE_BLOCKED",
                "message": f"Bot 自动化仅允许统计类 SQL，已重试 {max_regen_attempts} 次仍未通过",
                "sql_type": guard_result.sql_type,
                "reason": guard_result.reason,
                "sql": gen_result.sql,
            }

    # ============================================================
    # Phase 3 START: Validate SQL via backend
    # ============================================================
    # 后端校验：检查 SQL 语法与可执行性，返回 errors / warnings 列表。
    validate_result = phase_validate(client, gen_result.sql, datafrom, datetimefw, debug)
    if not validate_result.success:
        # 重试逻辑：校验未通过时仅尝试 1 次重新生成（不追加统计强调，使用原始 comment）。
        typer.echo("\n  [Bot] 校验未通过，尝试重新生成...")
        gen_result = phase_gen(client, comment, model, client_name, brand, datafrom, contype, datetimefw, debug)
        if gen_result.success:
            # 重新生成后必须重新走 Phase 2 守卫
            guard_result = phase_guard(gen_result.sql, bot_mode=True)
            if guard_result.allowed:
                # 守卫通过后重新校验
                validate_result = phase_validate(client, gen_result.sql, datafrom, datetimefw, debug)

        if not validate_result.success:
            # 重试后仍未通过：返回 VALIDATION_FAILED
            return {"success": False, "error": "VALIDATION_FAILED", "message": validate_result.error}

    # ============================================================
    # Phase 4 START: Create task
    # ============================================================
    create_result = phase_create(
        client, task_name, gen_result.sql, comment,
        client_name, brand, datafrom, contype or "-", datetimefw,
        clientid=clientid, brandid=brandid,
        saleid=saleid, dtsaccount=dtsaccount, dtspass=dtspass,
    )
    if not create_result.success:
        return {"success": False, "error": "CREATE_FAILED", "message": create_result.error}

    task_id = create_result.task_id

    # ============================================================
    # Phase 5 START: Perform task (create work order)
    # ============================================================
    perform_result = phase_perform(client, task_id)
    if not perform_result.success:
        return {
            "success": False,
            "error": "PERFORM_FAILED",
            "message": perform_result.error,
            "task_id": task_id,
        }

    # ============================================================
    # Phase 6 START: Watch task until completion (bot mode)
    # ============================================================
    watch_result = phase_watch(client, task_id, timeout=watch_timeout)
    if not watch_result.success:
        return {
            "success": False,
            "error": "WATCH_FAILED",
            "message": watch_result.error,
            "task_id": task_id,
            "status": watch_result.data.get("agentStatus"),
        }

    # ============================================================
    # Phase 7 START: Build & return structured result JSON
    # ============================================================
    result_data = watch_result.data
    typer.echo(f"\n[BOT SUCCESS] 任务执行完成!")
    typer.echo(f"  Task ID: {task_id}")
    typer.echo(f"  Status: {result_data.get('agentStatus')}")
    if result_data.get("tableName"):
        typer.echo(f"  Result Table: {result_data['tableName']}")
    if result_data.get("fileRouter"):
        typer.echo(f"  Result File: {result_data['fileRouter']}")

    return {
        "success": True,
        "task_id": task_id,
        "sql": gen_result.sql,
        "sql_type": guard_result.sql_type,
        "aggregate_functions": guard_result.aggregate_functions,
        "status": result_data.get("agentStatus"),
        "table_name": result_data.get("tableName", ""),
        "file_router": result_data.get("fileRouter", ""),
        "order_id": result_data.get("orderid", ""),
        "dms_query_id": result_data.get("sqldmsid", ""),
        "dms_export_id": result_data.get("dmstaskid", ""),
    }
