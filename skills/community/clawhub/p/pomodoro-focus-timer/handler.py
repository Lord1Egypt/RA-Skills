"""Pomodoro Focus Timer - 番茄专注计时器"""
import json
import re

def parse_pomodoro_input(text):
    result = {"task": None, "duration": 25, "break_duration": 5, "rounds": 4}
    m = re.search(r'(\d+)\s*分钟', text)
    if m: result["duration"] = int(m.group(1))
    skip_kw = ["番茄", "计时", "专注", "工作"]
    task = text
    for kw in skip_kw: task = task.replace(kw, "")
    task = re.sub(r'\d+\s*分钟', '', task)
    result["task"] = task.strip()[:50]
    return result

def generate_pomodoro_plan(task, duration, break_dur, rounds):
    sessions = []
    for r in range(rounds):
        sessions.append({"session": r+1, "type": "focus", "duration_minutes": duration, "task": task if r == 0 else None})
        if r < rounds - 1:
            sessions.append({"session": r+1, "type": "break", "duration_minutes": break_dur, "activity": "起身活动、喝水、眺望远处"})
    return {"sessions": sessions, "summary": {"total_focus_minutes": duration*rounds}}

def handle(text):
    parsed = parse_pomodoro_input(text)
    plan = generate_pomodoro_plan(parsed["task"] or "未命名任务", parsed["duration"], parsed["break_duration"], parsed["rounds"])
    return {"task": parsed["task"] or "未命名任务", "pomodoroPlan": plan, "timer_settings": {"focus_duration": parsed["duration"]}, "message": "番茄钟已设置"}

if __name__ == "__main__":
    tc = "我要写报告，25分钟一个番茄"
    r = handle(tc)
    print(f'OK: task={r["task"]}, duration={r["timer_settings"]["focus_duration"]}min')
