---
name: insurance-parser
description: 解析医疗险条款文档并提取32个结构化字段，含14个核心字段和18个增强字段，支持PDF/DOCX/TXT格式，输出标准JSON
dependency:
  python:
    - pypdf2==3.0.1
    - python-docx==1.1.0
---

# 医疗险条款结构化解析器

## 任务目标
- 本 Skill 用于：从医疗险条款文档中提取32个结构化字段
- 能力包含：解析PDF/DOCX/TXT格式文档，提取Level 1核心字段（14个）和Level 2增强字段（18个）
- 触发条件：用户提供医疗险条款文档或文本内容，需要结构化提取时

## 前置准备
- 依赖说明：无特殊依赖，已内置文档解析脚本

## 操作步骤
- 标准流程:
  1. **获取文档内容**
     - 如果用户提供的是PDF/DOCX/TXT文件，调用 `scripts/parse_document.py <file_path>` 获取纯文本内容
     - 如果用户直接输入保险条款文本，直接使用该文本
  2. **提取结构化信息**
     - 根据 [references/output-format.md](references/output-format.md) 中的字段定义，从文档内容中提取对应信息
     - 智能体将逐项分析文档，填充以下两部分：
       - `level1_core_fields`: 14个绝对核心字段（年度限额、免赔额、赔付比例、续保条件等）
       - `level2_enhancement_fields`: 18个对比增强字段（家庭共享免赔额、特殊门诊、院外购药、CAR-T等）
     - 数据类型转换规则：
       - DECIMAL类型：金额转换为元（如"100万" → 1000000.00），比例转换为小数（如"100%" → 1.0000）
       - ENUM类型：严格使用枚举值（如免赔额单位："年"/"次"/"疾病"/"住院"）
       - BOOLEAN类型：根据表述判断（"保障"/"是" → true，"不保障"/"否" → false）
       - INT类型：直接提取数字（如"30天" → 30）
  3. **输出结果**
     - 以JSON格式输出完整的结构化数据
     - Level 1字段必须填充，Level 2字段未明确说明可使用null
     - 确保所有字段类型和枚举值符合格式规范

## 资源索引
- 必要脚本:见 [scripts/parse_document.py](scripts/parse_document.py)(用途与参数:解析PDF/DOCX/TXT文件，返回纯文本)
- 领域参考:见 [references/output-format.md](references/output-format.md)(何时读取:始终读取，用于了解字段定义和提取规则)

## 注意事项
- 优先使用文档解析脚本处理文件，避免格式错误
- 提取时保持原文含义，必要时可进行总结归纳
- Level 1核心字段必须优先保证准确性，AI可100%提取无null风险
- Level 2增强字段允许null，体现产品差异化
- 严格按照数据类型转换规则处理数值、比例、枚举值
- 确保JSON格式正确，避免语法错误

## 使用示例
- 场景1：上传PDF医疗险合同
  - 调用脚本：`python scripts/parse_document.py ./insurance_contract.pdf`
  - 提取32个字段并输出结构化JSON
  - 核心字段示例：年度限额200万元、免赔额1万元/年、社保报销后100%赔付
  - 增强字段示例：院外购药保障、CAR-T治疗、家庭共享免赔额
- 场景2：直接输入医疗险条款文本
  - 直接分析文本内容
  - 按格式规范输出32个字段的结构化JSON
  - 未明确说明的Level 2字段使用null表示
