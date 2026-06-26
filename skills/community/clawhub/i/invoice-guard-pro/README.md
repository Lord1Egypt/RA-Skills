# InvoiceGuard · 发票合规管家

> AI 驱动发票查重、验真、合规报告生成工具

---

## 概述

InvoiceGuard 通过 AI 实现发票查重、验真、合规报告全流程。适用于企业财务报销合规检查、发票重复报销检测、发票真伪官方验真（金税四期）、符合财政部《财会便函〔2023〕18号》要求的合规报告生成。

**触发词**：发票、查重、验真、报销、合规、重复报销、假发票、发票识别、OFD、PDF发票

---

## 功能套餐

| 功能 | 免费版 | Pro 版 |
|------|--------|--------|
| 单张发票 AI 查重 | 每月 20 张 | 不限 |
| 批量处理（>20张） | ❌ | ✅ |
| 跨批次重复检测 | ❌ | ✅ |
| 官方验真（国税查验平台） | ❌ | ✅ |
| 合规报告生成 | 仅 Markdown | Markdown + 飞书云文档 |
| 发票明细存入飞书多维表格 | ❌ | ✅ |

---

## 支持的发票类型

| 类型 | 格式 | 说明 |
|------|------|------|
| 增值税专用发票 | 纸质/电子 | 可抵扣进项税 |
| 增值税普通发票 | 纸质/电子/卷式 | 不可抵扣 |
| 电子发票（数电票） | PDF / OFD / XML | 全国统一平台开具 |
| 机票行程单 | 纸质 | 航班信息 |
| 火车票 | 纸质 | 车次、日期、金额 |
| 出租车票 | 纸质 | 时间、金额 |

---

## 工作流程

```
用户上传发票
    │
    ├── 图片（JPG/PNG/截图）
    │   → miaoda-studio-cli image-understanding 提取文字
    │
    ├── PDF / OFD / XML
    │   → miaoda-studio-cli doc-parse 提取内容
    │
    ▼
解析关键字段（发票号码、日期、金额、购销方）
    │
    ▼
AI 查重引擎（三重校验）
    │  • 精确匹配：发票代码+号码相同 → 标记重复
    │  • 字段哈希：金额+日期+购销方 生成指纹 → 指纹碰撞检测
    │  • 篡改检测：同号码+不同金额 → 标记篡改
    ▼
官方验真（仅 Pro）
    │  • 对接国家税务总局增值税发票查验平台
    │  • 发票状态查询（正常/作废/红冲/失控）
    ▼
生成合规报告（Pro）
    │  • 标准 Markdown 报告
    │  • 飞书云文档报告（可分享、可评论）
    │  • 发票明细存入飞书多维表格
    ▼
返回结构化结果
```

---

## 发票查重三重校验逻辑

1. **精确匹配**：发票代码 + 发票号码完全相同 → 直接标记 `exact`（置信 1.0）
2. **篡改检测**：同代码+号码，但金额不一致 → 标记 `tampered`（置信 0.99）
3. **字段哈希**：金额 + 日期 + 购销方 生成指纹 → 指纹碰撞检测重复 → `hash_collision`

> ⚠️ 相同发票号+不同金额会被识别为"篡改"，不会误判为正常发票。

---

## 文件结构

```
skills/invoice-guard/
├── SKILL.md                        # Skill 定义文件（触发词、工具调用方式）
├── README.md                       # 本文件
├── references/
│   ├── changelog.md                # 变更记录（含问题修复历史）
│   ├── invoice-types.md            # 中国发票类型与字段规范
│   ├── tax-api.md                  # 国税增值税发票查验平台接入说明
│   └── compliance-report.md        # 发票合规报告模板（财会便函〔2023〕18号）
└── scripts/
    ├── duplicate_checker.py        # 发票查重引擎（三重校验+Pro/Free权限隔离）
    ├── batch_processor.py          # 批量发票处理器（识别→查重→验真→报告）
    └── compliance_report.py        # 合规报告生成器（Markdown+飞书原生方案）
```

---

## 核心脚本说明

### 1. `duplicate_checker.py` — 发票查重引擎

**功能**：三重校验发票重复，支持 Pro/Free 版本权限隔离。

**主要类**：
- `TierConfig`：用户版本配置（is_pro / monthly_count）
- `InvoiceRecord`：结构化发票数据
- `DuplicateResult`：查重结果（is_duplicate / match_type / confidence）

**关键函数**：
```python
check_duplicate(new_record: InvoiceRecord, existing_records: List[InvoiceRecord], tier: TierConfig) -> DuplicateResult
batch_check_duplicates(records: List[InvoiceRecord], tier: TierConfig, historical_records: List[InvoiceRecord] = None) -> List[DuplicateResult]
```

**权限控制**：
- 免费版：每月 20 张上限，限制批量处理
- Pro 版：无限制，支持跨批次查重

---

### 2. `batch_processor.py` — 批量发票处理器

**功能**：批量识别 → 批量查重 → 批量验真 → 汇总报告。

**主要类**：
- `BatchProcessor`：批量处理器，支持批量识别、并发查重
- `TaxVerificationResult`：验真结果（状态 / 说明）

