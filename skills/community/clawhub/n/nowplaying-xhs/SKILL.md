---
name: nowplaying
description: 当前院线推荐 - 实时检索公映影片 + 多维度评分 + 附近影院排片
version: "1.1.0"
author: seeu1688
license: MIT
---
  当前院线推荐 Skill。当用户问"现在有什么好看的电影"、"最近上映了什么"、"帮我选一部电影"、
  "今天想去看电影"、"附近影院有什么排片"等问题时，触发此 Skill。
  Skill 会实时检索当前公映影片、多维度评分与口碑、附近影院排片（猫眼/淘票票抓取，2 小时内场次），
  输出带综合推荐排名的完整报告，附评分柱状对比图 + Top 3 六维蛛网图。
---

# NowPlaying · 院线实时推荐系统

## 核心原则

- **时效优先**：所有数据必须通过实时工具获取，禁止使用训练数据中的历史票房/评分
- **地理感知**：优先利用用户位置缩小影院搜索范围；无法定位时降级为城市级别
- **来源透明**：每条评分/评论标注来源平台与证据级别
- **排名可解释**：综合得分公式明确，用户可理解排名依据
- **可操作输出**：最终提供"今晚就能去看"的具体场次信息

---

## 搜索工具优先级（关键配置）

### 按数据类型选择工具

| 数据类型 | 首选工具 | 备用工具 | 说明 |
|----------|----------|----------|------|
| **实时排片/场次** | `agent-browser`（直接访问猫眼/淘票票） | `博查 API` | 博查搜索国内院线数据更新快 |
| **今日票房** | `博查 API` | `tavily-search` | 博查实时性更好 |
| **豆瓣评分** | `tavily-search` | `博查 API` | Tavily 结果质量高 |
| **影评口碑** | `tavily-search` | `博查 API` | Tavily 适合长文本分析 |
| **海外评分** | `tavily-search` | — | IMDb/RT 等 |

### 搜索策略

```bash
# 1. 实时排片（优先使用博查 API）
curl -X POST "https://api.bocha.cn/v1/web-search" \
  -H "Authorization: Bearer $BOCHA_API_KEY" \
  -d '{"query":"猫眼电影 [城市] [片名] 今日排片 场次 [日期]"}'

# 2. 票房数据（博查 API）
curl -X POST "https://api.bocha.cn/v1/web-search" \
  -H "Authorization: Bearer $BOCHA_API_KEY" \
  -d '{"query":"猫眼专业版 实时票房 [日期]"}'

# 3. 豆瓣评分（Tavily）
node {baseDir}/../tavily-search/scripts/search.mjs "[片名] 豆瓣评分 影评" -n 5

# 4. 直接抓取（Agent Browser，最准确）
# 访问猫眼/淘票票网页获取实时场次
```

### 工具降级策略

```
博查 API 失败 → Tavily Search → 标注"数据可能非实时"
Agent Browser 失败 → 博查 API 搜索 → 提供猫眼/淘票票 App 直达链接
```

---

## Step 0 · 定位与偏好解析

### 0.1 地理定位（按优先级尝试）

1. **系统上下文定位**：检查是否有用户位置信息（城市/坐标）
2. **用户主动告知**：若用户在问题中提及城市/地区/影院名，直接使用
3. **降级策略**：若无任何位置信息，询问用户所在城市；若用户明确不提供，输出全国热映榜，影院排片模块留空并注明原因

### 0.2 偏好提取（可选）

若用户在提问中指定偏好（如"喜欢科幻"、"不要太血腥"、"带小孩去"、"情侣约会"），
在推荐排名中对匹配影片的**偏好匹配分**加权，并在影片卡中标注 ⭐ 符合您的偏好。

---

## Step 1 · 当前公映影片采集

### 1.1 主搜索（必须执行，并行查询）

**搜索工具选择：** 优先使用 `博查 API` 获取实时数据，`tavily-search` 补充口碑数据

```
【博查 API】查询 1：猫眼电影 正在热映 实时票房 [当前日期]
【博查 API】查询 2：淘票票 正在上映 电影 [当前月份年份]
【Tavily】查询 3：豆瓣 正在上映 电影 [当前月份年份]
【博查 API】查询 4（若用户有城市）：[城市] 电影院 正在上映 [当前月份年份]
```

