---
name: invoice-verify
description: 发票查验技能。按票面信息或上传文件查验发票真伪，返回完整票面信息。适用于验证发票真实性的场景。
---

# 发票查验技能

使用此技能通过票面信息或上传发票文件查验发票真伪，获取完整票面明细。

## 使用场景

满足以下需求时使用：

- 根据发票号码、开票日期、金额/校验码查验发票真伪。
- 上传发票文件（pdf/ofd/xml/jpg/png）进行批量查验。
- 查询查验记录，按日期范围、发票号码、发票类型等条件筛选。

## 触发语句示例

以下用户输入应触发此技能：

- 帮我查验这张发票 / 发票查验 / 查验发票
- 验证发票真伪 / 发票验真 / 验真
- 查一下这张发票是不是真的
- 上传发票文件查验 / 文件查验
- 这个发票文件帮我验一下
- 查验发票 26127000000211930033
- 查看一下查验记录 / 查验记录 / 查验历史
- 查一下5月份的查验记录
- 有没有查验失败的发票
- 查验状态不一致的发票有哪些

## 输入参数

执行前准备以下参数：

- apiKey（必填）：通过 https://skill.quandianfapiao.com/ 申请。

### 按票面查验 (inspect)

- 发票号码（必填）
- 开票日期（必填，格式 YYYY-MM-DD）
- 金额或校验码（必填，根据发票种类不同传入金额或校验码）
- 发票代码（可选）

### 按文件查验 (file)

- 发票文件路径（必填，支持 pdf、ofd、xml、jpg、png）

### 查询查验记录 (record)

- 开票日期开始（选填，格式 YYYY-MM-DD）
- 开票日期结束（选填，格式 YYYY-MM-DD）
- 发票号码（选填）
- 发票代码（选填）
- 发票类型（选填，可多选，传入编码值，详见下方 fplx 枚举）
- 页码（选填，默认 1）
- 每页条数（选填，默认 10）
- 查验时间开始（选填，格式 YYYY-MM-DD）
- 查验时间结束（选填，格式 YYYY-MM-DD）

#### fplx 发票类型枚举

| 票据大类               | 票据小类                           | 编码 |
| ---------------------- | ---------------------------------- | ---- |
| 增值税发票管理系统发票 | 增值税专用发票                     | 01   |
|                        | 货物运输业增值税专用发票           | 02   |
|                        | 机动车销售统一发票                 | 03   |
|                        | 增值税普通发票                     | 04   |
|                        | 增值税电子专用发票                 | 08   |
|                        | 增值税电子普通发票                 | 10   |
|                        | 增值税普通发票（卷票）             | 11   |
|                        | 二手车销售统一发票                 | 15   |
|                        | 道路通行费电子普通发票             | 14   |
| 电子发票服务平台       | 电子发票（增值税专用发票）         | 81   |
|                        | 电子发票（普通发票）               | 82   |
|                        | 电子发票（铁路电子客票）           | 51   |
|                        | 电子发票（航空运输电子客票行程单） | 61   |
|                        | 机动车销售电子统一发票             | 73   |
|                        | 电子发票（机动车销售统一发票）     | 83   |
|                        | 二手车销售电子统一发票             | 84   |
|                        | 纸质发票（增值税专用发票）         | 85   |
|                        | 纸质发票（普通发票）               | 86   |
|                        | 纸质发票（机动车销售统一发票）     | 87   |
|                        | 纸质发票（二手车销售统一发票）     | 88   |
|                        | 数电票（通行费发票）               | 59   |
| 地方通用发票           | 浙江通用（电子）发票               | Z1   |
|                        | 云南省通用电子发票                 | Y1   |
|                        | 广东通用机打发票（电子）           | G1   |
|                        | 北京电子普通发票                   | B1   |
|                        | 深圳电子普通发票                   | S1   |
|                        | 通用定额发票                       | TY   |
|                        | 江苏省车辆通行费通用（电子）发票   | J1   |
| 交通运输发票           | 出租车发票                         | CZ   |
|                        | 汽车票                             | QC   |
|                        | 轮船票                             | LC   |
|                        | 过路过桥费发票                     | GL   |
|                        | 火车票                             | HC   |
|                        | 机票行程单                         | JX   |
| 其他发票               | 其他发票                           | QT   |
| 财政票据               | 财政票据                           | CP   |
| 海关缴款书             | 海关缴款书                         | 17   |

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
   - 缺少发票号码、开票日期或金额/校验码：停止并提示用户提供对应参数。
   - 按文件查验时文件不存在或不支持该文件类型：停止并提示用户。
