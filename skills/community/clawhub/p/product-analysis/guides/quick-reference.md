# 产品分析 Skill v6.5 — 快速参考指南

本指南为熟悉本 skill 的用户提供一页纸速查表。

---

## 1. 复杂度评估（三档）

| 维度 | 低 (分) | 中 (分) | 高 (分) |
|:---|:---|:---|:---|
| 功能点 | 1–3 (3) | 4–8 (7) | 9+ (10) |
| 用户角色 | 1 (2) | 2–3 (5) | 4+ (10) |
| 系统集成 | 0 (0) | 1–2 (3) | 3+ (7) |
| 业务规则 | 简单 (3) | 中等 (7) | 复杂 (10) |
| 数据复杂度 | 简单 (3) | 中等 (7) | 复杂 (10) |

- **11–20 分** → 快速模式（3 步）
- **21–35 分** → 标准模式（步骤 5 可选）
- **36–47 分** → 完整标准模式（步骤 5 必选）

---

## 2. 工作流速查

### 快速模式（3 步）

| 步骤 | 核心任务 | 关键产出 | 自动化检查 |
|:---|:---|:---|:---|
| **1. 理解需求** | 应用 1–2 个分析框架，列出核心功能 | 需求摘要、功能清单 | — |
| **2. 设计流程** | 绘制高层级流程图，识别 2–3 个核心异常 | 流程图 (Mermaid)、异常清单 | `validate_mermaid.py` |
| **3. 构建架构** | 划分功能模块（MECE），进行优先级分类 | 架构图 (Mermaid)、功能清单 | `validate_mermaid.py` + `check_mece.py` |

### 标准模式（5 步 + Step 1.5）

| 步骤 | 核心任务 | 关键产出 | 自动化检查 |
|:---|:---|:---|:---|
| **1. 深入理解** | 应用 2–3 个分析框架，定义完整用户角色 | 完整需求文档、用户角色矩阵 | — |
| **1.5 外部调研** | 竞品/行业分析（36+分按需，21–35分按需）；结论指导 Step 2–4 | 调研报告、竞品对比表、设计方向影响说明 | — |
| **2. 设计流程** | 绘制高层级和详细流程图，创建 RACI/DFD | 两级流程图、RACI 矩阵、DFD | `validate_mermaid.py` |
| **3. 异常识别** | 全面检查异常，设计处理策略 | 完整异常清单、更新后的流程图 | — |
| **4. 设计架构** | 功能分层，综合 Step 1.5 结论，输出详细规格和迭代规划 | 详细架构图、功能规格说明 | `validate_mermaid.py` + `check_mece.py` |
| **5. 补充调研** | (按需) 验证特定设计决策；若 Step 1.5 已完整调研可跳过 | 专项调研报告 | — |

---

## 3. 关键命令

**Phase 3 初始化（每次会话执行一次）**：
```bash
# 创建输出目录并持久化
OUTPUT_DIR="/mnt/user-data/outputs/[名称]-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$OUTPUT_DIR" && echo "$OUTPUT_DIR" > /tmp/pa_output_dir.txt

# 定位脚本目录并持久化
SKILL_BASE=""
for _p in "/mnt/skills/public/product-analysis6.5" "/mnt/skills/public/product-analysis" \
           "/mnt/skills/user/product-analysis6.5" "/mnt/skills/user/product-analysis"; do
  [ -f "$_p/scripts/validate_mermaid.py" ] && SKILL_BASE="$_p" && break
done
[ -n "$SKILL_BASE" ] && echo "$SKILL_BASE" > /tmp/pa_skill_base.txt || echo "WARN: 脚本目录未找到"
```

**后续步骤读取变量（每个新 bash_tool 调用开头）**：
```bash
OUTPUT_DIR=$(cat /tmp/pa_output_dir.txt)
SKILL_BASE=$(cat /tmp/pa_skill_base.txt 2>/dev/null || echo "")
```

| 操作 | 命令（已读取 SKILL_BASE 后使用）|
|:---|:---|
| **验证 Mermaid 图** | `python3 "$SKILL_BASE/scripts/validate_mermaid.py" <文件路径>` |
| **最终质量检查** | `python3 "$SKILL_BASE/scripts/run_quality_check.py" <文件路径> --type flow\|arch\|prd\|tracking` |
| **MECE 原则检查** | `python3 "$SKILL_BASE/scripts/check_mece.py" <文件路径>` |

---

## 4. 分步确认要点

每步完成后必须：
1. 用实际产出内容填充 `guides/confirmation-templates.md` 对应模板
2. 展示产出，询问用户确认
3. **等待**用户明确回复，不能自动继续

用户要求跳过确认时 → 切换「连续执行模式」，完成所有步骤后一次性交付。

---

## 5. 输出文档

