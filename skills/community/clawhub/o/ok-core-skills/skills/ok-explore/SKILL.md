---
name: ok-explore
description: |
  OK.com 首页推荐与帖子详情。获取首页 feed 流、查看单条帖子完整详情。
  搜索帖子和浏览分类请使用 ok-search 技能。
---

# ok-explore — 首页推荐与帖子详情

获取 OK.com 首页推荐 feed 和单条帖子的完整详情。

> 搜索帖子、浏览分类、价格筛选等操作请使用 **ok-search** 技能。

## 执行约束

`<SKILL_DIR>` 是本 SKILL.md 的**上两级目录**（即包含 `pyproject.toml` 的项目根目录）。

## 命令

```bash
# 获取首页推荐（必须传 --country 和 --city，默认 singapore）
uv run --project <SKILL_DIR> ok-cli list-feeds --country singapore --city singapore
uv run --project <SKILL_DIR> ok-cli list-feeds --country usa --city hawaii --max-results 10

# 获取帖子详情（传入帖子 URL）
uv run --project <SKILL_DIR> ok-cli get-listing --url "https://us.ok.com/en/city-hawaii/cate-property/slug/"
```

## 参数说明

- `--country`: 国家（默认 `singapore`，其他地区必须显式传入）
- `--city`: 城市 code（默认 `singapore`，其他地区必须显式传入）
- `--lang`: 语言（默认 `en`）
- `--max-results`: 最大结果数（默认 20，仅 `list-feeds`）
- `--url`: 帖子 URL（仅 `get-listing`）

## 详情展示

`get-listing` 返回的 JSON 包含以下字段，结构化展示给用户：

标题、价格、描述（前 200 字）、卖家名称、发布时间、图片链接、分类面包屑。
