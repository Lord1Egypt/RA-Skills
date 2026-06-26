---
name: mocklab
description: |
  MockLab 是一个**智能接口工具箱**，支持 Mock 数据生成、请求转发、数据复现——接口开发调试一站式解决。

  支持任意格式的接口文档（Markdown、Word、Java 源码、纯文本等）和任意结构（表格、嵌套 JSON、加密字段、数组对象等）。模型自动理解文档并驱动整个流程：解析文档 → 生成 Schema → 启动 Mock Server → 打开 UI。

  触发词包括："启动 MockLab"、"创建一个 Mock Server"、"帮我 mock 这个接口"、"对接第三方接口"等。

  ⚠️ AI 生成 Schema 前必须先阅读参考示例：
  - `references/demo.json` — 完整 Schema 模板（如何写 interface / inner_schema / 字段规则）
  - `references/demo__实际返回示例.json` — Python 代码对每个规则的【实际生成结果】
  - `references/field_keys.md` — 字段 Key 命名规范（铁律：必须照抄文档第一列）
  AI 必须严格遵守 field_keys.md 的命名规则，Schema field.name 必须与接口文档一字不差，禁止自己发明或转换字段名。
---

# MockLab

## 核心流程

用户说"启动 MockLab"并提供接口文档后，执行以下步骤：

```
1. 获取文档内容
   - 本地文件路径 → Read 工具读取
   - URL 链接 → web_fetch 抓取
   - 直接粘贴内容 → 直接使用

2. 模型自主解析文档
   - 提取所有接口：路径、方法、请求/响应字段
   - 推断每个字段的 Mock 生成规则
   - 整理 inner_schemas（嵌套子结构）
   - 整理 partner 信息（渠道号、签名格式等）
   - 判断跨接口状态关联（ref 字段）

3. 保存 Schema 到 schema_store/
   - 文件名：schema_store/{project_name}.json
   - project_name 由模型根据文档内容生成（如"平安银行"、"微信支付"）

4. 启动 Mock Server
   python {skill_path}/mock_server.py --port 18080 --project {project_name}

5. 自动打开浏览器
   http://localhost:18080

6. 告知用户服务已启动，介绍如何使用
```

## Schema 生成规则

模型根据字段语义自动推断 rule，写入 Schema：

| 字段特征 | rule | 生成结果 |
|---------|------|---------|
| 渠道/合作方 ID | `fixed:{值}` | 固定值 |
| 随机数 | `random:6` | 6位随机数字 |
| 时间戳 | `timestamp:ms` | 毫秒时间戳 |
| 手机号 | `phone` | 11位真实号段手机号 |
| 身份证 | `idcard` | 18位合法身份证 |
| 姓名 | `name` | 中文姓名 |
| 车牌号 | `plate` | 合规车牌号 |
| 金额 | `amount:lo-hi` | 指定范围金额 |
| 利率 | `rate:lo-hi` | 指定范围利率 |
| Token | `token:32` | 32位随机字符串 |
| 枚举 | `enum:a,b,c` 或 `enum:k=v,k=v` | 枚举值 |
| 自增序列 | `sequence:{key}` | 自增序列号 |
| 国标码 | `province:code` | 省市国标码+名称 |
| 日期 | `date:format` | 格式化日期 |
| 嵌套对象 | `nested:{schema_name}` | 引用 inner_schemas |
| 对象数组 | `array:{schema_name}` | 数组，元素引用 inner_schemas |
| 子对象 | `object:{schema_name}` | 引用 inner_schemas |
| 跳过 | `skip` | 不生成（sign 等） |
| 请求镜像 | `mirror` | 取请求 body 中同名字段的值，原样返回 |
| 动态取 body | `body:data.order_id` | 取请求 body 中嵌套字段 |
| 动态取路径 | `path:order_id` | 取 URL 路径参数 |
| 动态取参数 | `query:page` | 取 URL query string 参数 |
| 动态取头 | `header:Authorization` | 取请求头 |
| 动态取状态 | `state:token` | 取跨次调用状态（ref 字段） |
| 条件包含 | `when:{"field":"status","eq":"1"}` | 满足条件时才返回该字段 |

## 字段语义智能判断

模型根据字段名和中文含义自主判断，无需用户指定：

- 含 `phone`、`mobile`、`手机` → `phone`
- 含 `idcard`、`身份证`、`证件号` → `idcard`
- 含 `name`、`姓名`、`cust_name` → `name`
- 含 `plate`、`license`、`车牌` → `plate`
- 含 `amount`、`amt`、`金额`、`loan` → `amount`
- 含 `rate`、`利率` → `rate`
- 含 `province`、`省份` → `province:code`
- 含 `city`、`城市` → `city:province_code`
- 含 `sign`、`签名` → `skip`
- 含 `ciphertext`、`加密` → `skip`（标注加密占位）
- 含 `seq`、`no`、`编号`、`订单` → `sequence:{field_name}`

