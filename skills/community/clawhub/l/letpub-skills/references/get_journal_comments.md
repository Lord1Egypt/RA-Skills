---
description: 获取期刊评论 - 获取LetPub期刊的用户投稿评论和经验分享
---

# 获取期刊评论

## 功能说明
获取 LetPub 期刊的用户投稿评论，包括审稿速度、录用比例、投稿经验等。需要登录后才能获取完整评论数据。

## 使用方法

```python
from letpub_skills import get_journal_comments, parse_comment, parse_comments_response

# 获取期刊评论（返回原始API响应）
response = get_journal_comments(journal_id=1642, page=1, sorttype="undefined")

# 解析评论响应
comments = parse_comments_response(response)
for comment in comments:
    print(comment['floor'])           # 楼层号
    print(comment['author'])          # 作者昵称
    print(comment['score'])           # 期刊评分
    print(comment['experience'])      # 投稿经验
    print(comment['replies'])         # 其他用户回复

# 也可以单独解析单条评论HTML
html_content = "<div class='comment'>...</div>"
comment = parse_comment(html_content)
```

## Cookies 配置

获取评论需要登录 LetPub 账号。请在 `letpub_skills/assets/cookies.json` 中配置 cookies：

```json
{
  "cookies": "PHPSESSID=xxxxx; letpub_user_id=xxxxx; ..."
}
```

从浏览器开发者工具中复制 cookies 字符串粘贴到 `cookies` 字段中。

## 函数说明

### get_journal_comments(journal_id, page=1, sorttype="undefined", cookies=None)
- `journal_id`: 期刊ID（从详情页获取）
- `page`: 评论页码，默认为 1
- `sorttype`: 排序方式，默认为 "undefined"
- `cookies`: cookies 字符串，如果为 None 则从 assets/cookies.json 读取
- 返回: API响应的JSON数据，包含 `count`（总记录数）、`pages`（总页数）、`data`（评论列表）

### parse_comments_response(response_data)
- `response_data`: API响应字典
- 返回: 解析后的评论列表

### parse_comment(html_content)
- `html_content`: 单条评论的HTML内容
- 返回: 解析后的评论字典

## 评论字段

| 字段 | 说明 |
|------|------|
| floor | 楼层号（如 #216楼） |
| author | 作者昵称 |
| author_id | 作者ID |
| score | 期刊评分（0-10分） |
| research_fields | 研究方向数组 |
| submission_result | 投稿结果 |
| submission_cycle | 投稿周期 |
| publish_time | 发表时间 |
| update_time | 最后更新时间 |
| experience | 投稿经验 |
| replies | 其他用户回复数组 |
| good_count | 点赞数 |
| bad_count | 踩数 |

## 回复字段（replies数组中）

| 字段 | 说明 |
|------|------|
| author | 回复作者昵称 |
| author_id | 回复作者ID |
| publish_time | 回复发表时间 |
| content | 回复内容 |
| good_count | 回复点赞数 |

## 分页说明

API 返回的分页信息：
- `count`: 总记录数
- `pages`: 总页数
- `data`: 当前页的评论数据列表

建议至少遍历5页获取评论内容分析。
