"""Application entrypoint for the hkipo_next CLI."""

from __future__ import annotations

import argparse
import sys
from typing import Sequence, TextIO

from hkipo_next.cli.commands.calendar import execute as execute_calendar
from hkipo_next.cli.commands.apply_suggestions import execute as execute_apply_suggestions
from hkipo_next.cli.commands.batch import execute as execute_batch
from hkipo_next.cli.commands.decision_card import execute as execute_decision_card
from hkipo_next.cli.commands.params import execute as execute_params
from hkipo_next.cli.commands.profile import execute as execute_profile
from hkipo_next.cli.commands.review import execute as execute_review
from hkipo_next.cli.commands.score import execute as execute_score
from hkipo_next.cli.commands.snapshot import execute as execute_snapshot
from hkipo_next.cli.commands.watchlist import execute as execute_watchlist
from hkipo_next.contracts.errors import AppError, build_error_response, exit_code_for
from hkipo_next.observability.run_context import RunContext
from hkipo_next.renderers.json_renderer import render_model_as_json
from hkipo_next.renderers.text_renderer import render_error_response


OUTPUT_FORMATS = ("json", "text", "markdown")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hkipo-next",
        description="重构后的港股 IPO 决策支持 CLI 主干。",
        exit_on_error=False,
    )
    subparsers = parser.add_subparsers(dest="command")

    calendar_parser = subparsers.add_parser(
        "calendar",
        help="发现即将截止或即将上市的 IPO。",
        exit_on_error=False,
    )
    calendar_parser.add_argument(
        "--window",
        choices=("deadline", "listing"),
        default="deadline",
        help="发现窗口类型：deadline=即将截止，listing=即将上市。",
    )
    calendar_parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="向未来查看的天数。",
    )
    calendar_parser.add_argument(
        "--format",
        choices=OUTPUT_FORMATS,
        default="text",
        help="输出格式，json 为机器权威接口。",
    )
    calendar_parser.add_argument("--output", help="可选：将渲染结果同时导出到文件。")

    snapshot_parser = subparsers.add_parser(
        "snapshot",
        help="查看单个 IPO 的标准化快照。",
        exit_on_error=False,
    )
    snapshot_parser.add_argument("symbol", help="IPO 股票代码。")
    snapshot_parser.add_argument(
        "--format",
        choices=OUTPUT_FORMATS,
        default="text",
        help="输出格式，json 为机器权威接口。",
    )
    snapshot_parser.add_argument("--output", help="可选：将渲染结果同时导出到文件。")

    profile_parser = subparsers.add_parser(
        "profile",
        help="查看或更新个人风险偏好与默认输出偏好。",
        exit_on_error=False,
    )
    profile_subparsers = profile_parser.add_subparsers(dest="profile_action", required=True)

    profile_show_parser = profile_subparsers.add_parser(
        "show",
        help="查看当前生效的 profile。",
        exit_on_error=False,
    )
    _add_profile_fields(profile_show_parser)
    profile_show_parser.add_argument(
        "--format",
        choices=OUTPUT_FORMATS,
        default="text",
        help="输出格式，json 为机器权威接口。",
    )

    profile_set_parser = profile_subparsers.add_parser(
        "set",
        help="更新保存到配置文件中的 profile。",
        exit_on_error=False,
    )
    _add_profile_fields(profile_set_parser)
    profile_set_parser.add_argument(
        "--format",
        choices=OUTPUT_FORMATS,
        default="text",
        help="输出格式，json 为机器权威接口。",
    )

    watchlist_parser = subparsers.add_parser(
        "watchlist",
        help="管理个人关注列表。",
        exit_on_error=False,
    )
    watchlist_subparsers = watchlist_parser.add_subparsers(dest="watchlist_action", required=True)

    watchlist_list_parser = watchlist_subparsers.add_parser(
        "list",
        help="列出 watchlist。",
        exit_on_error=False,
    )
    watchlist_list_parser.add_argument(
        "--format",
        choices=OUTPUT_FORMATS,
        default="text",
        help="输出格式，json 为机器权威接口。",
    )

    watchlist_add_parser = watchlist_subparsers.add_parser(
        "add",
        help="向 watchlist 添加一个或多个标的。",
        exit_on_error=False,
    )
    watchlist_add_parser.add_argument("symbols", nargs="+", help="一个或多个 IPO 股票代码。")
    watchlist_add_parser.add_argument(
        "--format",
        choices=OUTPUT_FORMATS,
        default="text",
        help="输出格式，json 为机器权威接口。",
    )

    watchlist_remove_parser = watchlist_subparsers.add_parser(
        "remove",
        help="从 watchlist 移除一个或多个标的。",
        exit_on_error=False,
    )
    watchlist_remove_parser.add_argument("symbols", nargs="+", help="一个或多个 IPO 股票代码。")
    watchlist_remove_parser.add_argument(
        "--format",
        choices=OUTPUT_FORMATS,
        default="text",
        help="输出格式，json 为机器权威接口。",
    )

    params_parser = subparsers.add_parser(
        "params",
        help="管理评分参数版本并比较同一标的在不同参数集下的差异。",
        exit_on_error=False,
    )
    params_subparsers = params_parser.add_subparsers(dest="params_action", required=True)

    params_save_parser = params_subparsers.add_parser(
        "save",
        help="保存一组评分参数并生成新版本。",
        exit_on_error=False,
    )
    params_save_parser.add_argument("--name", required=True, help="参数集名称。")
    _add_parameter_fields(params_save_parser)
    params_save_parser.add_argument("--notes", help="可选说明。")
    params_save_parser.add_argument(
        "--activate",
        action="store_true",
        help="保存后立刻切换为 active version。",
    )
    params_save_parser.add_argument(
        "--format",
        choices=OUTPUT_FORMATS,
        default="text",
        help="输出格式，json 为机器权威接口。",
    )

    params_list_parser = params_subparsers.add_parser(
        "list",
        help="列出所有参数版本。",
        exit_on_error=False,
    )
    params_list_parser.add_argument(
        "--format",
        choices=OUTPUT_FORMATS,
        default="text",
        help="输出格式，json 为机器权威接口。",
    )

    params_show_parser = params_subparsers.add_parser(
        "show",
        help="查看指定参数版本；不传版本时默认显示 active version。",
        exit_on_error=False,
    )
    params_show_parser.add_argument("version", nargs="?", help="参数版本 ID。")
    params_show_parser.add_argument(
        "--format",
        choices=OUTPUT_FORMATS,
        default="text",
        help="输出格式，json 为机器权威接口。",
    )

    params_use_parser = params_subparsers.add_parser(
        "use",
        help="切换 active 参数版本。",
        exit_on_error=False,
    )
    params_use_parser.add_argument("version", help="目标参数版本 ID。")
    params_use_parser.add_argument(
        "--format",
        choices=OUTPUT_FORMATS,
        default="text",
        help="输出格式，json 为机器权威接口。",
    )

    params_compare_parser = params_subparsers.add_parser(
        "compare",
        help="比较同一标的在两个参数版本下的评分差异。",
        exit_on_error=False,
    )
    params_compare_parser.add_argument("symbol", help="IPO 股票代码。")
    params_compare_parser.add_argument("baseline_version", help="基线参数版本 ID。")
    params_compare_parser.add_argument("candidate_version", help="候选参数版本 ID。")
    _add_compare_profile_fields(params_compare_parser)
    params_compare_parser.add_argument(
        "--format",
        choices=OUTPUT_FORMATS,
        default="text",
        help="输出格式，json 为机器权威接口。",
    )

    score_parser = subparsers.add_parser(
        "score",
        help="对单个 IPO 生成评分、建议动作和可解释拆解。",
        exit_on_error=False,
    )
    score_parser.add_argument("symbol", help="IPO 股票代码。")
    score_parser.add_argument("--parameter-version", help="显式指定参数版本；默认使用 active version。")
    _add_compare_profile_fields(score_parser)
    score_parser.add_argument(
        "--format",
        choices=OUTPUT_FORMATS,
        default=None,
        help="输出格式；未指定时默认沿用 profile 的默认输出格式。",
    )

    decision_card_parser = subparsers.add_parser(
        "decision-card",
        help="输出单标的决策卡。",
        exit_on_error=False,
    )
    decision_card_parser.add_argument("symbol", help="IPO 股票代码。")
    decision_card_parser.add_argument("--parameter-version", help="显式指定参数版本；默认使用 active version。")
    _add_compare_profile_fields(decision_card_parser)
    decision_card_parser.add_argument(
        "--format",
        choices=OUTPUT_FORMATS,
        default=None,
        help="输出格式；未指定时默认沿用 profile 的默认输出格式。",
    )

    batch_parser = subparsers.add_parser(
        "batch",
        help="批量输出多个标的的决策卡结果。",
        exit_on_error=False,
    )
    batch_parser.add_argument("symbols", nargs="*", help="一个或多个 IPO 股票代码。")
    batch_parser.add_argument(
        "--watchlist",
        action="store_true",
        help="把当前 watchlist 中的标的一并作为批处理输入。",
    )
    batch_parser.add_argument("--parameter-version", help="显式指定参数版本；默认使用 active version。")
    _add_compare_profile_fields(batch_parser)
    batch_parser.add_argument(
        "--format",
        choices=OUTPUT_FORMATS,
        default=None,
        help="输出格式；未指定时默认沿用 profile 的默认输出格式。",
    )

    review_parser = subparsers.add_parser(
        "review",
        help="查看或导出复盘历史数据。",
        exit_on_error=False,
    )
    review_subparsers = review_parser.add_subparsers(dest="review_action", required=True)

    review_list_parser = review_subparsers.add_parser(
        "list",
        help="查看已保存的复盘历史记录。",
        exit_on_error=False,
    )
    review_list_parser.add_argument("--from", dest="from_date", help="起始日期或时间（ISO-8601）。")
    review_list_parser.add_argument("--to", dest="to_date", help="结束日期或时间（ISO-8601）。")
    review_list_parser.add_argument("--limit", type=_positive_int, default=20, help="返回记录数量上限。")
    review_list_parser.add_argument(
        "--format",
        choices=OUTPUT_FORMATS,
        default="text",
        help="输出格式，json 为机器权威接口。",
    )

    review_export_parser = review_subparsers.add_parser(
        "export",
        help="导出复盘数据集供后续分析或 OpenClaw 使用。",
        exit_on_error=False,
    )
    review_export_parser.add_argument("--from", dest="from_date", help="起始日期或时间（ISO-8601）。")
    review_export_parser.add_argument("--to", dest="to_date", help="结束日期或时间（ISO-8601）。")
    review_export_parser.add_argument("--limit", type=_positive_int, help="导出记录数量上限。")
    review_export_parser.add_argument("--output", help="导出的 JSON 数据集路径。")
    review_export_parser.add_argument(
        "--format",
        choices=OUTPUT_FORMATS,
        default="text",
        help="stdout 渲染格式，json 为机器权威接口。",
    )

    review_show_parser = review_subparsers.add_parser(
        "show",
        help="查看单条复盘记录的预测、实际与追溯历史。",
        exit_on_error=False,
    )
    review_show_parser.add_argument("record_id", help="复盘记录 ID。")
    review_show_parser.add_argument(
        "--format",
        choices=OUTPUT_FORMATS,
        default="text",
        help="输出格式，json 为机器权威接口。",
    )

    review_update_parser = review_subparsers.add_parser(
        "update",
        help="补录实际结果与偏差说明。",
        exit_on_error=False,
    )
    review_update_parser.add_argument("record_id", help="复盘记录 ID。")
    review_update_parser.add_argument("--allocated-lots", type=int, help="实际分配手数。")
    review_update_parser.add_argument("--listing-return-pct", type=float, help="上市首日收益率（%%）。")
    review_update_parser.add_argument("--exit-return-pct", type=float, help="实际退出收益率（%%）。")
    review_update_parser.add_argument("--realized-pnl-hkd", type=float, help="实际盈亏（HKD）。")
    review_update_parser.add_argument("--exited-at", help="实际退出时间（ISO-8601）。")
    review_update_parser.add_argument("--notes", help="实际结果备注。")
    review_update_parser.add_argument("--variance-note", help="偏差说明。")
    review_update_parser.add_argument(
        "--format",
        choices=OUTPUT_FORMATS,
        default="text",
        help="输出格式，json 为机器权威接口。",
    )

    review_import_suggestions_parser = review_subparsers.add_parser(
        "import-suggestions",
        help="导入 OpenClaw 返回的 suggestions 文件。",
        exit_on_error=False,
    )
    review_import_suggestions_parser.add_argument("input", help="OpenClaw suggestions JSON 文件路径。")
    review_import_suggestions_parser.add_argument(
        "--format",
        choices=OUTPUT_FORMATS,
        default="text",
        help="输出格式，json 为机器权威接口。",
    )

    review_suggestions_parser = review_subparsers.add_parser(
        "suggestions",
        help="查看已导入的 OpenClaw suggestions。",
        exit_on_error=False,
    )
    review_suggestions_parser.add_argument("--record-id", help="按 record_id 过滤。")
    review_suggestions_parser.add_argument("--batch-id", help="按 batch_id 过滤。")
    review_suggestions_parser.add_argument(
        "--status",
        choices=("pending", "accepted", "rejected", "applied"),
        help="按 suggestion 状态过滤。",
    )
    review_suggestions_parser.add_argument(
        "--format",
        choices=OUTPUT_FORMATS,
        default="text",
        help="输出格式，json 为机器权威接口。",
    )

    apply_parser = subparsers.add_parser(
        "apply-suggestions",
        help="查看并接受或拒绝 OpenClaw suggestions。",
        exit_on_error=False,
    )
    apply_subparsers = apply_parser.add_subparsers(dest="apply_action", required=True)

    apply_show_parser = apply_subparsers.add_parser(
        "show",
        help="查看 suggestion 与当前参数的差异。",
        exit_on_error=False,
    )
    apply_show_parser.add_argument("suggestion_id", help="suggestion ID。")
    apply_show_parser.add_argument(
        "--format",
        choices=OUTPUT_FORMATS,
        default="text",
        help="输出格式，json 为机器权威接口。",
    )

    apply_accept_parser = apply_subparsers.add_parser(
        "accept",
        help="接受 suggestion 并在需要时创建新参数版本。",
        exit_on_error=False,
    )
    apply_accept_parser.add_argument("suggestion_id", help="suggestion ID。")
    apply_accept_parser.add_argument("--reason", help="可选：采纳说明。")
    apply_accept_parser.add_argument(
        "--format",
        choices=OUTPUT_FORMATS,
        default="text",
        help="输出格式，json 为机器权威接口。",
    )

    apply_reject_parser = apply_subparsers.add_parser(
        "reject",
        help="拒绝 suggestion 并记录决策。",
        exit_on_error=False,
    )
    apply_reject_parser.add_argument("suggestion_id", help="suggestion ID。")
    apply_reject_parser.add_argument("--reason", help="可选：拒绝说明。")
    apply_reject_parser.add_argument(
        "--format",
        choices=OUTPUT_FORMATS,
        default="text",
        help="输出格式，json 为机器权威接口。",
    )

    return parser


