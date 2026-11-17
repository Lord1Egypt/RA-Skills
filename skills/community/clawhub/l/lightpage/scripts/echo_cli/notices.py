"""Pass optional JSON notices through without interpreting their notification types."""

import json

MAXIMUM_BYTES = 8192
MESSAGE_CHARACTERS = 1000
ACCUMULATION_BYTES = 32768


def encoded(value):
    return json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(",", ":")).encode(
        "utf-8"
    )


def decode(value, maximum=MAXIMUM_BYTES):
    if not value:
        return None
    try:
        if isinstance(value, str):
            if len(value.encode("utf-8")) > maximum:
                return None
            value = json.loads(value)
        if not isinstance(value, dict) or not value or len(encoded(value)) > maximum:
            return None
        # Copy JSON data so truncation never mutates the HTTP response or caller.
        return json.loads(encoded(value))
    except (ValueError, TypeError, UnicodeError, RecursionError):
        return None


def trim_messages(value, maximum=MESSAGE_CHARACTERS):
    """Keep the first maximum Unicode code points across every message, in JSON order."""
    remaining = maximum

    def visit(node):
        nonlocal remaining
        if isinstance(node, dict):
            result = {}
            for key, child in node.items():
                if key == "message" and isinstance(child, str):
                    if remaining:
                        result[key] = child[:remaining]
                        remaining -= len(result[key])
                else:
                    result[key] = visit(child)
            return result
        if isinstance(node, list):
            return [visit(child) for child in node]
        return node

    return visit(value)


def merge(first, second):
    """Merge JSON metadata; later scalars win, arrays keep unique entries in first-seen order."""
    if isinstance(first, dict) and isinstance(second, dict):
        result = dict(first)
        for key, child in second.items():
            result[key] = merge(result[key], child) if key in result else child
        return result
    if isinstance(first, list) and isinstance(second, list):
        result = list(first)
        for child in second:
            position = next(
                (
                    i
                    for i, previous in enumerate(result)
                    if previous == child
                    or (
                        isinstance(previous, dict)
                        and isinstance(child, dict)
                        and child.get("id") is not None
                        and previous.get("id") == child["id"]
                        and previous.get("type") == child.get("type")
                        and previous.get("kind") == child.get("kind")
                    )
                ),
                None,
            )
            if position is None:
                result.append(child)
            else:
                result[position] = merge(result[position], child)
        return result
    return second


class Collector:
    """One bounded notice per CLI invocation, including intermediate and retry responses."""

    def __init__(self):
        self.value = {}

    def add(self, notice):
        if not notice:
            return
        try:
            candidate = merge(self.value, notice)
            visible = trim_messages(candidate)
            if (
                len(encoded(candidate)) <= ACCUMULATION_BYTES - 32
                and len(encoded(visible)) <= MAXIMUM_BYTES - 32
            ):
                self.value = candidate
            else:
                self.value["client_truncated"] = True
        except (ValueError, TypeError, UnicodeError, RecursionError):
            pass

    def attach(self, result):
        result = dict(result)
        self.add(decode(result.pop("notice", None)))
        if self.value:
            result["notice"] = trim_messages(self.value)
        return result


def output(result, api=None):
    collector = getattr(api, "notice_collector", None) or Collector()
    return collector.attach(result)
