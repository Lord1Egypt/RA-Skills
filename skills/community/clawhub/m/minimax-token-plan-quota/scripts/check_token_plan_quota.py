#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

CN_ENDPOINT = "https://www.minimaxi.com/v1/api/openplatform/coding_plan/remains"
GLOBAL_ENDPOINT = "https://www.minimax.io/v1/api/openplatform/coding_plan/remains"
ENV_FILE_HINT = "~/.openclaw/.env"
DEFAULT_ENV_FILE = os.path.expanduser(ENV_FILE_HINT)


def ms_to_human(ms):
    if not isinstance(ms, (int, float)) or ms < 0:
        return "-"
    total_seconds = int(ms // 1000)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    if hours and minutes:
        return f"{hours}小时{minutes}分钟"
    if hours:
        return f"{hours}小时"
    return f"{minutes}分钟"


def parse_simple_env_file(path):
    values = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            for raw_line in f:
                line = raw_line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                if not key:
                    continue
                if value and value[0] == value[-1] and value[0] in {'"', "'"}:
                    value = value[1:-1]
                values[key] = value
    except FileNotFoundError:
        return {}
    return values


def resolve_api_key(cli_api_key):
    if cli_api_key:
        return cli_api_key

    env_api_key = os.environ.get("MINIMAX_API_KEY")
    if env_api_key:
        return env_api_key

    return parse_simple_env_file(DEFAULT_ENV_FILE).get("MINIMAX_API_KEY")


def print_missing_key_guidance():
    print("missing MINIMAX_API_KEY", file=sys.stderr)
    if not os.path.exists(DEFAULT_ENV_FILE):
        print(
            f"未找到 {ENV_FILE_HINT}（实际路径：{DEFAULT_ENV_FILE}）。请先创建并填写，例如：",
            file=sys.stderr,
        )
        print(
            'mkdir -p ~/.openclaw && printf "MINIMAX_API_KEY=你的key\\n" > ~/.openclaw/.env',
            file=sys.stderr,
        )
    else:
        print(
            f"已找到 {ENV_FILE_HINT}（实际路径：{DEFAULT_ENV_FILE}），但里面没有 MINIMAX_API_KEY。请补一行：",
            file=sys.stderr,
        )
        print("MINIMAX_API_KEY=你的key", file=sys.stderr)


def fetch(endpoint, api_key):
    req = urllib.request.Request(
        endpoint,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "curl/8.5.0",
        },
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def classify_rows(model_remains):
    rows = []
    for item in model_remains:
        name = item.get("model_name", "未知模型")
        interval_total = item.get("current_interval_total_count", 0)
        interval_remaining = item.get("current_interval_usage_count", 0)
        weekly_total = item.get("current_weekly_total_count", 0)
        weekly_remaining = item.get("current_weekly_usage_count", 0)
        reset_in = ms_to_human(item.get("remains_time"))

        if interval_total:
            rows.append({
                "项目": name,
                "周期": "当前周期",
                "总额度": interval_total,
                "剩余额度": interval_remaining,
                "重置剩余时间": reset_in,
            })
        else:
            rows.append({
                "项目": name,
                "周期": "当前周期",
                "总额度": 0,
                "剩余额度": 0,
                "重置剩余时间": reset_in,
            })

        if weekly_total:
            rows.append({
                "项目": name,
                "周期": "本周",
                "总额度": weekly_total,
                "剩余额度": weekly_remaining,
                "重置剩余时间": ms_to_human(item.get("weekly_remains_time")),
            })
    return rows


def rows_to_markdown(rows):
    out = ["| 项目 | 周期 | 总额度 | 剩余额度 | 重置剩余时间 |", "|---|---|---:|---:|---|"]
    for row in rows:
        out.append(
            f"| {row['项目']} | {row['周期']} | {row['总额度']} | {row['剩余额度']} | {row['重置剩余时间']} |"
        )
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="Check MiniMax Token Plan remaining quota")
    ap.add_argument("--api-key", help="MiniMax Token Plan API key; falls back to MINIMAX_API_KEY")
    ap.add_argument("--region", choices=["cn", "global"], default="cn")
    ap.add_argument("--json", action="store_true", help="Print raw normalized JSON")
    args = ap.parse_args()

    api_key = resolve_api_key(args.api_key)
    if not api_key:
        print_missing_key_guidance()
        raise SystemExit(1)

    endpoint = CN_ENDPOINT if args.region == "cn" else GLOBAL_ENDPOINT
    try:
        data = fetch(endpoint, api_key)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(json.dumps({"ok": False, "status": e.code, "body": body[:2000]}, ensure_ascii=False, indent=2))
        raise SystemExit(2)

    rows = classify_rows(data.get("model_remains", []))
    result = {
        "region": args.region,
        "endpoint": endpoint,
        "rows": rows,
        "raw": data,
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(rows_to_markdown(rows))


if __name__ == "__main__":
    main()
