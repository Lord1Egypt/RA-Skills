---
name: hap-mongodb-slowlog-analysis
description: Analyze MongoDB 4.4.x slow logs from pasted slow-log text, uploaded log files, or mongodb.log content and produce practical query optimization advice, index recommendations, evidence-backed reasoning, and ready-to-run Mongo shell index commands. The skill is AI-first and should analyze logs directly in conversation without relying on local PowerShell by default. It should also be able to group repeated entries by namespace, deduplicate repeated query shapes, and summarize repeated patterns before giving advice. Only treat DOCX or PDF export as optional conversion steps that may require local tooling. Prefer Chinese output by default, but support English when requested. For HAP worksheet collections whose names start with ws, treat _id, utime, rowid, and ctime single-field indexes as existing defaults and never recommend recreating those single-field indexes. Treat status as a low-cardinality field with only 1 and 9, where 1 means active/in-use, and do not include status in recommended index definitions.
---

# MongoDB Slowlog Analysis

## Overview

默认优先由 AI 直接在对话中分析慢日志，不依赖本地 PowerShell。这个 skill 的主体能力是：

- 直接读取用户粘贴的慢日志文本
- 直接读取用户上传的 `mongodb.log`、`.log`、`.txt`、`.jsonl` 等文件内容
- 直接在对话中给出分析结论
- 对批量慢日志按集合（`ns`）归类，并按“查询形态”去重汇总
- 直接生成 Markdown 或 HTML 内容
- 只在必要时把 DOCX / PDF 视为可选转换结果，而不是默认能力

也就是说，这个 skill 的核心不是“运行脚本”，而是“AI 直接分析并输出结构化结果”。

## Default Mode

默认模式是“纯 AI 分析优先”：

1. 用户直接粘贴一段慢日志
2. 用户上传一个日志文件
3. 直接在对话中分析，不要求用户先保存文件
4. 直接输出结构化结论
5. 如有必要，再补充可执行的 Mongo Shell `createIndex(...)` 命令
6. 如果用户要求 `md` 或 `html`，优先由 AI 直接生成对应内容

在这个模式下：

- 不要求先运行本地脚本
- 不要求先解析成中间文件
- 不要求先落地 PowerShell 产物
- 用户上传文件时，也应优先直接读取文件内容并在对话中分析
- 批量日志应优先做“按表归类 + 按查询形态去重”的 AI 汇总
- 应优先把注意力放在执行计划、过滤条件、排序方式、扫描量和查询形态上

## Output Strategy

按优先级使用下面这套策略：

1. `对话分析`
   - 默认方式
   - 直接输出分析结果
2. `Markdown`
   - 优先由 AI 直接生成
   - 不依赖 PowerShell 也可以完成
3. `HTML`
   - 优先由 AI 直接生成 HTML 内容
   - 如需落文件，可以把 AI 生成的 HTML 保存到工作区
4. `DOCX / PDF`
   - 不作为 skill 的默认能力承诺
   - 如果用户明确需要真正的文件格式，可以说明这一步通常需要本地转换工具
   - 这属于可选增强，而不是主路径

## When to Use Tools

默认不要把脚本当作分析入口。

只有在下面场景下，才可以考虑使用本地工具或脚本：

- 用户明确要求把结果落成文件
- 用户明确要求批量处理整个 `mongodb.log`
- 用户明确要求把 Markdown / HTML 自动写入某个文件
- 用户明确要求尝试导出 DOCX / PDF

如果只是单条、少量、临时分析，或者上传文件后只需要直接分析，优先用 AI 完成。

## Workflow

1. 接受三类输入：
   - 用户直接粘贴的慢日志文本
   - 用户上传的日志文件内容
   - 一个 `mongodb.log` 文件路径或一段日志文件内容
2. 如果输入里包含多条慢日志，应先做批量归类：
   - 先按 `ns` 归类
   - 再按“查询形态”去重
   - 每组保留代表性样本，并统计重复次数
3. “查询形态”去重时，优先忽略具体常量值，重点看这些结构是否相同：
   - `operation` (`find` / `aggregate`)
   - `ns`
   - `filter` 的字段结构和操作符结构
   - `sort`
   - `projection`
   - `limit`
   - `pipeline` 的阶段结构
   - `planSummary`
4. 先尽量识别这些关键信号：
   - `ns`
   - `planSummary`
   - `keysExamined`
   - `docsExamined`
   - `nreturned`
   - `durationMillis`
   - `find` / `aggregate`
   - `filter`
   - `sort`
   - `projection`
   - `limit`
   - `$group`
   - `$or`
   - `$regex`
   - `$ne/$nin/$not/$size`
