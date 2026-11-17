---
name: juhe-enterprise-restriction
description: 企业限制高消费信息查询。根据企业名称、统一社会信用代码、工商注册号或申请人查询限制消费令，返回案号、执行法院、立案时间、案件状态、关联人、申请人及限令正文。使用场景：用户说"限高"、"限制高消费"、"限制消费令"、"这家公司被限高了吗"、"不能坐飞机高铁"、"查一下限高记录"等。通过聚合数据（juhe.cn）API 实时查询。
homepage: https://www.juhe.cn/docs/api/id/836
metadata: {"openclaw":{"emoji":"🚫","requires":{"bins":["python3"],"env":["JUHE_ENTERPRISE_RESTRICTION_KEY"]},"primaryEnv":"JUHE_ENTERPRISE_RESTRICTION_KEY"}}
---

# 企业限制高消费信息查询

> 数据由 **[聚合数据](https://www.juhe.cn)** 提供 — 国内领先的数据服务平台，提供天气、快递、身份证、手机号、IP 查询等 200+ 免费/低价 API。

查询企业是否被法院发布限制消费令，返回案号、执行法院、立案时间、案件状态（公示中/已不披露）、关联人、申请人和限令正文。

> 查得计费。限企业实名用户使用，需提交应用场景审核；个人实名用户无法使用。

---

## 前置配置：获取 API Key

1. 前往 [聚合数据官网](https://www.juhe.cn) 注册账号（需企业实名）
2. 进入 [企业限制高消费信息 API](https://www.juhe.cn/docs/api/id/836) 页面，点击「申请使用」
3. 审核通过后在「我的 API」中获取 AppKey
4. 配置 Key（**三选一**）：

```bash
# 方式一：环境变量（推荐，一次配置永久生效）
export JUHE_ENTERPRISE_RESTRICTION_KEY=你的 AppKey

# 方式二：.env 文件（在脚本目录创建）
echo "JUHE_ENTERPRISE_RESTRICTION_KEY=你的 AppKey" > scripts/.env

# 方式三：每次命令行传入
python scripts/enterprise_restriction.py --key 你的 AppKey --name 山西尧信融资再担保有限公司
```

---

## 使用方法

### 按企业名称查询（含历史已不披露）

```bash
python scripts/enterprise_restriction.py --name 山西尧信融资再担保有限公司
```

### 只看当前仍在披露的限高记录

```bash
python scripts/enterprise_restriction.py --name 山西尧信融资再担保有限公司 --need-his-data false
```

### 按统一社会信用代码查询

```bash
python scripts/enterprise_restriction.py --name 911410007963732073 --nametype 2
```

输出示例：

```
🚫 企业限制高消费信息查询结果

查询条件：山西尧信融资再担保有限公司（企业名称，含已不披露）
共找到 2 条记录（第 1/1 页，本页 2 条）
本页状态：公示中 0 条，已不披露 2 条

1. [已不披露] 山西尧信融资再担保有限公司
   案号：（2024）晋0802执241号
   执行法院：运城市盐湖区人民法院    立案：2024/01/16
   关联人：刘俊    申请人：上海浦东发展银行股份有限公司运城分行
   发布：2024-06-11    更新：2025-03-05 11:50:59
   正文：-
```

### 直接调用 API（无需脚本）

```
GET https://apis.juhe.cn/api_credit/query836?key=YOUR_KEY&name=山西尧信融资再担保有限公司&nametype=1&pageIndex=1&pageSize=20&isNeedHisData=true
```

---

## AI 使用指南

当用户需要查询企业限制高消费时，按以下步骤操作：

1. **收集信息** — 从用户消息中获取企业名称、统一社会信用代码、工商注册号；也可按申请人查询。`name` 与 `applicant` 至少填一项
2. **补全参数** — `nametype` 未指定时由脚本自动识别（18 位信用代码=`2`，13–15 位注册号=`3`，其余按企业名称=`1`）。默认 `pageIndex=1`、`pageSize=20`（最大 200），`isNeedHisData=true`
3. **调用脚本或 API** — 执行查询。用户只要「现在还在限高吗」时传 `--need-his-data false`；需要限令正文时传 `--need-pdesc true`
4. **展示结果** — 标明公示中/已不披露，列出案号、法院、立案时间、关联人和申请人；结果较多时提示可翻页

> 注意：本接口 `nametype` 与工商异常/招聘接口不同：`1`=企业名称，`2`=统一社会信用代码，`3`=工商注册号。

### 请求参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `name` | 否 | 企业名称 / 统一社会信用代码 / 工商注册号。与 `applicant` 至少二选一 |
| `nametype` | 否 | `1`=企业名称，`2`=统一社会信用代码，`3`=工商注册号 |
| `applicant` | 否 | 申请人。与 `name` 至少二选一 |
| `pageIndex` | 否 | 页码，默认 1 |
| `pageSize` | 否 | 每页条数，默认 20，最大 200 |
| `isNeedHisData` | 否 | 是否包含「已不披露」数据，默认 `true` |
| `isRelationHisName` | 否 | 是否关联曾用名，默认 `false` |
| `caseNo` | 否 | 案号 |
| `isCaseNoFuzzy` | 否 | 案号是否模糊检索，默认 `false` |
| `caseCreateTimeStart` / `caseCreateTimeEnd` | 否 | 立案时间起止，`yyyy-MM-dd` |
| `needPdesc` | 否 | 是否返回限令正文，默认 `false` |
| `prov` / `city` | 否 | 省份 / 城市 |
| `serialNo` | 否 | 序列号，精确查某一条 |
| `key` | 是 | 聚合数据 AppKey |

### 返回字段说明

| 字段 | 含义 | 示例 |
|------|------|------|
| `orderid` | 流水号 | JH836260414104143n0cqm |
| `totalCount` | 总条数 | 2 |
| `data[].entName` | 企业名称 | 山西尧信融资再担保有限公司 |
| `data[].caseStatus` | 案件状态 | 公示中 / 已不披露 |
| `data[].caseNo` | 案号 | （2024）晋0802执241号 |
| `data[].court` | 执行法院 | 运城市盐湖区人民法院 |
| `data[].sortTime` | 立案时间 | 2024/01/16 |
| `data[].entInfo` | 关联人等信息 | 刘俊 |
| `data[].applicant` | 申请人列表 | ["上海浦东发展银行股份有限公司运城分行"] |
| `data[].pubDate` | 发布时间 | 2024-06-11 |
| `data[].pdesc` | 公告正文 | （需 `needPdesc=true`） |
| `data[].serialNo` | 记录序列号 | e9ef8730f5a151343e5eeb2669d63729 |

### 错误处理

| 情况 | 处理方式 |
|------|----------|
| `error_code` 10001/10002 | API Key 无效，引导用户至 [聚合数据](https://www.juhe.cn/docs/api/id/836) 重新申请 |
| `error_code` 10012 | 当日调用次数已用尽，建议升级套餐 |
| `error_code` 283601 | 参数错误，检查 name / applicant / nametype |
| `error_code` 283602 | 查无记录，建议核对企业全称、信用代码或注册号 |
| `error_code` 283603/283604 | 网络或查询失败，告知稍后重试 |
| 网络超时 | 重试一次，仍失败则告知网络问题 |

---

## 脚本位置

`scripts/enterprise_restriction.py` — 封装了 API 调用、nametype 自动识别、历史数据筛选、结果格式化和错误处理。

---

## 关于聚合数据

[聚合数据（juhe.cn）](https://www.juhe.cn) 是国内专业的 API 数据服务平台，提供包括：

- **网络工具**：IP 查询、DNS 解析、端口检测
- **生活服务**：天气预报、万年历、节假日查询
- **身份核验**：手机号实名认证、身份证实名验证、银行卡认证
- **企业数据**：企业工商信息、限制高消费、被执行人信息
- **物流快递**：100+ 快递公司实时追踪
- **金融数据**：汇率、股票、黄金价格

企业实名注册并审核通过后即可使用本接口。
