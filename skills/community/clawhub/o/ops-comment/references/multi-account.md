# 多账号切换逻辑

## 一、账号管理架构

```
config/profiles/
├── default.yaml        # 主账号（首次设置时创建）
├── account-2.yaml      # 第二账号
└── account-3.yaml      # 第三账号

data/nurture-log/
├── default/            # 主账号日志（独立目录）
│   └── 2026-05-16.jsonl
├── account-2/
│   └── 2026-05-16.jsonl
└── account-3/
    └── 2026-05-16.jsonl
```

---

## 二、Profile 配置格式

```yaml
# config/profiles/default.yaml
profile:
  id: "default"
  name: "不期而遇"
  category: "期货/财经"
  stage: "growth"           # nurturing | growth | mature
  
  # 账号识别标志（用于确认当前登录的是这个账号）
  identity:
    nickname: "不期而遇"
    # 备用识别方式
    profile_url_fragment: "user/xxxxx"
  
  # 账号专属策略（覆盖全局 nurture-config.yaml）
  strategy_override:
    daily_limits:
      likes: 100
      collects: 25
      follows: 20
      comments: 12
    
    # 专属关键词
    targets:
      keywords: ["期货入门", "交易心得", "投资理财"]
      competitor_accounts: ["@竞品A", "@竞品B"]
  
  # 专属过滤器覆盖
  filter_override:
    note:
      keywords_include: ["期货", "交易", "原油", "黄金"]
  
  # 专属评论风格
  comment_style: "professional"
```

---

## 三、账号切换流程

### 3.1 切换触发

```python
def switch_account(target_profile_id):
    """切换到目标账号"""
    # 1. 加载目标 Profile
    target = load_profile(target_profile_id)
    if not target:
        notify_user(f"未找到账号配置: {target_profile_id}")
        return False
    
    # 2. 检查当前登录账号
    current = detect_current_account()
    
    # 3. 如果已经是目标账号，直接返回
    if current == target.identity.nickname:
        return True
    
    # 4. 执行切换
    success = perform_switch(target)
    
    # 5. 验证切换结果
    if success:
        new_current = detect_current_account()
        if new_current == target.identity.nickname:
            notify_user(f"已切换到账号: {target.name}")
            return True
    
    # 6. 切换失败
    notify_user(f"账号切换失败，请手动切换到 {target.name} 后告知我继续。")
    return False
```

### 3.2 检测当前账号

```python
def detect_current_account():
    """检测当前登录的是哪个账号"""
    # 方式1：从页面右上角头像区域获取昵称
    navigate("https://www.xiaohongshu.com")
    wait(2)
    
    # 尝试读取用户昵称
    nickname_element = find("当前用户昵称") or find("我的头像")
    if nickname_element:
        # 点击头像可能展开菜单显示昵称
        page_info = read_page(filter="all", depth=5)
        # 从页面结构中提取当前用户名
        nickname = extract_nickname_from_page(page_info)
        return nickname
    
    # 方式2：访问个人主页
    navigate("https://www.xiaohongshu.com/user/profile")
    wait(2)
    nickname = find_text("用户昵称")
    return nickname
```

### 3.3 执行切换操作

```python
def perform_switch(target_profile):
    """执行账号切换操作"""
    # 小红书 Web 端的账号切换方式：
    # 通常需要退出当前账号 → 登录目标账号
    # 或者如果平台支持多账号切换功能
    
    # 方式1：通过设置页切换（如果平台支持）
    navigate("https://www.xiaohongshu.com")
    wait(2)
    
    # 点击头像/设置入口
    avatar = find("我的头像") or find("个人中心")
    if avatar:
        click_element_humanlike(avatar)
        wait(random_uniform(1, 2))
    
    # 查找切换账号入口
    switch_btn = find("切换账号") or find("账号切换")
    if switch_btn:
        click_element_humanlike(switch_btn)
        wait(random_uniform(1, 3))
        
        # 在账号列表中找到目标账号
        target_item = find(target_profile.identity.nickname)
        if target_item:
            click_element_humanlike(target_item)
            wait(random_uniform(2, 4))
            return True
    
    # 方式2：如果没有切换入口，通知用户手动操作
    return False
```

---

## 四、多账号互动去重

### 4.1 跨账号去重

```python
class CrossAccountDedup:
    """确保多个账号不会互动同一个目标"""
    
    def __init__(self, profiles):
        self.profiles = profiles
        self.shared_history = self._load_all_histories()
    
    def _load_all_histories(self):
        """加载所有账号的互动历史"""
        all_notes = set()
        all_users = set()
        
        for profile_id in self.profiles:
            log_dir = f"data/nurture-log/{profile_id}/"
            for log_file in list_files(log_dir, pattern="*.jsonl", days=3):
                for entry in read_jsonl(log_file):
                    if entry.get("success"):
                        if entry.get("target_note_id"):
                            all_notes.add(entry["target_note_id"])
                        if entry.get("target_user"):
                            all_users.add(entry["target_user"])
        
        return {"notes": all_notes, "users": all_users}
    
    def is_safe_to_interact(self, target_id, target_type="note"):
        """检查是否可以互动（未被其他账号互动过）"""
        if target_type == "note":
            return target_id not in self.shared_history["notes"]
        elif target_type == "user":
            return target_id not in self.shared_history["users"]
        return True
```

