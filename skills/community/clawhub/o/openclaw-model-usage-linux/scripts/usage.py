#!/usr/bin/env python3
"""OpenClaw per-channel and per-model token usage analyzer - corrected version.

Fixes:
1. Uses sessionFile basename (not sessionId) to map filenames to channels.
2. Also maps sessionId for entries without sessionFile (cron/subagent).
3. Avoids double-counting by preferring .jsonl over .reset. for the same sid.
4. Robust channel detection from file content for orphaned sessions.
5. Adds per-model breakdown.
6. Uses cost.total when available instead of summing fields redundantly.
"""
import json
import os
import sys
import datetime
from collections import defaultdict

sessions_dir = os.path.expanduser('~/.openclaw/agents/main/sessions')
tz = datetime.timezone(datetime.timedelta(hours=8))

with open(os.path.join(sessions_dir, 'sessions.json')) as f:
    sessions_map = json.load(f)


def channel_from_key(key: str) -> str:
    """Map session key to channel label."""
    if 'qqbot' in key:
        return 'QQ'
    if 'weixin' in key or 'wechat' in key:
        return 'WeChat'
    if 'telegram' in key:
        return 'Telegram'
    if key == 'agent:main:main':
        return 'main'
    if key.startswith('agent:main:cron:'):
        return 'cron'
    if key.startswith('agent:main:subagent:'):
        return 'subagent'
    if 'heartbeat' in key:
        return 'main'
    return 'unknown'


# Two mapping tables:
# 1) file_to_channel: basename of sessionFile -> channel (handles most .jsonl files)
# 2) sid_to_channel: sessionId -> channel (handles cron/subagent where sessionFile is empty)
file_to_channel = {}
sid_to_channel = {}

for key, info in sessions_map.items():
    ch = channel_from_key(key)
    sid = info.get('sessionId', '')
    session_file = info.get('sessionFile', '')

    if sid:
        sid_to_channel[sid] = ch

    if session_file:
        filename = os.path.basename(session_file).replace('.jsonl', '')
        file_to_channel[filename] = ch

# Build a deduplicated file list: prefer .jsonl over .reset. for the same sid
raw_files = [f for f in os.listdir(sessions_dir) if f.endswith('.jsonl') or '.reset.' in f]

sid_to_files = defaultdict(list)
for fname in raw_files:
    sid = fname.replace('.jsonl', '').split('.reset.')[0]
    sid_to_files[sid].append(fname)

selected_files = []
for sid, files in sid_to_files.items():
    jsonl_files = [f for f in files if f.endswith('.jsonl')]
    if jsonl_files:
        # If a normal .jsonl exists, use it and ignore .reset. files
        selected_files.extend(jsonl_files)
    else:
        # Otherwise use the .reset. files
        selected_files.extend(files)


def parse_timestamp(ts):
    """Parse timestamp which can be string (ISO) or int (ms)."""
    if isinstance(ts, str) and ts.startswith("20"):
        dt = datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return dt.astimezone(tz).strftime("%Y-%m-%d")
    elif isinstance(ts, (int, float)):
        if ts > 1e12:
            dt = datetime.datetime.fromtimestamp(ts / 1000, tz=tz)
        else:
            dt = datetime.datetime.fromtimestamp(ts, tz=tz)
        return dt.strftime("%Y-%m-%d")
    return None


def detect_channel_from_file(path):
    """Detect channel from file content for orphaned sessions."""
    try:
        with open(path) as f:
            for i, line in enumerate(f):
                if i > 200:
                    break
                line = line.strip()
                if not line:
                    continue
                obj = json.loads(line)
                if obj.get("type") != "message":
                    continue
                msg = obj.get("message", {})
                content = msg.get("content", [])
                if isinstance(content, list):
                    text = " ".join([c.get("text", "") for c in content if isinstance(c, dict)])
                else:
                    text = str(content)

                text_lower = text.lower()

                # Strong signals
                if "[QQBot]" in text or "qqbot" in text_lower:
                    return "QQ"
                if "openclaw-weixin" in text_lower or "[微信]" in text or "wechat" in text_lower:
                    return "WeChat"
                if "telegram" in text_lower or "@D4rchr0w_bot" in text:
                    return "Telegram"
                if text.startswith("[cron:"):
                    return "cron"
                if "heartbeat" in text_lower and "checklist" in text_lower:
                    return "main"
                # /reset without channel prefix usually means main
                if text.startswith("/reset") and not any(x in text for x in ["[QQBot]", "[cron:", "[微信]"]):
                    return "main"
    except Exception:
        pass
    return "unknown"


