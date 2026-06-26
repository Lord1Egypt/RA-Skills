---
name: word-toolkit
description: "Word文档处理工具套件，提供Word文档的创建、读取、内容提取和基本处理功能。"
homepage: https://github.com/wanghao20150901/openclawkit-word.git
metadata: { "openclaw": { "emoji": "📝", "requires": { "bins": [], "python": ["python-docx"] } } }
---

# Word工具套件 (Word Toolkit)

## 功能概述

这是一个功能完整的Word文档处理工具套件，提供Word文档的创建、读取、内容提取和基本处理功能。

### 核心功能
- 📝 **文档创建**：创建新的Word文档，支持标题、段落、表格
- 📖 **文档读取**：读取现有Word文档，提取文本和结构信息
- 🔍 **内容提取**：提取纯文本、段落、表格内容
- 🛠️ **格式处理**：基本文档格式处理
- 📊 **批量处理**：支持批量文档操作

## 使用时机

✅ **使用此工具当：**
- 需要自动化生成Word文档
- 需要从Word文档中提取文本内容
- 需要批量处理多个Word文档
- 需要将数据导出为Word格式
- 需要进行文档格式转换

## 环境要求

- Python 3.6+
- 依赖包：
  - `python-docx` (Word文档处理)

安装依赖：
```bash
pip install python-docx
```

## 使用方法

### 命令行使用
```bash
# 查看帮助
python scripts/main.py --help

# 创建Word文档
python scripts/main.py create --file report.docx --title "项目报告"

# 读取Word文档
python scripts/main.py read --file document.docx

# 提取文本内容
python scripts/main.py extract --file document.docx --output text.txt

# 批量处理
python scripts/main.py batch --input "*.docx" --output extracted/
```

### Python API使用
```python
from openclawkit_word import WordToolkit

# 初始化工具
word = WordToolkit(debug=True)

# 创建Word文档
content = {
    'title': '项目报告',
    'paragraphs': [
        '这是项目概述。',
        '这是详细说明。',
        '这是总结部分。'
    ],
    'tables': [{
        'headers': ['任务', '负责人', '进度'],
        'rows': [
            ['需求分析', '张三', '100%'],
            ['开发实现', '李四', '80%'],
            ['测试验收', '王五', '60%']
        ]
    }]
}

word.create_document('项目报告.docx', content)

# 读取Word文档
doc_content = word.read_document('项目报告.docx')
if doc_content:
    print(f"段落数: {len(doc_content['paragraphs'])}")
    print(f"表格数: {len(doc_content['tables'])}")

# 提取文本
text = word.extract_text('项目报告.docx')
print(f"提取的文本: {text[:500]}...")
```

## 功能模块

### 1. 文档创建模块
- 创建新文档
- 添加标题和段落
- 插入表格
- 设置基本格式

### 2. 文档读取模块
- 读取现有文档
- 提取文档结构
- 获取元数据
- 验证文档完整性

### 3. 内容提取模块
- 提取纯文本
- 分离段落和表格
- 保留基本格式
- 处理特殊字符

### 4. 格式处理模块
- 字体和段落格式
- 表格样式设置
- 页面布局调整
- 样式模板应用

### 5. 批量处理模块
- 多文档并行处理
- 进度跟踪
- 结果汇总
- 错误处理

## 示例代码

### 基础示例
```python
from openclawkit_word import WordToolkit

# 创建工具实例
word = WordToolkit()

# 检查依赖
if word.check_docx_installed():
    # 创建简单文档
    simple_content = {
        'title': '会议纪要',
        'paragraphs': [
            '会议时间：2026年3月28日',
            '参会人员：张三、李四、王五',
            '会议内容：讨论项目进展和下一步计划'
        ]
    }
    
    if word.create_document('会议纪要.docx', simple_content):
        print("✅ 文档创建成功")
        
        # 读取文档
        content = word.read_document('会议纪要.docx')
        if content:
            for i, paragraph in enumerate(content['paragraphs'], 1):
                print(f"段落{i}: {paragraph}")
```

### 高级示例
```python
from openclawkit_word import WordToolkit
import json

word = WordToolkit(debug=True)

# 从JSON数据生成报告
def generate_report_from_json(json_file, output_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    report_content = {
        'title': f"{data['project_name']} - 项目报告",
        'paragraphs': [
            f"项目名称: {data['project_name']}",
            f"项目负责人: {data['project_manager']}",
            f"开始日期: {data['start_date']}",
            f"结束日期: {data['end_date']}",
            f"项目状态: {data['status']}",
            "",
            "项目里程碑:"
        ],
        'tables': []
    }
    
    # 添加里程碑表格
    if 'milestones' in data:
        milestones_table = {
            'headers': ['里程碑', '计划完成', '实际完成', '状态'],
            'rows': []
        }
        
        for milestone in data['milestones']:
            milestones_table['rows'].append([
                milestone['name'],
                milestone['planned_date'],
                milestone.get('actual_date', '未完成'),
                milestone['status']
            ])
        
        report_content['tables'].append(milestones_table)
    
    # 添加任务表格
    if 'tasks' in data:
        tasks_table = {
            'headers': ['任务', '负责人', '优先级', '进度'],
            'rows': []
        }
        
        for task in data['tasks']:
            tasks_table['rows'].append([
                task['description'],
                task['assignee'],
                task['priority'],
                f"{task['progress']}%"
            ])
        
        report_content['tables'].append(tasks_table)
    
    # 生成Word文档
    if word.create_document(output_file, report_content):
        print(f"✅ 报告生成成功: {output_file}")
        return True
    else:
        print(f"❌ 报告生成失败")
        return False

# 使用示例
generate_report_from_json('project_data.json', '项目报告.docx')
```

## 错误处理

工具包含完善的错误处理机制：
- 文件损坏或加密处理
- 格式不支持处理
- 内存不足处理
- 权限错误处理

## 性能优化

- **流式处理**：支持大文档分批处理
- **内存优化**：减少内存占用
- **并行处理**：多文档并行操作
- **缓存机制**：减少重复读取

## 更新日志

### v1.0.1 (2026-03-28)
- 初始版本发布
- 基础文档创建功能
- 文档读取和内容提取
- 表格处理功能
- 批量处理支持

## 许可证

MIT License

## 作者

浩哥 (Hao Ge)

## 反馈与贡献

欢迎提交Issue和Pull Request：
- GitHub: https://github.com/wanghao20150901/openclawkit-word.git
- Email: 512975801@qq.com