### 4.2 账号间冷却

```python
# 同一设备上切换账号后的冷却规则
SWITCH_COOLDOWN = {
    "min_minutes_between_switches": 30,  # 切换间隔至少 30 分钟
    "max_switches_per_day": 4,            # 每天最多切换 4 次
    "browse_after_switch_minutes": 3,     # 切换后先浏览 3 分钟再互动
}

def can_switch_now(switch_history):
    """检查当前是否可以切换账号"""
    if not switch_history:
        return True
    
    last_switch = switch_history[-1]
    elapsed = (now() - last_switch["time"]).total_seconds() / 60
    
    if elapsed < SWITCH_COOLDOWN["min_minutes_between_switches"]:
        remaining = SWITCH_COOLDOWN["min_minutes_between_switches"] - elapsed
        return False, f"距上次切换不足30分钟，请等待 {int(remaining)} 分钟"
    
    today_switches = sum(1 for s in switch_history if s["date"] == today_str())
    if today_switches >= SWITCH_COOLDOWN["max_switches_per_day"]:
        return False, "今日切换次数已达上限"
    
    return True, "ok"
```

---

## 五、多账号调度策略

### 5.1 轮转调度

```python
def schedule_multi_account(profiles, schedule_config):
    """多账号轮转调度计划"""
    plans = []
    
    # 将每天的活跃时段分配给不同账号
    active_slots = schedule_config.active_hours
    
    # 简单轮转：每个时段一个账号
    for i, slot in enumerate(active_slots):
        profile_idx = i % len(profiles)
        plans.append({
            "profile": profiles[profile_idx].id,
            "time_slot": slot,
            "mode": profiles[profile_idx].preferred_mode,
        })
    
    return plans
```

### 5.2 独立计数器

```python
class MultiAccountCounters:
    """每个账号独立的计数器管理"""
    
    def __init__(self, profiles):
        self.counters = {}
        for profile in profiles:
            self.counters[profile.id] = load_today_counters(
                today_str(), 
                profile.id
            )
    
    def get(self, profile_id):
        return self.counters.get(profile_id, default_counters())
    
    def increment(self, profile_id, action_type):
        self.counters[profile_id][action_type] += 1
        self.counters[profile_id]["total"] += 1
    
    def get_remaining(self, profile_id, limits):
        counters = self.get(profile_id)
        return {
            k: max(0, limits[k] - counters[k])
            for k in ["likes", "collects", "follows", "comments"]
        }
```

---

## 六、账号健康度独立监控

```python
class AccountHealthMonitor:
    """每个账号独立的健康度监控"""
    
    def __init__(self, profile_id):
        self.profile_id = profile_id
        self.risk_events = load_risk_history(profile_id)
    
    def record_risk_event(self, event_type, severity):
        self.risk_events.append({
            "time": now().isoformat(),
            "type": event_type,
            "severity": severity,
        })
        save_risk_history(self.profile_id, self.risk_events)
    
    def get_health_score(self):
        """计算账号健康分（0-100）"""
        score = 100
        recent = [e for e in self.risk_events if is_within_days(e["time"], 7)]
        
        for event in recent:
            match event["severity"]:
                case "low":
                    score -= 5
                case "medium":
                    score -= 15
                case "high":
                    score -= 30
                case "critical":
                    score -= 50
        
        return max(0, score)
    
    def should_pause(self):
        """健康分过低时建议暂停"""
        score = self.get_health_score()
        if score < 30:
            return True, f"账号 {self.profile_id} 健康分过低({score})，建议暂停 24-48 小时"
        return False, None
```

---

## 七、用户交互

### 切换账号指令

```
用户："切换到账号2"
系统：
1. 检查切换冷却时间
2. 保存当前账号状态
3. 执行切换
4. 验证切换成功
5. 加载新账号配置
6. 报告：
   "已切换到 [账号名]
    今日剩余配额：点赞 X / 收藏 X / 关注 X / 评论 X
    账号健康度：XX/100"
```

### 查看所有账号状态

```
用户："查看所有账号状态"
系统输出：
┌──────────┬────────┬──────────┬──────────┬──────┐
│ 账号     │ 阶段   │ 今日互动  │ 健康度   │ 状态 │
├──────────┼────────┼──────────┼──────────┼──────┤
│ 不期而遇 │ growth │ 65/150   │ 95/100   │ 正常 │
│ 账号2    │ nurture│ 30/70    │ 100/100  │ 正常 │
│ 账号3    │ growth │ 0/150    │ 45/100   │ 暂停 │
└──────────┴────────┴──────────┴──────────┴──────┘
```