def analyze_file(path):
    stats = {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0, "cost": 0.0, "turns": 0}
    daily = {}
    model_stats = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if obj.get("type") != "message":
                continue
            msg = obj.get("message", {})
            if msg.get("role") != "assistant":
                continue

            usage = msg.get("usage", {})
            cost_data = usage.get("cost", {})
            inp = usage.get("input", 0)
            out = usage.get("output", 0)
            cr = usage.get("cacheRead", 0)
            cw = usage.get("cacheWrite", 0)

            if isinstance(cost_data, dict):
                # Prefer total when available (it's the actual computed cost)
                c = cost_data.get("total")
                if c is None:
                    c = cost_data.get("input", 0) + cost_data.get("output", 0) + cost_data.get("cacheRead", 0) + cost_data.get("cacheWrite", 0)
            else:
                c = cost_data if isinstance(cost_data, (int, float)) else 0

            stats["input"] += inp
            stats["output"] += out
            stats["cacheRead"] += cr
            stats["cacheWrite"] += cw
            stats["cost"] += c
            stats["turns"] += 1

            ts = msg.get("timestamp")
            date = parse_timestamp(ts)
            if date:
                if date not in daily:
                    daily[date] = {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0, "cost": 0.0, "turns": 0}
                daily[date]["input"] += inp
                daily[date]["output"] += out
                daily[date]["cacheRead"] += cr
                daily[date]["cacheWrite"] += cw
                daily[date]["cost"] += c
                daily[date]["turns"] += 1

            model = msg.get("model", "unknown")
            provider = msg.get("provider", "")
            if model and model != "unknown":
                model_key = f"{provider}/{model}" if provider else model
            else:
                model_key = "unknown"

            if model_key not in model_stats:
                model_stats[model_key] = {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0, "cost": 0.0, "turns": 0}
            model_stats[model_key]["input"] += inp
            model_stats[model_key]["output"] += out
            model_stats[model_key]["cacheRead"] += cr
            model_stats[model_key]["cacheWrite"] += cw
            model_stats[model_key]["cost"] += c
            model_stats[model_key]["turns"] += 1

    return stats, daily, model_stats


# Channel data
ch_data = {}
ch_daily = {}
model_data = {}
orphan_files = []

for fname in sorted(selected_files):
    sid = fname.replace('.jsonl', '').split('.reset.')[0]

    if fname.endswith('.jsonl'):
        # Normal file: try file_to_channel first, then sid_to_channel
        ch = file_to_channel.get(sid, sid_to_channel.get(sid, 'unknown'))
        if ch == 'unknown':
            # Last resort: detect from content
            path = os.path.join(sessions_dir, fname)
            ch = detect_channel_from_file(path)
            if ch == 'unknown':
                orphan_files.append(fname)
    else:
        # .reset. file: detect from content
        path = os.path.join(sessions_dir, fname)
        ch = detect_channel_from_file(path)
        if ch == 'unknown':
            ch = sid_to_channel.get(sid, 'unknown')
        if ch == 'unknown':
            orphan_files.append(fname)

    if ch not in ch_data:
        ch_data[ch] = {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0, "cost": 0.0, "turns": 0}
        ch_daily[ch] = {}

    path = os.path.join(sessions_dir, fname)
    stats, daily, mstats = analyze_file(path)
    for k in stats:
        ch_data[ch][k] += stats[k]
    for date, d in daily.items():
        if date not in ch_daily[ch]:
            ch_daily[ch][date] = {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0, "cost": 0.0, "turns": 0}
        for k in d:
            ch_daily[ch][date][k] += d[k]

    for mkey, m in mstats.items():
        if mkey not in model_data:
            model_data[mkey] = {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0, "cost": 0.0, "turns": 0}
        for k in m:
            model_data[mkey][k] += m[k]

# Persistent offset tracking to handle session resets
offset_file = os.path.expanduser('~/.openclaw/workspace/skills/model-usage-linux/reset_offsets.json')
snapshot_file = os.path.expanduser('~/.openclaw/workspace/skills/model-usage-linux/last_snapshot.json')

offsets = {}
snapshot = {}
if os.path.exists(offset_file):
    with open(offset_file) as f:
        offsets = json.load(f)
if os.path.exists(snapshot_file):
    with open(snapshot_file) as f:
        snapshot = json.load(f)

