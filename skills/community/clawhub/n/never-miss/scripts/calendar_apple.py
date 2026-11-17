# -*- coding: utf-8 -*-
"""Calendar.app 的 AppleScript 封装（需求 §6.3）。

要点：
- 脚本经 osascript stdin 传入（避开 shell 转义）；用户文本嵌入前转义 \\ 与 "
- 日期用 date "YYYY-MM-DD HH:MM:SS"（系统本地时区解析，doctor 校验时区一致）
- 读回日期用 {year, month, day, hours, minutes} 组件拼 ISO（避免 locale 依赖）
- 本 Skill 创建的事件以 description 首行 "[never-miss] uid:..." 标识（Calendar 事件 uid 只读）
- 查重/查询范围：所有以基础日历名开头的日历（覆盖 per_account 变体）
- 冲突检查范围：全部日历（用户真实日程也参与冲突判断）
"""
import subprocess
import sys
from datetime import datetime

SEP = '␟'  # 展示用；脚本内实际用 character id 31


class CalendarError(Exception):
    def __init__(self, code, message, hint=None):
        super().__init__(message)
        self.code = code
        self.hint = hint


def _require_macos():
    if sys.platform != 'darwin':
        raise CalendarError('E_UNSUPPORTED', '当前系统非 macOS，无法写入系统日历',
                            hint='仅可生成 .ics 文件供手动导入')


def _esc(s):
    """AppleScript 字符串字面量转义（换行统一为 \\n）。"""
    return (str(s)
            .replace('\\', '\\\\')
            .replace('"', '\\"')
            .replace('\r', '\\n')
            .replace('\n', '\\n'))


