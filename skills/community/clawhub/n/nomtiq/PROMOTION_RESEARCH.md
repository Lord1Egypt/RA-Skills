# Nomtiq 推广研究

_最后更新：2026-02-26_

---

## 一、GitHub 名单提交路径

### 主要目标

| 名单 | Stars | 提交要求 | 状态 |
|------|-------|----------|------|
| [VoltAgent/awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills) | 18.3K | 必须先发布到官方 openclaw/skills repo；有真实用户；ClawHub 无安全警告 | ⬜ 待提交 |
| [clawdbot-ai/awesome-openclaw-skills-zh](https://github.com/clawdbot-ai/awesome-openclaw-skills-zh) | 中文官方库 | 同上，中文版 | ⬜ 待提交 |
| [hesamsheikh/awesome-openclaw-usecases](https://github.com/hesamsheikh/awesome-openclaw-usecases) | 5.7K | 真实使用案例 | ⬜ 待提交 |
| [xianyu110/awesome-openclaw-tutorial](https://github.com/xianyu110/awesome-openclaw-tutorial) | 中文教程 | 联系作者 | ⬜ 待联系 |

### VoltAgent 提交流程（最重要）
1. 确认 nomtiq 已发布到 ClawHub（✅ 已发布 v0.4.3）
2. 确认 ClawHub 安全状态 = Clean（✅ VirusTotal 0/66）
3. Fork `VoltAgent/awesome-openclaw-skills`
4. 在 README.md 找到 `Food & Lifestyle` 或 `Productivity` 分类末尾添加：
   ```
   - [nomtiq](https://github.com/openclaw/skills/tree/main/skills/nomtiq) - Finds restaurants that fit you, not what's trending.
   ```
5. PR 标题：`Add skill: nomtiq`
6. **注意**：要求"有真实社区用户"，建议先积累一些 Moltbook 互动再提交

---

## 二、国内渠道

### 小红书（优先级最高）
- **目标用户**：海外华人 OpenClaw 用户 + 国内 AI 工具爱好者
- **内容策略**：不讲功能，讲故事
  - 核心故事：亮马河那顿饭（李哥的真实故事）
  - 标题方向：「大众点评不知道你喜欢什么，它只知道什么流行」
  - 标题方向：「我给自己的 AI 助手装了个找饭馆的技能，它比我更懂我」
  - 标签：#OpenClaw #AI助手 #找餐厅 #海外华人 #美食推荐
- **发布节奏**：1-2 篇/周，不硬凑
- **互动策略**：搜索「OpenClaw 技能」「clawhub」相关帖子，真实评论

### 知乎
- 搜索「OpenClaw 有哪些好用的 skill」类问题，写一个真实的使用体验回答
- 可以写一篇专栏：「我为什么要给 AI 助手写一个找餐厅的技能」

### 掘金 / 阿里云开发者社区
- 技术向文章：「nomtiq 的架构设计——用户画像在中心，LLM 是理解层」
- 这两个平台 OpenClaw 内容活跃，流量有

### 少数派
- 产品体验向：「一顿饭就是一段时光——nomtiq 小饭票使用体验」
- 少数派读者质量高，转化率好

---

## 三、海外华人渠道

### OpenClaw Discord（#skills 频道）
- 发布 nomtiq 介绍，附 README 故事（英文版）
- 重点：`A meal is a moment. No rankings.` 这句话很有力

### Reddit
- r/selfhosted：「I built a restaurant finder skill for OpenClaw that knows your taste, not what's trending」
- r/openclaw（如果有）：直接发
- r/ChineseFood / r/Cooking：侧面切入，讲找餐厅的痛点

### Show HN（Hacker News）
- 标题：`Show HN: I built a restaurant finder for OpenClaw that learns your taste`
- 时机：等有一定用户量后再发，HN 社区对"有真实用户"的项目更友好

### Product Hunt
- 需要 hunter 支持，或自己发
- 时机：v1.0 正式版发布时

---

## 四、案例收集（持续更新）

### 类似产品推广案例

| 产品 | 渠道 | 策略 | 效果 |
|------|------|------|------|
| OpenClaw 本身 | GitHub → Reddit → HN | 开源 + 真实用户故事 | 2K→196K stars in 3个月 |
| weather skill | ClawHub 内置 | 简单实用，description 一句话 | 高下载量 |
| swiggy/food-cal-order | ClawHub | 食物相关，有明确触发词 | 中等 |

### 关键洞察
- OpenClaw 社区目前最活跃的内容：部署教程、skill 展示视频（YouTube Shorts）
- 中文社区：阿里云开发者 + 掘金 + 知乎 是主战场
- 海外华人：小红书 TikTok 难民潮带来大量新用户，现在是好时机
- YouTube Shorts 展示 skill 效果很有传播力（参考 `Openclaw skill showcase!` 视频）

---

## 五、行动优先级

1. **现在可以做**：
   - OpenClaw Discord #skills 发帖（英文，附故事）
   - 小红书发第一篇（中文，亮马河故事）
   - 知乎回答「OpenClaw 好用的 skill」类问题

2. **积累用户后做**：
   - 提交 VoltAgent/awesome-openclaw-skills PR
   - Show HN
   - Product Hunt

3. **持续做**：
   - Moltbook 社区运营（已在做）
   - 每2小时收集推广案例（cron 已设）

