# 标准模式工作流 v6.5

适用于中高复杂度需求（评分 21–47 分），包含 5 个核心步骤。

---

## 执行前一次性准备

**首次进入本文件时读取以下文件（仅读一次，后续步骤直接使用，无需重复读取）**：
- `guides/confirmation-templates.md` — 标准模式各步确认话术（含 Step 1.5 专属模板）
- `guides/quality-checklist.md` — 各步骤详细质量检查清单

---

## 分步确认机制说明

标准模式采用**强制分步确认机制**（不随用户要求自动跳过，可切换连续模式）：

- 每步完成后立即暂停，展示实际产出（不能保留占位符）
- 明确询问用户是否确认，等待明确回复后才继续
- 如用户提出修改，修改后**必须再次确认**，不能直接进入下一步
- 如用户要求跳过确认，询问是否所有步骤都跳过，然后切换「连续执行模式」

> 确认机制详细规范（含错误/正确示例）见 `guides/step-confirmation-checklist.md`。

---

## Step 1：深入理解需求

📚 **本步参考**：`references/analysis-frameworks.md`

**核心任务**：
1. 全面分析需求的业务背景、用户、目标和约束
2. 应用 2–3 个分析框架，如「用户故事 + KANO 模型 + MECE 原则」
3. 输出完整用户角色定义（含权限矩阵）、功能清单、关键假设和风险点

**交付产物**：需求理解与分析文档、用户角色与权限矩阵、功能清单（MECE）、关键假设与风险清单

**质量检查**：
- [ ] 已应用至少 2 个分析框架并说明应用方式
- [ ] 用户角色及权限定义清晰
- [ ] 功能清单完整，符合 MECE 原则

**用户确认（MUST）**：使用已读取的 `guides/confirmation-templates.md` 中「【标准模式】Step 1 确认」模板，填入实际产出，展示并等待用户回复。

---

## Step 1.5：外部调研（按需/必选）

> **重大调整**：外部调研从原 Step 5（架构之后）提前至此，确保调研结果能指导 Step 2–4 的设计。

**触发条件**：
- 复杂度评分 36–47 分（**可选**，Step 1 确认后询问用户）
- 复杂度评分 21–35 分且需求涉及不熟悉行业领域（**可选**，Step 1 确认后询问用户）
- 用户在任意步骤明确要求竞品分析

**执行前与用户确认调研范围**：
> "为了更好地指导后续流程设计和功能架构，建议先进行外部调研。请确认调研范围：
> 1. 竞品选择（1–3 个）
> 2. 重点关注维度（功能/体验/商业模式/合规）
> 或直接回复「跳过调研，继续下一步」。"

**核心任务**：
1. 使用 `web_search` 工具进行信息检索（至少 2–3 个独立信源）
2. 整合结果：竞品分析矩阵、行业最佳实践、可落地改进建议

**web_search 不可用时的降级方案**：
- 告知用户无法进行实时调研
- 基于训练知识提供行业通用做法分析，明确标注「基于已知知识，非实时调研」
- 建议用户自行补充调研结果后告知，以更新建议

**交付产物**：调研报告（含来源引用）、竞品功能对比表、对后续设计的影响说明

**质量检查**：
- [ ] 报告中清晰引用信息来源
- [ ] 竞品对比表维度合理，结论客观
- [ ] 已明确说明调研结果将如何影响后续步骤的设计方向

**用户确认（MUST）**：使用已读取的 `guides/confirmation-templates.md` 中「【标准模式】Step 1.5 确认」模板，填入实际产出，确认后进入 Step 2。

---

## Step 2：设计完整业务流程

📚 **本步参考**：`references/flowchart-standards.md`（需要时参考 Step 1.5 调研结论）

**核心任务**：
1. 生成**高层级流程图**（战略视图）和**详细流程图**（实施视图）
2. 创建角色职责矩阵（RACI）和数据流图（DFD）

**交付产物**：高层级与详细流程图（Mermaid）、流程步骤详细说明、RACI 矩阵和数据流图

**质量检查**：
- [ ] 两级流程图均已生成，风格统一
- [ ] 流程图遵循 `references/flowchart-standards.md` 规范
- [ ] 详细项参见已读取的 `guides/quality-checklist.md`「步骤2质量检查清单」
- [ ] 自动化检查：
  ```bash
  SKILL_BASE=$(cat /tmp/pa_skill_base.txt 2>/dev/null || echo "")
  cat << 'MERMAID_EOF' > /tmp/qa_check_temp.md
  <流程图内容>
  MERMAID_EOF
  if [ -n "$SKILL_BASE" ]; then
    python3 "$SKILL_BASE/scripts/validate_mermaid.py" /tmp/qa_check_temp.md
  else
    echo "SKIP: 脚本目录未找到，人工核查 Mermaid 语法"
  fi
  rm /tmp/qa_check_temp.md
  ```

