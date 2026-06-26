---
name: invoice-ocr-extractor
description: |
  发票票据识别虾 — 自动识别发票/票据图片，提取关键字段（金额、日期、商家、税号等），支持批量处理、费用分类、税务验真，并可写入飞书多维表格或导出 Excel。

  当以下情况时使用此 Skill：
  (1) 用户上传发票图片（JPG/PNG/PDF），要求识别或录入
  (2) 需要批量处理多张发票，生成汇总表
  (3) 需要验证增值税发票真实性
  (4) 需要将发票数据写入飞书多维表格或报销系统
  (5) 用户提到"发票识别"、"票据识别"、"报销凭证"、"自动填表"、"发票录入"、"OCR识别"、"增值税发票"、"费用报销"、"发票验真"、"财务录入"
---

# 发票票据识别虾

## 工作流程

```
[发票图片/PDF] → [图像预处理] → [OCR识别] → [字段提取] → [数据校验] → [入库/填表]
```

## 步骤

### 1. 接收输入
- 用户发送发票图片（飞书消息中的图片/文件）→ 用 `feishu_im_bot_image` 下载到本地
- 批量场景：用户提供文件夹路径或多张图片

### 2. OCR 识别
调用 `scripts/extract-invoice.py` 进行识别：

```bash
# 单张
python3 scripts/extract-invoice.py extract --file <图片路径>

# 批量
python3 scripts/extract-invoice.py batch --dir <目录> --output results.xlsx
```

**OCR 优先级**：
1. 百度发票识别 API（`BAIDU_OCR_API_KEY` + `BAIDU_OCR_SECRET_KEY`）
2. 阿里发票识别 API（`ALIYUN_OCR_ACCESS_KEY`）
3. 降级：使用 AI 视觉能力直接分析图片（无需 API key，准确率略低）

> 若无 OCR API，直接将图片发给 AI 模型，用视觉能力提取字段，并说明"使用 AI 视觉识别，建议人工复核金额"。

### 3. 提取标准字段

| 字段 | 说明 |
|------|------|
| invoice_type | 发票类型（增值税专票/普票/电子发票/机票/火车票/餐饮/住宿/出租车） |
| invoice_code | 发票代码（10或12位） |
| invoice_number | 发票号码（8位） |
| invoice_date | 开票日期（YYYY-MM-DD） |
| seller_name | 销售方名称 |
| buyer_name | 购买方名称 |
| amount | 不含税金额 |
| tax_rate | 税率 |
| tax_amount | 税额 |
| total_amount | 价税合计 |
| expense_category | 费用分类（见 references/expense-categories.md） |
| confidence | 识别置信度（high/medium/low） |

### 4. 数据校验
- 金额校验：`amount + tax_amount ≈ total_amount`（误差 < 0.01）
- 日期合理性：开票日期不能是未来日期
- 发票代码格式：10位或12位纯数字
- 重复发票检测：同一 `invoice_code + invoice_number` 组合视为重复

### 5. 费用分类
参考 `references/expense-categories.md` 自动分类。

### 6. 输出
根据用户需求选择输出方式：

**飞书多维表格**（推荐）：
- 参考 feishu-bitable skill，将结果写入多维表格
- 字段映射见上方标准字段表

**Excel 导出**：
```bash
python3 scripts/extract-invoice.py batch --dir ./invoices --output results.xlsx
```

**直接回复**：单张发票直接在对话中展示提取结果

## 税务验真（可选）

仅对增值税专票/普票有效：
```bash
python3 scripts/extract-invoice.py verify \
  --code <发票代码> \
  --number <发票号码> \
  --date <开票日期> \
  --amount <金额>
```

结果：真实 / 虚假 / 已作废 / 已冲红

> 税务验真 API 有每日免费额度，批量验真时注意控制频率。

## 注意事项

- 图片模糊时，提示用户重新拍摄（建议 300DPI 以上）
- 金额 > 1000 元时，建议提示用户人工复核
- 不支持手写收据和外文发票
- 批量处理时，自动去重（相同发票代码+号码只录入一次）

## 参考文件

- `references/invoice-types.md` — 各类发票版面特征
- `references/field-extraction.md` — 字段提取规则
- `references/expense-categories.md` — 费用分类规则
- `references/tax-verification.md` — 税务验真接口说明
