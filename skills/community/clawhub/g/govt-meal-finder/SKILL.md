---
name: govt-meal-finder
display_name: "银发助餐点查询"
description: 查询附近政府认证养老助餐点（北京、广州、深圳），数据来自政府公开名录，按距离排序，附电话和使用提醒。
metadata:
  version: 1.0.0
  agent:
    type: tool
    runtime: python
    context_isolation: execution
    parent_context_access: read-only
  openclaw:
    emoji: "🍱"
    priority: 80
    requires:
      bins:
        - python3
    intents:
      - senior_meal_search
      - govt_certified_restaurant
      - elderly_dining
    patterns:
      - "(老人|老年|长者|养老).*(吃饭|用餐|助餐|饭堂|食堂)"
      - "(附近|周边|哪里).*(助餐|政府.*餐|养老.*饭)"
      - "助餐点.*在哪"
      - "老人.*补贴.*餐"
---

# 银发助餐点查询

查询附近政府认证养老助餐点，适合老人或子女代为查找。数据来源于北京、广州、深圳三城政府公开名录，实时从商家库查询，按直线距离排序。

## 用法

```bash
# 环境变量（必须，不能写入任何文件）
export GAODE_POI_KEY="xl_xxx"

# 查询附近 1 公里内（默认）
python3 govt_meal_skill.py --city 北京 --place 天安门

# 查询附近 500 米内，返回前 3 条
python3 govt_meal_skill.py --city 广州 --place 北京路步行街 --radius 500 --top 3

# 深圳，2 公里半径
python3 govt_meal_skill.py --city 深圳 --place 华强北 --radius 2000
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--city` | 是 | 城市：北京 / 广州 / 深圳 |
| `--place` | 是 | 参考地点，如 天安门、回龙观地铁站、华强北 |
| `--radius` | 否 | 查询半径（米），默认 1000 |
| `--top` | 否 | 返回条数，默认 5，最多 20 |
| `--json` | 否 | 输出原始 JSON（调试用）|

## 输出示例

```markdown
# 北京 · 天安门广场 附近 1000m 内政府认证助餐点

共找到 3 处（按直线距离排序）

## 1. 东城区建国门街道养老助餐点
- 所属区：东城区
- 地址：北京市东城区建国门内大街xx号
- 直线距离：约 320m
- 电话：010-xxxxxxxx

---
⚠️ 使用提醒
- 距离为直线距离，实际步行路程可能更远
- 开放时间、剩余名额请致电确认，部分节假日停餐
- 部分助餐点仅限本街道户籍老人，请现场核实资格
```

## 覆盖范围与已知限制

| 城市 | 数据量 | 来源 |
|------|--------|------|
| 北京 | 约 2,127 条（含坐标） | 北京市民政局养老助餐点名录 |
| 广州 | 约 1,394 条 | 政府公开名录 |
| 深圳 | 约 732 条 | 政府公开名录 |

- 不支持以上三城之外的城市（会明确告知）
- 无法查询「近期新开」的助餐点（名录入库有延迟）
- 约 1,141 条北京名录无坐标，不会出现在距离查询结果里
- 深圳部分店名含特殊字符，已在输出时自动清洗

## 安全规则

`GAODE_POI_KEY` 必须通过环境变量传入，禁止写入任何文件（含 memory、config、脚本硬编码）。

## 获取 key

请联系服务运营方申请专属 key：微信 **15600688979**
