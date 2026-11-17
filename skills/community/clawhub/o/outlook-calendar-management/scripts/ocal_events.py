"""ocal_events — 命令实现：status/list/add/update/read/delete/move/next/free。"""
import html, re, json, sys, time
from datetime import datetime, timedelta
from urllib.parse import quote

from ocal_errors import CalError
from ocal_auth import get_token, TOKEN_PATH
from ocal_time import LOCAL_TZ, LOCAL_TZ_NAME, _parse_dt, _parse_dt_arg, _all_day_range, _fmt, _weekday, _local_time_exists, _shift_days
from ocal_graph import _call, _get_all
from ocal_recurrence import _build_recurrence, _fmt_recurrence, _occurrence_number
from ocal_i18n import t, d_md, date_weekday, all_day, join, range_sep, imp_name

# ── 命令实现 ──────────────────────────────────────

_EVENT_SELECT = "id,subject,start,end,location,categories,isAllDay,recurrence,seriesMasterId,type,isCancelled,bodyPreview"

# 邮箱首选时区缓存：全天日程用它写入，机器时区 ≠ 邮箱时区时 Outlook 里才不跨天。
# 每个进程只取一次；取不到（旧 token 无 MailboxSettings.Read / 网络问题）静默回退本机时区。
_mailbox_tz = {"name": None, "tried": False}


def _mailbox_tz_name(token):
    """取 Outlook 邮箱的首选时区名（全天日程写入用）；失败静默回退本机时区。

    老版本 token 只有 Calendars.ReadWrite 权限，GET /me/mailboxSettings 会 403，
    这时功能不阻断（按本机时区写，与旧版本行为一致）。

    :param token: 访问令牌
    :return: (时区名, 是否真的取到了邮箱时区)
    """
    if not _mailbox_tz["tried"]:
        _mailbox_tz["tried"] = True
        try:
            data = _call("GET", "/me/mailboxSettings?$select=timeZone", token)
            name = (data or {}).get("timeZone")
            if name:
                _mailbox_tz["name"] = name
        except CalError:
            pass  # 无权限/网络问题：回退本机时区
    return _mailbox_tz["name"] or LOCAL_TZ_NAME, bool(_mailbox_tz["name"])


def _event_date(ev):
    """Scheduled start date; all-day dates retain their calendar meaning."""
    s_tz = ev['start'].get('timeZone')
    if ev.get('isAllDay'):
        s, _ = _all_day_range(ev['start']['dateTime'], ev['end']['dateTime'])
        return s
    return _parse_dt(ev['start']['dateTime'], s_tz).date()


def _event_date_str(ev):
    """Format the scheduled start date for human output."""
    return date_weekday(_event_date(ev))


def _summary_counts(events):
    """Count each returned event once, grouped by its scheduled start date."""
    counts = {}
    for ev in events:
        day = _event_date(ev).isoformat()
        counts[day] = counts.get(day, 0) + 1
    return dict(sorted(counts.items()))


def _print_events(events, title, summary=False):
    """打印日程列表（list/next 共用的显示逻辑）。

    :param events: 要显示的事件列表
    :param title: 列表标题（如"接下来 7 天的安排"）
    :param summary: True 时只按天汇总条数，不显示明细
    """
    if not events:
        print(t("list_empty", title=title))
        return
    print(t("list_header", title=title))
    if summary:
        counts = {}
        for ev in events:
            d = _event_date_str(ev)
            counts[d] = counts.get(d, 0) + 1
        for d, n in counts.items():
            print(t("list_count", d=d, n=n))
        print()
        return
    last_date = ""
    for ev in events:
        s_tz = ev['start'].get('timeZone')
        e_tz = ev['end'].get('timeZone')
        is_all_day = ev.get('isAllDay', False)
        if is_all_day:
            s, e = _all_day_range(ev['start']['dateTime'], ev['end']['dateTime'])
            date_str = date_weekday(s)
            if e != s:
                date_str += f" {range_sep()} {d_md(e)}"
            time_str = all_day()
            icon = "📌"
        else:
            s_bj = _parse_dt(ev['start']['dateTime'], s_tz)
            date_str = date_weekday(s_bj)
            time_str = f"{_fmt(ev['start']['dateTime'], s_tz)} - {_fmt(ev['end']['dateTime'], e_tz)}"
            icon = "🕐"

        cats = ev.get('categories', [])
        cat_str = f" [{', '.join(cats)}]" if cats else ""

        # 定期事件标记：区分系列主事件 / 单次出现 / 例外 / 已取消
        rec_str = ""
        if ev.get('seriesMasterId'):
            if ev.get('isCancelled'):
                rec_str = t("rec_cancelled")
            elif ev.get('type') == 'exception':
                rec_str = t("rec_modified")
            else:
                rec_str = t("rec_series")
        elif ev.get('recurrence'):
            rec_str = f" 🔁{_fmt_recurrence(ev['recurrence'])}"

        if date_str != last_date:
            print(f"  {date_str}")
            last_date = date_str

        print(f"    {icon} {time_str}  {ev['subject']}{rec_str}{cat_str}")
        print(f"    🆔 {ev['id']}")
    print()


def _filter_events(events, search=None, category=None):
    """在本地按关键词或类别过滤事件（Graph 拉回来之后再做）。

    :param events: 事件列表
    :param search: 关键词，匹配标题/地点/备注（不区分大小写）
    :param category: 类别名，事件的 categories 里包含即算
    :return: 过滤后的事件列表
    """
    if search:
        search_l = search.lower()
        filtered = []
        for e in events:
            if search_l in (e.get('subject') or '').lower():
                filtered.append(e)
                continue
            loc = (e.get('location') or {}).get('displayName') or ''
            if search_l in loc.lower():
                filtered.append(e)
                continue
            if search_l in (e.get('bodyPreview') or '').lower():
                filtered.append(e)
        events = filtered
    if category:
        events = [e for e in events if category in e.get('categories', [])]
    return events


def _search_candidates(search, token):
    """按关键词在「过去 7 天 ~ 未来 30 天」窗口内搜索日程。

    供 update/move/delete 的 --search 定位使用：返回匹配事件列表，
    由调用方处理唯一匹配/多匹配/零匹配三种情形。

    :param search: 关键词（匹配标题/地点/备注，不区分大小写）
    :param token: 访问令牌
    :return: 匹配的事件列表
    """
    now = datetime.now(LOCAL_TZ)
    start = (now - timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0).isoformat(timespec="seconds")
    end = (now + timedelta(days=30)).replace(hour=23, minute=59, second=59, microsecond=0).isoformat(timespec="seconds")
    url = (f"/me/calendar/calendarView?startDateTime={quote(start, safe='')}&endDateTime={quote(end, safe='')}"
           f"&$select={_EVENT_SELECT}&$orderby=start/dateTime")
    events = _get_all(url, token, prefer_immutable=True)
    return _filter_events(events, search=search)