2. 通过 python 执行脚本调用远程 API（Windows 下使用 `python`，macOS/Linux 使用 `python3`），脚本优先使用 `--api-key` 参数，未传则回退读取环境变量 `ZXT_API_KEY`。
3. 检查返回的 status 字段，非 200 时停止并将错误信息展示给用户，禁止重试或忽略。
4. 解析返回结果并以可读格式输出。

## 请求参数说明

### 按票面查验 — POST /api/jxplus/zxtSkill/inspection/queryInspectionInvoice

| 参数          | 类型   | 必填 | 说明                                                        |
| ------------- | ------ | ---- | ----------------------------------------------------------- |
| apiKey        | string | 是   | apiKey                                                      |
| invoiceNumber | string | 是   | 发票号码                                                    |
| invoiceDate   | string | 是   | 开票日期（YYYY-MM-DD）                                      |
| jejym         | string | 是   | 金额或校验码，根据发票种类不同传入，详见下方 jejym 传入规则 |
| invoiceCode   | string | 否   | 发票代码                                                    |

### jejym 传入规则

不同发票类型的 jejym 入参不同：

| 发票类型                       | jejym 入参         |
| ------------------------------ | ------------------ |
| 增值税专用发票                 | 开具金额（不含税） |
| 机动车销售统一发票             | 不含税价           |
| 二手车销售统一发票             | 车价合计           |
| 增值税电子专用发票             | 开具金额（不含税） |
| 电子发票（增值税专用发票）     | 价税合计           |
| 电子发票（普通发票）           | 价税合计           |
| 增值税普通发票                 | 校验码后六位       |
| 增值税普通发票（卷票）         | 校验码后六位       |
| 增值税电子普通发票             | 校验码后六位       |
| 道路通行费电子普通发票         | 校验码后六位       |
| 铁路电子客票                   | 价税合计           |
| 航空运输电子客票行程单         | 价税合计           |
| 电子发票（机动车销售统一发票） | 价税合计           |
| 电子发票（通行费发票）         | 价税合计           |

### 按文件查验 — POST /api/jxplus/zxtSkill/inspection/queryInspectionFile

请求头：`Content-Type: multipart/form-data`

| 参数   | 类型   | 必填 | 说明                            |
| ------ | ------ | ---- | ------------------------------- |
| apiKey | string | 是   | apiKey                          |
| file   | file   | 是   | 发票文件（pdf/ofd/xml/jpg/png） |

### 查询查验记录 — POST /api/jxplus/zxtSkill/inspection/queryInspectionRecord

| 参数          | 类型     | 必填 | 说明                      |
| ------------- | -------- | ---- | ------------------------- |
| apiKey        | string   | 是   | apiKey                    |
| kprqStart     | string   | 否   | 开票日期开始 (YYYY-MM-DD) |
| kprqEnd       | string   | 否   | 开票日期结束 (YYYY-MM-DD) |
| invoiceNumber | string   | 否   | 发票号码                  |
| invoiceCode   | string   | 否   | 发票代码                  |
| fplxList      | string[] | 否   | 发票类型集合              |
| pageNo        | string   | 否   | 页码，默认 1              |
| pageSize      | string   | 否   | 每页条数，默认 10         |
| cysjStart     | string   | 否   | 查验时间开始 (YYYY-MM-DD) |
| cysjEnd       | string   | 否   | 查验时间结束 (YYYY-MM-DD) |

