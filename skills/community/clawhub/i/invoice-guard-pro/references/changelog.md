# InvoiceGuard 变更记录

## 升级：合规报告功能升级 - 飞书原生方案（2026-04-19）

**功能**：实现飞书原生方案
- **合规报告**：直接生成可分享可评论的飞书云文档，符合《财会便函〔2023〕18号》六节结构要求
- **发票明细**：自动存入飞书多维表格，支持筛选、排序、图表分析

**新增函数**：
- `generate_feishu_compliance_report_markdown()` - 生成 Lark-flavored Markdown 格式报告，直接用于 `feishu_create_doc`
- `prepare_invoices_for_feishu_bitable()` - 将发票记录转换为飞书多维表格批量创建格式
- `create_feishu_bitable_schema()` - 返回创建发票明细表所需的字段定义

**技术升级**：
- 使用飞书原生高亮块（callout）展示风险提示，视觉层次更清晰
- 多维表格完整字段支持：发票代码、号码、日期、金额、开票方、状态、查验状态
- 支持筛选、排序、数据透视表和图表分析
- 文档可分享、可评论，支持团队协作

**部署说明**：
- 91Skillhub 独立于 91TokenHub
- 复用 GEO Master 同一套付费系统
- 部署服务器：124.220.60.10

---

## 新增：合规报告生成器（2026-04-19）

**文件**：`scripts/compliance_report.py`

新增加规报告生成脚本，符合《财会便函〔2023〕18号》要求的完整六节结构：
1. 基本信息（企业名称、税号、报告时间）
2. 发票汇总（按类型分布 + 按月份分布）
3. 查重结果（重复/可疑发票列表）
4. 验真结果（异常状态发票列表）
5. 合规结论（检查项目总结 + 风险提示）
6. 附件清单

**附：发票明细表** — 所有发票的完整列表，含状态标记

**输出**：Markdown 格式，可直接写入飞书文档。

---

**审查日期**：2026-04-19
**审查人**：技能刀 / 妙搭 Agent
**状态**：Critical + Major 问题全部修复

---

## Critical 问题修复

### C-1 · 篡改检测死代码

**文件**：`scripts/duplicate_checker.py`

**问题**：第 68-74 行精确匹配 `return` 后，第 83-99 行相同 `if` 条件永远无法执行。相同发票号但金额被篡改的发票，错误标记为 `exact`（置信 1.0）而非 `tampered`（置信 0.99）。

**根因**：
```python
# 原代码（BUG）
for existing in existing_records:
    if new_code == exist_code:          # 精确匹配优先 return
        return DuplicateResult(match_type="exact", ...)  # 永不返回

    # 下面这段相同条件的检查永远无法执行！
    if new_code == exist_code:          # 死代码
        if abs(new_amount - exist_amount) > 0.01:
            return DuplicateResult(match_type="tampered", ...)
```

**修复**：将篡改检测提前到精确匹配 return 之前，先判断金额是否一致：
```python
if new_code == exist_code:
    if abs(new_amount_dec - exist_amount_dec) > Decimal("0.01"):
        return DuplicateResult(match_type="tampered", confidence=0.99, ...)
    return DuplicateResult(match_type="exact", confidence=1.0, ...)
```

**验证**：相同发票号+不同金额 → `match_type=tampered`，置信 0.99

---

### C-2 · Regex 字符类语法错误

**文件**：`duplicate_checker.py`、`batch_processor.py`

**问题**：`[纳税人识别号|税号]` 是字符类（匹配单一字符），而非逻辑 OR。

**修复**：改用正确的非捕获组 alternation：
```python
# 错误
r'[纳税人识别号|税号][：:\s]*([A-Z0-9]{15,20})'

# 正确
r'(?:纳税人识别号|税号)[：:\s]*([A-Z0-9]{15,20})'
```

---

### C-3 · 零 Pro/Free 权限隔离

**文件**：`duplicate_checker.py`、`batch_processor.py`

**问题**：代码无任何版本校验逻辑，任何用户可无限制使用批量处理和国税查验 API。

**修复**：引入 `TierConfig` 类实现完整权限隔离：

| 功能 | 免费版 | Pro版 |
|------|--------|-------|
| 单张查重 | 20张/月 | 无限制 |
| 批量处理 | 禁止 | 无限制 |
| 国税查验 API | 禁止 | 可用 |
| 跨批次查重 | 禁止 | 可用 |

---

### C-4 · 千分位金额提取失败

**文件**：`duplicate_checker.py`、`batch_processor.py`

**问题**：`￥1,234.56` 只提取出 `1`。

**修复**：新增 `_amount_from_text()` 函数：
```python
r'[价税合计|价税][：:\s]*[￥¥]?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)'
```

---

## Major 问题修复

### M-1 · SHA256 截断导致哈希碰撞风险
`fields_hash()` 从 `[:16]`（16字符）改为完整 64 字符 SHA256。

### M-2 · 机票行程单被错误识别为"电子发票"
检测顺序调整：`航空`/`机票`/`行程单` 优先于 `电子发票`。

### M-3 · 跨批次重复发票无法检测
`batch_check_duplicates()` 新增 `historical_records` 参数，支持跨批次比对。

### M-5 · 浮点数比较改用 `Decimal`
所有金额比较改用 `Decimal`，避免浮点精度问题。

### M-6 · XML/OFD 解析支持
新增 `parse_xml_text()` 和 `parse_ofd_text()` 函数，支持 XML/OFD 文件内容解析。

---

## 修改文件清单

| 文件 | 改动 |
|------|------|
| `scripts/duplicate_checker.py` | C-1, C-2, C-3, C-4, M-1, M-2, M-5 |
| `scripts/batch_processor.py` | C-2, C-3, C-4, M-1, M-2, M-3, M-5, M-6 |
| `SKILL.md` | 更新 Pro 版权限描述 |
| `references/changelog.md` | 本文档 |