目标：获取当前公映影片列表，覆盖票房/排片前 **10 部**。

### 1.1.1 实时性要求

| 数据类型 | 时效要求 | 来源 |
|----------|----------|------|
| 排片场次 | **2 小时内** | 猫眼/淘票票实时抓取 |
| 当日票房 | **当日** | 猫眼专业版 |
| 豆瓣评分 | **7 天内** | 豆瓣网页 |
| 影评口碑 | **30 天内** | 豆瓣/媒体 |

### 1.2 数据字段采集目标

对每部影片采集以下字段（缺失字段标注"数据不可用"，禁止伪造）：

| 字段 | 主要来源 | 重要性 |
|------|----------|--------|
| 片名（中英文） | 任意 | 必填 |
| 导演 / 主演 | 豆瓣 / IMDb | 必填 |
| 类型 / 片长 / 语言 | 豆瓣 / 猫眼 | 必填 |
| 上映日期 | 猫眼 / 灯塔 | 必填 |
| 豆瓣评分 + 评分人数 | 豆瓣 | 高 |
| IMDb 评分 | IMDb | 高 |
| 猫眼评分 + 想看人数 | 猫眼 | 高 |
| 淘票票评分 | 淘票票 | 中 |
| RT 新鲜度（专业/观众） | Rotten Tomatoes | 中 |
| 累计票房（内地） | 猫眼 / 灯塔专业版 | 高（用于热度分） |
| 日票房排名 | 猫眼实时 | 高（用于热度分） |
| 一句话核心看点 | 影评综合 | 高 |
| 代表性好评（1 条） | 豆瓣 / RT / 媒体 | 高 |
| 代表性差评（1 条） | 豆瓣 / RT / 媒体 | 中 |
| 独特卖点 / 差异化亮点 | 影评综合 | 高 |

### 1.3 搜索效率规则

- 票房前 5 部：分别独立搜索评分与影评
- 第 6–10 部：合并搜索（如"[片名] 豆瓣评分 口碑 [年份]"）
- 总搜索次数预算：**10–18 次**，根据影片数量动态调整
- 若某平台数据确实无法获取，标注"数据不可用"，不伪造

---

## Step 2 · 综合推荐评分计算

### 2.1 四维输入指标

| 指标 | 计算方式 | 权重 |
|------|----------|------|
| **口碑分** | 豆瓣×0.45 + IMDb×0.20 + 猫眼×0.20 + RT 新鲜度×0.15，归一化至 100 分 | **50%** |
| **热度分** | 以猫眼/灯塔当日票房排名换算：日榜第 1=100，第 2=90，第 3=82，第 4=75，第 5=68，第 6–10 线性插值至 30 | **20%** |
| **新鲜度分** | 上映天数：≤3 天=100，4–7 天=90，8–14 天=75，15–30 天=55，>30 天=35 | **15%** |
| **偏好匹配分** | 用户有偏好且完全匹配=100，部分匹配=60，不匹配=30；无偏好时所有影片均为 60 | **15%** |

### 2.2 综合推荐分公式

```
综合推荐分 = 口碑分×0.50 + 热度分×0.20 + 新鲜度分×0.15 + 偏好匹配分×0.15
```

> 综合推荐分 ≠ "最好看"，而是"当前最值得现在进影院看"的综合判断。
> 口碑极高但已上映 1 个月的影片，综合分会因新鲜度衰减略低于同等口碑的新片。

### 2.3 评级标签与可视化配色

| 分数段 | 标签 | 柱状图配色 |
|--------|------|-----------|
| 85–100 | 🏆 强烈推荐 | `#534AB7`（紫） |
| 70–84 | ✅ 值得一看 | `#1D9E75`（绿） |
| 55–69 | 🔶 有选择性地看 | `#BA7517`（琥珀） |
| 40–54 | ⚠️ 慎重选择 | `#888780`（灰） |
| < 40 | ❌ 不建议 | `#A32D2D`（红） |

---

## Step 3 · 影院排片采集（猫眼/淘票票 web_search）

### 3.1 定位成功时（有具体城市/区域）

**工具优先级：** `agent-browser` > `博查 API` > `tavily-search`

#### 方案 A：Agent Browser 直接抓取（最准确，需安装）

