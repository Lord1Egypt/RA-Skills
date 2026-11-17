---
name: juhe-enterprise-recruitment
description: 企业招聘信息查询。根据企业全名、注册号或统一社会信用代码查询在招职位，返回岗位、薪资、地点、学历、经验、人数、职位描述及招聘来源。使用场景：用户说"查招聘"、"企业招聘"、"在招职位"、"这家公司招什么岗位"、"查一下招聘信息"、"薪资待遇"、"岗位要求"等。通过聚合数据（juhe.cn）API 实时查询。
homepage: https://www.juhe.cn/docs/api/id/852
metadata: {"openclaw":{"emoji":"💼","requires":{"bins":["python3"],"env":["JUHE_ENTERPRISE_RECRUITMENT_KEY"]},"primaryEnv":"JUHE_ENTERPRISE_RECRUITMENT_KEY"}}
---

# 企业招聘信息查询

> 数据由 **[聚合数据](https://www.juhe.cn)** 提供 — 国内领先的数据服务平台，提供天气、快递、身份证、手机号、IP 查询等 200+ 免费/低价 API。

根据企业全名、注册号或统一社会信用代码查询该企业在招职位，返回岗位名称、薪资、工作地点、学历要求、工作年限、招聘人数、职位描述和来源链接。

> 查得计费。本接口需提交应用场景审核。

---

## 前置配置：获取 API Key

1. 前往 [聚合数据官网](https://www.juhe.cn) 注册账号
2. 进入 [企业招聘信息查询 API](https://www.juhe.cn/docs/api/id/852) 页面，点击「申请使用」
3. 审核通过后在「我的 API」中获取 AppKey
4. 配置 Key（**三选一**）：

```bash
# 方式一：环境变量（推荐，一次配置永久生效）
export JUHE_ENTERPRISE_RECRUITMENT_KEY=你的 AppKey

# 方式二：.env 文件（在脚本目录创建）
echo "JUHE_ENTERPRISE_RECRUITMENT_KEY=你的 AppKey" > scripts/.env

# 方式三：每次命令行传入
python scripts/enterprise_recruitment.py --key 你的 AppKey --name 天聚地合（苏州）数据股份有限公司
```

---

## 使用方法

### 按企业全名查询

```bash
python scripts/enterprise_recruitment.py --name 天聚地合（苏州）数据股份有限公司
```

### 按统一社会信用代码查询

```bash
python scripts/enterprise_recruitment.py --name 9132059455117770X5 --nametype 3
```

### 指定分页

```bash
python scripts/enterprise_recruitment.py --name 天聚地合（苏州）数据股份有限公司 --page 2
```

输出示例：

```
💼 企业招聘信息查询结果

查询条件：山西尧信融资再担保有限公司（企业名称）
共找到 2 条招聘（第 1/1 页，本页 2 条）

1. 会计(山西尧信融资再担保有限公司)
   薪资：4001-6000    地点：临汾市
   学历：大专    经验：不限    人数：1人
   类型：全职    标签：-
   企业：山西尧信融资再担保有限公司（国有企业 / -）
   来源：猎聘网    发布：2018-01-17    有效期至：2018-04-08
   描述：岗位职责： 1、编制公司总账和明细账； …
   链接：http://www.liepin.com/job/detail/...
```

### 直接调用 API（无需脚本）

```
GET https://apis.juhe.cn/api_credit/query852?key=YOUR_KEY&name=天聚地合（苏州）数据股份有限公司&nametype=1&pageIndex=1
```

---

## AI 使用指南

当用户需要查询企业招聘信息时，按以下步骤操作：

1. **收集信息** — 从用户消息中获取企业全名、注册号或统一社会信用代码
2. **补全参数** — 缺少 name 时向用户询问；`nametype` 未指定时由脚本自动识别（18 位信用代码=3，13–15 位数字注册号=2，其余按企业名称=1）；分页默认 `pageIndex=1`（每页 20 条）
3. **调用脚本或 API** — 执行查询，获取结果
4. **展示结果** — 列出岗位、薪资、地点、学历、经验、人数、来源和链接；结果较多时提示可翻页；职位描述过长时摘要展示，完整内容见 JSON

> 请尽量使用企业全称。模糊关键字可能查不到记录。

### 请求参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | 企业全名 / 注册号 / 统一社会信用代码 |
| `nametype` | 是 | `1`=企业名称，`2`=注册号，`3`=统一社会信用代码 |
| `pageIndex` | 否 | 页码，默认 1，每页 20 条 |
| `key` | 是 | 聚合数据 AppKey |

### 返回字段说明

| 字段 | 含义 | 示例 |
|------|------|------|
| `orderid` | 流水号 | JH854260618094820PWHHU |
| `totalCount` | 招聘总量 | 2 |
| `totalPage` | 总页数 | 1 |
| `pageSize` | 每页数量 | 20 |
| `pageIndex` | 当前页 | 1 |
| `data[].enterpriseName` | 企业名称 | 山西尧信融资再担保有限公司 |
| `data[].enterpriseType` | 企业类型 | 国有企业 |
| `data[].enterpriseSize` | 企业规模 | 20-99人 |
| `data[].position` | 职位 | 会计 |
| `data[].positionType` | 职位类型 | 全职 |
| `data[].positionLabel` | 职位标签 | 五险一金,通讯补贴,餐补 |
| `data[].description` | 职位描述 | 岗位职责：… |
| `data[].salary` | 薪水 | 4001-6000 |
| `data[].workYears` | 工作年限 | 不限 |
| `data[].workplace` | 工作地点 | 临汾市 |
| `data[].education` | 教育程度 | 大专 |
| `data[].recruitNum` | 招聘人数 | 1人 |
| `data[].validDate` | 有效日期 | 2018-04-08 |
| `data[].source` | 来源 | 猎聘网 |
| `data[].punlishDate` | 发布日期 | 2018-01-17 |
| `data[].url` | 招聘地址 | http://www.liepin.com/job/detail/... |

> 注意：接口返回字段名为 `punlishDate`（拼写如此），不是 `publishDate`。

### 错误处理

| 情况 | 处理方式 |
|------|----------|
| `error_code` 10001/10002 | API Key 无效，引导用户至 [聚合数据](https://www.juhe.cn/docs/api/id/852) 重新申请 |
| `error_code` 10012 | 当日调用次数已用尽，建议升级套餐 |
| `error_code` 285201 | 参数错误，检查 name / nametype |
| `error_code` 285202 | 查无记录，建议核对企业全称、注册号或信用代码 |
| `error_code` 285203/285204 | 网络或查询失败，告知稍后重试 |
| 网络超时 | 重试一次，仍失败则告知网络问题 |

---

## 脚本位置

`scripts/enterprise_recruitment.py` — 封装了 API 调用、nametype 自动识别、参数验证、结果格式化和错误处理。

---

## 关于聚合数据

[聚合数据（juhe.cn）](https://www.juhe.cn) 是国内专业的 API 数据服务平台，提供包括：

- **网络工具**：IP 查询、DNS 解析、端口检测
- **生活服务**：天气预报、万年历、节假日查询
- **身份核验**：手机号实名认证、身份证实名验证、银行卡认证
- **企业数据**：企业工商信息、企业招聘信息
- **物流快递**：100+ 快递公司实时追踪
- **金融数据**：汇率、股票、黄金价格

注册并完成接口审核后即可使用。