**关键函数**：
```python
BatchProcessor.process_batch(invoices: List[str], tier: TierConfig) -> BatchResult
BatchProcessor.verify_invoice(invoice_record: InvoiceRecord) -> TaxVerificationResult
```

---

### 3. `compliance_report.py` — 合规报告生成器

**功能**：生成符合《财会便函〔2023〕18号》要求的六节结构化合规报告。

**报告结构**：
1. 基本信息（企业名称、税号、报告时间）
2. 发票汇总（总数 + 金额合计 + 按类型分布 + 按月份分布）
3. 查重结果（重复/可疑发票列表）
4. 验真结果（异常状态发票列表）
5. 合规结论（检查项目总结 + 风险提示）
6. 附件清单

**输出方式**：

| 方式 | 函数 | 说明 |
|------|------|------|
| 标准 Markdown | `generate_compliance_report_markdown()` | 写入本地文件 |
| 飞书云文档（推荐） | `generate_feishu_compliance_report_markdown()` | Lark-flavored Markdown，用于 `feishu_create_doc` |
| 飞书多维表格 | `prepare_invoices_for_feishu_bitable()` | 将发票明细批量导入飞书多维表格 |

**使用示例**：
```python
from scripts.compliance_report import (
    generate_feishu_compliance_report_markdown,
    create_feishu_bitable_schema,
    prepare_invoices_for_feishu_bitable,
)

# 生成飞书云文档 Markdown
markdown = generate_feishu_compliance_report_markdown(
    records=invoice_records,
    summary=report_summary,
    buyer_name="XX有限公司",
    buyer_tax_id="91440000XXXXXXXXXX"
)

# 获取多维表格字段定义
fields = create_feishu_bitable_schema(app_token)

# 准备批量导入数据
bitable_records = prepare_invoices_for_feishu_bitable(invoice_records)
```

---

## 飞书原生方案（Pro）

### 生成合规报告到飞书云文档

1. 调用 `generate_feishu_compliance_report_markdown()` 获取 Lark-flavored Markdown
2. 使用 `feishu_create_doc` 工具创建飞书文档
3. 文档可直接分享、评论，符合《财会便函〔2023〕18号》格式

### 发票明细存入飞书多维表格

1. 调用 `feishu_bitable_app` 创建多维表格 App
2. 调用 `feishu_bitable_app_table` 创建数据表（使用 `create_feishu_bitable_schema()` 返回的字段定义）
3. 调用 `feishu_bitable_app_table_record` 的 `batch_create` 批量导入发票明细

**多维表格字段**：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 发票代码 | 文本 | |
| 发票号码 | 文本 | |
| 开票日期 | 日期 | 毫秒时间戳，支持日期筛选 |
| 金额 | 数字 | 支持金额排序和统计 |
| 开票方 | 文本 | |
| 状态 | 单选 | 正常/重复/可疑/异常 |
| 查验状态 | 单选 | 未查验/正常/作废/红冲/失控 |

---

## 发票状态说明

| 状态 | 含义 | 报销建议 |
|------|------|----------|
| 正常（00） | 发票有效 | ✅ 可报销 |
| 作废（01） | 企业自行作废 | ❌ 不可报销 |
| 红冲（02） | 开具红字发票冲销 | ❌ 不可报销 |
| 失控（03） | 已被税局列为失控 | ❌ 不可报销 |
| 异常（04） | 数据不一致 | ⚠️ 需核实 |

---

## 字段提取规则

| 发票类型 | 关键字段 | 提取方式 |
|---------|---------|---------|
| 增值税专用发票 | 发票代码（10位）+ 发票号码（8位）、金额、税额、购销方、税号 | 正则提取 |
| 增值税普通发票 | 发票代码 + 发票号码 + 金额 + 购销方 | 正则提取 |
| 电子发票 PDF/OFD/XML | 完整结构化字段 | `doc-parse` 直接解析 |
| 机票行程单 | 航班、日期、金额、乘客 | 正则提取 |
| 火车票 | 日期、出发/到达地、金额 | 正则提取 |
| 出租车票 | 日期、时间、金额 | 正则提取 |

---

## 隐私与安全

- **不存储发票原始数据**：处理后即弃，不留存
- **沙箱环境运行**：与外部系统隔离
- **Pro/Free 权限隔离**：免费版无法调用国税查验 API，无法使用批量处理
- **Token 计费**：每次验真消耗 Token 计入账户

---

## 常见问题

| 问题 | 解答 |
|------|------|
| 国税查验接口需要什么？ | 企业纳税人资格 + 开发者账号（免费配额 100次/天/IP）|
| OFD 格式怎么解析？ | `miaoda-studio-cli doc-parse --file invoice.ofd` |
| 免费版和 Pro 版怎么区分？ | 通过用户选择或上下文判断，代码内嵌权限校验 |
| 图片不清晰怎么办？ | 提示用户重拍或扫描，确保发票号码和金额清晰可见 |
| 篡改发票怎么识别？ | 同发票代码+号码但金额不一致，标记为 `tampered`（置信 0.99）|

---

## 变更记录

详见 [references/changelog.md](references/changelog.md)

---

**版本**：2.0（飞书原生方案）  
**审查日期**：2026-04-19  
**审查人**：技能刀 / 妙搭 Agent
