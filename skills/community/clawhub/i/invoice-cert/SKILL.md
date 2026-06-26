---
name: invoice-cert
description: 发票认证技能。税局登录、发票勾选认证、抵扣统计。适用于进项发票勾选、认证、统计等税务操作场景。
---

# 发票认证技能

使用此技能进行税局登录、发票勾选认证、查询认证状态、申请抵扣统计等操作。

## 使用场景

满足以下需求时使用：

- 登录税局系统（电子税务局）。
- 查询发票的勾选认证状态。
- 提交或取消发票勾选认证。
- 申请或撤销抵扣统计。
- 查询抵扣统计数据。
- 查询当前属期已认证的发票集合。
- 查询当前税款所属期。
- 确认签名。

## 触发语句示例

以下用户输入应触发此技能：

- 帮我登录税局 / 税局登录 / 登录电子税务局
- 查一下这张发票的认证状态 / 发票认证状态
- 提交认证 / 勾选认证 / 取消认证
- 申请统计 / 撤销统计 / 抵扣统计
- 查看已认证发票 / 当前属期发票
- 确认签名
- 税款所属期 / 当前属期 / 查询税款所属期
- 发票勾选 / 认证发票

## 输入参数

执行前准备以下参数：

- apiKey（必填）：通过 https://skill.quandianfapiao.com/ 申请。

### 税局登录 (login)

- 税号（必填）
- 账号（选填，登录时可能需要）
- 密码（选填，登录时可能需要）
- 地区码（选填，如 BJ、TJ）

### 验证码登录 (login-sms)

- 验证码（必填）
- 税号（必填）
- 账号（必填）

### 发送验证码 (send-sms)

- 税号（必填）
- 账号（必填）

### 确认签名 (sign)

无额外参数。

### 查询当前税款所属期 (current-period)

无额外参数。

### 申请或撤销统计 (statistics)

- 提交类型（必填）：1 申请统计，2 撤销统计
- bz（必填）：N 忽略未勾选发票直接统计，Y 取消未完成的统计状态

### 查询抵扣统计数据 (deduct-stats)

- 税款所属期（选填，不填默认当前属期）

### 查询当前属期认证发票集合 (checked-invoices)

- 税款所属期（选填，不填默认当前属期，传入可查询历史认证记录）

### 查询发票认证状态 (check-status)

- 发票号码（必填）
- 开票日期（必填，格式 YYYY-MM-DD）
- 发票代码（选填）

### 提交或取消认证 (commit-deduction)

- 提交类型（必填）：1 勾选认证，2 取消勾选认证
- 发票列表（必填）：每条包含发票代码、开票日期、发票号码
- 税款所属期（选填，不填默认当前属期）

**批量处理规则：**

- 提交前无需先查验认证状态，可直接提交或取消认证。
- 多张发票时自动按开票日期（kprq）升序排序后提交。
- 每批最多 50 张，超出自动分批。

## 执行流程

**前置检查（最高优先级）：检查环境变量 `ZXT_API_KEY` 是否已设置。**

注意：当前 shell 会话可能未继承 Windows 用户级环境变量，必须按以下方式检查，不能仅依赖 `$ZXT_API_KEY`：

- Windows：执行 `powershell -Command "[System.Environment]::GetEnvironmentVariable('ZXT_API_KEY', 'User')"` 获取用户级环境变量值，同时检查 `$ZXT_API_KEY`。
- macOS/Linux：检查 `$ZXT_API_KEY` 即可。

如果以上检查结果均为空，禁止执行任何后续操作，立即向用户输出以下提示并停止：

> 您需要完成以下三步，即可自动配置并执行技能：
>
> 1. **注册账号**
>    访问中兴通简税Skill平台：https://skill.quandianfapiao.com/ 完成注册。
>
> 2. **申请 apiKey**
>    登录后进入"技能中心"，复制您的 apiKey。
>
> 3. **提供 apiKey**
>    将复制的 apiKey 发送给我，我将为您完成配置并立即执行技能。

**严格限制：前置检查未通过时，禁止执行任何其他动作，包括但不限于：**

- 禁止读取文件（Excel、PDF、图片等）
- 禁止调用任何 API
- 禁止执行任何脚本或命令
- 禁止进行参数解析或预处理

**只允许输出提示信息，然后停止，等待用户提供 apiKey。**

用户提供 apiKey 后，写入系统环境变量并使当前会话生效：

- Windows：`setx ZXT_API_KEY <apiKey>` 写入用户级环境变量，然后执行 `export ZXT_API_KEY=<apiKey>` 使当前会话生效。
- macOS/Linux：将 `export ZXT_API_KEY=<apiKey>` 追加到 `~/.bashrc` 或 `~/.zshrc`（根据用户使用的 shell），同时执行 `export ZXT_API_KEY=<apiKey>` 使当前会话生效。

