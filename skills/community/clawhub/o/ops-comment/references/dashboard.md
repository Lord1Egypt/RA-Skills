# 数据看板规范

## 一、报告体系

```
data/reports/
├── daily-{date}.html         # 每日报告
├── weekly-{year}-W{week}.html # 周报
└── dashboard.html             # 总览面板（每次更新覆盖）
```

---

## 二、数据源

### 2.1 日志格式 (`data/nurture-log/{account}/{date}.jsonl`)

每条记录：
```json
{
  "ts": "2026-05-16T14:32:15.123Z",
  "session_id": "sess_20260516_abc123",
  "action": "like",
  "target_note_id": "note_xxx",
  "target_user": "user_yyy",
  "success": true,
  "duration_ms": 1200,
  "context": "discover_feed",
  "note_title": "期货入门指南",
  "note_likes": 2300
}
```

### 2.2 数据聚合

```python
def aggregate_daily(date, account):
    """聚合每日数据"""
    log_file = f"data/nurture-log/{account}/{date}.jsonl"
    entries = read_jsonl(log_file)
    
    stats = {
        "date": date,
        "account": account,
        "total_actions": len([e for e in entries if e["success"]]),
        "actions": {
            "likes": count(entries, action="like", success=True),
            "collects": count(entries, action="collect", success=True),
            "follows": count(entries, action="follow", success=True),
            "comments": count(entries, action="comment", success=True),
        },
        "sessions": count_unique(entries, "session_id"),
        "total_duration_minutes": sum_duration(entries) / 60,
        "success_rate": success_count / total_count,
        "errors": count(entries, success=False),
        "contexts": {
            "discover_feed": count(entries, context="discover_feed"),
            "search": count(entries, context="search"),
            "user_profile": count(entries, context="user_profile"),
            "comment_section": count(entries, context="comment_section"),
        },
        "hourly_distribution": group_by_hour(entries),
        "risk_events": count_risk_events(entries),
    }
    return stats
```

---

## 三、HTML 报告模板

### 3.1 技术栈

- 纯静态 HTML（单文件，无外部依赖 CDN）
- 内嵌 Chart.js (min) 用于图表
- 内嵌 CSS（无框架）
- 数据直接嵌入 `<script>` 标签中的 JSON