**安装 Agent Browser（如未安装）：**

```bash
npm install -g agent-browser
agent-browser install
agent-browser install --with-deps
```

**使用示例：**

```bash
# 访问猫眼电影网页
agent-browser open "https://piaofang.maoyan.com/"
# 获取页面快照
agent-browser snapshot -i
# 根据快照元素交互，搜索排片
```

> ⚠️ 如 Agent Browser 未安装或不可用，降级使用方案 B（博查 API）

#### 方案 B：博查 API 搜索（实时性较好）

```bash
curl -X POST "https://api.bocha.cn/v1/web-search" \
  -H "Authorization: Bearer $BOCHA_API_KEY" \
  -d '{"query":"猫眼电影 [城市] [片名] 今日排片 场次 [日期]"}'
```

#### 查询模板（博查 API）

```
查询模板 A：猫眼电影 [城市] [片名] 今天 场次 选座 [当前日期]
查询模板 B：淘票票 [城市] [片名] 今日排片 [当前日期]
查询模板 C（备用）：[城市][区/商圈] [片名] 电影 今天几点 场次
```

目标：提取从当前时间起 **2 小时内** 开场的场次，每部影片列出 3–5 条。

采集字段：
- 影院名称
- 距离（若可获取）
- 场次时间（精确到分钟）
- 厅型（IMAX / 杜比全景声 / 中国巨幕 / 普通）
- 参考票价（若可获取）

### 3.2 抓取失败重试规则

| 失败情形 | 重试策略 |
|----------|----------|
| 猫眼查询无结果 | 立即改用淘票票同名查询 |
| 淘票票也无结果 | 改为 `[城市] [片名] 电影院 今天` 宽泛查询 |
| 三次均失败 | 标注"排片数据获取失败"，提供猫眼/淘票票 App 直达搜索提示，不伪造场次 |
| 数据疑似非今日 | 标注"⚠️ 场次信息可能非实时，请在购票前以 App 为准" |

### 3.3 定位失败时

- 仅知城市：输出城市级别今日排片热门场次概览（不含精准距离）
- 完全未知：影院排片模块留空，注明"请告知您的城市或区域以获取附近场次"

### 3.4 排片数据局限声明（每次必须输出）

> ⚠️ 以上排片信息通过猫眼/淘票票 web_search 实时抓取，可能存在延迟或不完整。最终场次与票价请以猫眼 / 淘票票 App 为准。

---

## Step 4 · 结构化输出报告

按以下固定结构输出，**不得省略任何模块**：

---

### 📍 检索信息

**位置**：[城市/区域 或 "未能定位"]
**检索时间**：[当前日期时间]
**数据来源**：猫眼、豆瓣、IMDb、淘票票、Rotten Tomatoes

---

### 🎬 当前公映推荐榜（Top 10）

对每部影片输出以下卡片：

```
### #[名次] [评级标签] 《片名》
**综合推荐分**：XX.X / 100

| 项目 | 内容 |
|------|------|
| 类型 / 片长 | XX / XX 分钟 |
| 导演 / 主演 | XX / XX、XX |
| 上映日期 | XXXX-XX-XX（已上映 X 天）|
| 豆瓣 | X.X / 10（X 万人评）|
| IMDb | X.X / 10 |
| 猫眼 | X.X / 10 |
| RT 专业新鲜度 | XX% |
| 累计内地票房 | X.XX 亿 |

**一句话定位**：[精准定位影片的一句话]

**独特卖点**：[与同档期其他影片相比的差异化亮点，1–2 句]

**代表性好评**（来源：XX，证据级别 X）：[简述，不直接大段引用]

**主要槽点**（来源：XX）：[1 条；若无明显槽点注明"口碑整体正面"]
```

---

### 📊 评分对比图（横向柱状图）— 浏览器渲染截图版

**重要：** 由于 IM 平台无法直接渲染 Canvas/Chart.js，必须使用浏览器渲染后截图的方式。

#### 执行流程

1. **生成 HTML 文件** → `/tmp/nowplaying-chart-{timestamp}.html`
2. **启动 HTTP 服务器** → `python3 -m http.server 8888 -d /tmp`
3. **浏览器打开并等待加载** → `browser open` + `loadState: networkidle`
4. **截图** → `browser screenshot` (fullPage: true)
5. **发送图片** → 使用 `message` 工具附带图片，或在 Feishu 中使用 `buffer` 参数