def _candidate_line(ev):
    """搜索多匹配时，错误信息中的候选行：{时间} {标题} 🆔 {ID}（供 agent 指定目标）。"""
    s_tz = ev['start'].get('timeZone')
    if ev.get('isAllDay'):
        time_str = all_day()
    else:
        time_str = _fmt(ev['start']['dateTime'], s_tz)
    return f"    {time_str}  {ev.get('subject', '')}  🆔 {ev['id']}"


def _resolve_target_id(args, token):
    """确定 update/move/delete 的目标事件 ID。

    给定 event_id 时直接使用；未给 event_id 但给了 --search 时，
    在「过去 7 天 ~ 未来 30 天」窗口内搜索定位：唯一匹配直接返回其 ID，
    零匹配 / 多匹配抛 CalError（多匹配时错误信息内列出候选的标题+时间+🆔）。
    ID 与 search 均缺失时抛 err_id_required。

    :param args: argparse 参数（event_id/search）
    :param token: 访问令牌
    :return: 事件 ID
    :raises CalError: ID 与 search 均缺失 / 搜索零匹配 / 搜索多匹配
    """
    if args.event_id:
        return args.event_id
    search = getattr(args, 'search', None)
    if not search:
        raise CalError(t("err_id_required"))
    matches = _search_candidates(search, token)
    if not matches:
        raise CalError(t("err_search_none", s=search))
    if len(matches) > 1:
        lines = "\n".join(_candidate_line(e) for e in matches)
        raise CalError(t("err_search_multi", s=search, list=lines))
    return matches[0]["id"]


_IMPORTANCE_MAP = {"低": "low", "普通": "normal", "高": "high"}


def _parse_importance(v):
    """把命令行的重要度值归一成 Graph 的 importance。

    用户既可能输"高"也可能输"high"，这里统一映射；其余值原样返回（交给 argparse 兜底）。

    :param v: 用户输入的重要度
    :return: Graph 用的 low/normal/high
    """
    return _IMPORTANCE_MAP.get(v, v)



