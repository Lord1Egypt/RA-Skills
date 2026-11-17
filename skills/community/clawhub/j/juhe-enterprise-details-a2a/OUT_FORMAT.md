# 企业信息精确查询输出格式

支付成功并拿到接口 JSON 后渲染。**仅使用接口返回字段，禁止编造内容。**

## 输出顺序（固定）

```markdown
{企业概要模板}   ← 有 result.data 时必渲染，排第一

{主要人员模板}   ← employees 非空时渲染

{股东信息模板}   ← partners 非空时渲染

{分支机构模板}   ← branches 非空时渲染

{变更记录模板}   ← changerecords 非空时渲染

{经营异常模板}   ← abnormal_items 非空时渲染

---
*以上数据来源于第三方数据服务，仅供参考，请以国家企业信用信息公示系统等官方登记信息为准。*
```

无查询结果（`result.data` 缺失或为空）时，输出「未查询到该企业信息」提示 + 页脚免责。

---

## 企业概要模板

数据路径：`result.data.*`（外层 `reason`、`error_code`、`result.sign` 不展示给用户）。

### 渲染结构

```markdown
# 🏢 企业信息查询结果

> 🔍 查询关键词：{用户查询的 keyword}

## 基本信息

| 项目 | 内容 |
| ---- | ---- |
| 企业名称 | {name} |
| 经营状态 | {status} |
| 企业类型 | {econ_kind} |
| 法定代表人 | {oper_name} |
| 注册资本 | {regist_capi_new}{currency_unit 格式化} |
| 成立日期 | {start_date} |
| 核准日期 | {check_date} |
| 营业期限 | {term_start} 至 {term_end} |
| 注销日期 | {end_date，为 "-" 时显示「—」} |

## 注册信息

| 项目 | 内容 |
| ---- | ---- |
| 统一社会信用代码 | {credit_no} |
| 企业注册号 | {reg_no} |
| 组织机构号 | {org_no} |
| 所属工商局 | {belong_org} |
| 省份 | {province} |

## 地址与经营范围

**注册地址**：{address 或 addresses，空值显示「—」}

**经营范围**：

{scope}
```

### 字段映射

| 展示项 | JSON 字段 | 说明 |
| ------ | --------- | ---- |
| 企业名称 | `name` | 公司全称 |
| 经营状态 | `status` | 如「存续」「在业」 |
| 企业类型 | `econ_kind` | 如「股份有限公司」 |
| 法定代表人 | `oper_name` | 法人姓名 |
| 注册资本 | `regist_capi_new` + `currency_unit` | 如 `5011.82` + `CNY` →「5011.82 万元（CNY）」；`regist_capi` 有值时优先展示 |
| 成立日期 | `start_date` | 如 `2010-02-25` |
| 核准日期 | `check_date` | 如 `2024-10-24` |
| 营业期限起 | `term_start` | 营业开始日期 |
| 营业期限止 | `term_end` | 为 `-` 时显示「长期」或「—」 |
| 注销日期 | `end_date` | 未注销时为 `-` |
| 统一社会信用代码 | `credit_no` | 18 位 |
| 企业注册号 | `reg_no` | |
| 组织机构号 | `org_no` | |
| 所属工商局 | `belong_org` | |
| 省份 | `province` | 省份缩写，如 `JS` |
| 注册地址 | `address` 或 `addresses` | 接口可能返回其一 |
| 经营范围 | `scope` | 长文本单独段落展示 |

### currency_unit 格式化

| 原始值 | 展示格式 |
| ------ | -------- |
| `CNY` | 万元（人民币） |
| `-` 或空 | 不追加单位 |
| 其他 | 原样展示 |

---

## 主要人员模板

遍历 `result.data.employees` 数组渲染。

```markdown
## 主要人员

| 姓名 | 职位 |
| ---- | ---- |
| {name} | {job_title} |
```

---

## 股东信息模板

遍历 `result.data.partners` 数组，每人独立成节或合并表格。

```markdown
## 股东信息

### 股东 #{序号}：{name}

| 项目 | 内容 |
| ---- | ---- |
| 股东类型 | {stock_type} |
| 证照类型 | {identify_type，为 "-" 时显示「—」} |
| 证照号码 | {identify_no，为 "-" 时显示「非公示项」} |

**认缴出资**（`should_capi_items` 非空时）：

| 认缴出资额 | 出资方式 | 出资时间 |
| ---------- | -------- | -------- |
| {shoud_capi} | {invest_type} | {should_capi_date} |

**实缴出资**（`real_capi_items` 非空时）：

| 实缴出资额 | 出资方式 | 实缴时间 |
| ---------- | -------- | -------- |
| {real_capi} | {invest_type} | {real_capi_date} |
```

---

## 分支机构模板

遍历 `result.data.branches` 数组渲染。

```markdown
## 分支机构

| 序号 | 分支机构名称 |
| ---- | ------------ |
| 1 | {name} |
```

---

## 变更记录模板

遍历 `result.data.changerecords` 数组，**按 change_date 降序**（最新变更在前）。

```markdown
## 工商变更记录

### 变更 #{序号}：{change_item}

| 项目 | 内容 |
| ---- | ---- |
| 变更日期 | {change_date} |
| 变更前 | {before_content} |
| 变更后 | {after_content} |
```

变更内容过长时保留完整文本，可用引用块展示。

---

## 经营异常模板

遍历 `result.data.abnormal_items` 数组渲染；数组为空时跳过本节。

```markdown
## 经营异常记录

### 异常 #{序号}

| 项目 | 内容 |
| ---- | ---- |
| 列入原因 | {in_reason} |
| 列入日期 | {in_date} |
| 移出原因 | {out_reason，空值显示「—」} |
| 移出日期 | {out_date，空值显示「—」} |
```

---

## 渲染规则

1. **概要首位**：有 `result.data` 时，必须先渲染 [企业概要模板](#企业概要模板)，再渲染各明细节。
2. **数组遍历**：各数组字段独立成节，序号从 1 递增。
3. **排序**：变更记录默认按 `change_date` 降序；字段缺失时不参与排序比较。
4. **空值处理**：字段缺失、空字符串、`null`、`-` 时显示「—」；`abnormal_items`、`branches` 为空数组时跳过对应节。
5. **文本清洗**：去除 HTML/script 标签；保留中文标点与换行。
6. **禁止臆造**：不生成接口未返回的财务数据、诉讼信息等内容。
7. **页脚免责**（固定追加）：

```markdown
---
*以上数据来源于第三方数据服务，仅供参考，请以国家企业信用信息公示系统等官方登记信息为准。*
```
