---
name: product-data-collection
description: Describes product collection task HTTP APIs (create, pick, update, batch-update), task types, statuses, success payload rules, and browser-extension vs dashboard roles. Use when integrating collection workers, task queues, or product REST task endpoints.
version: 1.0.1
license: MIT
metadata: {"openclaw":{"emoji":"📦","requires":{"env":["PRODUCT_TASK_AUTH","PRODUCT_DATA_COLLECTION_BASE_URL"]},"primaryEnv":"PRODUCT_TASK_AUTH"}}
---

# 商品数据采集（任务队列）

## 环境与鉴权（勿写入仓库与对话）

以下变量由部署方提供，经 `openclaw.json` → `skills.entries["product-data-collection"].env` 或主机环境注入；**禁止**写进 skill 正文示例值、聊天、截图或日志。

| 变量 | 含义 |
|------|------|
| `PRODUCT_DATA_COLLECTION_BASE_URL` | API 根，**不含**末尾 `/`。例如 `https://你的主机` |
| `PRODUCT_TASK_AUTH` | 请求头 `Authorization` 的完整值（是否含 `Bearer ` 按服务端要求） |

Shell 中先组装前缀再调接口：

```bash
BASE="${PRODUCT_DATA_COLLECTION_BASE_URL}"
TASK="${BASE}/api/ebay_product/task"
```

未授权返回 403。代理、扩展、脚本均从环境变量读取，勿硬编码域名与密钥。

## 任务接口前缀

- 统一前缀：`${TASK}`（即 `$BASE/api/ebay_product/task`），以下路径均相对该前缀，方法均为 **POST**。

## 端点一览

| 路径 | 作用 |
|------|------|
| `/create` | 批量创建/覆盖排队任务（upsert：`itemId` + `taskVersionName`） |
| `/pick` | 领取下一条待采集任务（先本用户 `queued`，否则全局 `queued`） |
| `/update` | 上报成功/失败等；`status === success` 时会写入商品库 |
| `/batch-update` | 按筛选条件批量将非成功任务改为 `queued` 或 `canceled` |

完整 URL 形如：`"$TASK/create"`、`"$TASK/pick"` 等。

## 任务类型 `taskType`

- `all`：需车型表 `vehicle_information`，且需 `specifications` 或 `kit_parts_included` 至少其一。
- `ignore_vehicle_error`：不强制车型表；需 `specifications` 或 `kit_parts_included`。
- `ignore_attribute_error`：需 `vehicle_information`；规格/套件约束较宽松。

## 任务状态 `taskStatus`

- `queued` → `collecting`（pick 时）→ `success` / `failed` / `canceled`
- 已成功任务不可再被 update；批量更新会排除已成功记录。

## `POST …/task/create`

Body（JSON）：

- `taskVersionName`：非空字符串，用于批次/版本隔离。
- `taskType`：上表枚举之一。
- `data`：非空数组，元素含 `itemId`（数字）、可选 `category`。

返回常为写入统计（如 matched/upserted 计数等，以实现为准）。

## `POST …/task/pick`

- Body 可为空。
- 返回一条任务文档或 `null`（无队列时）。
- 领取后状态变为 `collecting`。

## `POST …/task/update`

常用字段：

- 标识：`itemId`、`taskVersionName`、`taskType`
- 页面元信息：`title`、`url`、`category`（可选）
- 结果：`status`（如 `success`、`failed`）；`failed` 时必须带 `failReason`
- 成功且需落库时，按 `taskType` 满足 DTO 校验后附带解析结果，例如：
  - `specifications`（对象）
  - `vehicle_information`（数组）
  - `kit_parts_included`（字符串数组）

`success` 时服务端会将商品数据 upsert 到商品集合（以 `itemId` 唯一）。

## `POST …/task/batch-update`

Body：

- `status`：`queued` 或 `canceled`
- `user`：筛选用户（非空）
- `createdAtStart` / `createdAtEnd`：创建时间范围（字符串，按服务端日切解析）
- 可选：`itemId`、`category`、`taskVersionName`、`taskStatus` 等缩小范围

仅更新**非 success** 任务。

## 浏览器端采集（内容脚本）

- 从详情页 DOM 解析：`specifications`、`vehicle_information`、`kit_parts_included`；`title`、`url` 等与页面一致即可。
- 通过已带鉴权的请求封装调用 `pick` → 抓取 → `update`；`BASE` 与 `Authorization` 来自构建时或运行时的私密配置，勿打印完整头。

## 控制台 / 看板

- 列表、导出等多走 dashboard 专用接口（如 `collect_tasks`、`export-data`），与上述 `$TASK/*` 任务接口分工不同。
- 批量导入任务、批量改队列状态可调用 `create`、`batch-update`；域名与密钥仍只来自环境变量。

## 发布与协作注意

- 文档与 skill 中不出现真实主机名与密钥字面量。
- 变更 API 时同步更新本 skill 中的路径与字段说明。