# Detect resets and update offsets
for ch in list(ch_data.keys()):
    curr = ch_data.get(ch, {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0, "cost": 0.0, "turns": 0})
    prev = snapshot.get(ch, {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0, "cost": 0.0, "turns": 0})

    if curr['turns'] < prev['turns']:
        if ch not in offsets:
            offsets[ch] = {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0, "cost": 0.0, "turns": 0}
        for k in offsets[ch]:
            offsets[ch][k] += prev[k] - curr[k]

# Save updated offsets and RAW snapshot (before applying offsets)
with open(offset_file, 'w') as f:
    json.dump(offsets, f)

new_snapshot = {}
for ch in list(ch_data.keys()):
    new_snapshot[ch] = ch_data.get(ch, {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0, "cost": 0.0, "turns": 0}).copy()
with open(snapshot_file, 'w') as f:
    json.dump(new_snapshot, f)

# Apply offsets to current data (totals only, not daily breakdown)
for ch in list(ch_data.keys()):
    if ch in offsets:
        for k in ch_data.get(ch, {}):
            ch_data[ch][k] += offsets[ch][k]

# Total data
total_data = {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0, "cost": 0.0, "turns": 0}
total_daily = {}
for ch in ch_data:
    for k in total_data:
        total_data[k] += ch_data[ch][k]
    for date, d in ch_daily[ch].items():
        if date not in total_daily:
            total_daily[date] = {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0, "cost": 0.0, "turns": 0}
        for k in d:
            total_daily[date][k] += d[k]

all_dates = sorted(total_daily.keys())


def fmt(n):
    if n >= 1_000_000_000:
        return f"{n/1_000_000_000:.2f}B"
    elif n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    elif n >= 1_000:
        return f"{n/1_000:.0f}K"
    return str(int(n))


CNY_RATE = 7.2

# Load previous data for incremental comparison
prev_file = os.path.expanduser('~/.openclaw/workspace/skills/model-usage-linux/last_usage.json')
prev_data = {}
if os.path.exists(prev_file):
    with open(prev_file) as f:
        prev_data = json.load(f)

print()
print("+=== OpenClaw 完整用量统计 ===+")
print()
if all_dates:
    print(f"  统计周期: {all_dates[0]} ~ {all_dates[-1]}（共 {len(all_dates)} 天）")
else:
    print("  统计周期: 无数据")
print()
print(f"  总费用（RMB）: ¥{total_data['cost']*CNY_RATE:.2f}")
print(f"  总输入（tokens）: {fmt(total_data['input'])}")
print(f"  总输出（tokens）: {fmt(total_data['output'])}")
print()

print("+=== 每日费用（最近 3 天）===+")
print()
for date in all_dates[-3:]:
    d = total_daily[date]
    if d["turns"] == 0:
        continue
    print(f"  {date} | {d['turns']} 轮 | ¥{d['cost']*CNY_RATE:.2f}")
print()

print("+=== 各渠道用量 ===+")
print()
print(f"  {'渠道':<12} {'轮次':>8} {'总输入':>14} {'总输出':>12} {'缓存率':>8} {'费用(¥)':>12} {'每轮(¥)':>10}")
print(f"  {'-'*80}")
for ch in sorted(ch_data.keys()):
    if ch_data[ch]["turns"] == 0:
        continue
    c = ch_data[ch]
    cr = c["cacheRead"]/c["input"]*100 if c["input"] > 0 else 0
    cost_per_turn = c["cost"]*CNY_RATE/c["turns"] if c["turns"] > 0 else 0
    print(f"  {ch:<12} {c['turns']:>8} {fmt(c['input']):>14} {fmt(c['output']):>12} {cr:>7.0f}%  ¥{c['cost']*CNY_RATE:>10.2f}  ¥{cost_per_turn:.4f}")
print(f"  {'-'*84}")
cr_t = total_data["cacheRead"]/total_data["input"]*100 if total_data["input"] > 0 else 0
print(f"  {'合计':<12} {total_data['turns']:>8} {fmt(total_data['input']):>14} {fmt(total_data['output']):>12} {cr_t:>7.0f}%  ¥{total_data['cost']*CNY_RATE:>10.2f}")
print()

