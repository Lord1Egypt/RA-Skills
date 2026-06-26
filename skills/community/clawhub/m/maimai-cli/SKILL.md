---
name: maimai-cli
description: >
  脉脉 CLI 路由技能。用于导入登录态、查看推荐流/热榜/公司圈、搜索内容、
  读取详情评论、下载图片和排查登录问题。Use when: maimai, 脉脉, 职言,
  同事圈, 推荐流, 热榜, 帖子详情, 评论, Cookie.
version: 1.1.0
license: MIT-0
metadata:
  openclaw:
    requires:
      bins:
        - maimai
    homepage: https://github.com/mariotong/maimai-cli
    emoji: "💬"
---

# maimai-cli

`maimai-cli` 是脉脉的本机命令行入口。主文档只保留路由和总规则；具体命令、场景和排错细节请按需阅读 `references/*.md`。

## 何时使用

当用户提到这些意图时，优先使用本 skill：
- 脉脉登录、Cookie 导入、状态检查
- 推荐流、热榜、公司圈、帖子列表、翻页
- 搜索脉脉话题、联系人、公司讨论
- 帖子详情、评论、图片、资料卡
- 脉脉 CLI 的短索引解析、输出格式、故障排查

## 快速开始

```bash
maimai --help
maimai status
maimai me
maimai feed --limit 5
```

## 路由表

| 用户意图 | 参考文档 |
| --- | --- |
| 登录、Cookie、安全边界 | `references/auth.md` |
| 推荐流、热榜、公司圈、列表翻页 | `references/feeds.md` |
| 搜索内容与联系人 | `references/search.md` |
| 详情、评论、图片、资料卡、短索引 | `references/detail.md` |
| 常见异常、调试、工作流 | `references/troubleshooting.md` |

## 最常用命令

```bash
# 登录与状态
maimai import-cookie-header
maimai status
maimai me
maimai cookies
maimai logout

# 列表
maimai feed --limit 10
maimai hot-rank
maimai company-feed --limit 10
maimai search 裁员 --section gossips

# 展开阅读
maimai refs
maimai detail 1 --kind gossip
maimai comments 1 --kind gossip
maimai images 1 --download ./images
maimai profile 1
maimai refs --scope comments
```

## 使用原则

1. 先验证 `maimai` 命令存在，再确认 `maimai status` 是否正常。
2. 列表读取优先从小结果集开始，例如 `feed --limit 5`。
3. 遇到 `1`、`2` 这类短索引时，先确认最近一次列表上下文是否还在；帖子看 `maimai refs`，评论看 `maimai refs --scope comments`。
4. 默认给用户摘要，不直接倾倒整屏原始输出；需要脚本消费时再加 `--json` 或 `--yaml`。
5. 如果用户把完整 Cookie 贴进对话，先提醒其让旧登录态失效，再继续其他操作。