#### 柱状图规范

- Chart.js，type: `bar`，`indexAxis: 'y'`
- Y 轴：片名，按综合推荐分从高到低排列（推荐分最高者在顶部）
- X 轴：豆瓣评分（若无则猫眼评分），范围固定 0–10，步进 2
- 配色：按评级标签赋色（见 Step 2.3）
- Canvas 高度：动态计算 `(影片数量 × 44) + 80` px
- 图表上方输出自定义 HTML 图例（色块 + 标签文字）
- 禁用 Chart.js 默认图例
- Tooltip 格式：`片名：X.X 分`
- X 轴 `autoSkip: false`

#### HTML 模板示例

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>NowPlaying Chart</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
  <style>
    body { font-family: Arial, sans-serif; padding: 20px; background: #f5f5f5; }
    h2 { text-align: center; color: #333; }
    .chart-container { background: white; border-radius: 8px; padding: 20px; margin: 20px auto; max-width: 800px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
  </style>
</head>
<body>
  <h2> 当前公映影片评分对比</h2>
  <div class="chart-container">
    <canvas id="nowChart"></canvas>
  </div>
  <script>
    const labels = ['《片名 1》','《片名 2》',...];
    const scores = [X.X, X.X, ...];
    const colors = ['#534AB7','#1D9E75',...];
    new Chart(document.getElementById('nowChart'), {
      type: 'bar',
      data: { labels, datasets: [{ data: scores, backgroundColor: colors, borderRadius: 4, label: '评分' }] },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { min: 0, max: 10, ticks: { stepSize: 2, autoSkip: false } },
          y: { ticks: { font: { size: 12 } } }
        }
      }
    });
  </script>
</body>
</html>
```

#### 执行命令示例

```bash
# 1. 写入 HTML 文件
write path=/tmp/nowplaying-chart.html content="<html>..."

# 2. 启动 HTTP 服务器（后台）
exec command="cd /tmp && nohup python3 -m http.server 8888 > /tmp/http.log 2>&1 &" background=true

# 3. 等待服务器启动
exec command="sleep 2"

# 4. 浏览器打开
browser action=open url="http://localhost:8888/nowplaying-chart.html"

# 5. 截图
browser action=screenshot targetId="xxx" fullPage=true type="png"

# 6. 发送图片（Feishu）
message action=send channel=feishu buffer="data:image/png;base64,..." filename="nowplaying-chart.png"
```

---

### 🕸️ Top 3 六维蛛网图 — 浏览器渲染截图版

**重要：** 与柱状图相同，雷达图必须使用浏览器渲染后截图的方式，不能在消息中直接嵌入 Canvas 代码。

#### 执行流程

1. **生成合并 HTML 文件** → 包含柱状图 +3 张雷达图于单一 HTML
2. **启动 HTTP 服务器** → `python3 -m http.server 8888 -d /tmp`
3. **浏览器打开并等待加载** → `browser open` + `delayMs: 3000`
4. **截图** → `browser screenshot` (fullPage: true)
5. **发送图片** → 使用 `message` 工具附带图片

#### 雷达图规范

- 维度：剧本与叙事 / 视听语言 / 表演质感 / 导演掌控 / 情感共鸣 / [第六维度按类型动态选取]
- 得分由 AI 基于已采集口碑材料独立判断（0–10），标注证据级别（A/B/C）
- 配色：
  - Top 1: border `#534AB7` (紫), fill `rgba(83,74,183,0.18)`
  - Top 2-3: border `#1D9E75` (绿), fill `rgba(29,158,117,0.18)`
- Canvas 尺寸：`max-width: 480px; height: 380px`
- 每张图下方标注影片名称与综合推荐分
- 三张图垂直排列，图与图之间有卡片分隔

#### HTML 模板示例（合并柱状图 + 雷达图）

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>NowPlaying Charts</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
  <style>
    body { font-family: Arial, sans-serif; padding: 20px; background: #f5f5f5; }
    h2 { text-align: center; color: #333; margin-bottom: 10px; }
    .chart-container { background: white; border-radius: 8px; padding: 20px; margin: 15px auto; max-width: 600px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
    p { text-align: center; font-weight: bold; margin-top: 10px; color: #555; }
    .legend { display:flex;flex-wrap:wrap;gap:12px;margin-bottom:12px;font-size:12px;color:#666;justify-content:center; }
    .legend span { display:flex;align-items:center;gap:4px; }
    .legend .color-box { width:10px;height:10px;border-radius:2px; }
  </style>
</head>
<body>
  <h2>🎬 当前公映影片评分对比</h2>
  
  <!-- 柱状图 -->
  <div class="chart-container">
    <canvas id="barChart"></canvas>
  </div>
  
  <h2>🕸️ Top 3 六维评分雷达图</h2>
  
  <!-- 雷达图 1 -->
  <div class="chart-container">
    <canvas id="radar1"></canvas>
    <p>#1《片名 1》(XX/100)</p>
  </div>
  
  <!-- 雷达图 2 -->
  <div class="chart-container">
    <canvas id="radar2"></canvas>
    <p>#2《片名 2》(XX/100)</p>
  </div>
  
  <!-- 雷达图 3 -->
  <div class="chart-container">
    <canvas id="radar3"></canvas>
    <p>#3《片名 3》(XX/100)</p>
  </div>

  <script>
    // 柱状图
    new Chart(document.getElementById('barChart'), {
      type: 'bar',
      data: { 
        labels: ['《片名 1》','《片名 2》',...],
        datasets: [{ 
          data: [X.X, X.X, ...], 
          backgroundColor: ['#534AB7','#1D9E75',...], 
          borderRadius: 4 
        }] 
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { min: 0, max: 10, ticks: { stepSize: 2 } },
          y: { ticks: { font: { size: 12 } } }
        }
      }
    });

    // 雷达图 1
    new Chart(document.getElementById('radar1'), {
      type: 'radar',
      data: {
        labels: ['剧本与叙事','视听语言','表演质感','导演掌控','情感共鸣','科学硬度'],
        datasets: [{
          data: [9.0, 9.5, 9.0, 8.5, 9.5, 9.0],
          borderColor: '#534AB7',
          backgroundColor: 'rgba(83,74,183,0.18)',
          borderWidth: 2
        }]
      },
      options: {
        scales: { r: { min: 0, max: 10, ticks: { stepSize: 2 } } },
        plugins: { legend: { display: false } }
      }
    });

    // 雷达图 2
    new Chart(document.getElementById('radar2'), {
      type: 'radar',
      data: {
        labels: ['剧本与叙事','视听语言','表演质感','导演掌控','情感共鸣','紧张刺激'],
        datasets: [{
          data: [8.5, 8.0, 9.0, 8.5, 7.5, 9.0],
          borderColor: '#1D9E75',
          backgroundColor: 'rgba(29,158,117,0.18)',
          borderWidth: 2
        }]
      },
      options: {
        scales: { r: { min: 0, max: 10, ticks: { stepSize: 2 } } },
        plugins: { legend: { display: false } }
      }
    });

    // 雷达图 3
    new Chart(document.getElementById('radar3'), {
      type: 'radar',
      data: {
        labels: ['剧本与叙事','视听语言','表演质感','导演掌控','情感共鸣','喜剧节奏'],
        datasets: [{
          data: [7.5, 7.0, 8.5, 8.0, 7.5, 7.0],
          borderColor: '#1D9E75',
          backgroundColor: 'rgba(29,158,117,0.18)',
          borderWidth: 2
        }]
      },
      options: {
        scales: { r: { min: 0, max: 10, ticks: { stepSize: 2 } } },
        plugins: { legend: { display: false } }
      }
    });
  </script>
</body>
</html>
```

#### 执行命令示例

```bash
# 1. 写入 HTML 文件（包含柱状图 +3 张雷达图）
write path=/tmp/nowplaying-charts.html content="<html>..."

# 2. 启动 HTTP 服务器（后台）
exec command="cd /tmp && nohup python3 -m http.server 8888 > /tmp/http.log 2>&1 &" background=true

# 3. 等待服务器启动
exec command="sleep 2"

# 4. 浏览器打开并等待图表渲染
browser action=open url="http://localhost:8888/nowplaying-charts.html"
# 等待 3 秒确保 Chart.js 加载完成
browser action=snapshot targetId="xxx" delayMs=3000

# 5. 截图（全页）
browser action=screenshot targetId="xxx" fullPage=true type="png"

# 6. 读取截图并发送（Feishu）
# 截图路径：/home/admin/.openclaw/media/browser/{uuid}.jpg
# 使用 message 工具发送，带 buffer 参数
```

#### 注意事项

1. **等待时间**：必须等待至少 2-3 秒让 Chart.js 库加载和渲染完成
2. **fullPage 截图**：确保捕获所有图表
3. **图片格式**：浏览器截图默认保存为 JPG，路径格式 `/home/admin/.openclaw/media/browser/{uuid}.jpg`
4. **清理**：完成任务后可停止 HTTP 服务器（可选）

---

### 🏟️ 附近影院排片（2 小时内场次）

对推荐榜 Top 3–5 输出排片表：

```markdown
#### 《片名》— 附近场次（[当前时间] 起 2 小时内）

| 影院 | 距离 | 场次 | 厅型 | 票价 |
|------|------|------|------|------|
| XX 影院 | X.Xkm | HH:MM | IMAX | ¥XX |
| XX 影院 | X.Xkm | HH:MM | 普通 | ¥XX |
```

> ⚠️ 场次信息通过猫眼/淘票票 web_search 抓取，可能存在延迟，请以 App 为准购票。

若定位失败：
> 📍 未能获取您的具体位置，无法提供附近场次。
> 请告知您的城市/区域，或直接在**猫眼** / **淘票票**搜索上述影片今日排片。

---

### 💡 选片速查

根据不同观影需求给出快速导航（仅列出与当前榜单匹配的条目）：

- **口碑最高** → 《XXX》（豆瓣 X.X）
- **最新上映** → 《XXX》（X 天前上映）
- **票房最火** → 《XXX》（累计 X.XX 亿）
- **适合带小孩** → 《XXX》（若有）
- **情侣约会** → 《XXX》（若有）
- **大银幕/IMAX 首选** → 《XXX》（若有）
- **符合您的偏好** → 《XXX》⭐（若用户有偏好）

---

### 🔗 深度分析入口

> 如需对某部影片进行完整六维口碑分析，请回复：**"深度分析《XXX》"**
>（将自动触发 CineScope skill）

---

### 📅 数据时效声明（必须输出）

**每次报告末尾必须包含以下声明：**

```markdown
---

## 📌 数据时效声明

| 数据类型 | 更新时间 | 来源 | 实时性 |
|----------|----------|------|--------|
| 排片场次 | [检索时间] | 猫眼/淘票票 | ⚠️ 可能有延迟，以 App 为准 |
| 当日票房 | [检索时间] | 猫眼专业版 | ✅ 准实时（延迟<1 小时）|
| 豆瓣评分 | [检索时间] | 豆瓣网页 | ✅ 准实时 |
| 累计票房 | [检索时间] | 猫眼/灯塔 | ✅ 准实时 |

**数据截止时间：** [YYYY-MM-DD HH:MM]

**搜索工具：**
- 实时排片：博查 API / Agent Browser
- 口碑数据：Tavily Search
- 备用源：博查 API

> ⚠️ 以上排片信息通过 API 实时抓取，可能存在 1-2 小时延迟。
> **最终场次与票价请以猫眼 / 淘票票 App 为准购票。**
```

---

## 异常处理规则

| 情况 | 处理方式 |
|------|----------|
| 某部影片豆瓣尚未开分 | 标注"⚡ 豆瓣未开分"，以猫眼/IMDb 替代计算口碑分，并降低该项权重 |
| 上映不足 3 天且评分人数 < 5000 | 影片卡顶部标注"⚡ 样本极少，评分参考性有限" |
| 影院排片三次搜索均失败 | 标注失败原因，提供猫眼/淘票票 App 直达提示，不伪造场次 |
| 场次信息疑似非今日 | 标注"⚠️ 场次信息可能非实时"并给出 App 核实提示 |
| 用户偏好与 Top 10 全不匹配 | 榜单外单独推荐 1 部"偏好精准匹配"影片，标注"不在热映主榜，但符合您的偏好" |
| 海外用户（无中文院线） | 切换为 IMDb / RT 推荐逻辑，影院排片改为提示通过 Google Maps 搜索附近影院 |
