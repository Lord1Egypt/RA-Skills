# 文件类型与分片类型参考

## 文件类型枚举 (file_type)

### 核心单据（参与数据提取与合并）

| file_type | 中文名称 | 英文名称 |
|---|---|---|
| `invoice` | 商业发票 | Commercial Invoice / Proforma Invoice |
| `contract` | 合同 | Sales Contract / Sales Confirmation |
| `packing_list` | 装箱单 | Packing List |
| `draft` | 报关单草单 | Customs Declaration Draft |
| `detail` | 明细表 | Item Detail List |
| `declaration` | 申报要素 | HS Declaration Elements |

### 辅助单据（仅分类标记，不参与数据合并）

| file_type | 中文名称 | 英文名称 |
|---|---|---|
| `bill_of_lading` | 提单 | Bill of Lading (B/L) / Air Waybill (AWB) |
| `certificate` | 证书 | Certificate (C/O, 质检证书, 卫生证书等) |
| `customs_release` | 放行通知 | Customs Release Notice |
| `other` | 其他单据 | Other (代理报关委托书、保险单等) |
| `unknown` | 未知文档 | Unrecognized |

### 类型覆盖规则（合并漏斗）

当同一票中出现多种核心单据时，系统按以下规则精简：

| 规则 | 条件 | 保留 | 丢弃 | 原因 |
|---|---|---|---|---|
| R1 | invoice + contract | `contract` | `invoice` | 合同包含发票核心字段且具法律效力 |
| R2 | draft + packing_list | `draft` | `packing_list` | 草单含件数重量且已有报关格式 |
| R3 | draft + detail | `draft` | `detail` | 草单信息覆盖明细表 |
| R4 | detail + packing_list | `packing_list` | `detail` | 箱单比明细表更权威 |
| R5 | declaration | 始终保留 | — | 申报要素独立，不与其他类型重叠 |

> 合并后最多保留 **3 种**核心类型。

## 分片类型枚举 (segment.type)

| type | 适用场景 | 说明 |
|---|---|---|
| `page` | PDF 文档 | 按页码划分，使用 `pages` 数组 |
| `image` | 图片文件 | 整张图片为一个分片，无 `pages` 字段 |
| `sheet` | Excel 文件 | 按 Sheet 划分 |
| `text` | 纯文本 | 文本段落划分 |

## 置信度 (confidence) 解读

| 范围 | 建议标注 | 操作建议 |
|---|---|---|
| ≥ 0.90 | ✅ 可信 | 直接确认 |
| 0.70 ~ 0.89 | ⚠️ 建议核实 | 提醒用户目测确认 |
| < 0.70 | ❗ 请人工确认 | 强制要求用户确认类型 |

## 展示分类结果的标准格式

为每个文件生成如下表格：

```
📋 文件 N：<file_name>（共 M 页，识别 K 个分片）

| 分片 | 页码/范围        | 识别类型                | 置信度 | 建议       |
|------|-----------------|------------------------|--------|------------|
| 1    | 第1页           | 提单 (bill_of_lading)   | 95%   | ✅ 可信    |
| 2    | 第2-6页         | 发票 (invoice)          | 88%   | ⚠️ 核实   |
| 3    | 第7-18页        | 装箱单 (packing_list)   | 65%   | ❗ 请确认  |

请确认分类结果是否准确？
- 修改类型：例如"分片2应该是装箱单"
- 拆分/合并：请说明页码范围
- 确认：回复"确认"或"OK"
```