### 3.2 模板结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>小红书养号数据看板 - {date}</title>
    <style>
        /* 内嵌样式 */
        :root {
            --primary: #ff2442;      /* 小红书红 */
            --bg: #fafafa;
            --card-bg: #ffffff;
            --text: #333333;
            --text-secondary: #666666;
            --border: #eeeeee;
            --success: #52c41a;
            --warning: #faad14;
            --danger: #ff4d4f;
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--bg); 
            color: var(--text);
            padding: 24px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 32px;
        }
        .header h1 { font-size: 24px; color: var(--primary); }
        .header .subtitle { color: var(--text-secondary); margin-top: 8px; }
        
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }
        
        .card {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        }
        .card h3 { 
            font-size: 14px; 
            color: var(--text-secondary); 
            margin-bottom: 8px; 
        }
        .card .value { 
            font-size: 32px; 
            font-weight: 700; 
            color: var(--text); 
        }
        .card .sub { 
            font-size: 12px; 
            color: var(--text-secondary); 
            margin-top: 4px; 
        }
        
        .chart-container {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 24px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        }
        .chart-container h3 {
            font-size: 16px;
            margin-bottom: 16px;
        }
        
        .status-badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 12px;
        }
        .status-good { background: #f6ffed; color: var(--success); }
        .status-warn { background: #fffbe6; color: var(--warning); }
        .status-bad { background: #fff2f0; color: var(--danger); }
    </style>
</head>
<body>
    <div class="header">
        <h1>小红书养号数据看板</h1>
        <div class="subtitle">{account_name} · {date_range}</div>
    </div>
    
    <!-- 今日概览 -->
    <div class="grid" id="overview-cards"></div>
    
    <!-- 趋势图 -->
    <div class="chart-container">
        <h3>近7天互动趋势</h3>
        <canvas id="trendChart" height="200"></canvas>
    </div>
    
    <!-- 时段分布 -->
    <div class="chart-container">
        <h3>互动时段分布</h3>
        <canvas id="hourlyChart" height="150"></canvas>
    </div>
    
    <!-- 动作类型占比 -->
    <div class="chart-container">
        <h3>动作类型分布</h3>
        <canvas id="actionPieChart" height="200"></canvas>
    </div>
    
    <!-- 账号健康度 -->
    <div class="chart-container">
        <h3>账号健康度</h3>
        <div id="health-gauge"></div>
    </div>
    
    <!-- Chart.js (内嵌压缩版) -->
    <script>
        // Chart.js CDN fallback - 实际部署时内嵌 min.js
        // 这里用 CDN 仅作为示例
    </script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>
    
    <!-- 数据 -->
    <script>
        const DATA = {json_data_placeholder};
    </script>
    
    <!-- 渲染逻辑 -->
    <script>
        // === 概览卡片 ===
        function renderOverview() {
            const cards = [
                { title: '今日点赞', value: DATA.today.likes, limit: DATA.limits.likes },
                { title: '今日收藏', value: DATA.today.collects, limit: DATA.limits.collects },
                { title: '今日关注', value: DATA.today.follows, limit: DATA.limits.follows },
                { title: '今日评论', value: DATA.today.comments, limit: DATA.limits.comments },
                { title: '总动作数', value: DATA.today.total, limit: DATA.limits.total },
                { title: '成功率', value: (DATA.today.success_rate * 100).toFixed(1) + '%', sub: '' },
                { title: '运行时长', value: DATA.today.duration_minutes + ' 分钟', sub: '' },
                { title: '健康度', value: DATA.health_score + '/100', sub: DATA.health_status },
            ];
            
            const container = document.getElementById('overview-cards');
            cards.forEach(card => {
                const el = document.createElement('div');
                el.className = 'card';
                const pct = card.limit ? ` / ${card.limit}` : '';
                el.innerHTML = `
                    <h3>${card.title}</h3>
                    <div class="value">${card.value}${pct}</div>
                    ${card.sub ? `<div class="sub">${card.sub}</div>` : ''}
                `;
                container.appendChild(el);
            });
        }
        
        // === 趋势图 ===
        function renderTrend() {
            const ctx = document.getElementById('trendChart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: DATA.trend.dates,
                    datasets: [
                        { label: '点赞', data: DATA.trend.likes, borderColor: '#ff2442', tension: 0.3 },
                        { label: '收藏', data: DATA.trend.collects, borderColor: '#faad14', tension: 0.3 },
                        { label: '关注', data: DATA.trend.follows, borderColor: '#52c41a', tension: 0.3 },
                        { label: '评论', data: DATA.trend.comments, borderColor: '#1890ff', tension: 0.3 },
                    ]
                },
                options: {
                    responsive: true,
                    plugins: { legend: { position: 'bottom' } },
                    scales: { y: { beginAtZero: true } }
                }
            });
        }
        
        // === 时段分布 ===
        function renderHourly() {
            const ctx = document.getElementById('hourlyChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: Array.from({length: 24}, (_, i) => `${i}:00`),
                    datasets: [{
                        label: '互动次数',
                        data: DATA.hourly_distribution,
                        backgroundColor: '#ff244233',
                        borderColor: '#ff2442',
                        borderWidth: 1,
                    }]
                },
                options: {
                    responsive: true,
                    plugins: { legend: { display: false } },
                    scales: { y: { beginAtZero: true } }
                }
            });
        }
        
        // === 动作占比 ===
        function renderPie() {
            const ctx = document.getElementById('actionPieChart').getContext('2d');
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['点赞', '收藏', '关注', '评论'],
                    datasets: [{
                        data: [
                            DATA.today.likes,
                            DATA.today.collects,
                            DATA.today.follows,
                            DATA.today.comments
                        ],
                        backgroundColor: ['#ff2442', '#faad14', '#52c41a', '#1890ff'],
                    }]
                },
                options: {
                    responsive: true,
                    plugins: { legend: { position: 'bottom' } }
                }
            });
        }
        
        // 初始化
        renderOverview();
        renderTrend();
        renderHourly();
        renderPie();
    </script>
