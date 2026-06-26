---
name: invoice-dedup
description: 发票查重技能。录入发票进行查重、查询查重记录。适用于验证发票是否重复录入的场景。
---

# 发票查重技能

使用此技能将发票信息录入系统进行查重，或查询已有的查重记录。

## 使用场景

满足以下需求时使用：

- 录入发票信息并检查是否与已有记录重复。
- 按日期范围查询已录入的查重记录。

## 触发语句示例

以下用户输入应触发此技能：

- 帮我查重这张发票 / 发票查重 / 这张发票有没有重复
- 录入发票进行查重 / 录入查重
- 查一下发票 26117000000698099579 是否重复
- 查询查重记录 / 看一下查重记录 / 查重历史
- 查一下5月份的查重记录
- 列出最近的查重记录
- 这张发票重不重复

## 输入参数

执行前准备以下参数：

- apiKey（必填）：通过 https://skill.quandianfapiao.com/ 申请。

### 查重录入 (enter)

- 发票号码（必填）
- 开票日期（必填，格式 YYYY-MM-DD）
- 发票代码（可选）
- 价税合计（可选）

### 查重记录查询 (query)

- 采集日期开始（可选，格式 YYYY-MM-DD）
- 采集日期结束（可选，格式 YYYY-MM-DD）
- 开票日期开始（可选，格式 YYYY-MM-DD）
- 开票日期结束（可选，格式 YYYY-MM-DD）
- 页码（可选，默认 1）
- 每页条数（可选，默认 10）

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
   - 缺少发票号码或开票日期：停止并提示用户提供对应参数。
2. 通过 python 执行脚本调用远程 API（Windows 下使用 `python`，macOS/Linux 使用 `python3`），脚本优先使用 `--api-key` 参数，未传则回退读取环境变量 `ZXT_API_KEY`。
3. 检查返回的 status 字段，非 200 时停止并将错误信息展示给用户，禁止重试或忽略。
4. 解析返回结果并以可读格式输出。

## 请求参数说明

### 查重录入 — POST /api/jxplus/zxtSkill/repeat/enterSkillRepeatInvoice

| 参数          | 类型   | 必填 | 说明                   |
| ------------- | ------ | ---- | ---------------------- |
| apiKey        | string | 是   | apiKey                 |
| invoiceNumber | string | 是   | 发票号码               |
| invoiceDate   | string | 是   | 开票日期（YYYY-MM-DD） |
| invoiceCode   | string | 否   | 发票代码               |
| jshj          | string | 否   | 价税合计               |

### 查重记录查询 — POST /api/jxplus/zxtSkill/repeat/getRepeatInvoiceList

| 参数            | 类型   | 必填 | 说明                     |
| --------------- | ------ | ---- | ------------------------ |
| apiKey          | string | 是   | apiKey                   |
| startDate       | string | 否   | 采集日期开始（YYYY-MM-DD）|
| endDate         | string | 否   | 采集日期结束（YYYY-MM-DD）|
| startKprqDate   | string | 否   | 开票日期开始（YYYY-MM-DD）|
| endKprqDate     | string | 否   | 开票日期结束（YYYY-MM-DD）|
| pageNo          | string | 否   | 页码，默认 1             |
| pageSize        | string | 否   | 每页条数，默认 10        |

## 返回说明

### 查重录入返回字段

| 字段           | 说明                       |
| -------------- | -------------------------- |
| invoiceNumber  | 发票号码                   |
| invoiceCode    | 发票代码                   |
| invoiceDate    | 开票日期                   |
| jshj           | 价税合计                   |
| repeatType     | 重复类型：0 不重复，1 重复 |
| repeatTypeName | 不重复 / 重复              |
| collectTime    | 采集时间                   |

### 查重记录查询返回

返回分页列表，每条记录包含上述字段，额外包含 `total`（总条数）。

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

### 查重录入 — POST /api/jxplus/zxtSkill/repeat/enterSkillRepeatInvoice

请求：

```json
{
  "data": {
    "apiKey": "sk-sg-9EVbsJLJnlKVLaSO4FZtPUVFysbFL",
    "invoiceNumber": "26117000000698099579",
    "invoiceDate": "2026-05-14"
  }
}
```

成功返回：

```json
{
  "status": "200",
  "message": "成功",
  "data": {
    "invoiceCode": null,
    "invoiceNumber": "26117000000698099579",
    "invoiceDate": null,
    "jshj": null,
    "repeatType": "0",
    "repeatTypeName": "不重复",
    "collectTime": "2026-05-18 08:58:28"
  },
  "logId": "2056177564666896386"
}
```

异常返回：

```json
{
  "status": "400",
  "message": "开票日期不能为空",
  "data": ""
}
```

### 查重记录查询 — POST /api/jxplus/zxtSkill/repeat/getRepeatInvoiceList

请求：

```json
{
  "data": {
    "apiKey": "sk-sg-9EVbsJLJnlKVLaSO4FZtPUVFysbFL",
    "startDate": "2026-05-01",
    "endDate": "2026-05-31",
    "pageNo": "1",
    "pageSize": "10"
  }
}
```

成功返回：

```json
{
  "status": "200",
  "message": "成功",
  "data": {
    "pageNo": "1",
    "pageSize": "10",
    "total": "1",
    "list": [
      {
        "invoiceCode": null,
        "invoiceNumber": "26117000000698099579",
        "invoiceDate": "2026-05-14",
        "jshj": null,
        "repeatType": "0",
        "repeatTypeName": "不重复",
        "collectTime": "2026-05-18 08:59:19"
      }
    ]
  },
  "logId": "2056182604139966466"
}
```

## 命令示例

查重录入：

```bash
python3 .claude/skills/invoice-dedup/invoice_dedup.py --api-key "<apiKey>" enter --invoice-number "26117000000698099579" --invoice-date "2026-05-14"
```

查重记录查询：

```bash
python3 .claude/skills/invoice-dedup/invoice_dedup.py --api-key "<apiKey>" query --start-date "2026-05-01" --end-date "2026-05-31" --page-no "1" --page-size "10"
```
