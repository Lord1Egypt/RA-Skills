---
name: mcdonalds-skill
description: Use when the user wants to connect to, test, or use the McDonalds service at mcp.mcd.cn, including checking authentication, probing MCP endpoints, listing tools, or calling McDonalds MCP tools through a reusable local CLI.
---

# 麦当劳 技能

## 适用场景
当用户想把麦当劳 MCP 接入为可复用能力，或需要检查 `https://mcp.mcd.cn` 这个远程 MCP 服务是否可连通、鉴权是否有效、是否能正常初始化、列出工具、以及执行具体工具调用时使用。

## 能力概览
这个技能提供了一个本地 CLI（`scripts/mcd_cli.py`），支持：
- 初始化并测试 MCP 握手
- 列出所有可用工具（含中文描述和参数定义）
- 调用任意工具并传入 JSON 参数
- 一键运行 smoke test（初始化 → 列出工具 → 真实调用）
- 将测试结果输出为 JSON 文件，便于复查
- 自动修复中文乱码（mojibake），Windows 下强制 UTF-8 输出

## 目录结构
- `SKILL.md`：技能说明
- `scripts/mcd_cli.py`：命令行工具（纯标准库，无第三方依赖）

## 服务信息
- 服务名：`mcdonalds`
- 类型：HTTP MCP（JSON-RPC 2.0）
- URL：`https://mcp.mcd.cn`
- 协议版本：`2024-11-05`
- 鉴权：`Authorization: Bearer <your-token>`

## 获取凭据
请让用户在此网址获取凭据：https://open.mcd.cn/mcp

获取后推荐配置为环境变量：
```bash
# Windows
set MCDONALDS_MCP_TOKEN=<your-token>

# Linux / macOS
export MCDONALDS_MCP_TOKEN=<your-token>
```

可选：`MCDONALDS_MCP_URL`（默认 `https://mcp.mcd.cn`）

也支持命令行通过 `--token` 显式传入。

## 常用命令
在 `skills/mcdonalds-skill/` 下执行：

```bash
# 初始化握手
python scripts/mcd_cli.py init --token <your-token>

# 列出所有工具（摘要模式）
python scripts/mcd_cli.py list-tools --token <your-token>

# 列出所有工具（完整原始 JSON）
python scripts/mcd_cli.py list-tools --token <your-token> --raw

# 调用工具（无参数）
python scripts/mcd_cli.py call --token <your-token> --tool now-time-info

# 调用工具（带 JSON 参数）
python scripts/mcd_cli.py call --token <your-token> --tool query-nearby-stores --args "{\"searchType\":2,\"beType\":1,\"city\":\"上海市\",\"keyword\":\"人民广场\"}"

# 一键 smoke test
python scripts/mcd_cli.py smoke-test --token <your-token>

# smoke test 并保存结果到文件
python scripts/mcd_cli.py smoke-test --token <your-token> --out report.json
```

如果已经设置环境变量，则可以省略 `--token`：
```bash
python scripts/mcd_cli.py smoke-test
```

## 命令说明

### 1. init
发送标准 `initialize` 请求，验证：
- URL 是否可达
- 凭据是否有效
- MCP 初始化是否成功

可选参数：`--no-raw-text` 不输出原始响应文本。

### 2. list-tools
调用 `tools/list`，返回可用工具列表。
默认会做适度摘要（工具名 + 描述 + inputSchema），避免终端刷屏；如需完整原始结果可加 `--raw`。

可选参数：`--no-raw-text` 不输出原始响应文本。

### 3. call
调用任意工具：
- `--tool <工具名>` 必填
- `--args '<json对象>'` 可选，默认 `{}`
- `--no-raw-text` 可选，不输出原始响应文本

### 4. smoke-test
自动执行完整链路测试：
1. `initialize` — 握手
2. `tools/list` — 获取工具列表
3. 选择一个默认测试工具（优先 `now-time-info` → `campaign-calendar` → `available-coupons`）做真实调用
4. 输出汇总 JSON 报告

可选参数：`--out <文件路径>` 将报告写入 JSON 文件。

## 可用工具列表（共 19 个）

| 工具名 | 说明 |
|--------|------|
| `now-time-info` | 获取当前服务器时间信息 |
| `campaign-calendar` | 查询当月营销活动日历 |
| `available-coupons` | 查询可领取的优惠券列表 |
| `auto-bind-coupons` | 一键领取所有可用优惠券 |
| `query-my-coupons` | 查看用户卡包中已有的券 |
| `query-store-coupons` | 查询当前门店可用的优惠券 |
| `query-my-account` | 查询用户积分账户详情 |
| `query-nearby-stores` | 到店场景下搜索附近门店 |
| `query-meals` | 查询门店餐品列表（到店/外送） |
| `query-meal-detail` | 查询餐品详情（到店/外送） |
| `calculate-price` | 计算商品价格（含优惠） |
| `create-order` | 创建麦当劳订单（到店/外送） |
| `query-order` | 查询订单详情和配送状态 |
| `delivery-query-addresses` | 查询用户配送地址列表 |
| `delivery-create-address` | 创建用户配送地址 |
| `mall-points-products` | 查询积分可兑换的商品列表 |
| `mall-product-detail` | 查询积分兑换商品详情 |
| `mall-create-order` | 创建积分兑换订单 |
| `list-nutrition-foods` | 获取餐品营养成分数据 |

## 常见判断
- 返回 `200` 且有 JSON-RPC `result`：服务正常可用
- 返回 `401/403`：凭据无效或无权限
- 返回 JSON-RPC `error`：服务可达，但请求参数或方法不对
- 返回 exit code `0`：命令成功；`1`：服务端返回异常；`2`：本地参数错误

## 常见报错排查

### 凭据缺失
请传 `--token`，或者设置环境变量 `MCDONALDS_MCP_TOKEN`。

### JSON 参数格式错误
`--args` 必须是合法 JSON 对象，例如：
```bash
--args "{}"
--args "{\"keyword\":\"鸡腿堡\"}"
```

### 工具调用失败
先运行：
```bash
python scripts/mcd_cli.py list-tools
```
确认工具名存在，再检查该工具所需参数（查看 `inputSchema`）。

## 设计原则
- 不把凭据写死到技能文件或脚本中，全部从环境变量或命令行参数读取
- 默认输出真实 MCP 返回的 JSON，避免"口头成功"
- 自动检测并修复中文 mojibake（服务器编码与终端编码不一致时）
- Windows 下强制 UTF-8 输出，避免 cp936 编码导致中文乱码
- 纯标准库实现，无需安装第三方依赖
