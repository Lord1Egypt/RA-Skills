"""Local clock context and deterministic date arithmetic; no authentication or Graph calls."""
import json
from datetime import datetime, timedelta

import ocal_time
from ocal_errors import CalError
from ocal_i18n import t

_WEEKDAYS = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")


def cmd_context(args):
    now = datetime.now(ocal_time.LOCAL_TZ)
    offset = now.strftime("%z")
    result = {
        "now": now.isoformat(timespec="seconds"),
        "today": now.date().isoformat(),
        "timezone": ocal_time.LOCAL_TZ_NAME,
        "utc_offset": offset[:3] + ":" + offset[3:],
        "weekday": _WEEKDAYS[now.weekday()],
        "week_start": (now.date() - timedelta(days=now.weekday())).isoformat(),
    }
    if getattr(args, "json", False):
        print(json.dumps(result, ensure_ascii=True))
    else:
        print(t("context_result", **result))
    return 0


def cmd_date(args):
    base = ocal_time._parse_dt_arg(args.base, date_only=True).date()
    try:
        result_date = base + timedelta(days=args.days)
    except (OverflowError, TypeError) as exc:
        raise CalError(t("err_date_offset")) from exc
    result = {"base": base.isoformat(), "days": args.days, "date": result_date.isoformat()}
    if getattr(args, "json", False):
        print(json.dumps(result, ensure_ascii=True))
    else:
        print(result["date"])
    return 0
