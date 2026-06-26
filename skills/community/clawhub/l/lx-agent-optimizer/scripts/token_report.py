#!/usr/bin/env python3
"""
OpenClaw Token 消耗周报脚本
统计近7天各模型、各日期的 token 消耗
"""
import json, os
from datetime import datetime, timedelta, timezone

week_ago = datetime.now(timezone.utc) - timedelta(days=7)
by_day = {}
by_model = {}

for sessions_dir in [
    os.path.expanduser('~/.openclaw/agents/work/sessions'),
    os.path.expanduser('~/.openclaw/agents/main/sessions'),
]:
    if not os.path.exists(sessions_dir):
        continue
    for f in os.listdir(sessions_dir):
        if not f.endswith('.jsonl'):
            continue
        path = os.path.join(sessions_dir, f)
        try:
            with open(path) as fp:
                for line in fp:
                    try:
                        d = json.loads(line.strip())
                        if d.get('type') == 'message':
                            msg = d.get('message', {})
                            if msg.get('role') == 'assistant' and 'usage' in msg:
                                u = msg['usage']
                                ts = d.get('timestamp', '')
                                model = msg.get('model', 'unknown')
                                if ts:
                                    dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                                    if dt > week_ago:
                                        dt_sh = dt + timedelta(hours=8)
                                        day = dt_sh.strftime('%m-%d')
                                        for dic in [by_day.setdefault(day, {}), by_model.setdefault(model, {})]:
                                            dic['input'] = dic.get('input', 0) + u.get('input', 0)
                                            dic['output'] = dic.get('output', 0) + u.get('output', 0)
                                            dic['cacheRead'] = dic.get('cacheRead', 0) + u.get('cacheRead', 0)
                                            dic['cacheWrite'] = dic.get('cacheWrite', 0) + u.get('cacheWrite', 0)
                    except:
                        pass
        except:
            pass

# 计算汇总
total_input = sum(v.get('input', 0) for v in by_day.values())
total_output = sum(v.get('output', 0) for v in by_day.values())
total_cache_read = sum(v.get('cacheRead', 0) for v in by_day.values())
total_cache_write = sum(v.get('cacheWrite', 0) for v in by_day.values())
total_all = total_input + total_output + total_cache_read + total_cache_write
cache_hit_rate = total_cache_read / (total_input + total_cache_read) * 100 if (total_input + total_cache_read) > 0 else 0

print("📊 Token 周报（近7天）\n")

print("【按日期】")
for day in sorted(by_day.keys()):
    v = by_day[day]
    t = v.get('input', 0) + v.get('output', 0) + v.get('cacheRead', 0) + v.get('cacheWrite', 0)
    out_ratio = v.get('output', 0) / t * 100 if t > 0 else 0
    cache_ratio = (v.get('cacheRead', 0) + v.get('cacheWrite', 0)) / t * 100 if t > 0 else 0
    print(f"  {day}：{t:,} tokens（输出 {out_ratio:.0f}%，缓存 {cache_ratio:.0f}%）")

print("\n【按模型】")
for model, v in sorted(by_model.items(), key=lambda x: -(x[1].get('input', 0) + x[1].get('output', 0) + x[1].get('cacheRead', 0) + x[1].get('cacheWrite', 0))):
    t = v.get('input', 0) + v.get('output', 0) + v.get('cacheRead', 0) + v.get('cacheWrite', 0)
    ratio = t / total_all * 100 if total_all > 0 else 0
    short_model = model.split('/')[-1] if '/' in model else model
    print(f"  {short_model}：{t:,} tokens（占 {ratio:.0f}%）")

print(f"\n【总计】")
print(f"  总 tokens：{total_all:,}")
print(f"  缓存命中率：{cache_hit_rate:.0f}%")

if cache_hit_rate >= 70:
    print(f"  评价：✅ 缓存利用率高，成本控制良好")
elif cache_hit_rate >= 40:
    print(f"  评价：🟡 缓存命中率一般，有优化空间")
else:
    print(f"  评价：⚠️ 缓存命中率低，建议减少新 session 创建频率")
