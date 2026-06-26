---
name: kam-qianlu-doc-standards
description: 千路=询价管理+出入库/WMS(开发中)。本包权威=询价侧 Excel 表头/文件名(REFERENCE §1–10)、报价对比§12；问价单导出与报价单导入列对齐（含 MOQ/MPQ，无「状态」列）。术语/流程=naming+process。触发：表头命名、单据核验、报价对比矩阵、两子系统边界、filebrowser、采购单回传作用。
version: v6.1.2
---

# kam-qianlu-doc-standards（精简版，详表见 REFERENCE）

**版本 `version`**：与仓库 **Git 带 `v` 前缀的语义化 tag** 对齐（当前 **`v6.1.2`**）。打新 tag 时请同步更新本文件 frontmatter 中的 `version`，避免 skill 与线上/发布口径漂移。

## 1. 产品边界（必答清）
- **询价管理系统**：询价/报价/回询/订货/采购/报价对比/可订等 — **本 SKILL + 同目录 [REFERENCE.md](REFERENCE.md) 管表头与文件名**。
- **出入库管理系统（WMS）**：**开发中**；实收核销、库内表头 **不在此包权威范围**，答用户时单列说明。
- **易混**：「订货单入库完整版」= 询价侧**导出**给仓库用的 Excel，**≠** WMS 产品本体。

## 2. 同目录文档（勿在对话里复述长表）
| 文件 | 内容 |
|------|------|
| [REFERENCE.md](REFERENCE.md) | **§1–10** 各单据表头/别名/文件名；**§11** 术语索引；**§12** 报价对比（基准单/品牌矩阵，仅有效报价单） |
| [naming-and-terminology.md](naming-and-terminology.md) | 术语、UI 用词 |
| [process-and-rules.md](process-and-rules.md) | 流程、校验（订货↔回询匹配等）；与 `apps/inquiry-server/docs/functions/process-and-rules.md` 宜对照维护 |

## 3. 行为约定
- **查标准**：按用户单据类型打开 REFERENCE 对应节，**摘要**要点即可；完整列名/别名以 REFERENCE 为准。
- **核验 Excel**：确认类型 → **先问**是否核验表头与建议文件名 → 用 openpyxl 找表头行（含「品牌」或 brand 的首行，否则第 1 行）→ 对照 REFERENCE 别名 → 输出映射 + §1 文件名规则。
- **术语/流程**：REFERENCE §11 → 打开 naming 或 process。
- **上传**：若有 filebrowser-api / kam-filebrowser-operator 可代传；本 skill 只做表头/命名。

## 4. 单据类型 → REFERENCE 节号（速查）
二询价导入 · 三报价导入 · **四问价导出**（§4：第 1 行说明合并整行；表头 **9 列** — 品牌、零件号、替换号、中文名称、数量、报价含税、**MOQ、MPQ**、备注；与 §3 报价单可识别列一致，**不含「状态」**）· **五回询导出**（§5：英文表头 **8 列** — BRAND、PARTS、QTY、PRICE、**MOQ、MPQ**、Replace No、价差比例）· 六订货导入 · **七**订货导出（§7.1 校对版 9 列 / §7.2 入库版 11 列）· 八采购导出 · **九采购单回传导入** · 十可订导入 · **十二报价对比**

**问价单（实现一句）**：常量 `QUOTE_REQUEST_HEADERS` / `build_quote_request_excel` 见 `apps/inquiry-server/server/services/rfq_quote_group_service.py`；规范 §5.8 见 `apps/inquiry-server/docs/requirements-0309-1122.md`。

**采购单回传（业务一句）**：我方导出采购单 → 供应商填**无效/替换号/备注** → 文件 `校对-采购单-*.xlsx` 再导入 → 按品牌+零件号更新订货行，与线下一致。

## 5. 与 `apps/inquiry-*` 实现锚点（写代码/对需求时优先查）

以下为 **AI-CRM 询价子系统** 中与「单据格式、导入导出、校对」最直接相关的路径；表头别名仍以 **REFERENCE + 后端 `ORDER_HEADER_ALIASES`** 为准，勿仅凭记忆改列名。

### 5.1 后端 `apps/inquiry-server`
| 主题 | 位置 |
|------|------|
| **问价单** Excel 导出（组 / ZIP） | `server/services/rfq_quote_group_service.py` → `QUOTE_REQUEST_HEADERS`、`INSTRUCTION_ROW`、`build_quote_request_excel`、`build_batch_export_zip`；路由 `server/routers/rfq.py`（`/groups/{id}/export`、`batch-export`） |
| 订货单 Excel 列检测与别名 | `server/services/order_import_service.py` → `ORDER_HEADER_ALIASES`、`detect_order_columns` |
| 订货导入/校对版导出/订单校对 API 数据 | 同上 → `import_order_excel`、`export_order_excel`、`get_order_verify`、`parse_order_feedback_excel` 等 |
| 订货单列表（含「采购关联」统计） | `server/routers/order.py` → `list_orders`（`matched_items` = 订货明细与 `confirmed_purchase` 命中行数） |
| 采购汇总、确认入库、已确认采购、导出 | `server/routers/purchase.py`；业务实现多在 `server/services/purchase_summary_service.py`、`purchase_feedback_service.py` |
| 待订单校对（推导、与订货基准比对） | `server/services/confirmed_feedback_derive.py` |
| 报价对比导出 | `server/services/compare_service.py`（矩阵/基准与 REFERENCE §12 一致） |
| 可订库 / 替换号 | `server/services/availability_service.py` 等 |
| 补充需求与历史说明 | `apps/inquiry-server/docs/`、`docs/requirements-*.md`（仓库根目录） |

### 5.2 前端 `apps/inquiry-web`
| 主题 | 位置 |
|------|------|
| 询价单操作总页（Tab：回询/订货匹配/采购单生成等） | `src/pages/RfqOperatePage.tsx` |
| 问价单组、生成/打包下载 | `src/pages/RfqOperate/AskTab.tsx`；API `src/api/rfq.ts`（`exportQuoteRequest`、`exportQuoteRequestBatch`） |
| 订货单列表与切换 | `src/pages/RfqOperate/OrderListSection.tsx` |
| 订货单匹配 / 校对表格 | `src/pages/RfqOperate/OrderVerifySection.tsx`、`OrderFeedbackPanel.tsx` |
| 采购单生成工作台与已确认采购 | `src/pages/RfqOperate/PurchaseConfirmSection.tsx` |
| API 类型与请求 | `src/api/order.ts`、`src/api/purchase.ts` |
| 采购工作台本地草稿 | `src/utils/workbenchStorage.ts` |

### 5.3 仓库级说明
- 工作区约定与 MySQL 本地配置摘要：仓库根目录 **`CLAUDE.md`**（与 skill 互补：skill 管**单据标准**，CLAUDE 管**怎么跑项目**）。

## 6. ClawHub / 嵌入
正文刻意缩短以防 **8192 token** 上限；**任何「完整表头表」必须从 REFERENCE.md 读取**，不要凭记忆编造列名。
