# 快速模式工作流 v6.5

适用于低复杂度需求（评分 11–20 分），包含 3 个核心步骤。

---

## 执行前一次性准备

**首次进入本文件时读取以下文件（仅读一次，后续步骤直接使用，无需重复读取）**：
- `guides/confirmation-templates.md` — 快速模式三步确认话术
- `guides/quality-checklist.md` — 各步骤详细质量检查清单

---

## 执行模式说明

**默认：连续执行模式**

快速模式默认在 Phase 2 时已与用户确认执行偏好：
- **连续执行模式**（默认）：3 步全部执行完毕后，一次性展示所有产出并交付文档
- **分步确认模式**（用户主动要求）：每步完成后暂停确认，等待回复后继续

> 若用户在 Phase 2 未指定，默认连续执行模式。

**连续模式中**：每步仍需执行质量检查并记录摘要；遇到需要用户决策的阻塞性问题（需求矛盾、关键信息缺失）必须中断告知，不能自行假设继续。

---

## Step 1：理解需求

📚 **本步参考**：`references/analysis-frameworks.md`

**核心任务**：
1. 分析需求背景和核心目标
2. 定义主要用户角色（及权限差异）
3. 应用 1–2 个分析框架（推荐：用户故事 + MECE 原则）
4. 列出核心功能清单，标注关键假设

**交付产物**：需求理解摘要、核心功能清单（MECE）、关键假设与待澄清问题

**质量检查**：
- [ ] 已明确应用至少一个分析框架
- [ ] 功能清单覆盖所有核心需求点，符合 MECE 原则
- [ ] 关键假设已清晰标注

**分步确认模式下**（MUST）：
使用已读取的 `guides/confirmation-templates.md` 中「【快速模式】Step 1 确认」模板，填入实际产出，展示并等待用户回复。

---

## Step 2：设计核心业务流程

📚 **本步参考**：`references/flowchart-standards.md` + `references/exception-checklist.md`

**核心任务**：
1. 生成**高层级业务流程图**（Mermaid 格式），仅含核心成功路径
2. 参考 `references/exception-checklist.md`，识别 2–3 个最高优先级异常（P0/P1）
3. 为 P0/P1 异常设计简要处理策略

**交付产物**：高层级流程图（Mermaid）、关键步骤说明、高优先级异常清单及处理策略

**质量检查**：
- [ ] 流程图遵循 `references/flowchart-standards.md` 基础规范
- [ ] 流程图对非技术人员清晰可理解
- [ ] 已识别至少 2 个关键异常（P0/P1 级别）
- [ ] 详细项参见已读取的 `guides/quality-checklist.md`「步骤2质量检查清单」
- [ ] 自动化检查（执行后删除临时文件）：
  ```bash
  SKILL_BASE=$(cat /tmp/pa_skill_base.txt 2>/dev/null || echo "")
  OUTPUT_DIR=$(cat /tmp/pa_output_dir.txt)
  cat << 'MERMAID_EOF' > /tmp/qa_check_temp.md
  <流程图内容>
  MERMAID_EOF
  if [ -n "$SKILL_BASE" ]; then
    python3 "$SKILL_BASE/scripts/validate_mermaid.py" /tmp/qa_check_temp.md
  else
    echo "SKIP: 脚本目录未找到，跳过自动化检查，改为人工核查 Mermaid 语法"
  fi
  rm /tmp/qa_check_temp.md
  ```

**分步确认模式下**（MUST）：
使用已读取的 `guides/confirmation-templates.md` 中「【快速模式】Step 2 确认」模板，填入实际产出，展示并等待用户回复。

---

## Step 3：构建简要功能架构

📚 **本步参考**：`references/architecture-patterns.md`

**核心任务**：
1. 进行功能模块划分（MECE 原则）
2. 参考 Step 2 识别的 P0/P1 异常，将对应兜底功能纳入架构：
   - 如：错误提示模块、重试机制、降级展示页、空状态处理等
3. 为核心功能进行优先级分类（P0/P1/P2）
4. 输出简要功能架构图（Mermaid 格式）和 MVP 范围建议

**交付产物**：功能架构图（Mermaid）、带优先级的功能清单（含异常兜底功能）、简要迭代建议

**质量检查**：
- [ ] 功能模块划分清晰，无明显重叠（MECE）
- [ ] Step 2 的 P0/P1 异常已有对应功能设计
- [ ] 核心功能优先级已定义
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
    echo "SKIP: 脚本目录未找到，跳过自动化检查，改为人工核查 MECE 原则"
  fi
  rm /tmp/qa_check_temp.md
  ```

**分步确认模式下**（MUST）：
使用已读取的 `guides/confirmation-templates.md` 中「【快速模式】Step 3 确认」模板，填入实际产出，展示并等待用户回复。

---

## 轻量版调研（按需扩展）

**触发条件**：快速模式执行期间，用户明确要求竞品分析或行业调研。

**执行规则**：不升级为标准模式，在当前步骤确认完成后立即执行：
1. 与用户确认调研主题（1–2 个竞品或行业关键词）
2. 使用 `web_search` 工具检索 1–2 个信源
3. 输出格式：简要竞品对比表（功能/优劣势/可借鉴点），不超过 1 页
4. 执行分步确认后继续原流程

**web_search 不可用时**：基于训练知识给出行业通用做法，明确标注「基于已知知识，非实时调研」。

---

## 最终交付

### 连续执行模式下的一次性产出展示（含格式选择）

完成 3 步后，**在同一条消息中**展示所有步骤产出摘要，并同时询问输出格式，减少用户确认轮次：

```
✅ 快速模式全流程完成