## reqData / data 加密字段处理

- 模型从文档提取加密**明文结构**
- 写入 `rule: "nested:{schema_name}"` 引用 inner_schemas
- UI 上点击可展开看到完整明文
- 响应中字段值显示 `"[SM4加密占位]"`

## ref 跨接口状态关联

- 响应字段标记 `"is_ref": true` → 自动存入状态表
- 后续接口请求中引用该字段时，自动填充上一次的值
- 状态持久化到 `state_store.json`，服务重启不丢失
- UI 上显示"引用自 X.X"标识

**示例（accessToken 跨接口传递）：**
```json
// applyAccessToken 响应字段
{ "name": "accessToken", "rule": "token:32", "is_ref": true }

// 后续接口请求字段
{ "name": "accessToken", "rule": "state:accessToken" }
```

## ① 延迟模拟（interface.delay）

**推荐在 UI 上直接配置**（http://localhost:18080 选中接口后顶部设置栏）。

勾选"延迟" → 输入最小值和最大值（ms）。也可以在 Schema JSON 里写：

```json
{ "delay": "200-500" }
```

| 写法 | 效果 |
|------|------|
| `"delay": "300"` | 固定 300ms |
| `"delay": "200-500"` | 随机 200~500ms |
| `"delay": "1000-3000"` | 大压力测试 1~3s |

## ② 错误注入（interface.error）

**推荐在 UI 上直接配置**，清晰分隔每个参数。

勾选"错误" → 选择错误类型 → 填概率/错误码/消息。也可以在 Schema JSON 里写：

```json
{ "error": "500@0.05:ERR001:自定义错误消息" }
```

格式：`错误类型[@概率[:错误码[:消息]]]`

| 字段 | 说明 |
|------|------|
| 错误类型 | HTTP状态码（500/400/401/403/404/429）或 `timeout` / `network_error` / `rate_limit` |
| 概率 | 0.0~1.0，1.0 = 100% 触发 |
| 错误码 | 自定义业务错误码（如 ERR001） |
| 消息 | 自定义错误消息内容 |

## ③ 请求镜像（mirror / body:xxx）

把请求参数原样反射回响应，让接口"更逼真"：

```json
{
  "name": "下单",
  "path": "/order/create",
  "req_fields": [
    { "name": "order_id", "type": "string" },
    { "name": "amount", "type": "number" }
  ],
  "resp_fields": [
    { "name": "order_id", "rule": "mirror" },
    { "name": "amount", "rule": "mirror" },
    { "name": "status", "rule": "fixed:PAID" }
  ]
}
```

请求 `{"order_id": "A123", "amount": 100}` → 响应 `{"order_id": "A123", "amount": 100, "status": "PAID"}`

## ④ 动态响应（path:xxx / query:xxx / header:xxx / state:xxx / when）

根据请求内容动态生成响应，不只是返回假数据：

### 路径参数
```json
{ "name": "order_id", "rule": "path:order_id" }
```
`GET /order/{order_id}` → 响应中 `order_id` 引用 URL 里实际的值

### 查询参数
```json
{ "name": "page", "rule": "query:page" }
```
`GET /list?page=2` → 响应中 `page` 取 query 参数值

### 嵌套 body 字段
```json
{ "name": "user_phone", "rule": "body:user.phone" }
```
请求 `{"user": {"phone": "13800138000"}}` → 响应 `{"user_phone": "13800138000"}`

### 跨次状态引用
```json
{ "name": "token", "rule": "state:access_token" }
```
取上一次登录接口存入的 `access_token` 状态

### 条件字段（when）
```json
{ "name": "vip_discount", "rule": "amount:0-0.5", "when": {"field": "body.is_vip", "op": "eq", "value": true} }
{ "name": "discount", "rule": "fixed:0", "when": {"field": "body.is_vip", "op": "exists"} }
```
只有满足条件时才返回该字段，支持 `eq` / `ne` / `gt` / `lt` / `contains` / `exists` / `not_exists`

## 启动命令

```bash
python {skill_path}/mock_server.py --port 18080 --project {project_name}
```

## 运行时文件结构

```
{skill_path}/
├── SKILL.md
├── mock_server.py          # FastAPI 服务（内嵌 HTML UI）
└── schema_store/           # 由服务器自动创建
    ├── {project_1}.json
    └── {project_2}.json
```

服务器运行后创建：
- `schema_store/` 目录
- `state_store.json` 状态文件

## 多项目支持

- 每个第三方为独立项目
- 运行中调用 `POST /mock/load` 实时加载新项目（无需重启）
- UI 右上角项目下拉框切换

## 错误处理

- 文档格式无法解析 → 向用户询问更多信息
- 缺少关键字段 → 模型根据语义合理推断，标注"推测"
- 端口被占用 → 自动尝试下一个端口（18081, 18082...）
- Schema 加载失败 → 报错并展示具体错误位置