| 选项 | 模板 | 适合场景 |
|:---|:---|:---|
| 1. 业务流程分析报告 | `assets/business-flow.tpl.md` | 内部讨论、快速交付 |
| 2. 功能架构设计 | `assets/feature-architecture.tpl.md` | 技术团队实施 |
| 3a. 埋点清单（快速版）| `assets/tracking-plan-lite.tpl.md` | 数据团队（快速交付） |
| 3b. 埋点方案设计（标准版）| `assets/tracking-plan-template.md` | 数据团队（完整方案） |
| 4. 完整 PRD 文档 | `assets/prd.tpl.md` | 正式立项、对外展示 |

---

## 6. v6.5 关键变更速查

| 变更项 | v6.4 行为 | v6.5 新增行为 |
|:---|:---|:---|
| 步骤编号 | 主流程 Step 0–6，子流程也用 Step 1–N（冲突） | 主流程用 Phase，子流程用 Step（独立命名空间） |
| 外部调研时机 | 标准模式最后（Step 5，架构之后） | 标准模式前置（Step 1.5，需求理解之后） |
| 质量保证 | SKILL.md 独立 Phase + 子工作流每步各自检查（重复） | 仅子工作流每步内嵌 + 最终交付前全文档检查 |
| 快速模式默认 | 每步强制确认 | 默认连续执行，Phase 2 时提前确认偏好 |
| 交付确认模板 | 8 种固定场景枚举 | 动态拼装（文档块+标准特点块+通用收尾） |
| 输出文件名 | `[名称]-类型-模式版.md` | `[名称]-类型-模式版-YYYYMMDD.md`（含日期） |
| 快速模式 Step 3 | 功能架构划分（无异常回流要求） | 功能架构划分 + Step 2 异常兜底功能纳入 |
| 迭代/改版支持 | 无，所有场景走新建流程 | 新增迭代模式（3步，Diff分析+影响面+变更规格） |
| 优先级框架 | P0/P1/P2/P3 标签 | RICE 评分（Reach×Impact×Confidence÷Effort）量化 |
| 需求分析框架 | 用户故事、KANO、MECE、STAR | 新增 JTBD（动机挖掘）框架 |
| 验收标准格式 | 自由文本 checklist | BDD 三段式（Given / When / Then） |
| 数据实体设计 | ERD 简图 | 完整实体定义（字段+约束+枚举+关系说明） |
| 开发交付 | PRD 为终点 | 新增 Ticket 拆解（Epic→Story→Task，可导入 Jira/Linear） |
| 输出文档选项 | 5 项 | 6 项（新增第6项：开发任务拆解清单） |

---

## 6b. v6.6 修复速查

| 修复项 | v6.5 问题 | v6.6 修复方式 |
|:---|:---|:---|
| 脚本路径解析 | `$0` 在 bash_tool 中解析为 `/bin/sh`，脚本路径错误，质量检查静默失败 | Phase 3 遍历候选路径探测，写入 `/tmp/pa_skill_base.txt` |
| OUTPUT_DIR 跨调用丢失 | bash 子进程间变量不共享，输出目录机制失效 | Phase 3 写入 `/tmp/pa_output_dir.txt`，后续步骤从文件读取 |
| 标准模式 Step 5 空壳 | 仅有触发条件，无任务/产物/确认模板定义 | 补充完整四段式规格 + confirmation-templates.md 对应模板 |
| 迭代模式无示例 | examples/ 目录无迭代模式参考文件 | 新增 `examples/iteration-analysis.md`（含 Diff 图/JTBD/BDD） |
| 输出文档选项编号重复 | 快速参考中选项 3 出现两次 | 拆分为 3a（快速版）和 3b（标准版） |
| description 字段冗长 | 8 行触发词/框架枚举，稀释触发精度 | 压缩至 3 行核心触发条件 |
| Draw.io 兜底方案缺失 | 仅说「直接写入文件」，无具体代码 | 三个工作流均补充兜底 bash 代码示例 |
| files/ 目录无说明 | 空目录，用途不明 | 新增 `files/README.md` 说明用途 |

---

## 7. 输出文档（v6.5 完整版）

| 选项 | 模板 | 适合场景 |
|:---|:---|:---|
| 1. 业务流程分析报告 | `assets/business-flow.tpl.md` | 内部讨论、快速交付 |
| 2. 功能架构设计 | `assets/feature-architecture.tpl.md` | 技术团队实施 |
| 3a. 埋点清单（快速版）| `assets/tracking-plan-lite.tpl.md` | 数据团队（快速交付） |
| 3b. 埋点方案设计（标准版）| `assets/tracking-plan-template.md` | 数据团队（完整方案） |
| 4. 完整 PRD 文档 | `assets/prd.tpl.md` | 正式立项、对外展示 |
| 5. Draw.io 图表文件 | 参见各工作流 Draw.io 章节 | 可视化编辑、分享 |
| 6. 开发任务拆解清单 | `assets/tickets.tpl.md` | 研发团队、导入 Jira/Linear |
