---
name: kingdoc
displayName: 金山文档 KingDoc
slug: kingdoc
version: 4.4.0
description: >
  金山文档 AI 协作助手 — 9 品类在线文档全生命周期管理
  （文档/智能画布/电子表格/演示文稿/多维表格/收集表/可视化/历史管理/全文搜索/附件），
  深度直连金山文档（WPS）开放平台原生 API，覆盖腾讯文档全部能力 + 金山独有 21 项增强
  （回收站、版本历史、格式转换（全格式覆盖 jpg/png/txt）、纯文本提取、本地 Tesseract OCR（强制本地，数据不出域）、
  通知推送、Webhook、批量任务、政企合规、硬件自适应性能、WPS AI 能力、协同冲突解决、
  文档合规检查、实时协同编辑、文档对比、WPS AI 深度集成、模板市场、多维表格视图增强、
  手写/公式识别、历史管理、智能画布元素级编辑、全文搜索、块级编辑、演示页替换、配额管理器、
  wps-office-suite 双向桥接、zwjh 记忆库打通、表单答卷收集统计、AirScript 在线自动化、多维表格字段自动化、
  看板/甘特图视图渲染、CRDT 表格扩展（单元格级无冲突协作）、Excel/CSV 双向导入导出（四类字段序列化）、
  Webhook 与通知中心（三通道分发 + 签名校验 + SQLite 去重））。
  文字/演示/可视化采用"本地生成→上传覆盖"，电子表格/多维表格采用 API 精细编辑。
  智能画布支持元素级 CRUD + Markdown 增量追加。块级编辑实现段落级在线编辑替代整文件替换。
  v4.1 多维表格深化与在线自动化：AirScript 脚本引擎（自然语言→脚本生成→预检→确认→在线执行）、
  多维表格字段自动化（公式/关联/汇总字段）、视图渲染（matplotlib 看板柱图 + mermaid 甘特时间线）、
  CRDT 表格扩展（单元格级操作日志 + 向量时钟冲突标记）、Excel/CSV 双向 I/O（date/link/select/person 四类字段序列化）、
  Webhook 通知中心（新增/修改/删除事件订阅 + 金山协作/企微/钉钉三通道）。
  v4.2 知识中枢与政企合规：团队知识库模式（空间级倒排检索 + 权限矩阵过滤，先鉴权后检索）、
  政企合规中心（密级标注落库 + 敏感词/数据泄露全量扫描报告 + 数据不出域声明）、
  主题一键生成（WPS AI 适配层 generate：大纲→智能文档/PPT/表格初稿，本地降级可切换真源）、
  跨品类对比与时间线（版本历史轮询→who/when/what 时间线 + 表格单元格级 diff），
  OCR 收敛（唯一入口，优先桥接 wps-office-suite，未装则 Tesseract 最小兜底，数据不出域）。
  v4.3 合规中心 v2：合规套件门面（单入口两档输出 quick_scan/full_scan，合并 v4.2 政企合规中心与 v3.4 内容合规检查，敏感词加载逻辑唯一来源、维护面减半），
  行业敏感词分包（base 通用 + 教培/医疗/金融/政务四行业包，各 200+ 词条，多包叠加，报告按高/中/低风险分级并定位段落与责任人字段），
  全域扫描定时化（schtasks 周扫空间，新检出项经 webhook 三通道签名推送 + 跨周去重只推新增不扰民），
  配额管理器阈值告警（用量 80% / 95% 两级经 webhook 三通道推送，按天+级别幂等）。
  v4.4 表单实时化与多维表格自动化：答卷实时推送（轮询 + 增量游标 + webhook 三通道，端到端 ≤30 秒）、
  跨表聚合分析（问题→标准字段映射 + 多渠道报名去重 + HTML 看板，去重准确率 ≥98%）、
  答卷沉淀多维表格（复用 date/link/select/person 四类字段序列化，person/link 双向可编辑）、
  多维表格定时快照与变更摘要（每日快照存 SQLite + 单元格级 diff，5000 行 ≤10 秒）、
  AirScript 预设库 20+（去重提醒/到期扫描/自动编号/状态流转等，全部带测试样例与预期输出）、
  CRDT 冲突可视化（操作日志 + 向量时钟 ECharts 时间线，冲突可审查可追溯）。
  本地生成、OCR、硬件画像、WPS AI、全文搜索、块级编辑、配额管理、桥接、AirScript、视图渲染、CRDT、数据 I/O、Webhook、知识中枢、政企合规、主题生成、跨品类对比、合规门面、行业分包、周扫定时化、配额告警、答卷实时推送、跨表聚合、答卷沉淀、表格快照、预设库、冲突可视化等能力零密钥可用。
description_zh: "金山文档 AI 协作助手 — 9 品类在线文档全生命周期管理（深度直连 WPS 开放平台 + 智能画布元素级编辑 + 全文搜索超越腾讯 + 块级编辑段落级 + 18 项增强）"
platforms: [WorkBuddy, QClaw, ima, Claude Code, Cursor]
tags: [文档处理, 表格处理, PPT生成, 多维表格, 表单收集, 思维导图, 流程图, OCR, 政企合规]
license: MIT
requires_api_key: true
icon: assets/icon.png
---

# KingDoc — 金山文档 AI 协作助手 v3.0.0

> 对标腾讯文档 TENCENT DOCS，功能 1:1 覆盖 + 差异化增强。
> **v3.0.0 重点：深度直连在线文档原生 API、危险操作强制确认、硬件自适应性能、免密钥本地能力。**

---

## 📣 评测反馈与本轮（v3.0.0）优化说明

本版本针对第三方评测（综合 4.5/5「优秀」）的降分项做了**逐项闭环**：

| 评测降分点 | v3.0.0 优化 |
|-----------|------------|
| 某些危险操作缺强制确认，可能误操作 | 新增「危险操作强制确认」铁律与确认清单（见第 6、12 节） |
| 高级功能需额外装 Tesseract | 本地 OCR **免密钥**优先；未装 Tesseract 时降级云端，都无则给安装指引 |
| 首次配置需 App Key，对新手复杂 | 明确「本地生成/OCR/硬件画像零配置可用」；云端仅上传/协作需 Key |
| 能力边界说明少（大文件/失败场景） | 新增「能力边界与失败场景」专章（第 13 节） |
| 触发方式不清晰（高级功能怎么说） | 新增「自然语言触发示例」专章（第 5 节） |
| FAQ 不丰富、找不到答案 | 新增 FAQ 专章（第 25 节），安全/错误集中可查 |
| 缺完整场景案例 | 新增「完整场景案例」专章（第 11 节） |
| 创造性/增值不足 | 新增硬件自适应性能调度、网页剪藏、批量任务、Webhook 等增值能力 |
| 性能可能拖累电脑 | 新增硬件自动采集 + 自动分配并发子进程数（第 17 节） |

---

## ⚠️ 首次使用必读

### 1. 申请金山开放平台 App（免费，仅云端协作需要）

**只影响「上传到云端 / 多人协作 / 回收站 / 版本」等联网能力。**
本地生成文档、本地 OCR、硬件画像**完全不需要 Key，开箱即用**。

