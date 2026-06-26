# 定时调度规范

## 一、调度架构

```
┌──────────────────────────────────────────┐
│           OpenClaw Cron Runtime            │
├──────────────────────────────────────────┤
│  Schedule Config (config/schedule.yaml)   │
│           ↓                               │
│  Cron Trigger → Pre-check → Jitter Delay │
│           ↓                               │
│  Session Launcher → xhs-nurture Skill     │
│           ↓                               │
│  Post-session → Log + Report + Notify     │
└──────────────────────────────────────────┘
```

---

## 二、调度配置

### 2.1 配置文件格式 (`config/schedule.yaml`)

```yaml
scheduler:
  enabled: true
  timezone: "Asia/Shanghai"
  
  # 全局约束
  constraints:
    # 每日最大会话数
    max_sessions_per_day: 3
    # 会话间最小间隔（分钟）
    min_session_gap_minutes: 120
    # 启动时间抖动（避免固定时间模式）
    start_jitter_minutes: 10
    # 周末策略
    weekend_mode: "reduced"   # normal | reduced | off
    weekend_multiplier: 0.6   # reduced 模式下配额乘数
  
  # 定时任务列表
  plans:
    - id: "morning"
      name: "上午互动"
      cron: "30 9 * * *"              # 每天 9:30
      account: "default"
      mode: "discover_feed"
      duration_minutes: 30
      enabled: true
      
    - id: "afternoon"
      name: "下午精准互动"
      cron: "0 14 * * 1-5"           # 工作日 14:00
      account: "default"
      mode: "search"
      duration_minutes: 25
      enabled: true
      
    - id: "evening"
      name: "晚间引流"
      cron: "30 20 * * *"            # 每天 20:30
      account: "default"
      mode: "user_profile"
      duration_minutes: 40
      enabled: true
      
    - id: "account2_morning"
      name: "账号2上午"
      cron: "0 10 * * *"             # 每天 10:00
      account: "account-2"
      mode: "discover_feed"
      duration_minutes: 25
      enabled: false                  # 默认关闭

  # 特殊日期规则
  special_dates:
    - date: "2026-05-20"
      action: "skip"                  # 跳过（如遇到平台活动/严查期）
      reason: "平台活动日，暂停自动互动"
    
    - date: "2026-06-01"
      action: "boost"                 # 加量
      multiplier: 1.3
      reason: "内容推广期"
```

---

## 三、调度执行流程

### 3.1 Cron 触发流程

```python
def on_cron_trigger(plan):
    """Cron 触发时的执行流程"""
    
    # === Phase 1: 前置检查 ===
    checks = pre_flight_checks(plan)
    if not checks.passed:
        log_skip(plan, checks.reason)
        notify_if_important(checks)
        return
    
    # === Phase 2: 启动抖动 ===
    jitter = random_uniform(0, plan.constraints.start_jitter_minutes * 60)
    wait(jitter)
    
    # === Phase 3: 二次检查（抖动后再确认）===
    checks = pre_flight_checks(plan)
    if not checks.passed:
        log_skip(plan, checks.reason)
        return
    
    # === Phase 4: 启动会话 ===
    session = start_nurture_session(plan)
    
    # === Phase 5: 会话结束处理 ===
    post_session(session, plan)
```

### 3.2 前置检查