def cmd_status(args):
    """查看连接状态：是否已认证、当前账户、登录剩余有效期。

    :param args: argparse 参数（json 决定输出 JSON 还是人类文案）
    :return: 0 正常；1 未连接或 API 异常
    """
    is_json = getattr(args, 'json', False)

    def _expires_left():
        """估一下 token 还剩多少秒有效；文件读不了就当不知道，返回 None。"""
        try:
            with open(TOKEN_PATH, 'r', encoding='utf-8') as f:
                tok = json.load(f)
            exp = tok.get('expires_at', 0)
            if exp:
                return exp - time.time()
        except Exception:
            pass
        return None

    token = get_token()
    if not token:
        if is_json:
            print(json.dumps({"connected": False, "account": None, "expires_in_seconds": None},
                             ensure_ascii=True))
            return 1
        print(t("status_not_connected"))
        print(t("status_run_setup"))
        return 1
    try:
        data = _call("GET", "/me/calendar", token)
    except CalError as e:
        if is_json:
            print(json.dumps({"connected": False, "account": None,
                              "expires_in_seconds": _expires_left()}, ensure_ascii=True))
            return 1
        print(t("status_api_error", e=e))
        return 1
    account = data.get('owner', {}).get('address', data.get('name', ''))
    exp_left = _expires_left()
    today = datetime.now(LOCAL_TZ).date()
    if is_json:
        print(json.dumps({"connected": True, "account": account, "expires_in_seconds": exp_left,
                          "today": today.strftime("%Y-%m-%d")}, ensure_ascii=True))
        return 0
    print(t("status_connected"))
    print(f"   {account}")
    # 当前日期是 agent 换算相对时间（今天/明天）的基准，status 直接给出来
    print(t("status_today", d=date_weekday(today, with_year=True)))
    mtz, mtz_ok = _mailbox_tz_name(token)
    if mtz_ok and mtz != LOCAL_TZ_NAME:
        print(t("status_mailbox_tz", tz=mtz))
    if exp_left is not None:
        if exp_left > 0:
            print(t("status_expiry", h=int(exp_left // 3600), m=int((exp_left % 3600) // 60)))
        else:
            print(t("status_expired_auto"))
    return 0


def cmd_list(args):
    """查询明确的日程日期窗口或创建时间窗口。

    :param args: argparse 参数（days/search/category/summary/from/created-after/created-before/reminders/json）
    :return: 0 成功
    """
    is_json = getattr(args, 'json', False)
    days = getattr(args, 'days', 7)
    if isinstance(days, bool) or not isinstance(days, int) or days < 1:
        raise CalError(t("err_days_min"))
    search = getattr(args, 'search', None)
    category = getattr(args, 'category', None)
    summary = bool(getattr(args, 'summary', False))
    from_date = getattr(args, 'from_date', None)
    created_after = getattr(args, 'created_after', None)
    created_before = getattr(args, 'created_before', None)
    reminders_only = bool(getattr(args, 'reminders', False))
    if (from_date is None) == (created_after is None) or (created_before is not None and created_after is None):
        raise CalError(t("err_list_range"))
    if created_after is not None:
        ca = _parse_dt_arg(created_after, date_only=True).replace(tzinfo=LOCAL_TZ)
        filters = "createdDateTime ge " + ca.isoformat(timespec="seconds")
        if created_before is not None:
            cb = _parse_dt_arg(created_before, date_only=True).replace(tzinfo=LOCAL_TZ)
            if cb <= ca:
                raise CalError(t("err_end_after_start"))
            filters += " and createdDateTime lt " + cb.isoformat(timespec="seconds")
        url = (f"/me/events?$filter={quote(filters, safe='')}"
               f"&$select={_EVENT_SELECT},createdDateTime,reminderMinutesBeforeStart,isReminderOn"
               f"&$orderby=createdDateTime desc")
        title = t("title_created", d=ca.strftime('%Y-%m-%d'))
    else:
        fd = _parse_dt_arg(from_date, date_only=True).replace(tzinfo=LOCAL_TZ)
        try:
            stop = fd + timedelta(days=days)
        except OverflowError as exc:
            raise CalError(t("err_date_offset")) from exc
        start = fd.isoformat(timespec="seconds")
        end = stop.isoformat(timespec="seconds")
        title = t("title_from", d=fd.strftime('%Y-%m-%d'), n=days)
        url = (f"/me/calendar/calendarView?startDateTime={quote(start, safe='')}&endDateTime={quote(end, safe='')}"
               f"&$select={_EVENT_SELECT},reminderMinutesBeforeStart,isReminderOn&$orderby=start/dateTime")
    token = get_token()
    if not token:
        raise CalError(t("err_auth_first"))
    events = _get_all(url, token, prefer_immutable=True)

    # 本地筛选
    filtered = _filter_events(events, search, category)
    if reminders_only:
        # 只看设了提醒的日程（isReminderOn 为 True 且设置了提醒时间）
        filtered = [e for e in filtered if e.get('isReminderOn') and e.get('reminderMinutesBeforeStart') is not None]
        title += t("suffix_reminders")

    if is_json:
        # 明细数组或明确请求的按开始日期汇总，均跳过人类展示。
        result = _summary_counts(filtered) if summary else filtered
        print(json.dumps(result, ensure_ascii=True))
        return 0

    if search or category:
        conds = []
        if search:
            conds.append(t("filter_contains", s=search))
        if category:
            conds.append(t("filter_category", c=category))
        title += t("filter_suffix", c=t("filter_join").join(conds))
        if not filtered:
            print(t("list_no_match", n=len(events), title=title))
            return 0

    _print_events(filtered, title, summary=summary)
    return 0


def _parse_timed_arg(value):
    result = _parse_dt_arg(value)
    if len(value) == 10:
        raise CalError(t("err_timed_bounds"))
    return result


def _validate_wall_times(*dts):
    """Reject nonexistent or ambiguous local instants instead of asking Graph to guess."""
    for dt in dts:
        if dt is None:
            continue
        values = {"value": dt.strftime("%Y-%m-%d %H:%M"), "zone": LOCAL_TZ_NAME}
        if not _local_time_exists(dt, LOCAL_TZ):
            raise CalError(t("err_dst_nonexistent", **values))
        if dt.replace(tzinfo=LOCAL_TZ, fold=0).utcoffset() != dt.replace(tzinfo=LOCAL_TZ, fold=1).utcoffset():
            raise CalError(t("err_dst_ambiguous", **values))


def _overlaps(a_s, a_e, b_s, b_e):
    """两个时段有没有重叠（naive datetime；只是首尾相接不算）。

    :param a_s: 时段 a 的开始
    :param a_e: 时段 a 的结束
    :param b_s: 时段 b 的开始
    :param b_e: 时段 b 的结束
    :return: True 有重叠
    """
    return a_s < b_e and b_s < a_e


def _check_conflicts(token, start_dt, end_dt, all_day):
    """查新日程会跟哪些现有日程重叠（add 时非 --force 调用）。

    查询窗口：时段事件前后各扩 1 小时，全天事件查整个日期段
    （多天全天查全程，含第 2 天起的每一天）。
    showAs=free 与已取消的单次不算占用；calendarView 返回窗口内的全部出现，
    所以定期系列落在窗口内的每次出现都会按实际时间检查。

    :param token: 访问令牌
    :param start_dt: 新日程开始（naive）
    :param end_dt: 新日程结束（naive；全天时是末日次日 00:00）
    :param all_day: 新日程是否全天
    :return: [(事件, 占用开始, 占用结束, 是否系列), ...]
    """
    if all_day:
        q_start = start_dt.replace(hour=0, minute=0, second=0, microsecond=0)
        q_end = end_dt.replace(hour=0, minute=0, second=0, microsecond=0)
        if q_end <= q_start:
            q_end = q_start + timedelta(days=1)  # 防御异常数据
    else:
        q_start = start_dt - timedelta(hours=1)
        q_end = end_dt + timedelta(hours=1)
    start_iso = q_start.replace(tzinfo=LOCAL_TZ).isoformat(timespec="seconds")
    end_iso = q_end.replace(tzinfo=LOCAL_TZ).isoformat(timespec="seconds")
    url = (f"/me/calendar/calendarView?startDateTime={quote(start_iso, safe='')}&endDateTime={quote(end_iso, safe='')}"
           f"&$select={_EVENT_SELECT},showAs&$orderby=start/dateTime")
    events = _get_all(url, token, prefer_immutable=True)
    result = []
    for ev in events:
        if ev.get('showAs') == 'free':
            continue  # 标记为 free 的不算占用
        if ev.get('isCancelled'):
            continue  # 定期系列已取消的单次不算占用（calendarView 会返回它们）
        if ev.get('isAllDay'):
            s, e = _all_day_range(ev['start']['dateTime'], ev['end']['dateTime'])
            b_s = datetime.combine(s, datetime.min.time())
            b_e = b_s + timedelta(days=(e - s).days + 1)
        else:
            b_s = _parse_dt(ev['start']['dateTime'], ev['start'].get('timeZone')).replace(tzinfo=None)
            b_e = _parse_dt(ev['end']['dateTime'], ev['end'].get('timeZone')).replace(tzinfo=None)
        is_series = bool(ev.get('recurrence') or ev.get('seriesMasterId'))
        if _overlaps(start_dt, end_dt, b_s, b_e):
            result.append((ev, b_s, b_e, is_series))
    return result


def cmd_add(args):
    """新建日程（会议/生日/提醒/定期），默认检查重叠（--force 跳过）。

    :param args: argparse 参数（subject/start/end/all-day/location/body/category/remind/repeat/...）
    :return: 0 成功
    """
    is_json = getattr(args, 'json', False)

    if args.all_day:
        start_dt = _parse_dt_arg(args.start, date_only=True)
        if args.end is not None:
            # 多天全天：结束给日期（含当天），Graph 的 end 存次日 00:00
            end_dt = _shift_days(_parse_dt_arg(args.end, date_only=True), 1)
            if end_dt <= start_dt:
                raise CalError(t("err_end_after_start"))
            time_desc = f"{d_md(start_dt)} {range_sep()} {d_md(end_dt.date() - timedelta(days=1))} {all_day()}"
        else:
            end_dt = _shift_days(start_dt, 1)
            time_desc = f"{d_md(start_dt)} {all_day()}"
        event_data = {
            "subject": args.subject,
            "start": {"dateTime": start_dt.isoformat(timespec="seconds"), "timeZone": LOCAL_TZ_NAME},
            "end": {"dateTime": end_dt.isoformat(timespec="seconds"), "timeZone": LOCAL_TZ_NAME},
            "isAllDay": True,
        }
    else:
        start_dt = _parse_timed_arg(args.start)
        if args.end is not None:
            end_dt = _parse_timed_arg(args.end)
        else:
            raise CalError(t("err_timed_bounds"))
        if end_dt <= start_dt:
            raise CalError(t("err_end_after_start"))
        event_data = {
            "subject": args.subject,
            "start": {"dateTime": start_dt.isoformat(timespec="seconds"), "timeZone": LOCAL_TZ_NAME},
            "end": {"dateTime": end_dt.isoformat(timespec="seconds"), "timeZone": LOCAL_TZ_NAME},
        }
        time_desc = f"{d_md(start_dt)} {start_dt.strftime('%H:%M')} - {end_dt.strftime('%H:%M')}"
        _validate_wall_times(start_dt, end_dt)

    if args.location:
        event_data["location"] = {"displayName": args.location}
    if args.body:
        event_data["body"] = {"contentType": "text", "content": args.body}
    if args.category:
        event_data["categories"] = [c.strip() for c in args.category.split(",") if c.strip()]
    if args.importance:
        imp = _parse_importance(args.importance)
        if imp in ("low", "normal", "high"):
            event_data["importance"] = imp
    if args.private:
        event_data["sensitivity"] = "private"
    if args.busy:
        event_data["showAs"] = args.busy

    # 定期事件
    recurrence_desc = ""
    if args.repeat is not None:
        recurrence, recurrence_desc = _build_recurrence(args.repeat, args.repeat_until, args.repeat_times, start_dt)
        recurrence["range"]["recurrenceTimeZone"] = event_data["start"]["timeZone"]
        event_data["recurrence"] = recurrence
    elif args.repeat_until is not None or args.repeat_times is not None:
        raise CalError(t("err_repeat_until"))

    if args.remind is not None:
        if args.remind < 0:
            raise CalError(t("err_remind_negative"))
        if args.all_day:
            # 全天事件：提醒按分钟数（天数 × 1440），上限 2629800 分钟（约 5 年）
            minutes = args.remind * 1440
            if minutes > 2629800:
                raise CalError(t("err_allday_remind_max", n=2629800 // 1440, m=args.remind))
            event_data["reminderMinutesBeforeStart"] = minutes
            remind_desc = t("remind_days", n=args.remind)
        else:
            event_data["reminderMinutesBeforeStart"] = args.remind
            remind_desc = t("remind_minutes", n=args.remind)
        # 显式打开提醒开关：只给分钟数在个别邮箱默认关闭提醒时不会生效
        event_data["isReminderOn"] = True

    token = get_token()
    if not token:
        raise CalError(t("err_auth_first"))
    if args.all_day:
        # 参数校验完再读取邮箱时区，全天边界和重复规则使用同一时区。
        all_day_tz, _ = _mailbox_tz_name(token)
        event_data["start"]["timeZone"] = event_data["end"]["timeZone"] = all_day_tz
        if "recurrence" in event_data:
            event_data["recurrence"]["range"]["recurrenceTimeZone"] = all_day_tz

    # 冲突检测：--force 跳过；只提示不阻断。
    # 警告一律走 stderr：冲突列表里带现有事件的 🆔 行，进 stdout 会让
    # agent 分不清哪个 🆔 是新日程（拿错 ID 会改/删错日程）
    if not getattr(args, 'force', False):
        overlaps = _check_conflicts(token, start_dt, end_dt, args.all_day)
        if overlaps:
            print(t("conflict_header"), file=sys.stderr)
            for ev, _, _, _is_series in overlaps:
                if ev.get('isAllDay'):
                    s, e = _all_day_range(ev['start']['dateTime'], ev['end']['dateTime'])
                    t_str = f"{d_md(s)} {all_day()}"
                    if e != s:
                        t_str += f" {range_sep()} {d_md(e)}"
                else:
                    t_str = f"{_fmt(ev['start']['dateTime'], ev['start'].get('timeZone'))} - {_fmt(ev['end']['dateTime'], ev['end'].get('timeZone'))}"
                print(f"   {ev['subject']}  {t_str}  🆔 {ev['id']}", file=sys.stderr)
            print(file=sys.stderr)

    result = _call("POST", "/me/events", token, event_data, prefer_immutable=True)
    if is_json:
        print(json.dumps(result, ensure_ascii=True))
        return 0
    print(t("add_success"))
    print(f"   {result['subject']}")
    print(f"   🆔 {result['id']}")
    print(f"   {time_desc}")
    if recurrence_desc:
        print(f"   🔁 {recurrence_desc}")
    if args.category:
        print(f"   🏷️ {result.get('categories', [])}")
    if args.remind is not None:
        print(f"   ⏰ {remind_desc}")
    if args.importance:
        print(t("importance_line", v=args.importance))
    if args.private:
        print(t("private_line"))
    if args.busy:
        print(t("showas_line", v=args.busy))
    if args.location:
        print(f"   📍 {args.location}")
    if args.body:
        print(f"   📝 {args.body}")
    print()
    return 0


def cmd_update(args):
    """更新已有日程：标题/时间/地点/备注/类别/重要度/私密/忙闲/提醒/重复规则，支持全天<->时段互转。

    :param args: argparse 参数（event_id + 各 --xx 字段；-y 跳过确认）
    :return: 0 成功；1 没有可改的字段或用户取消
    """
    is_json = getattr(args, 'json', False)
    token = get_token()
    if not token:
        raise CalError(t("err_auth_first"))
    event_id = _resolve_target_id(args, token)

    # 读取原事件
    data = _call("GET", f"/me/events/{quote(event_id, safe='')}", token, prefer_immutable=True)
    was_all_day = data.get('isAllDay', False)

    # 收集要修改的字段
    changes = []
    patch = {}

    if args.subject is not None:
        patch["subject"] = args.subject
        changes.append(t("ch_subject"))

    if args.all_day is not None:
        # --all-day / --no-all-day 显式切换类型
        target_all_day = args.all_day
    else:
        target_all_day = was_all_day

    if target_all_day != was_all_day and (not args.start or not args.end):
        raise CalError(t("err_convert_bounds"))

    new_start_date = None  # --repeat 同命令改 --start 时，range.startDate 必须用新日期
    if args.start is not None or args.end is not None or args.all_day is not None:
        if target_all_day:
            # 全天：start 是日期（原全天事件的日期按 naive 日期段取，避免 UTC 换算错一天）
            if args.start is not None:
                start_dt = _parse_dt_arg(args.start, date_only=True)
            else:
                start_dt = datetime.strptime(data['start']['dateTime'][:10], "%Y-%m-%d")
            if args.end is not None:
                # 多天全天：结束给日期（含当天），Graph 的 end 存次日 00:00
                end_dt = _shift_days(_parse_dt_arg(args.end, date_only=True), 1)
                if end_dt <= start_dt:
                    raise CalError(t("err_end_after_start"))
            else:
                end_dt = datetime.strptime(data['end']['dateTime'][:10], "%Y-%m-%d")
            if end_dt <= start_dt:
                raise CalError(t("err_end_after_start"))
            # 全天日程按邮箱首选时区写入（机器时区 ≠ 邮箱时区时不跨天；取不到回退本机）
            all_day_tz, _ = _mailbox_tz_name(token)
            patch["start"] = {"dateTime": start_dt.strftime("%Y-%m-%dT00:00:00"), "timeZone": all_day_tz}
            patch["end"] = {"dateTime": end_dt.strftime("%Y-%m-%dT00:00:00"), "timeZone": all_day_tz}
            patch["isAllDay"] = True
            changes.append(t("ch_allday_date"))
            new_start_date = start_dt.date()
        else:
            # 时段：start/end 是 "日期 时间"
            if args.start is not None:
                start_dt = _parse_timed_arg(args.start)
            else:
                start_dt = _parse_dt(data['start']['dateTime'], data['start'].get('timeZone')).replace(tzinfo=None)
            if args.end is not None:
                end_dt = _parse_timed_arg(args.end)
            else:
                end_dt = _parse_dt(data['end']['dateTime'], data['end'].get('timeZone')).replace(tzinfo=None)
            if end_dt <= start_dt:
                raise CalError(t("err_end_after_start"))
            patch["start"] = {"dateTime": start_dt.strftime("%Y-%m-%dT%H:%M:%S"), "timeZone": LOCAL_TZ_NAME}
            patch["end"] = {"dateTime": end_dt.strftime("%Y-%m-%dT%H:%M:%S"), "timeZone": LOCAL_TZ_NAME}
            patch["isAllDay"] = False
            changes.append(t("ch_time"))
            new_start_date = start_dt.date()
            _validate_wall_times(start_dt, end_dt)

    if args.location is not None:
        patch["location"] = {"displayName": args.location}
        changes.append(t("ch_location"))
    if args.body is not None:
        patch["body"] = {"contentType": "text", "content": args.body}
        changes.append(t("ch_body"))

    # 类别（--category "" 清空）
    if args.category is not None:
        patch["categories"] = [c.strip() for c in args.category.split(",") if c.strip()]
        changes.append(t("ch_category"))

    # 重要度
    if args.importance:
        imp = _parse_importance(args.importance)
        if imp in ("low", "normal", "high"):
            patch["importance"] = imp
            changes.append(t("ch_importance"))

    # 私密（--private / --no-private 显式切换；均未给则不修改）
    if args.private is not None:
        patch["sensitivity"] = "private" if args.private else "normal"
        changes.append(t("ch_private"))

    # 忙闲
    if args.busy:
        patch["showAs"] = args.busy
        changes.append(t("ch_busy"))

    # 提醒（--no-remind 优先于 --remind：关闭提醒）
    # 注意：Graph 对 reminderMinutesBeforeStart 的 null PATCH 会忽略，且 null+isReminderOn 组合报 500；
    # 有效做法是单独 PATCH isReminderOn:false（reminderMinutesBeforeStart 数值残留但不再提醒）。
    if args.no_remind:
        patch["isReminderOn"] = False
        changes.append(t("ch_reminder"))
    elif args.remind is not None:
        if args.remind < 0:
            raise CalError(t("err_remind_negative"))
        # 用转换后的类型判断 N 的语义（天/分钟），而不是事件原类型：
        # --no-all-day --remind N 时事件已是时段，N 必须按分钟算
        if target_all_day:
            # 全天事件：N 语义 = 天数（×1440），上限 2629800 分钟（约 5 年）
            minutes = args.remind * 1440
            if minutes > 2629800:
                raise CalError(t("err_allday_remind_max", n=2629800 // 1440, m=args.remind))
            patch["reminderMinutesBeforeStart"] = minutes
            changes.append(t("ch_reminder"))
        else:
            patch["reminderMinutesBeforeStart"] = args.remind
            changes.append(t("ch_reminder"))
        # 显式设提醒必须同时打开提醒开关：事件此前 --no-remind 时 isReminderOn=false，
        # 只 PATCH 分钟数不会自动打开，用户会以为设了提醒其实永远不会响
        patch["isReminderOn"] = True

    # 重复规则
    if args.repeat is not None or args.repeat_until is not None or args.repeat_times is not None:
        # 守卫：定期系列的单次出现不可修改系列规则
        if data.get('seriesMasterId'):
            raise CalError(t("err_series_rule"))
        if args.repeat is None:
            raise CalError(t("err_repeat_until"))
        if args.repeat == "":
            if args.repeat_until is not None or args.repeat_times is not None:
                raise CalError(t("err_repeat_until"))
            # 解除定期
            patch["recurrence"] = None
            changes.append(t("ch_recurrence"))
            print(t("warn_repeat_removed"), file=sys.stderr)
        else:
            # range.startDate 必须与新的事件开始日期一致：同一命令里给了 --start 时
            # 用新日期，否则 Graph 会拒绝（"startDate must match start"）或造出错系列
            start_date = new_start_date or datetime.strptime(data['start']['dateTime'][:10], "%Y-%m-%d")
            recurrence, _ = _build_recurrence(args.repeat, args.repeat_until, args.repeat_times, start_date)
            recurrence["range"]["recurrenceTimeZone"] = patch.get("start", data["start"])["timeZone"]
            patch["recurrence"] = recurrence
            changes.append(t("ch_recurrence"))
            print(t("warn_repeat_reset"), file=sys.stderr)

    if not patch:
        if is_json:
            raise CalError(t("warn_nothing_to_update"))
        print(t("warn_nothing_to_update"), file=sys.stderr)
        return 1

    # 幂等确认：--yes 或 --json 跳过确认
    if not getattr(args, 'yes', False) and not is_json:
        if data.get('seriesMasterId'):
            print(t("warn_occurrence_only"))
        print(t("confirm_update", s=data['subject'], changes=", ".join(changes)))
        print(t("confirm_prompt"), end="", flush=True)
        try:
            ans = input().strip().lower()
        except (EOFError, KeyboardInterrupt):
            print(t("cancel_eof"))
            return 1
        if ans not in ("y", "yes"):
            print(t("cancel"))
            return 1

    result = _call("PATCH", f"/me/events/{quote(event_id, safe='')}", token, patch, prefer_immutable=True)
    if is_json:
        print(json.dumps(result, ensure_ascii=True))
        return 0
    print(t("update_success"))
    print(f"   {result['subject']}")
    s_tz = result['start'].get('timeZone')
    e_tz = result['end'].get('timeZone')
    if result.get('isAllDay'):
        s, e = _all_day_range(result['start']['dateTime'], result['end']['dateTime'])
        if e != s:
            print(f"   📅 {d_md(s)} {range_sep()} {d_md(e)}  {all_day()}")
        else:
            print(t("date_all_day", d=d_md(s)))
    else:
        print(f"   🕐 {_fmt(result['start']['dateTime'], s_tz)} - {_fmt(result['end']['dateTime'], e_tz)}")
    print()
    return 0


def cmd_read(args):
    """看一个日程的完整详情；定期系列的某一次会附带系列上下文。

    :param args: argparse 参数（event_id/json）
    :return: 0 成功
    """
    is_json = getattr(args, 'json', False)
    token = get_token()
    if not token:
        raise CalError(t("err_auth_first"))
    if not args.event_id:
        raise CalError(t("err_id_required"))

    data = _call("GET", f"/me/events/{quote(args.event_id, safe='')}", token, prefer_immutable=True)
    if is_json:
        print(json.dumps(data, ensure_ascii=True))
        return 0

    print(f"\n📋 {data['subject']}")
    print(f"🆔 {data['id']}")
    print("─" * 40)

    s_tz = data['start'].get('timeZone')
    e_tz = data['end'].get('timeZone')
    if data.get('isAllDay'):
        s, e = _all_day_range(data['start']['dateTime'], data['end']['dateTime'])
        if e == s:
            print(f"📅 {date_weekday(s, with_year=True)} {all_day()}")
        else:
            print(f"📅 {d_md(s)} {range_sep()} {d_md(e)}  {all_day()}")
    else:
        print(f"🕐 {_fmt(data['start']['dateTime'], s_tz)} - {_fmt(data['end']['dateTime'], e_tz)}")
        print(f"   {_weekday(data['start']['dateTime'], s_tz)}")

    loc = data.get('location', {}).get('displayName', '')
    if loc:
        print(f"📍 {loc}")

    created = data.get('createdDateTime')
    if created:
        print(t("read_added", t=_fmt(created)))

    org = (data.get('organizer') or {}).get('emailAddress', {}).get('address', '')
    if org:
        print(t("read_organizer", a=org))

    cats = data.get('categories', [])
    if cats:
        print(f"🏷️ {', '.join(cats)}")

    if data.get('recurrence'):
        print(f"🔁 {_fmt_recurrence(data['recurrence'])}")

    # 定期系列单次出现的上下文
    master_id = data.get('seriesMasterId')
    if master_id:
        try:
            master = _call("GET", f"/me/events/{quote(master_id, safe='')}", token, prefer_immutable=True)
            rec = _fmt_recurrence(master.get('recurrence'))
            print(t("read_series", s=master.get('subject', ''), rec=rec))
            # 改期的例外不能从当前日期倒推原序号；跨时区日期也不作估算。
            recurrence_zone = (master.get('recurrence') or {}).get('range', {}).get('recurrenceTimeZone')
            n = (_occurrence_number(master.get('recurrence'), data['start']['dateTime'])
                 if data.get('type') != 'exception' and recurrence_zone == data['start'].get('timeZone')
                 else None)
            if n:
                print(t("read_occ_num", n=n))
            print(t("read_master_id", id=master_id))
        except CalError:
            print(t("read_series_fail"))

    imp = data.get('importance')
    if imp and imp != 'normal':
        print(t("read_importance", v=imp_name(imp)))

    if data.get('sensitivity') == 'private':
        print(t("read_private"))

    show = data.get('showAs')
    if show and show != 'busy':
        print(t("read_showas", v=show))

    body = data.get('body', {}).get('content', '')
    if body:
        clean = html.unescape(re.sub(r'<[^>]+>', '', body)).replace("\xa0", " ").strip()
        if clean:
            print(f"📝 {clean}")

    wl = data.get('webLink')
    if wl:
        print(f"🔗 {wl}")
    print()
    return 0


def cmd_delete(args):
    """删日程；定期日程默认只删本次，--series 或交互选择可删整个系列。

    :param args: argparse 参数（event_id/-y/--series/json）
    :return: 0 成功；1 用户取消
    """
    is_json = getattr(args, 'json', False)
    token = get_token()
    if not token:
        raise CalError(t("err_auth_first"))
    event_id = _resolve_target_id(args, token)

    data = _call("GET", f"/me/events/{quote(event_id, safe='')}", token, prefer_immutable=True)
    master_id = data.get('seriesMasterId')
    is_master = data.get('recurrence') is not None

    # 确定删除目标：单次出现（默认）还是整个系列
    target_id = event_id
    if master_id:
        if args.series:
            target_id = master_id
        elif not args.yes and not is_json:
            # 交互选择；-y 时默认最小破坏：仅删本次（--json 同 -y 语义）
            print(t("warn_occ_of_series", s=data['subject']))
            print(t("delete_choice"))
            try:
                ans = input(t("delete_prompt")).strip().lower()
            except (EOFError, KeyboardInterrupt):
                print(t("cancel_eof_delete"))
                return 1
            if ans in ("2", "系列", "s", "series"):
                target_id = master_id
    deleting_series = target_id != event_id or is_master

    # 确认（--yes 或 --json 跳过）
    if not getattr(args, 'yes', False) and not is_json:
        if deleting_series:
            print(t("warn_series_all"))
        print(t("confirm_delete", s=data['subject']))
        print(t("confirm_prompt"), end="", flush=True)
        try:
            ans = input().strip().lower()
        except (EOFError, KeyboardInterrupt):
            print(t("cancel_eof"))
            return 1
        if ans not in ("y", "yes"):
            print(t("cancel"))
            return 1

    _call("DELETE", f"/me/events/{quote(target_id, safe='')}", token, prefer_immutable=True)
    if is_json:
        print(json.dumps({"deleted": target_id, "subject": data['subject'], "series": deleting_series},
                         ensure_ascii=True))
        return 0
    if deleting_series:
        print(t("deleted_series", s=data['subject']))
    elif master_id:
        print(t("deleted_occurrence", s=data['subject']))
    else:
        # 单次日程：没有"其余出现"可言，用中性文案
        print(t("deleted_single", s=data['subject']))
    # Graph 的删除进 Outlook「已删除项目」，一段时间内可找回——告诉用户别慌
    print(t("delete_recoverable"))
    return 0


# ── move：移动日程（按天数平移 或 移到目标日期，保留时段/时长）──

def cmd_move(args):
    """把日程按天数平移（--days）或挪到某天（--to），时段和时长不变。

    :param args: argparse 参数（event_id/--days/--to/-y/json）
    :return: 0 成功；1 用户取消
    """
    is_json = getattr(args, 'json', False)
    token = get_token()
    if not token:
        raise CalError(t("err_auth_first"))
    event_id = _resolve_target_id(args, token)
    if args.days is not None and args.to is not None:
        raise CalError(t("err_days_to"))
    if args.days is None and args.to is None:
        raise CalError(t("err_move_args"))
    if args.days == 0:
        raise CalError(t("err_move_zero"))

    data = _call("GET", f"/me/events/{quote(event_id, safe='')}", token, prefer_immutable=True)

    # 计算新起止：保留原时段与时长，只移动日期
    if data.get('isAllDay'):
        s, e = _all_day_range(data['start']['dateTime'], data['end']['dateTime'])
        if args.days is not None:
            ns, ne = _shift_days(s, args.days), _shift_days(e, args.days)
        else:
            target = _parse_dt_arg(args.to, date_only=True).date()
            ns, ne = target, _shift_days(e, (target - s).days)
        # 全天日程按邮箱首选时区写入（机器时区 ≠ 邮箱时区时不跨天；取不到回退本机）
        all_day_tz, _ = _mailbox_tz_name(token)
        patch = {
            "start": {"dateTime": ns.strftime("%Y-%m-%dT00:00:00"), "timeZone": all_day_tz},
            "end": {"dateTime": _shift_days(ne, 1).strftime("%Y-%m-%dT00:00:00"), "timeZone": all_day_tz},
        }
    else:
        s_dt = _parse_dt(data['start']['dateTime'], data['start'].get('timeZone')).replace(tzinfo=None)
        e_dt = _parse_dt(data['end']['dateTime'], data['end'].get('timeZone')).replace(tzinfo=None)
        if args.days is not None:
            ns, ne = _shift_days(s_dt, args.days), _shift_days(e_dt, args.days)
        else:
            target = _parse_dt_arg(args.to, date_only=True)
            delta = (target.date() - s_dt.date()).days
            ns, ne = _shift_days(s_dt, delta), _shift_days(e_dt, delta)
        patch = {
            "start": {"dateTime": ns.strftime("%Y-%m-%dT%H:%M:%S"), "timeZone": LOCAL_TZ_NAME},
            "end": {"dateTime": ne.strftime("%Y-%m-%dT%H:%M:%S"), "timeZone": LOCAL_TZ_NAME},
        }
        _validate_wall_times(ns, ne)

    # 系列提示
    if data.get('recurrence'):
        print(t("warn_move_series"), file=sys.stderr if is_json else sys.stdout)
    elif data.get('seriesMasterId'):
        print(t("warn_move_occ"), file=sys.stderr if is_json else sys.stdout)

    # 确认（--json 视为 -y；非交互 EOF 取消）
    if not is_json and not getattr(args, 'yes', False):
        if data.get('isAllDay'):
            target_range = f"{d_md(ns)}{t('move_allday_suffix')}"
        else:
            target_range = f"{d_md(ns)} {ns.strftime('%H:%M')} - {ne.strftime('%H:%M')}"
        print(t("confirm_move", s=data['subject'], range=target_range))
        print(t("confirm_prompt"), end="", flush=True)
        try:
            ans = input().strip().lower()
        except (EOFError, KeyboardInterrupt):
            print(t("cancel_eof"))
            return 1
        if ans not in ("y", "yes"):
            print(t("cancel"))
            return 1

    result = _call("PATCH", f"/me/events/{quote(event_id, safe='')}", token, patch, prefer_immutable=True)
    if is_json:
        print(json.dumps(result, ensure_ascii=True))
    else:
        print(t("move_success"))
        print(f"   {result['subject']}")
        s_tz = result['start'].get('timeZone')
        e_tz = result['end'].get('timeZone')
        if result.get('isAllDay'):
            s2, e2 = _all_day_range(result['start']['dateTime'], result['end']['dateTime'])
            if e2 != s2:
                print(f"   📅 {d_md(s2)} {range_sep()} {d_md(e2)}  {all_day()}")
            else:
                print(t("date_all_day", d=d_md(s2)))
        else:
            print(f"   🕐 {_fmt(result['start']['dateTime'], s_tz)} - {_fmt(result['end']['dateTime'], e_tz)}")
        print()
    return 0


# ── next：定期系列下次出现 ──

def cmd_next(args):
    """定期系列的下次出现（未来 365 天内最近一次）。

    :param args: argparse 参数（event_id/json）
    :return: 0 成功
    """
    is_json = getattr(args, 'json', False)
    token = get_token()
    if not token:
        raise CalError(t("err_auth_first"))
    if not args.event_id:
        raise CalError(t("err_id_required"))

    data = _call("GET", f"/me/events/{quote(args.event_id, safe='')}", token, prefer_immutable=True)
    if data.get('seriesMasterId'):
        master_id = data['seriesMasterId']
    elif data.get('recurrence'):
        master_id = data['id']
    else:
        raise CalError(t("err_not_recurring"))

    now = datetime.now(LOCAL_TZ)
    now_iso = now.isoformat(timespec="seconds")
    end_iso = (now + timedelta(days=365)).isoformat(timespec="seconds")
    # 注意：不带 $top/$orderby——/instances 端点对这两个参数有报错先例，
    # 而且它默认就按开始时间升序返回，本地截断取第一条即为下次出现
    url = (f"/me/events/{quote(master_id, safe='')}/instances?startDateTime={quote(now_iso, safe='')}"
           f"&endDateTime={quote(end_iso, safe='')}"
           f"&$select={_EVENT_SELECT}")
    instances = _get_all(url, token, prefer_immutable=True)
    instances = instances[:1]
    if instances:
        if is_json:
            print(json.dumps(instances, ensure_ascii=True))
        else:
            _print_events(instances, t("next_title"))
    else:
        if is_json:
            print(json.dumps({"ended": True}, ensure_ascii=True))
        else:
            print(t("next_ended"))
    return 0


# ── free：空闲时段（本地计算）──

def _compute_free_slots(events, day, from_min, to_min):
    """算某天从 from_min 到 to_min 之间的空闲时段（纯计算，不碰外部状态）。

    占用 = showAs != 'free' 的事件：全天占整天，时段按实际起止算，
    跨出查询窗口的部分只算窗口内；相邻的空闲段会合并。

    :param events: 当天的事件列表
    :param day: 要查的日期（date 对象）
    :param from_min: 窗口起点（当天第几分钟）
    :param to_min: 窗口终点（当天第几分钟）
    :return: [(开始, 结束), ...]，naive datetime，已合并相邻
    """
    day_start = datetime.combine(day, datetime.min.time())
    win_start = day_start + timedelta(minutes=from_min)
    win_end = day_start + timedelta(minutes=to_min)
    busy = []
    for ev in events:
        if ev.get('showAs') == 'free':
            continue  # 标记为 free 的不算占用
        if ev.get('isCancelled'):
            continue  # 定期系列已取消的单次不算占用（calendarView 会返回它们）
        if ev.get('isAllDay'):
            s, e = _all_day_range(ev['start']['dateTime'], ev['end']['dateTime'])
            b_s = datetime.combine(s, datetime.min.time())
            b_e = b_s + timedelta(days=(e - s).days + 1)
        else:
            b_s = _parse_dt(ev['start']['dateTime'], ev['start'].get('timeZone')).replace(tzinfo=None)
            b_e = _parse_dt(ev['end']['dateTime'], ev['end'].get('timeZone')).replace(tzinfo=None)
        s = max(b_s, win_start)
        e = min(b_e, win_end)
        if s < e:
            busy.append((s, e))
    busy.sort()
    # 合并相邻/重叠占用
    merged = []
    for s, e in busy:
        if merged and s <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], e))
        else:
            merged.append((s, e))
    # 占用区间的补集即空闲
    free = []
    cur = win_start
    for s, e in merged:
        if cur < s:
            free.append((cur, s))
        cur = max(cur, e)
    if cur < win_end:
        free.append((cur, win_end))
    return free


def _format_free_day(day, free, from_min, to_min):
    """把一天的空闲结果拼成显示行（如「📅 08月10日 周一：09:00-10:00 空闲」）。

    :param day: 日期
    :param free: _compute_free_slots 的结果
    :param from_min: 窗口起点（分钟）
    :param to_min: 窗口终点（分钟）
    :return: 显示行字符串
    """
    day_str = date_weekday(day)
    if not free:
        return t("free_none", d=day_str)
    total = to_min - from_min
    covered = sum((e - s).total_seconds() for s, e in free) / 60
    if covered >= total:
        return t("free_all", d=day_str)
    parts = [f"{s.strftime('%H:%M')}-{e.strftime('%H:%M')}" for s, e in free]
    return t("free_slots", d=day_str, parts=join(parts))


def cmd_free(args):
    """查指定日期起每天的空闲时段（默认窗口 09:00-18:00）。

    :param args: argparse 参数（date/--from/--to/--days/json）
    :return: 0 成功
    """
    is_json = getattr(args, 'json', False)
    start_date = _parse_dt_arg(args.date, date_only=True).date()
    from_str = args.from_time if getattr(args, 'from_time', None) is not None else "09:00"
    to_str = args.to_time if getattr(args, 'to_time', None) is not None else "18:00"
    for value in (from_str, to_str):
        if not re.fullmatch(r"[0-9]{2}:[0-9]{2}", value):
            raise CalError(t("err_time_hhmm", s=value))
    try:
        from_dt = datetime.strptime(from_str, "%H:%M")
        to_dt = datetime.strptime(to_str, "%H:%M")
    except ValueError as exc:
        raise CalError(t("err_time_hhmm", s=str(exc))) from exc
    from_min = from_dt.hour * 60 + from_dt.minute
    to_min = to_dt.hour * 60 + to_dt.minute
    if to_min <= from_min:
        raise CalError(t("err_to_from", to=to_str, **{"from": from_str}))
    days = getattr(args, 'days', None)
    if days is None:
        days = 1
    if days < 1:
        raise CalError(t("err_days_min"))
    _shift_days(start_date, days)  # Validate the complete window before the first query.
    for i in range(days):
        day = start_date + timedelta(days=i)
        window_start = datetime.combine(day, from_dt.time())
        window_end = datetime.combine(day, to_dt.time())
        _validate_wall_times(window_start, window_end)
        if (window_start.replace(tzinfo=LOCAL_TZ).utcoffset()
                != window_end.replace(tzinfo=LOCAL_TZ).utcoffset()):
            # HH:MM output cannot represent a fold or gap unambiguously.
            raise CalError(t("err_dst_window", zone=LOCAL_TZ_NAME, date=day.isoformat()))

    token = get_token()
    if not token:
        raise CalError(t("err_auth_first"))
    result = {}
    for i in range(days):
        d = start_date + timedelta(days=i)
        q_start = datetime.combine(d, datetime.min.time())
        q_end = q_start + timedelta(days=1)
        start_iso = q_start.replace(tzinfo=LOCAL_TZ).isoformat(timespec="seconds")
        end_iso = q_end.replace(tzinfo=LOCAL_TZ).isoformat(timespec="seconds")
        url = (f"/me/calendar/calendarView?startDateTime={quote(start_iso, safe='')}&endDateTime={quote(end_iso, safe='')}"
               f"&$select={_EVENT_SELECT},showAs&$orderby=start/dateTime")
        events = _get_all(url, token, prefer_immutable=True)
        free = _compute_free_slots(events, d, from_min, to_min)
        if is_json:
            # 按天结构：{"YYYY-MM-DD": [["HH:MM","HH:MM"], ...]}
            result[d.strftime("%Y-%m-%d")] = [[s.strftime("%H:%M"), e.strftime("%H:%M")] for s, e in free]
        else:
            print(_format_free_day(d, free, from_min, to_min))
    if is_json:
        print(json.dumps(result, ensure_ascii=True))
    else:
        print()
    return 0