## 返回说明

按票面查验和按文件查验共享相同的返回数据结构。按文件查验返回集合，集合内每条记录结构与按票面查验一致。

### 查验记录返回 (record)

返回分页列表，每条记录包含：

| 字段          | 说明                                                                                                     |
| ------------- | -------------------------------------------------------------------------------------------------------- |
| invoiceNumber | 发票号码                                                                                                 |
| invoiceCode   | 发票代码                                                                                                 |
| fplx          | 发票类型                                                                                                 |
| fplxName      | 发票类型名称                                                                                             |
| kprq          | 开票日期                                                                                                 |
| jshj          | 价税合计                                                                                                 |
| cyzt          | 查验状态：0 未查验，1 查验中，2 查验真票，3 查无此票，4 查询不一致，5 查验失败，6 不支持查验，7 抬头不符 |
| cyztName      | 查验状态名称                                                                                             |
| cysj          | 查验时间                                                                                                 |
| xsfMc         | 销售方名称                                                                                               |

### 外层返回字段

| 字段    | 类型   | 说明                             |
| ------- | ------ | -------------------------------- |
| status  | string | 返回接口状态码                   |
| message | string | 返回接口状态描述信息             |
| data    | object | 业务数据体（按文件查验时为数组） |

### data 业务数据体

| 字段           | 类型    | 说明                                                 |
| -------------- | ------- | ---------------------------------------------------- |
| invoiceType    | string  | 发票种类，详见发票类型说明                           |
| invoiceCode    | string  | 发票代码                                             |
| invoiceNumber  | string  | 发票号码                                             |
| invoiceDate    | string  | 开票日期                                             |
| hjje           | decimal | 合计金额                                             |
| hjse           | decimal | 合计税额                                             |
| jshj           | decimal | 价税合计                                             |
| fpStatus       | string  | 发票状态：0 正常，2 作废，3 红冲                     |
| xsfMc          | string  | 销售方名称                                           |
| xsfNsrsbh      | string  | 销售方纳税人识别号                                   |
| xsfAddressTel  | string  | 销售方地址、电话                                     |
| xsfBankAccount | string  | 销售方开户行及账号                                   |
| gmfMc          | string  | 购买方名称                                           |
| gmfNsrsbh      | string  | 购买方税号                                           |
| gmfAddressTel  | string  | 购买方地址、电话                                     |
| gmfBankAccount | string  | 购买方开户行及账号                                   |
| payee          | string  | 收款人                                               |
| reviewer       | string  | 复核人                                               |
| invoicer       | string  | 开票人                                               |
| machineNo      | string  | 机器编号                                             |
| checkCode      | string  | 校验码                                               |
| passwordArea   | string  | 密码区                                               |
| remark         | string  | 备注                                                 |
| xmlFileUrl     | string  | xml 文件地址                                         |
| pdfFileUrl     | string  | pdf 文件地址                                         |
| ofdFileUrl     | string  | ofd 文件地址                                         |
| items          | List    | 发票明细                                             |
| specialDetail  | List    | 特殊票种明细（铁路电子客票、航空运输电子客票行程单） |

### items 明细数据体

#### 商品详情列表（其他类型发票）

| 字段           | 类型   | 说明                     |
| -------------- | ------ | ------------------------ |
| projectName    | string | 货物或应税劳务、服务名称 |
| ggxh           | string | 规格型号                 |
| projectUnit    | string | 单位                     |
| projectCount   | string | 数量                     |
| projectPriceEt | string | 单价                     |
| projectJeEt    | string | 金额                     |
| sl             | string | 税率                     |
| se             | string | 税额                     |

#### 二手车详情列表（15 二手车发票）