Step 1 产出摘要：[需求摘要 + 功能清单核心内容]
Step 2 产出摘要：[流程图 + 关键异常清单]
Step 3 产出摘要：[架构图 + 功能优先级清单]

以上内容是否符合预期？请同时选择输出文档格式（可多选）：

📄 **输出文档格式**
1. 业务流程分析报告（快速版）— 聚焦业务流程和异常场景
2. 功能架构设计（快速版）— 聚焦功能模块和数据模型
3. 埋点清单（快速版）— 页面埋点+核心事件清单+漏斗定义（3页内）
4. 完整 PRD 文档（快速版）— 13 章节完整需求文档
5. Draw.io 图表文件 — 将流程图和架构图导出为可编辑的 .drawio 文件（可用 Draw.io 或 diagrams.net 打开）
6. 开发任务拆解清单 — 按 Epic → Story → Task 三层拆解，含 BDD 验收标准，可直接导入 Jira / Linear

推荐组合：快速交付选 1+2，正式立项选 4，技术实施选 1+2+3，给开发团队选 4+6，全套选全部；需要可视化编辑图表时加选 5。

请回复「确认 + 文档编号」（如：确认，选 1+2 或 1+2+5），或告知需要修改的内容。
```

> **设计说明**：连续模式的核心诉求是"快速出结果"，将内容确认与格式选择合并为一次回复，避免原有的三轮交互（摘要确认→格式选择→交付确认）。

### 分步确认模式下的最终交付

分步确认模式下，Step 3 已完成确认。进入最终交付时，直接询问输出文档格式：

> "📄 **选择输出文档格式**
>
> 1. **业务流程分析报告**（快速版）— 聚焦业务流程和异常场景
> 2. **功能架构设计**（快速版）— 聚焦功能模块和数据模型
> 3. **埋点清单**（快速版）— 页面埋点+核心事件清单+漏斗定义（3页内）
> 4. **完整 PRD 文档**（快速版）— 13 章节完整需求文档
> 5. **Draw.io 图表文件** — 将流程图和架构图导出为可编辑的 .drawio 文件（可用 Draw.io 或 diagrams.net 打开）
> 6. **开发任务拆解清单** — 按 Epic → Story → Task 三层拆解，含 BDD 验收标准，可直接导入 Jira / Linear
>
> 推荐组合：快速交付选 1+2，正式立项选 4，技术实施选 1+2+3，给开发团队选 4+6，全套选全部；需要可视化编辑图表时加选 5。"

### 生成文档

| 选项 | 模板 | 输出文件名（含日期） |
|:---|:---|:---|
| 1. 业务流程分析报告 | `assets/business-flow.tpl.md` | `[名称]-业务流程分析-快速版-YYYYMMDD.md` |
| 2. 功能架构设计 | `assets/feature-architecture.tpl.md` | `[名称]-功能架构设计-快速版-YYYYMMDD.md` |
| 3. 埋点清单 | `assets/tracking-plan-lite.tpl.md` | `[名称]-埋点清单-快速版-YYYYMMDD.md` |
| 4. 完整 PRD 文档 | `assets/prd.tpl.md` | `[名称]-PRD-快速版-YYYYMMDD.md` |
| 5. Draw.io 图表文件 | 参见「Draw.io 图表输出」章节 | `[名称]-[图表类型]-YYYYMMDD.drawio` |
| 6. 开发任务拆解清单 | `assets/tickets.tpl.md` | `[名称]-Tickets-快速版-YYYYMMDD.md` |

文件保存至 Phase 3 创建的专属目录（路径从 `/tmp/pa_output_dir.txt` 读取）：
```bash
OUTPUT_DIR=$(cat /tmp/pa_output_dir.txt)
# 示例：cp [名称]-PRD-快速版-YYYYMMDD.md "$OUTPUT_DIR/"
```

**最终质量检查**：
```bash
SKILL_BASE=$(cat /tmp/pa_skill_base.txt 2>/dev/null || echo "")
OUTPUT_DIR=$(cat /tmp/pa_output_dir.txt)
if [ -n "$SKILL_BASE" ]; then
  python3 "$SKILL_BASE/scripts/run_quality_check.py" "$OUTPUT_DIR/<文件名>.md" --type flow
else
  echo "SKIP: 脚本目录未找到，人工检查文档结构完整性"
fi

### 交付确认（MUST）

读取 `guides/delivery-confirmation-dynamic.md` 的动态拼装指引，生成交付确认话术，展示并等待用户明确回复。

**最终质量保证**：
- [ ] 所有选定文档已生成
- [ ] Mermaid 图表语法正确
- [ ] 已执行最终质量检查
- [ ] 文件命名包含日期后缀，已保存至输出目录
- [ ] 已展示文档清单和内容摘要
- [ ] 等待用户明确回复


---

## Draw.io 图表输出（可选附加步骤）

**触发时机**：用户在最终交付的格式选择中选择了第 5 项（Draw.io 图表文件）。

**用户选择第 5 项时执行**：

📚 **读取**：`references/drawio-standards.md`

1. 识别本次已生成的 Mermaid 图（Step 2 高层级流程图 + Step 3 功能架构图）
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
