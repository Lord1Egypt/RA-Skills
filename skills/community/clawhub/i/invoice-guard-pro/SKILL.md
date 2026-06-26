---
name: invoice-guard
description: "InvoiceGuard · 发票合规管家 — AI 驱动发票查重、验真、合规报告生成工具。用于：发票上传/扫码识别、发票重复报销检测（AI 查重）、发票真伪官方验真（金税四期）、合规报告生成（财会便函〔2023〕18号）、批量发票处理。当用户提到：发票、查重、验真、报销、合规、重复报销、假发票、发票识别、OFD、PDF发票时使用此技能。"
---

# InvoiceGuard · 发票合规管家

通过 AI 实现发票查重、验真、合规报告全流程。

## 工作流程

```
用户上传发票
    │
    ├── 图片/截图/拍照
    │   → miaoda-studio-cli image-understanding 提取文字
    │
    ├── PDF / OFD / XML
    │   → miaoda-studio-cli doc-parse 提取内容
    │
    ▼
解析关键字段（发票号码、日期、金额、购销方）
    │
    ▼
AI 查重引擎
    │  • 图像指纹哈希比对
    │  • 关键字段一致性校验
    ▼
官方验真（Pro）
    │  • 对接国家税务总局查验平台
    │  • 发票状态查询（正常/作废/红冲）
    ▼
生成合规报告 → 写入飞书文档（Pro）
    │
    ▼
返回结构化结果
```

## 功能详解

### 1. 发票上传与识别

支持格式：图片（JPG/PNG）、PDF、OFD、XML

```bash
# 图片发票 → OCR 识别
miaoda-studio-cli image-understanding -i invoice.png

# PDF/OFD/XML 发票 → 文本提取
miaoda-studio-cli doc-parse --file invoice.pdf --output json
```

**关键字段提取：**
- 发票类型（增值税专用发票 / 普通发票 / 电子发票 / 火车票 / 机票等）
- 发票代码 + 发票号码
- 开票日期
- 价税合计金额
- 购买方名称 + 纳税人识别号
- 销售方名称 + 纳税人识别号
- 货物或应税劳务名称

### 2. AI 查重引擎

**免费版 + Pro 版均可用**

基于三重校验识别重复发票：
1. **精确匹配**：发票代码 + 号码完全相同 → 直接标记重复
2. **字段哈希**：金额 + 日期 + 购销方 生成指纹 → 指纹碰撞检测
3. **图像相似度**：图片结构相似度比对（截图/套打票识别）

```python
# 查重核心逻辑（见 scripts/duplicate_checker.py）
# 返回: {is_duplicate: bool, match_type: str, confidence: float}
```

### 3. 官方验真（Pro）

**仅 Pro 版可用**

对接国家税务总局增值税发票查验平台：
- 实时验证发票真伪
- 查询发票状态：正常 / 作废 / 红冲 / 失控
- 校验开票金额与系统记录是否一致

> ⚠️ 国税查验接口需企业开发者账号。配置方式见 references/tax-api.md

### 4. 合规报告（Pro）

**仅 Pro 版可用**

符合财政部《财会便函〔2023〕18号》要求，生成结构化合规报告。现在支持飞书原生方案：
- **合规报告** → 直接生成可分享评论的飞书云文档
- **发票明细** → 自动存入飞书多维表格，支持筛选分析

```
报告结构（六节，符合《财会便函〔2023〕18号》格式）：
├── 一、基本信息（企业名称、税号、报告时间）
├── 二、发票汇总（总数、金额合计、按类型/月份分布）
├── 三、查重结果（重复发票列表）
├── 四、验真结果（异常状态发票）
├── 五、合规结论（合规总结 + 风险提示）
└── 六、附件清单
```

#### 标准 Markdown 报告生成

调用 `scripts/compliance_report.py` 生成 Markdown 格式报告：
```bash
python3 scripts/compliance_report.py <summary_json> <records_json> [buyer_name] [buyer_tax_id]
```

**输出**：符合《财会便函〔2023〕18号》的完整 Markdown 报告，包含六节结构 + 发票明细表。

#### 飞书原生方案（推荐 Pro 用户使用）

**步骤 1：生成飞书文档报告**

调用 `generate_feishu_compliance_report_markdown()` 获取 Lark-flavored Markdown，
然后使用 `feishu_create_doc` 工具创建可分享可评论的飞书文档：

```python
from scripts.compliance_report import generate_feishu_compliance_report_markdown

markdown = generate_feishu_compliance_report_markdown(
    records=invoice_records,
    summary=report_summary, 
    buyer_name="XX有限公司",
    buyer_tax_id="91440000XXXXXXXXXX"
)

# 然后调用飞书 API 创建文档
# feishu_create_doc(title="发票合规检查报告-2026年X月", markdown=markdown)
```

