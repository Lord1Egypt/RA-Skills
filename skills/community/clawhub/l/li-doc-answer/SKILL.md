# Li_doc_answer - 通用文档 AI 答案生成

**版本:** 3.0.4  
**描述:** 通用 Word 文档处理工具，AI 自动识别题目并生成参考答案，支持 doc/docx 格式批量处理  
**作者:** 北京老李

## 功能特性

### v3.0 AI 核心功能
- 🤖 **AI 智能答案生成** - 自动识别文档中的题目并生成参考答案
- 🎯 **8 种题型支持** - 判断/单选/多选/简答/论述/案例/填空/名词解释
- 📝 **自动格式排版** - 统一的答案格式和美观排版
- 🔍 **智能题目识别** - 自动检测文档中的问题

### 基础功能
- ✅ 支持任意 doc/docx 文档处理（不局限于特定主题）
- ✅ 批量文档转换（doc ↔ docx）
- ✅ 文档内容校验与整理
- ✅ Markdown 与 Word 互转
- ✅ 安全无隐私泄露

## 适用场景

- 📚 教育/培训题库文档处理（任意学科）
- 📄 企业办公文档批量转换
- 📝 文档内容整理与归档
- 🔄 格式统一化处理
- 📋 文档答案/备注批量添加

## 使用方法

### AI 答案生成（v3.0 核心功能）

```bash
# AI 自动识别题目并生成答案
python3 scripts/ai_generate_answers.py <输入文件> [输出文件]

# 示例
python3 scripts/ai_generate_answers.py 题库.doc
# 输出：题库_AI 答案版.docx
```

### 其他功能

```bash
# 处理单个文档
python3 scripts/generate_answers.py <输入文件> [输出文件]

# 批量处理目录
python3 scripts/generate_all_answers.py <目录路径>

# 格式转换
python3 scripts/convert_md_to_docx.py <输入.md> <输出.docx>

# 文档校验
python3 scripts/check_answers.py <文件路径>
```

## 支持题型

| 题型 | AI 识别 | 答案格式 |
|------|--------|----------|
| 判断题 | ✅ | 正确/错误 + 理由 |
| 单选题 | ✅ | 正确选项 + 解析 |
| 多选题 | ✅ | 正确选项 + 解析 |
| 简答题 | ✅ | 要点 1/2/3 + 详细说明 |
| 论述题 | ✅ | 引言 + 主体论述 + 结论 |
| 案例分析 | ✅ | 问题识别 + 理论应用 + 解决方案 + 总结 |
| 填空题 | ✅ | 正确答案 |
| 名词解释 | ✅ | 定义 + 特点 + 意义 |

## 文件结构

```
Li_doc_answer/
├── SKILL.md              # 技能说明
├── README.md             # 使用文档（中文）
├── README_EN.md          # 使用文档（英文）
├── data/                 # 待处理文件目录（可选）
└── scripts/
    ├── ai_generate_answers.py    # AI 答案生成（核心）
    ├── generate_answers.py       # 单文档处理
    ├── generate_all_answers.py   # 批量处理
    ├── complete_all_answers.py   # 完整处理
    ├── add_answers_to_questions.py # 答案添加
    ├── check_answers.py          # 文档校验
    └── convert_md_to_docx.py     # 格式转换
```

## 安全说明

- ✅ 无 API 密钥硬编码
- ✅ 无个人隐私数据
- ✅ 无外部网络请求
- ✅ 仅本地文件操作
- ✅ 使用相对路径，可跨环境部署

## 依赖

```bash
pip3 install python-docx mammoth
```

## 更新日志

- v3.0.1 - AI 答案生成核心版本，支持 8 种题型自动识别和答案生成
- v3.0.0 - 新增 AI 智能答案生成，自动识别题目并生成参考答案
- v2.0.0 - 升级为通用文档处理工具，支持任意 doc/docx 文档
- v1.0.0 - 初始版本

## 核心功能

### v3.0 新增
- ✅ **AI 智能答案生成** - 自动为题目生成参考答案
- ✅ **自动问题识别** - 智能识别文档中的题目
- ✅ **多题型支持** - 判断、单选、多选、简答、论述、案例、填空、名词解释
- ✅ **答案格式化** - 统一的答案格式和排版

### v2.0 功能
- ✅ 通用文档处理
- ✅ 批量处理
- ✅ 格式转换
- ✅ 文档校验