5. 重点判断这些性能模式：
   - 全表扫描 `COLLSCAN`
   - 当前索引主要在服务排序，而不是先过滤
   - `limit: 1` 但扫描很多文档
   - `$or` 不同分支需要不同索引
   - `$ne`、`$nin`、`$not`、`$size` 这类负向条件拖慢查询
   - 正则、包含搜索这类普通索引收益很差的查询
   - aggregate 首段 `$match` 不够收敛
   - `$group` 放大上游扫描成本
6. 给出结构化建议，并明确说明应当：
   - 先改查询条件
   - 或者可以直接尝试加索引

## Output Contract

默认输出顺序如下：

1. `摘要 / Summary`
2. `归类与去重摘要 / Grouping & Dedup Summary`（批量日志时必须出现）
3. `处理优先级 / Action Priority`
4. `证据 / Evidence`
5. `查询条件 / Query Shape`
6. `为什么慢 / Why It Is Slow`
7. `索引建议 / Index Advice`
8. `索引创建命令 / Index Commands`
9. `可执行优化路径 / Practical Optimization Paths`
10. `查询优化建议 / Query Advice`
11. `验证建议 / Validation`
12. `参考文档 / References`\r\n\r\n报告中应尽量解释：

- 为什么慢
- 为什么当前计划不理想
- 为什么是“先改查询”还是“先试索引”
- 如果建议索引，为什么是这个字段顺序
- 如果不建议先加索引，为什么普通索引收益不高
- 对于“先改查询”的场景，最好额外给一节 `可执行优化路径 / Practical Optimization Paths`
- 这一节应至少拆成：`不改写入逻辑可做项`、`允许改写写入默认值时可做项`
- 查询条件本身长什么样，最好以 JSON 形式展示
- 如果是批量日志，先告诉用户：哪些集合重复出现、哪些查询形态重复最多、每组重复了多少次

## References in Output

每次完整报告都应固定带一个“参考文档 / References”小节，至少包含：