def _as_date(dt):
    """返回纯日期字符串（'YYYY-MM-DD HH:MM:SS'），模板中已含 `date "..."` 包裹。"""
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt)
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def _run(script, timeout=90):
    try:
        proc = subprocess.run(
            ['osascript', '-'],
            input=script, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        raise CalendarError('E_CALENDAR', 'Calendar.app 响应超时')
    if proc.returncode != 0:
        err = (proc.stderr or '').strip()
        low = err.lower()
        if 'not authorized' in low or '-1743' in low or 'appleevent' in low:
            raise CalendarError(
                'E_AUTH', '未获得控制"日历"的授权：%s' % err,
                hint='系统设置 → 隐私与安全性 → 自动化 → 允许控制"日历"，然后重试')
        raise CalendarError('E_CALENDAR', '日历操作失败：%s' % err)
    return proc.stdout


def _iso_handler():
    return '''on isoDate(d)
	set y to text -4 thru -1 of ("0000" & (year of d))
	set m to text -2 thru -1 of ("00" & ((month of d) as integer))
	set dd to text -2 thru -1 of ("00" & (day of d))
	set hh to text -2 thru -1 of ("00" & (hours of d))
	set mm to text -2 thru -1 of ("00" & (minutes of d))
	return y & "-" & m & "-" & dd & " " & hh & ":" & mm & ":00"
end isoDate

on flatText(t)
	set prevDelim to AppleScript's text item delimiters
	set AppleScript's text item delimiters to {return, linefeed, character id 31}
	set theParts to text items of t
	set AppleScript's text item delimiters to "|"
	set outText to theParts as text
	set AppleScript's text item delimiters to prevDelim
	return outText
end flatText
'''


def _parse_lines(out):
    """解析 osascript 输出：行分隔 linefeed，字段分隔 US(31)。"""
    events = []
    for line in out.split('\n'):
        line = line.rstrip('\r')
        if not line:
            continue
        fields = line.split('\x1f')
        events.append(fields)
    return events


def ensure_calendar(name, want_icloud=False):
    """确保专用日历存在。返回 {'created': bool, 'source': str}。

    注意：macOS 26 的 Calendar.app 已从 AppleScript 移除 source 类，无法再按名称指定
    iCloud/On My Mac 位置；want_icloud 仅作语义保留，实际统一创建到系统默认位置。
    """
    _require_macos()
    script = '''on run
	tell application "Calendar"
		set calName to "__CAL__"
		set createdFlag to "exists"
		if not (exists calendar calName) then
			make new calendar with properties {name:calName}
			set createdFlag to "created"
		end if
		return createdFlag
	end tell
end run'''
    script = script.replace('__CAL__', _esc(name))
    out = _run(script).strip()
    return {'created': out == 'created', 'source': '默认位置（macOS 26 不再暴露 source 类）'}


def find_uid(base_name, uid):
    """统计 UID 已存在于多少事件（跨账户去重）。"""
    _require_macos()
    script = '''on run
	tell application "Calendar"
		set hits to 0
		repeat with c in (every calendar whose name begins with "__BASE__")
			try
				set evs to (every event of c whose description contains "__UID__")
				set hits to hits + (count of evs)
			end try
		end repeat
		return (hits as text)
	end tell
end run'''
    script = script.replace('__BASE__', _esc(base_name)).replace('__UID__', _esc(uid))
    return int(_run(script).strip() or 0)


def check_conflict(start, end, exclude_uid=None):
    """检查全部日历中与 [start, end) 重叠的事件。"""
    _require_macos()
    script = _iso_handler() + '''on run
	tell application "Calendar"
		set res to ""
		repeat with c in (every calendar)
			try
				set evs to (every event of c whose (start date < date "__END__") and (end date > date "__START__"))
				repeat with e in evs
					set s to ""
					set dsc to ""
					try
						set s to summary of e
					end try
					try
						set dsc to description of e
					end try
					if dsc does not contain "__EXCLUDE__" then
						set res to res & s & (character id 31) & my isoDate(start date of e) & (character id 31) & my isoDate(end date of e) & (character id 31) & ((name of c) as text) & linefeed
					end if
				end repeat
			end try
		end repeat
		return res
	end tell
end run'''
    script = (script
              .replace('__START__', _as_date(start))
              .replace('__END__', _as_date(end))
              .replace('__EXCLUDE__', _esc(exclude_uid or '')))
    conflicts = []
    for fields in _parse_lines(_run(script)):
        if len(fields) >= 3:
            conflicts.append({'title': fields[0], 'start': fields[1], 'end': fields[2],
                              'calendar': fields[3] if len(fields) > 3 else ''})
    return conflicts


def create_event(cal_name, title, start, end, all_day, description, location='',
                 reminder_lead_minutes=60, all_day_alarm_at=None):
    """在指定日历创建带提醒的事件。all_day 事件提醒时刻取 all_day_alarm_at（'HH:MM'）。"""
    _require_macos()
    if all_day and all_day_alarm_at:
        hh, mm = all_day_alarm_at.split(':')
        # 全天事件 start 为日期串（或 00:00 时刻），取其日期部分
        day = str(start)[:10]
        trigger_date = datetime.strptime('%s %s:%s' % (day, hh, mm), '%Y-%m-%d %H:%M')
        alarm = ('make new display alarm at end of display alarms of newEvent '
                 'with properties {trigger date:date "%s"}' % trigger_date.strftime('%Y-%m-%d %H:%M:%S'))
    else:
        alarm = ('make new display alarm at end of display alarms of newEvent '
                 'with properties {trigger interval:%d}' % -int(reminder_lead_minutes))
    loc = ', location:"%s"' % _esc(location) if location else ''
    script = '''on run
	tell application "Calendar"
		tell calendar "__CAL__"
			set newEvent to make new event with properties {summary:"__TITLE__", start date:date "__START__", end date:date "__END__", allday event:__ALLED__, description:"__DESC__"__LOC__}
			__ALARM__
		end tell
	end tell
	return "ok"
end run'''
    script = (script
              .replace('__CAL__', _esc(cal_name))
              .replace('__TITLE__', _esc(title))
              .replace('__START__', _as_date(start))
              .replace('__END__', _as_date(end))
              .replace('__ALLED__', 'true' if all_day else 'false')
              .replace('__DESC__', _esc(description))
              .replace('__LOC__', loc)
              .replace('__ALARM__', alarm))
    _run(script)
    return True


def list_events(base_name, date_from, date_to):
    """列出 [date_from, date_to) 内本 Skill 创建的事件（按 description 标记过滤）。"""
    _require_macos()
    script = _iso_handler() + '''on run
	tell application "Calendar"
		set res to ""
		repeat with c in (every calendar whose name begins with "__BASE__")
			try
				set evs to (every event of c whose (start date ≥ date "__FROM__") and (start date < date "__TO__") and (description contains "[never-miss]"))
				repeat with e in evs
					set s to ""
					set dsc to ""
					try
						set s to summary of e
					end try
					try
						set dsc to description of e
					end try
					set res to res & s & (character id 31) & my isoDate(start date of e) & (character id 31) & my isoDate(end date of e) & (character id 31) & ((allday event of e) as text) & (character id 31) & my flatText(dsc) & linefeed
				end repeat
			end try
		end repeat
		return res
	end tell
end run'''
    script = (script
              .replace('__BASE__', _esc(base_name))
              .replace('__FROM__', _as_date(date_from))
              .replace('__TO__', _as_date(date_to)))
    events = []
    for fields in _parse_lines(_run(script)):
        if len(fields) < 5:
            continue
        events.append({
            'title': fields[0], 'start': fields[1], 'end': fields[2],
            'all_day': fields[3] == 'true', 'description': fields[4],
        })
    return events


def write_test(cal_name):
    """写入一条测试事件并立即删除（doctor --write-test）。"""
    _require_macos()
    now = datetime.now()
    script = '''on run
	tell application "Calendar"
		tell calendar "__CAL__"
			set te to make new event with properties {summary:"never-miss 自检事件（已自动删除）", start date:date "__START__", end date:date "__END__", description:"[never-miss] uid:nm-doctor-selftest@never-miss.local"}
			delete te
		end tell
	end tell
	return "ok"
end run'''
    script = (script
              .replace('__CAL__', _esc(cal_name))
              .replace('__START__', (now).strftime('%Y-%m-%d %H:%M:%S'))
              .replace('__END__', (now).strftime('%Y-%m-%d %H:%M:%S')))
    _run(script)
    return True
