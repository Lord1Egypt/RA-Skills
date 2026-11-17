---
name: invoice-cert
description: 发票认证技能。税局扫码登录、登录企业查询、发票勾选认证、抵扣统计。适用于进项发票勾选、认证、统计等税务操作场景。
---

# 发票认证技能

使用此技能进行税局扫码登录、登录企业查询、发票勾选认证、查询认证状态、申请抵扣统计等操作。

## 使用场景

满足以下需求时使用：

- 扫码登录税局系统（电子税务局）。
- 查询当前登录的企业信息（企业名称、纳税人识别号）。
- 查询发票的勾选认证状态。
- 提交或取消发票勾选认证。
- 申请或撤销抵扣统计。
- 查询抵扣统计数据。
- 查询当前属期已认证的发票集合。
- 查询当前税款所属期。
- 确认签名。

## 触发语句示例

以下用户输入应触发此技能：

- 帮我登录税局 / 税局登录 / 扫码登录 / 登录电子税务局
- 现在登录的是哪个企业 / 查询企业信息 / 当前企业
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

### 扫码登录 (login-qr)

无额外参数。获取税局登录二维码并在终端展示，用户使用微信扫码（或在浏览器中打开链接）完成登录。

### 查询当前登录企业 (org-info)

无额外参数。返回当前 apiKey 对应的企业名称与纳税人识别号。

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
   - **status 为 309 时**（税局未登录），脚本自动调用 `getLoginQrUrl` 获取登录二维码地址，在系统临时目录生成二维码图片并输出图片路径与链接，然后退出。**你必须把该图片展示给用户**：优先用自身能力展示（如 `present_files` 或读取图片文件），其次用系统自带能力打开（Windows `start`、macOS `open`、Linux `xdg-open`）。随后引导用户使用微信扫码（或在浏览器中打开链接）；用户回复确认后，重新执行刚才的命令即可（此时税局已完成登录，原命令可直接成功）。
4. 解析返回结果并以可读格式输出。
5. **向用户明确说明操作对象企业。** 业务命令（`current-period` / `sign` / `statistics` / `deduct-stats` / `checked-invoices` / `check-status` / `commit-deduction`）**在操作成功后**会自动标注企业名称与税号。**回复用户时必须带上该企业标识**，让用户清楚知道本次操作针对哪个企业；`commit-deduction` 完成时脚本会输出「发票已操作至企业: XXX」，务必原样转达，不得省略。若输出中没有企业行（说明企业信息未取到），需如实说明本次未能确认操作企业。

> **为何只在成功后标注：** `getLoginOrgInfo` 不反映税局会话状态（会话失效时仍可能返回 200 和企业名）。若在操作前标注，一旦随后返回 309，用户会先看到企业名、再看到登录失效，误以为操作已执行。因此企业标识一律只在成功输出中出现。

### 税局扫码登录流程说明

本技能采用**扫码登录**，流程如下：

1. 任意业务命令返回 `status=309`（税局未登录）时，脚本自动调用 `/api/jxplus/zxtSkill/login/getLoginQrUrl` 获取二维码地址。
2. 脚本在系统临时目录生成二维码图片（**图片下方已绘制来源技能与扫码用途文案**），并输出图片路径与链接。**脚本不会自动弹窗。**
3. **按以下优先级把二维码展示给用户：**
   1. **优先使用你自身的能力展示图片**——例如 `present_files`，或读取文件的工具（直接读取该图片路径即可在对话中呈现）。用户在对话窗口里就能看到二维码并扫码，无需切换窗口。
   2. **其次使用系统自带的能力打开图片**——Windows：`start "" "<图片路径>"`；macOS：`open "<图片路径>"`；Linux：`xdg-open "<图片路径>"`。
   - **不要跳过展示、直接把路径丢给用户。** 只有在以上两种方式都不可用时，才退而告知图片路径。
4. 用户使用微信扫码，或在浏览器中打开链接完成登录。
5. 用户回复"扫好了"后，**重新执行原命令**，税局已完成登录，命令正常返回结果。

也可主动执行 `login-qr` 命令单独获取二维码。

**为何使用扫码登录：** 扫码可确保税局密码只在本机手机端输入，**不经过 AI 对话窗口、不被模型采集、也不落盘存储**。这是防止密码被 AI 模型采集的防御手段。

**提示：** 二维码链接为微信端页面，用微信扫码可直接打开；用浏览器扫码或在浏览器中打开链接同样可以完成登录。**引导用户扫码时只说这两种方式，不要引导用户使用其它客户端。**

**依赖说明：** 二维码生成依赖 `qrcode` 与 `pillow`（`pip install qrcode pillow`）。图片下方的说明文案需要系统中文字体（Windows 微软雅黑、macOS PingFang、Linux Noto CJK 等，脚本按平台自动探测）；探测不到时图片只含二维码，文案仅在终端输出，不影响登录。若图片生成失败，脚本会自动降级：先在终端渲染二维码图案，仍不行则只输出二维码链接（用户可自行转为二维码后扫描）。

