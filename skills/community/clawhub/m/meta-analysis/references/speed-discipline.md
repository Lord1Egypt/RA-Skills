# §0 执行纪律 · 扩展备查（speed-discipline）

> 本文件是 `SKILL.md` §0 执行纪律的完整扩展。主文件只保留「双轨门控 + 操作卡 + 5 条铁律 + 指向」，
> 需要深度理解边界 / 例外 / 反模式时读此文件。**默认快路径 agent 无需读它——5 条铁律已足够约束。**

## 0.0 Two-track gating / 双轨门控

首条用户消息必须经由 `python scripts/classify.py "<query>"` **确定性分流**（关键词表映射，零 LLM 决策）。两条轨道：

- **计算轨（compute）**：Simple / 清晰的 Complex（"合并这 4 项 OR"、"画森林图"、"亚组分析"）→ 描述即执行：`python scripts/build_request.py --query "..." --data-json '[...]' --out request.json`（内部调 `classify.py` 出 spec + 装配 request.json，1 次调用）→ `python adapters/run_analysis.py request.json` → `present_files(html)`。受本 §0 速度纪律**全约束**（规则 1–6 + 延迟不变量）。
- **选题轨（topic）**：Vague / "没方向" / 可行性 / 选课题 / "被拒为重复" → `adapters/literature_probe.py`（代码跑真实命中数）→ `generate_topic_report.py` → `present_files`。**允许结构化推理，但零自由发挥**：候选排序必须基于探针真实命中数，禁止 LLM 拍脑袋补充"我觉得哪个方向好"的论述。

> 速度纪律规则 1–6 的**显式适用范围 = 计算轨**；选题轨单列"代码接地、不靠思考"规则。两条轨道都**禁止**为"确认怎么调 / 该用哪个 task"去 Read/Grep/Bash 翻 SKILL.md / references / adapter / config——那是 `classify.py` 的职责，不是 LLM 的。

**核心原则：准备数据 → 调 `run_analysis` → 呈现 HTML，三步到位。严禁任何"深度思考/反思/复盘/再推导"。**

## 0.0.1 Agent 操作卡（照抄执行，禁止改花样）

> 计算轨就这一条命令，**复制即可，不要做任何其他事**（不要读源码、不要 grep、不要写长解读、不要手算）：

```bash
python scripts/run_meta.py --query "<用户原始请求>" --data "<数据csv绝对路径>"
```

- 运行后从 stdout 读取 `META_HTML_REPORT=<绝对路径>` 这一行，直接用 `present_files` 打开该路径即可（报告已内联全部 SVG + 统计表）。
- 跨轮 follow-up（如"去掉北美再算"）：先对数据做子集生成新 csv（这是数据处理，允许），再发**同一条** `run_meta.py` 命令指向新 csv + 新 query。`run_meta.py` 每次独立、完整地由 query+data 决定一切，不要试图从对话历史"继承设置"做复杂合并。
- 选题轨（用户说"没方向 / 选课题 / 可行性"）**不要**用 `run_meta.py`——走 `literature_probe.py` + `generate_topic_report.py`。
- 兜底：若 `run_meta.py` 打印 `META_STATUS=build_failed` 且提示列名未解析，按提示用 `--colmap '{"规范键":"实际列名"}'` 或 `--measure`/`--model` 回灌重跑（仅最小判断，禁止重读文档/重算）。

## 规则 1–7（完整）

1. **禁止深度思考（HARD BAN）**：大模型在跑本技能时**只做流程执行**，不做任何额外推理、方案权衡、结果复核或自我解释。这些"思考"除浪费时间外毫无意义。拿到数据即归一化、即调用、即呈现，不犹豫、不展开、不追问（除非输入确实缺字段——此时只问缺的字段，不展开讨论）。
   - ⚠️ **跨轮引用 carve-out**：上列禁令**仅约束计算/呈现阶段**。当用户显式引用前文（"用之前的数据""和刚才一样"等）时，LLM **允许**回看对话历史提取既有数据/spec **用于回填 `--data-json`/参数**，但**禁止**据此重新推导数值或重路由——这属于合法使用长上下文，不破本纪律。
