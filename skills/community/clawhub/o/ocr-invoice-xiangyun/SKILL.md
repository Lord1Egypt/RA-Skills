---
name: xiangyun-invoice-ocr
version: 1.0.1
description: |
  翔云发票识别与查验 Skill。当用户请求以下操作时触发：
  - 发票识别、发票 OCR、识别发票
  - 发票查验、发票验真、发票核验、核查发票真伪
  - 扫描发票、读取发票信息、提取发票数据
  - 增值税发票识别、电子发票识别、数电票识别
  - 发票导出、发票台账、发票入账表、发票勾选抵扣
  - 旅客运输抵扣表、货物明细表
  - 批量发票处理、发票文件夹识别
  - netocr 发票、翔云发票
author: sinosecu
tags:
  - OCR
  - invoice
  - 发票
  - 税务
---

# xiangyun-invoice-ocr — 翔云发票识别与查验 Skill

本 Skill 调用翔云平台 API，实现发票图片/PDF **识别 → 查验**全流程。
导出功能仅在用户**明确提出**时才执行。

---

## 能力概览

| 功能 | 说明 |
|:---|:---|
| **发票识别** | 支持全票种（增值税专票/普票/数电票/电子票等），JPG/PNG/PDF/OFD |
| **发票查验** | 识别后自动提取查验入参，联网核验真伪，返回完整票面信息 |
| **Excel 导出** | 5 种标准模版按发票类型自动匹配（仅用户明确要求时） |
| **批量处理** | 支持单张和文件夹批量模式，批量前验证 key/secret |

---

## 凭据配置

首次使用必须配置凭据。凭据存储于本 Skill 目录下的 `config.json`。

