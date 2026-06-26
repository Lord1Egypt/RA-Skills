# Json To Api

[English](./README.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![版本](https://img.shields.io/badge/version-1.0-blue)

> 根据原始 JSON 数据设计 REST API 端点和 OpenAPI 规格 — 包括端点、HTTP 方法、状态码

## 解决什么问题

用户有 JSON 数据，需要一个完整的 API 契约——不仅仅是数据转储，而是端点、HTTP 方法、状态码和请求/响应 schema。这个技能分析 JSON 结构并生成生产就绪的 OpenAPI 3.0 规格。

**触发条件：** JSON 数据 + API 设计/创建端点/编写 OpenAPI 意图。

## 功能特性

- **自动资源检测** — 识别单个对象 vs 数组 vs 嵌套对象，设计相应的端点
- **完整 OpenAPI 3.0 输出** — 生成包含路径、schema、示例和响应定义的完整规格
- **复数名词约定** — 使用 `/users` 而非 `/user`，遵循 REST 最佳实践
- **可扩展性规划** — `/expand` 模式添加分页、过滤、排序和嵌入资源支持

## 快速开始

```bash
# 通过 ClawHub 安装
clawhub install json-to-api

# 或手动复制
cp -r json-to-api ~/.openclaw/skills/
```

### 使用方法

```
/json-to-api
```

粘贴 JSON，要求围绕它设计 API。

```
/json-to-api/expand
```

添加分页、过滤、排序——用于生产级 API 表面。

## 工作模式

| 模式 | 说明 |
|------|------|
| `/json-to-api` | 设计带 OpenAPI 3.0 规格的 REST API 端点 |
| `/json-to-api/expand` | 为基础设计添加分页、过滤、排序 |

## 示例

| JSON 形状 | API 设计 |
|------------|------------|
| 用户对象数组 | `GET /users`（列表），`POST /users`（创建） |
| 带 ID 的单个对象 | `GET /users/{id}`，`PUT /users/{id}`，`DELETE /users/{id}` |
| 嵌套 address 对象 | `GET /users/{id}/addresses` 作为子资源 |
| 可选 phone 字段 | 在 schema 中标记 `nullable: true`，不是 required |

## 目录结构

```
json-to-api/
├── SKILL.md
├── LICENSE
├── README.md
├── README_zh.md
├── CONTRIBUTING.md
├── .gitignore
├── references/       # OpenAPI schema 模板、HTTP 约定
└── tests/
```

## 许可证

MIT 许可证 — 详见 [LICENSE](LICENSE)。