---
name: movie-rec-personal-cn
description: 猫眼电影个性化推荐系统——每周抓取中国大陆新上映/即将上映电影，基于用户观影偏好档案智能排序推荐，推送飞书周报
user-invocable: true
allowed-tools: Bash(python3:*), Read, Write
metadata:
  version: "1.0.1"
  author: ljd
  tags: [movie, recommendation, maoyan, feishu, china, cron]
---

# 猫眼电影个性化推荐系统

每周从猫眼电影 API 抓取中国大陆正在热映和即将上映的全部电影，结合用户观影偏好档案，由 LLM 进行智能匹配、排序和推荐，生成飞书周报推送。

## 需求

- Python 3.6+（脚本仅依赖标准库 `urllib` + `json`，无需额外安装）
- 飞书渠道已配置（用于推送周报）
- 网络可访问猫眼 API（`m.maoyan.com`）

## 工作原理

```
每周定时触发
     │
     ▼
① 数据采集：python3 scripts/maoyan_movies.py
   → 输出 movies.json（全量电影数据）
     │
     ▼
② 偏好匹配：AI 读取 movies.json + profile.json
   → LLM 基于 core_traits / recommendation_rules 智能排序
     │
     ▼
③ 生成周报：结构化 Markdown 格式
   → 分级推荐：🎯 强烈推荐 / 👍 值得关注 / 👀 可观望
     │
     ▼
④ 飞书推送：发送到用户会话
```

### 数据采集脚本

`scripts/maoyan_movies.py` 调用猫眼移动端 API：

| API | 说明 |
|-----|------|
| `ajax/movieOnInfoList` | 正在热映列表 |
| `ajax/comingList?ci=10` | 即将上映列表（极限 100 部） |
| `ajax/detailmovie?movieId=` | 单部电影详情（类型、导演、时长、制片国家等） |

输出 JSON 包含 `now_showing`（正在热映）、`coming`（即将上映）两个列表，每部电影含：片名、上映日期、评分、主演、类型、导演、制片国家、时长、想看人数等字段。

### 偏好匹配逻辑

AI 读取 `profile.json` 中的：

- **`liked_movies`**：用户已喜欢/观看的电影，每部标注了喜欢的理由和特征标签 → LLM 用于学习用户口味
- **`want_to_watch`**：用户已知且想看但还没看的 → 与新片列表交叉比对，命中时直接标记「你已标记想看」
- **`core_traits`**：用户观影偏好骨架（类型偏好、IP 偏好、风格倾向、排除信号）
- **`recommendation_rules`**：匹配规则（优先级逻辑、boost/downgrade 关键词）

LLM 对每部未看过的电影打分，按匹配度排序，输出三级推荐。

## 安装

```bash
# 1. 安装 skill（通过 ClawHub 或手动复制）
clawhub install movie-rec-personal-cn

# 2. 编辑偏好档案
cp profile-template.json profile.json
# 用编辑器修改 profile.json，填入你的观影偏好
```

## 配置

### 用户偏好档案（profile.json）

复制模板后按以下说明填写：

