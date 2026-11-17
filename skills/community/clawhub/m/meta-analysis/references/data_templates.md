# Data Input Templates / 数据输入模板

## Type 1: Binary Data / 二分类数据

**Required columns / 必填列**:

| study | n_exp | event_exp | n_ctrl | event_ctrl | year |
|-------|-------|-----------|--------|------------|------|

**Example / 示例**:

| study | n_exp | event_exp | n_ctrl | event_ctrl | year |
|-------|-------|-----------|--------|------------|------|
| Zhang2020 | 100 | 15 | 100 | 30 | 2020 |
| Wang2019 | 80 | 20 | 80 | 35 | 2019 |
| Liu2021 | 120 | 10 | 120 | 25 | 2021 |

**Column descriptions / 列名说明**:
- `study`：研究名称/ID（必填）
- `n_exp`：处理组总人数（必填）
- `event_exp`：处理组发生事件人数（必填）
- `n_ctrl`：对照组总人数（必填）
- `event_ctrl`：对照组发生事件人数（必填）
- `year`：发表年份（选填，用于元回归）
- `arm`：臂标识（选填，多臂/多对照试验用；如 `BCG-Moreau` / `BCG-Prague`，区分同一试验的不同干预臂）

**Covariate columns / 协变量列（选填）**:
通过 `extract_assist.py scaffold --covariates "latitude,allocation,vaccine_type"` 追加。
协变量与主结局列同表固化，用于**亚组分析 / 元回归**（如 BCG 效力随纬度变化）。
- 数值型协变量（`latitude`, `followup_years`, `age_mean`, `dose` 等）→ 自动 float 校验
- 分类型协变量（`allocation`, `vaccine_type`, `region` 等）→ 字符串透传
- 无法定位填 `NR`（该研究在元回归中被剔除，不阻断）

**Notes / 说明**:
- Column names are case-insensitive / 列名不区分大小写
- Chinese column names supported (e.g., "研究名称" instead of "study") / 支持中英文列名
- **零事件单元**（event_exp=0 或 event_ctrl=0）：RR/OR 在该单元无定义，validate 会告警，
  引擎自动做连续性校正（+0.5）；如需 risk difference 用 `--measure RD`。
- **多臂/多对照**：同一 `study` 多行 = 同一试验多个臂/对照比较，validate 会提示独立性风险
  （直接全纳会破坏独立性假设、低估 SE）。请用 `arm` 列区分，并考虑多臂稳健方差估计（RVE）。

---

## Type 2: Continuous Data / 连续型数据

**Required columns / 必填列**:

| study | n_exp | mean_exp | sd_exp | n_ctrl | mean_ctrl | sd_ctrl | year |
|-------|-------|----------|--------|--------|-----------|---------|------|

**Example / 示例**:

| study | n_exp | mean_exp | sd_exp | n_ctrl | mean_ctrl | sd_ctrl | year |
|-------|-------|----------|--------|--------|-----------|---------|------|
| Smith2020 | 50 | 12.3 | 3.2 | 48 | 10.1 | 2.8 | 2020 |
| Doe2019 | 65 | 15.6 | 2.9 | 60 | 13.2 | 3.0 | 2019 |
| Lee2021 | 40 | 11.8 | 3.5 | 42 | 10.5 | 3.2 | 2021 |

**Column descriptions / 列名说明**:
- `study`：研究名称/ID（必填）
- `n_exp`：处理组样本量（必填）
- `mean_exp`：处理组均值（必填）
- `sd_exp`：处理组标准差（必填）
- `n_ctrl`：对照组样本量（必填）
- `mean_ctrl`：对照组均值（必填）
- `sd_ctrl`：对照组标准差（必填）
- `year`：发表年份（选填）

**Notes / 说明**:
- Supports mean ± 95%CI input (auto-convert to SD) / 支持输入均值±95%CI（自动转换为SD）
- Ensure SD is standard deviation, not SEM / 请确保 SD 是标准差，不是 SEM（标准误）

---

## Type 3: Pre-calculated Effect Sizes / 已有效应量

**Required columns / 必填列**:

| study | effect_type | effect_size | lower95 | upper95 | year |
|-------|-------------|-------------|---------|---------|------|

**Example / 示例**:

| study | effect_type | effect_size | lower95 | upper95 | year |
|-------|-------------|-------------|---------|---------|------|
| Zhao2020 | lnOR | 0.35 | -0.12 | 0.82 | 2020 |
| Chen2019 | lnOR | 0.52 | 0.10 | 0.94 | 2019 |
| Sun2021 | SMD | 0.28 | -0.05 | 0.61 | 2021 |

**Column descriptions / 列名说明**:
- `study`：研究名称/ID（必填）
- `effect_type`：效应量类型（必填）：`lnOR` / `SMD` / `ROM` / `ZCOR` / `logHR`
- `effect_size`：效应量值（必填，lnOR 等已取对数的值）
- `lower95`：95%CI 下限（必填）
- `upper95`：95%CI 上限（必填）
- `year`：发表年份（选填）

