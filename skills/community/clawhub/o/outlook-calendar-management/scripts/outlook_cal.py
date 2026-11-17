#!/usr/bin/env python3
"""
Outlook 日历助手 — 在终端管理你的 Outlook 日历
手机、电脑、网页实时同步

用法:
  python outlook_cal.py status             查看连接状态
  python outlook_cal.py list --from 2026-09-07 --days 7
  python outlook_cal.py list --from 2026-09-09 --days 30
  python outlook_cal.py list --from 2026-08-10 --days 30   从指定日期开始查看
  python outlook_cal.py list --from 2026-09-07 --days 7 --summary
  python outlook_cal.py context --json     当前时间与时区（无需登录）
  python outlook_cal.py date --base 2026-09-07 --days 4 --json
  python outlook_cal.py add "聚餐" "2026-08-10 18:00" "2026-08-10 20:00"
  python outlook_cal.py add "生日" "2026-08-15" --all-day
  python outlook_cal.py add "周会" "2026-08-10 09:00" "2026-08-10 10:00" -l "3号会议室" -b "讨论Q3计划"
  python outlook_cal.py read <事件ID>
  python outlook_cal.py delete <事件ID>
  python outlook_cal.py next <事件ID>      定期系列的下次出现
  python outlook_cal.py free <日期> [--from HH:MM] [--to HH:MM] [--days N]   空闲时段
"""
import argparse, json, sys
from pathlib import Path

from ocal_errors import CalError
from ocal_i18n import t, set_lang
from ocal_bootstrap import ensure_deps, harden_stdio

# ── 入口 ──────────────────────────────────────────


def _argv_lang(argv):
    """在 argparse 正式解析前先捞一遍 --lang。

    帮助文本要按选定的语言渲染，所以得赶在 parser 构建之前定下来。

    :param argv: sys.argv 去掉脚本名之后的列表
    :return: --lang 的值；没给返回 None
    """
    for i, a in enumerate(argv):
        if a == "--lang" and i + 1 < len(argv):
            return argv[i + 1]
        if a.startswith("--lang="):
            return a.split("=", 1)[1]
    return None


def _json_requested(argv):
    """识别顶层/子命令的 --json，忽略 -- 之后作为普通值传入的内容。"""
    options = argv[:argv.index("--")] if "--" in argv else argv
    # argparse 默认接受无歧义缩写；非法的 --json=value 也应给出 JSON 参数错误。
    return any(arg.split("=", 1)[0] in ("--j", "--js", "--jso", "--json") for arg in options)


class _ArgumentParser(argparse.ArgumentParser):
    """让 --json 下的参数错误也使用统一错误对象；普通帮助/错误行为不变。"""

    def error(self, message):
        if _json_requested(sys.argv[1:]):
            raise CalError(message)
        super().error(message)


def main():
    """入口错误边界：包括参数解析和依赖启动失败。"""
    try:
        return _main()
    except CalError as e:
        if _json_requested(sys.argv[1:]):
            # ASCII 转义保留 Unicode 数据，避免 Windows 窄编码管道替换字符。
            print(json.dumps({"error": str(e), "exit": 1}, ensure_ascii=True))
            return 1
        raise


