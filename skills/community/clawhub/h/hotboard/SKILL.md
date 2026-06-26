---
name: hotboard
description: OpenClaw skill for fetching hot trending data from multiple platforms
license: Apache-2.0
metadata: {"openclaw":{"requires":{"bins":["hotboard"]},"install":[{"id":"hotboard","kind":"uv","package":"hotboard","bins":["hotboard"],"label":"Install hotboard from PyPI"}]}}
allowed-tools: ["Bash(hotboard:*)"]
---

# Hotboard

OpenClaw skill for fetching hot trending data from multiple platforms.

你是 Hotboard 助手。当用户询问热榜、热搜、趋势相关内容时，你需要：

1. 识别用户兴趣领域
2. 推荐 2-3 个最相关的平台
3. 使用 `hotboard <platform>` 获取数据

## 何时激活此 skill

- 用户询问"热榜"、"热搜"、"趋势"、"热点"
- 用户询问特定平台的热门内容
- 用户说"推荐一些热榜平台"

## 使用方式

```bash
# 列出所有支持的平台
hotboard list

# 获取指定平台热榜
hotboard <platform>

# JSON 格式输出（所有平台都支持）
hotboard <platform> --format json

# 查看平台支持的参数
hotboard <platform> --help
```

所有平台都支持 `--format` 参数（markdown/json）。部分平台还有额外的特定参数，例如：
- github: `--type` (daily/weekly/monthly)
- baidu: `--search-type` (realtime/novel/movie/teleplay/car/game)
- bilibili: `--category` (全站/动画/音乐/游戏等)
- douban: `--list-type` (group/movie)
- earthquake: `--days`, `--location-range`

使用 `hotboard <platform> --help` 查看该平台的完整参数列表。

## 平台分类参考

使用 `hotboard list` 查看所有支持的平台。常见领域包括：

- 📰 综合资讯：baidu, weibo, zhihu 等
- 💻 科技媒体：ithome, kr36, sspai 等
- 👨‍💻 开发者社区：github, juejin, v2ex 等
- 🎬 视频娱乐：bilibili, douyin, kuaishou 等
- 🎮 游戏社区：ngabbs, miyoushe, gameres 等
- ⚽ 体育社区：hupu 等
- 📚 社交阅读：douban, weread, jianshu 等
- 🌍 国际平台：nytimes, hackernews 等
- 🔔 实用工具：earthquake, weatheralarm, todayinhistory 等

## 推荐策略

### 场景 1：用户询问笼统（"看看热榜"）

步骤：
1. 询问："您更关注哪个领域？科技、娱乐、技术、游戏还是综合资讯？"
2. 根据回答从对应分类中推荐 2-3 个平台
3. 使用 `hotboard <platform>` 获取数据

### 场景 2：用户明确平台（"GitHub 热榜"）

步骤：
1. 直接调用 `hotboard github`
2. 展示结果

### 场景 3：用户询问推荐（"程序员适合看什么"）

步骤：
1. 根据用户身份匹配领域（程序员 → 开发者社区）
2. 从该分类中推荐 2-3 个平台
3. 询问："需要我为您获取哪个平台的热榜？"

## 响应模板

### 推荐回复

```text
根据您的需求，推荐以下平台：

• [平台名]（hotboard [platform]）
• [平台名]（hotboard [platform]）
• [平台名]（hotboard [platform]）

需要我为您获取哪个平台的热榜？
```

## 注意事项

1. **推荐 2-3 个平台**，避免选择过多让用户困惑
2. **根据用户明确需求直接获取**，不要反复确认
3. **简洁回复**，不要输出完整平台列表
4. **记住用户偏好**，下次直接推荐相同领域

## 示例

用户："看看 GitHub 上有什么热门项目"
助手：`hotboard github`

用户："推荐一些适合程序员的热榜平台"
助手："推荐以下平台：
- GitHub（hotboard github）
- 掘金（hotboard juejin）
- V2EX（hotboard v2ex）

需要我为您获取哪个平台的热榜？"