def _add_profile_fields(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--risk-profile",
        choices=("conservative", "balanced", "aggressive"),
        help="风险偏好。",
    )
    parser.add_argument(
        "--default-output-format",
        choices=OUTPUT_FORMATS,
        help="后续评分/决策命令默认输出格式。",
    )
    parser.add_argument(
        "--max-budget-hkd",
        type=float,
        help="默认预算上限（HKD）。",
    )
    parser.add_argument(
        "--financing-preference",
        choices=("cash", "margin", "auto"),
        help="默认融资偏好。",
    )


def _add_compare_profile_fields(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--risk-profile",
        choices=("conservative", "balanced", "aggressive"),
        help="用于 compare 的风险偏好覆盖。",
    )
    parser.add_argument(
        "--max-budget-hkd",
        type=float,
        help="用于 compare 的预算上限覆盖。",
    )
    parser.add_argument(
        "--financing-preference",
        choices=("cash", "margin", "auto"),
        help="用于 compare 的融资偏好覆盖。",
    )


def _add_parameter_fields(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--snapshot-quality-weight", type=float, help="快照质量权重。")
    parser.add_argument("--affordability-weight", type=float, help="预算承受度权重。")
    parser.add_argument("--pricing-stability-weight", type=float, help="发行区间稳定性权重。")
    parser.add_argument("--sponsor-support-weight", type=float, help="保荐人支持因子权重。")
    parser.add_argument("--cost-efficiency-weight", type=float, help="成本效率因子权重。")
    parser.add_argument("--participate-min", type=float, help="建议参与的最低分阈值。")
    parser.add_argument("--cautious-min", type=float, help="建议谨慎参与的最低分阈值。")
    parser.add_argument("--handling-fee-hkd", type=float, help="单次固定手续费（HKD）。")
    parser.add_argument("--financing-rate-annual-pct", type=float, help="融资年化成本（%%）。")
    parser.add_argument(
        "--cash-opportunity-rate-annual-pct",
        type=float,
        help="资金占用机会成本年化（%%）。",
    )
    parser.add_argument("--lockup-days", type=int, help="预计锁资天数。")


def _extract_format(argv: Sequence[str]) -> str:
    for index, value in enumerate(argv):
        if value == "--format" and index + 1 < len(argv):
            return argv[index + 1]
    return "text"


def _positive_int(value: str) -> int:
    parsed = int(value)
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed


def _render_argument_error(message: str, output_format: str, stdout: TextIO, stderr: TextIO) -> int:
    run_context = RunContext.create()
    error = AppError.arg(
        "命令参数无效。",
        details={"reason": message},
    )
    response = build_error_response(error, run_context.meta(degraded=True, data_status="error"))
    if output_format == "json":
        print(render_model_as_json(response), file=stdout)
    elif output_format == "markdown":
        from hkipo_next.renderers.markdown_renderer import render_error_markdown

        print(render_error_markdown(response), file=stderr)
    else:
        print(render_error_response(response), file=stderr)
    return exit_code_for(error.code)


def main(
    argv: Sequence[str] | None = None,
    *,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
) -> int:
    args = list(argv if argv is not None else sys.argv[1:])
    stdout = stdout or sys.stdout
    stderr = stderr or sys.stderr
    parser = build_parser()

    if not args:
        parser.print_help(file=stdout)
        return 0

    output_format = _extract_format(args)

    try:
        namespace = parser.parse_args(args)
    except argparse.ArgumentError as exc:
        return _render_argument_error(str(exc), output_format, stdout, stderr)
    except SystemExit as exc:
        return int(exc.code)

    if namespace.command == "calendar":
        return execute_calendar(namespace, stdout=stdout, stderr=stderr)
    if namespace.command == "batch":
        return execute_batch(namespace, stdout=stdout, stderr=stderr)
    if namespace.command == "apply-suggestions":
        return execute_apply_suggestions(namespace, stdout=stdout, stderr=stderr)
    if namespace.command == "decision-card":
        return execute_decision_card(namespace, stdout=stdout, stderr=stderr)
    if namespace.command == "params":
        return execute_params(namespace, stdout=stdout, stderr=stderr)
    if namespace.command == "profile":
        return execute_profile(namespace, stdout=stdout, stderr=stderr)
    if namespace.command == "review":
        return execute_review(namespace, stdout=stdout, stderr=stderr)
    if namespace.command == "score":
        return execute_score(namespace, stdout=stdout, stderr=stderr)
    if namespace.command == "snapshot":
        return execute_snapshot(namespace, stdout=stdout, stderr=stderr)
    if namespace.command == "watchlist":
        return execute_watchlist(namespace, stdout=stdout, stderr=stderr)

    parser.print_help(file=stdout)
    return 0
