# AGENTS.md - 职业分析项目指南

> 本文件帮助 Agent 快速理解项目，避免常见错误。

## 项目概述

职业教育专业建设辅助工具，生成职业分析报告（工作过程系统化方法，七部分结构）。

支持教育层次：中职、高职、职教本科。

## 核心命令

```bash
# 专业检索及职业对照查询（步骤1）
# --include-occupations 参数会同时输出对照表中的职业编码
python scripts/search_major.py --major "专业名称" --level "层次" --include-occupations --output temp/major_info.json

# 本地文档查询（步骤5）
python scripts/fetch_local.py --mapping temp/occupation_mapping_info.json --output temp/international_data.json

# 报告生成（步骤15）
python scripts/generate_report.py --data temp/analysis_data.json --output temp/report.md

# Word转换
pandoc temp/report.md --reference-doc=references/reference.docx -o output/report.docx

# 报告验证
python scripts/validate_report.py --report temp/report.md --data temp/analysis_data.json
```

## 数据文件位置

| 数据源 | 路径 | 说明 |
|--------|------|------|
| 专业教学标准 | `assets/moe_pdfs_final.json` | 172KB JSON索引 |
| 专业-职业对照表 | `assets/专业-职业对照表.xlsx` | 专业对应职业编码和名称（1169条） |
| 职业大典 | `assets/occupation_dictionary_split/class_*.md` | 按大类拆分（7个文件） |
| ESCO文档 | `assets/esco_details_md/*.md` | ~3000+文件 |
| O*NET文档 | `assets/onet_details_md/*.md` | 894文件 |

## 关键约束（NEVER Do）

### Token 优化

- **NEVER** 一次性加载完整职业大典（~136K tokens，会耗尽上下文）
  - 正确做法：用 `OccupationDictionaryLoader` 按职业代码首位加载对应大类
  - 示例：`loader.load_by_occupation_code('6-22-02')` 只加载第6大类

- **NEVER** 在同一会话重复加载同一大类文件（`OccupationDictionaryLoader` 已缓存）

### 流程约束

- **NEVER** 跳过步骤0预检验证（数据缺失会导致后续全部失败）
  
- **NEVER** 跳过步骤3用户确认环节
  - 必须用 `question` 工具展示确认面板
  - **等待用户回复**后才能继续步骤4
  - 即使"全流程测试"也必须等待确认

- **NEVER** 接受非职业大典中的职业（无法获取标准定义）

### 教育层次适配

| 层次 | 能力动词（允许） | 禁止动词 |
|------|-----------------|----------|
| 中职 | 操作、执行、完成、使用、识别、检测 | 设计、优化、创新、管理、分析 |
| 高职 | 检测、诊断、分析、维护、维修、优化 | 研发、创新、管理 |
| 职教本科 | 设计、优化、管理、创新 | - |

## 架构

**分层架构**：

```
Python脚本层（数据获取）     →  JSON数据  →  大模型层（语义分析）
├─ search_major.py          → major_info.json
├─ fetch_local.py           → international_data.json
├─ generate_report.py       → report.md
└─ occupation_dict_loader   → 职业大典按需加载
```

**职责划分**：
- Python脚本：精确匹配、文件读写、格式转换（不调用大模型）
- 大模型：语义理解、职业映射推断、分析生成（不单独调用API）

## 参考文档加载时机

| 文件 | 加载时机 |
|------|----------|
| `references/work_process_method.md` | 步骤10/12/13 **必须** 加载对应章节 |
| `references/analysis_data_template.json` | 步骤14 **必须** 参考 |
| `references/report_template.md` | 步骤15 **必须** 加载 |
| `references/troubleshooting.md` | 遇到问题时 **按需** 加载 |
| `references/precheck_guide.md` | 步骤0 **按需** 加载 |

## 常见问题速查

| 问题 | 解决方案 |
|------|----------|
| 找不到专业 | 用代码检索，检查官方名称 |
| 职业大典解析失败 | 用分块加载，检查职业代码格式（X-XX-XX-XX） |
| ESCO/O*NET文档缺失 | 检查英文名/O*NET代码，展示缺失列表让用户确认继续 |
| 表格编号跳跃 | 检查 analysis_data.json 数据完整性 |
| 表7/表8不一致 | 确保能力编号（Z/F/S前缀）一一对应 |

## 目录结构

```
occupation-analysis/
├── SKILL.md              # 技能定义（完整流程）
├── AGENTS.md             # Agent快速指南
├── scripts/              # Python脚本
├── references/           # 参考文档+模板
├── assets/               # 数据文件
│   ├── moe_pdfs_final.json       # 专业教学标准
│   ├── 专业-职业对照表.xlsx       # 专业对应职业对照表
│   ├── occupation_dictionary_split/  # 职业大典（7大类）
│   ├── esco_details_md/          # ESCO职业文档
│   └── onet_details_md/          # O*NET职业文档
├── temp/                 # 临时输出（运行时生成）
└── output/               # 最终报告（运行时生成）
```

## 能力编号规则

- **Z** = 专业能力（ZhuanYe），编号 Z001, Z002...
- **F** = 方法能力（FangFa），编号 F001, F002...
- **S** = 社会能力（SheHui），编号 S001, S002...

表7与表8能力编号必须完全一致。