环境变量就绪后，继续以下步骤：

1. 校验必填参数存在且非空。**任何必填参数缺失时必须立即停止，禁止跳过或使用空值继续执行。**
2. 通过 python 执行脚本调用远程 API（Windows 下使用 `python`，macOS/Linux 使用 `python3`），脚本优先使用 `--api-key` 参数，未传则回退读取环境变量 `ZXT_API_KEY`。
3. 检查返回的 status 字段：
   - 非 200 且非 309 时，停止并将错误信息展示给用户。
   - **status 为 309 时**，脚本自动使用会话缓存中的登录凭证（creditCode、account、password）重新登录税局，登录成功后自动重试原请求。若缓存不存在或自动重登失败，则提示用户手动登录。
4. 解析返回结果并以可读格式输出。

### 税局登录流程说明

调用登录接口后，根据 `returnType` 分支处理：

- **returnType=4000**：直接登录成功，可继续调用其他接口。
- **returnType=4001**：需要验证码登录，会返回带星手机号。引导用户发送验证码（`send-sms`）→ 输入验证码完成登录（`login-sms`）。
- **returnType=4002**：需要设置地区，会返回可选地区列表。引导用户选择地区码后使用 `--area-code` 参数重新登录。

## 请求参数说明

### 1. 税局登录 — POST /api/jxplus/zxtSkill/dzsj/dzsjLogin

| 参数       | 类型   | 必填 | 说明                 |
| ---------- | ------ | ---- | -------------------- |
| apiKey     | string | 是   | apiKey               |
| creditCode | string | 是   | 税号（纳税人识别号） |
| account    | string | 否   | 税局账号             |
| password   | string | 否   | 税局密码             |
| areaCode   | string | 否   | 地区码（如 BJ、TJ）  |

### 2. 验证码登录 — POST /api/jxplus/zxtSkill/dzsj/dzsjLoginBySmsCode

| 参数       | 类型   | 必填 | 说明         |
| ---------- | ------ | ---- | ------------ |
| apiKey     | string | 是   | apiKey       |
| creditCode | string | 是   | 纳税人识别号 |
| account    | string | 是   | 税局账号     |
| smsCode    | string | 是   | 短信验证码   |

### 3. 发送验证码 — POST /api/jxplus/zxtSkill/dzsj/dzsjSendSmsCode

| 参数       | 类型   | 必填 | 说明         |
| ---------- | ------ | ---- | ------------ |
| apiKey     | string | 是   | apiKey       |
| creditCode | string | 是   | 纳税人识别号 |
| account    | string | 是   | 税局账号     |

### 4. 确认签名 — POST /api/jxplus/zxtSkill/check/doSignature

| 参数   | 类型   | 必填 | 说明   |
| ------ | ------ | ---- | ------ |
| apiKey | string | 是   | apiKey |

### 5. 查询当前税款所属期 — POST /api/jxplus/zxtSkill/check/getCurrSkssq

| 参数   | 类型   | 必填 | 说明   |
| ------ | ------ | ---- | ------ |
| apiKey | string | 是   | apiKey |

返回 data 为税款所属期字符串，如 `"2026-05"`。

### 6. 申请或撤销统计 — POST /api/jxplus/zxtSkill/check/commitStatistics

| 参数       | 类型   | 必填 | 说明                                             |
| ---------- | ------ | ---- | ------------------------------------------------ |
| apiKey     | string | 是   | apiKey                                           |
| commitType | string | 是   | 1 申请统计，2 撤销统计                           |
| bz         | string | 是   | N 忽略未勾选发票直接统计，Y 取消未完成的统计状态 |

### 7. 查询抵扣统计数据 — POST /api/jxplus/zxtSkill/check/getDeductStatistList

| 参数   | 类型   | 必填 | 说明                         |
| ------ | ------ | ---- | ---------------------------- |
| apiKey | string | 是   | apiKey                       |
| skssq  | string | 否   | 税款所属期，不填默认当前属期 |

### 8. 查询当前属期认证发票集合 — POST /api/jxplus/zxtSkill/check/getCheckedInvoiceList

| 参数   | 类型   | 必填 | 说明                             |
| ------ | ------ | ---- | -------------------------------- |
| apiKey | string | 是   | apiKey                           |
| skssq  | string | 否   | 税款所属期，不填默认当前属期     |

### 9. 查询发票认证状态 — POST /api/jxplus/zxtSkill/check/getInvoiceCheckStatus

| 参数          | 类型   | 必填 | 说明                   |
| ------------- | ------ | ---- | ---------------------- |
| apiKey        | string | 是   | apiKey                 |
| invoiceNumber | string | 是   | 发票号码               |
| invoiceDate   | string | 是   | 开票日期（YYYY-MM-DD） |
| invoiceCode   | string | 否   | 发票代码               |

