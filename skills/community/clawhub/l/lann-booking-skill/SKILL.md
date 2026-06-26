---
name: lann-booking
slug: lann-booking
label: 兰泰式按摩预约
description: 提供蘭泰式按摩（Lann Thai Massage）的门店查询、SPA服务查询和在线预约功能。支持泰式古法按摩、精油护理、草本热敷等专业服务预约，覆盖上海、杭州、成都等多城市门店。
metadata: {"clawdbot":{"emoji":"💆","requires":{"bins":[]}}}
version: "2.0.0"
---

# 蘭泰式按摩预约技能 (Lann Booking Skill)

**关键词**：泰式按摩、预约、SPA、Lann、lann、蘭、兰泰、古法按摩、精油护理、草本热敷

## 意图与数据源

**意图触发**：
| 意图 | 触发关键词 |
|------|-----------|
| `query_stores` | 门店、地址、电话、附近、哪里有 |
| `query_services` | 服务、按摩、SPA、项目、有什么、多长时间 |
| `create_booking` | 预约、预订、订一个、帮我约 |

**数据源**：
- `org_store.json` — 75 家门店（名称、地址、电话、交通指引、经纬度）
- `prod_service.json` — 28 项服务（名称、描述）

**参考文档**：
- API 规范 / MCP 配置 / 错误码：`references/api_reference.md`
- 预约回复模板：`assets/booking_template.md`

## 集成模式

本 Skill 支持三种调用模式，AI 应根据运行环境自动选择：

| 优先级 | 模式 | 场景 | 连接方式 |
|--------|------|------|----------|
| 1 | MCP 客户端 | 本地或远程部署 `lann-mcp-server` | stdio / streamableHttp |
| 2 | 远程 MCP 服务 | 直接连接已部署的 MCP 服务 | `https://open.lannlife.com/mcp`（streamableHttp） |
| 3 | 直连 API（降级） | 无 MCP 环境时的备选 | HTTP POST `https://open.lannlife.com/mcp/book/create` |

> MCP 配置和 API 请求/响应详细规范见 `references/api_reference.md`。

## 能力定义

### 查询门店 (query_stores)

通过读取 `org_store.json` 或调用 MCP 工具 `query_stores` 检索门店信息。

**支持操作**：列出全部门店、按城市筛选（上海/杭州/成都/深圳/苏州/武汉/宁波）、按关键词模糊匹配（名称/地址/地铁站）、获取单店详情。

**门店数据字段**：
| 字段 | 说明 |
|------|------|
| `name` | 门店名称（**唯一标识符**，预约时必须完全匹配） |
| `address` | 详细地址 |
| `telephone` | 联系电话 |
| `traffic` | 交通指引（含地铁线路和出口） |
| `longitude` / `latitude` | 经纬度，可用于距离计算 |

**门店分布**：上海 ~60 家、杭州 7 家、成都 4 家、其他城市各 1-2 家。

### 查询服务 (query_services)

通过读取 `prod_service.json` 或调用 MCP 工具 `query_services` 检索服务项目。

**支持操作**：列出全部服务、按名称/描述关键词匹配、根据用户需求推荐。

**服务数据字段**：
| 字段 | 说明 |
|------|------|
| `name` | 服务名称（**唯一标识符**，预约时必须完全匹配） |
| `desc` | 服务详细描述（用于关键词匹配和推荐） |

**服务分类概览**：
1. **传统古法按摩系列**（6 项）：90-120 分钟，推/拉/蹬/摇/踩等手法
2. **泰式精油护理系列**（7 项）：60-120 分钟，植物精油 + 泰式手法
3. **特色护理系列**（8 项）：椰香按摩、轻体 Spa、水光焕肤等
4. **快速/专项服务系列**（5 项）：肩颈版、精华版、深度拉伸等
5. **其他**（2 项）

> 注意：`"泊兰泰"` 的 `desc` 为 null，推荐时应跳过该条目或提示用户联系门店了解详情。

### 创建预约 (create_booking)

**必填参数**：

| 参数 | 类型 | 校验规则 | 示例 |
|------|------|----------|------|
| `mobile` | string | 正则 `/^1[3-9]\d{9}$/`（11 位中国大陆手机号） | `"13812345678"` |
| `storeName` | string | 必须与 `org_store.json` 中 `name` 完全一致 | `"淮海店"` |
| `serviceName` | string | 必须与 `prod_service.json` 中 `name` 完全一致 | `"传统古法全身按摩-90分钟"` |
| `count` | number | 1-20 之间的整数 | `2` |
| `bookTime` | string | ISO 8601 格式，且晚于当前时间 | `"2024-01-15T14:00:00"` |

> 请求/响应格式、错误码和重试策略见 `references/api_reference.md`。
> 预约成功/失败的回复模板见 `assets/booking_template.md`。

## 工作流规则

### 参数收集

当用户意图为创建预约但信息不完整时：
- **缺门店** → 根据用户提到的地区/地标/地铁线在 `org_store.json` 中模糊匹配，展示前 5 个候选让用户选择
- **缺服务** → 根据用户需求描述匹配 `prod_service.json` 中的 `desc` 字段，推荐 3-5 个相关服务
- **缺时间** → 询问并将自然语言（如"明天下午2点"）转换为 ISO 8601 格式，确保晚于当前时间
- **缺手机号** → 提示用户提供，说明仅用于门店联系确认
- **缺人数** → 默认 1 人，或询问用户

### 名称匹配

用户输入通常包含简称或错别字，不能直接作为 API 参数：
1. 先用用户输入在数据源中做模糊匹配（包含匹配）
2. 若命中唯一结果，使用该结果的 `name` 字段
3. 若命中多个结果，列出候选让用户选择
4. 若未命中，提示用户重新描述或展示可用列表

### 提交确认

在调用预约 API 之前，必须将所有参数汇总展示（手机号脱敏为 `138****5678`），等用户确认后再提交。

### 时间处理

- 存储/传输：ISO 8601（`YYYY-MM-DDTHH:mm:ss`）
- 展示：友好格式（`2024年1月15日 14:00`）
- 时区：默认北京时间（UTC+8）

## 业务规则

- 建议至少提前 2 小时预约
- 取消或改期需至少提前 1 小时联系门店
- 单次预约最多 20 人，超过需分批预约或联系门店
- 各门店营业时间可能不同，请以门店实际为准
- 手机号仅在预约时临时使用，日志中脱敏显示，不持久化存储

## 相关资源

- API 请求/响应规范、MCP 配置、错误码：[`references/api_reference.md`](references/api_reference.md)
- 预约回复消息模板：[`assets/booking_template.md`](assets/booking_template.md)
- 测试脚本：[`scripts/test_booking.py`](scripts/test_booking.py) / [`scripts/test_booking.sh`](scripts/test_booking.sh)
- 门店数据：[`org_store.json`](org_store.json)（75 家）
- 服务数据：[`prod_service.json`](prod_service.json)（28 项）

## 版本历史

- **v2.0.0**（2026-04-09）：重构 Skill 架构，支持三种集成模式，优化意图识别和参数校验
- **v1.0.2**（2026-04-03）：初始版本