```python
def pre_flight_checks(plan):
    """启动前的所有检查"""
    results = CheckResults()
    
    # 1. 浏览器是否打开
    if not is_browser_connected():
        results.fail("browser_not_open", "浏览器未连接")
        return results
    
    # 2. 小红书是否可访问
    try:
        navigate("https://www.xiaohongshu.com")
        wait(3)
    except:
        results.fail("site_unreachable", "小红书无法访问")
        return results
    
    # 3. 登录态检查
    if not is_logged_in():
        results.fail("not_logged_in", "未登录或登录已过期")
        return results
    
    # 4. 目标账号检查
    current_account = detect_current_account()
    if current_account != plan.account:
        # 尝试切换
        if not can_switch_now():
            results.fail("wrong_account", f"当前账号非 {plan.account}，无法切换")
            return results
    
    # 5. 每日限额检查
    counters = load_today_counters(today_str(), plan.account)
    limits = get_limits_for_account(plan.account)
    remaining = get_remaining_quota(counters, limits)
    
    if remaining["total"] <= 0:
        results.fail("quota_exhausted", "今日配额已用完")
        return results
    
    # 6. 会话间隔检查
    last_session = get_last_session_end_time(plan.account)
    if last_session:
        gap = (now() - last_session).total_seconds() / 60
        if gap < plan.constraints.min_session_gap_minutes:
            results.fail("too_soon", f"距上次会话仅 {int(gap)} 分钟")
            return results
    
    # 7. 每日会话次数检查
    today_sessions = count_today_sessions(plan.account)
    if today_sessions >= plan.constraints.max_sessions_per_day:
        results.fail("max_sessions", "今日会话次数已达上限")
        return results
    
    # 8. 特殊日期检查
    special = check_special_date(today_str(), plan.special_dates)
    if special and special.action == "skip":
        results.fail("special_date_skip", special.reason)
        return results
    
    # 9. 账号健康度检查
    health = AccountHealthMonitor(plan.account)
    should_pause, reason = health.should_pause()
    if should_pause:
        results.fail("health_low", reason)
        return results
    
    results.pass_all()
    return results
```

### 3.3 会话启动

```python
def start_nurture_session(plan):
    """启动养号互动会话"""
    # 构造会话参数
    session_config = {
        "account": plan.account,
        "mode": plan.mode,
        "duration": plan.duration_minutes,
        "source": "scheduled",  # 标记为定时触发
    }
    
    # 周末降级处理
    if is_weekend() and plan.constraints.weekend_mode == "reduced":
        session_config["duration"] = int(
            plan.duration_minutes * plan.constraints.weekend_multiplier
        )
    
    # 特殊日期 boost
    special = check_special_date(today_str(), plan.special_dates)
    if special and special.action == "boost":
        session_config["boost_multiplier"] = special.multiplier
    
    # 启动（调用 SKILL.md 中的主流程）
    return execute_nurture_session(session_config)
```

### 3.4 会话后处理

```python
def post_session(session, plan):
    """会话结束后的处理"""
    # 1. 记录调度日志
    schedule_log = {
        "plan_id": plan.id,
        "account": plan.account,
        "trigger_time": plan.trigger_time,
        "actual_start": session.start_time,
        "end_time": session.end_time,
        "duration_minutes": session.actual_duration_minutes,
        "actions_completed": session.counters,
        "status": session.status,
        "errors": session.errors,
    }
    append_to_log("data/nurture-log/schedule-history.jsonl", schedule_log)
    
    # 2. 生成通知摘要
    summary = format_session_summary(session)
    
    # 3. 异常通知
    if session.status != "completed_normally":
        notify_user(f"定时任务 [{plan.name}] 异常结束: {session.status}\n{summary}")
    
    # 4. 更新报告（如果是当天最后一个计划任务）
    if is_last_planned_session_today(plan):
        generate_daily_report(today_str(), plan.account)
```

---

## 四、调度管理命令

### 用户可用命令

| 指令 | 说明 |
|------|------|
| "查看定时任务" | 列出所有计划任务及状态 |
| "添加定时任务" | 交互式创建新的定时计划 |
| "修改定时任务 X" | 修改指定任务的参数 |
| "暂停定时任务 X" | 临时禁用某个任务 |
| "恢复定时任务 X" | 重新启用某个任务 |
| "暂停所有定时" | 全部暂停 |
| "查看调度历史" | 查看最近的执行记录 |

### 交互示例

