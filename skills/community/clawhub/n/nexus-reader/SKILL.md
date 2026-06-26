---
name: nexus-reader
description: 微信读书飙升榜每日推荐卡片生成器。从微信读书飙升榜抓取热门书籍数据，生成精美的每日读书推荐卡片（HTML/PNG）。当用户说「读书推荐」「微信读书」「飙升榜」「今日好书」「推荐一本书」「读书卡片」「book recommendation」时触发。也可用于每日定时推送读书推荐场景。
---

# nexus-reader - 微信读书飙升榜每日推荐

生成精美的每日读书推荐卡片，数据来源于[微信读书飙升榜](https://weread.qq.com/web/category/rising)。

## 核心工作流程（四步）

### Step 1：抓取榜单数据

```bash
python scripts/reader.py --fetch-only
```

脚本会自动：
1. 抓取微信读书飙升榜（20本书）
2. 保存原始数据到 `data/weread_rising_YYYY-MM-DD.json`
3. 输出榜单摘要（书名、作者、推荐值）

输出示例：
```
[抓取] 正在获取微信读书飙升榜...
[解析] 找到 20 个书籍项
[保存] 数据已缓存: data/weread_rising_2026-05-04.json

==================================================
飙升榜 TOP 20
==================================================
  1. 《阿勒泰的角落》- 李娟 (推荐值: 88.4%)
  2. ...
```

> **缓存机制**：当天JSON文件 < 1小时自动跳过重新抓取，`--force` 强制刷新

---

### Step 2：模型选书 + 创作内容

读取 `data/weread_rising_YYYY-MM-DD.json`，从TOP10中选一本书，然后**自己创作**以下内容（不要直接复制书籍简介）：

| 字段 | 说明 | 字数建议 |
|------|------|----------|
| `title` | 金句标题，根据书籍主题提炼一句有深度、有力量的话 | 8-15字 |
| `yi` | 宜××，结合书籍主题创作 | 4-6字 |
| `ji` | 忌××，结合书籍主题创作 | 4-6字 |
| `book_desc` | 推荐语，用温暖、有感染力的语言为这本书写一段推荐 | 50-100字 |

示例（推荐《百年孤独》）：
```json
{
  "title": "每个人都在守护自己的孤独",
  "yi": "静心阅读",
  "ji": "浮躁焦虑",
  "book_desc": "马尔克斯用一座虚构的小镇，写尽了人类共有的孤独与执念。每一次重读，都会在某个角色身上看见自己。适合在一个安静的下午，泡一杯咖啡，慢慢走进马孔多。"
}
```

> **重要**：`book_desc` 是 LLM 的创作内容，不是书籍简介的截取！

---

### Step 3：生成 card JSON 文件

将以下内容保存为 `data/nexus-reader-YYYYMMDD.json`：

```json
{
  "date": "2026/05/04",
  "day": "04",
  "weekday": "星期日",
  "lunar_date": "农历 四月十八",
  "yi": "静心品读",
  "ji": "焦虑内耗",
  "title": "有一分热就去发光",
  "book_title": "阿勒泰的角落",
  "book_author": "李娟",
  "book_desc": "...（LLM创作的推荐语）",
  "cover_url": "https://weread-1258476245.cos.ap-nanjing.myqcloud.com/...",
  "book_url": "https://weread.qq.com/web/reader/...",
  "rating": "88.4%",
  "reading_count": "1486"
}
```

> **提示**：`cover_url`、`book_url`、`rating`、`reading_count`、`book_title`、`book_author` 从 `weread_rising_YYYY-MM-DD.json` 中对应的书籍项获取。其余字段由 LLM 创作或计算。

---

### Step 4：渲染卡片

```bash
# 只生成 HTML
python scripts/reader.py --card data/nexus-reader-2026-05-04.json

# 生成 HTML + PNG 图片
python scripts/reader.py --card data/nexus-reader-2026-05-04.json --png
```

输出：
- `data/nexus-reader-YYYYMMDD.html` — 精美推荐卡片
- `data/nexus-reader-YYYYMMDD.png` — PNG 图片（需加 `--png`）

然后用 `preview_url` 打开 HTML 卡片展示给用户。

---

## 命令行参数速查

| 命令 | 说明 |
|------|------|
| `--fetch-only` | 阶段1：只抓取数据 |
| `--card JSON_PATH` | 阶段2：渲染指定 JSON 的卡片 |
| `--png` | 额外生成 PNG（需配合 `--card`） |
| `--output DIR` | 指定输出目录 |
| `--force` | 强制重新抓取 |
| `--cache-hours N` | 缓存有效时间（小时，默认1） |

> `--fetch-only` 和 `--card` 互斥，必须指定其中一个

---

## 数据结构

### 原始榜单 JSON（`weread_rising_YYYY-MM-DD.json`）

从微信读书抓取的原始数据，包含20本书：

```json
[
  {
    "index": "1",
    "title": "阿勒泰的角落",
    "author": "李娟",
    "desc": "书籍简介...",
    "cover_url": "https://...",
    "book_url": "https://weread.qq.com/...",
    "reading_count": "1486",
    "rating": "88.4%",
    "date": "2026-05-04"
  }
]
```

### 卡片 JSON（`nexus-reader-YYYYMMDD.json`）

由 LLM 创作内容后生成的完整卡片数据，用于渲染：

```json
{
  "date": "2026/05/04",
  "day": "04",
  "weekday": "星期日",
  "lunar_date": "农历 四月十八",
  "yi": "静心品读",
  "ji": "焦虑内耗",
  "title": "有一分热就去发光",
  "book_title": "阿勒泰的角落",
  "book_author": "李娟",
  "book_desc": "李娟用质朴的笔触...",
  "cover_url": "https://...",
  "book_url": "https://...",
  "rating": "88.4%",
  "reading_count": "1486"
}
```

---

## 卡片设计说明

卡片采用暖色调书卷风格：
- 背景：`#fdfcfa`（米白色）+ 淡雅渐变
- 主色：`#9d7a58`（古铜色）用于日期
- 字体：`Noto Serif SC`（宋体风格衬线字体）
- 结构：日期 → 宜忌 → 金句标题+推荐语+书名 → 分隔线 → 封面+详情+阅读按钮

---

## 农历日期计算

`lunar_date` 字段由 LLM 根据当天日期计算，格式为 `农历 X月XX日`。

示例中 `LUNAR_MONTHS` 为简化版本，实际农历需要专用库（`lunarcalendar`）或 LLM 直接计算。推荐让 LLM 直接计算，避免额外依赖。

---

## 注意事项

- 微信读书页面不需要登录即可查看飙升榜
- 封面图片来自 CDN，可能在某些网络环境下无法加载
- `--png` 需要安装 `html2image`：`pip install html2image`
- 推荐值和阅读人数是实时数据，每天不同
- 如果抓取失败，脚本会尝试使用旧缓存降级

---

## 定时推送场景

当用户要求每日定时推送读书推荐时，创建 automation（recurring）：
1. prompt 内容：运行 `reader.py --fetch-only` → LLM 创作内容 → 生成 card JSON → 运行 `reader.py --card` [--png] → 推送
2. schedule 为每日固定时间（如 `RRULE:FREQ=DAILY;BYHOUR=8;BYMINUTE=0`）