### 10. 提交或取消认证 — POST /api/jxplus/zxtSkill/check/commitDeduction

| 参数       | 类型   | 必填 | 说明                                              |
| ---------- | ------ | ---- | ------------------------------------------------- |
| apiKey     | string | 是   | apiKey                                            |
| commitType | string | 是   | 1 勾选认证，2 取消勾选认证                        |
| skssq      | string | 否   | 税款所属期，不填默认当前属期                      |
| list       | array  | 是   | 发票列表，每条含 invoiceCode、kprq、invoiceNumber |

## 返回说明

### 登录返回 (login)

| 字段        | 类型   | 说明                                                      |
| ----------- | ------ | --------------------------------------------------------- |
| returnType  | string | 4000 直接登录成功，4001 需验证码，4002 需设置地区         |
| loginMobile | string | 带\*手机号（returnType=4001 时返回）                      |
| areaList    | array  | 地区列表（returnType=4002 时返回），含 areaCode、areaName |

### 认证发票返回 (checked-invoices)

| 字段          | 说明         |
| ------------- | ------------ |
| invoiceCode   | 发票代码     |
| invoiceNumber | 发票号码     |
| qdfphm        | 全电发票号码 |
| kprq          | 开票日期     |
| hjje          | 合计金额     |
| hjse          | 合计税额     |
| jshj          | 价税合计     |
| fplx          | 发票类型     |
| fplxName      | 发票类型名称 |
| xsfNsrsbh     | 销售方税号   |
| xsfMc         | 销售方名称   |

### 认证状态返回 (check-status)

| 字段          | 说明                         |
| ------------- | ---------------------------- |
| invoiceCode   | 发票代码                     |
| invoiceNumber | 发票号码                     |
| kprq          | 开票日期                     |
| hjje          | 合计金额                     |
| hjse          | 合计税额                     |
| gxzt          | 勾选状态：0 未勾选，1 已勾选 |
| skssq         | 认证属期                     |

### 提交认证返回 (commit-deduction)

| 字段         | 说明           |
| ------------ | -------------- |
| successCount | 成功数量       |
| failCount    | 失败数量       |
| successList  | 成功集合       |
| failLIst     | 失败集合       |
| skssq        | 当前税款所属期 |

## 异常状态码

| 状态码 | 说明                     |
| ------ | ------------------------ |
| 400    | 请求参数错误             |
| 300    | 参数为空或格式错误       |
| 305    | 无权访问该接口           |
| 307    | 消费失败，授权余次不足   |
| 308    | 超出接口调用次数         |
| 309    | 税局未登录，需先登录税局 |
| 500    | 系统异常                 |

## 命令示例

税局登录：

```bash
python .claude/skills/invoice-cert/invoice_cert.py login --credit-code "911101087582285868" --account "account" --password "password"
```

发送验证码：

```bash
python .claude/skills/invoice-cert/invoice_cert.py send-sms --credit-code "911101087582285868" --account "account"
```

验证码登录：

```bash
python .claude/skills/invoice-cert/invoice_cert.py login-sms --sms-code "123456" --credit-code "911101087582285868" --account "account"
```

确认签名：

```bash
python .claude/skills/invoice-cert/invoice_cert.py sign
```

查询当前税款所属期：

```bash
python .claude/skills/invoice-cert/invoice_cert.py current-period
```

查询发票认证状态：

```bash
python .claude/skills/invoice-cert/invoice_cert.py check-status --invoice-number "26127000000211930033" --invoice-date "2026-05-12"
```

查询当前属期认证发票：

```bash
python .claude/skills/invoice-cert/invoice_cert.py checked-invoices
```

查询指定属期认证发票（历史记录）：

```bash
python .claude/skills/invoice-cert/invoice_cert.py checked-invoices --skssq "202604"
```

提交勾选认证（单张）：

```bash
python .claude/skills/invoice-cert/invoice_cert.py commit-deduction --commit-type "1" --invoices "011002000311,2026-05-12,26127000000211930033"
```

提交勾选认证（多张，自动按开票日期排序，每批最多 50 张）：

```bash
python .claude/skills/invoice-cert/invoice_cert.py commit-deduction --commit-type "1" --invoices "011002000311,2026-05-10,26127000000211930033" "011002000311,2026-05-12,26127000000211930034" "011002000311,2026-05-08,26127000000211930035"
```

申请统计：

```bash
python .claude/skills/invoice-cert/invoice_cert.py statistics --commit-type "1" --bz "N"
```

查询抵扣统计：

```bash
python .claude/skills/invoice-cert/invoice_cert.py deduct-stats
```