| 字段    | 类型   | 说明                         |
| ------- | ------ | ---------------------------- |
| cpzh    | string | 车牌照号                     |
| djzh    | string | 登记证号                     |
| cllx    | string | 车辆类型                     |
| cjh     | string | 车架号/车辆识别号            |
| cpxh    | string | 厂牌型号                     |
| glsMc   | string | 转入地车辆管理所名称         |
| jyDw    | string | 经营、拍卖单位               |
| jyDz    | string | 经营、拍卖单位地址           |
| jySh    | string | 经营、拍卖单位税号           |
| jyYh    | string | 经营、拍卖单位开户银行、账号 |
| jyDh    | string | 经营、拍卖单位电话           |
| escsc   | string | 二手车市场                   |
| escscSh | string | 二手车市场税号               |
| escscDz | string | 二手车市场地址               |
| escscYh | string | 二手车市场开户银行、账号     |
| escscDh | string | 二手车市场电话               |

#### 通行费详情列表（14 道路通行费 & 59 电子发票通行费）

| 字段        | 类型   | 说明     |
| ----------- | ------ | -------- |
| projectName | string | 项目名称 |
| carNumber   | string | 车牌号   |
| type        | string | 类型     |
| beginDate   | string | 通行日起 |
| endDate     | string | 通行日止 |
| projectJeEt | string | 金额     |
| sl          | string | 税率     |
| se          | string | 税额     |

#### 机动车详情列表（03 机动车发票 & 83 电子发票机动车）

| 字段     | 类型   | 说明                  |
| -------- | ------ | --------------------- |
| hgzh     | string | 合格证号              |
| jkzmsh   | string | 进口证明书号          |
| sjdh     | string | 商检单号              |
| fdjhm    | string | 发动机号码            |
| clsbh    | string | 车辆识别代号/车架号码 |
| zzssl    | string | 增值税税率或征收率    |
| zzsse    | string | 增值税税额            |
| zgswjg   | string | 主管税务机关          |
| zgswjgdm | string | 主管税务机关代码      |
| bhsj     | string | 不含税价              |
| wspzhm   | string | 完税凭证号码          |
| dw       | string | 吨位                  |
| xccr     | string | 限乘人数              |
| dz       | string | 地址                  |
| dh       | string | 电话                  |
| khyh     | string | 开户银行              |
| zh       | string | 账号                  |

### specialDetail 特殊票种明细数据体

#### 铁路电子客票详情列表（51 铁路电子客票）

| 字段                  | 类型   | 说明         |
| --------------------- | ------ | ------------ |
| nameOfPassenger       | string | 旅客姓名     |
| departureTime         | string | 出发时间     |
| fare                  | string | 票价         |
| promptInformationArea | string | 提示信息     |
| seat                  | string | 座位         |
| travelDate            | string | 乘车日期     |
| passengerIdNumber     | string | 身份证号码   |
| departureStation      | string | 出发地       |
| trainNumber           | string | 车次         |
| destinationStation    | string | 目的地       |
| eticketNumber         | string | 电子客票号码 |
| seatLevel             | string | 座位等级     |

#### 航空运输电子客票行程单详情列表（61 航空运输电子客票行程单）

| 字段                             | 类型   | 说明         |
| -------------------------------- | ------ | ------------ |
| nameOfPassenger                  | string | 旅客姓名     |
| issuingStatus                    | string | 填开状态     |
| departureStation                 | string | 出发地       |
| firstDestinationStation          | string | 第一站       |
| secondDestinationStation         | string | 第二站       |
| thirdDestinationStation          | string | 第三站       |
| fourthDestinationStation         | string | 第四站       |
| totalAmount                      | string | 合计         |
| markingOfDomesticOrInternational | string | 国内国际标识 |
| gpoddnumbers                     | string | GP 单号      |
| eticketNumber                    | string | 电子客票号码 |
| itineraryDetail                  | List   | 行程明细     |

#### itineraryDetail 行程明细数据体

