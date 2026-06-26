# ry-data.py 命令参数速查表

所有命令格式：`python3 {baseDir}/scripts/ry-data.py <command> [action] [options]`

全局说明：
- 所有列表命令支持 `--json` 输出原始 JSON
- 分页参数：`--page`（页码，从1开始）、`--page-size`（每页条数，默认20，最大100）
- 排序参数：`--sort-by`（排序字段）、`--sort-order`（asc/desc）

---

## check

检查 API 连接状态。

```bash
python3 ry-data.py check
```

无参数。输出配置信息、API 地址、连接状态。

---

## accounts

账号搜索与查询。

```bash
python3 ry-data.py accounts <action> [options]
```

| action | 说明 | 必填参数 | 可选参数 |
|--------|------|---------|---------|
| `search` | 多维筛选账号 | — | 见下方筛选参数 |
| `get` | 查看账号详情 | `--sec-uid` | `--json` |

### search 筛选参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--keyword` | 搜索昵称/简介 | `--keyword "荣耀"` |
| `--follower-min` | 最低粉丝数 | `--follower-min 1000` |
| `--follower-max` | 最高粉丝数 | `--follower-max 100000` |
| `--brand-tags` | 品牌标签，逗号分隔 | `--brand-tags "荣耀,华为"` |
| `--content-tags` | 内容标签，逗号分隔 | `--content-tags "拍摄,电池"` |
| `--user-type` | 账号类型，逗号分隔 | `--user-type "1,2"` (1=个人,2=黄V,3=蓝V) |
| `--exclude-star` | 排除明星账号 | `--exclude-star` |
| `--exclude-shop` | 排除带货账号 | `--exclude-shop` |
| `--sort-by` | 排序字段 | `follower_count`(默认), `total_favorited`, `aweme_count` |

可用品牌标签：荣耀, 华为, 小米, OPPO, vivo, 苹果, 三星

可用内容标签：拍摄, 电池, 屏幕, AI, 外观, 性能, 游戏, 评测, 开箱, 折叠屏, 性价比

---

## videos

视频搜索与趋势查询。

```bash
python3 ry-data.py videos <action> [options]
```

| action | 说明 | 必填参数 | 可选参数 |
|--------|------|---------|---------|
| `search` | 搜索视频 | — | 见下方参数 |
| `trend` | 视频互动趋势 | `--aweme-id` | `--days`(默认7) |

### search 参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--keyword` | 搜索视频标题/描述 | `--keyword "拍照"` |
| `--sec-uids` | 作者 sec_uid，逗号分隔 | `--sec-uids "uid1,uid2"` |
| `--interaction-min` | 最低互动量 | `--interaction-min 1000` |
| `--interaction-max` | 最高互动量 | `--interaction-max 10000` |
| `--publish-start` | 发布起始时间 (Unix timestamp) | `--publish-start 1708300800` |
| `--publish-end` | 发布结束时间 (Unix timestamp) | `--publish-end 1711000000` |
| `--sort-by` | 排序字段 | `interaction_count`(默认), `play_count`, `digg_count`, `create_time` |

---

## keywords

关键词搜索与管理。

```bash
python3 ry-data.py keywords <action> [options]
```

| action | 说明 | 必填参数 | 可选参数 |
|--------|------|---------|---------|
| `search` | 搜索关键词 | — | `--keyword`, `--brand`, `--category` |
| `add` | 添加监控关键词 | `--word` | `--json` |
| `delete` | 删除关键词 | `--word` | — |

### search 参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--keyword` | 模糊搜索关键词 | `--keyword "荣耀"` |
| `--brand` | 品牌筛选 | `--brand "荣耀"` |
| `--category` | 分类筛选 | `--category "手机"` |
| `--sort-by` | 排序字段 | `mounth_search_index`(默认), `competition`, `video_count` |

---

## keyword-videos

关键词搜索排名视频。

```bash
python3 ry-data.py keyword-videos search [options]
```

| 参数 | 说明 | 示例 |
|------|------|------|
| `--keyword` | 关键词（精确匹配） | `--keyword "荣耀Magic7"` |
| `--search-date` | 搜索日期 | `--search-date "2026-03-24"` |
| `--sort-by` | 排序字段 | `rank`(默认) |

---

## hot-videos

热榜视频查询。

```bash
python3 ry-data.py hot-videos <action> [options]
```

| action | 说明 | 必填参数 | 可选参数 |
|--------|------|---------|---------|
| `search` | 搜索热榜视频 | — | 见下方参数 |
| `categories` | 查看所有分类 | — | `--json` |

### search 参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--category` | 分类名称 | `--category "科技"` |
| `--snapshot-date` | 日期 | `--snapshot-date "2026-03-24"` |
| `--keyword` | 搜索视频标题 | `--keyword "手机"` |
| `--sort-by` | 排序字段 | `score`(默认), `play_cnt`, `like_cnt`, `follow_rate` |

可用分类（38个）：剧情, 明星, 综艺, 电影, 电视剧, 音乐, 二次元, 游戏, 公益, 随拍, 舞蹈, 动物, 三农, 科技, 财经, 母婴, 亲子, 生活家居, 法律, 医疗健康, 科普, 情感, 文化, 职场, 教育校园, 摄影摄像, 美食, 旅行, 时尚, 艺术, 体育, 休闲娱乐, 汽车, 生活记录, 人文社科, 颜值, 特效&小游戏, AI原生影像

---

## hashtags

话题标签搜索与热门趋势。

```bash
python3 ry-data.py hashtags <action> [options]
```

| action | 说明 | 必填参数 | 可选参数 |
|--------|------|---------|---------|
| `search` | 搜索话题标签 | — | `--keyword`, `--is-trending` |
| `trending` | 热门话题趋势 | — | `--days`(默认7), `--size`(默认50) |

### search 参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--keyword` | 搜索话题 | `--keyword "手机"` |
| `--is-trending` | 仅热门话题 | `--is-trending` |
| `--sort-by` | 排序字段 | `video_count`(默认), `total_interaction` |

### trending 参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--days` | 天数范围 | `--days 7` |
| `--size` | 返回数量 | `--size 100` |