```
用户："添加一个周末专用的互动任务"
系统：
  "好的，我来帮你创建一个周末专用任务。请确认以下配置：

   任务名称：周末轻量互动
   执行时间：每周六日 10:30
   账号：不期而遇
   模式：发现页浏览
   时长：20 分钟
   
   是否确认创建？"
```

---

## 五、OpenClaw Cron 集成

### 5.1 注册定时任务

```python
def register_cron_tasks(schedule_config):
    """将配置中的定时任务注册到 OpenClaw 调度系统"""
    for plan in schedule_config.plans:
        if plan.enabled:
            cron_create(
                name=f"xhs-nurture-{plan.id}",
                schedule=plan.cron,
                command=f"run_skill xhs-nurture --plan={plan.id}",
                timezone=schedule_config.timezone,
            )

def unregister_cron_task(plan_id):
    """取消注册某个定时任务"""
    cron_delete(name=f"xhs-nurture-{plan_id}")
```

### 5.2 任务状态同步

```python
def sync_schedule_status():
    """同步调度状态（配置文件 ↔ OpenClaw cron）"""
    config = load_schedule_config()
    active_crons = cron_list(prefix="xhs-nurture-")
    
    # 检查配置中启用但未注册的任务
    for plan in config.plans:
        cron_name = f"xhs-nurture-{plan.id}"
        if plan.enabled and cron_name not in active_crons:
            register_cron_tasks([plan])
        elif not plan.enabled and cron_name in active_crons:
            unregister_cron_task(plan.id)
    
    # 检查已注册但配置中不存在的任务
    config_names = {f"xhs-nurture-{p.id}" for p in config.plans}
    for cron_name in active_crons:
        if cron_name not in config_names:
            cron_delete(name=cron_name)
```

---

## 六、故障恢复

### 6.1 错过的任务处理

```python
def handle_missed_task(plan, missed_time):
    """处理因故错过的定时任务"""
    elapsed_minutes = (now() - missed_time).total_seconds() / 60
    
    # 如果错过不超过 30 分钟，可以补执行
    if elapsed_minutes <= 30:
        # 检查是否仍在活跃时段
        if is_within_active_hours(now()):
            return "execute_now"
    
    # 超过 30 分钟，记录为跳过
    log_skip(plan, f"missed by {int(elapsed_minutes)} minutes")
    return "skip"
```

### 6.2 连续失败处理

```python
def check_consecutive_failures(plan_id, max_failures=3):
    """检查连续失败次数"""
    history = load_schedule_history(plan_id, days=3)
    recent = sorted(history, key=lambda x: x["trigger_time"], reverse=True)
    
    consecutive_fails = 0
    for entry in recent:
        if entry["status"] != "completed_normally":
            consecutive_fails += 1
        else:
            break
    
    if consecutive_fails >= max_failures:
        # 自动暂停该任务
        disable_plan(plan_id)
        notify_user(
            f"定时任务 [{plan_id}] 已连续失败 {consecutive_fails} 次，已自动暂停。\n"
            f"最近失败原因：{recent[0].get('errors', '未知')}\n"
            f"请排查问题后手动恢复。"
        )
        return True
    
    return False
```

---

## 七、状态报告

```python
def format_schedule_status():
    """格式化调度状态报告"""
    config = load_schedule_config()
    
    report = "📅 定时调度状态\n"
    report += "=" * 40 + "\n\n"
    
    for plan in config.plans:
        status_icon = "✅" if plan.enabled else "⏸️"
        next_run = calculate_next_run(plan.cron)
        last_result = get_last_result(plan.id)
        
        report += f"{status_icon} {plan.name}\n"
        report += f"   Cron: {plan.cron}\n"
        report += f"   账号: {plan.account} | 模式: {plan.mode}\n"
        report += f"   下次执行: {next_run}\n"
        if last_result:
            report += f"   上次结果: {last_result.status} ({last_result.time})\n"
        report += "\n"
    
    return report
```
