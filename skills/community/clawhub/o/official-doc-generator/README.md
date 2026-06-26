# official-document-generator 技能

## 技能概述
专门用于自动生成体制内讨论材料并按照公文格式自动排版的技能。支持会议纪要、发言稿、讨论提纲、工作汇报等多种文档类型，遵循GB/T 9704-2012标准、党政机关公文格式和企业公文规范。

## 技能特点

### 1. 核心能力
- **多种文档类型**：会议纪要、发言稿、讨论提纲、工作汇报等
- **标准格式遵循**：GB/T 9704-2012、党政机关公文格式、企业公文规范
- **智能内容生成**：基于体制内语言风格和组织文化
- **格式自动化**：多级标题自动编号、段落格式标准化
- **合规性检查**：敏感词检查、格式验证、内容审核

### 2. 技术实现
- **模板系统**：基于Jinja2的模板引擎，支持自定义模板
- **格式引擎**：使用python-docx进行精确格式控制
- **合规检查**：内置敏感词库和格式验证规则
- **脚本工具**：完整的命令行工具集

## 文件结构

```
official-document-generator/
├── SKILL.md                    # 技能主文档
├── README.md                   # 本文件
├── scripts/
│   ├── generate_document.py    # 文档生成主脚本
│   ├── format_validator.py     # 格式验证脚本
│   ├── sensitive_words_check.py # 敏感词检查脚本
│   ├── template_manager.py     # 模板管理脚本
│   └── test_generator.py       # 测试脚本
├── references/
│   ├── gb_t_9704_2012_standard.md      # GB/T 9704-2012标准
│   ├── official_language_style.md      # 体制内语言风格
│   ├── document_types_specification.md # 文档类型规范
│   └── sensitive_words_list.md         # 敏感词库
└── assets/
    ├── templates/              # 模板文件目录
    └── examples/               # 示例文档目录
```

## 快速开始

### 1. 生成会议纪要
```bash
python scripts/generate_document.py --type meeting_minutes --example --output meeting.docx
```

### 2. 验证文档格式
```bash
python scripts/format_validator.py --file document.docx --standard gb_t_9704_2012
```

### 3. 检查敏感词
```bash
python scripts/sensitive_words_check.py --text "需要检查的文本内容"
```

### 4. 管理模板
```bash
python scripts/template_manager.py list
python scripts/template_manager.py init  # 初始化默认模板
```

## 使用示例

### 生成会议纪要
```python
from scripts.generate_document import OfficialDocumentGenerator, create_example_config

generator = OfficialDocumentGenerator()
config = create_example_config("meeting_minutes")
generator.create_document("meeting_minutes", config)
generator.save_document("meeting_minutes.docx")
```

### 验证格式
```python
from scripts.format_validator import DocumentFormatValidator

validator = DocumentFormatValidator()
result = validator.validate_document("document.docx", "gb_t_9704_2012")
print(f"验证结果: {'通过' if result['valid'] else '未通过'}")
```

### 检查敏感词
```python
from scripts.sensitive_words_check import SensitiveWordsChecker

checker = SensitiveWordsChecker()
result = checker.check_text("需要检查的文本内容", "strict")
print(f"敏感词数量: {result['sensitive_count']}")
```

## 依赖要求
- Python 3.7+
- python-docx（用于Word文档处理）
- 可选：Jinja2（用于模板渲染）

## 测试
运行测试脚本验证所有功能：
```bash
python scripts/test_generator.py
```

## 技能触发场景
- 当用户需要生成体制内正式文档时
- 当需要按照标准公文格式自动排版时
- 当需要确保文档符合体制内语言风格和组织文化时
- 当需要进行敏感词和合规性检查时

## 更新记录

### v1.0.0 (2026-03-28)
- 初始版本发布
- 支持4种主要文档类型
- 集成GB/T 9704-2012标准格式
- 提供敏感词检查和格式验证功能
- 完整的脚本工具集