---
name: material-review
description: Use when user wants to review material forms for data sharing catalogs, field completeness, platform consistency, and issue-list output. Triggers include「材料审核」「共享清单审核」「检查文档审查」「平台对接核对」「编目一致性检查」.
metadata: {"openclaw":{"emoji":"📋","requires":{"anyBins":["markdownlint-cli2"]}}}
---

# Material Review

材料审核助手，面向《数据共享清单（试运行环节）》和平台编目核验，提供 6 步审核流程。

## 核心原则

| 原则 | 说明 |
|------|------|
| **先核对再结论** | 先逐项核对字段和平台信息，再给出通过/退回建议 |
| **问题必须可追溯** | 每条问题都要写清：位置、现状、规则依据、修正建议 |
| **先文档后平台** | 先做表单完整性检查，再做系统对接与编目一致性核验 |

## 6 步审核流程

```text
1. 范围确认 → 2. 字段完整性 → 3. 特殊字段规则 → 4. 数据表筛选 → 5. 平台一致性核验 → 6. 问题清单输出
```

### 步骤 1: 范围确认

**目标**：确认本次审核对象与边界，避免漏审。

- 核对材料版本是否为《数据共享清单（试运行环节）》模板
- 记录系统名称、单位及科室、联系人、数据库对接方式
- 确认审核范围：仅审核业务相关、拟共享的数据表

详见 [platform-consistency.md](references/platform-consistency.md)

### 步骤 2: 字段完整性

**目标**：先卡住必填项，避免进入后续环节才发现基础信息缺失。

- 除备注外均按必填处理
- 重点检查易漏字段：系统上线时间、数据资源摘要、目前数据量、数据项中文描述
- 检查易错填写：数据增量写成数字、上线时间写成 `/` 等无效值

详见 [field-completeness.md](references/field-completeness.md)

### 步骤 3: 特殊字段规则

**目标**：处理高频退回项，保证可审核、可落地。

- **数据增量**：当目前数据量超过 10000 且持续新增时必填；若明确全量更新可不填
- **数据项中文描述**：每个字段必须有中文描述，不能为空，且不能与英文名完全一致
- **共享类型**：一般不可直接写「不予共享」；若确需不共享，必须给出法律或制度依据

详见 [special-field-rules.md](references/special-field-rules.md)

### 步骤 4: 数据表筛选

**目标**：只保留应共享的业务表，减少无效编目和后续维护成本。

- 剔除业务无关表（如配置表、日志表等）
- 对目前数据量为 0 的表单独标注，要求确认是否仍需保留
- 逐表核对：中文表名、英文表名、摘要、更新频率、字段定义是否完整

详见 [field-completeness.md](references/field-completeness.md)

### 步骤 5: 平台一致性核验

**目标**：校验材料与平台现状是否一致，明确对接状态和差异。

- 在平台前台/后台检索系统，确认是否已对接
- 若未对接，明确标注「未对接」
- 若已对接，核对四类差异：系统名称、数据表数量、表名映射、未编目表
- 检查平台表更新情况：超过半年未更新需标注
- 检查平台字段中文名：中文名为「默认信息」或直接英文时需标注
- `TIMEFLAG` 为系统统一字段，中文名为默认信息时可忽略

详见 [platform-consistency.md](references/platform-consistency.md)

### 步骤 6: 问题清单输出

**目标**：输出可直接回传给填报单位的整改清单。

- 按「必填缺失 / 规则不符 / 平台不一致 / 待确认」分类
- 每条问题都给出修正动作，不只指出错误
- 一次只处理一个系统，完成后再进入下一个系统

详见 [issue-template.md](references/issue-template.md)

## 审核节奏

```text
1) 先过“字段完整性+特殊规则”
2) 再做“平台检索+一致性比对”
3) 输出问题清单并等待用户确认
4) 用户确认后再继续下一个系统
```

## 脚本调用

该 Skill 内置自动审核脚本：`scripts/material_review_audit.py`  
用途：把填报文档抽取为结构化数据，并按《文档审查》规则输出问题清单。

执行命令：

```bash
python material-review/scripts/material_review_audit.py \
  --submission "待审核材料.docx" \
  --template "material-review/2附件1-5：数据共享清单（试运行环节）.docx" \
  --rules "material-review/文档审查.docx" \
  --output-dir "material-review/output"
```

输出文件：

- `material-review/output/structured_data.json`：结构化填报数据
- `material-review/output/issues.json`：审核问题列表
- `material-review/output/audit_report.md`：可直接回传的问题清单报告

## 输出格式速查

| 要素 | 要求 |
|------|------|
| 问题定位 | 明确到字段名/数据表名/系统名称 |
| 规则依据 | 对应模板要求或审核规则 |
| 风险描述 | 不改会导致什么后果（如审核不通过、无法编目） |
| 修正建议 | 可执行动作，避免笼统建议 |

## 详细参考

- [field-completeness.md](references/field-completeness.md) - 必填项与常见漏填
- [special-field-rules.md](references/special-field-rules.md) - 特殊字段判定规则
- [platform-consistency.md](references/platform-consistency.md) - 平台对接与一致性核验
- [issue-template.md](references/issue-template.md) - 问题清单模板
