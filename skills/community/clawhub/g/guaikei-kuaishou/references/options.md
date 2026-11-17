# 快手数据助手 

## 🔎 快手关键词搜索

| 参数         | 缩写 | 作用       | 可选值                                                 | 必填 | 默认值 |
| :----------- | :--: | :--------- | :----------------------------------------------------- | :--- | :----: |
| `--keyword`  | `-K` | 搜索关键词 | 2-50 位长度的汉字或单词                                | 是   |        |
| `--sort`     | `-S` | 排序方式   | 0 = 综合排序 / 1 = 最新发布 / 2 = 最多点赞             | 否   |   0    |
| `--time`     | `-T` | 时间范围   | 0 = 全部 / 1 = 近1日 / 7 = 近一周 / 30 = 近一月        | 否   |   0    |
| `--duration` | `-D` | 视频时长   | 0 = 不限 / 1 = 1分钟以内 / 2 = 1-5分钟 / 3 = 5分钟以上 | 否   |   0    |
| `--limit`    | `-L` | 获取数量   | 1-10000 条                                             | 否   |   10   |

```bash
# **基础语法**
node scripts/kuaishou/search-cli.js --keyword <关键词> --sort <排序方式> --time <时间范围> --duration <视频时长> --limit <获取数量>

# **使用示例**

# 搜索"AI 教程"的快手内容
node scripts/kuaishou/search-cli.js --keyword "AI 教程"

# 搜索 AI 获取最多点赞的快手内容
node scripts/kuaishou/search-cli.js --keyword "AI" --sort 2

# 搜索近7天"AI 模型"的快手内容
node scripts/kuaishou/search-cli.js --keyword "AI 模型" --time 7

# 搜索"AI 教程"视频时长在5分钟以上的快手内容
node scripts/kuaishou/search-cli.js --keyword "AI 教程" --duration 3

# 搜索一月内最新20条"AI 教程"的快手内容
node scripts/kuaishou/search-cli.js --keyword "AI 教程" --sort 1 --time 30 --limit 20
```

## 🦸 快手博主作品获取

| 参数      | 缩写 | 作用                     | 可选值                    | 必填 | 默认值 |
| :-------- | :--: | :----------------------- | :------------------------ | :--- | :----: |
| `--url`   | `-U` | 快手博主主页URL或user_id |                           | 是   |        |
| `--sort`  | `-S` | 排序方式                 | 0 = 最新 / 1 = 最热(默认) | 否   |   1    |
| `--limit` | `-L` | 获取作品数量             | 0-10000 条                | 否   |   10   |

> **💡"快手博主主页URL"说明**
>
> - PC端 ( 格式：<https://www.kuaishou.com/profile/3xxx> )
> - 移动端 ( 格式：<https://v.kuaishou.com/xxx> )
> - 技能关键词搜索返回的user_id字段

```bash
# **基础语法**
node scripts/kuaishou/post-cli.js --url "https://www.kuaishou.com/profile/3xxx"

# **使用示例**

# 获取快手博主 3xxx 已发布的20条热门作品
node scripts/kuaishou/post-cli.js --url "https://www.kuaishou.com/profile/3xxx" --limit 20
```

## 💬 快手作品评论数据

| 参数      | 缩写 | 作用            | 可选值     | 必填 | 默认值 |
| :-------- | :--: | :-------------- | :--------- | :--- | :----: |
| `--url`   | `-u` | 快手视频URL或id |            | 是   |        |
| `--limit` | `-l` | 获取评论数量    | 1-10000 条 | 否   |   10   |

```bash
# **基础语法**
node scripts/kuaishou/comment-cli.js --url "https://www.kuaishou.com/short-video/xxx"

# **使用示例**

# 获取视频 xxx 的100条评论
node scripts/kuaishou/comment-cli.js --url "3xxx" --limit 100
```
