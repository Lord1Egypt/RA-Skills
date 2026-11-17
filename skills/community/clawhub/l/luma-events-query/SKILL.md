---
name: luma-events-query
description: 查 lu.ma / Luma 公开活动，方式与 Luma App 搜索框相同（关键词 Hangzhou/杭州/重庆，不限城市目录）。用户说查活动、Luma、meetup、某城最近有什么活动时使用。用户没指定主题时只搜城市，不要默认加 AI。不要用来查大麦/秀动/猫眼。不要向用户索要 Parse/pmx_ API Key。
version: 1.0.1
license: MIT-0
metadata:
  openclaw:
    emoji: "📅"
    homepage: https://github.com/diaoxiaoniu/luma-events-query
    requires:
      bins:
        - python3
---

# Luma 活动查询

跟 **Luma App 搜索框**一样：打城市名或关键词。不要再用 Parse 的 87 城 slug（那份没有杭州）。

不需要任何 API Key。直接调 Luma 公开 JSON：

`GET https://api.lu.ma/discover/get-paginated-events?pagination_limit=20&query=Hangzhou`

## 何时用

- 查 lu.ma 公开活动，包括**中国大陆**（杭州、重庆、上海、北京、深圳、成都、广州）
- 用户说 Hangzhou / 杭州 / 某城最近有什么活动
- 只有用户明确说了主题（AI、音乐、摄影、创业）才加 `--topic`

**不要用**：大麦、秀动、猫眼。

## 命令

优先跑本技能目录里的脚本（`<skill_dir>` = 本 `SKILL.md` 所在目录）：

用户没说主题时，不要加 `--topic`：

```bash
python3 "<skill_dir>/scripts/luma-events.py" search 杭州 --limit 10
python3 "<skill_dir>/scripts/luma-events.py" search Hangzhou --limit 10
python3 "<skill_dir>/scripts/luma-events.py" search 重庆 --limit 10
```

只有用户点名主题才加，例如「东京的 AI 活动」：

```bash
python3 "<skill_dir>/scripts/luma-events.py" search 东京 --topic AI --limit 10
```

没有 Python 时用 curl（中英文各搜一遍，合并去重）：

```bash
curl -sS "https://api.lu.ma/discover/get-paginated-events?pagination_limit=20&query=Hangzhou"
curl -sS "https://api.lu.ma/discover/get-paginated-events?pagination_limit=20&query=%E6%9D%AD%E5%B7%9E"
```

脚本会用中英关键词各搜一遍，再过滤标题/城市字段里真正带该城的结果。不要只传经纬度，不要用 `city=hangzhou` 那种 Parse slug。不要向用户要 `pmx_` / parse.bot 账号。

## 给别人用 / 发布

本 skill 查的是 Luma 公开页，**接收者不需要申请 API**。

- 禁止附带 `PARSE_API_KEY`、`parse.env`、`pmx_` 字符串
- 禁止写作者本机绝对路径
- 发布前清掉简介和记忆里的密钥、内网地址

## 对用户怎么说

中文、短。每条：标题、时间（标活动 timezone）、城市/场地、主办、`https://lu.ma/...`。
`location_mismatch: true` 表示关键词没命中该城，先说明再列。地点 `报名后可见` 是 Luma 对未报名隐藏地址。不要贴 JSON。
用户没指定主题时，如实列出该城所有匹配场次（音乐会、车活动、社区日都要），不要只挑 AI。
