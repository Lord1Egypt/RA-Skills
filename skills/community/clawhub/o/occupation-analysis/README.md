# 职业分析报告生成工具

> 职业教育专业建设辅助工具 - 按工作过程系统化方法自动生成职业分析报告

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📖 项目简介

本工具用于职业教育专业建设中的职业分析环节，按照**工作过程系统化课程开发方法**，自动生成规范的职业分析报告。支持三个教育层次：

- 🎓 **中等职业教育**（中职）
- 🎓 **高等职业教育**（高职/专科）
- 🎓 **职业教育本科**（职教本科）

### 核心功能

- ✅ 自动检索专业教学标准
- ✅ 专业-职业对照表智能匹配（1169条对照关系）
- ✅ 智能提取职业大典信息
- ✅ ESCO/O*NET 国际职业映射（大模型世界知识推断）
- ✅ 典型工作任务分析
- ✅ 行动领域划分
- ✅ 学习领域转换
- ✅ 学习情境设计
- ✅ 生成七部分结构报告（Markdown/Word）
- ✅ 报告质量自动验证（14项验证指标）

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Pandoc（用于 Word 文档转换）

### 安装依赖

```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 安装 Pandoc（Ubuntu/Debian）
sudo apt-get update && sudo apt-get install -y pandoc

# 安装 Pandoc（macOS）
brew install pandoc
```

### 基本使用示例

```bash
# 1. 检索专业教学标准（含职业对照）
python scripts/search_major.py --major "数字媒体技术应用" --level "中等职业教育" --include-occupations --output temp/major_info.json

# 2. 整合基础数据（合并JSON+MD文件，包含国际原始文档）
python scripts/integrate_data.py \
  --major temp/major_info.json \
  --occupation temp/occupation_dict_data.json \
  --mapping temp/occupation_mapping_info.json \
  --output temp/combined_data.md

# 3. 生成分析报告（需先完成大模型语义分析，生成analysis_data.json）
python scripts/generate_report.py --data temp/analysis_data.json --output temp/report.md

# 4. 转换为 Word 文档
pandoc temp/report.md --reference-doc=references/reference.docx -o output/report.docx

# 5. 验证报告质量
python scripts/validate_report.py --report temp/report.md --data temp/analysis_data.json
```

## 📁 项目结构

```
occupation-analysis/
├── SKILL.md                    # 技能定义（完整工作流程）
├── AGENTS.md                   # Agent 快速指南
├── README.md                   # 项目说明文档
├── requirements.txt            # Python 依赖
│
├── scripts/                    # 核心脚本
│   ├── search_major.py        # 专业教学标准检索（含职业对照）
│   ├── generate_report.py     # 报告生成
│   ├── validate_report.py     # 报告验证（14项指标）
│   ├── occupation_dict_loader.py  # 职业大典分块加载
│   ├── integrate_data.py      # 数据整合
│   ├── pdf_parser.py          # PDF 解析
│   └── ...
│
├── references/                 # 参考文档和模板
│   ├── work_process_method.md     # 工作过程系统化方法
│   ├── analysis_data_template.json # 分析数据模板
│   ├── report_template.md     # 报告模板
│   ├── reference.docx         # Word 参考样式
│   ├── troubleshooting.md     # 故障排除指南
│   └── precheck_guide.md      # 预检指南
│
├── assets/                     # 数据文件
│   ├── moe_pdfs_final.json    # 专业教学标准索引（172KB）
│   ├── moe_pdfs_md/           # 专业教学标准 MD 文件
│   ├── 专业-职业对照表.xlsx    # 专业对应职业对照表（1169条）
│   ├── occupation_dictionary_split/  # 中国职业大典（按7大类拆分）
│   ├── esco_details_md/       # ESCO 职业文档（~3,000个）
│   └── onet_details_md/       # O*NET 职业文档（894个）
│
├── temp/                       # 临时输出（运行时生成）
│   ├── major_info.json        # 专业检索结果
│   ├── occupation_mapping_info.json  # 职业映射信息
│   ├── combined_data.md       # 整合数据（~400KB，Markdown格式）
│   ├── analysis_data.json     # 语义分析结果
│   └── report.md              # Markdown 报告
│
└── output/                     # 最终报告（运行时生成）
    └── report.docx             # Word 文档输出
```