print("+=== 各模型用量 ===+")
print()
print(f"  {'模型':<40} {'轮次':>8} {'总输入':>14} {'总输出':>12} {'费用(¥)':>12} {'占比':>8}")
print(f"  {'-'*94}")
sorted_models = sorted(model_data.items(), key=lambda x: x[1]["cost"], reverse=True)
for model_key, m in sorted_models:
    if m["turns"] == 0 or model_key == "openclaw/delivery-mirror":
        continue
    pct = m["cost"] / total_data["cost"] * 100 if total_data["cost"] > 0 else 0
    print(f"  {model_key:<40} {m['turns']:>8} {fmt(m['input']):>14} {fmt(m['output']):>12} ¥{m['cost']*CNY_RATE:>10.2f} {pct:>7.1f}%")
print(f"  {'-'*98}")
print()

print("+=== 各渠道每日详情（最近 3 天）===+")
for ch in sorted(ch_data.keys()):
    if ch_data[ch]["turns"] == 0:
        continue
    c = ch_data[ch]
    cr_ch = c["cacheRead"]/c["input"]*100 if c["input"] > 0 else 0
    print(f"\n  {ch}（共） | 对话：{c['turns']} 轮 | 费用（RMB）：¥{c['cost']*CNY_RATE:.2f} | 输入（tokens）：{fmt(c['input'])} | 输出（tokens）：{fmt(c['output'])} | 缓存率 {cr_ch:.0f}%")
    for date in all_dates[-3:]:
        if date in ch_daily[ch] and ch_daily[ch][date]["turns"] > 0:
            d = ch_daily[ch][date]
            cr = d["cacheRead"]/d["input"]*100 if d["input"] > 0 else 0
            print(f"    {date} | 对话：{d['turns']} 轮 | 费用（RMB）：¥{d['cost']*CNY_RATE:.2f} | 输入（tokens）：{fmt(d['input'])} | 输出（tokens）：{fmt(d['output'])} | 缓存率 {cr:.0f}%")
print()

print("+=== 关键分析 ===+")
print()
days = len(all_dates) if all_dates else 1
print(f"  日均轮次: {total_data['turns']/days:.0f} 轮/天")
print(f"  日均费用: ¥{total_data['cost']*CNY_RATE/days:.2f}/天")
print(f"  单轮平均: {fmt((total_data['input']+total_data['output'])/total_data['turns'])} tokens/轮")
print(f"  单轮平均费用: ¥{total_data['cost']*CNY_RATE/total_data['turns']:.4f}/轮")
print()
print(f"  费用占比:")
total_cost_cny = total_data['cost'] * CNY_RATE
for ch in sorted(ch_data.keys()):
    if ch_data[ch]["cost"] == 0:
        continue
    pct = ch_data[ch]["cost"] * CNY_RATE / total_cost_cny * 100
    print(f"    {ch:<10} ¥{ch_data[ch]['cost']*CNY_RATE:>8.2f}  ({pct:5.1f}%)")

if orphan_files:
    print()
    print(f"  ⚠️  无法识别渠道的文件数: {len(orphan_files)}")
    for f in orphan_files[:5]:
        print(f"    - {f}")
    if len(orphan_files) > 5:
        print(f"    ... 等共 {len(orphan_files)} 个文件")

print()
print("+=== 较上次查询增量 ===+")
print()
if prev_data:
    for ch in sorted(ch_data.keys()):
        if ch_data[ch]["turns"] == 0:
            continue
        prev_ch = prev_data.get('ch_data', {}).get(ch, {})
        if prev_ch:
            turns_diff = ch_data[ch]["turns"] - prev_ch.get("turns", 0)
            cost_diff = (ch_data[ch]["cost"] - prev_ch.get("cost", 0)) * CNY_RATE
            if turns_diff != 0 or cost_diff != 0:
                sign = '+' if cost_diff >= 0 else ''
                t_sign = '+' if turns_diff >= 0 else ''
                c_sign = '+' if cost_diff >= 0 else ''
                print(f"  {ch}: {t_sign} {turns_diff} 轮，{c_sign} ¥{cost_diff:.2f}")
    total_diff = (total_data["cost"] - prev_data.get("total", {}).get("cost", 0)) * CNY_RATE
    total_turns_diff = total_data["turns"] - prev_data.get("total", {}).get("turns", 0)
    t_sign = '+' if total_turns_diff >= 0 else ''
    c_sign = '+' if total_diff >= 0 else ''
    print(f"  合计 | {t_sign} {total_turns_diff} 轮 | {c_sign} ¥{total_diff:.2f}")
else:
    print("  (无历史数据)")

print()

# Save current data for next comparison (include model data)
save_data = {
    "ch_data": ch_data,
    "total": total_data,
    "all_dates": all_dates,
    "model_data": model_data,
}
with open(prev_file, 'w') as f:
    json.dump(save_data, f)
