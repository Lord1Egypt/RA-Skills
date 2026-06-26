---
name: google-search-web
description: "调用 Google 网页搜索接口，获取实时网页搜索结果。使用此技能当用户需要：Google 搜索/网页搜索/搜索引擎查询、调用 /google/search/web 接口、用 Python 脚本执行 Google 搜索、获取搜索结果列表（标题/链接/摘要）。Use this skill for Google web search, search engine queries, fetching search results via API."
argument-hint: "必填：q（搜索关键词）；可选：azt_api_key"
user-invocable: true
---

# Google 网页搜索 Skill

调用接口：
- `POST https://coze-js-api.devtool.uk/google/search/web`

执行随附的 Python 脚本来完成请求，不要在回复中内联构造 curl 命令（除非用户明确要求）。

## 使用场景

以下情况触发本技能：
- 用户想搜索某个关键词并获取网页结果
- 用户需要实时搜索引擎数据
- 用户想批量获取搜索结果（标题、链接、摘要）
- 用户需要调用 Google 搜索 API

## 输入参数

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `q` | **必填** | — | 搜索关键词 |
| `azt_api_key` | 可选 | — | 付费版鉴权 Key；不填则使用免费版（每天限一次） |

## API Key 获取方式

`azt_api_key` 为可选参数，解析顺序如下：

1. 读取环境变量 `AZT_API_KEY`。
2. 用户在参数中直接传入 `--azt_api_key`。
3. 两者均未提供时，使用**免费版**（每天限制一次）。

> 免费版次数已用完或需要更高频率，请前往 **https://devtool.uk/plugin** 购买付费版。

## 执行方式

```bash
# 免费版（每天一次）
python3 scripts/google_search.py --q "Python 教程"

# 付费版（设置环境变量）
export AZT_API_KEY="your_key_here"
python3 scripts/google_search.py --q "AI 最新进展"

# 付费版（直接传参）
python3 scripts/google_search.py --q "OpenAI news" --azt_api_key your_key_here

# 输出原始 JSON
python3 scripts/google_search.py --q "搜索词" --json
```

## 响应处理

1. 显示请求结果状态（`code: 0` 为成功，`code: -1` 为失败）。
2. 列出返回的搜索结果（标题、链接、摘要）。
3. 如果失败，给出可能原因及修正建议。

常见失败原因：
- `azt_api_key` 无效或已过期 → 前往 https://devtool.uk/plugin 重新购买
- `azt_api_key` 积分已用完 → 联系作者续费
- 免费版每日限额已用完 → 等待次日重置或购买付费版
- 网络问题或服务器错误 → 稍后重试

## 输出格式

```markdown
# Google 网页搜索结果

- 接口：POST https://coze-js-api.devtool.uk/google/search/web
- 关键词：<q>
- azt_api_key 来源：<env: AZT_API_KEY | 用户传入 | 免费版>

## 搜索结果

1. **<标题>**
   <链接>
   <摘要>

2. ...

## 状态
<成功/失败信息及剩余积分>
```