**获取方式**：登录 [netocr.com](https://netocr.com) → 个人中心 → 查看 key / secret

**配置文件格式**（`config.json`）：
```json
{
  "key": "你的 ocrKey",
  "secret": "你的 ocrSecret"
}
```

---

## 脚本使用

### 识别单张发票（仅识别）
```bash
python scripts/invoice.py --image <发票路径>
```

### 识别 + 查验（默认行为）
```bash
python scripts/invoice.py --image <发票路径> --verify
```

### 批量识别 + 查验（默认行为，批量前自动验证 key/secret）
```bash
python scripts/invoice.py --dir <目录路径> --verify
```

### 交互选择导出Excel模版（仅用户明确要求时才加 --export，并鼠标点选）
```bash
python scripts/invoice.py --image <发票路径> --verify --export --select-template
python scripts/invoice.py --dir <目录路径> --verify --export --select-template
```
脚本检测到 `--select-template` 时输出结构化标记并退出，由 Agent 调用 `ask_followup_question` 弹出多选窗口，用户点选后 Agent 将结果通过 `--template` 重新调用脚本。

### 指定导出模版（仅配合 --export 使用）
```bash
# 单选
python scripts/invoice.py --image <发票路径> --verify --export --template ledger
# 多选（逗号分隔）
python scripts/invoice.py --dir <目录> --verify --export --template goods,booking
```

模版名称及说明：

| 编号 | 参数值 | 说明 |
|:---:|:---|:---|
| 1 | `deduction` | 增值税发票勾选抵扣表（抵扣进项税额） |
| 2 | `transport` | 国内旅客运输服务抵扣表（航空/铁路/客车/旅客运输服务/通行费） |
| 3 | `goods` | 增值税发票货物明细表（商品明细记录） |
| 4 | `ledger` | 增值税发票台账表（最全字段，覆盖广） |
| 5 | `booking` | 发票入账表（财务记账用） |

> **严格票种过滤**：每个模板只导出其适用票种的数据，票种不匹配时自动跳过并提示 `[SKIP] {模版} 不适用于票种 {类型}，跳过`。
> **空文件生成**：批量模式下，即使用户选择的模板没有任何匹配发票，也会生成空表头文件（仅标题+列头，无数据行）。
>
> **Agent 使用说明**：当用户需要导出但未指定 `--template` 时，Agent 应主动调用 `ask_followup_question`（multiSelect=true）展示 5 个模板选项供用户点选，再将结果通过 `--template` 参数传给脚本。

---

## 发票类型映射

本 Skill 支持 **46 种**发票类型的识别，区分**可查验**与**仅识别**两大类。

### 可查验（识别后可联网核验真伪）

查验入参 `totalAmount` 按类型分两类取值：

| 票种名称 | 票种代码 | totalAmount 取值 |
|:---|:---:|:---|
| 增值税专用发票 | 01 | `totalAmount`（不含税） |
| 机动车销售统一发票 | 03 | `totalAmount`（不含税） |
| 增值税普通发票 | 04 | `totalAmount`（不含税） |
| 增值税专用发票(电子) | 08 | `totalAmount`（不含税） |
| 电子发票(增值税专用发票) | 09 | `amountTax`（价税合计） |
| 增值税电子普通发票 | 10 | `totalAmount`（不含税） |
| 增值税普通发票(卷票) | 11 | `totalAmount`（不含税） |
| 通行费增值税电子普通发票 | 14 | `totalAmount`（不含税） |
| 二手车销售统一发票 | 15 | `totalAmount`（不含税） |
| 电子发票(航空运输电子客票行程单) | 61 | `amountTax`（价税合计） |
| 电子发票(铁路电子客票) | 62 | `amountTax`（价税合计） |
| 电子发票(机动车销售统一发票) | 63 | `totalAmount`（不含税） |
| 电子发票(二手车销售统一发票) | 64 | `totalAmount`（不含税） |
| 电子发票（普通发票）通行费 | 72 | `amountTax`（价税合计） |
| 电子发票(普通发票) | 83 | `amountTax`（价税合计） |
| 数电纸质发票(增值税专用发票) | 91 | `totalAmount`（不含税） |
| 数电纸票发票(普通发票) | 92 | `totalAmount`（不含税） |
| 数电纸质发票(机动车销售统一发票) | 93 | `totalAmount`（不含税） |
| 数电纸票发票(二手车销售统一发票) | 94 | `totalAmount`（不含税） |

### 仅识别（不支持查验）

| 票种名称 | 票种代码 |
|:---|:---:|
| 火车票 | 20 |
| 区块链发票 | 21 |
| 船票 | 22 |
| 定额发票 | 23 |
| 机打发票 | 24 |
| 出租车发票 | 25 |
| 客运汽车 | 26 |
| 航空运输电子客票行程单 | 27 |
| 过路费 | 28 |
| 打车行程单 | 31 |
| 货物清单 | 33 |
| 财政电子票据 | 34 |
| 海关缴款书 | 35 |
| 通用电子发票 | 36 |
| 完税证明 | 37 |
| 医疗票据 | 38 |
| 退票费报销凭证 | 39 |
| 非税收入一般缴款书(电子) | 40 |
| 车辆通行费通用(电子)发票 | 41 |
| 银行回单 | 42 |

---

## 5 种 Excel 模版及适用票种

| 模版 | 参数值 | 适用票种代码 |
|:---|:---:|:---|
| 增值税发票勾选抵扣表 | `deduction` | 01,03,08,09,14,91,93,61,62,72 |
| 国内旅客运输服务抵扣表 | `transport` | 10,14,20,22,26,27,61,62,83,92,72 |
| 增值税发票货物明细表 | `goods` | 01,03,04,08,09,10,11,14,15,21,63,64,83,91,92,72 |
| 增值税发票台账表 | `ledger` | 01,03,04,08,09,10,11,14,15,21,61,62,63,64,83,91,92,72 |
| 发票入账表 | `booking` | 01,03,04,08,09,10,15,61,62,63,64,83,91,92,14,72 |

---

## Agent 执行规范

### 默认行为（识别 + 查验）
当用户说"识别"、"OCR"、"扫描发票"等意图时：
- 单张：`--image <路径> --verify`
- 目录：`--dir <目录> --verify`
- **不加 --export**

### 仅识别（不查验）
当用户明确说"仅识别"、"不查验"时：
- 去掉 `--verify` 参数

### 导出 Excel
当用户明确提到"导出"、"台账"、"抵扣表"、"明细表"等时：
- 在识别查验基础上加上 `--export`
- 配合 `--template` 指定模板（可多选，逗号分隔）

### 批量前验证
批量处理（`--dir`）时会自动先用空请求验证 key/secret 是否可用，若认证失败会提前报错并提示。

---

## 执行逻辑

```
用户输入（图片/目录）
  │
  ├─ 检查 config.json → 若无 key/secret，要求用户配置后退出
  │
  ├─ 发票识别（recogInvoiveBase64.do，typeId=20090）
  │    └─ 解析返回：invoiceCode, invoiceNumber, billingDate,
  │                  totalAmount, checkCode, salesTaxNo 等
  │
  ├─ [--verify] 发票查验（verInvoice.do，typeId=3007）
  │    └─ 用识别结果自动填充查验入参
  │    └─ 返回完整票面 + 真伪状态
  │
  └─ [--export] 导出 Excel（仅用户明确要求）
       └─ 按 invoiceType 匹配模版
       └─ 写入对应字段，保存到 <原文件名>_<模版名>.xlsx
```

---

## API 参考

- 发票识别：`https://netocr.com/api/v2/recogInvoiveBase64.do`（typeId=20090）
- 发票查验：`https://netocr.com/verapi/v2/verInvoice.do`（typeId=3007）

---

## 认证错误检测

识别和查验接口返回时，会自动检测 key/secret 错误：
- 检测关键词：key、secret、密钥、认证、auth、unauthorized、401 等
- 检测到后打印友好提示，引导用户检查凭据或前往 netocr.com 重新获取

---

## ⚠️ 安全说明

- 用户图片及 API 凭据通过 HTTPS 发送至翔云（netocr.com）进行处理
- 凭据仅存储于本地 `config.json`，不上传至任何其他平台
