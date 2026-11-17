#!/usr/bin/env python3
"""Small, dependency-free evidence checker for the published JSON event fields."""
import json
import re
import sys
from datetime import datetime
from pathlib import Path


def parse_time(value):
    """Return (axis, minutes), keeping wall-clock and dated time separate."""
    if isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}(?::\d{2})?", value):
        try:
            dt = datetime.fromisoformat(value.replace(" ", "T"))
            return ("dated", dt.toordinal() * 86400 + dt.hour * 3600 + dt.minute * 60 + dt.second)
        except (ValueError, OverflowError):
            return None
    if isinstance(value, str) and re.fullmatch(r"\d{2}:\d{2}", value):
        hours, mins = (int(part) for part in value.split(":"))
        if 0 <= hours < 24 and 0 <= mins < 60:
            return ("clock", hours * 3600 + mins * 60)
    return None


def is_nonnegative_minutes(value):
    """Return whether a declared travel duration is valid, including zero."""
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def event_time(event, by_id, cache=None, visiting=None):
    """Resolve explicit and relative event times without mixing time axes."""
    cache = {} if cache is None else cache
    visiting = set() if visiting is None else visiting
    event_id = event.get("id")
    if event_id in cache:
        return cache[event_id]
    if event_id in visiting:
        return None
    visiting.add(event_id)
    value = event.get("time")
    if isinstance(value, dict) and isinstance(value.get("after"), str) and isinstance(value.get("minutes"), int) and not isinstance(value.get("minutes"), bool) and value["minutes"] > 0:
        base = by_id.get(value["after"])
        resolved = event_time(base, by_id, cache, visiting) if base else None
        result = (resolved[0], resolved[1] + value["minutes"] * 60) if resolved else None
    else:
        result = parse_time(value)
    visiting.remove(event_id)
    cache[event_id] = result
    return result


def get_predecessor_ids(event):
    """Return every declared predecessor, including relative and top-level after."""
    relative = event.get("time") if isinstance(event.get("time"), dict) else {}
    return list(dict.fromkeys(value for value in (relative.get("after"), event.get("after")) if isinstance(value, str) and value))


def order_events(events, resolved):
    """Stable topological order for explicit after constraints; return any cycle."""
    by_id = {event.get("id"): event for event in events}
    original_index = {event.get("id"): index for index, event in enumerate(events)}
    outgoing = {event.get("id"): set() for event in events}
    indegree = {event.get("id"): 0 for event in events}
    for event in events:
        current_id = event.get("id")
        for prior_id in get_predecessor_ids(event):
            if prior_id in by_id and current_id not in outgoing[prior_id]:
                outgoing[prior_id].add(current_id)
                indegree[current_id] += 1

    def priority(event_id):
        value = resolved.get(event_id)
        return (0, value[1], original_index[event_id]) if value is not None else (1, original_index[event_id], original_index[event_id])

    ready = sorted((event_id for event_id, degree in indegree.items() if degree == 0), key=priority)
    ordered_ids = []
    while ready:
        current_id = ready.pop(0)
        ordered_ids.append(current_id)
        for next_id in sorted(outgoing[current_id], key=priority):
            indegree[next_id] -= 1
            if indegree[next_id] == 0:
                ready.append(next_id)
                ready.sort(key=priority)
    if len(ordered_ids) != len(events):
        cycle_ids = [event.get("id", "(未命名)") for event in events if indegree.get(event.get("id"), 0) > 0]
        return events, cycle_ids
    return [by_id[event_id] for event_id in ordered_ids], []


