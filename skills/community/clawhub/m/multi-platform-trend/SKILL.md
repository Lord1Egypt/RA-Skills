---
slug: multi-platform-trend
name: 多平台热点聚合
version: "1.0.0"
author: 千策
---


# 多平台热点聚合

一站式抓取中国主流平台实时热点，返回结构化数据供后续分析使用。

## 核心能力

1. **多平台抓取** — 知乎热榜、微博热搜、百度热搜、B站排行榜
2. **热度数据** — 获取每个热点的热度值和排名
3. **按平台/关键词过滤** — 支持按平台或关键词筛选
4. **结构化JSON输出** — 便于后续AI分析或程序处理

## 快速开始

用户说"今天什么热点"时：

```
1. 运行 python3 scripts/fetch_trends.py --all
2. 呈现各平台热点列表
3. 用户选择感兴趣的热点
4. 将热点标题发给 AI 进行选题分析和内容创作
```

## 支持平台

| 平台 | 数据源 | 更新速度 |
|------|--------|----------|
| 知乎热榜 | api.zhihu.com | 实时 |
| 微博热搜 | weibo.com/ajax | 实时 |
| 百度热搜 | top.baidu.com | 实时 |
| B站排行榜 | api.bilibili.com | 每日 |

## 使用方式

### 查看所有平台热点
```bash
python3 scripts/fetch_trends.py --all --limit 20
```

### 查看单平台
```bash
python3 scripts/fetch_trends.py --platform zhihu --limit 10
python3 scripts/fetch_trends.py --platform weibo --limit 10
python3 scripts/fetch_trends.py --platform baidu --limit 10
python3 scripts/fetch_trends.py --platform bilibili --limit 10
```

### 按关键词过滤
```bash
python3 scripts/fetch_trends.py --all --keyword "AI"
python3 scripts/fetch_trends.py --all --keyword "科技"
```

### JSON 输出（供程序处理）
```bash
python3 scripts/fetch_trends.py --all --json
```

## 输出格式

### 文字报告
```
📊 今日热点速览（2026-04-19）

🔥 知乎 | 15 条
  1. 追觅科技砸2亿年薪招首席科学家  🔥152万
  2. OpenAI发布新模型  🔥98万
  ...

🔥 微博 | 15 条
  1. [热]明星官宣新恋情  🔥850万
  ...
```

### JSON 输出（推荐用于程序处理）
```bash
python3 scripts/fetch_trends.py --all --json
```
返回字段：title / platform / heat / heat_display / url / category / excerpt

## 后续处理建议

获取热点列表后，用户可将标题和摘要复制给 AI 进行选题分析和内容创作。Skill本身只负责数据抓取，不包含自动分析功能。

## 配置项

| 配置 | 说明 | 默认值 |
|------|------|--------|
| 监控平台 | 抓取哪些平台 | 知乎+微博+百度 |
| 过滤关键词 | 只看哪些领域 | 无（全部） |
| 抓取数量 | 每个平台取几条 | 15条 |

## 文件结构

```
multi-platform-trend/
├── SKILL.md              # 本文件
├── scripts/
│   ├── fetch_trends.py   # 热点抓取脚本
│   └── config.json       # 用户配置（运行时生成）
└── assets/               # 评分参考文件（可选）
```

## 与其他 Skill 的配合

- **cn-auto-publisher**：热点分析后，生成内容可交给 cn-auto-publisher 发布到知乎/小红书
- **rss-content-flow**：热点 + RSS = 完整内容来源

## 注意事项

- API 请求设置合理的超时（10秒），失败时自动跳过
- 微博热搜需要 User-Agent 伪装，已在脚本中处理
- 热度数据为估算值，仅供参考
- 本 Skill 只负责热点数据抓取，不包含选题分析和内容生成功能

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
