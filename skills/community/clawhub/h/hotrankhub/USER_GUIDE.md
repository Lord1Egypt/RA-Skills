# HotRank Hub Skill 用户使用指南

## 📖 本指南面向谁？

本指南面向 **ClawHub 平台上的 agent 开发者**，帮助你了解如何在你的 agent 中使用 HotRank Hub Skill 来获取各平台的热榜信息。

---

## 🚀 快速开始

### 第一步：安装 Skill

在 ClawHub 平台上搜索 "HotRank Hub" 并安装到你的 agent 配置中。

### 第二步：在 Agent 中调用

安装完成后，你的 agent 就可以通过自然语言或直接 API 调用的方式获取热榜数据。

---

## 🎯 使用方式

HotRank Hub 提供了 **两种使用方式**，你可以根据需求选择：

### 方式一：自然语言调用（推荐）

这是最简单的方式。安装 Skill 后，用户可以直接用自然语言询问，agent 会自动调用 HotRank Hub 获取数据。

#### 示例对话

**用户**：
```
帮我获取微博热搜前10条
```

**Agent 自动**：
1. 识别用户意图（获取微博热搜）
2. 调用 HotRank Hub Skill
3. 返回格式化的热榜数据

**Agent 回复**：
```
【微博热搜】共获取10条新闻：

1. 某某明星官宣结婚 | 热度: 1500万
   链接: https://weibo.com/...

2. 某某事件持续发酵 | 热度: 1200万
   链接: https://weibo.com/...

3. ...
```

#### 更多示例

```
用户: "今天知乎有什么热门话题？"
Agent: [自动调用 zhihu 热榜并返回]

用户: "GitHub 上有什么热门项目？"
Agent: [自动调用 github-trending 并返回]

用户: "帮我看看抖音和快手的热榜有什么不同"
Agent: [对比两个平台的热榜数据]
```

### 方式二：直接 API 调用

如果你需要更精确的控制，可以直接调用 API 端点。

#### API 基础信息

```
基础 URL: https://airouter.tech/api
请求方式: GET
响应格式: JSON
```

#### 获取单个平台热榜

```bash
# 获取微博热搜
curl https://airouter.tech/api/weibo

# 获取知乎热榜
curl https://airouter.tech/api/zhihu

# 获取抖音热点
curl https://airouter.tech/api/douyin
```

#### 响应格式

```json
{
  "code": 200,
  "msg": "请求成功",
  "data": [
    {
      "id": "1",
      "title": "热搜标题",
      "desc": "热搜描述",
      "hot": 1500000,
      "url": "https://weibo.com/...",
      "mobileUrl": "https://m.weibo.com/..."
    }
  ],
  "timestamp": 1709500000000
}
```

---

## 📋 支持的平台列表

HotRank Hub 支持 **47 个平台**，完整列表如下：

### 社交媒体（7个）
| 平台 ID | 平台名称 | 调用示例 |
|---------|---------|---------|
| `weibo` | 微博热搜 | `获取微博热搜` |
| `zhihu` | 知乎热榜 | `知乎有什么热门话题` |
| `zhihu-daily` | 知乎日报 | `知乎日报精选` |
| `baidu` | 百度热搜 | `百度热搜榜` |
| `baidutieba` | 百度贴吧 | `贴吧热议话题` |
| `xiaohongshu` | 小红书 | `小红书热门笔记` |
| `quark` | 夸克热搜 | `夸克搜索热点` |

### 短视频/视频（4个）
| 平台 ID | 平台名称 | 调用示例 |
|---------|---------|---------|
| `douyin` | 抖音热点 | `抖音热点内容` |
| `kuaishou` | 快手热榜 | `快手热榜` |
| `bilibili` | B站热门 | `B站热门视频` |
| `qqvideo` | 腾讯视频 | `腾讯视频热门` |