- [MongoDB 慢查询优化](https://docs-pd.mingdao.com/deployment/components/mongodb/slowQueryOptimization)

如果是 HTML 输出，应把这个链接做成可点击超链接。

## HTML Expectations

如果用户要求 HTML 内容或 HTML 文件，输出应尽量满足这些要求：

- 文首固定免责声明：
  - `声明：内容由 AI 生成。尽管已努力确保信息的合理性，但 AI 模型仍可能产生不准确、过时或存在偏差的内容。请在执行关键操作前，务必对照 官方文档 进行核实校验。`
- 官方文档应为可点击链接
- 查询条件应单独展示，优先用 JSON 代码块
- HTML 应自动生成目录（Table of Contents / 目录），桌面端默认放在左侧并支持点击跳转到各节，移动端可回退到顶部区块
- 索引创建命令应使用代码块
- 如果支持交互增强，代码块右上角应有复制按钮

### HTML 目录交互规范（必须遵守）

生成 HTML 时，目录（TOC）必须满足以下所有要求，否则视为不合格输出：

1. **锚点完整性**：每个 TOC 链接的 `href`（如 `#g2`）必须在正文中存在对应的 `id` 属性。
   - 生成 HTML 后必须自检：遍历所有 TOC 链接，确认每个 `href` 去掉 `#` 后都能在 DOM 中找到对应元素。
   - 如果 TOC 链接指向分组（如 G1-G18），必须给每个分组的容器元素（如 `<div class="group-section" id="g2">`）加上对应 `id`。
   - 不允许只给第一个分组加 `id` 而遗漏其余分组。

2. **平滑滚动**：CSS 必须包含：
   ```css
   html {
     scroll-behavior: smooth;
     scroll-padding-top: 20px;
   }
   ```

3. **TOC 滚动高亮兼容性**：
   - 侧边栏通常是 `position: sticky` 布局。
   - 判断当前可见章节时，必须使用 `getBoundingClientRect().top` 而非 `element.offsetTop`，因为 `offsetTop` 在 sticky 容器下会返回错误值。
   - 正确写法示例：
     ```javascript
     sections.forEach(s => {
       if (s.getBoundingClientRect().top <= 120) {
         current = s.id;
       }
     });
     ```

4. **目标元素间距**：被跳转到的目标元素应设置 `scroll-margin-top`，确保不会被页面顶部遮挡：
   ```css
   h2[id], h3[id], .group-section[id] {
     scroll-margin-top: 20px;
   }
   ```

5. **自检清单**：生成 HTML 后，在最终写入文件前，用以下清单自检：
   - [ ] 每个 TOC `<a href="#xxx">` 是否都有对应的 `id="xxx"` 元素
   - [ ] 是否包含 `scroll-behavior: smooth`
   - [ ] 是否包含 `scroll-padding-top` 或 `scroll-margin-top`
   - [ ] TOC 高亮是否使用 `getBoundingClientRect` 而非 `offsetTop`

如果 HTML 已写入文件，任务完成时可以提供一个最小化交付提示，但不要默认增加单独的“交付结果 / Deliverables”小节。\r\n\r\n默认只需要：\r\n\r\n- 在最终回复里给出最重要产物的可点击文件路径\r\n- 如有必要，再补一个可点击目录路径\r\n- 如果是 HTML，可选补一个本地打开示例\r\n\r\n如果用户没有要求展示目录或打开方式，不要额外展开太多交付说明。\r\n\r\n在 Codex 桌面环境里，优先使用简洁的可点击路径。


## Batch Output Compatibility

批量日志分析时，不能因为做了“按表归类 + 查询形态去重”就丢掉老的细节输出。必须同时满足这两层：

1. `汇总层 / Summary Layer`
- 先给出按 `ns` 归类、按查询形态去重后的总览
- 说明哪些集合重复最多、哪些查询形态重复最多、每组出现多少次

2. `细节层 / Detail Layer`
- 每个分组下面仍然必须保留一个“代表性样本 / Representative Sample”
- 这个代表性样本应继续使用单条慢日志分析时的老结构，至少包含：
  - `证据 / Evidence`
  - `查询条件 / Query Shape`
  - `为什么慢 / Why It Is Slow`
  - `索引建议 / Index Advice`
  - `索引创建命令 / Index Commands`
  - `查询优化建议 / Query Advice`
- `查询条件 / Query Shape` 不允许省略；优先展示格式化 JSON
- 如果是 `find`，至少展示：
  - `filter`
  - `sort`
  - `projection`（如果存在）
  - `limit`（如果存在）
- 如果是 `aggregate`，至少展示：
  - `pipeline`
  - 如能拆出首段 `$match`，应单独展示 `match` JSON
- 如果同一分组的建议一致，可以合并文字说明，但查询字段结构和代表性样本不能只剩一句摘要

也就是说：
- 新功能保留：按表归类、按查询形态去重、重复次数统计
- 老功能保留：像手动输入单条慢日志那样，继续看到完整查询字段、证据、索引命令和优化建议
- 推荐的最终结构应是：`先汇总，再按分组展开细节`
## Batch Analysis Rules

当输入是整份日志文件、长文本、或多条慢日志时，默认按下面方式处理：

1. 先按 `ns` 归类
2. 再按“查询形态”去重
3. 对每组输出：
   - 所属集合
   - 出现次数
   - 查询形态摘要
   - 代表性慢日志特征
   - 代表性样本的查询条件 JSON
   - 是否建议先改查询还是先试索引
   - 如果能给索引建议，仍然要保留完整 `createIndex(...)` 或“当前不建议直接执行 createIndex”的模板
4. 如果多个重复样本的建议一致，应合并输出，不要逐条重复写相同建议
5. 如果同一集合里存在多种不同查询形态，应分成多个子组输出

## Uploaded File Handling

如果用户上传了日志文件，默认应：

- 直接读取用户上传文件的内容
- 优先按 AI 方式分析，不要求用户先运行本地脚本
- 先做归类和去重，再输出结果
- 但输出时必须保留代表性样本的详细结构，不能只剩汇总摘要
- 只有在用户明确要求落地导出文件时，才考虑可选脚本或本地工具

如果用户上传文件后又要求导出结果：\r\n\r\n- 默认把结果写到工作区内可访问目录\r\n- 输入来源在报告中默认只显示文件名，不显示完整本地路径\r\n- 例如应显示 `mongodb.log`，而不是 `C:\\Users\\admin\\Downloads\\mongodb.log`\r\n- 完成后默认只返回最重要产物的可点击路径；除非用户要求，否则不要额外展开“交付结果”说明\r\n\r\n## Index Recommendation Rules

统一遵循这些规则：

- 等值过滤字段优先作为复合索引前缀。
- 排序字段只有在慢日志显示排序成本明显时才纳入建议。
- 范围字段一般放在复合索引后部，除非证据明确支持别的顺序。
- 如果查询有 `$or` 且不同分支走不同字段，优先考虑“每个分支一套可命中的索引”。
- `_id` 字段默认已有索引。看到 `planSummary: IXSCAN { _id: 1 }` 或 `IXSCAN { _id: -1 }` 时，不要说“缺少 `_id` 索引”。
- 对 HAP 工作表集合（集合名以 `ws` 开头），默认认为单字段索引 `{ "_id": 1 }`、`{ "utime": 1 }`、`{ "rowid": 1 }`、`{ "ctime": 1 }` 已存在。
- 不要为 `ws*` 集合建议重复创建单字段 `_id`、`utime`、`rowid`、`ctime` 索引；如果需要使用这些字段，只能作为复合索引中的排序键或辅助键来解释。
- 如果查询同时有业务字段过滤和 `sort: { _id: 1/-1 }`，且日志显示 `IXSCAN { _id: ... }`、`docsExamined` 很高、`nreturned` 很低，应说明：当前 `_id` 默认索引主要在服务排序，不能同时高效完成业务字段过滤。
- 这类场景不要建议创建单字段 `{ "_id": 1 }` 索引，也不要把建议表述成“给 `_id` 建索引”。
- 只有当查询已改写成正向等值/范围条件，且完整 slowlog 或 explain 显示排序仍由 `_id` 路径导致大量扫描时，才建议把 `_id` 作为复合索引的尾部排序键，例如 `{ "业务过滤字段": 1, "_id": 1 }`。
- 对只有查询命令体、没有执行计划的复杂 `$or` / 空值混合查询，改写后候选索引默认先给业务等值字段和范围字段，不要默认把 `_id` 放进候选索引；只补充说明“如 explain 证明仍需按 `_id` 保序，再评估把 `_id` 作为复合索引尾部排序键”。
- 参考这篇经验文档：[MongoDB 慢查询优化](https://docs-pd.mingdao.com/deployment/components/mongodb/slowQueryOptimization)
  - 不等于、不包含、开头不是等否定条件，通常不走索引
  - 包含、为空、正则搜索、`$or` 条件，通常不走索引或索引收益很差
  - 这类查询应优先改写成正向、精确、可索引的等值查询，而不是盲目补普通索引
- 遇到 `null`、空字符串 `""`、空数组 `$size: 0`、字段不存在、`$ne/$nin/$not`、不包含、开头不是、普通包含正则等不走索引或索引收益差的查询时，优先建议在写入侧给原字段写入统一默认值。
- 默认值优化必须优先保留原字段 key，不要建议新增辅助字段或重命名字段。示例：把未填写统一写成 `"__EMPTY__"`、`"未填写"`、`0`、`false` 或业务认可的枚举值，然后查询改成 `{ "原字段": 默认值 }`。
- 默认值必须保持字段类型一致。不要让同一字段同时混用 `null`、`""`、`[]`、字符串默认值和数组值；如果历史数据已混用，应建议先做一次数据归一化，再建索引和改查询。
- 当原查询是 `{ "$or": [ { field: null }, { field: "" }, { field: { "$size": 0 } } ] }` 时，优先建议改为写入统一默认值后查询 `{ field: 默认值 }`，再基于该等值条件设计索引。
- 明确排除以下字段：
  - `_id` 单字段索引
  - `ctime`
  - `utime` 单字段索引
  - `rowid` 单字段索引
  - `status`
- 不要为低基数字段单独建议索引。
- 如果查询里出现 `status`，可以解释它是业务过滤条件，但不要把它纳入推荐索引定义。
- 如果查询里出现 `_id`、`utime`、`rowid`、`ctime`，要说明 `ws*` 集合默认已有这些单字段索引，不需要重复建议。
- 生成索引命令时：
  - 不要给索引名
  - 默认使用后台创建参数 `background: true`

## Ambiguity Handling

如果日志格式不完整、JSON 不标准、或过滤条件无法完全结构化提取：

- 允许直接从原始日志文本中推断 `$group`、`$or`、`$regex`、`$not`、`$size` 等特征
- 允许给出“基于当前可见信号”的保守结论
- 不要虚构不存在的字段
- 如果证据不足，应明确写出“不建议先补索引”或“仅能给出临时候选建议”

## Optional Local Tools

本 skill 可以带脚本，但脚本只是可选增强：

1. [`scripts/extract-slowlog-signals.ps1`](./scripts/extract-slowlog-signals.ps1)
   - 适合批量抽取日志信号
   - 适合文件输入
2. [`scripts/generate-slowlog-report.ps1`](./scripts/generate-slowlog-report.ps1)
   - 适合把结果落地成文件
   - 适合作为可选导出工具
   - 不应替代 AI 的默认分析路径

如果用户只是贴一段慢日志，或者上传一个日志文件需要直接分析，不需要主动调用这些脚本。

## Examples

直接 AI 分析：

- `用 $mongodb-slowlog-analysis 分析下面这段 MongoDB 4.4 慢日志，中文输出`
- `分析这条慢日志，告诉我为什么慢、索引怎么加、查询条件怎么改`
- `分析这个上传的 mongodb.log，按表归类并对重复查询去重汇总`
- `不要生成文件，直接在对话里分析`

直接让 AI 生成 Markdown / HTML 内容：

- `用 $mongodb-slowlog-analysis 生成一份 markdown 报告内容`
- `用 $mongodb-slowlog-analysis 生成 html 报告内容，不依赖本地脚本`

如果用户明确要求尝试真实文件导出，再说明：

- `md/html` 可以直接由 AI 生成并保存
- `docx/pdf` 通常需要本地转换工具，这属于可选增强

## Reference

需要复查规则时，读取 [`references/mongodb-4.4-slowlog-guidelines.md`](./references/mongodb-4.4-slowlog-guidelines.md)。重点关注：

- MongoDB 4.4 慢日志信号如何解读
- 候选索引字段如何排序
- 为什么本项目要排除 `ctime` 和 `status`
- [MongoDB 慢查询优化](https://docs-pd.mingdao.com/deployment/components/mongodb/slowQueryOptimization) 中关于否定条件、`$or`、正则查询和后台创建索引的经验规则

## Index Output Template

索引相关输出必须走下面两种模板之一，不要混用，也不要只给一个孤立的 `use 库名`：

1. `可直接建索引`
   - `索引建议`：给出候选索引形态
   - `索引创建命令`：给出完整 Mongo Shell 命令，至少包含：
     - `use 库名`
     - `db.getCollection("集合名").createIndex(..., { background: true })`

2. `暂不建议直接建索引`
   - `索引建议`：明确写“当前不建议直接创建普通索引”
   - `索引创建命令`：明确写“当前不建议直接执行 createIndex，请先改写查询条件”
   - 不要只输出 `use 库名`
   - 如果确实需要补充，也只能补“改写完成后再回到这里生成候选索引命令”的说明

补充规则：
- 如果当前判断是“先改查询条件”，则不要伪造 `createIndex(...)` 命令来凑模板。
- 这类场景必须明确写出“当前不建议直接执行 createIndex，请先改写查询条件”。
- 不允许只输出一个孤立的 `use 库名`。

## Post-Rewrite Candidates

如果当前结论是“暂不建议直接建索引”，但日志里仍然能看出较明确的正向过滤字段、范围字段或排序字段，则报告应额外给出一个：

- `改写后候选索引 / Post-Rewrite Candidate Indexes`

这一节的作用是：
- 先明确“不是现在就执行 createIndex”
- 再保留“等你把查询改写成正向可索引条件后，优先测试哪组索引”的方向

输出要求：
- 这一节只能给“候选索引形态”，不能伪装成当前可直接执行的索引命令
- 如果是 `$or` 场景，可以额外给出“分支索引”示例
- 如果存在较明确的单一路径候选，应标记为 `主候选索引 / Primary candidate index`
- 如果存在 `$or` 分支拆分后的候选，应标记为 `分支候选索引 / Branch candidate indexes`
- 这一节应放在 `索引创建命令` 之后、`查询优化建议` 之前

## Fixed Keys Rule

对于这类 MongoDB 动态业务字段，默认视为：
- 字段 key 固定
- 不允许为了优化慢查询而随意重命名已有字段 key

因此在给建议时必须遵守：
- 不要建议“把现有字段改名”
- 不要把“重命名原字段 key”当作优化方案
- 如果同一字段在日志里同时出现等值判断和 `$size/$not/$ne` 等复杂谓词，应把它标记为“混合约束字段”，不要把它直接当作可建索引前缀
- 对混合约束字段，优先建议：保留原字段 key 不变，在写入侧统一默认值，把复杂判断改成精确等值查询
- 不要把“新增辅助字段/派生字段”作为默认建议；只有用户明确说不能改原字段写入值、但允许新增字段时，才把辅助字段作为备选方案
- 如果业务也不允许新增字段，则应优先建议：
  - 收敛查询条件
  - 预聚合
  - 报表中间表
  - 专门检索方案

在 aggregate 场景下尤其要注意：
- `regex`
- `$ne/$nin/$not/$size`
- 复杂 `$or`
这些场景应优先建议“在原字段上统一默认值并改成精确查询”，不能建议“改原字段 key”。只有用户明确允许新增字段且不允许改原字段值时，才把辅助字段作为备选。