</body>
</html>
```

---

## 四、报告生成逻辑

### 4.1 每日报告

```python
def generate_daily_report(date, account):
    """生成每日报告"""
    # 聚合今日数据
    today_stats = aggregate_daily(date, account)
    
    # 聚合近7天趋势数据
    trend = []
    for i in range(7):
        d = (parse_date(date) - timedelta(days=i)).strftime("%Y-%m-%d")
        day_stats = aggregate_daily(d, account)
        trend.insert(0, day_stats)
    
    # 获取配额配置
    limits = get_limits_for_account(account)
    
    # 计算健康度
    health = AccountHealthMonitor(account)
    health_score = health.get_health_score()
    
    # 构造报告数据
    report_data = {
        "today": today_stats["actions"] | {
            "total": today_stats["total_actions"],
            "success_rate": today_stats["success_rate"],
            "duration_minutes": int(today_stats["total_duration_minutes"]),
        },
        "limits": limits,
        "trend": {
            "dates": [t["date"] for t in trend],
            "likes": [t["actions"]["likes"] for t in trend],
            "collects": [t["actions"]["collects"] for t in trend],
            "follows": [t["actions"]["follows"] for t in trend],
            "comments": [t["actions"]["comments"] for t in trend],
        },
        "hourly_distribution": today_stats["hourly_distribution"],
        "health_score": health_score,
        "health_status": "正常" if health_score > 70 else ("注意" if health_score > 30 else "危险"),
    }
    
    # 渲染 HTML
    html = render_template("templates/dashboard/base.html", {
        "json_data_placeholder": json.dumps(report_data, ensure_ascii=False),
        "account_name": account,
        "date_range": date,
    })
    
    # 写入文件
    output_path = f"data/reports/daily-{date}.html"
    write_file(output_path, html)
    
    # 更新总览面板
    write_file("data/reports/dashboard.html", html)
    
    return output_path
```

### 4.2 周报

```python
def generate_weekly_report(year, week, account):
    """生成周报"""
    # 获取本周每天的数据
    week_start = get_week_start(year, week)
    daily_stats = []
    for i in range(7):
        d = (week_start + timedelta(days=i)).strftime("%Y-%m-%d")
        stats = aggregate_daily(d, account)
        daily_stats.append(stats)
    
    # 计算周汇总
    weekly_summary = {
        "total_actions": sum(d["total_actions"] for d in daily_stats),
        "total_likes": sum(d["actions"]["likes"] for d in daily_stats),
        "total_collects": sum(d["actions"]["collects"] for d in daily_stats),
        "total_follows": sum(d["actions"]["follows"] for d in daily_stats),
        "total_comments": sum(d["actions"]["comments"] for d in daily_stats),
        "total_sessions": sum(d["sessions"] for d in daily_stats),
        "total_duration_hours": sum(d["total_duration_minutes"] for d in daily_stats) / 60,
        "avg_success_rate": mean([d["success_rate"] for d in daily_stats]),
        "active_days": sum(1 for d in daily_stats if d["total_actions"] > 0),
        "risk_events": sum(d["risk_events"] for d in daily_stats),
    }
    
    # 与上周对比
    last_week_stats = get_last_week_stats(year, week - 1, account)
    comparison = calculate_week_comparison(weekly_summary, last_week_stats)
    
    # 渲染并保存
    output_path = f"data/reports/weekly-{year}-W{week:02d}.html"
    # ... 渲染逻辑类似日报
    return output_path
```

---

## 五、效果追踪指标

### 5.1 直接指标（可从日志计算）

| 指标 | 计算方式 | 意义 |
|------|---------|------|
| 日互动量 | 当日成功动作总数 | 活跃度基线 |
| 动作成功率 | 成功数 / 总尝试数 | 运行稳定性 |
| 会话持续时长 | 会话结束时间 - 开始时间 | 运行效率 |
| 动作均匀度 | 各时段动作数的标准差 | 自然度指标 |
| 错误率 | 失败次数 / 总次数 | 风控指标 |

### 5.2 效果指标（需用户补充数据）

| 指标 | 获取方式 | 意义 |
|------|---------|------|
| 互动回访率 | 手动记录 / 通知检查 | 引流效果 |
| 新增粉丝/日 | 对比昨日粉丝数 | 增长效果 |
| 笔记曝光变化 | 对比互动前后数据 | 权重变化 |

### 5.3 用户可手动补充数据

```
用户："今天粉丝增了 15 个"
系统：记录到效果追踪中

用户："更新一下今天的数据"
系统：
  "请提供以下数据（可选，有多少填多少）：
   - 今日新增粉丝：___
   - 收到的互动通知数：___
   - 笔记曝光量变化：___"
```

---

## 六、告警机制

```python
ALERT_RULES = [
    {
        "name": "成功率过低",
        "condition": lambda stats: stats["success_rate"] < 0.8,
        "level": "warning",
        "message": "今日操作成功率 {rate}%，低于 80% 阈值",
    },
    {
        "name": "风控事件",
        "condition": lambda stats: stats["risk_events"] > 0,
        "level": "danger",
        "message": "今日出现 {count} 次风控事件",
    },
    {
        "name": "配额未完成",
        "condition": lambda stats: stats["total_actions"] < stats["planned"] * 0.5,
        "level": "info",
        "message": "今日仅完成计划的 {pct}%",
    },
    {
        "name": "连续多天无操作",
        "condition": lambda stats: stats["inactive_days"] >= 2,
        "level": "warning",
        "message": "已连续 {days} 天无互动操作",
    },
]
```