### 科技资讯（16个）
| 平台 ID | 平台名称 | 调用示例 |
|---------|---------|---------|
| `github` | GitHub | `GitHub今日热榜` |
| `github-trending` | GitHub趋势 | `GitHub热门项目` |
| `hello-github` | HelloGitHub | `GitHub有趣项目` |
| `juejin` | 掘金 | `掘金热门文章` |
| `csdn` | CSDN | `CSDN技术博客` |
| `v2ex` | V2EX | `V2EX热门话题` |
| `linuxdo` | Linux.do | `Linux社区讨论` |
| `hackernews` | Hacker News | `黑客新闻资讯` |
| `ithome` | IT之家 | `IT之家新闻` |
| `36kr` | 36氪 | `36氪科技资讯` |
| `huxiu` | 虎嗅 | `虎嗅商业资讯` |
| `sspai` | 少数派 | `少数派应用推荐` |
| `ifanr` | 爱范儿 | `爱范儿科技生活` |
| `coolapk` | 酷安 | `酷安数码社区` |
| `freebuf` | FreeBuf | `网络安全资讯` |

### 财经新闻（4个）
| 平台 ID | 平台名称 | 调用示例 |
|---------|---------|---------|
| `xueqiu` | 雪球 | `雪球热帖` |
| `wallstreetcn` | 华尔街见闻 | `华尔街见闻财经资讯` |
| `jin10` | 金十数据 | `金十数据财经快讯` |
| `cls` | 财联社 | `财联社财经电报` |

### 游戏娱乐（6个）
| 平台 ID | 平台名称 | 调用示例 |
|---------|---------|---------|
| `steam` | Steam | `Steam热销游戏` |
| `hupu` | 虎扑 | `虎扑体育热帖` |
| `douban-movic` | 豆瓣电影 | `豆瓣热门电影` |
| `lol` | 英雄联盟 | `英雄联盟资讯` |
| `netease-music` | 网易云音乐 | `网易云音乐热歌榜` |
| `qq` | QQ音乐 | `QQ音乐热歌榜` |

### 新闻资讯（4个）
| 平台 ID | 平台名称 | 调用示例 |
|---------|---------|---------|
| `toutiao` | 今日头条 | `今日头条热榜` |
| `netease` | 网易新闻 | `网易热点新闻` |
| `thepaper` | 澎湃新闻 | `澎湃新闻时事热点` |
| `cankaoxiaoxi` | 参考消息 | `参考消息国际新闻` |

### 生活方式（4个）
| 平台 ID | 平台名称 | 调用示例 |
|---------|---------|---------|
| `weread` | 微信读书 | `微信读书热榜` |
| `smzdm` | 什么值得买 | `什么值得买好物推荐` |
| `dongchedi` | 懂车帝 | `懂车帝汽车资讯` |
| `history-today` | 历史上的今天 | `历史上的今天` |

### 社区论坛（2个）
| 平台 ID | 平台名称 | 调用示例 |
|---------|---------|---------|
| `woshipm` | 人人都是产品经理 | `产品经理热门话题` |

---

## 💡 实际使用场景

### 场景 1：日常热点查询

**用户**：
```
今天有什么热点新闻？
```

**Agent**：
```
我帮你查看了今天的多个平台热榜：

【微博热搜 TOP 3】
1. 某某事件 - 热度 2000万
2. 某某新闻 - 热度 1500万
3. 某某话题 - 热度 1200万

【知乎热榜 TOP 3】
1. 如何看待某某事件？
2. 某某领域的最新进展
3. 有哪些值得关注的新技术？

【今日头条 TOP 3】
...

需要我详细介绍某个热点吗？
```

### 场景 2：跨平台对比分析

**用户**：
```
帮我对比微博和知乎的热榜有什么不同
```

**Agent**：
```
【微博 vs 知乎 热榜对比】

共同热点（2个）：
1. "某某事件" - 两个平台都在热榜前三
2. "某某话题" - 微博第5，知乎第7

微博独有热点：
- 某某明星相关（娱乐属性强）
- 某某综艺节目

知乎独有热点：
- 某某技术讨论（知识属性强）
- 某某行业分析

总结：微博偏娱乐八卦，知乎偏知识讨论
```

### 场景 3：特定领域监控

**用户**：
```
帮我关注科技圈的最新动态
```

**Agent**：
```
【科技圈最新动态】

GitHub 趋势：
1. 新兴项目：某某框架 - 3000+ stars
2. 热门语言：Rust 项目增多

IT之家：
- 某某公司发布新产品
- 某某技术迎来重大更新

36氪：
- 某某领域融资动态
- 科技行业最新趋势

V2EX：
- 关于某某技术的讨论热烈
```

### 场景 4：生成热点报告

**用户**：
```
帮我生成今天的财经热点报告
```