## 📊 数据源说明

| 数据源 | 文件位置 | 说明 |
|--------|----------|------|
| **专业教学标准** | `assets/moe_pdfs_final.json` | 教育部发布的官方标准（172KB） |
| **专业-职业对照表** | `assets/专业-职业对照表.xlsx` | 专业对应职业编码和名称（1169条） |
| **中国职业大典** | `assets/occupation_dictionary_split/` | 2022版，按7个大类拆分 |
| **ESCO** | `assets/esco_details_md/` | 欧洲技能/能力/资格框架（~3,000个文件） |
| **O*NET** | `assets/onet_details_md/` | 美国职业信息网络（894个文件） |

## 📝 报告结构（七部分）

生成的职业分析报告包含以下七个部分：

| 部分 | 内容 | 对应表格 |
|------|------|----------|
| 一 | 职业面向分析 | 表1：工作任务分析表 |
| 二 | 典型工作任务确定 | 表2-3：典型工作任务汇总表 |
| 三 | 典型工作任务描述 | 表4-5：任务详细描述表 |
| 四 | 行动领域划分 | 表6：行动领域表 |
| 五 | 职业能力分析 | 表7-8：能力一览表和解构表 |
| 六 | 学习领域转换 | 表9-10：学习领域表 |
| 七 | 学习情境设计 | 表11：学习情境表 |

## 🔧 核心脚本说明

### search_major.py - 专业教学标准检索

```bash
python scripts/search_major.py --major "专业名称或代码" --level "教育层次" --include-occupations --output temp/major_info.json

# 参数说明
--major              专业名称或6位代码（如 "710204"）
--level              教育层次（中等职业教育/高等职业教育/职业教育本科）
--include-occupations 同时输出对照表中的职业编码
--output             输出文件路径
--no-pdf             跳过PDF解析（仅返回基本信息）
```

### fetch_local.py - 本地文档查询（已移除）

> ⚠️ 本脚本已从工作流中移除。国际文档查询功能已整合到 `integrate_data.py` 中。

### integrate_data.py - 数据整合

```bash
python scripts/integrate_data.py \
  --major temp/major_info.json \
  --occupation temp/occupation_dict_data.json \
  --mapping temp/occupation_mapping_info.json \
  --output temp/combined_data.md

# 合并JSON文件（步驟1-3输出）和原始MD文档（按映射代码从assets/读取），输出combined_data.md
# Python脚本只做数据搬运，不做语义推断
```

### generate_report.py - 报告生成

```bash
python scripts/generate_report.py --data temp/analysis_data.json --output temp/report.md

# 将 analysis_data.json 转换为 Markdown 报告
```

### validate_report.py - 报告验证

```bash
python scripts/validate_report.py --report temp/report.md --data temp/analysis_data.json

# 验证项（14项）：
# - 必需字段完整性
# - job_tasks字段完整性
# - job_tasks数量一致性
# - 表1-job_tasks对应关系
# - typical_tasks引用有效性
# - 数据源分离正确性
# - 表格编号连续性（表1→表11）
# - 表格空白单元格检测
# - 典型任务覆盖性
# - 能力编号一致性（Z/F/S前缀）
# - 学习领域数量（≥10个）
# - 总学时合理性（中职≥1200，高职/本科≥1600）
# - 领域学时范围（48-128学时/域）
# - 学习情境数量验证（3-6个/域）
```

## 🎯 教育层次适配

不同教育层次对应不同的能力动词要求：