2. **最快路径执行**：前期数据整理、后期结果呈现，一律走最短路径——
   - 不重复校验已返回的数值；
   - 不重新推导 / 不自行计算任何统计量（OR、CI、I² 等一律原样引用 coze 返回的 `stats`）；
   - 不重绘、不二次渲染任何图形。
3. **上下文只给文字分析结果**：对话流里**只输出文字版分析结论**（来自 `stats` 原样引用 + 一句必要解读），**绝不在对话流内联图形**（`show_widget` 已废止）。
4. **HTML 直出，不做任何渲染**：`run_analysis` 生成的 `out['html_report']`（聚合 HTML 报告，内嵌所有 `figures[].svg`）即**最终交付物**。大模型**不得**对其内容做任何再加工 / 再排版 / 再渲染 / 重新抽取数值——直接 `present_files` 打开预览即可。图形只在 HTML 中展示，按原始宽度、过宽滚动。
5. **数字零改写**：所有数值必须原样引用 coze 返回的 `stats` / `pooled` / `heterogeneity` / `bias`，禁止大模型四舍五入、换算或重新格式化（呈现层硬约束 #1 同义重申）。
6. **后端绝对锁定 coze（HARD BAN 本地计算）**：**严禁**用本地 R 或 Python（含 `statsmodels`/`scipy`/`metafor`/`meta` 等）自行完成任何 meta 分析计算——**连"考虑用本地算"都不允许**。所有需求一律**严格转发 coze 端点执行**（`adapters/run_analysis.py` → `https://ct-meta.coze.site/run`）。无论用户是否声明"本地算"，均不走本地；若 coze 不可达/未授权，按技能 §6 返回结构化错误，**绝不静默回落本地**。本技能无本地-R 回退分支。
7. **有边界 LLM 兜底（error-only，不破默认快路径）**：`build_request.py` 先对列名做**别名自动匹配**（中/英同义表），仍解析不出才发 `needs_llm_fallback` JSON（exit 2）。此时 LLM **仅做最小判断**——补 `-colmap` 缺的列映射或 `-measure`/`-model` 纠正参数后**重跑** `build_request.py`，**禁止**重读 SKILL/references/adapter/config、禁止重算任何统计量。非数值/缺值等用户数据错误一律硬错误（exit 1），不触发兜底。默认快路径（列名规范/可别名匹配）仍是 1 次调用、零 LLM。

## Latency invariants / 延迟不变量（防回归硬指标，违规 = 拖慢）

- **计算轨 fire 前本地工具调用 ≤ 1**：唯一允许的火前动作 = `python scripts/build_request.py ...`（内部调 `classify.py` 出 spec 并装配 `request.json`，1 次调用即完成轨道判定 + 归一化 + 列名对齐）。**禁止**为"确认怎么调 / 该用哪个 task / 列名怎么填"去 Read/Grep/Bash 翻 SKILL.md / references / adapter / config。
  - **兜底例外**：仅当 `build_request.py` 返回 `needs_llm_fallback` 时，允许 +1 次 LLM 判断（补给 `-colmap`/`-measure`/`-model` 后重跑）；此分支属错误恢复、非默认快路径，且 LLM 动作严格受限（规则 7）。
  - **跨轮回填例外**：用户引用前文（"用之前的数据"等）时，LLM 回看对话历史提取既有数据用于**构造** `--data-json` 属合法动作，**不计入**火前调用次数（构造入参不是额外工具调用）；回填后仍是 1 次 `build_request.py`。此例外仅放宽"数据来源"，不放宽规则 1 的计算/呈现禁令。
- **计算轨 fire 后本地工具调用 ≤ 1**：唯一允许的火后动作 = `present_files` 打开 HTML 报告。禁止再跑 Bash 抽数、重排表、重绘/重渲染。
- **选题轨本地工具调用 ≤ 2**：`literature_probe.py` + `generate_topic_report.py`；无 LLM deliberation 循环、无重复检索。
- **禁止循环重试**：任何步骤不得为"结果不满意"而重复调用 coze / 重排；coze 失败按 §6 结构化报错，无本地兜底。