## 请求参数说明

### 1. 获取税局登录二维码 — POST /api/jxplus/zxtSkill/login/getLoginQrUrl

| 参数   | 类型   | 必填 | 说明   |
| ------ | ------ | ---- | ------ |
| apiKey | string | 是   | apiKey |

返回 `data.qrUrl` 为税局登录二维码地址。

### 2. 查询当前登录企业 — POST /api/jxplus/zxtSkill/dzsj/getLoginOrgInfo

| 参数   | 类型   | 必填 | 说明   |
| ------ | ------ | ---- | ------ |
| apiKey | string | 是   | apiKey |

返回 `data.orgName` 为企业名称，`data.nsrsbh` 为纳税人识别号。

> **重要限制：** 该接口返回的是 apiKey 在平台上绑定的企业，**不反映税局会话是否有效**。实测税局会话失效（其它接口返回 309）时，本接口仍会返回 200 和企业名称。因此它**只能用于标注操作对象，不能用于判断登录状态**——登录状态一律以业务接口的 309 为准。

### 3. 确认签名 — POST /api/jxplus/zxtSkill/check/doSignature

| 参数   | 类型   | 必填 | 说明   |
| ------ | ------ | ---- | ------ |
| apiKey | string | 是   | apiKey |

### 4. 查询当前税款所属期 — POST /api/jxplus/zxtSkill/check/getCurrSkssq

| 参数   | 类型   | 必填 | 说明   |
| ------ | ------ | ---- | ------ |
| apiKey | string | 是   | apiKey |

返回 data 为税款所属期字符串，如 `"2026-05"`。

### 5. 申请或撤销统计 — POST /api/jxplus/zxtSkill/check/commitStatistics

| 参数       | 类型   | 必填 | 说明                                             |
| ---------- | ------ | ---- | ------------------------------------------------ |
| apiKey     | string | 是   | apiKey                                           |
| commitType | string | 是   | 1 申请统计，2 撤销统计                           |
| bz         | string | 是   | N 忽略未勾选发票直接统计，Y 取消未完成的统计状态 |

### 6. 查询抵扣统计数据 — POST /api/jxplus/zxtSkill/check/getDeductStatistList

| 参数   | 类型   | 必填 | 说明                         |
| ------ | ------ | ---- | ---------------------------- |
| apiKey | string | 是   | apiKey                       |
| skssq  | string | 否   | 税款所属期，不填默认当前属期 |

### 7. 查询当前属期认证发票集合 — POST /api/jxplus/zxtSkill/check/getCheckedInvoiceList

| 参数   | 类型   | 必填 | 说明                             |
| ------ | ------ | ---- | -------------------------------- |
| apiKey | string | 是   | apiKey                           |
| skssq  | string | 否   | 税款所属期，不填默认当前属期     |

### 8. 查询发票认证状态 — POST /api/jxplus/zxtSkill/check/getInvoiceCheckStatus

| 参数          | 类型   | 必填 | 说明                   |
| ------------- | ------ | ---- | ---------------------- |
| apiKey        | string | 是   | apiKey                 |
| invoiceNumber | string | 是   | 发票号码               |
| invoiceDate   | string | 是   | 开票日期（YYYY-MM-DD） |
| invoiceCode   | string | 否   | 发票代码               |

### 9. 提交或取消认证 — POST /api/jxplus/zxtSkill/check/commitDeduction

| 参数       | 类型   | 必填 | 说明                                              |
| ---------- | ------ | ---- | ------------------------------------------------- |
| apiKey     | string | 是   | apiKey                                            |
| commitType | string | 是   | 1 勾选认证，2 取消勾选认证                        |
| skssq      | string | 否   | 税款所属期，不填默认当前属期                      |
| list       | array  | 是   | 发票列表，每条含 invoiceCode、kprq、invoiceNumber |

## 返回说明

### 登录企业返回 (org-info)

| 字段    | 说明           |
| ------- | -------------- |
| orgName | 企业名称       |
| nsrsbh  | 纳税人识别号   |

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

| 状态码 | 说明                                |
| ------ | ----------------------------------- |
| 400    | 请求参数错误                        |
| 300    | 参数为空或格式错误                  |
| 305    | 无权访问该接口                      |
| 307    | 消费失败，授权余次不足              |
| 308    | 超出接口调用次数                    |
| 309    | 税局未登录，脚本自动展示扫码登录二维码 |
| 500    | 系统异常                            |

## 命令示例

获取税局扫码登录二维码：

```bash
python .claude/skills/invoice-cert/invoice_cert.py login-qr
```

查询当前登录企业：

```bash
python .claude/skills/invoice-cert/invoice_cert.py org-info
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
