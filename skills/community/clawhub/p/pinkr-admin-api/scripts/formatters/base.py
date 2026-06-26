from typing import Any, Dict


class BaseFormatter:
    def format(self, raw: Dict[str, Any]) -> Dict[str, Any]:  # pragma: no cover
        raise NotImplementedError

    def _format_time(self, ts: Any) -> Any:
        if ts is None:
            return None
        import datetime
        try:
            if isinstance(ts, (int, float)):
                dt = datetime.datetime.fromtimestamp(int(ts))
                return dt.strftime('%Y-%m-%d %H:%M:%S')
            if isinstance(ts, str) and ts.isdigit():
                dt = datetime.datetime.fromtimestamp(int(ts))
                return dt.strftime('%Y-%m-%d %H:%M:%S')
        except Exception:
            pass
        return ts