**用户确认（MUST）**：使用已读取的 `guides/confirmation-templates.md` 中「【标准模式】Step 2 确认」模板，填入实际产出，展示并等待用户回复。

---

## Step 3：进行全面异常识别

📚 **本步参考**：`references/exception-checklist.md`

**核心任务**：
1. 使用 `references/exception-checklist.md` 对业务流程逐项检查
2. 将异常按四大类（业务/场景/用户/技术）分类和优先级评估
3. 为所有 P0/P1 异常设计处理策略
4. 在详细流程图中标注异常处理路径

**交付产物**：完整异常场景清单（分类、分级）、P0/P1 处理策略说明、更新后的详细流程图

**质量检查**：
- [ ] 至少识别出 10–15 个有意义的异常场景
- [ ] 四大类异常均有覆盖
- [ ] 所有 P0/P1 异常均有明确处理策略
- [ ] 详细项参见已读取的 `guides/quality-checklist.md`「步骤3质量检查清单」

**用户确认（MUST）**：使用已读取的 `guides/confirmation-templates.md` 中「【标准模式】Step 3 确认」模板，填入实际产出，展示并等待用户回复。

---

## Step 4：设计详细功能架构

📚 **本步参考**：`references/architecture-patterns.md`（综合 Step 1.5 调研结论 + Step 3 异常清单）

**核心任务**：
1. 进行功能分层设计（表现层、业务逻辑层、数据访问层）
2. 将 Step 3 识别的 P0/P1 异常对应的兜底功能纳入架构
3. 输出详细功能模块划分、规格说明、依赖关系图和迭代规划

**交付产物**：功能架构图与分层说明（Mermaid）、详细功能规格（含验收标准）、依赖关系图与流转矩阵、迭代规划（MVP → 完整版）

**质量检查**：
- [ ] 功能划分严格遵循 MECE 原则
- [ ] Step 3 的 P0/P1 异常已有对应功能设计
- [ ] 每个核心功能有明确验收标准
- [ ] 详细项参见已读取的 `guides/quality-checklist.md`「步骤4质量检查清单」
- [ ] 自动化检查：
  ```bash
  SKILL_BASE=$(cat /tmp/pa_skill_base.txt 2>/dev/null || echo "")
  cat << 'MERMAID_EOF' > /tmp/qa_check_temp.md
  <架构内容>
  MERMAID_EOF
  if [ -n "$SKILL_BASE" ]; then
    python3 "$SKILL_BASE/scripts/validate_mermaid.py" /tmp/qa_check_temp.md
    python3 "$SKILL_BASE/scripts/check_mece.py" /tmp/qa_check_temp.md
  else
    echo "SKIP: 脚本目录未找到，人工核查 MECE 原则"
  fi
  rm /tmp/qa_check_temp.md
  ```

**用户确认（MUST）**：使用已读取的 `guides/confirmation-templates.md` 中「【标准模式】Step 4 确认」模板，填入实际产出，展示并等待用户回复。

---

## Step 5：（可选）补充深化调研

**与 Step 1.5 的区别**：

| | Step 1.5（前置调研） | Step 5（收尾调研） |
|:---|:---|:---|
| 时机 | 需求理解之后 | 功能架构设计之后 |
| 目的 | 指导整体设计方向 | 验证/细化特定设计决策 |
| 范围 | 宏观竞品/行业全局 | 某具体功能点的最佳实现 |
| 必要性 | 36+ 分必选 | 通常可跳过 |

**触发条件**（满足任一即执行）：
- Step 4 设计过程中遇到无法确定的具体实现方案（如：「通知中心的已读状态同步机制业界主流做法？」）
- 用户在 Step 4 确认时明确提出需要补充竞品对比

**若已在 Step 1.5 完成完整调研**：本步通常可跳过，直接进入最终交付。跳过时无需用户确认，在最终交付话术中注明「Step 5 已跳过（Step 1.5 调研完整覆盖）」。

**核心任务**：
1. 与用户明确本步调研的具体问题（聚焦 1–2 个功能级问题，不做全局重调）
2. 使用 `web_search` 检索 1–3 个信源，重点查找：同类功能的具体交互设计、技术实现选型、用户反馈数据
3. 输出调研结论，并明确说明对 Step 4 哪个功能规格的修订建议

**交付产物**：专项调研摘要（≤半页）、针对 Step 4 的修订建议（若有）

**web_search 不可用时**：告知用户，基于训练知识给出行业通用做法，标注「基于已知知识，非实时调研」。

**质量检查**：
- [ ] 调研问题聚焦，不超过 2 个功能级问题
- [ ] 结论有信源引用（或明确标注为已知知识）
- [ ] 已说明调研结论是否触发 Step 4 内容修订

**用户确认（MUST）**：使用 `guides/confirmation-templates.md` 中「【标准模式】Step 5 确认」模板，填入实际产出，展示并等待用户回复。

---

## 最终交付

### 询问输出格式

