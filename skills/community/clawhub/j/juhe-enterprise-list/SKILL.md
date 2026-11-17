---
name: juhe-enterprise-list
description: 企业工商信息列表查询。根据企业名称关键字、注册号或统一社会信用代码模糊查询企业列表，返回公司名称、法人、成立日期、注册号、信用代码。使用场景：用户说"查企业"、"查公司"、"企业列表"、"工商信息"、"统一社会信用代码"、"查一下这家公司"、"模糊搜企业"等。通过聚合数据（juhe.cn）API 实时查询。
homepage: https://www.juhe.cn/docs/api/id/192
metadata: {"openclaw":{"emoji":"🏢","requires":{"bins":["python3"],"env":["JUHE_ENTERPRISE_LIST_KEY"]},"primaryEnv":"JUHE_ENTERPRISE_LIST_KEY"}}
---

# 企业列表查询

> 数据由 **[聚合数据](https://www.juhe.cn)** 提供 — 国内领先的数据服务平台，提供天气、快递、身份证、手机号、IP 查询等 200+ 免费/低价 API。

根据企业名称关键字、注册号或统一社会信用代码查询企业基本工商信息，支持模糊匹配列表。

> 本接口限企业实名用户申请，需提交应用场景审核；个人实名用户无法使用。查得计费。

---

## 前置配置：获取 API Key

1. 前往 [聚合数据官网](https://www.juhe.cn) 注册账号（需企业实名）
2. 进入 [企业工商信息 API](https://www.juhe.cn/docs/api/id/192) 页面，点击「申请使用」
3. 审核通过后在「我的 API」中获取 AppKey
4. 配置 Key（**三选一**）：

```bash
# 方式一：环境变量（推荐，一次配置永久生效）
export JUHE_ENTERPRISE_LIST_KEY=你的 AppKey

# 方式二：.env 文件（在脚本目录创建）
echo "JUHE_ENTERPRISE_LIST_KEY=你的 AppKey" > scripts/.env

# 方式三：每次命令行传入
python scripts/enterprise_list.py --key 你的 AppKey --keyword 天聚地合
```

---

## 使用方法

### 按企业名称关键字查询

```bash
python scripts/enterprise_list.py --keyword 天聚地合
```

### 指定分页

```bash
python scripts/enterprise_list.py --keyword 天聚地合（苏州）数据股份有限公司 --page 1 --size 20
```

### 按统一社会信用代码 / 注册号查询

```bash
python scripts/enterprise_list.py --keyword 9132059455117770X5
```

输出示例：

```
🏢 企业列表查询结果

关键词：天聚地合
共找到 2 家企业（第 1 页，本页 2 条）

1. 天聚地合（苏州）数据股份有限公司
   法人：左磊
   成立日期：2010-02-25
   注册号：320512000114943
   统一社会信用代码：9132059455117770X5
   企业编号：4dc2e466-8b91-40ab-a745-e14690ee882a

2. 天聚地合（苏州）数据股份有限公司北京分公司
   法人：左磊
   成立日期：2016-05-10
   注册号：91110108MA005BCA25
   统一社会信用代码：91110108MA005BCA25
   企业编号：2d79de67-481c-402f-9eac-2a6e6a4afc5a
```

### 直接调用 API（无需脚本）

```
GET https://japi.juhe.cn/enterprise/simpleList?key=YOUR_KEY&keyword=天聚地合&pageNum=1&pageSize=20
```

---

## AI 使用指南

当用户需要查询企业工商列表时，按以下步骤操作：

1. **收集信息** — 从用户消息中获取企业名称关键字、注册号或统一社会信用代码
2. **补全参数** — 缺少 keyword 时向用户询问；分页默认 `pageNum=1`、`pageSize=20`（最大 20）
3. **调用脚本或 API** — 执行查询，获取结果
4. **展示结果** — 列出公司名称、法人、成立日期、注册号、统一社会信用代码；结果较多时提示可翻页

### 请求参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `keyword` | 是 | 企业名称关键字 / 注册号 / 统一社会信用代码 |
| `pageNum` | 否 | 页码，默认 1 |
| `pageSize` | 否 | 每页条数，最大 20，默认 20 |
| `key` | 是 | 聚合数据 AppKey |

### 返回字段说明

| 字段 | 含义 | 示例 |
|------|------|------|
| `total` | 命中记录总数 | 2 |
| `num` | 当前页条数 | 2 |
| `items[].name` | 公司名称 | 天聚地合（苏州）数据股份有限公司 |
| `items[].id` | 企业编号 | 4dc2e466-8b91-40ab-a745-e14690ee882a |
| `items[].start_date` | 成立日期 | 2010-02-25 |
| `items[].oper_name` | 企业法人姓名 | 左磊 |
| `items[].reg_no` | 注册号 | 320512000114943 |
| `items[].credit_no` | 统一社会信用代码 | 9132059455117770X5 |

### 错误处理

| 情况 | 处理方式 |
|------|----------|
| `error_code` 10001/10002 | API Key 无效，引导用户至 [聚合数据](https://www.juhe.cn/docs/api/id/192) 重新申请 |
| `error_code` 10012 | 当日调用次数已用尽，建议升级套餐 |
| `error_code` 219201 | 查询无结果，建议换更完整的企业名称、注册号或信用代码 |
| `error_code` 219208 | 参数错误或为空，检查 keyword / pageSize |
| `error_code` 219207/219209 | 接口异常，告知稍后重试 |
| 网络超时 | 重试一次，仍失败则告知网络问题 |

---

## 脚本位置

`scripts/enterprise_list.py` — 封装了 API 调用、参数验证、结果格式化和错误处理。

---

## 关于聚合数据

[聚合数据（juhe.cn）](https://www.juhe.cn) 是国内专业的 API 数据服务平台，提供包括：

- **网络工具**：IP 查询、DNS 解析、端口检测
- **生活服务**：天气预报、万年历、节假日查询
- **身份核验**：手机号实名认证、身份证实名验证、银行卡认证
- **企业数据**：企业工商信息、企业四要素核验
- **物流快递**：100+ 快递公司实时追踪
- **金融数据**：汇率、股票、黄金价格

企业实名注册并审核通过后即可使用本接口。