**Auto-calculation / 自动计算**:
- SE from CI: `SE = (upper95 − lower95) / (2 × 1.96)`
- Variance: `vi = SE²`
- Original OR will be auto-transformed to logOR / 原始 OR 会自动转换为 logOR

---

## Type 3b: Rate Ratio (IRR) / 率比数据

**Required columns / 必填列**:

| study | a | b | c | d | year |
|-------|---|---|---|---|------|

- `a`：处理组事件数；`b`：处理组人时（分母，person-time）
- `c`：对照组事件数；`d`：对照组人时

**调用**：`ma_analyze(data, type="rate", measure="IRR")`

---

## Type 3c: Correlation / 相关系数

**Required columns / 必填列**:

| study | r | n | year |
|-------|---|---|------|

- `r`：Pearson 相关系数；`n`：样本量

**调用**：`ma_analyze(data, type="correlation")` → Fisher z 变换，森林/漏斗图自动反变换为 r

---

## Type 3d: Single-Group Proportion / 单组率

**Required columns / 必填列**:

| study | events | n | year |
|-------|--------|---|------|

- `events`：发生数；`n`：总数

**调用**：`ma_analyze(data, type="single_proportion", measure="PLOGIT")` → logit 变换（默认），图自动反变换为比例；量度 `PRAW` 为原始比例
> 2026-09-01 口径统一：主口径 `PLOGIT`/`PRAW`（与 coze 主路径 `metaprop(sm="PLOGIT")` 一致）；旧写法 `PLO`/`PR`（metafor 名）仍作为等价别名接受。

---

## Type 3e: Single-Group Mean / 单组均值

**Required columns / 必填列**:

| study | mean | sd | n | year |
|-------|------|----|---|------|

- `mean`：均值；`sd`：标准差；`n`：样本量

**调用**：`ma_analyze(data, type="single_mean", measure="MN")`

---

## Type 4: File Upload / 文件上传

**Supported formats / 支持格式**: `.csv`, `.xlsx`, `.xls`

**Auto-detection / 自动检测**:
- File encoding (UTF-8 / GBK) / 文件编码识别
- Column matching (Chinese/English) / 列名匹配（中英文兼容）
- Missing value detection / 缺失值检测
- Data type check / 数据类型检查
- Record count confirmation / 记录数量确认

**Recommendations / 建议**:
- Encoding: UTF-8 (avoid Chinese garbling) / 编码：UTF-8（避免中文乱码）
- Delimiter: comma / 分隔符：逗号
- First row: column names / 首行：列名

**文档 / 模板类上传（docx / pptx / pdf / doc）不属于本表范围**：非结构化文档按 **ct-base §6.7**（`ct-base/docs/03-interaction-constraints.md`）处理——先转 md/文本再提取研究数据（共享转换器 `scripts/office_to_md.py`；`.pdf` 走环境 pdf 技能；`.doc` 提示安装 word-reader / antiword）；**转换前须向用户展示 §6.7.2 提示**（PPT 转换易丢非文本元素）。结构化数据（csv/xlsx/xls）仍走本表验证流程；文档内容若涉密，按 §6.7.3 由用户决定出域与否（技能不主动拦截）。⚠️ 本技能默认计算路径为 coze 云端——会向 coze 端点发送汇总统计量（事件数/样本量/效应量等，不含个人身份信息）；若用户**强制要求数据不出域**，云端路径无法满足，需明确告知并建议改用离线工具（开发调试用的 `adapters/_dev/local_engine.py` 不随发布包分发，不在运行路径内）。

---

## Validation Checklist / 验证检查清单

| Check / 检查项 | Pass / 通过 | Fail / 不通过 |
|----------------|-------------|---------------|
| Records ≥ 2 / 记录数≥2 | ✅ X studies detected / 检测到X项研究 | ⚠️ Need ≥ 2 / 至少需要2项 |
| Required columns / 必填列完整 | ✅ All columns found / 全部必填列检测到 | ❌ Missing: XXX / 缺少列：XXX |
| No missing values / 无缺失值 | ✅ Complete / 完整 | ⚠️ X missing / 发现X个缺失值 |
| Valid numbers / 数值合理 | ✅ Range OK / 范围合理 | ⚠️ Outliers in XX / XX列有异常值 |
| Year format / 年份格式 | ✅ Year detected / 年份正确 | ℹ️ No year column / 未检测到年份列 |

**After passing all checks / 通过所有检查后**:

```
✅ Data validation complete / 数据格式检查完成
   - Studies: X / 研究数量：X
   - Data type: XXX / 数据类型：XXX
   - Covariates: XXX / 协变量字段：XXX
   - Missing values: None / X / 缺失值：无 / X

[Show first 3 rows preview / 展示前3行数据预览]

Confirm? Reply "1" to continue. / 确认无误？回复"1"继续分析。
```