| 字段          | 类型   | 说明              |
| ------------- | ------ | ----------------- |
| departureTime | string | 出发时间          |
| flight        | string | 航班号            |
| carrier       | string | 承运人            |
| level         | string | 座位等级          |
| carrierDate   | string | 承运日期          |
| fareBasis     | string | 客票级别/客票类别 |

## 异常状态码

| 状态码 | 说明                   |
| ------ | ---------------------- |
| 400    | 请求参数错误           |
| 300    | 参数为空或格式错误     |
| 305    | 无权访问该接口         |
| 307    | 消费失败，授权余次不足 |
| 308    | 超出接口调用次数       |
| 500    | 系统异常               |

## 接口请求示例

### 按票面查验 — POST /api/jxplus/zxtSkill/inspection/queryInspectionInvoice

请求：

```json
{
  "data": {
    "apiKey": "sk-sg-9EVbsJLJnlKVLaSO4FZtPUVFysbFL",
    "invoiceNumber": "26127000000211930033",
    "invoiceDate": "2026-05-12",
    "jejym": "162.43"
  }
}
```

成功返回：

```json
{
  "status": "200",
  "message": "成功",
  "data": {
    "invoiceType": "82",
    "invoiceCode": "",
    "invoiceNumber": "26127000000211930033",
    "invoiceDate": "2026-05-12",
    "hjje": "146.33",
    "hjse": "16.10",
    "jshj": "162.43",
    "fpStatus": "0",
    "xsfMc": "天津象鲜科技有限公司",
    "xsfNsrsbh": "91120101MADQKPT067",
    "xsfAddressTel": "天津市和平区南市街道张自忠路与多伦道交口合生国际大厦1号楼1-L7-101 021-52559777",
    "xsfBankAccount": "招商银行股份有限公司天津滨海分行营业部 122917783510000",
    "gmfMc": "北京中兴通融资产管理股份有限公司",
    "gmfNsrsbh": "911101087582285868",
    "gmfAddressTel": "",
    "gmfBankAccount": "",
    "items": [
      {
        "projectName": "*水果*水果",
        "ggxh": "/",
        "projectUnit": "件",
        "projectCount": "4",
        "projectPriceEt": "18.4850000000",
        "projectJeEt": "73.94",
        "sl": "0.090",
        "se": "6.66"
      },
      {
        "projectName": "*纸制品*纸制品",
        "ggxh": "/",
        "projectUnit": "件",
        "projectCount": "1",
        "projectPriceEt": "16.7300000000",
        "projectJeEt": "16.73",
        "sl": "0.130",
        "se": "2.17"
      }
    ]
  }
}
```

异常返回：

```json
{
  "status": "400",
  "message": "金额/校验码不能为空",
  "data": ""
}
```

### 按文件查验 — POST /api/jxplus/zxtSkill/inspection/queryInspectionFile

请求方式：`multipart/form-data`，包含 `apiKey` 字段和 `file` 文件字段。

返回值：集合，集合内结构与按票面查验一致。

## 命令示例

按票面查验：

```bash
python .claude/skills/invoice-verify/invoice_verify.py inspect --invoice-number "26127000000211930033" --invoice-date "2026-05-12" --jejym "162.43"
```

按文件查验：

```bash
python .claude/skills/invoice-verify/invoice_verify.py file --file "E:\\invoices\\test.pdf"
```

查询查验记录（按日期范围）：

```bash
python .claude/skills/invoice-verify/invoice_verify.py record --kprq-start "2026-05-01" --kprq-end "2026-05-31"
```

查询查验记录（按发票号码）：

```bash
python .claude/skills/invoice-verify/invoice_verify.py record --invoice-number "26127000000211930033"
```

查询查验记录（按发票类型筛选，可多选）：

```bash
python .claude/skills/invoice-verify/invoice_verify.py record --kprq-start "2026-05-01" --kprq-end "2026-05-31" --fplx 82 81
```