**Agent**：
```
【今日财经热点报告】

一、市场动态
（数据来源：雪球、华尔街见闻、金十数据）
- A股今日走势...
- 美股最新行情...

二、政策解读
（来源：财联社）
- 央行最新政策...
- 监管动态...

三、投资热点
（来源：雪球热帖）
- 某某板块受关注
- 某某股票讨论热烈

四、专家观点
（来源：华尔街见闻）
- ...
```

---

## 🔧 高级用法

### 1. 批量获取多个平台

**自然语言方式**：
```
帮我获取微博、知乎、抖音三个平台的热榜
```

**API 方式**：
```javascript
const platforms = ['weibo', 'zhihu', 'douyin'];
const results = await Promise.all(
  platforms.map(p =>
    fetch(`https://airouter.tech/api/${p}`).then(r => r.json())
  )
);
```

### 2. 定时监控热点

在你的 agent 中设置定时任务：

```javascript
// 每小时监控一次
setInterval(async () => {
  const weibo = await fetch('https://airouter.tech/api/weibo');
  const data = await weibo.json();

  // 检测新的热点
  if (hasNewHotTopic(data)) {
    notifyUser('发现新的微博热点！');
  }
}, 3600000);
```

### 3. 关键词追踪

**用户**：
```
帮我追踪"AI"相关的热点话题
```

**Agent**：
```
在以下平台找到"AI"相关热点：

微博热搜：
- 第3位：某某AI产品发布

知乎热榜：
- 第5位：AI技术的发展趋势

GitHub趋势：
- 多个AI项目进入热榜

36氪：
- AI创业公司融资新闻
```

---

## ⚡ 最佳实践

### 1. 缓存策略

数据每 5 分钟更新一次，建议在 agent 中实现本地缓存：

```javascript
const cache = new Map();
const CACHE_TIME = 5 * 60 * 1000;

async function getHotList(source) {
  if (cache.has(source)) {
    const { data, time } = cache.get(source);
    if (Date.now() - time < CACHE_TIME) {
      return data;
    }
  }

  const response = await fetch(`https://airouter.tech/api/${source}`);
  const data = await response.json();

  cache.set(source, { data, time: Date.now() });
  return data;
}
```

### 2. 错误处理

```javascript
try {
  const response = await fetch('https://airouter.tech/api/weibo');
  if (!response.ok) {
    throw new Error('API 请求失败');
  }
  const data = await response.json();
  // 处理数据
} catch (error) {
  console.error('获取热榜失败:', error);
  // 返回友好的错误提示
}
```

### 3. 并发控制

避免同时请求过多平台：

```javascript
async function fetchBatch(platforms, batchSize = 5) {
  const results = [];
  for (let i = 0; i < platforms.length; i += batchSize) {
    const batch = platforms.slice(i, i + batchSize);
    const batchResults = await Promise.all(
      batch.map(p => fetch(`https://airouter.tech/api/${p}`))
    );
    results.push(...batchResults);
  }
  return results;
}
```

---

## 🚫 使用限制

### 速率限制
- 建议：每分钟不超过 60 次请求
- 数据更新：每 5 分钟一次

### 数据使用
- 仅供个人学习和研究使用
- 请勿用于商业用途（未经授权）
- 请遵守各平台的 ToS

---

## ❓ 常见问题

### Q1: 安装 Skill 后，agent 如何知道何时调用？

**A:** ClawHub 平台会根据用户的自然语言输入，自动识别意图并调用相应的 Skill。例如用户说"微博热搜"，平台会识别为需要调用 HotRank Hub 的 weibo 数据源。

### Q2: 可以同时获取多个平台的数据吗？

**A:** 可以！你可以说"帮我获取微博、知乎、抖音的热榜"，agent 会并发调用多个 API 并整合结果。

### Q3: 数据的时效性如何？

**A:** 所有数据每 5 分钟更新一次，确保获取的是最新的热榜信息。

### Q4: 支持历史数据查询吗？

**A:** 目前不支持历史数据，仅提供实时热榜数据。

### Q5: 如何知道某个平台是否支持？

**A:** 参考"支持的平台列表"章节，或直接询问 agent："支持哪些平台？"。

---

## 📞 技术支持

如有问题，请访问：
- **官网**：https://airouter.tech
- **API 文档**：https://airouter.tech/docs/api
- **使用示例**：https://airouter.tech/docs/examples

---

**祝你使用愉快！🎉**