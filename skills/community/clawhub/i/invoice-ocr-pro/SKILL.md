---
name: invoice-ocr
description: 发票识别技能。上传发票文件进行 OCR 识别，返回发票票面信息。适用于从发票图片或文件中提取结构化数据的场景。
---

# 发票识别技能

使用此技能通过上传发票文件进行 OCR 识别，自动提取发票票面结构化信息。

## 使用场景

满足以下需求时使用：

- 上传发票图片或文件（PDF/OFD/JPEG/JPG/PNG/XML）进行 OCR 识别。
- 从发票图片中提取发票号码、金额、销购方等结构化信息。
- 批量处理发票文件的自动识别。

## 触发语句示例

以下用户输入应触发此技能：

- 帮我识别这张发票 / 发票识别 / 识别发票
- 这张发票里有什么信息
- 提取发票信息 / 发票 OCR
- 读取发票内容
- 这个发票文件帮我识别一下
- 识别发票文件

## 输入参数

执行前准备以下参数：

- apiKey（必填）：通过 https://skill.quandianfapiao.com/ 申请。

### 发票识别 (ocr)

- 发票文件路径（必填，支持 PDF、OFD、JPEG、JPG、PNG、XML）

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
   - 缺少发票文件路径：停止并提示用户提供文件。
   - 文件不存在或不支持该文件类型：停止并提示用户。
2. 通过 python 执行脚本调用远程 API（Windows 下使用 `python`，macOS/Linux 使用 `python3`），脚本优先使用 `--api-key` 参数，未传则回退读取环境变量 `ZXT_API_KEY`。
3. 检查返回的 status 字段，非 200 时停止并将错误信息展示给用户，禁止重试或忽略。
4. 解析返回结果并以可读格式输出。

## 请求参数说明

### 发票识别 — POST /api/jxplus/zxtSkill/discern/invoiceDiscern

请求头：`Content-Type: multipart/form-data`

| 参数   | 类型   | 必填 | 说明                             |
| ------ | ------ | ---- | -------------------------------- |
| apiKey | string | 是   | apiKey                           |
| file   | file   | 是   | 发票文件（pdf/ofd/jpeg/jpg/png/xml） |

## 返回说明

### 外层返回字段

| 字段    | 类型   | 说明                 |
| ------- | ------ | -------------------- |
| status  | string | 返回接口状态码       |
| message | string | 返回接口状态描述信息 |
| data    | object | 业务数据体           |

### data 业务数据体

| 字段           | 类型   | 说明               |
| -------------- | ------ | ------------------ |
| invoiceType    | string | 发票种类           |
| invoiceCode    | string | 发票代码           |
| invoiceNumber  | string | 发票号码           |
| invoiceDate    | string | 开票日期           |
| hjje           | string | 合计金额           |
| hjse           | string | 合计税额           |
| jshj           | string | 价税合计           |
| xsfMc          | string | 销售方名称         |
| xsfNsrsbh      | string | 销售方纳税人识别号 |
| xsfAddressTel  | string | 销售方地址、电话   |
| xsfBankAccount | string | 销售方开户行及账号 |
| gmfMc          | string | 购买方名称         |
| gmfNsrsbh      | string | 购买方税号         |
| gmfAddressTel  | string | 购买方地址、电话   |
| gmfBankAccount | string | 购买方开户行及账号 |
| payee          | string | 收款人             |
| reviewer       | string | 复核人             |
| invoicer       | string | 开票人             |
| machineNo      | string | 机器编号           |
| checkCode      | string | 校验码             |
| passwordArea   | string | 密码区             |
| remark         | string | 备注               |
| item           | List   | 发票明细列表       |
| otherInfo      | string | 其他信息           |

### item 明细数据体

| 字段           | 类型   | 说明     |
| -------------- | ------ | -------- |
| projectName    | string | 项目名称 |
| ggxh           | string | 规格型号 |
| projectUnit    | string | 单位     |
| projectCount   | string | 数量     |
| projectPriceEt | string | 单价     |
| projectJeEt    | string | 金额     |
| sl             | string | 税率     |
| se             | string | 税额     |

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

### 发票识别 — POST /api/jxplus/zxtSkill/discern/invoiceDiscern

请求方式：`multipart/form-data`，包含 `apiKey` 字段和 `file` 文件字段。

成功返回：

```json
{
  "status": "200",
  "message": "成功",
  "data": {
    "invoiceType": "82",
    "invoiceCode": "数电票",
    "invoiceNumber": "23622000000012981281",
    "invoiceDate": "2023-10-18",
    "hjje": "34.65",
    "hjse": "0.35",
    "jshj": "35.00",
    "xsfMc": "金昌市安行征途汽车运输有限公司",
    "xsfNsrsbh": "91620302MA71XY3022",
    "xsfAddressTel": "",
    "xsfBankAccount": "",
    "gmfMc": "北京中兴通融资产管理股份有限公司",
    "gmfNsrsbh": "911101087582285868",
    "gmfAddressTel": "",
    "gmfBankAccount": "",
    "payee": null,
    "reviewer": null,
    "invoicer": "张玉芳",
    "machineNo": null,
    "checkCode": "23622000000012981281",
    "passwordArea": null,
    "remark": "车人1 00****00 2023-10-16 武威- 金川机场- 长途汽车\n价税合计（大写） 叁拾伍圆整 （小写）¥35.00\n线路：武威-金川机场日期：2023-10-1608:30\n",
    "otherInfo": null,
    "item": [
      {
        "projectName": "*运输服务*客运服务",
        "ggxh": null,
        "projectUnit": null,
        "projectCount": "34.65",
        "projectPriceEt": "1",
        "projectJeEt": "34.65",
        "sl": "1%",
        "se": "0.35"
      }
    ]
  }
}
```

异常返回：

```json
{
  "status": "400",
  "message": "文件不能为空",
  "data": ""
}
```

## 命令示例

发票识别：

```bash
python .claude/skills/invoice-ocr/invoice_ocr.py ocr --file "E:\\invoices\\test.pdf"
```
