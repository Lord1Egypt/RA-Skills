---
name: huangli-query-cn
license: MIT
homepage: https://nongli.skill.4glz.com
repository: https://github.com/Leocdchina/huangli-agent-skills
publisher: Leocdchina
version: 1.0.1
compatibility: Requires Python 3.9+ or bash with curl. Set required HUANGLI_TOKEN env var (Bearer token from https://nongli.skill.4glz.com/dashboard). Optional HUANGLI_BASE env var overrides API base. Needs HTTPS outbound access to api.nongli.skill.4glz.com.
required_env:
  - HUANGLI_TOKEN (required)
  - HUANGLI_BASE (optional)
outbound_hosts:
  - api.nongli.skill.4glz.com
description: |
  黄历查询工具。按公历日期查询今日黄历、老黄历、每日宜忌、吉神凶煞、神煞、冲煞、吉日凶日。适合查询今天黄历怎么样、今天宜忌、明天适不适合搬家、结婚开业开工选哪天、最近哪些是吉日。支持单日黄历、批量区间查询、多日筛选吉日。
---

# 黄历查询

这是一个专门面向“黄历查询”和“宜忌择日”场景的技能，目标是稳定回答“今天黄历怎么样”“今天宜什么忌什么”“哪天适合搬家、结婚、开业、开工”这类问题。

## 适用问题

当用户提出下面这类问题时使用：

- 今天黄历怎么样？
- 今天宜什么、忌什么？
- 明天适不适合搬家？
- 这周哪天适合结婚？
- 最近哪些日期适合开业、开工？
- 老黄历怎么查？

## 能查到什么

返回数据里通常包含：

- 每日宜忌
- 吉凶判断
- 神煞、冲煞
- 吉日凶日相关字段
- 基础农历信息

这个 skill 的重点是“黄历查询”和“择日判断”，不是单纯的农历日期换算。

## 使用方式

### 1）查询单日黄历

```bash
python3 toolkit.py by-date 2027-08-08
```

### 2）批量筛选适合某项活动的日期

```bash
python3 toolkit.py batch 2027-08-01 2027-08-31 --filter 搬家
```

### 3）按关键词检索特殊日期

```bash
python3 toolkit.py search 甲子日 --year 2027
```

## 触发词建议

高匹配中文搜索表达：

- 黄历查询
- 今日黄历
- 老黄历
- 今日宜忌
- 黄历宜忌
- 搬家吉日
- 结婚吉日
- 开业吉日

## 环境变量

```bash
export HUANGLI_TOKEN="***"
export HUANGLI_BASE="https://api.nongli.skill.4glz.com"
```

Token 获取地址：

- https://nongli.skill.4glz.com/dashboard

## 常见错误

- `401`：Token 无效或过期
- `429`：免费额度已用完，需要到控制台手动重置
- `404`：日期超出可用数据范围