def _main():
    """命令入口：定语言 → 解析参数 → 按需装依赖 → 分发到各 cmd_*。

    :return: 进程退出码（0 正常，1 出错）
    """
    # 语言先于 argparse 生效：--lang > OCAL_LANG > 系统检测 > 默认 zh
    set_lang(_argv_lang(sys.argv[1:]))
    # 窄编码管道（Windows GBK）下 emoji 输出不崩（见 harden_stdio）
    harden_stdio()
    parser = _ArgumentParser(description=t("desc_main"), epilog=t("epilog"))
    # 全局 --json：顶层 + 各子命令均注册（argparse 顶层选项在子命令后不被识别，
    # 必须双注册；default=SUPPRESS 避免 Python 3.13+ 子 parser 默认值覆盖顶层已解析的值）
    parser.add_argument("--json", action="store_true", help=t("help_json"))
    parser.add_argument("--lang", choices=["zh", "en"], default=argparse.SUPPRESS, help=t("help_lang"))
    parser.add_argument("--timezone", default=argparse.SUPPRESS, help=t("help_timezone"))
    sub = parser.add_subparsers(dest="command")

    def _add_common(_p):
        """给子命令注册共用的 --json / --lang（default=SUPPRESS 避免覆盖顶层已解析值）。

        :param _p: 子命令的 argparse parser
        """
        _p.add_argument("--json", action="store_true", default=argparse.SUPPRESS,
                        help=t("help_json"))
        _p.add_argument("--lang", choices=["zh", "en"], default=argparse.SUPPRESS,
                        help=t("help_lang"))
        _p.add_argument("--timezone", default=argparse.SUPPRESS, help=t("help_timezone"))

    p_context = sub.add_parser("context", help=t("help_context"))
    _add_common(p_context)
    p_date = sub.add_parser("date", help=t("help_date"))
    _add_common(p_date)
    p_date.add_argument("--base", required=True, help=t("help_date_base"))
    p_date.add_argument("--days", type=int, required=True, help=t("help_date_days"))

    _p_status = sub.add_parser("status", help=t("help_status"))
    _add_common(_p_status)

    p_list = sub.add_parser("list", help=t("help_list"))
    _add_common(p_list)
    p_list.add_argument("--days", type=int, default=7, help=t("help_days"))
    p_list.add_argument("--search", help=t("help_search"))
    p_list.add_argument("--category", help=t("help_category"))
    p_list.add_argument("--from", dest="from_date", help=t("help_from"))
    p_list.add_argument("--created-after", dest="created_after", help=t("help_created_after"))
    p_list.add_argument("--created-before", dest="created_before", help=t("help_created_before"))
    p_list.add_argument("--reminders", action="store_true", help=t("help_reminders"))
    p_list.add_argument("--summary", action="store_true", help=t("help_summary"))

    p_add = sub.add_parser("add", help=t("help_add"))
    _add_common(p_add)
    p_add.add_argument("subject", help=t("help_subject"))
    p_add.add_argument("start", help=t("help_start"))
    p_add.add_argument("end", nargs="?", help=t("help_end"))
    p_add.add_argument("--all-day", action="store_true", help=t("help_all_day"))
    p_add.add_argument("-l", "--location", help=t("help_location"))
    p_add.add_argument("-b", "--body", help=t("help_body"))
    p_add.add_argument("--category", help=t("help_category_arg"))
    p_add.add_argument("--remind", type=int, help=t("help_remind"))
    add_repeat = p_add.add_mutually_exclusive_group()
    add_repeat.add_argument("--repeat", help=t("help_repeat"))
    add_repeat.add_argument("--repeat-file", help=t("help_repeat_file"))
    p_add.add_argument("--repeat-until", help=t("help_repeat_until"))
    p_add.add_argument("--repeat-times", type=int, help=t("help_repeat_times"))
    p_add.add_argument("--importance", choices=["低", "普通", "高", "low", "normal", "high"], help=t("help_importance"))
    p_add.add_argument("--private", action="store_true", help=t("help_private"))
    p_add.add_argument("--busy", choices=["free", "tentative", "busy", "oof", "workingElsewhere"], help=t("help_busy"))
    p_add.add_argument("--force", action="store_true", help=t("help_force"))

    p_update = sub.add_parser("update", help=t("help_update"))
    _add_common(p_update)
    p_update.add_argument("event_id", nargs="?", help=t("help_event_id"))
    p_update.add_argument("--search", help=t("help_search_target"))
    p_update.add_argument("--subject", help=t("help_new_subject"))
    p_update.add_argument("--start", help=t("help_new_start"))
    p_update.add_argument("--end", help=t("help_new_end"))
    p_update.add_argument("--all-day", dest="all_day", action="store_true", default=None, help=t("help_all_day_switch"))
    p_update.add_argument("--no-all-day", dest="all_day", action="store_false", help=t("help_no_all_day"))
    p_update.add_argument("-l", "--location", help=t("help_new_location"))
    p_update.add_argument("-b", "--body", help=t("help_new_body"))
    p_update.add_argument("--category", help=t("help_new_category"))
    p_update.add_argument("--importance", choices=["低", "普通", "高", "low", "normal", "high"], help=t("help_importance"))
    p_update.add_argument("--private", dest="private", action="store_true", default=None, help=t("help_private"))
    p_update.add_argument("--no-private", dest="private", action="store_false", help=t("help_no_private"))
    p_update.add_argument("--busy", choices=["free", "tentative", "busy", "oof", "workingElsewhere"], help=t("help_busy"))
    p_update.add_argument("--remind", type=int, help=t("help_remind"))
    p_update.add_argument("--no-remind", action="store_true", help=t("help_no_remind"))
    update_repeat = p_update.add_mutually_exclusive_group()
    update_repeat.add_argument("--repeat", help=t("help_repeat_update"))
    update_repeat.add_argument("--repeat-file", help=t("help_repeat_file"))
    p_update.add_argument("--repeat-until", help=t("help_repeat_until"))
    p_update.add_argument("--repeat-times", type=int, help=t("help_repeat_times"))
    p_update.add_argument("-y", "--yes", action="store_true", help=t("help_yes"))

    p_read = sub.add_parser("read", help=t("help_read"))
    _add_common(p_read)
    p_read.add_argument("event_id", help=t("help_event_id"))

    p_delete = sub.add_parser("delete", help=t("help_delete"))
    _add_common(p_delete)
    p_delete.add_argument("event_id", nargs="?", help=t("help_event_id"))
    p_delete.add_argument("--search", help=t("help_search_target"))
    p_delete.add_argument("-y", "--yes", action="store_true", help=t("help_yes_delete"))
    p_delete.add_argument("--series", action="store_true", help=t("help_series"))

    p_move = sub.add_parser("move", help=t("help_move"))
    _add_common(p_move)
    p_move.add_argument("event_id", nargs="?", help=t("help_event_id"))
    p_move.add_argument("--search", help=t("help_search_target"))
    p_move.add_argument("--days", type=int, help=t("help_move_days"))
    p_move.add_argument("--to", help=t("help_move_to"))
    p_move.add_argument("-y", "--yes", action="store_true", help=t("help_yes"))

    p_next = sub.add_parser("next", help=t("help_next"))
    _add_common(p_next)
    p_next.add_argument("event_id", help=t("help_event_id"))

    p_free = sub.add_parser("free", help=t("help_free"))
    _add_common(p_free)
    p_free.add_argument("date", help=t("help_free_date"))
    p_free.add_argument("--from", dest="from_time", help=t("help_free_from"))
    p_free.add_argument("--to", dest="to_time", help=t("help_free_to"))
    p_free.add_argument("--days", type=int, default=1, help=t("help_free_days"))

    args = parser.parse_args()
    # 子命令后出现 --lang 时以实际解析值为准（预扫已兜底，这里再确认一次）
    set_lang(getattr(args, 'lang', None))

    if args.command:
        repeat_file = getattr(args, "repeat_file", None)
        if repeat_file is not None:
            try:
                args.repeat = Path(repeat_file).read_text(encoding="utf-8-sig")
            except (OSError, UnicodeError) as exc:
                raise CalError(t("err_repeat_file", path=repeat_file, detail=exc)) from exc
            if not args.repeat.strip():
                raise CalError(t("err_repeat_json"))
        # 离线辅助命令和帮助不触发安装或登录；日历命令先装依赖再导入 Graph。
        if args.command not in ("context", "date"):
            try:
                ensure_deps()
            except SystemExit as e:
                if e.code and _json_requested(sys.argv[1:]):
                    raise CalError(t("deps_fail_code", code=e.code)) from e
                raise
        return _dispatch(args)
    if getattr(args, 'json', False):
        parser.error("a command is required")
    parser.print_help()
    return 0


def _dispatch(args):
    """Apply one explicit timezone consistently to parsing, API headers and output."""
    import ocal_time
    import ocal_context
    modules = [ocal_time]
    if args.command in ("context", "date"):
        command = getattr(ocal_context, "cmd_" + args.command)
    else:
        import ocal_events
        import ocal_graph
        import ocal_recurrence
        modules.extend([ocal_events, ocal_graph, ocal_recurrence])
        command = getattr(ocal_events, "cmd_" + args.command)
    zone = getattr(args, "timezone", None)
    name, tzinfo = (ocal_time.resolve_timezone(zone) if zone is not None
                    else (ocal_time.LOCAL_TZ_NAME, ocal_time.LOCAL_TZ))
    previous = []
    for module in modules:
        for attr, value in (("LOCAL_TZ", tzinfo), ("LOCAL_TZ_NAME", name)):
            if hasattr(module, attr):
                previous.append((module, attr, getattr(module, attr)))
                setattr(module, attr, value)
    try:
        return command(args)
    finally:
        for module, attr, value in previous:
            setattr(module, attr, value)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except CalError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)