**飞书文档特性**：
- 使用飞书原生高亮块展示风险提示，视觉更清晰
- 文档生成后自动可分享、可评论、可协作
- 完全符合《财会便函〔2023〕18号》的六节结构要求

**步骤 2：发票明细存入飞书多维表格**

先创建多维表格和数据表，定义字段，然后批量导入发票数据：

```python
from scripts.compliance_report import create_feishu_bitable_schema, prepare_invoices_for_feishu_bitable

# 1. 创建多维表格 App
# feishu_bitable_app action="create" name="发票合规检查明细表"

# 2. 获取 app_token，创建数据表（包含预设字段）
fields = create_feishu_bitable_schema(app_token)
# feishu_bitable_app_table action="create" app_token="<app_token>" name="发票明细" fields=fields

# 3. 准备发票数据并批量导入
bitable_records = prepare_invoices_for_feishu_bitable(invoice_records)
# feishu_bitable_app_table_record action="batch_create" app_token="<app_token>" table_id="<table_id>" records=bitable_records
```

**多维表格字段**：
| 字段 | 类型 | 说明 |
|------|------|------|
| 发票代码 | 文本 | |
| 发票号码 | 文本 | |
| 开票日期 | 日期 | 毫秒时间戳，支持日期筛选 |
| 金额 | 数字 | 支持金额排序和统计 |
| 开票方 | 文本 | |
| 状态 | 单选 | 正常/重复/可疑/异常，支持筛选 |
| 查验状态 | 单选 | 未查验/正常/作废/红冲/失控 |

**多维表格优势**：
- 支持按状态、日期、金额筛选查询
- 支持生成数据透视表和统计图表
- 团队协作方便，所有发票数据集中管理

### 5. 批量处理

**仅 Pro 版可用**（免费版限额 20 张/月）

支持批量上传数百张发票，自动排队处理：
- 批量识别 → 批量查重（支持跨批次）→ 批量验真 → 汇总报告

## 使用示例

### 示例 1：单张发票查重
```
用户：帮我查一下这张发票有没有重复报销
[上传发票图片]
```

→ 调用 `miaoda-studio-cli image-understanding` 识别
→ 提取发票关键字段
→ 调用本地查重引擎
→ 返回：发票号码、金额、查重结果

### 示例 2：发票验真（Pro）
```
用户：验一下这张发票真假
[上传发票图片]
```

→ 识别发票 → 调用国税查验 API → 返回真伪状态

### 示例 3：生成合规报告（Pro）
```
用户：帮我生成这批发票的合规报告
[上传多张发票]
```

→ 批量识别 → 批量查重 → 批量验真 → 生成飞书文档报告

### 示例 4：批量发票处理
```
用户：批量处理这50张发票
[上传压缩包或批量文件]
```

→ 解压归档 → 逐张识别 → 并发查重 → 汇总结果

## 字段提取规则

| 发票类型 | 关键字段 | 提取难度 |
|---------|---------|---------|
| 增值税专用发票 | 发票代码、号码、金额、税额、购销方 | ★★☆ |
| 增值税普通发票 | 发票代码、号码、金额、购销方 | ★★☆ |
| 电子发票（PDF/OFD/XML）| 完整结构化字段 | ★☆☆ |
| 火车票 | 日期、出发/到达地、金额 | ★☆☆ |
| 机票行程单 | 航班、日期、金额、乘客 | ★☆☆ |
| 出租车票 | 日期、时间、金额 | ★☆☆ |

## 常见问题

| 问题 | 解答 |
|------|------|
| 国税查验接口需要什么？ | 企业纳税人资格 + 开发者账号，免费配额有限 |
| OFD 格式怎么解析？ | `miaoda-studio-cli doc-parse --file invoice.ofd` |
| 隐私合规怎么保证？ | 不存储发票原始数据，处理后即弃 |
| 免费版和 Pro 版怎么区分？ | 通过用户选择或上下文判断，核心功能一致 |
| 图片不清晰怎么办？ | 提示用户重拍或扫描，确保发票号码和金额清晰可见 |

## 参考资料

- 发票格式规范：[references/invoice-types.md](references/invoice-types.md)
- 税局验真接口：[references/tax-api.md](references/tax-api.md)
- 合规报告模板：[references/compliance-report.md](references/compliance-report.md)
- 查重引擎脚本：[scripts/duplicate_checker.py](scripts/duplicate_checker.py)
