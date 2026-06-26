---
name: latte-news-fetcher-v2
description: |
  新闻获取与RSS订阅工具。从免费信源获取新闻，支持RSS订阅和Tavily搜索。
  触发词：新闻、今日新闻、RSS、订阅、阅读。
metadata:
  openclaw:
    requires:
      bins:
        - node
    optionalEnv:
      - TAVILY_API_KEY
    install:
      - kind: node
        package: node-fetch
        bins: []
    emoji: "📰"
---

# Latte News Fetcher V2 - 新闻获取工具 ☕

获取新闻列表，搜索相关报道，深入了解新闻内容。

---

## 🚀 核心流程

### 首次使用：初始化偏好

**检查配置文件** `CONFIG/news-preferences.md`（workspace 根目录）

如果用户偏好为空，执行初始化：

```
询问用户：
"你想要看哪些方面的新闻？可以选择以下类别，也可以告诉我你常看的网站："

🌍 国际时事 - BBC、Reuters、Al Jazeera
🇨🇳 国内要闻 - 人民网、新华网、澎湃新闻
💰 财经金融 - 财联社、Bloomberg、华尔街见闻
💻 科技互联网 - 36氪、The Verge、虎嗅
⚽ 体育娱乐 - 虎扑、ESPN、新浪体育
📊 商业市场 - 界面、财新、第一财经

你也可以直接告诉我你想关注的网站。"
```

**保存偏好** → 写入 `CONFIG/news-preferences.md`（workspace 根目录）

---

### 日常使用：获取今日新闻

**触发场景（两种）：**

1. **通用请求**：用户问"今天有什么新闻"、"看看新闻"等
   - → 读取用户偏好配置，获取偏好类别对应的网站

2. **指定网站**：用户问"看看华尔街日报今天有什么新闻"、"BBC今天新闻"等
   - → 直接访问用户指定的网站，跳过偏好检查

---

### 📰 获取新闻首页

#### 工具选择优先级

| 优先级 | 工具 | 适用场景 | 说明 |
|--------|------|----------|------|
| 🔴 **首选** | `browser` | WSJ、Bloomberg、NYT、FT 等主流媒体 | 能处理 JS 渲染和复杂页面 |
| 🟡 备选 | `web_fetch` | BBC、Reuters、AP 等开放网站 | 轻量级，速度快 |
| 🟢 兜底 | Tavily 搜索 | 首页获取失败时 | 搜索 `site:xxx.com` 获取今日新闻 |

#### 首页获取流程

```
1. browser 打开网站首页
   browser action=open url="https://cn.wsj.com" profile="openclaw"
   
2. 等待页面加载（3-5秒）
   browser action=act kind=wait timeMs=5000
   
3. 获取页面快照
   browser action=snapshot
   
4. 从快照中提取新闻标题和链接

5. 关闭浏览器
   browser action=close
```

---

### 输出格式（纯文本 Markdown）

使用 `message` 工具发送纯文本消息：

```markdown
**[来源名称] 今日新闻** (YYYY-MM-DD)

---

**🔥 热门文章**

1. [标题](原文链接) | 类别
   简短摘要（1-2行）

2. [标题](原文链接) | 类别
   简短摘要

---

**🌍 国际**

- [标题](原文链接) | 摘要

**🇨🇳 中国**

- [标题](原文链接) | 摘要

**💰 财经**

- [标题](原文链接) | 摘要

**💻 科技**

- [标题](原文链接) | 摘要

---

对哪条新闻感兴趣？我可以帮你搜索相关报道或替代信源。
```

---

## 📋 核心类别与知名网站

| 类别 | 首选网站 | 备选网站 |
|------|----------|----------|
| 🌍 **国际时事** | BBC、Reuters、Al Jazeera | AP News、DW、NHK World |
| 🇨🇳 **国内要闻** | 人民网、新华网、澎湃新闻 | 中国新闻网、环球网 |
| 💰 **财经金融** | 财联社、Bloomberg、华尔街见闻 | Reuters财经、第一财经 |
| 💻 **科技互联网** | 36氪、The Verge、虎嗅 | TechCrunch、钛媒体 |
| ⚽ **体育娱乐** | 虎扑、ESPN、新浪体育 | BBC Sport、懂球帝 |

---

## 🔍 深入新闻：获取全文

**触发：用户说"详细了解 XX"、"展开第 X 条"等**

### 获取优先级

```
1. web_fetch 直接获取（免费信源）
      ↓ 失败
2. browser 访问页面
      ↓ 失败
3. 搜索替代信源（Tavily API）
      ↓ 失败
4. 诚实告知 + 提供已获取的摘要
```

---

## 🔎 搜索替代信源

**使用 Tavily API 搜索同一事件的免费报道：**

```bash
node scripts/fetch_news.mjs https://example.com/article --search "关键词"
```

**替代优先级**：
1. BBC / Reuters / AP（国际通讯社）
2. 官方来源（如政府公告）
3. 其他免费媒体
4. 综合多信源整理

---

## 🛠️ 工具选择速查表

### 获取新闻列表

| 场景 | 推荐工具 |
|------|----------|
| 主流媒体首页 | `browser` |
| 开放媒体 | `web_fetch` 或 `browser` |
| 首页获取失败 | Tavily 搜索 |

### 获取文章全文

| 场景 | 工具 |
|------|------|
| 公开信源 | `web_fetch` |
| 复杂页面 | `browser` |
| 找不到原文 | Tavily 搜索替代信源 |

---

## ⚠️ 注意事项

1. **链接格式** - 新闻列表使用 `[标题](原文链接)` 格式
2. **热门新闻** - 选择当天最热门的内容
3. **优先免费信源** - BBC/Reuters/AP 是第一选择
4. **诚实透明** - 无法获取时明确告知 + 提供替代
5. **输出格式** - 使用纯文本 Markdown

---

## 📝 更新日志

- **1.0.0** (2026-03-10) - 首个版本
  - 新闻列表获取
  - Tavily 搜索替代信源
  - RSS 订阅支持
  - 纯文本 Markdown 输出

---

_最后更新: 2026-03-10_