```jsonc
{
  "_description": "我的观影偏好档案",
  "updated": "YYYY-MM-DD",

  // 已喜欢的电影——用于 AI 学习你的口味
  // 每部需包含：片名、上映日期、类型、主演、导演、产地、喜欢原因、特征标签
  "liked_movies": [
    {
      "nm": "电影名称",
      "rt": "上映日期",
      "cat": "类型（如：动作,科幻,惊悚）",
      "star": "主演",
      "dir": "导演",
      "src": "制片国家/地区",
      "sc": null,
      "reason": "你为什么喜欢这部电影",
      "traits": ["特征1", "特征2"]
    }
  ],

  // 想看但还没看的电影——用于与新片交叉比对
  // 结构同上，可不填 reason/traits
  "want_to_watch": [
    {
      "nm": "电影名称",
      "rt": "上映日期",
      "cat": "类型",
      "star": "主演"
    }
  ],

  // 核心偏好——定义你的口味骨架
  "core_traits": {
    "genre_affinity": {
      "动作": "你对动作类型的感觉——不是纯打斗，而是动作驱动叙事？还是爆米花爽片？",
      "科幻": "偏好硬科幻/高概念设定，还是软科幻/科幻背景的爱情/剧情？",
      "悬疑/惊悚": "接受度如何？偏好与其他类型混搭还是纯悬疑？",
      "武侠/奇幻": "对强世界观、架空设定有偏好吗？",
      "动画": "是否接受动画电影？偏好什么类型的动画？"
    },
    "ip_affinity": "对 IP 改编（漫画/小说/游戏/翻拍）的偏好程度：极高/中等/无所谓/排斥",
    "style_preferences": [
      "你喜欢的风格类型（高概念、类型混搭、暴力美学等）",
      "多写几条让 AI 更了解你"
    ],
    "weak_signals": [
      "你明确不看的类型（纯爱、文艺、慢节奏、恐怖等）",
      "这些信号会让 AI 降级或排除相应电影"
    ]
  },

  // 推荐规则——定义排序逻辑
  "recommendation_rules": {
    "priority_logic": "用一句话描述优先级：匹配越多核心 trait 排序越高，什么组合是最高优先，什么组合应该降级",
    "boost_keywords": ["关键词1", "关键词2"],
    "downgrade_keywords": ["关键词3", "关键词4"],
    "exclude_keywords": []
  }
}
```

**提示**：`liked_movies` 越多越好（建议 5-10 部），AI 的推荐会越精准。如果刚开始用，可以先填 2-3 部。

### Cron 设置

在 OpenClaw 中创建 cron job，每周一和周五上午推送：

```json
{
  "name": "猫眼电影推荐（周一周五）",
  "schedule": {"kind": "cron", "expr": "40 8 * * 1,5", "tz": "Asia/Shanghai"},
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "timeoutSeconds": 180,
    "lightContext": true,
    "message": "执行猫眼电影周报：先运行 python3 skills/movie-rec-personal-cn/scripts/maoyan_movies.py 采集最新电影数据。然后读取 profile.json（如不存在则使用默认偏好），基于 core_traits 和 recommendation_rules 为每部未看过的电影打分排序。输出结构化周报（🎯 强烈推荐 / 👍 值得关注 / 👀 可观望），推送到飞书。如果 want_to_watch 里有电影撞上正在热映列表，开头醒目提醒。"
  },
  "delivery": {"mode": "announce", "channel": "feishu", "to": "user:your_open_id"}
}
```

**推荐时段**：
- 每周一 08:40（新片首周上映提醒）
- 每周五 08:40（周末观影指南）

## 使用示例

### 手动触发一次推荐

直接在对话中说：

```
帮我做一期猫眼电影周报
```

AI 会：
1. 运行 `python3 scripts/maoyan_movies.py` 采集最新数据
2. 读取 `profile.json` 了解你的偏好
3. 分析匹配，生成推荐周报
4. 推送到飞书

### 查看原始数据

```bash
# 全量 JSON（格式化）
python3 scripts/maoyan_movies.py

# 紧凑 JSON（一行）
python3 scripts/maoyan_movies.py --compact
```

### 更新偏好档案

直接在对话中说：

```
我刚才看了《流浪地球3》，感觉很不错，帮我更新到观影偏好里
```

AI 会更新 `profile.json` 的 `liked_movies` 数组。

## 注意事项

- 脚本请求猫眼 API 时内置 0.3-0.5s 随机延迟，全量抓取约需 30-120 秒（取决于当前上映电影数量）
- 猫眼 API 返回的「想看人数」是用户标记「想看」的累计值，可辅助判断热度
- `profile.json` 的 `liked_movies` 不需要实时同步猫眼评分——重要的是你**为什么喜欢**，不是别人怎么打分
- 如果某部电影详情接口失败，脚本会跳过详情但保留基本信息（片名、类型、上映日期等）

## 文件结构

```
movie-rec-personal-cn/
├── SKILL.md                  # 本文件
├── README.md                 # 详细使用说明（中文）
├── profile-template.json     # 用户偏好档案模板
├── profile.json              # 你的个人偏好档案（从模板复制后填写，不提交到 git）
└── scripts/
    └── maoyan_movies.py      # 猫眼电影数据采集脚本
```
