---
name: juhe-enterprise-detail
description: 企业信息精确查询。根据企业全名、注册号或统一社会信用代码精确匹配工商详情，返回法人、注册资本、经营范围、地址、主要人员、股东、分支机构、变更记录、经营异常。使用场景：用户说"精确查企业"、"工商详情"、"查一下这家公司详细信息"、"股东和法人"、"经营范围"、"变更记录"、"用信用代码查公司"等。通过聚合数据（juhe.cn）API 实时查询。
homepage: https://www.juhe.cn/docs/api/id/319
metadata: {"openclaw":{"emoji":"📋","requires":{"bins":["python3"],"env":["JUHE_ENTERPRISE_DETAIL_KEY"]},"primaryEnv":"JUHE_ENTERPRISE_DETAIL_KEY"}}
---

# 企业信息精确查询

> 数据由 **[聚合数据](https://www.juhe.cn)** 提供 — 国内领先的数据服务平台，提供天气、快递、身份证、手机号、IP 查询等 200+ 免费/低价 API。

根据企业全名、注册号或统一社会信用代码**精确匹配**目标企业，返回法定代表人、注册资本、经营范围、注册地址、主要人员、股东、分支机构、变更记录和经营异常等完整工商信息。

> 查得计费。限企业实名用户使用，需提交应用场景审核；个人实名用户无法使用。  
> 模糊搜企业列表请用 `juhe-enterprise-list`；本技能需要全称或证件号精确查询。

---

## 前置配置：获取 API Key

1. 前往 [聚合数据官网](https://www.juhe.cn) 注册账号（需企业实名）
2. 进入 [企业信息精确查询 API](https://www.juhe.cn/docs/api/id/319) 页面，点击「申请使用」
3. 审核通过后在「我的 API」中获取 AppKey
4. 配置 Key（**三选一**）：

```bash
# 方式一：环境变量（推荐，一次配置永久生效）
export JUHE_ENTERPRISE_DETAIL_KEY=你的 AppKey

# 方式二：.env 文件（在脚本目录创建）
echo "JUHE_ENTERPRISE_DETAIL_KEY=你的 AppKey" > scripts/.env

# 方式三：每次命令行传入
python scripts/enterprise_detail.py --key 你的 AppKey --keyword 天聚地合（苏州）数据股份有限公司
```

---

## 使用方法

### 按企业全名精确查询

```bash
python scripts/enterprise_detail.py --keyword 天聚地合（苏州）数据股份有限公司
```

### 按统一社会信用代码查询

```bash
python scripts/enterprise_detail.py --keyword 9132059455117770X5
```

输出示例：

```
📋 企业信息精确查询结果

企业名称：天聚地合（苏州）数据股份有限公司北京分公司
经营状态：在业
企业类型：股份有限公司分公司(非上市、自然人投资或控股)
法定代表人：左磊
成立日期：2016-05-10
统一社会信用代码：91110108MA005BCA25
地址：北京市海淀区永澄北路2号院1号楼A座四层405-200
经营范围：网络技术服务；会议服务；…

主要人员（1）
   1. 左磊  负责人

变更记录（1）
   1. 2017-11-29  企业名称
      变更前：苏州新科兰德科技有限公司北京分公司
      变更后：天聚地合（苏州）数据股份有限公司北京分公司
```

### 直接调用 API（无需脚本）

```
GET https://japi.juhe.cn/enterprise/getDetailByName?key=YOUR_KEY&keyword=天聚地合（苏州）数据股份有限公司
```

---

## AI 使用指南

当用户需要查询企业详细工商信息时，按以下步骤操作：

1. **收集信息** — 获取企业全名、注册号或统一社会信用代码。只有简称时先引导补全全称，或改用企业列表模糊查询
2. **调用脚本或 API** — 执行精确查询
3. **展示结果** — 先给基本信息（名称、状态、法人、资本、信用代码、地址、经营范围），再列主要人员、股东、分支、变更、经营异常

### 请求参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `keyword` | 是 | 企业全名 / 注册号 / 统一社会信用代码 |
| `key` | 是 | 聚合数据 AppKey |

### 返回字段说明

| 字段 | 含义 | 示例 |
|------|------|------|
| `name` | 公司名称 | 天聚地合（苏州）数据股份有限公司北京分公司 |
| `status` | 经营状态 | 在业 |
| `econ_kind` | 企业类型 | 股份有限公司分公司… |
| `oper_name` | 法人 | 左磊 |
| `start_date` | 成立日期 | 2016-05-10 |
| `regist_capi_new` | 注册资本 | 万元 |
| `currency_unit` | 货币单位 | 人民币 |
| `credit_no` | 统一社会信用代码 | 91110108MA005BCA25 |
| `reg_no` | 注册号 | — |
| `address` | 地址 | 北京市海淀区… |
| `scope` | 经营范围 | 网络技术服务；… |
| `employees[]` | 主要人员 | name / job_title |
| `partners[]` | 股东 | name / stock_type / 认缴实缴 |
| `branches[]` | 分支机构 | name |
| `changerecords[]` | 变更记录 | change_item / change_date / before_content / after_content |
| `abnormal_items[]` | 经营异常 | in_reason / in_date / out_reason / out_date |

> 文档字段名 `addresses`、`brances` 与实际返回可能为 `address`、`branches`。股东认缴金额字段为 `shoud_capi`（拼写如此）。证件号码为非公示项，接口固定返回 `-`。

### 错误处理

| 情况 | 处理方式 |
|------|----------|
| `error_code` 10001/10002 | API Key 无效，引导用户至 [聚合数据](https://www.juhe.cn/docs/api/id/319) 重新申请 |
| `error_code` 10012 | 当日调用次数已用尽，建议升级套餐 |
| `error_code` 231901 | 查询无结果，建议改用企业全称、注册号或信用代码 |
| `error_code` 231908 | 参数为空，检查 keyword |
| `error_code` 231907/231909 | 接口异常，告知稍后重试 |
| 网络超时 | 重试一次，仍失败则告知网络问题 |

---

## 脚本位置

`scripts/enterprise_detail.py` — 封装了 API 调用、工商详情分组展示和错误处理。

---

## 关于聚合数据

[聚合数据（juhe.cn）](https://www.juhe.cn) 是国内专业的 API 数据服务平台，提供包括：

- **企业数据**：企业列表、企业精确查询、经营异常、被执行人、限制高消费
- **车辆数据**：VIN 查车辆信息
- **身份核验**：手机号实名认证、身份证实名验证、银行卡认证
- **生活服务**：天气预报、万年历、快递查询

企业实名注册并审核通过后即可使用本接口。
