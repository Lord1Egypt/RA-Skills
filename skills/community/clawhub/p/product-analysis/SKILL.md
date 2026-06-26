---
name: product-analysis
version: v6.6
description: >-
  产品需求分析专用 skill。触发词：「分析需求」「产品分析」「业务流程」「功能架构」「PRD」「改版」「迭代需求」，
  或用户上传需求文档/PRD 时。支持快速模式（3步）、标准模式（5步）、迭代模式（Diff分析）三种工作流，
  输出 Mermaid 流程图、功能架构、埋点方案、PRD、开发 Ticket 等文档。
---

# 产品需求分析

提供结构化的产品需求分析工作流程，生成专业的业务流程图和架构设计文档。

> **命名规范**
> - **Phase**（阶段）：主流程顶层阶段，编号 Phase 1–5，不出现在用户确认话术中
> - **Step**（步骤）：子工作流内部步骤，编号 Step 1–N，确认话术引用格式：`快速模式-Step2`
> - 两套编号互不干扰，消除歧义

---

## 核心工作流程（5 个 Phase）

---

### Phase 1：读取需求信息

**文件上传时**：
```bash
view /mnt/user-data/uploads/<文件名>
```
提取：产品/功能名称、核心目标、涉及用户角色、主要功能点列表。

**直接描述时**：从用户描述提取上述信息，必要时使用 **5W1H** 澄清（What/Why/Who/When/Where/How）。

**产出**：向用户展示需求解析摘要，等待用户确认或补充后进入 Phase 2。

---

### Phase 2：评估复杂度并确认工作模式

#### 评分表

| 评估维度 | 低 | 中 | 高 |
|:---|:---|:---|:---|
| 功能点数量 | 1–3 个 (3分) | 4–8 个 (7分) | 9+ 个 (10分) |
| 用户角色数 | 1 个 (2分) | 2–3 个 (5分) | 4+ 个 (10分) |
| 系统集成 | 无 (0分) | 1–2 个 (3分) | 3+ 个 (7分) |
| 业务规则复杂度 | 简单 (3分) | 中等 (7分) | 复杂 (10分) |
| 数据复杂度 | 简单 (3分) | 中等 (7分) | 复杂 (10分) |

> **权重说明**：「系统集成」上限 7 分，低于其他维度的 10 分。原因：系统集成复杂度主要影响技术实现难度，对产品分析本身的宽度和深度影响相对较小；其他 4 个维度直接决定分析的业务复杂度和文档体量。

**评分范围**：最低 11 分（3+2+0+3+3），最高 47 分（10+10+7+10+10）。

**复杂度判定**：
- **11–20 分**：低复杂度 → **快速模式**（3 步，默认连续执行）
- **21–35 分**：中等复杂度 → **标准模式**（5 步，调研可选，分步确认）
- **36–47 分**：高复杂度 → **完整标准模式**（5 步，调研必选，分步确认）

**临界升档规则**：若总分在 18–22 分或 33–37 分的临界区间，且任意一个维度评为「高」，自动升一档。

**向用户确认**：

> "基于复杂度评估（__分），推荐使用 **[模式名称]**。
>
> **快速模式**：3 步完成，默认全部执行后一次性交付，适合快速出结果。
> **标准模式**：5 步完成，每步确认后继续，适合正式立项。
> **迭代模式**：3 步完成，专为存量功能改版设计，聚焦 Diff 分析，适合已有产品的需求变更。
>
> 【快速模式专属】默认在 3 步完成后一次性交付所有产出。如需分步确认，请现在告知。
>
> 确认继续使用推荐模式，或告知我您的选择？"

**迭代模式触发规则**（满足任一条即优先推荐迭代模式，不受复杂度评分限制）：
- 用户描述包含「改版」「迭代」「优化现有」「在 XX 基础上」等语义
- 用户上传了现有 PRD、功能文档或设计稿
- 需求以变更语言描述（「把 XX 改成 YY」「增加 XX 能力」「去掉 XX」）

---

### Phase 3：执行前准备

**创建本次调用专属输出目录并持久化**（`OUTPUT_DIR` 贯穿全流程，通过文件持久化解决跨 bash_tool 调用变量丢失问题）：
```bash
# [名称] 取自 Phase 1 提取的产品/功能名称，去除空格和特殊字符
OUTPUT_DIR="/mnt/user-data/outputs/[名称]-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$OUTPUT_DIR"
# 持久化路径，后续所有步骤通过此文件读取
echo "$OUTPUT_DIR" > /tmp/pa_output_dir.txt
echo "输出目录已创建：$OUTPUT_DIR"
```

**后续步骤读取 OUTPUT_DIR 的标准方式**（每次新的 bash_tool 调用开头执行）：
```bash
OUTPUT_DIR=$(cat /tmp/pa_output_dir.txt)
```

> 每次调用生成独立子文件夹，多次分析结果不相互混入。`/tmp/pa_output_dir.txt` 在单次会话内持久，会话结束自动清理。

**定位 Skill 脚本目录**（供自动化质量检查使用，Phase 3 执行一次后各步骤复用）：
```bash
# 按常见部署路径逐一探测，找到即停止
SKILL_BASE=""
for _p in \
  "/mnt/skills/public/product-analysis6.5" \
  "/mnt/skills/public/product-analysis" \
  "/mnt/skills/user/product-analysis6.5" \
  "/mnt/skills/user/product-analysis"; do
  if [ -f "$_p/scripts/validate_mermaid.py" ]; then
    SKILL_BASE="$_p"
    break
  fi
done
if [ -z "$SKILL_BASE" ]; then
  echo "WARN: 未找到脚本目录，自动化检查将跳过（不影响交付）"
else
  echo "SKILL_BASE=$SKILL_BASE"
  echo "$SKILL_BASE" > /tmp/pa_skill_base.txt
fi
```

