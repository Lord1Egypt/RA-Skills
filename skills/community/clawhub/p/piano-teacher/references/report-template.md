# HTML 报告模板

用于生成钢琴教学相关的交互式 HTML 报告。

## 使用说明
在 SKILL.md 中，当需要生成完整教学报告时（如同时包含多个模块的内容），使用此模板生成 HTML。

## 模板变量
- `{{TITLE}}` — 报告标题
- `{{STUDENT_LEVEL}}` — 学生级别
- `{{REPORT_DATE}}` — 生成日期
- `{{MODULES}}` — 各模块内容卡片（HTML片段）
- `{{NAV_ITEMS}}` — 目录导航项

## 基础框架

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{TITLE}}</title>
    <style>
        :root {
            --bg: #faf8f5;
            --card-bg: #ffffff;
            --text: #2c2416;
            --text-secondary: #6b5e4a;
            --gold: #c9a84c;
            --gold-light: #f5e6c8;
            --black: #1a1a1a;
            --white: #ffffff;
            --accent: #8b7355;
            --border: #e0d5c1;
            --shadow: 0 2px 12px rgba(0,0,0,0.06);
            --radius: 12px;
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.7;
        }
        
        /* 头部 */
        .header {
            background: linear-gradient(135deg, var(--black) 0%, #2c2416 100%);
            color: var(--white);
            padding: 48px 24px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .header::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: repeating-linear-gradient(
                90deg,
                transparent,
                transparent 40px,
                rgba(201,168,76,0.05) 40px,
                rgba(201,168,76,0.05) 42px
            );
        }
        
        .header h1 {
            font-size: 2em;
            font-weight: 700;
            position: relative;
            letter-spacing: 2px;
        }
        
        .header .subtitle {
            color: var(--gold);
            margin-top: 8px;
            font-size: 0.95em;
            position: relative;
        }
        
        .student-badge {
            display: inline-block;
            background: var(--gold);
            color: var(--black);
            padding: 4px 16px;
            border-radius: 20px;
            font-size: 0.85em;
            margin-top: 12px;
            font-weight: 600;
            position: relative;
        }
        
        /* 钢琴键盘装饰 */
        .keys-decor {
            display: flex;
            justify-content: center;
            margin: 12px 0 0;
            opacity: 0.3;
            position: relative;
        }
        
        .keys-decor .white-key {
            width: 28px;
            height: 40px;
            background: white;
            border: 1px solid #ccc;
            border-radius: 0 0 3px 3px;
        }
        
        .keys-decor .black-key {
            width: 18px;
            height: 24px;
            background: #333;
            border-radius: 0 0 2px 2px;
            margin: 0 -9px;
            z-index: 1;
        }
        
        /* 导航 */
        .nav {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            padding: 20px 24px;
            justify-content: center;
            background: var(--card-bg);
            border-bottom: 1px solid var(--border);
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        .nav a {
            text-decoration: none;
            color: var(--text-secondary);
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 0.9em;
            transition: all 0.2s;
            border: 1px solid transparent;
        }
        
        .nav a:hover {
            background: var(--gold-light);
            color: var(--accent);
            border-color: var(--gold);
        }
        
        /* 主内容 */
        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 32px 24px;
        }
        
        /* 卡片 */
        .card {
            background: var(--card-bg);
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            margin-bottom: 24px;
            overflow: hidden;
            border: 1px solid var(--border);
        }
        
        .card-header {
            padding: 20px 24px;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .card-header .icon {
            font-size: 1.4em;
        }
        
        .card-header h2 {
            font-size: 1.2em;
            font-weight: 700;
            color: var(--black);
        }
        
        .card-body {
            padding: 24px;
        }
        
        .card-body h3 {
            font-size: 1.05em;
            color: var(--accent);
            margin: 20px 0 10px;
            padding-bottom: 6px;
            border-bottom: 2px solid var(--gold-light);
        }
        
        .card-body h3:first-child {
            margin-top: 0;
        }
        
        .card-body p {
            margin-bottom: 12px;
            color: var(--text);
        }
        
        /* 表格样式 */
        .card-body table {
            width: 100%;
            border-collapse: collapse;
            margin: 16px 0;
            font-size: 0.92em;
        }
        
        .card-body th {
            background: var(--black);
            color: var(--white);
            padding: 10px 14px;
            text-align: left;
            font-weight: 600;
        }
        
        .card-body td {
            padding: 10px 14px;
            border-bottom: 1px solid var(--border);
        }
        
        .card-body tr:nth-child(even) td {
            background: #faf8f3;
        }
        
        /* 难点高亮 */
        .difficulty-highlight {
            background: #fff8e7;
            border-left: 4px solid var(--gold);
            padding: 16px 20px;
            border-radius: 0 8px 8px 0;
            margin: 16px 0;
        }
        
        .difficulty-highlight .label {
            font-weight: 700;
            color: var(--gold);
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        /* 练习步骤 */
        .practice-steps {
            list-style: none;
            counter-reset: step;
        }
        
        .practice-steps li {
            counter-increment: step;
            padding: 10px 0 10px 40px;
            position: relative;
            border-bottom: 1px dashed var(--border);
        }
        
        .practice-steps li::before {
            content: counter(step);
            position: absolute;
            left: 0;
            top: 8px;
            width: 26px;
            height: 26px;
            background: var(--gold);
            color: var(--white);
            border-radius: 50%;
            font-size: 0.8em;
            font-weight: 700;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        /* 计划表 */
        .schedule-table td:first-child {
            font-weight: 700;
            white-space: nowrap;
            color: var(--accent);
        }
        
        /* 提示框 */
        .tip-box {
            background: #f0f7f0;
            border-left: 4px solid #4a9;
            padding: 14px 18px;
            border-radius: 0 8px 8px 0;
            margin: 16px 0;
            font-size: 0.93em;
        }
        
        .warn-box {
            background: #fff5f0;
            border-left: 4px solid #e88;
            padding: 14px 18px;
            border-radius: 0 8px 8px 0;
            margin: 16px 0;
            font-size: 0.93em;
        }
        
        /* 评分/进度条 */
        .skill-bar {
            display: flex;
            align-items: center;
            margin: 8px 0;
            gap: 10px;
        }
        
        .skill-bar .label {
            width: 90px;
            font-size: 0.9em;
            color: var(--text-secondary);
        }
        
        .skill-bar .bar {
            flex: 1;
            height: 8px;
            background: #eee;
            border-radius: 4px;
            overflow: hidden;
        }
        
        .skill-bar .fill {
            height: 100%;
            background: var(--gold);
            border-radius: 4px;
            transition: width 0.6s ease;
        }
        
        .skill-bar .score {
            width: 36px;
            text-align: right;
            font-weight: 700;
            font-size: 0.9em;
            color: var(--accent);
        }
        
        /* 页脚 */
        .footer {
            text-align: center;
            padding: 32px 24px;
            color: var(--text-secondary);
            font-size: 0.85em;
        }
        
        .footer .keys-decor {
            margin-bottom: 12px;
        }
        
        /* 响应式 */
        @media (max-width: 600px) {
            .header h1 { font-size: 1.5em; }
            .container { padding: 16px; }
            .card-body { padding: 16px; }
            .card-body table { font-size: 0.8em; }
            .card-body th, .card-body td { padding: 8px 10px; }
        }
        
        /* 打印优化 */
        @media print {
            .nav { display: none; }
            .header { padding: 24px; }
            .card { break-inside: avoid; box-shadow: none; }
        }
    </style>
</head>
<body>
    <!-- 头部 -->
    <header class="header">
        <h1>{{TITLE}}</h1>
        <p class="subtitle">AI 钢琴老师 教学报告</p>
        <span class="student-badge">{{STUDENT_LEVEL}}</span>
        <div class="keys-decor">
            <span class="white-key"></span><span class="black-key"></span>
            <span class="white-key"></span><span class="black-key"></span>
            <span class="white-key"></span>
            <span class="white-key"></span><span class="black-key"></span>
            <span class="white-key"></span><span class="black-key"></span>
            <span class="white-key"></span><span class="black-key"></span>
            <span class="white-key"></span>
        </div>
    </header>
    
    <!-- 导航 -->
    <nav class="nav">
        {{NAV_ITEMS}}
    </nav>
    
    <!-- 内容 -->
    <div class="container">
        {{MODULES}}
    </div>
    
    <!-- 页脚 -->
    <footer class="footer">
        <div class="keys-decor">
            <span class="white-key"></span><span class="black-key"></span>
            <span class="white-key"></span>
        </div>
        <p>AI 钢琴老师 · 生成于 {{REPORT_DATE}}</p>
        <p style="font-size:0.8em;margin-top:4px;">本报告由 AI 生成，仅供参考，建议配合专业教师指导使用</p>
    </footer>
</body>
</html>
```

## 模块卡片模板

### 乐理教学卡片
```html
<section class="card" id="theory">
    <div class="card-header">
        <span class="icon">🎼</span>
        <h2>乐理知识</h2>
    </div>
    <div class="card-body">
        <!-- 各知识点按教学格式输出 -->
    </div>
</section>
```

### 曲目分析卡片
```html
<section class="card" id="repertoire">
    <div class="card-header">
        <span class="icon">🎹</span>
        <h2>曲目分析：{曲目名}</h2>
    </div>
    <div class="card-body">
        <!-- 按曲目分析格式输出 -->
    </div>
</section>
```

### 练习计划卡片
```html
<section class="card" id="plan">
    <div class="card-header">
        <span class="icon">📋</span>
        <h2>练习计划</h2>
    </div>
    <div class="card-body">
        <table class="schedule-table">
            <!-- 计划表格 -->
        </table>
    </div>
</section>
```

### 技巧指导卡片
```html
<section class="card" id="technique">
    <div class="card-header">
        <span class="icon">✋</span>
        <h2>技巧指导</h2>
    </div>
    <div class="card-body">
        <!-- 技巧分析内容 -->
    </div>
</section>
```

### 能力评估卡片
```html
<section class="card" id="assessment">
    <div class="card-header">
        <span class="icon">📊</span>
        <h2>能力评估</h2>
    </div>
    <div class="card-body">
        <div class="skill-bar">
            <span class="label">技术水平</span>
            <div class="bar"><div class="fill" style="width:80%"></div></div>
            <span class="score">8/10</span>
        </div>
        <!-- ...更多能力条... -->
    </div>
</section>
```

## 使用规则
1. 生成 HTML 时，先用实际内容替换所有 `{{VARIABLE}}` 占位符
2. 模块卡片根据用户需要选择性生成，不要全部生成
3. 导航项 `{{NAV_ITEMS}}` 应与实际生成的模块保持一致
4. 文件名：`piano-report-{日期}.html`，保存到当前工作目录
