---
name: ifind-repilot-announcement-search
description: 通过问句语义化搜索A股、基金、港美股相关公告信息（年报、半年报、季报、临时公告、招股说明书等），返回与问句相关的公告片段信息。当需要检索上市公司公告、财务报告、监管公告等信息时，使用此 skill。
metadata:  {"openclaw":{"emoji":"📰︎","requires":{"bins":["python3"]}}}
---

## 概述

此 skill 通过自然语言问句查询（向量检索）全市场公司公告信息。它调用封装好的 Python 脚本，向同花顺数据接口发送请求，返回与问句相关的公告列表信息。支持按照时间范围查询。

## 前置要求

### 环境依赖

- Python 3.x
- 标准库：`json`, `urllib`, `pathlib`
- 无需安装第三方库
- 注1：若 `python3` 命令不可用（常见于 Windows），请改用 `python`
- 注2：`<skill_dir>` 为当前 skill 所在目录的完整路径，请根据当前上下文自动获取。


### 首次配置

首次使用 skill 前，需要先配置认证 token。

1. 提示用户先从飞研平台获取 token。平台地址： https://repilot.51ifind.com/ ，菜单路径：业务管理 -> Skills技能库。
2. 用户提供token后，运行以下命令配置 token：
```bash
python3 <skill_dir>/scripts/fetch_data.py --set-token <your_auth_token>
```
3. 检查 token 是否已配置：
```bash
python3 <skill_dir>/scripts/fetch_data.py --check-token
```

注：配置文件位于：`~/.config/ifind-repilot/config.json`

## 使用方式

### 基本查询

```bash
python3 <skill_dir>/scripts/fetch_data.py "<查询语句>"
```

### 带时间范围查询

```bash
python3 <skill_dir>/scripts/fetch_data.py "<查询语句>" --start-date <开始日期> --end-date <结束日期>
```

日期格式：`YYYY-MM-DDTHH:MM:SS`，例如 `2025-01-01T00:00:00`

日期参数可以放在查询语句之前或之后：

```bash
# 方式一：日期参数在前
python3 <skill_dir>/scripts/fetch_data.py --start-date 2025-01-01T00:00:00 --end-date 2026-01-01T00:00:00 "同花顺公告"

# 方式二：日期参数在后
python3 <skill_dir>/scripts/fetch_data.py "同花顺公告" --start-date 2025-01-01T00:00:00 --end-date 2026-01-01T00:00:00
```

### 查询示例

| 查询内容 | 命令 |
|---------|------|
| 同花顺公告 | `python3 <skill_dir>/scripts/fetch_data.py "同花顺公告"` |
| 贵州茅台临时公告 | `python3 <skill_dir>/scripts/fetch_data.py "贵州茅台临时公告"` |
| 2025年同花顺公告 | `python3 <skill_dir>/scripts/fetch_data.py "同花顺公告" --start-date 2025-01-01T00:00:00 --end-date 2025-12-31T23:59:59` |


### 返回格式

脚本直接返回查询结果的 JSON 数据，包含以下字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `total` | int | 检索到的公告总数 |
| `status_code` | int | 状态码，0表示成功 |
| `status_msg` | string | 状态信息 |
| `data` | array | 公告列表 |

每条公告包含以下字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `title` | string | 公告标题 |
| `summary` | string | 公告摘要 |
| `url` | string | 公告原文链接 |
| `channel` | string | 频道类型 |
| `publish_time` | int | 发布时间（Unix时间戳） |
| `publish_date` | string | 发布时间（格式：YYYY-MM-DD HH:MM:SS） |
| `score` | float | 相关性评分 |
| `stock_infos` | array | 关联股票信息列表，每项包含 `code` 和 `name` |
| `extra` | object | 扩展信息 |

返回示例：

```json
{
  "total": 4,
  "status_code": 0,
  "data": [
    {
      "title": "同花顺：关于股票交易异常波动公告",
      "summary": "证券代码：300033         证券简称：同花顺         公告编号：2024-029\n浙江核新同花顺网络信息股份有限公司关于股票交易异常波动公告...",
      "url": "http://static.cninfo.com.cn/finalpage/2024-09-30/1221332134.PDF",
      "channel": "announcement",
      "publish_time": 1727625600,
      "publish_date": "2024-09-30 00:00:00",
      "score": 0.108995356,
      "stock_infos": [
        {"code": "A00627"},
        {"code": "300033", "name": "同花顺"}
      ],
      "extra": {}
    }
  ],
  "status_msg": "OK"
}
```

### 错误处理

| 错误信息 | 原因 | 解决方法 |
|----------|------|----------|
| `请先配置 auth_token` | 未设置 token | 提示用户获取并发送token，收到token后，运行 `--set-token` 配置 |
| `API HTTP 错误` | 请求失败 | 检查网络或 API 地址 |
| `网络错误` | 无法连接 | 检查网络连接 |
| `API 返回失败` | 接口返回错误 | 查看具体错误信息 |
| `API HTTP 错误: 429` | 触发当日请求限制 | 提醒用户到飞研平台检查用量信息 |
| `API HTTP 错误: 401` | 缺失token或者token无效 | 提醒用户检查token是否正确 |
| `API HTTP 错误: 403` | 没有权限访问接口 | 没有权限访问接口 |


## 执行规则

1. 先判断用户请求或任务是否需要公司公告检索。
2. 若需要公司公告检索，根据用户请求内容与思考，生成一个合适的自然语言查询语句作为参数调用脚本。
3. 若请求返回未检索到数据、或者返回的数据不符合期望，可以尝试生成一个新的自然语言查询语句重新查询。
4. 不要编造任何公告信息。若脚本失败或返回空结果，应明确说明失败原因或未检索到数据。
5. 将脚本输出中的信息重新组织和提炼；保留公告标题、关联股票和摘要中的重要数据。
6. 当出现401、403、429错误时，请勿再重试，直接提醒用户skill返回的错误内容。
