# 快手用户需求洞察与产品机会分析 完整选项参数说明

命令在技能目录下执行。stdout 是一份 JSON 信封，字段见 `assets/*.schema.json`。非法枚举和越界数量会直接失败，不会改成默认值。

短参数大小写都可以，下面用小写。

## 🔎 关键词搜索

| 参数 | 缩写 | 作用 | 可选值 | 必填 | 默认值 |
| --- | --- | --- | --- | --- | --- |
| `--keyword` | `-k` | 搜索关键词 | 1-50 个字符，不能是链接，不含 `< > " '` | 是 | |
| `--sort` | `-s` | 排序方式 | 0 综合 / 1 最新发布 / 2 最多点赞 | 否 | 0 |
| `--time` | `-t` | 时间范围 | 0 不限 / 1 近 1 日 / 7 近 7 日 / 30 近 1 月 | 否 | 0 |
| `--duration` | `-d` | 视频时长 | 0 不限 / 1 1 分钟内 / 2 1-5 分钟 / 3 超过 5 分钟 | 否 | 0 |
| `--limit` | `-l` | 获取数量 | 1-10000（**包月 Token 实际最多 30**） | 否 | 10 |

```bash
node scripts/kuaishou/search-cli.js --keyword "AI 教程"
node scripts/kuaishou/search-cli.js --keyword "AI" --sort 2
node scripts/kuaishou/search-cli.js --keyword "AI 模型" --sort 1 --time 7 --limit 20
```

> **套餐双上限**：技能硬上限 10000（按量）。包月 Token 超限返回 `PLAN_LIMIT`：搜索 ≤30，作品 ≤50，评论 ≤60。

## 🦸 博主作品

| 参数 | 缩写 | 作用 | 可选值 | 必填 | 默认值 |
| --- | --- | --- | --- | --- | --- |
| `--url` | `-u` | 主页链接或数字 user_id | 最长 255 | 是 | |
| `--sort` | `-s` | 排序方式 | 0 最新 / 1 最热 | 否 | 1 |
| `--limit` | `-l` | 获取作品数量 | 0-10000（**包月最多 50**；0 只要博主信息和互动数据） | 否 | 10 |

接受：

- `https://www.kuaishou.com/profile/3x...`
- 搜索结果里的 `user.user_id`（纯数字）或 `user.url`

不接受裸的 `3x` 视频 id，也不接受 `v.kuaishou.com`。这里的 `--sort 0` 才是最新，和搜索命令不同。

```bash
node scripts/kuaishou/post-cli.js --url "https://www.kuaishou.com/profile/3xabc" --sort 0 --limit 20
node scripts/kuaishou/post-cli.js --url 123456 --limit 0
```

## 💬 作品评论

| 参数 | 缩写 | 作用 | 可选值 | 必填 | 默认值 |
| --- | --- | --- | --- | --- | --- |
| `--url` | `-u` | 视频链接或视频 id | 最长 255 | 是 | |
| `--limit` | `-l` | 获取评论数量 | 1-10000（**包月最多 60**） | 否 | 10 |

接受：

- `https://www.kuaishou.com/short-video/3x...`
- `https://v.kuaishou.com/...`
- `3x` 开头的视频 id

不接受博主主页和纯数字 user_id。

```bash
node scripts/kuaishou/comment-cli.js --url "https://www.kuaishou.com/short-video/3xabc" --limit 40
node scripts/kuaishou/comment-cli.js --url 3xabc --limit 40
```