def audit(events):
    rows, conflicts, missing = [], [], []
    ids = [event.get("id") for event in events if isinstance(event.get("id"), str) and event.get("id").strip()]
    duplicates = sorted({event_id for event_id in ids if ids.count(event_id) > 1})
    if duplicates:
        return {"timeline": [], "conflicts": [{"type": "重复事件ID", "ids": duplicates,
                "minimum_revision": "为每个事件分配唯一 ID 后重新核对；重复 ID 会使 after 引用和时间缓存产生歧义。"}], "missing_basis": []}
    by_id = {event.get("id"): event for event in events if isinstance(event.get("id"), str) and event.get("id").strip()}
    time_cache = {}
    resolved = {event.get("id"): event_time(event, by_id, time_cache) for event in events}
    # Normalize dependencies on the same resolved axis. A declared trip may
    # cross midnight. Ordinary after events can inherit that established day,
    # but cannot roll themselves into another day to hide a reversed clock.
    for _ in range(len(events)):
        changed = False
        for event in events:
            relative = event.get("time") if isinstance(event.get("time"), dict) else None
            predecessor_id = relative.get("after") if relative else event.get("after")
            predecessor = by_id.get(predecessor_id)
            before_time = resolved.get(predecessor_id)
            after_time = resolved.get(event.get("id"))
            required = event.get("travel_minutes")
            if (relative and predecessor and before_time
                    and isinstance(relative.get("minutes"), int)
                    and not isinstance(relative.get("minutes"), bool)
                    and relative["minutes"] > 0):
                normalized = (before_time[0], before_time[1] + relative["minutes"] * 60)
                if after_time != normalized:
                    resolved[event.get("id")] = normalized
                    changed = True
            if (predecessor and before_time and after_time and before_time[0] == after_time[0] == "clock"
                    and after_time[1] < before_time[1] and not relative):
                day_offset, before_clock = divmod(before_time[1], 86400)
                after_clock = after_time[1] % 86400
                # Zero minutes is still an explicit trip constraint: it may
                # establish that a later wall-clock time is on the next day.
                explicit_trip = is_nonnegative_minutes(required)
                if explicit_trip and after_clock < before_clock:
                    normalized = ("clock", after_clock + (day_offset + 1) * 86400)
                elif day_offset > 0:
                    # A normal `after` may inherit the day already established
                    # by an earlier trip, but it must never create another
                    # overnight rollover. Keep an earlier wall-clock value on
                    # that same day so the strict-after check can report it.
                    normalized = ("clock", after_clock + day_offset * 86400)
                else:
                    normalized = after_time
                if after_time != normalized:
                    resolved[event.get("id")] = normalized
                    changed = True
        if not changed:
            break
    axes = {time[0] for time in resolved.values() if time is not None}
    mixed_axes = len(axes) > 1

    referenced_ids = {prior_id for event in events for prior_id in get_predecessor_ids(event)}
    for event in events:
        event_id = event.get("id", "(未命名)")
        when = resolved.get(event.get("id"))
        relative_order = event.get("time") if isinstance(event.get("time"), dict) else {}
        has_order = bool(get_predecessor_ids(event)) or event_id in referenced_ids
        if when is None and not has_order:
            missing.append({"id": event_id, "reason": "没有时间或事件顺序依据", "status": "未定"})
        elif when is None and isinstance(event.get("time"), dict):
            relative = event["time"]
            if isinstance(relative.get("minutes"), int) and not isinstance(relative.get("minutes"), bool) and relative["minutes"] <= 0:
                conflicts.append({"from": relative.get("after"), "to": event_id, "type": "相对时间 after", "given_minutes": relative["minutes"], "required_minutes": 1, "minimum_revision": f"修正 {event_id} 的相对分钟数为正数；after 必须严格晚于所指事件。"})
            else:
                missing.append({"id": event_id, "reason": "相对时间的 after 引用不存在、循环或分钟数无效", "status": "未定"})
        elif mixed_axes and when is not None:
            missing.append({"id": event_id, "reason": "输入混用 HH:MM 与绝对日期时间，不能放在同一时间轴比较", "status": "未定"})
        rows.append({
            "id": event_id,
            "chapter": event.get("chapter", event.get("scene", "未提供")),
            "time": event.get("time", "未定"),
            "flashback": bool(event.get("flashback", False)),
            "status": "未定" if when is None or mixed_axes else "可比较",
            "_time": when,
        })

    # `after` is a published ordering constraint independent of event-list order.
    for event in events:
        relative = event.get("time") if isinstance(event.get("time"), dict) else {}
        travel_parent = event.get("after") or relative.get("after")
        for predecessor_id in get_predecessor_ids(event):
            predecessor = by_id.get(predecessor_id)
            if predecessor is None:
                missing.append({"id": event.get("id", "(未命名)"), "reason": f"after 引用的事件 {predecessor_id} 不存在", "status": "未定"})
                continue
            before_time = resolved.get(predecessor_id)
            after_time = resolved.get(event.get("id"))
            required = event.get("travel_minutes") if predecessor_id == travel_parent else None
            if before_time and after_time and before_time[0] == after_time[0]:
                gap = after_time[1] - before_time[1]
                if gap <= 0:
                    conflicts.append({"from": predecessor_id, "to": event.get("id"), "type": "after 顺序", "given_seconds": gap, "required_seconds": 1, "minimum_revision": f"核对并更正 {predecessor_id} 或 {event.get('id')} 的明确时间；after 要求 {predecessor_id} 先于 {event.get('id')}。"})

            if is_nonnegative_minutes(required):
                if before_time and after_time and before_time[0] == after_time[0]:
                    travel_gap = after_time[1] - before_time[1]
                    required_seconds = required * 60
                    if travel_gap < required_seconds:
                        shortfall = required_seconds - travel_gap
                        given_minutes = travel_gap / 60
                        shortfall_minutes = shortfall / 60
                        conflicts.append({"from": predecessor_id, "to": event.get("id"), "type": "行程时长", "given_seconds": travel_gap, "given_minutes": round(given_minutes, 6), "required_minutes": required, "shortfall_minutes": round(shortfall_minutes, 6), "minimum_revision": f"核对并更正 {predecessor_id} 或 {event.get('id')} 的明确时刻；若行程时长有来源，再据来源更正 travel_minutes。仅补时间跳转说明不能消除这两个时刻之间的 {given_minutes:g} 分钟间隔。"})
                elif mixed_axes or not before_time or not after_time or (before_time and after_time and before_time[0] != after_time[0]):
                    missing.append({"id": event.get("id", "(未命名)"), "reason": "行程时长存在，但起止时间不在可比较的同一时间轴上", "status": "未定"})

    # Input order is story order only for adjacent events without an explicit
    # dependency or a marked flashback. Do not silently sort away an unmarked
    # reversal that the author supplied in narrative sequence.
    for previous, current in zip(events, events[1:]):
        if current.get("flashback") is True or previous.get("flashback") is True:
            continue
        previous_id, current_id = previous.get("id"), current.get("id")
        current_time = current.get("time") if isinstance(current.get("time"), dict) else {}
        previous_time = previous.get("time") if isinstance(previous.get("time"), dict) else {}
        directly_linked = (current.get("after") == previous_id or current_time.get("after") == previous_id
                           or previous.get("after") == current_id or previous_time.get("after") == current_id)
        if directly_linked:
            continue
        before_time, after_time = resolved.get(previous.get("id")), resolved.get(current.get("id"))
        # Equal clock readings are not a narrative reversal.  Strict ordering
        # is enforced separately when an explicit `after` relation exists.
        if before_time and after_time and before_time[0] == after_time[0] and after_time[1] < before_time[1]:
            conflicts.append({"from": previous.get("id"), "to": current.get("id"), "type": "相邻事件倒序",
                "given_seconds": after_time[1] - before_time[1], "minimum_revision": f"核对 {previous.get('id')} 与 {current.get('id')} 的明确时间，或在确属回忆时标记 flashback。"})

    ages_by_day = {}
    for event in events:
        when = resolved.get(event.get("id"))
        age = event.get("age")
        # Identity is deliberately opt-in: only a non-empty character_id can
        # link age records.  Display names and generic fields such as
        # character, person_id, and subject are not stable character IDs.
        person = event.get("character_id") if isinstance(event.get("character_id"), str) and event.get("character_id").strip() else None
        if when and person and isinstance(age, (int, float)) and not isinstance(age, bool):
            # HH:MM inputs share an implicit day; normalized cross-midnight
            # clock values naturally form their following day.  Keep axes
            # distinct so mixed absolute/clock input remains indeterminate.
            day = when[1] // 86400
            ages_by_day.setdefault((when[0], day, person.strip()), []).append((event, age))
    for same_day in ages_by_day.values():
        for index, (earlier, earlier_age) in enumerate(same_day):
            for later, later_age in same_day[index + 1:]:
                if earlier_age != later_age:
                    conflicts.append({"from": earlier.get("id"), "to": later.get("id"), "type": "同日年龄变化", "given_ages": [earlier_age, later_age], "minimum_revision": f"核对 {earlier.get('id')} 与 {later.get('id')} 的年龄依据；同一日期不能从 {earlier_age} 岁变为 {later_age} 岁。"})

    ordered_events, cycle_ids = order_events(events, resolved)
    if cycle_ids:
        conflicts.append({"type": "after 循环", "ids": cycle_ids,
            "minimum_revision": "打破 after 循环，使每条事件顺序约束最终指向一个无环顺序。"})
    if not mixed_axes:
        # Sort all comparable events by story time even when some events are
        # untimed. Keep undated events together at the end, respecting their
        # explicit after constraints (and otherwise preserving input order).
        original_order = {event.get("id"): index for index, event in enumerate(events)}
        dependency_order = {event.get("id"): index for index, event in enumerate(ordered_events)}
        rows.sort(key=lambda row: (row["_time"] is None,
                                   row["_time"][1] if row["_time"] is not None else 0,
                                   dependency_order.get(row["id"], original_order.get(row["id"], len(events)))
                                   if row["_time"] is None else original_order.get(row["id"], len(events))))
    elif any(get_predecessor_ids(event) for event in events) and not cycle_ids:
        order_index = {event.get("id"): index for index, event in enumerate(ordered_events)}
        rows.sort(key=lambda row: order_index.get(row["id"], len(order_index)))
    for row in rows:
        del row["_time"]
    return {"timeline": rows, "conflicts": conflicts, "missing_basis": missing}


def main():
    if len(sys.argv) != 2:
        raise SystemExit("用法: audit_timeline.py INPUT.json")
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    events = data.get("events")
    if not isinstance(events, list) or len(events) > 100:
        raise SystemExit("events 必须是至多 100 项的数组")
    scene_keys = {event.get("scene", event.get("chapter")) for event in events if event.get("scene", event.get("chapter")) is not None}
    if len(scene_keys) > 20:
        raise SystemExit("scene/chapter 场景标识不得超过 20 个；请指定分批范围")
    print(json.dumps(audit(events), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