> "📄 **选择输出文档格式**
>
> 1. **业务流程分析报告**（完整版）— 含高层级+详细流程图、完整异常分析
> 2. **功能架构设计**（完整版）— 含功能分层、依赖关系、迭代规划
> 3. **埋点方案文档** — 完整数据埋点设计方案（13 章）
> 4. **完整 PRD 文档** — 13 章节产品需求文档
> 5. **Draw.io 图表文件** — 将流程图、架构图、状态机图、泳道图导出为可编辑的 .drawio 文件（可用 Draw.io 或 diagrams.net 打开）
> 6. **开发任务拆解清单** — 按 Epic → Story → Task 三层拆解，含 BDD 验收标准，可直接导入 Jira / Linear
>
> 标准模式建议至少选择完整 PRD（选项 4），以充分体现分析深度；给开发团队交付时加选 6；需要可视化编辑图表时加选 5。"

### 生成文档

| 选项 | 模板 | 输出文件名（含日期） |
|:---|:---|:---|
| 1. 业务流程分析报告 | `assets/business-flow.tpl.md` | `[名称]-业务流程分析-标准版-YYYYMMDD.md` |
| 2. 功能架构设计 | `assets/feature-architecture.tpl.md` | `[名称]-功能架构设计-标准版-YYYYMMDD.md` |
| 3. 埋点方案文档 | `assets/tracking-plan-template.md` | `[名称]-埋点方案设计-标准版-YYYYMMDD.md` |
| 4. 完整 PRD 文档 | `assets/prd.tpl.md` | `[名称]-PRD-标准版-YYYYMMDD.md` |
| 5. Draw.io 图表文件 | 参见「Draw.io 图表输出」章节 | `[名称]-[图表类型]-YYYYMMDD.drawio` |
| 6. 开发任务拆解清单 | `assets/tickets.tpl.md` | `[名称]-Tickets-标准版-YYYYMMDD.md` |

文件保存至 Phase 3 创建的专属目录（路径从 `/tmp/pa_output_dir.txt` 读取）：
```bash
OUTPUT_DIR=$(cat /tmp/pa_output_dir.txt)
# 示例：cp [名称]-PRD-标准版-YYYYMMDD.md "$OUTPUT_DIR/"
```

**最终质量检查**：
```bash
SKILL_BASE=$(cat /tmp/pa_skill_base.txt 2>/dev/null || echo "")
OUTPUT_DIR=$(cat /tmp/pa_output_dir.txt)
if [ -n "$SKILL_BASE" ]; then
  python3 "$SKILL_BASE/scripts/run_quality_check.py" "$OUTPUT_DIR/<文件名>.md" --type prd
else
  echo "SKIP: 脚本目录未找到，人工检查文档结构完整性"
fi

### 交付确认（MUST）

读取 `guides/delivery-confirmation-dynamic.md` 的动态拼装指引，生成交付确认话术，展示并等待用户明确回复。

**最终质量保证**：
- [ ] 所有选定文档已生成
- [ ] 体现了标准模式的分析深度（含外部调研结论）
- [ ] Mermaid 图表语法正确
- [ ] 已执行最终质量检查
- [ ] 文件命名包含 `-标准版-YYYYMMDD` 后缀，已保存至输出目录
- [ ] 等待用户明确回复

---

## Draw.io 图表输出（可选附加步骤）

**触发时机**：用户在最终交付的格式选择中选择了第 5 项（Draw.io 图表文件）。

**用户选择第 5 项时执行**：

📚 **读取**：`references/drawio-standards.md`

1. 识别本次已生成的全部 Mermaid 图（Step 2 业务流程图 + Step 3 详细流程图 + Step 4 功能架构图，以及任何状态机图、泳道图）
2. 按 `references/drawio-standards.md` 中对应图表类型的规范，逐一转换为 Draw.io XML
3. 输出 `.drawio` 文件，优先调用 MCP 工具；MCP 不可用时使用以下兜底方式直接写入：
   ```bash
   OUTPUT_DIR=$(cat /tmp/pa_output_dir.txt)
   FILENAME="[名称]-[图表类型]-$(date +%Y%m%d).drawio"
   cat << 'DRAWIO_EOF' > "$OUTPUT_DIR/$FILENAME"
   <mxfile><diagram name="Page-1"><mxGraphModel>
   <!-- 将转换后的 Draw.io XML 内容粘贴至此处 -->
   </mxGraphModel></diagram></mxfile>
   DRAWIO_EOF
   echo "文件已写入：$OUTPUT_DIR/$FILENAME（MCP 不可用，已直接写入文件）"
   ```
4. 文件命名：`[名称]-[图表类型]-YYYYMMDD.drawio`，保存至 OUTPUT_DIR
5. 展示已输出的文件清单，流程结束

**质量检查**：
- [ ] 每张 Mermaid 图均有对应 `.drawio` 文件
- [ ] 节点名称、连线方向与原 Mermaid 图一致
- [ ] 文件已保存至输出目录并展示给用户
