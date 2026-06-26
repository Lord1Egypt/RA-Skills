---
name: obsidian-clipper
description: >
  Save web content (articles, videos, notes) to Obsidian vault with automatic classification,
  intelligent naming, and content extraction. Supports: 小红书 (Xiaohongshu), YouTube, 知乎,
  WeChat articles, and general web pages. Auto-categorizes based on configurable rules.
  Trigger words: 收藏, 保存到obsidian, 归档, clip, save to obsidian. Use when user sends links
  or asks to save content to Obsidian.
version: 2.0.0
author: Lucien L
license: MIT
tags: [obsidian, clipper, web-scraping, content-management, 小红书, youtube, 知乎]
---

# Obsidian Clipper

将网页、文章、视频、小红书笔记等内容收藏到 Obsidian vault。

## 配置

Skill **首次运行时**，必须先确认以下配置。读取 `config.json`（与本 SKILL.md 同目录），不存在则**询问用户**并创建。

### config.json 格式

```json
{
  "vault_path": "/path/to/your/vault/收藏文档/",
  "collector_name": "你的名字",
  "categories": {
    "AI工具": ["AI", "机器学习", "LLM", "GPT", "Claude", "OpenClaw", "Agent", "量化"],
    "兴趣爱好": ["路亚", "钓鱼", "户外", "游戏", "音乐", "运动", "3D打印"],
    "技术教程": ["编程", "代码", "教程", "开发", "配置", "部署", "API", "DevOps"],
    "生活日常": ["美食", "旅行", "健康", "生活技巧", "读书"]
  }
}
```

### 配置项说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `vault_path` | ✅ | Obsidian Vault 中收藏文档的根目录路径（绝对路径，末尾带 `/`） |
| `collector_name` | ❌ | 签名用的名字，默认不签名 |
| `categories` | ❌ | 自动分类规则，键=目录名，值=关键词数组。默认包含常用分类（见示例） |

### 首次运行流程

1. 检查 `config.json` 是否存在
2. 不存在 → 询问用户 Vault 路径，分类使用默认值
3. 创建 `config.json` 保存配置
4. 后续运行直接读取，用户可随时要求修改

### 用户修改配置

用户随时可以说：
- "把 Vault 路径改成 xxx"
- "加一个「读书笔记」分类"
- "我的名字改成 xxx"
→ 更新 `config.json`

## 文件命名规范

**格式**: `「来源类型」主题-YYYY.MM.DD.md`

**来源类型**:
- `「小红书」` — 小红书笔记
- `「Youtube视频」` — YouTube 视频
- `「B站视频」` — B站视频
- `「知乎文章」` — 知乎文章
- `「公众号」` — 微信公众号文章
- `「网页」` — 普通网页
- `「技术文档」` — 官方文档、技术博客
- `「短视频」` — 抖音/快手等短视频

## 标题提取策略

按优先级获取标题：
1. **页面 `<title>` 标签** — 最可靠
2. **og:title meta 标签** — 社交平台常用
3. **搜索结果中的标题** — web_search 返回的 title
4. **用户消息中的描述** — 用户发送时的上下文

**原则**：标题简洁、准确。过长时（>50字）截取核心部分。

## 工作流程

### 1. 接收输入

用户可能提供：
- 直接链接（小红书、YouTube、知乎、公众号等）
- 内容描述 + 要求收藏
- 多个链接批量处理
- 截图 + 要求收藏

### 2. 获取内容

根据来源类型选择方法（三层降级）：

```
第一层：web_fetch 直接抓取
  ↓ 失败
第二层：web_search 搜索相关内容，整合补充
  ↓ 搜索无结果
第三层：浏览器打开页面抓取（browser snapshot）
  ↓ 仍失败
提示用户提供内容（复制文字/截图）
```

#### 各平台策略

| 平台 | 识别特征 | 策略 |
|------|---------|------|
| 普通网页/知乎 | 通用 URL | web_fetch → web_search |
| 小红书 | `xhslink.com` | ⚠️ 登录墙，web_search 降级 |
| 微信公众号 | `mp.weixin.qq.com` | ⚠️ 必须用浏览器抓取 |
| 抖音/快手 | `v.douyin.com` / `douyin.com` | ❌ 无法解析，提示用户截图/复制文字 |
| YouTube | `youtube.com` / `youtu.be` | web_search 搜索标题 + 要点 |
| B站 | `bilibili.com` / `b23.tv` | web_fetch → web_search |

### 3. 自动分类

读取 `config.json` 中的 `categories` 规则，**默认自动分类，不打扰用户**：
1. **用户明确指定** → 直接使用，无视关键词匹配
2. **关键词匹配** → 遍历 categories，内容包含关键词最多的分类胜出
3. **无匹配** → 归入第一个分类，不询问
4. 用户说"放到 XX" → 直接创建 `vault_path/XX/` 目录

**原则：静默自动分类。只在用户主动要求时才讨论分类。**

### 4. 生成文档

**Markdown 模板**:

```markdown
# {标题}

**来源**: {来源链接或描述}
**保存日期**: {YYYY.MM.DD}
**类别**: {分类名}

---

## 摘要

{简短摘要，1-3句话}

---

## 正文内容

{整理后的内容}

---

## 关键要点

- {要点1}
- {要点2}
- {要点3}

---

## 相关链接

- {原始链接}
- {其他参考}

---
{如果 config.json 中设置了 collector_name，追加：*收藏人: {collector_name}*}
```

### 5. 保存文件

1. 从 `config.json` 读取 `vault_path` + 确定分类
2. 确定文件名
3. 使用 `write` 工具保存（自动创建目录）
4. 回复用户：✅ 已保存 + 路径 + 核心要点

## 批量收藏

用户一次发送多个链接时，逐个处理，统一回复：

```
✅ 已保存 3 篇到 Obsidian

1. 「小红书」AI转3D工具 → AI工具/
2. 「小红书」路亚教程 → 兴趣爱好/
3. 「小红书」OpenClaw优化 → AI工具/
```

## 注意事项

1. **首次运行必须配置** — 读取或创建 `config.json`
2. **小红书/抖音** — 有登录墙，降级到搜索或提示用户提供内容
3. **公众号文章** — 必须用浏览器抓取
4. **默认自动分类** — 静默完成，不打扰用户。无匹配时归入第一个分类
5. **内容过长** — 提取核心要点
6. **日期格式** — 统一 `YYYY.MM.DD`
7. **浏览器用完关闭** — browser open 后记得 close
8. **不要硬编码个人路径/名字** — 一切从 config.json 读取