**后续步骤读取 SKILL_BASE 的标准方式**：
```bash
SKILL_BASE=$(cat /tmp/pa_skill_base.txt 2>/dev/null || echo "")
```

**读取工作流指南**（Phase 3 必须执行）：
- 快速模式 → `guides/fast-workflow.md`
- 标准模式 → `guides/standard-workflow.md`
- 迭代模式 → `guides/iteration-workflow.md`

**按需读取参考文档**（执行对应任务时再读）：
- `references/analysis-frameworks.md` — 需要应用分析框架时
- `references/flowchart-standards.md` — 需要创建流程图时
- `references/exception-checklist.md` — 需要识别异常场景时
- `references/architecture-patterns.md` — 需要设计架构时

**推荐读取示例**（以下情况 SHOULD 主动读取）：
- 首次执行该行业类型需求、或不确定流程图层级组织时
- 快速模式 → `examples/simple-feature-analysis.md`
- 标准模式 → `examples/complex-system-analysis.md`

---

### Phase 4：执行工作流程

**以子工作流文件为唯一权威**（含步骤、确认机制、质量检查、调研时机、最终交付）：
- 快速模式 → `guides/fast-workflow.md`
- 标准模式 → `guides/standard-workflow.md`

> SKILL.md 不重复描述步骤内容，一切以子工作流为准，避免不一致。

---

### Phase 5：最终交付

**以子工作流末尾的「最终交付」章节为准**。

**文件命名规范（含日期后缀）**：

| 文档类型 | 快速版文件名 | 标准版文件名 | 迭代版文件名 |
|:---|:---|:---|:---|
| 业务流程分析报告 | `[名称]-业务流程分析-快速版-YYYYMMDD.md` | `[名称]-业务流程分析-标准版-YYYYMMDD.md` | `[名称]-变更分析-YYYYMMDD.md` |
| 功能架构设计 | `[名称]-功能架构设计-快速版-YYYYMMDD.md` | `[名称]-功能架构设计-标准版-YYYYMMDD.md` | `[名称]-功能架构设计-迭代版-YYYYMMDD.md` |
| 埋点方案 | `[名称]-埋点清单-快速版-YYYYMMDD.md` | `[名称]-埋点方案设计-标准版-YYYYMMDD.md` | — |
| 完整 PRD 文档 | `[名称]-PRD-快速版-YYYYMMDD.md` | `[名称]-PRD-标准版-YYYYMMDD.md` | `[名称]-PRD-迭代版-YYYYMMDD.md` |
| 开发任务拆解清单 | `[名称]-Tickets-快速版-YYYYMMDD.md` | `[名称]-Tickets-标准版-YYYYMMDD.md` | `[名称]-Tickets-YYYYMMDD.md` |

> `YYYYMMDD` 为执行日期（如 `20260220`）。所有文件保存至 Phase 3 持久化的专属目录（路径从 `/tmp/pa_output_dir.txt` 读取）。

---

## 资源库

| 类型 | 路径 | 说明 |
|:---|:---|:---|
| **工作流指南** | `guides/fast-workflow.md` | 快速模式权威来源（步骤+确认+质量+最终交付） |
| **工作流指南** | `guides/standard-workflow.md` | 标准模式权威来源（步骤+确认+质量+最终交付） |
| **工作流指南** | `guides/iteration-workflow.md` | 迭代模式权威来源（Diff分析+影响面+变更规格） |
| **确认话术** | `guides/confirmation-templates.md` | 分步确认标准模板（含迭代模式模板） |
| **交付确认** | `guides/delivery-confirmation-dynamic.md` | 动态拼装式最终交付确认指南 |
| **确认规范** | `guides/step-confirmation-checklist.md` | 确认机制执行规范 |
| **质量检查** | `guides/quality-checklist.md` | 各步骤质量检查清单 |
| **速查表** | `guides/quick-reference.md` | 核心信息一页纸速查（含初始化命令） |
| **故障排除** | `guides/troubleshooting.md` | 常见问题解决方案 |
| **分析框架** | `references/analysis-frameworks.md` | 用户故事、KANO、MECE、JTBD、RICE 等框架 |
| **流程图规范** | `references/flowchart-standards.md` | Mermaid 绘图标准 |
| **异常清单** | `references/exception-checklist.md` | 四类异常系统检查清单 |
| **架构模式** | `references/architecture-patterns.md` | 常见架构模式参考 |
| **文档模板** | `assets/` | 交付文档模板（含 tickets.tpl.md Ticket 拆解模板） |
| **示例** | `examples/` | 快速/标准/迭代模式完整示例 |
| **自动化脚本** | `scripts/` | Mermaid 验证和质量检查工具 |
| **暂存目录** | `files/` | 系统保留（见 files/README.md） |

---

## 故障排查

| 问题 | 解决方案 |
|:---|:---|
| 需求模糊 | 使用 5W1H 引导澄清，澄清后重新评分再确认模式 |
| 脚本执行失败 / 脚本目录未找到 | 输出 SKIP 提示，改为人工检查；脚本失败不影响交付 |
| OUTPUT_DIR 读取为空 | 重新执行 Phase 3 初始化命令（见 quick-reference.md Section 3）重建 `/tmp/pa_output_dir.txt` |
| 用户拒绝推荐模式 | 解释各模式差异，尊重用户最终选择 |
| 临界复杂度难以判断 | 参考升档规则；不确定时选更详细的模式 |
| 更多问题（含用户中途修改需求范围） | 参见 `guides/troubleshooting.md` |
