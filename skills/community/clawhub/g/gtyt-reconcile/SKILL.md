---
name: gtyt-reconcile
description: 共同赢（GTYT）供应商账单与到货单的三阶段对账流程。用于按月核对「共同赢X月账单-上海-共同赢.xls」与「到货单明细表」在每店每产品上的「单价」「数量」「金额」是否一致，输出两份 Excel：(1) 两表金额差异对比 .xls（全量店名对比 + 25 店差异清单），(2) 共同赢X月账单-已标差异 .xls（在原账单上用黄色背景标出每个差异单元格）。触发关键词：「对账」「核对」「共同赢」「到货单差异」「标差异」「账单 vs 到货」。
---

# GTYT Reconcile — 共同赢账单与到货单对账

## 适用场景

核对同一供应商（上海共同赢实业有限公司）在一个自然月内的：
- **账单**：`共同赢X月账单-上海--共同赢.xls`（销售出库序时簿格式）
- **到货单**：`到货单明细表.xlsx`（CGRKD 前缀单号）

输出两份 .xls，并通过飞书 DM 发送给用户。

## 输入文件约定

| 文件 | 格式 | 关键列 |
| --- | --- | --- |
| 共同赢账单 | .xls（CFB/WPS） | col0 单据编号 / col1 分店名称 / col2 产品长代码 / col3 产品名称 / col4 规格 / col5 单位 / col6 实发数量 / col7 销售单价 / col8 销售金额 |
| 到货单 | .xlsx | col0 账套 / col1 门店 / col3 到货单号 / col4 到货时间 / col5 存货编码 / col6 存货名称 / col7 规格 / col8 单位 / col9 单价 / col10 到货数量 / col11 金额 |

**末尾的"合计"行（门店列为空，金额合计）必须剔除**。

## 店名映射规则

账单是「哥哥的深夜食堂-上海龙凤PRSCO店」全称，到货单是「龙凤PRSCO店」简称。skill 内置一份 152 条人工映射表（见 `scripts/store_mapping.py`），跑全量覆盖 126 个上海/苏州/杭州/深圳店。

未映射的店会落入「未匹配到货店」桶，不影响主流程。

## 工作流

### Step 1: 解析两份表
用 `scripts/parse_tables.py`：
- 账单 → 按 (分店名称, 产品长代码) 聚合 数量/金额/单价
- 到货单 → 按 (门店, 存货编码) 聚合 数量/金额/单价（剔除「合计」空行）
- 合并到统一 (invoice_store_name, sku) keyspace

### Step 2: 生成「两表金额差异对比.xls」
调用 `scripts/build_diff_report.py`：
- 4 个工作表：差异对比明细（25 行）、差异店清单、全量对比(126店)、对比说明
- 差异判定：|销售金额 − 到货金额| > 0.01 元
- 用 xlwt 输出，差额列正数红/负数绿

### Step 3: 生成「共同赢X月账单-已标差异.xls」
调用 `scripts/mark_bill_diff.py`：
- 用 xlutils 复制**原账单 xls**（保留字体/列宽/货币格式）
- 黄色背景（pattern_colour_index=13）标在「数量/单价/金额」三列
- 标记条件：任一字段差异 > 0.01 元，或账单有但到货单无

### Step 4: 飞书发送
- 两份 .xls 写到 /tmp/
- 复制到 /root/.openclaw/media/outbound/
- 通过 `message` 工具的 `filePath` 参数发送
- 文本中说明：差异店数 / 标黄单元格数 / 店名合并提示（如陆悦天地+金杨陆悦坊）

## 关键约定

1. **金额 = 单价 × 数量** 在两份表上必须严格成立（输入校验）
2. **陆悦天地 vs 金杨陆悦坊** 映射到同一到货仓库，账单上几乎全行标黄——这是预期行为，不要视为错误
3. **末尾"合计"行** 必须从到货单剔除，否则金额汇总虚增一倍
4. xlutils 修改时只动背景色 pattern，不改字体/列宽，保留原表观感

## 脚本入口

```bash
# 完整跑（账单 vs 到货单）
python3 scripts/run_full.py <账单.xls> <到货单.xlsx> [output_dir]

# 单独跑某一步
python3 scripts/parse_tables.py <账单.xls> <到货单.xlsx>
python3 scripts/build_diff_report.py <parsed.json> <output.xls>
python3 scripts/mark_bill_diff.py <账单.xls> <parsed.json> <output.xls>
```

## 错误处理

- 账单 .xls 文件名编码异常（飞书附件中文乱码）→ 不影响解析，按文件实际内容判断
- 同一 SKU 在账单上出现多次（如不同规格多行）→ 按 (店, SKU) 聚合并保留多行匹配
- 店名完全不在映射表中 → 计入「未匹配到货店」并提示用户手工核对
- 数量/单价/金额任一字段 0 偏差仍超过 0.01 → 三列都标黄

## 已知坑

1. xlrd 1.2.0 读 .xls，xlrd 2.0+ 不支持 .xls——必须用 1.2.0
2. xlwt 只能新建 .xls，不能编辑；用 xlutils.copy 桥接
3. xlutils 写入时不要动格式，背景色用 pattern_colour_index
4. openpyxl 读 .xlsx 时「合计」空行的 cell 值是 `''`（空字符串），不是 None，要用 `r[1] != '合计'` 双重判断