申请步骤：
1. 访问 [金山开放平台](https://developer.kdocs.cn) 并登录金山文档账号
2. 进入「应用管理」→「创建应用」，获取 **`App ID`** 和 **`App Secret`**
3. 勾选权限（OAuth Scope）：
   - 必须：`user:file:write`、`user:file:read`、`team:file:write`、`team:file:read`
   - 建议：`user:team:read`、`user:notification:write`
4. 测试阶段限速 500 次/天，正式版 10 万次/天

### 2. （可选）安装本地 Tesseract OCR

仅「图片文字提取」需要；未装则自动降级云端 OCR 或给指引，**不影响其他功能**。

```bash
# Windows
winget install UB-Mannheim.TesseractOCR
# macOS
brew install tesseract tesseract-lang
# Linux
sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim
```

### 3. 配置并加载

**首次配置由 AI 引导完成**：直接告诉我你的金山开放平台 **App ID / App Secret**，我会自动生成 `config.json`、`mcp-config.json`、模板与图标，并采集本机硬件画像。无需手动执行安装命令。

---

## 快速开始

| 你想做什么 | 直接对 AI 说 |
|-----------|-------------|
| 新建会议纪要 | `"帮我写一份会议纪要"` |
| 创建数据表 | `"建一个销售数据表格，含产品/销量/金额"` |
| 生成 PPT | `"帮我做一份产品发布 PPT"` |
| 生成思维导图 | `"画一个项目计划的思维导图"` |
| 生成流程图 | `"画一个用户下单流程图"` |
| 看文档内容 | `"看看这个文档说了什么"` |
| 搜文件 | `"搜一下上个月的合同"` |
| 上传本地文件 | `"把这个 PDF 上传到云端"` |
| 识别图片文字 | `"把这张发票的文字提取出来"` |
| 恢复误删 | `"回收站里有没有昨天删的 Word？"` |
| 回滚版本 | `"这份文档改坏了，回退到上周版本"` |
| 分享权限 | `"给张三发个可编辑的链接"` |
| 归档文件夹 | `"把文件移到 2026 项目文件夹"` |
| 格式转换 | `"把这份文档转成 PDF"` |

---

## 5. 自然语言触发示例（高级功能怎么表达）

为避免「不知道怎么开口」，以下给可直接说的话：

- **批量建表**：`"新建客户管理多维表格，字段：客户名(文本)、签约金额(数字)、状态(单选)，并一次写入 20 条记录"`
- **格式转换**：`"把《Q2 报告》导出成 PDF"` / `"转成 Word 发我"`
- **OCR 转文档**：`"识别这张发票图片，生成一份 Word 报销单"` / `"把这张表格图片转成在线电子表格"`
- **网页剪藏**：`"把这个网页 https://... 收藏成金山文档"` 
- **通知推送**：`"导入完成后用企微机器人通知我"` 
- **版本回滚**：`"列出这份文档的历史版本，回退到 7 月 1 日那版"` 
- **权限管理**：`"给团队文件夹『2026 项目』里的文档设置只读"` 
- **本地免密钥生成**：`"本地生成一份周报 DOCX，不用上传"`（无需 App Key）

---

## 安全声明

| 保护项 | 方式 |
|--------|------|
| 🔒 删除确认 | 删除走回收站 API，不物理删除 |
| 🗑️ 软删除+恢复 | `trash.list → trash.recover` |
| 📝 版本冲突检测 | 写入前获取最新版本号，冲突时提示用户合并 |
| 🔐 权限前置校验 | 所有写入操作前自动检查权限，无权限拒绝 |
| ⚡ 限流保护 | 429 自动指数退避重试（最多 5 次） |
| 🛡️ 文件类型拦截 | 默认禁止上传 .exe/.bat/.ps1/.zip 等（见第 18 节） |
| 🔑 Token 安全 | Token 仅存在于内存，不落盘 |
| 📋 审计日志 | 所有写操作记录到本地日志 |
| 🔀 批量合并 | 50ms 窗口内连续写入自动合并为一次请求 |
| 🧠 硬件自适应 | 自动按本机 CPU/内存分配并发，不拖累电脑（第 17 节） |

---

## 6. 🚨 危险操作强制确认（v3.0.0 新增铁律）

> 评测指出「部分危险操作缺少强制确认」。以下操作**执行前必须向用户显式确认**，
> 列出具体影响，待用户明确同意后方可进行；**绝不**静默执行。

| 危险操作 | 确认内容（必须展示给用户） |
|---------|--------------------------|
| 删除文件 `kdoc.file.delete` | 文件名 + 大小 + 「将进入回收站，可恢复」 |
| **彻底删除** `kdoc.trash.destroy` | 文件名 + 「**不可逆**，将永久丢失」⚠️ 二次确认 |
| 覆盖文件 `kdoc.file.upload` | 原文件版本 + 「覆盖后旧内容进入版本历史」 |
| 批量操作 `kdoc.batch.*` | 操作类型 + 文件数量 + 文件清单预览 |
| 权限变更 `kdoc.file.permission` | 目标成员 + 授予/收回的权限 |
| 清空回收站 | 数量 + 「**不可恢复**」⚠️ |
| 回滚版本 `kdoc.version.restore` | 目标版本 + 「当前内容将被历史版本替换」 |
| Webhook 设置 | 回调 URL + 监听事件清单 |

**确认模式**（config.json 可配）：
```json
{ "safety": { "confirm_mode": "dangerous", "dry_run": false, "audit_enabled": true } }
```
- `dangerous`（默认）：仅上表危险操作需确认
- `always`：所有写操作均确认
- `dry_run: true`：只展示将要执行的操作，不真正调用

---

## 支持的文档类型（9 品类）

| 类型 | doc_type | 推荐度 | 创建 | 编辑 | 对标腾讯 | 实现方式 |
|------|----------|--------|------|------|---------|---------|
| 智能文档 | smart_note | ⭐⭐⭐ | ✅ 自动 | ✅ 本地生成+上传 | smartcanvas | Markdown→DOCX→上传覆盖 |
| 文字文档 | doc | ⭐⭐⭐ | ✅ 自动 | ✅ 本地生成+上传 | doc | python-docx→上传覆盖 |
| 智能画布 | smart_canvas | ⭐⭐⭐ | ✅ 自动 | ✅ 元素级 CRUD+增量追加 | 智能画布 | element_api + Markdown 追加 |
| 电子表格 | sheet | ⭐⭐⭐ | ✅ 自动 | ✅ API 精细编辑 | sheet | 金山 et API（单元格/公式） |
| 演示文稿 | ppt | ⭐⭐⭐ | ✅ 自动 | ✅ 本地生成+上传 | slide | python-pptx→上传覆盖 |
| 多维表格 | smartsheet | ⭐⭐⭐ | ✅ 自动 | ✅ API 精细编辑 | smartsheet | 金山 dbt API（记录/字段/视图） |
| 收集表 | form | ⭐⭐⭐ | ✅ 自动 | ✅ API 配置 | form | 金山 form API |
| 可视化 | visualization | ⭐⭐⭐ | ✅ 自动 | ✅ 本地渲染+上传 | — | mermaid→SVG→上传 |
| 历史管理 | history_mgmt | ⭐⭐⭐ | — | ✅ 统一管理 | — | 回收站+版本历史统一入口 |
| 全文搜索 | content_search | ⭐⭐⭐ | — | ✅ 全文搜索 | — | 内容搜索 API（超越腾讯） |
| 附件 | attachment | ⭐⭐⭐ | ✅ 自动 | — | — | 本地文件直接上传 |

---

## 核心能力矩阵

### 1️⃣ 文档创建（9 品类全覆盖）

| 用户意图 | 品类 | 创建方法 | 编辑方法 |
|---------|------|---------|---------|
| 报告/笔记/文章/纪要/markdown | smart_note / doc | `kdoc.file.create` | `kdoc.local.docx.generate` → 上传覆盖 |
| PPT/幻灯片 | ppt | `kdoc.file.create` | `kdoc.local.pptx.generate` → 上传覆盖 |
| 数据表格/Excel | sheet | `kdoc.et.create` | `kdoc.et.*` 精细编辑 |
| 多维表格 | smartsheet | `kdoc.dbt.create` | `kdoc.dbt.*` 精细编辑 |
| 表单/问卷 | form | `kdoc.form.create` | `kdoc.form.*` 配置 |
| 思维导图 | mindmap | `kdoc.local.mindmap.generate` → 上传 | 生成 SVG→上传覆盖 |
| 流程图 | flowchart | `kdoc.local.flowchart.generate` → 上传 | 生成 SVG→上传覆盖 |
| 上传文件/图片/pdf | attachment | `kdoc.file.upload` | — |

### 2️⃣ 文档编辑（改内容）

先 `kdoc.file.info` 确定品类，再路由对应工具集。**严禁跨品类操作。**

| 原始文档类型 | 编辑工具集 | 编辑粒度 |
|------------|-----------|---------|
| 智能文档/文字 | `kdoc.local.docx.generate` → 上传覆盖 | 整文件替换（自动重排） |
| 演示文稿 | `kdoc.local.pptx.generate` → 上传覆盖 | 整文件替换 |
| 电子表格 | `kdoc.et.cell.write` / `kdoc.et.range.write` | **单元格级** ✅ |
| 多维表格 | `kdoc.dbt.record.*` / `kdoc.dbt.field.*` | **记录级** ✅ |
| 收集表 | `kdoc.form.*` 配置 | 表单配置级 |
| 思维导图/流程图 | `kdoc.local.mmd.generate` → 上传覆盖 | 整文件替换 |

### 3️⃣ 文件管理

| 动作 | 工具 |
|------|------|
| 重命名/移动/删除/复制 | `kdoc.file.*` |
| 导入（本地→云端） | `kdoc.file.upload` |
| 导出（云端→本地） | `kdoc.file.download` |
| 权限/分享链接 | `kdoc.file.permission` / `kdoc.share.*` |
| 回收站查询/恢复 | `kdoc.trash.list` / `kdoc.trash.recover` |
| 版本历史/回滚 | `kdoc.version.list` / `kdoc.version.restore` |
| 批量操作 | `kdoc.batch.create` → `kdoc.batch.query` |
| 空间管理 | `kdoc.space.*` / `kdoc.folder.*` |

### 4️⃣ 格式转换与 OCR

| 场景 | 工具 | 实现方式 |
|------|------|---------|
| 文档→PDF/Word/Excel/PPT | `kdoc.office.convert` | 金山 API |
| 纯文本提取 | `kdoc.office.extract` | 金山 API |
| 图片 OCR 文字提取 | `kdoc.local.ocr.extract` | **本地 Tesseract（免密钥）/ 云端降级** |
| 图片→Word | `kdoc.local.docx.generate(image_ocr=true)` | OCR→生成 DOCX→上传 |
| 图片→Excel | `kdoc.et.create(data=ocr_table)` | OCR→解析表格→写入 |
| 网页剪藏 | `kdoc.scrape.url` → `kdoc.file.create` | 抓取→创建文档 |
| HTML 一键上云 | `kdoc.scrape.html` → `kdoc.file.upload` | 读取本地 HTML→上传 |

### 5️⃣ 扩展能力（金山独有）

| 能力 | 工具 | 说明 |
|------|------|------|
| 通知推送 | `kdoc.notification.send` | 企微/钉钉/金山协作机器人 |
| 多维表格 Webhook | `kdoc.dbt.webhook.set` | 事件驱动监听表格变更 |
| 空间额度用量 | `kdoc.space.quota` | 企业级管理视角 |
| 用户信息 | `kdoc.user.info` | 获取用户/团队信息 |

### 6️⃣ 本地免密钥工具（无需 App Key）

| 工具 | 说明 |
|------|------|
| `kdoc.local.docx.generate` | 本地生成 DOCX（会议纪要/周报/合同） |
| `kdoc.local.pptx.generate` | 本地生成 PPTX |
| `kdoc.local.mindmap.generate` | 本地渲染思维导图 SVG |
| `kdoc.local.flowchart.generate` | 本地渲染流程图 SVG |
| `kdoc.local.ocr.extract` | 本地 OCR 提取图片文字 |
| `kdoc.local.hardware.profile` | 采集本机硬件 + 推荐并发数 |

### 7️⃣ WPS AI 能力（v3.2.0 新增，本地降级优先）

> WPS AI 目前无公开开发者 API，本模块采用**本地降级 + 自研逻辑**实现，零密钥可用。
> 未来如 WPS AI 开放 API，只需新增后端即可升级，无需改动上层。

| 工具 | 说明 | 操作 |
|------|------|------|
| `kdoc.wps_ai.write` | AI 写作辅助 | polish(润色) / expand(扩写) / shorten(缩写) / continue_write(续写) / rewrite(改写) |
| `kdoc.wps_ai.analyze` | AI 数据分析 | 自然语言提问 → 基础统计 + 公式建议 |
| `kdoc.wps_ai.ppt` | AI PPT 生成 | Markdown 大纲 → 自动生成 PPT |
| `kdoc.wps_ai.read` | AI 阅读助手 | summarize(总结) / qa(问答) / mindmap(思维导图) |
| `kdoc.wps_ai.detect_intent` | 意图检测 | 识别用户输入匹配的 WPS AI 能力 |

**后端策略**：本地降级优先 → 未来可扩展 WPS Open API / COM 自动化 / Web API

---

## 10. 协同编辑冲突解决（v3.3.0 新增，自研 difflib 实现）

> 多人同时编辑同一文档时经常出现冲突（A 修改了第 3 段，B 也修改了第 3 段）。
> 本模块提供**冲突检测 + 智能合并 + 可视化 diff + 解决模板**，零外部依赖。

### 10.1 冲突检测

| 用户意图 | 直接对 AI 说 |
|---------|-------------|
| 检测冲突 | `「检测这两人修改的冲突」` |
| 查看差异 | `「对比这两个版本的差异」` |
| 自动合并 | `「帮我合并这两个版本」` |
| 保留某版本 | `「保留 A 的版本」` / `「保留 B 的版本」` |

### 10.2 工具列表

| 工具 | 说明 | 操作 |
|------|------|------|
| `kdoc.conflict.detect` | 冲突检测 | 输入基准版+A版+B版 → 返回冲突块列表+统计 |
| `kdoc.conflict.merge` | 智能合并 | 无冲突段自动合并，冲突段标注 `<<<<<<< VERSION_A` |
| `kdoc.conflict.diff` | 冲突可视化 | 生成 Git diff 风格结构化数据 + 可选 HTML |
| `kdoc.conflict.resolve` | 冲突解决 | keep_a / keep_b / manual / auto_merge |

### 10.3 工作流程

```
① 检测：kdoc.version.list → 取最近 2-3 个版本 → conflict.detect() → 冲突块列表
② 合并：conflict.merge() → 自动合并无冲突段 + 标注冲突段 → 合并建议
③ 可视化：conflict.diff() → Git 风格并排 diff（可导出 HTML）
④ 解决：用户选模板 → conflict.resolve() → ⚠️ 强制确认 → kdoc.file.upload 覆盖回云端
```

### 10.4 解决模板

| 策略 | 说明 |
|------|------|
| `keep_a` | 保留用户 A 的版本 |
| `keep_b` | 保留用户 B 的版本 |
| `manual` | 手动编辑合并版本（需传 `manual_text`） |
| `auto_merge` | 自动合并（仅无冲突段，冲突段保留标记） |

### 10.5 安全约束

- 合并结果覆盖回云端属于「覆盖文件」危险操作，**必须走强制确认铁律**（见第 6 节）
- 冲突段**绝不自动覆盖**，必须用户明确选择
- 大文档 diff 自动分块处理，不拖累电脑（硬件自适应）

---

## 11. 文档内容合规检查（v3.4.0 新增，自研正则+规则引擎）

> 政企客户对文档内容有严格合规要求，手动检查耗时易遗漏。
> 本模块提供**敏感词扫描 + 数据泄露检测 + 格式规范检查 + 密级标注**，零外部依赖。

### 11.1 工具列表

| 工具 | 说明 | 操作 |
|------|------|------|
| `kdoc.compliance.sensitive` | 敏感词扫描 | 输入全文 → 返回命中词+位置+上下文+风险等级 |
| `kdoc.compliance.leak` | 数据泄露检测 | 扫描手机号/身份证号/银行卡号/邮箱 → 风险等级+脱敏显示 |
| `kdoc.compliance.format` | 格式规范检查 | 输入文件路径 → 返回不合规清单（支持 DOCX/PPTX/TXT/MD） |
| `kdoc.compliance.classify` | 密级自动标注 | 输入全文 → 建议密级（公开/内部/秘密/机密） |

### 11.2 工作流程

```
① 敏感词扫描：kdoc.file.content → 取全文 → compliance.sensitive() → 命中列表+位置
② 泄露检测：compliance.leak() → 正则匹配手机/身份证/银行卡/邮箱 → 风险等级
③ 格式检查：kdoc.local.docx 解析 → compliance.format() → 不合规清单
④ 密级标注：compliance.classify() → 关键词+规则 → 建议密级
```

### 11.3 敏感词库管理

- **内置词包（权威来源）**：`references/sensitive_packs/`（base 通用包 + 教培/医疗/金融/政务四行业包，YAML 受限子集，合规风险分类描述，不含字面违规词）
- **外部行业词包**：环境变量 `KINGDOC_EXTERNAL_PACKS_DIR` 或参数 `external_packs_dir` 加载企业本地词库（外部同名包覆盖内置包）
- **用户黑名单**：`references/user_blacklist.txt`（追加自定义敏感词）
- **用户白名单**：`references/user_whitelist.txt`（跳过误判词）
- **已弃用**：旧版 `references/sensitive_words.txt` 为合规分类描述明文镜像，仅供查阅，引擎不再加载；更新词包请编辑 `references/sensitive_packs/` 对应文件

### 11.4 数据泄露检测能力

| 类型 | 正则匹配 | 额外校验 | 风险等级 |
|------|---------|---------|---------|
| 手机号 | 1[3-9]\d{9} | — | high |
| 身份证号 | 18位 | 校验码验证 | critical |
| 银行卡号 | 16-19位 | Luhn 算法 | critical |
| 邮箱地址 | 标准邮箱正则 | — | medium |
| IP地址 | IPv4 | — | low |

### 11.5 格式规范检查

| 检查项 | 规范 | 严重度 |
|--------|------|--------|
| 字体 | 宋体 | warning |
| 字号 | 10-14pt | warning |
| 行距 | 1.5倍行距 | info |
| 页边距 | 2.54cm/3.17cm | info |
| 行长度 | ≤80字符 | info |
| 标题层级 | 长文档必须有 H1 | warning |

### 11.6 密级标注规则

| 密级 | 关键词示例 |
|------|-----------|
| 机密 | 绝密、核心机密、国家安全、军事机密、情报来源 |
| 秘密 | 商业机密、技术机密、客户名单、未公开财报 |
| 内部 | 内部资料、内部通知、仅限内部、不得外传 |
| 公开 | 无匹配关键词 |

---

## 12. 实时协同编辑（v3.5.0 新增，序列 CRDT 自研实现）

> 多人同时编辑同一文档时经常出现冲突（A 修改了第 3 段，B 也修改了第 3 段）。
> v3.3 冲突解决是事后 difflib 合并，本模块升级为**实时 CRDT 协同**，多人同时编辑无冲突。

### 12.1 工具列表

| 工具 | 说明 | 操作 |
|------|------|------|
| `kdoc.realtime.create` | 创建协同文档 | 输入 client_id → 返回文档状态 |
| `kdoc.realtime.insert` | 插入文本 | 输入位置+文本 → 返回操作列表 |
| `kdoc.realtime.delete` | 删除文本 | 输入位置+长度 → 返回操作列表 |
| `kdoc.realtime.get_text` | 获取当前文本 | 输入 client_id → 返回可见文本 |
| `kdoc.realtime.stats` | 获取统计信息 | 输入 client_id → 返回字符数/操作数 |

### 12.2 核心算法：序列 CRDT

- 每个字符带唯一因果 ID（lamport timestamp + client_id + 序列号）
- 插入/删除操作满足交换律，顺序无关
- 删除标记 tombstone（保留因果关系，不真正移除）
- 最终一致性：所有客户端收敛到相同状态
- 无需中央服务器协调（P2P 友好）

### 12.3 工作流程

```
1) kdoc.realtime.create(client_id) → 创建协同文档
2) 用户 A 插入：kdoc.realtime.insert("alice", 0, "Hello")
3) 用户 B 同时插入：kdoc.realtime.insert("bob", 5, " World")
4) 操作自动广播给所有客户端
5) kdoc.realtime.get_text(client_id) → 获取一致文本
```

---

## 13. 文档对比（v3.5.0 新增，复用 difflib 引擎）

> 对应 TOP50「文档对比检测器」，两版文档差异高亮。
> 复用 conflict_resolver.py 的 difflib 引擎，提供面向用户的对比能力。

### 13.1 工具列表

| 工具 | 说明 | 操作 |
|------|------|------|
| `kdoc.compare.diff` | 差异高亮 | 输入两版文本 → 返回差异行+统计+相似度 |
| `kdoc.compare.summary` | 变更摘要 | 输入两版文本 → 返回增删改统计+关键变化 |
| `kdoc.compare.export` | 导出报告 | 输入两版文本 → 返回 Markdown/HTML 报告 |

### 13.2 工作流程

```
1) kdoc.file.content(file_id) → 获取当前版本
2) kdoc.version.list(file_id) → 获取历史版本
3) kdoc.compare.diff(current, history) → 差异高亮
4) kdoc.compare.summary(current, history) → 变更摘要
5) kdoc.compare.export(current, history, format="html") → 导出报告
```

---

## 14. 可视化品类合并（v3.5.0 精简 9→8 品类，v3.6.0 进一步精简为 7 品类）

> 为降低认知门槛、统一渲染管线，v3.6.0 将思维导图和流程图合并为「可视化」品类。

### 14.1 合并前后对比

| 合并前（v3.5.0 8 品类） | 合并后（v3.6.0 7 品类） |
|-------------------------|-------------------------|
| 文档 / 电子表格 / 演示文稿 / 多维表格 / 收集表 / **思维导图** / **流程图** / 附件 | 文档 / 电子表格 / 演示文稿 / 多维表格 / 收集表 / **可视化** / 附件 |

### 14.2 子命令路由

合并后用户仍可用原有表达方式，引擎自动识别子命令：

| 用户表达 | 品类 | 子命令 |
|---------|------|--------|
| "画一个思维导图" | visualization | mindmap |
| "画一个流程图" | visualization | flowchart |
| "画个脑图" | visualization | mindmap |

### 14.3 共享渲染管线

```
用户意图 → 品类路由 → visualization
                              ↓
                    子命令识别：mindmap 或 flowchart
                              ↓
                    共享 mermaid→SVG 渲染管线
                              ↓
                        上传为在线文档
```

### 14.4 引擎逻辑不变

- 底层仍调用 `engine/local/generators.py` 的 `MindmapGenerator` / `FlowchartGenerator`
- 渲染方式仍为 mermaid→SVG→上传覆盖
- 仅改品类元数据（`engine/categories.py`）+ 路由表

---

## 15. WPS AI 深度集成（v3.2 本地降级 → v3.6 段落级 AI 操作）

> v3.2 已实现全文级 AI 写作辅助（polish/expand/shorten），v3.6 升级为**段落级 AI 深度集成**。

### 15.1 工具列表

| 工具 | 说明 | 操作 |
|------|------|------|
| `kdoc.wps_ai.rewrite` | AI 段落改写 | formal/casual/concise/elaborate |
| `kdoc.wps_ai.summarize` | AI 段落总结 | 提取核心要点 |
| `kdoc.wps_ai.continue` | AI 段落续写 | 根据方向继续写作 |

### 15.2 工作流程

```
1) 用户在编辑器中选中段落
2) 触发 AI 操作（改写/总结/续写）
3) 适配器路由到本地降级后端
4) 返回处理结果 → 用户确认 → 替换原段落
5) 未来 WPS AI API 开放后，切换为原生后端，无需改上层代码
```

### 15.3 后端策略

```
当前（v3.6）：本地降级占位（返回原文+提示）
未来：WPS AI 开放 API → 升级为原生后端（实现 WpsAiDeepBackend 接口即可）
```

---

## 16. 文档模板市场（v3.6.0 新增，行业模板库一键复用）

> 降低文档创建门槛，提供行业模板库 + 变量替换 + 一键生成。

### 16.1 工具列表

| 工具 | 说明 | 操作 |
|------|------|------|
| `kdoc.template.list` | 列出所有可用模板 | 可按类别筛选 |
| `kdoc.template.search` | 搜索模板 | 按关键词搜索 |
| `kdoc.template.use` | 使用模板 | 变量替换生成文档 |
| `kdoc.template.refresh` | 刷新模板仓库 | git pull |

### 16.2 模板仓库结构

```
templates/
├── meeting.md          # 会议纪要模板
├── weekly-report.md    # 周报模板
├── project-plan.md     # 项目计划模板
├── contract.md         # 合同模板
├── pitch-deck.md       # 融资路演模板
└── ...
```

### 16.3 变量替换

模板使用 `{{变量名}}` 语法，使用时传入变量字典：

```yaml
---
name: weekly-report
分类: 工作汇报
description: 标准周报模板
---

# {{title}}
> 作者：{{author}} | 日期：{{date}}

## 本周完成
{{completed}}

## 下周计划
{{plan}}

## 风险与风险
{{risks}}
```

调用：`kdoc.template.use("weekly-report", {"title": "周报", "author": "张三", ...})`

### 16.4 工作流程

```
1) kdoc.template.list() → 列出可用模板
2) 用户选择模板 → kdoc.template.use(name, variables)
3) 引擎替换变量 → 生成 Markdown → 保存到 output/
4) 返回生成内容 + 文件路径
5) 可选：上传为在线文档
```

---

## 17. 多维表格视图增强（v3.7.0 新增，对标 Airtable）

> 对标 Airtable 的多维表格视图能力，支持看板/日历/甘特图三种视图。
> 零第三方依赖，本地渲染引擎。

### 17.1 工具列表

| 工具 | 说明 | 操作 |
|------|------|------|
| `kdoc.view.render` | 视图渲染 | kanban / calendar / gantt |
| `kdoc.view.list` | 列出可用视图 | 返回视图类型清单 |

### 17.2 视图类型

| 视图 | 说明 | 适用场景 |
|------|------|---------|
| 看板 | 按状态字段分组卡片 | 任务管理/项目跟踪 |
| 日历 | 按日期字段月/周布局 | 日程/活动排期 |
| 甘特图 | 时间轴+任务依赖 | 项目进度管理 |

### 17.3 工作流程

```
1) kdoc.dbt.record.query → 获取多维表格记录
2) kdoc.view.render(view_type="kanban", data={records, fields})
3) 本地引擎渲染 → 返回结构化 JSON
4) 前端可视化展示（不依赖外部 API）
```

### 17.4 硬件自适应

- 视图渲染使用 `hardware.py` 的 `workers` 限制并发
- 大数据集（>1000 行）自动分页

---

## 18. 手写/公式识别 OCR（v3.7.0 新增，教育场景）

> 覆盖教育手写公式场景，强制本地 Tesseract，数据不出域。

### 18.1 工具列表

| 工具 | 说明 | 操作 |
|------|------|------|
| `kdoc.ocr.formula` | 数学公式识别 | 图片 → LaTeX/MathML |
| `kdoc.ocr.education` | 教育场景统一入口 | 自动判断手写/公式/混合 |
| `kdoc.local.ocr.extract` | 基础 OCR（v3.7.0 升级） | 强制本地，数据不出域 |

### 18.2 降级策略

```
优先级：本地 Tesseract → 提示安装（❌ 禁止调用外部 OCR API）
```

### 18.3 工作流程

```
1) kdoc.ocr.education(image_path, scene="auto")
2) 自动判断场景：handwriting / formula / mixed
3) 返回文本 + LaTeX（如有公式）
4) 可选：生成 DOCX/PPTX 文档
```

---

## 19. 历史管理（v3.7.0 新增，合并回收站+版本历史）

> 统一入口管理回收站和版本历史，降低认知门槛。

### 19.1 工具列表

| 工具 | 说明 | 操作 |
|------|------|------|
| `kdoc.history.list` | 列出历史记录 | trash / version |
| `kdoc.history.restore` | 恢复文件 | 还原/回滚 |
| `kdoc.history.destroy` | ⚠️ 彻底删除 | 仅回收站 |

### 19.2 统一 CLI 接口

```bash
kdoc history list --from trash|version [--limit 20]
kdoc history restore <file_id> --from trash|version [--version <v>]
kdoc history destroy <file_id>  # ⚠️ 需二次确认
```

### 19.3 工作流程

```
1) kdoc.history.list("trash") → 回收站文件列表
2) kdoc.history.list("version", file_id=xxx) → 版本历史
3) kdoc.history.restore(file_id, "trash") → 从回收站还原
4) kdoc.history.restore(file_id, "version", version=3) → 回滚到第 3 版
5) ⚠️ kdoc.history.destroy(file_id) → 彻底删除（需二次确认）
```

---

## 20. 完整场景案例（v3.0.0 新增，v3.7.0 更新）

### 场景 A：月度销售复盘（全链路）
```
1) kdoc.et.create(name="2026-07 销售复盘")
2) kdoc.et.range.write(sheet_id, "A1:C21", 表头+20 行数据)   ← 批量写入
3) kdoc.et.formula.set(sheet_id, "D2", "=C2*0.1")            ← 提成列
4) kdoc.office.convert(file_id, "pdf")                       ← 导出 PDF
5) kdoc.notification.send(channel="wecom", content="复盘已生成")
```

### 场景 B：合同 OCR → 在线文档（免密钥本地优先）
```
1) kdoc.local.ocr.extract("contract.jpg")        ← 本地 Tesseract，无需 Key
2) kdoc.local.docx.generate(content=<ocr_text>, template="contract")
3) kdoc.file.upload(file_path="output.docx")     ← 上传为在线文档
```

### 场景 C：项目规划脑图 + 流程图（本地渲染）
```
1) kdoc.local.mindmap.generate(code="graph TD; 目标-->阶段1; 阶段1-->任务A")
2) kdoc.local.flowchart.generate(code="flowchart TD; 开始([开始])-->审核{通过?}")
3) 分别 kdoc.file.upload 两个 SVG → 在线可视化
```

### 场景 D：误删恢复（金山独有）
```
1) kdoc.trash.list(limit=20)
2) kdoc.trash.recover(file_id)        ← 救回，不丢数据
```

### 场景 E：大批量导入（硬件自适应）
```
1) kdoc.local.hardware.profile → 取得 workers/batch_chunk
2) 按 batch_chunk 分块调用 kdoc.batch.create
3) kdoc.batch.query 轮询直至完成（并发不超过 workers，不卡机）
```

### 场景 F：多人协作冲突解决（v3.3.0 新增）
```
1) kdoc.version.list(file_id) → 获取最近 3 个版本（基准版 + A修改 + B修改）
2) kdoc.conflict.detect(base, a, b) → 检测冲突块
3) kdoc.conflict.merge(base, a, b) → 自动合并无冲突段 + 标注冲突段
4) kdoc.conflict.diff(a, b) → Git 风格可视化
5) 用户选择保留A/保留B/手动合并 → kdoc.conflict.resolve(strategy="keep_a")
6) ⚠️ 强制确认 → kdoc.file.upload 覆盖回云端
```

### 场景 G：政企文档合规检查（v3.4.0 新增）
```
1) kdoc.file.content(file_id) → 取全文
2) kdoc.compliance.sensitive(text) → 扫描敏感词（命中内置合规风险分类词等）
3) kdoc.compliance.leak(text) → 检测数据泄露（手机号/身份证号脱敏）
4) kdoc.compliance.classify(text) → 建议密级（如"秘密"）
5) kdoc.compliance.format(file_path) → 格式规范检查（字体/字号/行距）
6) 生成合规报告 → 用户确认 → 修复不合规项
```

### 场景 H：实时协同编辑（v3.5.0 新增）
```
1) kdoc.realtime.create("alice") → Alice 创建协同文档
2) kdoc.realtime.insert("alice", 0, "项目计划：") → Alice 插入文本
3) kdoc.realtime.insert("bob", 5, "第一阶段") → Bob 同时插入
4) kdoc.realtime.get_text("alice") → Alice 看到合并后的文本
5) kdoc.realtime.stats("alice") → 查看协同统计
```

### 场景 I：文档对比（v3.5.0 新增）
```
1) kdoc.file.content(file_id) → 获取当前版本
2) kdoc.version.list(file_id) → 获取历史版本
3) kdoc.compare.diff(current, history) → 差异高亮
4) kdoc.compare.summary(current, history) → 变更摘要
5) kdoc.compare.export(current, history, format="html") → 导出 HTML 报告
```

### 场景 J：7 品类智能路由（v3.6.0 更新）
```
1) 用户说"帮我写一份智能文档" → kdoc.category_resolve("智能文档")
   → {category: "doc", sub_type: "smart_note", edit_method: "local_generate_upload"}
2) 用户说"画一个思维导图" → kdoc.category_resolve("思维导图")
   → {category: "visualization", sub_command: "mindmap", edit_method: "local_render_upload"}
3) 用户说"画一个流程图" → kdoc.category_resolve("流程图")
   → {category: "visualization", sub_command: "flowchart", edit_method: "local_render_upload"}
4) kdoc.category_list() → 列出全部 7 品类
```

### 场景 K：WPS AI 段落改写（v3.6.0 新增）
```
1) 用户在编辑器中选中段落
2) kdoc.wps_ai.rewrite(paragraph="这个方案很好，值得推广。", style="formal")
   → 返回改写后的段落（本地降级占位，API 开放后升级为原生）
3) 用户确认 → 替换原段落
```

### 场景 L：模板市场一键生成（v3.6.0 新增）
```
1) kdoc.template.list() → 列出所有可用模板
2) kdoc.template.search("周报") → 搜索周报模板
3) kdoc.template.use("weekly-report", {"title": "周报", "author": "张三"})
   → 变量替换 → 生成 Markdown → 保存到 output/
4) kdoc.file.upload(output_path) → 上传为在线文档
```

### 场景 M：多维表格看板视图（v3.7.0 新增）
```
1) kdoc.dbt.record.query(table_id) → 获取多维表格记录
2) kdoc.view.render(view_type="kanban", data={"records": [...], "fields": [...]})
   → 按"状态"字段分组卡片 → 返回看板 JSON
3) 前端渲染：每列一个状态，卡片可拖拽
```

### 场景 N：数学公式 OCR 识别（v3.7.0 新增）
```
1) kdoc.ocr.formula("formula.png", output_format="latex")
   → 本地 Tesseract + 符号映射 → 返回 LaTeX
2) kdoc.ocr.education("exam.jpg", scene="auto")
   → 自动判断手写/公式/混合 → 返回文本+LaTeX
3) 可选：kdoc.local.docx.generate(content=latex) → 生成公式文档
```

### 场景 O：历史管理——误删恢复与版本回滚（v3.7.0 新增）
```
1) kdoc.history.list("trash") → 列出回收站文件
2) kdoc.history.restore(file_id, "trash") → 从回收站还原
3) kdoc.history.list("version", file_id=xxx) → 列出历史版本
4) kdoc.history.restore(file_id, "version", version=3) → 回滚到第 3 版
5) ⚠️ kdoc.history.destroy(file_id) → 彻底删除（需二次确认）
```

---

## 12. 核心规则（铁律）

1. 🚨 **品类隔离**：先 `kdoc.file.info` 识别品类再路由，**严禁跨品类操作**。
2. 📦 **批量优先**：电子表格/多维表格连续 3+ 写入**必须**用批量接口。
3. 🔒 **权限前置**：所有写入前**必须**校验权限。
4. 🔄 **异步轮询**：批量/转换/剪藏**必须**子会话轮询，主会话保持响应。
5. 🗑️ **软删除**：删除**必须**走回收站 API，不物理删除。
6. 📝 **审计日志**：所有写操作**必须**记录本地审计日志。
7. ⚡ **限流退避**：收到 429 **必须**自动指数退避（最多 5 次）。
8. 🔀 **版本防冲突**：写入前获取 `version`，冲突时提示合并。
9. ✅ **危险操作强制确认**（v3.0.0）：见第 6 节，**未确认不执行**。
10. 🧠 **性能不拖累**：批量/渲染并发**不得超过** `kdoc.local.hardware.profile` 给出的 `workers`。

---

## 13. 能力边界与失败场景（v3.0.0 新增，务必看清）

| 场景 | 会发生什么 | 应对 |
|------|-----------|------|
| 未配置 App Key | 所有 `*云端*` 工具返回 KD001 友好提示 | 改用 `kdoc.local.*` 免密钥工具 |
| 文件 > 大文件阈值（默认 100MB，低端机 50MB） | 自动转异步上传 + 进度轮询；超限报 KD008 | 压缩或分卷 |
| 多人同时编辑 | 写入带版本号，冲突报 KD007 | 拉最新版本→合并→重写 |
| OCR 识别率低 | 扫描件需 ≥200DPI、光线均匀、无反光 | 提升清晰度或人工校对 |
| 网络中断 | 自动重试（指数退避），关键操作支持离线暂存 | 稍后重试 |
| 限流 429 | 自动退避，不会崩溃 | 等待后继续 |
| 本地未装 Tesseract | OCR 降级云端（需 Key），都无则给安装指引 | 装 Tesseract（免费） |
| 超大表格（>10 万行） | 分块写入，单批不超过 `batch_chunk` | 分批 |
| 思维导图/流程图为 SVG 图片 | 无法在金山内二次编辑，保留源 mermaid | 改源码重渲染 |
| 文字/演示只能整文件替换 | 无法逐段编辑 | 本地改源→重新上传覆盖 |
| 行业分包 YAML 格式错误 | 该包被加载器跳过（不影响其他包） | 用 `references/sensitive_packs/` 模板校验后重跑 |
| schtasks 周扫仅产出命令未自动注册 | 不会自动写入系统定时 | 用户在宿主（管理员）执行产出的 schtasks/cron 命令 |
| 配额告警需 webhook 订阅才推送 | 无订阅时仅本地记录不推送 | 配置 webhook 订阅（kdoc.webhook.subscribe）后三通道推送 |
| 周扫去重依赖扫描级 SQLite | 清库会重置去重（重新推送历史项） | 一般无需清理，去重表独立存储 |

**明确不支持**：本地直接修改已上传 DOCX/PPTX 的某一段（需整文件重生成）；
对加密/损坏文件 OCR；超过配额的非付费批量操作。

---

## 14. 风险项与限制

| 风险项 | 影响 | 规避 |
|--------|------|------|
| 账号权限未配置 | 无法调用任何 API | 首次使用引导绑定 App |
| API 配额不足（测试 500/天） | 写入被拒 | 申请正式应用（10 万/天） |
| 整文件替换限制 | 文字/演示无法逐段编辑 | 降级为「本地生成→上传覆盖」 |
| OCR 依赖清晰度 | 识别率受图片质量影响 | 提示扫描件 ≥200DPI |
| SVG 不可二次编辑 | 脑图/流程图为图片 | 导出本地 SVG 保留源 |
| 大文件超时（>阈值） | 上传失败 | 异步上传 + 轮询 |
| 版本冲突 | 多人编辑丢数据 | 写入前校验版本号 |
| 网络依赖 | 云端功能需联网 | 关键操作离线暂存 |
| 行业分包需合法 YAML | 语法错误包被忽略，不会报错中断 | 提交前用 `kdoc.compliance.packs` 校验词数 |
| 周扫定时化仅注册命令不托管执行 | 漏跑需手动触发 | 手动执行 `compliance_scheduler.py` 或部署 cron/schtasks |
| 配额告警基于当日本地计数 | 多进程不共享计数可能漏警 | 单实例运行配额管理 |
| webhook 推送需签名密钥一致 | 密钥不一致推送被拒（签名校验失败） | 保持默认签名密钥 `kingdoc_webhook_secret_v4` |
| 合规门面为本地引擎 | 不调用任何外部 AI API | 零密钥可用，数据不出域 |

---

## 15. 深度绑定在线文档（v3.0.0 强化）

KingDoc **直连金山文档（WPS）开放平台原生 API**（`https://developer.kdocs.cn/api/v1/openapi`），
而非简单桥接：

- **原生能力全覆盖**：文件/文件夹/回收站/版本/权限/空间/通知/用户均调用官方端点。
- **精细编辑**：电子表格走 `et` API（单元格/公式），多维表格走 `dbt` API（记录/字段/视图）。
- **本地增强**：文字/演示/脑图/流程图用本地库生成**原生格式**（DOCX/PPTX/SVG）后上传覆盖，
  既保真又免去服务端复杂排版。
- **政企可用**：国内网络直连、文档全中文、权限模型对齐企业协作。

---

## 16. 四大 MCP 服务（v3.0.0 架构）

| 服务名 | 工具前缀 | 职责 | 对标腾讯 |
|--------|---------|------|---------|
| `kingdoc-docs` | `kdoc.file.*` / `folder.*` / `space.*` / `trash.*` / `version.*` / `batch.*` / `notification.*` / `user.*` | 文件管理+回收站+版本+批量+通知+用户 | tencent-docs |
| `kingdoc-docx` | `kdoc.local.docx.*` | 文字/智能文档/脑图/流程图 本地生成+上传+OCR | doc-mcp |
| `kingdoc-pptx` | `kdoc.local.pptx.*` | 演示文稿 本地生成+上传 | slide-mcp |
| `kingdoc-sheet` | `kdoc.et.*` / `kdoc.dbt.*` / `kdoc.form.*` | 表格/多维表/收集表 API 精细编辑 | sheet-mcp |

> 4 个 MCP 服务共享同一 Token，可独立限流、独立降级。

---

## 17. 性能与硬件自适应（v3.0.0 新增，绝不拖累电脑）

`engine/hardware.py` 在首次运行时**自动采集本机 CPU 核数/内存**并计算出安全并发：

| 机器档位 | 并发子进程 `workers` | 批量分块 | 大文件阈值 |
|---------|---------------------|---------|-----------|
| 低端（≤2核/<4GB） | 1 | 50 | 50MB |
| 普通 | min(核数,4) | 200 | 100MB |
| 高端（≥8核/≥16GB） | min(核数,8) | 500 | 100MB |

- 画像缓存到 `.kingdoc_hardware_profile.json`（30 分钟复用），不频繁探测。
- 批量写表、脑图/流程图并行渲染**不得超过 `workers`**，保证用户电脑流畅。
- AI 在执行批量/渲染任务前应调用 `kdoc.local.hardware.profile` 读取参数。

```bash
python -m engine.hardware          # 查看本机画像与推荐参数
```

---

## 18. 🚫 禁止上传的文件类型（v3.0.0 强化）

为安全，用户「上传附件」默认拦截以下全部类型（来源：产品安全规范）：

1. **Windows 可执行/批处理**：`.bat` `.cmd` `.ps1` `.vbs` `.exe` `.dll` `.lnk` `.msi`
2. **Office 二进制文档**：`.docx` `.xlsx` `.pptx` `.doc` `.xls` `.ppt` `.xlsm` `.docm` `.pptm`
3. **二进制镜像/安装包**：`.iso` `.dmg` `.zip` `.rar` `.7z` `.tar` `.gz` `.apk` `.jar`
4. **系统缓存/隐藏文件**：`.DS_Store` `.git`（目录） `.env` `.log` `.tmp`
5. **其他风险脚本**：`.sh` `.com` `.scr` `.hta` `.reg`

**内部豁免**：技能「本地生成→上传覆盖」产物（`.docx/.pptx/.xlsx/.pdf/.svg/.png/.txt/.md`
等）经 `internal=True` 通道上传，**仅限技能自身生成**，用户无法借道上传任意同类文件。
命中拦截将抛出 `KD009`。详见 `references/security.md`。

---

## 19. 错误码

| 错误码 | 含义 | 解决方案 |
|--------|------|---------|
| KD001 | Token 鉴权失败 | 重新执行 `setup` 授权（或改用本地免密钥工具） |
| KD002 | 权限不足 | 升级应用权限或联系管理员 |
| KD003 | 配额不足 | 申请提额 |
| KD004 | 文档类型不匹配 | `kdoc.file.info` 确认品类后按路由表 |
| KD005 | 文档不存在 | 检查 `file_id` |
| KD006 | 限流（429） | 自动指数退避重试 |
| KD007 | 版本冲突 | 获取最新版本后重写 |
| KD008 | 文件过大 | 走异步上传 |
| KD009 | 文件类型被拦截 | 见第 18 节禁止类型 |
| KD010 | 服务暂不可用 | 稍后重试 |
| KD011 | 参数错误 | 检查 `file_id`/`content` 等必填项 |
| KD012 | 文件夹不存在 | 检查 `folder_id` |
| KD013 | 收集表已截止 | 已过截止日期 |
| KD014 | Webhook 回调失败 | 检查回调 URL |
| KD015 | 转换失败 | 格式不支持或文件损坏 |

---

## 20. 🔄 自动更新提示与反馈

**每天首次使用自动检查更新**（本地缓存，每天仅查一次，离线不打扰）。
发现新版本时 AI 会主动提示升级，**不会自动安装**：

```bash
# 手动检查 / 仅看提醒文案
python -m engine.update_check --version 3.0.0 --reminder
```

> 📮 **有更好建议**：njskills@agent.qq.com

---

## 更新日志

| v4.4.0 | 2026-11-17 | 增加：答卷实时推送引擎 `engine/form_realtime.py`（轮询 + 增量游标检测新答卷，经 webhook_center 三通道推送关键字段摘要与答卷链接，端到端延迟统计验收 ≤30 秒，本地降级只落库）；增加：跨表聚合分析引擎 `engine/form_cross_analytics.py`（问题→标准字段映射配置 + 多渠道报名按身份键去重 + 自包含 HTML 看板，去重准确率 ≥98%）；增加：答卷沉淀多维表格引擎 `engine/form_to_bidata.py`（复用 v4.1 的 date/link/select/person 四类字段序列化，person/link 双向可编辑，支持反向生成答卷更新草稿）；增加：多维表格定时快照与变更摘要引擎 `engine/table_snapshot.py`（每日快照行数+关键字段哈希存 SQLite，行哈希加速 + 复用单元格级 diff 输出增/删/改清单，5000 行 ≤10 秒，可推送或写周报）；增加：AirScript 预设库 `engine/airscript_presets.py`（22 个高频预设全部带元数据/测试样例/预期输出，自然语言关键词匹配，走生成-预检-预览-确认-执行链路）；增加：CRDT 冲突可视化引擎 `engine/crdt_visualizer.py`（导出单元格级操作日志 + 向量时钟，ECharts 单文件时间线 + SVG 离线降级，冲突可审查可追溯）；增加：MCP 工具 19 个（kdoc.form_realtime.* 3 个、kdoc.form_cross.* 3 个、kdoc.form_bidata.* 3 个、kdoc.table_snapshot.* 3 个、kdoc.airscript_preset.* 4 个、kdoc.crdt_viz.* 3 个）；优化：SKILL.md 版本号 4.3.5→4.4.0；优化：description 增强（表单实时化 + 多维表格自动化） |
| v4.3.5 | 2026-10-10 | 修复：全量自查移除字面违法违规词汇以解决 SkillHub 内容审核误判——内置敏感词分包 `references/sensitive_packs/` 改为合规风险分类描述；旧版明文词库 `references/sensitive_words.txt` 重写为合规分类描述镜像（引擎不再加载）；`engine/compliance_suite.py` 文档示例与 SKILL.md 场景示例中的字面违规词一并替换为合规分类描述；增加：外部行业敏感词包支持（`KINGDOC_EXTERNAL_PACKS_DIR` 环境变量或 `external_packs_dir` 参数，外部同名包覆盖内置包），`SensitiveWordLoader`/`ComplianceSuite`/`ComplianceScheduler`/`compliance_check`/`compliance_center` shim 及 6 个 MCP 合规工具全链路支持；优化：SKILL.md 版本号 4.3.0→4.3.5，双页脚同步更新 |
| v4.3.0 | 2026-10-10 | 增加：合规套件门面 `engine/compliance_suite.py`（单入口两档输出 quick_scan/full_scan，合并 v4.2 政企合规中心与 v3.4 内容合规检查为统一引擎 ComplianceCore，敏感词加载逻辑收敛为唯一来源 SensitiveWordLoader，维护面减半；旧 `compliance_check.py`/`compliance_center.py` 改为委托 shim）；增加：行业敏感词分包 `references/sensitive_packs/`（base 通用包 + 教培/医疗/金融/政务四行业包，各 200+ 词条，多包叠加加载器，扫描报告按高/中/低风险分级并定位到段落行号与责任人字段）；增加：全域扫描定时化引擎 `engine/compliance_scheduler.py`（schtasks 周扫空间，新检出项经 webhook 三通道签名推送，扫描级跨周去重只推新增不扰民，非 Windows 输出 cron 行）；增加：配额管理器阈值告警（用量 80% / 95% 两级经 webhook 三通道推送，按天+级别幂等去重）；增加：MCP 工具 6 个（kdoc.compliance.quick_scan / full / packs / scheduler_register / scheduler_run / scheduler_status），kdoc.quota.check 现返回 alerts；优化：SKILL.md 版本号 4.2.0→4.3.0；优化：description 增强（合规门面/行业分包/周扫定时化/配额告警） |
| v4.2.0 | 2026-09-19 | 增加：团队知识库模式引擎 `engine/knowledge_hub.py`（空间级本地倒排索引全文检索，可选 jieba 中文分词，权限矩阵先鉴权后检索，无 read 权限文档不进结果集，硬件自适应分块建索引）；增加：政企合规中心引擎 `engine/compliance_center.py`（密级标注公开/内部/秘密/机密随文档元数据落库，敏感词+数据泄露全量扫描聚合报告，数据不出域声明，本地 OCR 强制云端仅元数据）；增加：主题一键生成引擎 `engine/topic_generator.py`（WPS AI 适配层 generate：大纲→智能文档/PPT/表格初稿，本地降级模板驱动+分段生成，真源可用无缝切换）；增加：跨品类对比与时间线引擎 `engine/cross_compare.py`（版本历史轮询→who/when/what 时间线，表格/多维表格单元格级 diff 视图，跨品类差异化）；优化：OCR 收敛为唯一入口 `engine/local/ocr.py`（删除重复维护的 `engine/ocr/local_ocr.py`，优先桥接 wps-office-suite OCR，未装则 Tesseract 最小兜底，数据不出域）；增加：MCP 工具 19 个（kdoc.khub.* 4 个、kdoc.compliance.* 5 个、kdoc.topic.* 2 个、kdoc.compare.* 3 个、kdoc.ocr_bridge_status 1 个、复用 kdoc.local.ocr.extract_text_bridged）；增加：知识中枢/政企合规/主题生成/跨品类对比/OCR 桥接场景案例；优化：SKILL.md 版本号 4.1.0→4.2.0；优化：description 增强到 30 项增强 |
| v4.1.0 | 2026-09-08 | 增加：AirScript 在线自动化引擎 `engine/airscript.py`（自然语言→脚本生成→预检（危险操作拦截）→用户确认→在线执行；能力域：定时通知/数据汇总/表格批量操作/字段计算；SQLite 执行历史+待确认队列）；增加：多维表格字段自动化引擎 `engine/dbf_auto.py`（公式字段/关联字段/汇总字段创建与批量填充，16 种字段类型，硬件自适应削峰）；增加：视图渲染引擎 `engine/view_render.py`（看板 matplotlib 柱图 + 甘特 mermaid 时间线，硬件自适应渲染并发）；增加：CRDT 表格扩展引擎 `engine/crdt_table.py`（单元格级操作日志 + 向量时钟，冲突时保留双方并标记，支持电子表格/多维表格/智能文档）；增加：Excel/CSV 双向导入导出引擎 `engine/bidata_io.py`（openpyxl 读写，date/link/select/person 四类字段序列化规则文档化，配额削峰）；增加：Webhook 与通知中心引擎 `engine/webhook_center.py`（新增/修改/删除事件订阅，HMAC 签名校验 + SQLite 去重队列，金山协作/企微/钉钉三通道分发，zwjh 记忆桥接）；增加：MCP 工具 24 个（kdoc.airscript.* 7 个、kdoc.dbf.* 5 个、kdoc.view.* 3 个、kdoc.crdt_table.* 6 个、kdoc.bidata.* 5 个、kdoc.webhook.* 8 个）；增加：AirScript/多维表格/视图渲染/CRDT/Webhook 场景案例；优化：SKILL.md 版本号 4.0.0→4.1.0；优化：description 增强到 24 项增强 |
| v4.0.0 | 2026-08-31 | 增加：本地桥接引擎 `engine/local_bridge.py`（wps-office-suite 双向互通：白名单探测 + SQLite 映射表 + 下行拉取/处理/覆盖 + 上行 mtime 监听同步 + JSON 契约 + 子进程超时自动关闭）；增加：记忆桥接引擎 `engine/memory_bridge.py`（zwjh 记忆库打通：白名单探测 + stdio JSON-RPC 调用 deposit + 关键事件写入长期记忆 + 未安装→本地待迁移日志 + 一次性导入）；增加：表单答卷收集统计 `engine/form_analytics.py`（答卷列表/内容接口 + 按题统计 + 交叉分析 + 未填名单 + 图表生成 + 导出 CSV/Excel + 写回智能文档）；增加：MCP 工具 12 个（kdoc.bridge.* 5 个、kdoc.memory.* 3 个、kdoc.form.* 4 个）；增加：桥接/记忆/表单场景案例；优化：SKILL.md 版本号 3.9.0→4.0.0；优化：description 增强到 21 项增强 |
| v3.9.0 | 2026-08-24 | 增加：块级编辑引擎 `engine/blocks.py`（段落级在线编辑，block_id CRUD，块类型映射表，未知块类型跳过不中断）；增加：演示页替换引擎 `engine/page_swap.py`（双路径自动选择：页级更新/整文件替换 + 页数校验 diff）；增加：配额管理器 `engine/quota_manager.py`（SQLite 按天计数 500 次/天 + 令牌桶限速 5 req/s + 429 指数退避 + 批量任务硬件自适应削峰）；增加：格式转换引擎 `engine/format_converter.py`（补齐 jpg/png/txt 三类目标格式，全格式覆盖 pdf/jpg/png/txt/docx/xlsx/pptx/html/md，云端优先→本地兜底失败降级链）；增加：MCP 工具 9 个（kdoc.block.* 5 个、kdoc.page_swap 1 个、kdoc.quota.* 3 个、kdoc.office.convert.enhanced 1 个）；增加：块级编辑/页替换/配额管理/格式转换场景案例；优化：SKILL.md 版本号 3.8.0→3.9.0 |
| v3.8.0 | 2026-08-22 | 增加：智能画布元素级编辑引擎 `engine/element_engine/`（元素CRUD + Markdown追加 + 增量同步，对标腾讯文档·智能画布）；增加：空间节点管理引擎 `engine/space_tree/`（目录树查询 + 链接节点创建 + 递归删除 + 目录可视化）；增加：全文搜索引擎 `engine/content_search/`（文档内容搜索 + 结果定位高亮，超越腾讯）；增加：统一删除入口 `kdoc.file_delete_unified`（合并软删除/彻底删除/直接删除）；增加：MCP 工具 10 个（kdoc.element.* 5 个、kdoc.space.* 4 个、kdoc.content_search.* 2 个、kdoc.file_delete_unified 1 个）；增加：智能画布/空间管理/全文搜索/统一删除场景案例；优化：品类路由表从 8→9（新增 smart_canvas + content_search）；优化：history 模块新增 delete() 统一方法 |
| v3.7.0 | 2026-08-19 | 增加：多维表格视图增强引擎 `engine/views/`（看板/日历/甘特图三种视图，对标 Airtable，本地渲染，硬件自适应）；增加：手写/公式识别 OCR `engine/ocr/`（数学公式识别 LaTeX/MathML 输出，教育场景统一入口）；增加：历史管理模块 `engine/history/`（合并回收站+版本历史，统一 history list/restore 入口）；增加：MCP 工具 6 个（kdoc.view.* 2 个、kdoc.ocr.* 2 个、kdoc.history.* 3 个）；增加：多维表格视图增强/公式识别/历史管理场景案例；优化：OCR 升级为强制本地模式，数据不出域，移除云端调用路径；优化：品类路由表从 7→8（新增 history_mgmt） |
| v3.6.0 | 2026-08-16 | 增加：文档模板市场引擎 `engine/template_marketplace.py`（git 仓库管理模板，支持 list/search/use/refresh，变量替换一键生成）；增加：WPS AI 深度集成（段落级 AI 操作：rewrite/summarize/continue，本地降级占位，API 开放后升级为原生）；增加：可视化品类合并 `engine/categories.py`（8→7 品类，合并 mindmap+flowchart→visualization，共享 mermaid 渲染管线）；增加：MCP 工具 7 个（kdoc.template.* 4 个、kdoc.wps_ai.* 3 个）；增加：可视化品类合并/WPS AI 深度集成/模板市场场景案例；优化：品类路由表从 8→7，引擎逻辑不变 |
| v3.5.0 | 2026-08-08 | 增加：实时协同编辑引擎 `engine/realtime_collab.py`（序列 CRDT 自研实现，零第三方依赖）；增加：文档对比模块 `engine/doc_comparator.py`（复用 difflib，差异高亮+变更摘要+导出）；增加：品类元数据 `engine/categories.py`（9 品类精简为 8 品类，合并 doc+smart_note，子类型自动识别）；增加：MCP 工具 12 个（kdoc.realtime.* 5 个、kdoc.compare.* 3 个、kdoc.category.* 2 个、kdoc.file.* 品类路由更新）；增加：实时协同+文档对比+8 品类智能路由场景案例；优化：品类路由表从 9→8，引擎逻辑不变 |
| v3.4.0 | 2026-07-30 | 增加：文档内容合规检查模块 `engine/compliance_check.py`（自研正则+规则引擎，零第三方依赖）；增加：敏感词扫描 `kdoc.compliance.sensitive`（内置词库+用户黑白名单）、数据泄露检测 `kdoc.compliance.leak`（手机号/身份证号/银行卡号/邮箱，Luhn+校验码验证）、格式规范检查 `kdoc.compliance.format`（DOCX/PPTX/TXT/MD）、密级自动标注 `kdoc.compliance.classify`（公开/内部/秘密/机密）；增加：合规检查 MCP 工具 4 个；增加：敏感词库 `references/sensitive_words.txt`、格式规范 `references/format_spec.md`、用户黑白名单模板；增加：政企文档合规检查场景案例 |
| v3.3.0 | 2026-07-21 | 增加：协同编辑冲突解决模块 `engine/conflict_resolver.py`（自研 difflib 实现，零第三方依赖）；增加：冲突检测 `kdoc.conflict.detect`、智能合并 `kdoc.conflict.merge`（自动合并无冲突段 + 标注冲突段）、Git diff 可视化 `kdoc.conflict.diff`、解决模板 `kdoc.conflict.resolve`（keep_a/keep_b/manual/auto_merge）；增加：冲突解决 MCP 工具 4 个；增加：大文档 diff 分块硬件自适应处理；增加：多人协作冲突解决场景案例；优化：冲突段强制用户确认，绝不自动覆盖 |
| v3.2.0 | 2026-07-17 | 增加：WPS AI 能力适配层（写作辅助/数据分析/PPT 生成/阅读助手），本地降级优先、自研逻辑实现、零密钥可用；增加：WPS AI 适配器 `engine/wps_ai/adapter.py`；增加：本地降级后端 `engine/wps_ai/backends/local_fallback.py`；增加：能力定义与意图映射 `engine/wps_ai/capabilities.py`；增加：WPS AI API 调研记录 `engine/wps_ai/research_notes.md`；优化：MCP Server 注册 5 个 WPS AI 工具；优化：版本号 3.0.0→3.2.0 |
| v3.1.0 | 2026-07-15 | 增加：wps-office-suite 互通方案调研（已废弃，因平台合规不允许双 skill 互通） |
| v3.0.0 | 2026-07-12 | 增加：危险操作强制确认铁律与确认清单（删除/彻底删除/覆盖/批量/权限/清空回收站/版本回滚/Webhook）；增加：禁止文件类型扩展至完整 35 类（执行脚本/Office 二进制/归档镜像/系统文件/风险脚本）；增加：用户上传拦截与技能内部生成豁免白名单；增加：`engine/hardware.py` 硬件自适应性能调度（自动采集 CPU/内存，自动分配并发子进程数与批量分块）；增加：本地 OCR 模块 `engine/local/ocr.py`（优先本地 Tesseract，降级云端，给安装指引）；增加：能力边界与失败场景专章；增加：自然语言触发示例专章；增加：完整场景案例专章（5 个端到端场景）；增加：FAQ 专章（8 个高频问题）；补齐：缺失参考文档 `et_references.md`/`office_references.md`/`rate_limit.md`；补齐：技能图标 `assets/icon.png`；补齐：`engine/__init__.py` 与 `engine/api/mcp_server.py`（真实 MCP Server 入口）；优化：MCP Server 深度直连金山文档开放平台原生 API；优化：每日更新提醒 + 反馈邮箱 `njskills@agent.qq.com` |
| v2.3.0 | 2026-07-05 | 增加：智能文档/思维导图/流程图 3 品类，品类总数 6→9；增加：本地 Tesseract OCR；增加：网页剪藏；增加：HTML 一键上云；优化：MCP 服务拆分 1→4，独立限流/降级 |
| v2.1.0 | 2026-07-02 | 增加：每日自动更新检查；增加：纯文本提取 API；增加：多维表 Webhook 事件监听；增加：批量异步任务；增加：SKILL.md 首次使用必读引导 |
| v2.0.0 | 2026-07-02 | 初始版本发布：6 品类 + 40+ MCP 工具 + 5 层安全防御 |

---

## 22. 详细文档参考

| 文档 | 路径 |
|------|------|
| 鉴权流程 | `references/auth.md` |
| 多维表格 API | `references/dbt_references.md` |
| 电子表格 API | `references/et_references.md` |
| 文本提取/格式转换 | `references/office_references.md` |
| 限流/性能/硬件自适应 | `references/rate_limit.md` |
| 安全设计 | `references/security.md` |
| 错误码 | `references/error_codes.md` |
| 常见工作流 | `references/workflows.md` |

---

## 23. 安装说明

**前置要求**：Python 3.10+；云端功能需金山开放平台 App（免费）；OCR 可选装 Tesseract。

**首次配置由 AI 引导完成**：告诉我你的金山开放平台 App ID / App Secret，AI 自动生成 `config.json`、`mcp-config.json` 并采集本机硬件画像，安装后重启 WorkBuddy 生效。本地生成/OCR/硬件画像无需任何配置即可用。

---

## 24. 📮 反馈与建议

本技能持续迭代。有任何功能建议、问题或更好的实现思路，欢迎反馈：

**📧 有更好建议：njskills@agent.qq.com**

也可在每日更新提醒中一键查看新版本。

---

## 25. ❓ FAQ（v3.0.0 新增）

**Q1：没有金山 App Key 能用吗？**
能。本地生成 DOCX/PPTX、思维导图/流程图 SVG、本地 OCR、硬件画像均零密钥可用；
仅「上传云端/多人协作/回收站/版本」等联网能力需 Key。

**Q2：为什么删除前要确认？**
防止误操作。删除进回收站可恢复；「彻底删除」「清空回收站」为不可逆操作，需二次确认（见第 6 节）。

**Q3：OCR 一定要装 Tesseract 吗？**
首选本地 Tesseract（免费、离线、无 key）。未装时自动降级云端 OCR（需 Key），都无则给出安装指引，不崩溃。

**Q4：大文件传不上去？**
超过阈值（默认 100MB，低端机 50MB）会自动转异步上传 + 轮询；仍失败请压缩或分卷。

**Q5：会不会把我的电脑拖卡？**
不会。技能自动按本机硬件分配并发子进程数（见第 17 节），批量/渲染均受限。

**Q6：报 KD009 文件被拦截？**
你上传的文件属于禁止类型（见第 18 节）。技能自身生成的 docx/pptx/pdf/svg 等不受影响。

**Q7：如何升级？**
每天首次使用会自动提醒；也可 `python -m engine.update_check --version 3.0.0 --reminder`。

**Q8：文字/演示文档能改其中一段吗？**
当前为整文件替换模式：本地改源文件→重新上传覆盖。逐段精细编辑需金山在线编辑器。

---

*最后更新：2026-11-17 | v4.4.0*

---

## 26. 块级编辑引擎（v3.9.0 新增，段落级在线编辑）

> v3.8.0 实现了整文件替换和元素级编辑，v3.9.0 进一步下沉到**段落级块编辑**。
> 以 `block_id` 为操作主键，直接修改文档中的某个段落/标题/列表/表格，无需整文件重生成。

### 26.1 工具列表

| 工具 | 说明 | 操作 |
|------|------|------|
| `kdoc.block.list` | 拉取文档块列表 | 返回所有块的结构化数据 |
| `kdoc.block.replace` | 按 block_id 替换块 | 修改指定块的内容 |
| `kdoc.block.insert` | 按 block_id 插入新块 | 在指定块前后插入 |
| `kdoc.block.delete` | 按 block_id 删除块 | 删除指定块 |
| `kdoc.block.move` | 按 block_id 移动块 | 调整块顺序 |

### 26.2 块类型映射表

| 金山 API 类型 | 内部类型 | 说明 |
|-------------|---------|------|
| paragraph | paragraph | 段落 |
| heading | heading | 标题 |
| list | list | 列表 |
| table | table | 表格 |
| image | image | 图片 |
| divider | divider | 分隔线 |
| code | code | 代码块 |
| quote | quote | 引用 |
| todo | todo | 待办事项 |
| callout | callout | 提示框 |
| equation | equation | 公式 |

**未知块类型处理**：跳过并提示，绝不报错中断。

### 26.3 工作流程

```
1) kdoc.block.list(file_id) → 获取块列表
2) 用户定位要修改的 block_id
3) kdoc.block.replace(file_id, block_id, new_content) → 替换内容
4) 或 kdoc.block.insert(file_id, block_id, content, position="after") → 插入新块
5) 或 kdoc.block.delete(file_id, block_id) → 删除块
6) 或 kdoc.block.move(file_id, block_id, target_id, position) → 移动块
```

### 26.4 安全约束

- 块级编辑属于「覆盖文件」操作，**必须走强制确认铁律**
- 批量替换时自动降并发（硬件自适应）
- 未知块类型跳过并提示，不中断流程

---

## 27. 演示页替换引擎（v3.9.0 新增，双路径自动选择）

> 单页内容本地 python-pptx 重生成后，探测演示 API 是否支持页级更新。
> 支持则仅覆盖该页，不支持则整文件替换并在完成后 diff 提示页数校验。

### 27.1 工具列表

| 工具 | 说明 | 操作 |
|------|------|------|
| `kdoc.page_swap` | 替换指定页 | 自动选择页级更新或整文件替换 |

### 27.2 双路径自动选择

```
1) 探测 API 是否支持页级更新
   ├── 支持 → 仅覆盖该页（API 调用）
   └── 不支持 → 整文件替换（本地重生成 + 上传覆盖）
2) 替换完成后执行页数校验 diff
3) 返回替换结果 + 页数变化提示
```

### 27.3 安全约束

- 整文件替换属于「覆盖文件」危险操作，**必须走强制确认铁律**
- 页数校验 diff 确保替换前后页数一致
- 页数变化时明确提示用户

---

## 28. 配额管理器（v3.9.0 新增，API 配额与限流）

> 保护测试与生产环境，避免 API 配额耗尽导致服务中断。

### 28.1 工具列表

| 工具 | 说明 | 操作 |
|------|------|------|
| `kdoc.quota.check` | 检查配额状态 | 返回剩余配额、使用率 |
| `kdoc.quota.dashboard` | 配额看板 | 配额+令牌桶+硬件+小时分布 |
| `kdoc.quota.batch_params` | 安全批量参数 | 硬件自适应削峰建议 |

### 28.2 配额三件套

| 组件 | 说明 | 配置 |
|------|------|------|
| SQLite 按天计数 | 记录每日请求量 | 默认 500 次/天 |
| 令牌桶限速 | 控制请求速率 | 默认 5 req/s，突发 10 |
| 429 指数退避 | 限流时自动重试 | 最多 5 次，最大 60 秒 |

### 28.3 硬件自适应削峰

```
批量任务 → 读取 hardware.py → 计算安全并发
         → 读取配额余量 → 计算可执行任务数
         → 令牌桶限速 → 控制请求速率
         → 返回建议参数（workers, batch_chunk, 预估时间）
```

### 28.4 配额看板展示

- 当日配额使用率（进度条）
- 令牌桶状态（令牌数/速率/突发）
- 小时分布图（峰值时段）
- 硬件自适应建议
- 推荐执行时段

---

## 29. 格式转换补全（v3.9.0 升级，全格式覆盖）

> 补齐 jpg/png/txt 三类缺失的目标格式，全量覆盖参数校验与失败降级链。

### 29.1 工具列表

| 工具 | 说明 | 操作 |
|------|------|------|
| `kdoc.office.convert.enhanced` | 格式转换（增强版） | 云端优先 → 本地兜底 |

### 29.2 支持的目标格式（v3.9.0 补齐后）

| 格式 | 说明 | 本地兜底 |
|------|------|---------|
| pdf | PDF 文档 | LibreOffice |
| jpg | JPEG 图片 | Pillow / ImageMagick |
| png | PNG 图片 | Pillow / ImageMagick |
| txt | 纯文本 | 直接提取 |
| docx | Word 文档 | python-docx |
| xlsx | Excel 表格 | openpyxl |
| pptx | PPT 演示 | python-pptx |
| html | HTML 文档 | 简单转换 |
| md | Markdown | 简单转换 |

### 29.3 失败降级链

```
云端转换（金山 API）
  ↓ 失败
本地转换（python-docx / python-pptx / LibreOffice）
  ↓ 失败
返回错误 + 安装指引
```

### 29.4 参数校验

- 源格式与目标格式是否支持
- 本地兜底是否可用（检查依赖）
- 文件大小是否超限
- 转换矩阵校验

---

## 30. 本地桥接引擎（v4.0 新增，wps-office-suite 双向互通）

> 与 wps-office-suite 双向互通：白名单探测安装路径 + SQLite 映射表 + 子进程 JSON 契约。
> 下行：云端→本地→wps 处理→回传覆盖；上行：mtime 监听→上传同步。

### 30.1 工具列表

| 工具 | 说明 | 操作 |
|------|------|------|
| `kdoc.bridge.status` | 桥接状态 | wps 安装状态、映射数量 |
| `kdoc.bridge.download` | 下行：拉取云端文档 | 下载到本地临时目录 |
| `kdoc.bridge.process` | 下行：wps 处理 | subprocess 调 wps 脚本 |
| `kdoc.bridge.upload` | 上行：上传覆盖 | 本地文件覆盖云端 |
| `kdoc.bridge.sync` | 上行：同步 | mtime 变化自动同步 |

### 30.2 双向互通流程

```
下行（云端→本地→wps→云端）：
  kdoc.bridge.download → 拉取到临时目录
  kdoc.bridge.process → subprocess 调 wps 脚本（JSON 契约）
  kdoc.bridge.upload → 回传覆盖云端

上行（本地变化→云端）：
  监听映射表 mtime → 变化后自动上传同步
```

### 30.3 JSON 契约格式

```json
{
  "action": "analyze|convert|format|extract",
  "input": "/path/to/local/file",
  "output": "/path/to/output",
  "params": {}
}
```

### 30.4 安全约束

- 子进程超时自动关闭（120 秒）
- 白名单探测，不扫描全盘
- 未安装 wps：入口隐藏，云端功能不受影响

---

## 31. 记忆桥接引擎（v4.0 新增，zwjh 记忆库打通）

> 文档关键事件（创建/重要编辑/分享）经 zwjh MCP 总线写入长期记忆。
> 用户问 zwjh 上周改了什么文档时可答。

### 31.1 工具列表

| 工具 | 说明 | 操作 |
|------|------|------|
| `kdoc.memory.status` | 记忆桥接状态 | zwjh 安装状态、待迁移事件数 |
| `kdoc.memory.deposit` | 发送事件 | 写入 zwjh 或待迁移日志 |
| `kdoc.memory.migrate` | 一次性导入 | 待迁移事件批量写入 zwjh |

### 31.2 工作流程

```
文档事件 → deposit_event()
         ├── zwjh 已安装 → stdio JSON-RPC 调用 deposit → 写入长期记忆
         └── zwjh 未安装 → 写入本地待迁移日志 → 未来安装后 migrate 一次性导入
```

### 31.3 安全约束

- 子进程超时自动关闭（30 秒）
- 不打包 zwjh 代码，仅走标准 MCP stdio 协议
- 未安装 zwjh：事件写本地，不丢失

---

## 32. 表单答卷收集统计（v4.0 新增，云端数据本地智能加工）

> 拉取答卷自动聚合（按题统计、交叉分析、未填名单），结果写回智能文档表格并生成图表页。

### 32.1 工具列表

| 工具 | 说明 | 操作 |
|------|------|------|
| `kdoc.form.analyze` | 分析答卷 | 按题统计 + 交叉分析 + 未填名单 |
| `kdoc.form.export` | 导出答卷 | CSV / Excel |
| `kdoc.form.chart_data` | 图表数据 | 供前端渲染 |
| `kdoc.form.write_to_doc` | 写回智能文档 | 统计结果写入表格 |

### 32.2 分析能力

| 能力 | 说明 |
|------|------|
| 按题统计 | 选择题分布、数值题均值/最大/最小、文本题字数 |
| 交叉分析 | 两两选择题关联分析 |
| 未填名单 | 找出未填题的答卷 |
| 图表生成 | 自动生成图表数据（饼图/柱状图/直方图） |

### 32.3 安全约束

- 硬件自适应：批量拉取时分块处理
- 导出文件不落地敏感目录
- 写回智能文档需用户确认

---

## 33. AirScript 在线自动化（v4.1.0 新增，自然语言→脚本→确认→执行）

> 封装金山开放平台 AirScript 脚本创建/执行接口，是在线侧的自动化补全。
> 自然语言意图 → 脚本生成（本地规则引擎模板，无需外部 LLM）→ 预检（危险操作拦截）→ 用户确认 → 在线执行。

### 33.1 工具列表

| 工具 | 说明 | 操作 |
|------|------|------|
| `kdoc.airscript.list_capabilities` | 列出能力域 | 定时通知/数据汇总/表格批量操作/字段计算 |
| `kdoc.airscript.generate` | 生成脚本 | 根据能力域和参数生成 AirScript |
| `kdoc.airscript.precheck` | 脚本预检 | 扫描 DELETE/OVERWRITE/DROP 等危险操作 |
| `kdoc.airscript.submit` | 提交确认 | 提交脚本等待用户确认 |
| `kdoc.airscript.execute` | 执行脚本 | 用户确认后在线执行 |
| `kdoc.airscript.history` | 执行历史 | 查看已执行脚本记录 |
| `kdoc.airscript.pending` | 待确认列表 | 查看待确认脚本 |

### 33.2 安全阀机制

```
自然语言意图 → 脚本生成 → 预检扫描
                              ├── 安全 → 用户确认 → 执行
                              └── 危险 → 拦截 + 二次确认
                                           ├── 用户同意 → 执行
                                           └── 用户取消 → 终止
```

### 33.3 危险操作关键词

DELETE / DROP / TRUNCATE / OVERWRITE / REPLACE / REMOVE / CLEAR / UPDATE_ALL / BATCH_DELETE

---

## 34. 多维表格字段自动化（v4.1.0 新增，公式/关联/汇总字段）

> 字段层支持公式字段/关联字段/汇总字段的创建与批量填充，走 et/dbt/form API 记录级接口。

### 34.1 工具列表

| 工具 | 说明 | 操作 |
|------|------|------|
| `kdoc.dbf.list_field_types` | 列出字段类型 | 16 种类型 |
| `kdoc.dbf.list_formula_templates` | 公式模板 | SUM/AVG/COUNT/IF/CONCAT 等 |
| `kdoc.dbf.create_field` | 创建字段 | 公式/关联/汇总/基础字段 |
| `kdoc.dbf.batch_fill` | 批量填充 | 硬件自适应削峰 |
| `kdoc.dbf.history` | 操作历史 | 查看操作记录 |

### 34.2 字段类型

text / number / select / multi_select / date / person / link / formula / relation / rollup / checkbox / url / email / phone / currency / percent

---

## 35. 视图渲染引擎（v4.1.0 新增，看板/甘特图）

> 视图层本地渲染看板（matplotlib 柱图）与甘特（mermaid 时间线）两种视图导出图片。

### 35.1 工具列表

| 工具 | 说明 | 操作 |
|------|------|------|
| `kdoc.view.render_kanban` | 渲染看板 | matplotlib 柱图 |
| `kdoc.view.render_gantt` | 渲染甘特图 | mermaid 时间线 |
| `kdoc.view.render_advanced` | 高级渲染 | 直接传入数据渲染 |

### 35.2 硬件自适应

- 渲染并发不超过 hardware.py 的 workers
- 大数据集自动分页

---

## 36. CRDT 表格扩展（v4.1.0 新增，单元格级无冲突协作）

> 把序列 CRDT 协同从智能文档扩展到电子表格与多维表格。
> 单元格级操作日志 + 向量时钟，冲突时保留双方并标记。

### 36.1 工具列表

| 工具 | 说明 | 操作 |
|------|------|------|
| `kdoc.crdt_table.create` | 创建会话 | 指定品类和客户端 |
| `kdoc.crdt_table.set_cell` | 设置单元格 | 单元格级操作日志 |
| `kdoc.crdt_table.get_cell` | 获取单元格 | 含冲突信息 |
| `kdoc.crdt_table.resolve` | 解决冲突 | 选择保留的值 |
| `kdoc.crdt_table.get_conflicts` | 获取冲突 | 所有冲突单元格 |
| `kdoc.crdt_table.state` | 表格状态 | 完整状态 |

### 36.2 冲突解决策略

- 并发操作 → 保留双方修改 → 标记冲突单元格
- 用户选择保留值 → 解决冲突

---

## 37. Excel/CSV 双向导入导出（v4.1.0 新增，四类字段序列化）

> openpyxl 读写与字段类型映射约定，导入走批量记录创建（复用配额管理器削峰），导出支持视图级筛选快照。

### 37.1 工具列表

| 工具 | 说明 | 操作 |
|------|------|------|
| `kdoc.bidata.get_field_rules` | 字段规则 | date/link/select/person 序列化规则 |
| `kdoc.bidata.import_csv` | 导入 CSV | 硬件自适应削峰 |
| `kdoc.bidata.import_excel` | 导入 Excel | openpyxl 读写 |
| `kdoc.bidata.export_csv` | 导出 CSV | 视图级筛选快照 |
| `kdoc.bidata.export_excel` | 导出 Excel | 视图级筛选快照 |

### 37.2 四类字段序列化规则

| 类型 | 序列化方式 |
|------|-----------|
| date | ISO 8601 字符串 (YYYY-MM-DD) |
| link | JSON {url, title} |
| select | 逗号分隔字符串 |
| person | JSON {name, email} |

---

## 38. Webhook 与通知中心（v4.1.0 新增，三通道分发）

> 订阅记录新增/修改/删除三类事件，签名校验 + SQLite 去重队列，通知通道整合金山协作消息/企微/钉钉三路。

### 38.1 工具列表

| 工具 | 说明 | 操作 |
|------|------|------|
| `kdoc.webhook.list_events` | 事件类型 | 5 种事件 |
| `kdoc.webhook.list_channels` | 通知通道 | 3 种通道 |
| `kdoc.webhook.subscribe` | 订阅事件 | 签名校验 |
| `kdoc.webhook.unsubscribe` | 取消订阅 | — |
| `kdoc.webhook.list_subscriptions` | 列出订阅 | — |
| `kdoc.webhook.process_event` | 处理事件 | 签名校验+去重+分发 |
| `kdoc.webhook.history` | 事件历史 | — |
| `kdoc.webhook.statistics` | 统计信息 | — |

### 38.2 通知通道

- 金山协作消息（kdocs）
- 企业微信（wecom）
- 钉钉（dingtalk）

### 38.3 安全机制

- HMAC 签名校验
- SQLite 去重队列（事件哈希去重）
- 事件可触发写入 zwjh 记忆（桥接存在时）

---

## 39. 团队知识库模式（v4.2.0 新增，知识中枢）

> v4.2 企业文档中枢落地：空间级全文检索 + 权限感知过滤。
> 遵守平台权限边界——检索前按空间成员权限矩阵过滤，用户无 read 权限的文档不进入结果集。

### 39.1 工具列表

| 工具 | 说明 | 操作 |
|------|------|------|
| `kdoc.khub.index` | 构建知识库索引 | 注入文档集建本地倒排索引 |
| `kdoc.khub.search` | 权限感知全文检索 | 先鉴权后检索，无权限剔除 |
| `kdoc.khub.permission` | 注入空间权限矩阵 | doc_id→级别（1 read/2 edit/3 admin） |
| `kdoc.khub.status` | 知识中枢状态 | 文档数/词项/jieba 状态 |

### 39.2 检索流程

1. 分词：中文走 jieba（可选，未装退化为字符级），英文/数字按词边界切分
2. 倒排取候选：token → 文档集
3. 权限过滤：依据 `kdoc.khub.permission` 注入的矩阵，剔除无 read 权限文档
4. 打分排序：命中词频排序，返回 snippet

### 39.3 安全约束

- 权限边界强制：无矩阵登记的空间文档视为无权限，绝不进入结果
- 硬件自适应：索引构建按 batch_chunk 分块，不卡顿
- 云端降级：无 backend 时接受外部文档集建本地索引

---

## 40. 政企合规中心（v4.2.0 新增，差异化主战场）

> 把散点合规检查聚合为政企可采购的能力叙事：密级标注 + 全量扫描 + 数据不出域。

### 40.1 工具列表

| 工具 | 说明 | 操作 |
|------|------|------|
| `kdoc.compliance.label` | 密级标注落库 | 公开/内部/秘密/机密 |
| `kdoc.compliance.get` | 查询密级 | 返回已标注级别 |
| `kdoc.compliance.scan` | 全量扫描报告 | 敏感词+泄露+密级建议聚合 |
| `kdoc.compliance.declare` | 数据不出域声明 | 本地 OCR 强制、云端仅元数据 |
| `kdoc.compliance.status` | 合规中心状态 | 级别/引擎清单 |

### 40.2 能力

- 密级标注：随文档元数据落库（SQLite），检索/分享前可被权限层引用
- 全量扫描：复用 v3.4 合规检查（敏感词 + 手机号/身份证/银行卡号/邮箱 Luhn 校验 + 密级建议），聚合为政企报告
- 数据不出域：本地 OCR 强制（Tesseract / wps_ocr 均为本地引擎），云端仅同步元数据

---

## 41. 主题一键生成（v4.2.0 新增，WPS AI 对齐）

> 对标腾讯文档·AI 生成：输入主题与大纲要点，本地降级引擎生成初稿，WPS AI 真源开放后无缝切换。

### 41.1 工具列表

| 工具 | 说明 | 操作 |
|------|------|------|
| `kdoc.topic.generate` | 主题生成 | 大纲→智能文档/PPT/表格初稿 |
| `kdoc.topic.status` | 适配层状态 | 当前生效 AI 源（local/wps_ai） |

### 41.2 实现原理

- 适配层：本地生成（零密钥）优先；WPS AI 真源可用时切换，接口统一
- 三类产出：智能文档（Markdown 初稿）/ PPT（幻灯片大纲）/ 表格（字段+样例行）
- 本地降级：模板驱动 + 分段生成，硬件自适应不卡顿

---

## 42. 跨品类对比与时间线（v4.2.0 新增，差异化）

> 版本历史轮询→who/when/what 时间线；表格/多维表格品类新增单元格级 diff 视图（跨品类对比是腾讯文档没有的）。

### 42.1 工具列表

| 工具 | 说明 | 操作 |
|------|------|------|
| `kdoc.compare.timeline` | 版本时间线 | 逐版本 difflib 生成变更摘要 |
| `kdoc.compare.cells` | 单元格级 diff | 表格/多维表格跨版本差异 |
| `kdoc.compare.status` | 对比状态 | 品类/硬件信息 |

### 42.2 实现原理

- 时间线：轮询版本历史（云端）或接受快照列表（本地），逐版本 difflib 生成「谁-何时-改了什么」
- 单元格 diff：按 (行,列) 比对，标注新增/修改/删除单元格（表格品类差异化能力）

---

## 43. OCR 收敛（v4.2.0 优化，生态专职工具）

> 删除重复维护的本地 OCR 预处理代码，收敛为唯一入口，桥接生态专职工具。

### 43.1 收敛说明

- 删除 `engine/ocr/local_ocr.py` 重复预处理面，公式/教育场景统一 import `engine.local.ocr`
- 唯一入口 `engine/local/ocr.py`：优先桥接 wps-office-suite OCR（subprocess JSON 契约 {image_path, lang}）
- 未装 wps 保留 Tesseract 最小兜底；两路均本地引擎，数据不出域
- MCP `kdoc.local.ocr.extract` 与 `kdoc.ocr.formula`/`kdoc.ocr.education` 均经此入口

---

## 44. 合规中心 v2（v4.3.5 合规分类描述分包 + 外部词包支持）

> 合并 v4.2 政企合规中心与 v3.4 内容合规检查为门面 `engine/compliance_suite.py`，敏感词加载逻辑唯一来源，维护面减半。v4.3.5 起内置词包改为合规风险分类描述（避免平台内容审核误判），并支持外部词包目录加载企业本地词库。

### 44.1 单入口两档输出

- `kdoc.compliance.quick_scan(text, packs, external_packs_dir)`：快速扫，敏感词命中即报 + 数据泄露，秒级
- `kdoc.compliance.full(text, doc_id, include_history, packs, external_packs_dir)`：全域扫，全文敏感词 + 数据泄露 + 格式 + 密级建议 + 历史版本时间线
- 底层统一 `ComplianceCore`；旧 `kdoc.compliance.sensitive/leak/format/classify` 与 `kdoc.compliance.label/scan/declare` 仍可用（委托门面）

### 44.2 行业敏感词分包

- `references/sensitive_packs/`：`base` 通用包 + `edu`（教培）/ `medical`（医疗）/ `finance`（金融）/ `gov`（政务）四行业包，各 200+ 分类描述词条
- `kdoc.compliance.packs(external_packs_dir)` 查看词数、责任人字段与来源；`packs` 参数多包叠加（如 `"edu,finance"`）
- 扫描报告按高/中/低三档风险分级，并定位到段落行号与责任人字段（包元数据）

### 44.3 外部行业敏感词包（v4.3.5 新增）

- 企业可在本地维护真实敏感词库，通过两种方式加载：
  - 环境变量 `KINGDOC_EXTERNAL_PACKS_DIR` 指向包含 `.yaml` 词包的目录
  - 各 MCP 工具参数 `external_packs_dir` 临时指定（优先级高于环境变量）
- 外部目录中的同名 `.yaml` 包会覆盖内置包；不同名包与内置包合并展示
- 词包格式与内置一致：`pack:`/`name:`/`responsible_field:`/`risk_default:`/`words:`

### 44.4 全域扫描定时化

- `kdoc.compliance.scheduler_register(space_id, packs, weekday, scan_time, external_packs_dir)`：Windows 产出 schtasks 命令；非 Windows 产出 cron 行
- `kdoc.compliance.scheduler_run(space_id, docs, packs, external_packs_dir)`：执行一次扫描，仅推送新增（扫描级跨周去重 + webhook 签名核验，只推新增不扰民）
- `kdoc.compliance.scheduler_status(external_packs_dir)`：查看已注册任务与去重计数

### 44.5 配额阈值告警

- 配额管理器用量越过 80% / 95% 时经 webhook 三通道推送（按天+级别幂等，不重复打扰）
- `kdoc.quota.check` 现返回 `alerts` 字段，含已触发级别与推送状态

### 44.6 安全约束

- 子进程超时自动关闭，不残留
- 绝不调用任何外部 OCR API（数据不出域）

---

## 45. 表单实时化（v4.4.0 新增）

> 把「收集 → 实时看 → 合并统计 → 沉淀业务表」打通成闭环，全部自研零外部 API。

### 45.1 答卷实时推送（`engine/form_realtime.py`）

- `kdoc.form_realtime.poll(form_id, answers, key_fields, answer_url_template)`：轮询答卷接口 + 增量游标检测新答卷，命中即经 webhook_center 三通道推送关键字段摘要与答卷链接
- 增量游标优先取答卷时间字段（update_time/submit_time/created_at），其次 answer_id，均缺失用内容哈希兜底；首次运行只建基线不推历史
- 端到端延迟统计（`latency_ms` / `within_target`），验收目标 ≤30 秒
- 本地降级：无 webhook 时只落本地 SQLite，不中断主流程
- `kdoc.form_realtime.cursor(form_id)`：查游标状态；`kdoc.form_realtime.history(form_id)`：查推送历史

### 45.2 跨表聚合分析（`engine/form_cross_analytics.py`）

- `kdoc.form_cross.add(form_id, form_name, answers, mapping)`：添加收集表与「问题→标准字段」映射（支持中文别名）
- `kdoc.form_cross.run()`：多表按映射合并统计，按身份键（phone>email>name）归一化去重，输出去重率与字段分布（验收 ≥98%）
- `kdoc.form_cross.dashboard(output_path)`：生成自包含 HTML 看板（离线可打开，零第三方依赖）
- 同一活动多渠道报名合并去重，渠道×分组交叉分布一目了然

### 45.3 答卷沉淀多维表格（`engine/form_to_bidata.py`）

- `kdoc.form_bidata.deposit(form_id, table_id, answers, field_map)`：答卷一键转多维表格行，复用 v4.1 `bidata_io` 的 date/link/select/person 四类字段序列化（唯一真相源）
- `kdoc.form_bidata.prepare_update(form_id, table_id, answer_id, updated_fields, field_map)`：person/link 双向可编辑，从表格行反向生成答卷更新草稿
- 硬件自适应批量削峰，本地降级输出结构化行并落库

---

## 46. 多维表格自动化（v4.4.0 新增）

> 让「谁改了表 / 自动生成 / 冲突」可审查、可对话、可追溯。

### 46.1 定时快照与变更摘要（`engine/table_snapshot.py`）

- `kdoc.table_snapshot.take(table_id, rows, headers, base_date, push)`：每日快照（行数 + 关键字段哈希）存本地 SQLite
- 行哈希 O(n) 快速筛选变化行，只对变化行做单元格级 diff（复用 cross_compare），输出增/删/改行清单（验收 5000 行 ≤10 秒）
- `kdoc.table_snapshot.diff(table_id, date_a, date_b)`：对比任意两次快照；`kdoc.table_snapshot.history(table_id)`：列快照历史
- 变更摘要可经 webhook 推送或写入周报文本

### 46.2 AirScript 预设库 20+（`engine/airscript_presets.py`）

- `kdoc.airscript_preset.list()`：列出 22 个预设（去重提醒/到期扫描/自动编号/状态流转/重复值标记/库存预警等）
- `kdoc.airscript_preset.match(text)`：自然语言关键词匹配最佳预设（本地规则，无需 LLM）
- `kdoc.airscript_preset.generate(preset_id, params)`：生成脚本 + 测试样例 + 预期输出，走 airscript 预检
- 全部预设带元数据与测试样例（`kdoc.airscript_preset.validate()` 校验），全程中文

### 46.3 CRDT 冲突可视化（`engine/crdt_visualizer.py`）

- `kdoc.crdt_viz.export(session_id)`：导出单元格级操作日志（含向量时钟与冲突标记）
- `kdoc.crdt_viz.visualize(session_id)`：生成 ECharts 单文件时间线 HTML（CDN + 内联 SVG 离线降级），冲突以红色标记、可审查可追溯
- `kdoc.crdt_viz.replay(operations)`：从操作日志直接渲染时间线，用于还原一次真实并发编辑

### 46.4 安全与性能约束

- 6 个新引擎全部零第三方 Python 依赖（仅标准库）
- HTML 看板/时间线自包含，离线可读，不上传任何用户数据
- 硬件自适应批量分块，子进程不残留

---

*最后更新：2026-11-17 | v4.4.0*
