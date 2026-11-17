---
name: juhe-enterprise-executed
description: 企业被执行人信息查询（公示中及历史）。根据企业名称、统一社会信用代码、工商注册号或关键词查询被执行案件，返回案号、执行法院、执行标的、立案时间、案件状态。使用场景：用户说"被执行人"、"被执行"、"查执行案件"、"这家公司有没有被法院执行"、"执行标的"、"公示中被执行"、"历史被执行"等。通过聚合数据（juhe.cn）API 实时查询。
homepage: https://www.juhe.cn/docs/api/id/842
metadata: {"openclaw":{"emoji":"⚖️","requires":{"bins":["python3"],"env":["JUHE_ENTERPRISE_EXECUTED_KEY"]},"primaryEnv":"JUHE_ENTERPRISE_EXECUTED_KEY"}}
---

# 企业被执行人信息查询（公示中及历史）

> 数据由 **[聚合数据](https://www.juhe.cn)** 提供 — 国内领先的数据服务平台，提供天气、快递、身份证、手机号、IP 查询等 200+ 免费/低价 API。

查询企业当前公示中及历史被执行人记录，返回案号、执行法院、执行标的、立案时间和案件状态。

> 查得计费。限企业实名用户使用，需提交应用场景审核；个人实名用户无法使用。

---

## 前置配置：获取 API Key

1. 前往 [聚合数据官网](https://www.juhe.cn) 注册账号（需企业实名）
2. 进入 [企业被执行人信息 API](https://www.juhe.cn/docs/api/id/842) 页面，点击「申请使用」
3. 审核通过后在「我的 API」中获取 AppKey
4. 配置 Key（**三选一**）：

```bash
# 方式一：环境变量（推荐，一次配置永久生效）
export JUHE_ENTERPRISE_EXECUTED_KEY=你的 AppKey

# 方式二：.env 文件（在脚本目录创建）
echo "JUHE_ENTERPRISE_EXECUTED_KEY=你的 AppKey" > scripts/.env

# 方式三：每次命令行传入
python scripts/enterprise_executed.py --key 你的 AppKey --name 河北展发房地产开发有限公司
```

---

## 使用方法

### 按企业名称查询（含历史已不披露）

```bash
python scripts/enterprise_executed.py --name 河北展发房地产开发有限公司
```

### 只看当前公示中的被执行记录

```bash
python scripts/enterprise_executed.py --name 河北展发房地产开发有限公司 --need-his-data false
```

### 按统一社会信用代码查询

```bash
python scripts/enterprise_executed.py --name 911309005661956791 --nametype 2
```

输出示例：

```
⚖️ 企业被执行人信息查询结果

查询条件：河北展发房地产开发有限公司（企业名称，含已不披露）
共找到 127 条记录（第 1/7 页，本页 20 条）
本页状态：公示中 4 条，已不披露 16 条

1. [公示中] 河北展发房地产开发有限公司
   案号：（2026）冀0929执2777号
   执行法院：河北省沧州市献县人民法院
   执行标的：126,000    立案：2026/07/09
   主体标识：911309005661956791
   采集：2026/07/13    更新：2026/07/20
```

### 直接调用 API（无需脚本）

```
GET https://apis.juhe.cn/api_credit/query842?key=YOUR_KEY&name=河北展发房地产开发有限公司&nametype=1&pageIndex=1&pageSize=20&isNeedHisData=true
```

---

## AI 使用指南

当用户需要查询企业被执行人信息时，按以下步骤操作：

1. **收集信息** — 从用户消息中获取企业名称、统一社会信用代码、工商注册号或关键词
2. **补全参数** — 缺少 name 时向用户询问；`nametype` 未指定时由脚本自动识别（18 位信用代码=`2`，13–15 位注册号=`3`，其余按企业名称=`1`）。默认 `pageIndex=1`、`pageSize=20`（最大 200），`isNeedHisData=true`
3. **调用脚本或 API** — 执行查询。用户只要「现在还在被执行吗」时传 `--need-his-data false`
4. **展示结果** — 标明公示中/已不披露，列出案号、法院、执行标的、立案时间；结果较多时提示可翻页

> 注意：本接口 `nametype` 与工商异常/招聘接口不同：`1`=企业名称，`2`=统一社会信用代码，`3`=工商注册号，`4`=关键词。  
> `partyCardNum` 可能是组织机构代码/信用代码，也可能是身份证号。若为身份证号，面向用户必须脱敏（保留前 6 后 4），禁止明文回显。

### 请求参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `name` | 否 | 企业全名 / 统一社会信用代码 / 工商注册号 / 关键词 |
| `nametype` | 否 | `1`=企业名称，`2`=统一社会信用代码，`3`=工商注册号，`4`=关键词查询 |
| `pageIndex` | 否 | 页码，默认 1 |
| `pageSize` | 否 | 每页条数，默认 20，最大 200 |
| `isNeedHisData` | 否 | 是否包含「已不披露」数据，默认 `true` |
| `isRelationHisName` | 否 | 是否关联曾用名，默认 `false` |
| `caseNo` | 否 | 案号 |
| `isCaseNoFuzzy` | 否 | 案号是否模糊检索，默认 `false` |
| `caseCreateTimeStart` / `caseCreateTimeEnd` | 否 | 立案时间起止，`yyyy-MM-dd` |
| `province` / `city` | 否 | 省份 / 城市 |
| `serialNo` | 否 | 序列号，精确查某一条 |
| `key` | 是 | 聚合数据 AppKey |

### 返回字段说明

| 字段 | 含义 | 示例 |
|------|------|------|
| `orderid` | 流水号 | JH842260721114908XMcze |
| `totalCount` | 总条数 | 127 |
| `totalPage` | 总页数 | 7 |
| `data[].pName` | 被执行人名称 | 河北展发房地产开发有限公司 |
| `data[].caseCode` | 案号 | （2026）冀0929执2777号 |
| `data[].execCourtName` | 执行法院 | 河北省沧州市献县人民法院 |
| `data[].execMoney` | 执行标的 | 126000 |
| `data[].partyCardNum` | 主体标识 | 组织机构代码 / 信用代码 / 身份证号 |
| `data[].caseCreateTime` | 立案时间 | 2026/07/09 |
| `data[].caseStatus` | 案件状态 | 公示中 / 已不披露 |
| `data[].inputTime` | 首次采集日期 | 2026/07/13 |
| `data[].updateTime` | 最新更新日期 | 2026/07/20 |
| `data[].serialNo` | 记录序列号 | 27a1e9b5ce264a601fd06ace2c5aec65 |

### 错误处理

| 情况 | 处理方式 |
|------|----------|
| `error_code` 10001/10002 | API Key 无效，引导用户至 [聚合数据](https://www.juhe.cn/docs/api/id/842) 重新申请 |
| `error_code` 10012 | 当日调用次数已用尽，建议升级套餐 |
| `error_code` 284201 | 参数错误，检查 name / nametype |
| `error_code` 284202 | 查无记录，建议核对企业全称、信用代码或注册号 |
| `error_code` 284203/284204 | 网络或查询失败，告知稍后重试 |
| 网络超时 | 重试一次，仍失败则告知网络问题 |

---

## 脚本位置

`scripts/enterprise_executed.py` — 封装了 API 调用、nametype 自动识别、身份证号脱敏、结果格式化和错误处理。

---

## 关于聚合数据

[聚合数据（juhe.cn）](https://www.juhe.cn) 是国内专业的 API 数据服务平台，提供包括：

- **网络工具**：IP 查询、DNS 解析、端口检测
- **生活服务**：天气预报、万年历、节假日查询
- **身份核验**：手机号实名认证、身份证实名验证、银行卡认证
- **企业数据**：企业工商信息、被执行人信息、限制高消费
- **物流快递**：100+ 快递公司实时追踪
- **金融数据**：汇率、股票、黄金价格

企业实名注册并审核通过后即可使用本接口。
