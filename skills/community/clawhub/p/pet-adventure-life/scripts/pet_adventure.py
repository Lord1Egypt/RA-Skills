#!/usr/bin/env python3
"""Core engine for the pet-adventure-life skill."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import random
import sys
import textwrap
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

VERSION = "0.1.0"
STATE_DIR = "pet-life"

LOCATIONS = [
    {
        "name": "Kyoto",
        "country": "Japan",
        "lat": 35.0116,
        "lon": 135.7681,
        "timezone": "Asia/Tokyo",
        "terrain": "temples, alleys, mossy gardens",
    },
    {
        "name": "Reykjavik",
        "country": "Iceland",
        "lat": 64.1466,
        "lon": -21.9426,
        "timezone": "Atlantic/Reykjavik",
        "terrain": "black stone, harbor wind, northern light rumors",
    },
    {
        "name": "Marrakesh",
        "country": "Morocco",
        "lat": 31.6295,
        "lon": -7.9811,
        "timezone": "Africa/Casablanca",
        "terrain": "markets, red walls, desert road dust",
    },
    {
        "name": "Cusco",
        "country": "Peru",
        "lat": -13.532,
        "lon": -71.9675,
        "timezone": "America/Lima",
        "terrain": "thin mountain air, stone steps, old paths",
    },
    {
        "name": "Queenstown",
        "country": "New Zealand",
        "lat": -45.0312,
        "lon": 168.6626,
        "timezone": "Pacific/Auckland",
        "terrain": "cold lake light, mountains, long grass",
    },
    {
        "name": "Lofoten",
        "country": "Norway",
        "lat": 68.2083,
        "lon": 13.9153,
        "timezone": "Europe/Oslo",
        "terrain": "fishing villages, sharp peaks, sea weather",
    },
    {
        "name": "Dali",
        "country": "China",
        "lat": 25.6065,
        "lon": 100.2676,
        "timezone": "Asia/Shanghai",
        "terrain": "lake wind, old town stones, blue mountains",
    },
]

SPECIES = ["小狐狸", "水獭", "狸花猫", "小狗", "乌龟", "渡鸦"]
PERSONALITIES = [
    {
        "name": "谨慎但好奇",
        "traits": {"courage": 0, "wit": 2, "heart": 1, "survival": 1},
        "voice": "短句、观察细、常把危险写得很轻。",
    },
    {
        "name": "勇敢又有点莽",
        "traits": {"courage": 3, "wit": 0, "heart": 1, "survival": 0},
        "voice": "语气明亮，容易把困难说成小插曲。",
    },
    {
        "name": "温柔的收藏家",
        "traits": {"courage": 0, "wit": 1, "heart": 3, "survival": 0},
        "voice": "会记住人、气味、票根和没说完的话。",
    },
    {
        "name": "安静的路线师",
        "traits": {"courage": 1, "wit": 1, "heart": 0, "survival": 2},
        "voice": "像写地图，也像写梦。",
    },
]

EVENT_TEMPLATES = [
    {
        "title": "陌生车站的求助",
        "urgency": "normal",
        "dc": 12,
        "skill": "heart",
        "message": "它在车站遇见一个丢了回家车票的人，对方只记得站台有一盏蓝灯。",
        "choices": [
            {"text": "陪对方慢慢找线索", "skill": "heart", "modifier": 1},
            {"text": "先去问售票窗口和站务员", "skill": "wit", "modifier": 1},
            {"text": "留下一半干粮，继续赶路", "skill": "survival", "modifier": 0},
        ],
    },
    {
        "title": "暴雨前的山路",
        "urgency": "urgent",
        "dc": 14,
        "skill": "survival",
        "message": "天气忽然压低，山路旁的风像在推它。它打来电话，问要不要继续翻过垭口。",
        "choices": [
            {"text": "立刻下撤，找最近的屋檐", "skill": "survival", "modifier": 2},
            {"text": "沿原路前进，但每十分钟标记一次路", "skill": "wit", "modifier": 0},
            {"text": "相信直觉，跟着风声找捷径", "skill": "courage", "modifier": 1},
        ],
    },
    {
        "title": "夜市里的旧地图",
        "urgency": "normal",
        "dc": 13,
        "skill": "wit",
        "message": "一个摊主拿出手绘旧地图，说上面标着一处不在旅游册里的小路。",
        "choices": [
            {"text": "买下地图，明早再研究", "skill": "wit", "modifier": 1},
            {"text": "和摊主聊聊地图来历", "skill": "heart", "modifier": 1},
            {"text": "现在就去找那条小路", "skill": "courage", "modifier": 1},
        ],
    },
]


@dataclass
class Paths:
    root: Path
    life: Path
    diary: Path
    state: Path
    world: Path
    events: Path
    calls: Path


def paths(workspace: Path) -> Paths:
    life = workspace / STATE_DIR
    return Paths(
        root=workspace,
        life=life,
        diary=life / "diary",
        state=life / "state.json",
        world=life / "world.json",
        events=life / "events.jsonl",
        calls=life / "calls.jsonl",
    )


def ensure_dirs(p: Paths) -> None:
    p.diary.mkdir(parents=True, exist_ok=True)


def now_utc() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def iso_now() -> str:
    return now_utc().replace(microsecond=0).isoformat()


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def append_jsonl(path: Path, data: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(data, ensure_ascii=False) + "\n")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def rewrite_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )


def stable_rng(seed: str, *parts: Any) -> random.Random:
    text = "|".join([seed, *[str(part) for part in parts]])
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return random.Random(int(digest[:16], 16))


def pick(rng: random.Random, values: list[Any]) -> Any:
    return values[rng.randrange(len(values))]


def fetch_weather(location: dict[str, Any], offline: bool = False) -> dict[str, Any]:
    if offline:
        return {"source": "offline", "summary": "天气资料暂不可用，风从地图边缘吹来。"}
    query = urllib.parse.urlencode(
        {
            "latitude": location["lat"],
            "longitude": location["lon"],
            "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
            "timezone": location["timezone"],
        }
    )
    url = f"https://api.open-meteo.com/v1/forecast?{query}"
    try:
        with urllib.request.urlopen(url, timeout=8) as response:
            payload = json.loads(response.read().decode("utf-8"))
        current = payload.get("current", {})
        return {
            "source": "open-meteo",
            "temperature_c": current.get("temperature_2m"),
            "humidity": current.get("relative_humidity_2m"),
            "wind_kmh": current.get("wind_speed_10m"),
            "weather_code": current.get("weather_code"),
            "summary": describe_weather(current),
        }
    except Exception as exc:
        return {
            "source": "fallback",
            "summary": f"天气接口没有回应，记录为旅途中不确定的天气。({type(exc).__name__})",
        }


def describe_weather(current: dict[str, Any]) -> str:
    code = current.get("weather_code")
    temp = current.get("temperature_2m")
    wind = current.get("wind_speed_10m")
    code_words = {
        0: "晴朗",
        1: "大致晴朗",
        2: "有云",
        3: "阴天",
        45: "有雾",
        48: "雾凇",
        51: "小毛毛雨",
        53: "毛毛雨",
        55: "浓毛毛雨",
        61: "小雨",
        63: "雨",
        65: "大雨",
        71: "小雪",
        73: "雪",
        75: "大雪",
        80: "阵雨",
        95: "雷雨",
    }.get(code, "天气变化中")
    bits = [code_words]
    if temp is not None:
        bits.append(f"{temp}°C")
    if wind is not None:
        bits.append(f"风速 {wind} km/h")
    return "，".join(bits)


def init_state(args: argparse.Namespace) -> dict[str, Any]:
    p = paths(Path(args.workspace).resolve())
    ensure_dirs(p)
    if p.state.exists() and not args.force:
        raise SystemExit(f"state already exists: {p.state}")
    seed = args.seed or hashlib.sha256(iso_now().encode("utf-8")).hexdigest()[:12]
    rng = stable_rng(seed, "init")
    personality = pick(rng, PERSONALITIES)
    location = next((loc for loc in LOCATIONS if loc["name"].lower() == args.home.lower()), LOCATIONS[0])
    pet = {
        "name": args.name or pick(rng, ["阿苔", "小满", "云豆", "栗子", "米舟"]),
        "species": args.species or pick(rng, SPECIES),
        "personality": personality["name"],
        "voice": personality["voice"],
    }
    state = {
        "version": VERSION,
        "created_at": iso_now(),
        "last_advanced_date": None,
        "rng_seed": seed,
        "pet": pet,
        "traits": personality["traits"],
        "skills": {"pathfinding": 0, "foraging": 0, "story-listening": 0},
        "mood": "期待出门",
        "fatigue": 0,
        "home": location,
        "location": location,
        "inventory": ["小布包", "铅笔", "半块饼干"],
        "memories": [],
        "world_threads": [],
        "relationships": {},
    }
    world = {"version": VERSION, "visited": [location["name"]], "rumors": []}
    save_json(p.state, state)
    save_json(p.world, world)
    write_diary(
        p,
        dt.date.today().isoformat(),
        "# 第一页\n\n"
        f"{pet['name']}，一只{pet['species']}，把小布包放在门口。\n\n"
        f"它的性格是：{pet['personality']}。家在 {location['name']}, {location['country']}。\n\n"
        "它还没有出发，但已经把铅笔削尖了。\n",
    )
    return {"ok": True, "state": state, "path": str(p.life)}


def load_state_or_exit(p: Paths) -> dict[str, Any]:
    if not p.state.exists():
        raise SystemExit("No pet-life/state.json found. Run init first.")
    return load_json(p.state, {})


def write_diary(p: Paths, date_text: str, content: str) -> Path:
    ensure_dirs(p)
    path = p.diary / f"{date_text}.md"
    path.write_text(content, encoding="utf-8")
    return path


def choose_next_location(state: dict[str, Any], rng: random.Random) -> dict[str, Any]:
    current = state["location"]["name"]
    candidates = [loc for loc in LOCATIONS if loc["name"] != current]
    if state.get("fatigue", 0) >= 6 and rng.random() < 0.35:
        return state["home"]
    return pick(rng, candidates)


def advance(args: argparse.Namespace) -> dict[str, Any]:
    p = paths(Path(args.workspace).resolve())
    ensure_dirs(p)
    state = load_state_or_exit(p)
    auto = auto_resolve_pending(p, state, save=True)
    date_text = args.date or dt.date.today().isoformat()
    if state.get("last_advanced_date") == date_text and not args.force:
        return {
            "ok": True,
            "message": f"{date_text} already advanced. Use --force to rewrite.",
            "state": state,
            "auto_resolved": auto,
        }
    rng = stable_rng(state["rng_seed"], "advance", date_text, len(state.get("memories", [])))
    location = choose_next_location(state, rng)
    weather = fetch_weather(location, offline=args.offline)
    local_time = dt.datetime.now(ZoneInfo(location["timezone"])).replace(microsecond=0)
    event = make_daily_event(p, state, rng, date_text, args.force_call)
    memory = make_memory(state, location, weather, rng)
    state["location"] = location
    state["last_advanced_date"] = date_text
    state["fatigue"] = max(0, min(10, state.get("fatigue", 0) + rng.choice([-1, 0, 1, 2])))
    state["mood"] = rng.choice(["想家", "警觉", "开心", "有点累", "被风鼓励", "安静"])
    state["memories"] = (state.get("memories", []) + [memory])[-12:]
    world = load_json(p.world, {"version": VERSION, "visited": [], "rumors": []})
    if location["name"] not in world["visited"]:
        world["visited"].append(location["name"])
    if event:
        world["rumors"] = (world.get("rumors", []) + [event["title"]])[-20:]
    save_json(p.state, state)
    save_json(p.world, world)
    append_jsonl(
        p.events,
        {
            "type": "advance",
            "date": date_text,
            "location": location["name"],
            "weather": weather,
            "event_id": event["id"] if event else None,
            "created_at": iso_now(),
        },
    )
    diary_path = write_diary(
        p,
        date_text,
        render_diary(date_text, state, location, local_time, weather, memory, event, auto),
    )
    return {
        "ok": True,
        "date": date_text,
        "diary": str(diary_path),
        "event": event,
        "auto_resolved": auto,
        "state": state,
    }


def make_memory(
    state: dict[str, Any],
    location: dict[str, Any],
    weather: dict[str, Any],
    rng: random.Random,
) -> str:
    pet = state["pet"]["name"]
    fragments = [
        f"{pet}记住了{location['name']}空气里的一点味道：{location['terrain']}。",
        f"{pet}把今天的天气写在票根背面：{weather['summary']}。",
        f"{pet}在路边听见一个故事，暂时还不知道它是不是真的。",
        f"{pet}捡到一小段适合夹在日记里的光。",
    ]
    return pick(rng, fragments)


def make_daily_event(
    p: Paths,
    state: dict[str, Any],
    rng: random.Random,
    date_text: str,
    force_call: bool,
) -> dict[str, Any] | None:
    if not force_call and rng.random() > 0.42:
        return None
    return create_call(p, state, rng, date_text=date_text)


def create_call(
    p: Paths,
    state: dict[str, Any],
    rng: random.Random | None = None,
    date_text: str | None = None,
    template_name: str | None = None,
    deadline_minutes: int | None = None,
) -> dict[str, Any]:
    rng = rng or stable_rng(state["rng_seed"], "call", iso_now())
    template = next((item for item in EVENT_TEMPLATES if item["title"] == template_name), pick(rng, EVENT_TEMPLATES))
    created_at = now_utc().isoformat()
    urgency = template["urgency"]
    deadline = None
    if urgency == "urgent":
        minutes = 360 if deadline_minutes is None else deadline_minutes
        deadline = (now_utc() + dt.timedelta(minutes=minutes)).replace(microsecond=0).isoformat()
    call_id = hashlib.sha1(f"{created_at}|{template['title']}|{rng.random()}".encode("utf-8")).hexdigest()[:10]
    call = {
        "id": call_id,
        "status": "pending",
        "date": date_text or dt.date.today().isoformat(),
        "created_at": created_at,
        "deadline": deadline,
        "title": template["title"],
        "urgency": urgency,
        "message": template["message"],
        "dc": template["dc"],
        "default_skill": template["skill"],
        "choices": template["choices"],
    }
    append_jsonl(p.calls, call)
    append_jsonl(p.events, {"type": "call_created", "call_id": call_id, "title": call["title"], "created_at": iso_now()})
    return call


def render_diary(
    date_text: str,
    state: dict[str, Any],
    location: dict[str, Any],
    local_time: dt.datetime,
    weather: dict[str, Any],
    memory: str,
    event: dict[str, Any] | None,
    auto: list[dict[str, Any]],
) -> str:
    pet = state["pet"]
    quote = inspiration_line(state)
    event_text = ""
    if event:
        event_text = render_call_notice(event)
    auto_text = ""
    if auto:
        lines = [f"- {item['title']}：{item['outcome']}，{item['summary']}" for item in auto]
        auto_text = "\n## 自动处理的未接来电\n\n" + "\n".join(lines) + "\n"
    return textwrap.dedent(
        f"""\
        # {date_text} · {pet['name']}的旅行日记

        地点：{location['name']}, {location['country']}
        当地时间：{local_time.isoformat()}
        天气：{weather['summary']}
        心情：{state['mood']} · 疲劳：{state['fatigue']}/10

        {memory}

        它写道：

        > 今天的路不是很长，但世界把声音放得很低。{location['terrain']}。我在停下来的时候想起家，也想起还没有发生的事。

        灵感句：{quote}
        {event_text}{auto_text}
        """
    )


def render_call_notice(call: dict[str, Any]) -> str:
    choices = "\n".join(f"{idx + 1}. {choice['text']}" for idx, choice in enumerate(call["choices"]))
    deadline = f"\n截止：{call['deadline']}" if call.get("deadline") else ""
    return textwrap.dedent(
        f"""

        ## 电话

        来电：{call['title']}（{call['urgency']}）{deadline}

        {call['message']}

        可选回应：
        {choices}

        回应时使用：`answer --call-id {call['id']} --choice 1`
        """
    )


def inspiration_line(state: dict[str, Any]) -> str:
    if "温柔" in state["pet"]["personality"]:
        return "有些地方不是抵达的，是被记住以后才开始存在。"
    if "勇敢" in state["pet"]["personality"]:
        return "路先发出邀请，胆量随后才赶到。"
    if "路线师" in state["pet"]["personality"]:
        return "地图上的空白不是错误，是还没有被生活命名。"
    return "慢一点也没关系，世界经常在慢处露出线索。"


def status(args: argparse.Namespace) -> dict[str, Any]:
    p = paths(Path(args.workspace).resolve())
    state = load_state_or_exit(p)
    pending = [call for call in read_jsonl(p.calls) if call.get("status") == "pending"]
    result = {
        "ok": True,
        "pet": state["pet"],
        "location": state["location"],
        "mood": state["mood"],
        "fatigue": state["fatigue"],
        "memories": state.get("memories", [])[-3:],
        "pending_calls": pending,
    }
    if args.json:
        return result
    print_status(result)
    return result


def print_status(result: dict[str, Any]) -> None:
    pet = result["pet"]
    loc = result["location"]
    print(f"{pet['name']}（{pet['species']}）现在在 {loc['name']}, {loc['country']}。")
    print(f"心情：{result['mood']}；疲劳：{result['fatigue']}/10。")
    if result["pending_calls"]:
        print(f"未接/待处理电话：{len(result['pending_calls'])} 通。")
        for call in result["pending_calls"]:
            print(f"- {call['id']} {call['title']} ({call['urgency']})")
    else:
        print("没有未接来电。")


def answer(args: argparse.Namespace) -> dict[str, Any]:
    p = paths(Path(args.workspace).resolve())
    state = load_state_or_exit(p)
    calls = read_jsonl(p.calls)
    call = next((row for row in calls if row.get("id") == args.call_id), None)
    if not call:
        raise SystemExit(f"Call not found: {args.call_id}")
    if call.get("status") != "pending" and not args.force:
        raise SystemExit(f"Call is already {call.get('status')}. Use --force to reroll.")
    choice_index = args.choice - 1
    if choice_index < 0 or choice_index >= len(call["choices"]):
        raise SystemExit("Choice out of range.")
    rng = stable_rng(state["rng_seed"], "answer", call["id"], args.choice, args.roll or "")
    result = resolve_call(state, call, choice_index, rng, forced_roll=args.roll, automatic=False)
    update_call_rows(calls, call["id"], result["call"])
    rewrite_jsonl(p.calls, calls)
    save_json(p.state, result["state"])
    append_jsonl(p.events, {"type": "call_resolved", **result["event"]})
    append_resolution_to_diary(p, result)
    return {"ok": True, **result}


def resolve_call(
    state: dict[str, Any],
    call: dict[str, Any],
    choice_index: int,
    rng: random.Random,
    forced_roll: int | None = None,
    automatic: bool = False,
) -> dict[str, Any]:
    choice = call["choices"][choice_index]
    skill = choice.get("skill") or call.get("default_skill", "wit")
    roll = forced_roll if forced_roll is not None else rng.randint(1, 20)
    modifier = state.get("traits", {}).get(skill, 0) + choice.get("modifier", 0)
    total = roll + modifier
    outcome = classify_roll(roll, total, call["dc"])
    summary = outcome_summary(state, call, choice, outcome, automatic)
    state = dict(state)
    state["fatigue"] = max(0, min(10, state.get("fatigue", 0) + fatigue_delta(outcome)))
    state["mood"] = mood_after(outcome)
    state["memories"] = (state.get("memories", []) + [summary])[-12:]
    if outcome in ("critical_success", "success"):
        state.setdefault("skills", {})[skill] = state.setdefault("skills", {}).get(skill, 0) + 1
    resolved = dict(call)
    resolved.update(
        {
            "status": "auto_resolved" if automatic else "resolved",
            "resolved_at": iso_now(),
            "selected_choice": choice_index + 1,
            "selected_text": choice["text"],
            "roll": roll,
            "modifier": modifier,
            "total": total,
            "outcome": outcome,
            "summary": summary,
        }
    )
    event = {
        "call_id": call["id"],
        "title": call["title"],
        "choice": choice_index + 1,
        "roll": roll,
        "modifier": modifier,
        "total": total,
        "dc": call["dc"],
        "outcome": outcome,
        "summary": summary,
        "automatic": automatic,
        "created_at": iso_now(),
    }
    return {"state": state, "call": resolved, "event": event, "summary": summary, "outcome": outcome}


def classify_roll(roll: int, total: int, dc: int) -> str:
    if roll == 20 or total >= dc + 8:
        return "critical_success"
    if roll == 1 or total <= dc - 8:
        return "critical_failure"
    if total >= dc:
        return "success"
    if total >= dc - 3:
        return "mixed"
    return "failure"


def outcome_summary(
    state: dict[str, Any],
    call: dict[str, Any],
    choice: dict[str, Any],
    outcome: str,
    automatic: bool,
) -> str:
    pet = state["pet"]["name"]
    prefix = "因为没有等到你的回复，" if automatic else ""
    table = {
        "critical_success": f"{prefix}{pet}把事情办得比想象中更好，还得到一个新的线索。",
        "success": f"{prefix}{pet}稳稳处理了这件事，并把它记成一次小胜利。",
        "mixed": f"{prefix}{pet}做到了，但付出了一点代价，路也因此偏了一点。",
        "failure": f"{prefix}{pet}没能完全解决问题，只好带着遗憾继续走。",
        "critical_failure": f"{prefix}{pet}判断失误，事情留下了会在之后回响的裂缝。",
    }
    return f"{call['title']}：选择“{choice['text']}”。{table[outcome]}"


def fatigue_delta(outcome: str) -> int:
    return {
        "critical_success": -1,
        "success": 0,
        "mixed": 1,
        "failure": 2,
        "critical_failure": 3,
    }[outcome]


def mood_after(outcome: str) -> str:
    return {
        "critical_success": "兴奋",
        "success": "踏实",
        "mixed": "若有所思",
        "failure": "低落",
        "critical_failure": "惊魂未定",
    }[outcome]


def update_call_rows(rows: list[dict[str, Any]], call_id: str, new_call: dict[str, Any]) -> None:
    for index, row in enumerate(rows):
        if row.get("id") == call_id:
            rows[index] = new_call
            return


def append_resolution_to_diary(p: Paths, result: dict[str, Any]) -> None:
    date_text = dt.date.today().isoformat()
    path = p.diary / f"{date_text}.md"
    if not path.exists():
        write_diary(p, date_text, f"# {date_text} · 电话记录\n")
    with path.open("a", encoding="utf-8") as fh:
        event = result["event"]
        fh.write(
            textwrap.dedent(
                f"""

                ## 电话结果

                {event['title']}：d20={event['roll']}，修正={event['modifier']}，合计={event['total']}，DC={event['dc']}。

                结果：{event['outcome']}

                {event['summary']}
                """
            )
        )


def auto_resolve(args: argparse.Namespace) -> dict[str, Any]:
    p = paths(Path(args.workspace).resolve())
    state = load_state_or_exit(p)
    results = auto_resolve_pending(p, state, save=True)
    return {"ok": True, "resolved": results}


def auto_resolve_pending(p: Paths, state: dict[str, Any], save: bool) -> list[dict[str, Any]]:
    calls = read_jsonl(p.calls)
    changed = False
    results = []
    for call in calls:
        if call.get("status") != "pending" or not call.get("deadline"):
            continue
        deadline = dt.datetime.fromisoformat(call["deadline"])
        if deadline > now_utc():
            continue
        rng = stable_rng(state["rng_seed"], "auto", call["id"])
        choice_index = automatic_choice_index(state, call)
        result = resolve_call(state, call, choice_index, rng, automatic=True)
        state.clear()
        state.update(result["state"])
        call.update(result["call"])
        append_jsonl(p.events, {"type": "call_auto_resolved", **result["event"]})
        results.append({"title": call["title"], "outcome": result["outcome"], "summary": result["summary"]})
        changed = True
    if changed and save:
        rewrite_jsonl(p.calls, calls)
        save_json(p.state, state)
    return results


def automatic_choice_index(state: dict[str, Any], call: dict[str, Any]) -> int:
    traits = state.get("traits", {})
    best_score = -999
    best_index = 0
    for index, choice in enumerate(call["choices"]):
        skill = choice.get("skill", call.get("default_skill", "wit"))
        score = traits.get(skill, 0) + choice.get("modifier", 0)
        if score > best_score:
            best_score = score
            best_index = index
    return best_index


def create_call_command(args: argparse.Namespace) -> dict[str, Any]:
    p = paths(Path(args.workspace).resolve())
    ensure_dirs(p)
    state = load_state_or_exit(p)
    call = create_call(
        p,
        state,
        template_name=args.template,
        deadline_minutes=args.deadline_minutes,
    )
    return {"ok": True, "call": call}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Pet Adventure Life engine")
    parser.add_argument("--workspace", default=".", help="Workspace where pet-life data is stored")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init")
    init.add_argument("--name")
    init.add_argument("--species")
    init.add_argument("--home", default="Dali")
    init.add_argument("--seed")
    init.add_argument("--force", action="store_true")
    init.set_defaults(func=init_state)

    adv = sub.add_parser("advance")
    adv.add_argument("--date")
    adv.add_argument("--offline", action="store_true")
    adv.add_argument("--force", action="store_true")
    adv.add_argument("--force-call", action="store_true")
    adv.set_defaults(func=advance)

    st = sub.add_parser("status")
    st.add_argument("--json", action="store_true")
    st.set_defaults(func=status)

    call = sub.add_parser("call")
    call.add_argument("--template")
    call.add_argument("--deadline-minutes", type=int)
    call.set_defaults(func=create_call_command)

    ans = sub.add_parser("answer")
    ans.add_argument("--call-id", required=True)
    ans.add_argument("--choice", required=True, type=int)
    ans.add_argument("--roll", type=int)
    ans.add_argument("--force", action="store_true")
    ans.set_defaults(func=answer)

    auto = sub.add_parser("auto-resolve")
    auto.set_defaults(func=auto_resolve)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    result = args.func(args)
    if result is not None and (args.command != "status" or getattr(args, "json", False)):
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