## 0.1 已由代码自动化的事（agent 严禁重复做 / 严禁为"确认它能做"去读源码）

> 这些能力**已在 adapter 内实现**，agent 只需发对 query / 传对文件，不要画蛇添足，更不要为"验证它确实做了"去 `Read`/`Grep`/`Bash` 翻 `build_request.py`/`classify.py`/`coze_cases`/`config.json`——那正是 §0 禁止的探索行为，也是"大模型深度思考浪费"的主要来源。

1. **亚组变量列自动透传**：`build_request.py` 已从 `classify.py` 的 `params_extra.subgroup`（由 query 中"按 X 亚组 / by X / subgroup X"正则提取）取出该列名，自动加入 `carry_cols` 原样透传进 `request.json.data.rows`，并写入 `params.subgroup`。**agent 只需在 query 写"按 region 亚组分析"，切勿手动拼 Python 把 region 等列补回 request.json，也切勿改 `byvar`/`group`/`by`（coze 只认 `subgroup`，其余静默失效）。** 列名不匹配交由别名表自动匹配；仅当 `build_request` 返回 `needs_llm_fallback`（exit 2）才补 `--colmap` 重跑。
2. **列名中/英别名自动匹配**：`COLUMN_ALIASES`（二分类 event/n、连续 mean/sd、NMA 多格式）已由 `_resolve_colmap` 自动匹配，agent 不读该表即可信赖。
3. **亚组差异显著性（组间 Q_between）= 走 `metareg`**：`metareg` 端点**已接线**（见 §端点能力边界）。`subgroup_analysis` 端点**不返回 Q_between 属已知限制**——agent 不要在每轮结论里重复声明"缺 Q_between 无法下结论"，应直接建议用户改用 metareg（需已算效应量列 `te`/`sete` + 协变量列，以 `params.cov` 传入）。
4. **产物完整性由 `run_analysis` 保证**：`run_analysis` 生成的 `out['html_report']` 内联全部 `figures[].svg`（森林图/漏斗图/Egger/L'Abbé/影响诊断/剪补…），生成失败被捕获且不中断主结果。**禁止** fire 后用 `Bash` `grep "<svg"` / `grep "漏斗图"` 等"验证产物是否完整"——纯浪费轮次，且违反 fire 后 ≤1 不变量（唯一允许 `present_files`）。改为读取 `run_analysis.py` / `run_meta.py` stdout 的 `META_HTML_REPORT=<abs path>` 行直接 `present_files`，无需任何额外 Bash 探索。

## 0.2 反模式清单（违反 §0 的 concrete 行为，明令禁止）

- ❌ fire 前 `Read`/`Grep`/`Bash` 翻 `build_request.py`/`classify.py`/`run_analysis.py`/`rendering.py`/`coze_client.py`/`config.json`/`coze_cases/*.json` 去"确认调用方式 / 列名怎么填 / subgroup 怎么传"。
- ❌ fire 后 `Bash` `ls output/*.html` / `grep "<svg"` / `grep "漏斗图"` 等"找/验证报告"。正确做法：从 `run_meta.py` / `run_analysis.py` 的 stdout 读取 `META_HTML_REPORT=<abs path>` 行，直接 `present_files` 该路径（零额外 Bash）。
- ❌ 每轮生成长篇"证据链 / 深度解读 / 跨轮对比表 / 为什么梯度成立"——除非用户**显式**要求解释（"为什么""讲解一下"）。
- ❌ 手动 Python 把 subgroup 列补回 `request.json`；手动对 coze 返回的 log OR 做 `e^x` 换算表（云端已给 OR/CI，原样引用即可）。
- ❌ 因 `subgroup_analysis` 不返回 Q_between 而在每轮纠结/声明，应直接转 metareg。

违反上述任一条的"深度思考行为"或"本地计算冲动"均为本技能明令禁止。