| 层次 | 允许动词 | 禁止动词 | 总学时要求 |
|------|----------|----------|-----------|
| **中职** | 操作、执行、完成、使用、识别、检测、制作、编制、应用、处理、采集、编辑、合成 | 设计、优化、创新、管理、分析、诊断、研发、开发 | ≥1600学时 |
| **高职** | 检测、诊断、分析、维护、维修、优化 | 研发、创新、管理 | ≥1600学时 |
| **职教本科** | 设计、优化、管理、创新 | - | ≥1600学时 |

## ⚙️ 工作流程

完整的工作流程包含6个阶段：

```
阶段一：数据获取（步骤1-5）
├─ 步骤1: 检索专业教学标准（含职业对照）
├─ 步骤2: 获取职业大典信息（分块加载）
├─ 步骤3: ESCO/O*NET映射推断（大模型世界知识）
├─ 步骤4: 用户确认职业信息（必须等待）
└─ 步骤5: 整合全部数据

阶段二：语义分析（步骤6-13）
├─ 步骤6-7: 工作任务分析
├─ 步骤8: 行动领域划分
├─ 步骤9: 职业能力分析
├─ 步骤10: 学习领域转换
├─ 步骤11: 学习情境设计
└─ 步骤12: 输出结构化数据

阶段三：报告生成（步骤13）
└─ 步骤13: 生成 Markdown 报告

阶段四：质量校验（步骤14-15）
├─ 步骤14: 质量校验（14项验证）
└─ 步骤15: Word 文档转换
```

### 关键约束

- **步骤4必须等待用户确认**：用 `question` 工具展示确认面板
- **步骤3使用大模型推断**：无需本地文档依赖，直接利用大模型世界知识
- **步骤5输出Markdown格式**：`combined_data.md`，合并JSON和原始MD文件输出（零提取、零转换）
- **步骤6-12由大模型完成**：语义分析（工作任务分析、典型任务提炼、行动领域划分等）
- **职业大典分块加载**：按职业代码首位加载对应大类，避免一次性加载全部
- **Python脚本职责边界**：只做数据搬运和格式转换，不做语义推断（由大模型完成）

## 🔑 能力编号规则

- **Z** = 专业能力（ZhuanYe），编号 Z001, Z002...
- **F** = 方法能力（FangFa），编号 F001, F002...
- **S** = 社会能力（SheHui），编号 S001, S002...

> ⚠️ 表7（能力一览表）与表8（能力解构表）的能力编号必须完全一致

## 📚 参考文档

| 文档 | 用途 | 加载时机 |
|------|------|----------|
| `references/work_process_method.md` | 工作过程系统化方法理论基础 | 步骤10/12/13 **必须** |
| `references/analysis_data_template.json` | 分析数据 JSON 格式模板 | 步骤14 **必须** |
| `references/report_template.md` | 报告 Markdown 模板 | 步骤15 **必须** |
| `references/troubleshooting.md` | 故障排除指南 | 遇到问题时 **按需** |
| `references/precheck_guide.md` | 预检指南 | 步骤0 **按需** |

## 📋 已完成案例

### 中职数字媒体技术应用专业（710204）

**分析结果统计**：
- 职业数量：4个（数字媒体艺术专业人员、视觉传达设计人员、虚拟现实产品设计师、全媒体运营师）
- 典型工作任务：10个
- 行动领域：12个
- 学习领域：12个
- 学习情境：36个
- 总学时：1272学时
- 职业能力：33个（Z001-Z015, F001-F009, S001-S009）
- 输出文档：`output/report.docx`（30KB）

**验证结果**：14项验证全部通过 ✅

**数据流特征**：
- 步骤5输出：`temp/combined_data.md`（~400KB，合并JSON+原始MD文档）
- 步骤6-12由大模型完成：生成`temp/analysis_data.json`含job_tasks/typical_tasks/action_domains等

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 📮 联系方式

如有问题或建议，请提交 [GitHub Issue](https://github.com/flyboat403/occupation-analysis/issues)

---

**⭐ 如果这个项目对您有帮助，请给一个 Star！**