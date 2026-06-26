# Paper Reader Deep - 论文深度阅读助手

真正深度阅读PDF论文，进行理解性分析，生成具有研究价值的深度阅读报告。

## 功能特点

- **自动提取**：从PDF中提取标题、DOI、作者、期刊等元数据
- **深度理解**：对论文进行真正理解性分析，不是简单的信息提取
- **批判性分析**：分析论文的优点、局限性和未解决的问题
- **结构化输出**：生成标准化的Markdown格式报告

## 核心原则

**真正理解 + 结构化输出 + 用户研究关联**

## 安装依赖

```bash
pip install pdfplumber PyYAML
```

## 使用方法

### 命令行

```bash
python3 ~/.openclaw/skills/paper-reader-deep/scripts/deep_reader.py /path/to/pdfs/
```

### 在对话中

```
深度阅读 /path/to/pdfs/
```

## 报告结构

### 第一部分：基础信息（自动提取）
- 标题、期刊、DOI、作者、日期
- 一句话概括
- 关键数据

### 第二部分：核心理解（AI分析）
1. 这篇论文到底在做什么？
2. 为什么要做这个？（研究动机）
3. 是怎么做到的？（技术路线）
4. 做得怎么样？（关键数据）
5. 意味着什么？（研究意义）

### 第三部分：批判性分析
1. 优点/亮点
2. 潜在问题/局限
3. 未解决的关键问题

### 第四部分：与用户研究的关联
1. 相关度评估：高/中/低
2. 可借鉴之处
3. 可能的应用场景

## 输出示例

处理完成后，会在PDF所在目录生成：

```
/path/to/pdfs/
├── Diao_2025_NatCommun_深度阅读报告.md
├── Shu_2026_Microbiome_深度阅读报告.md
├── Zhang_2026_Microbiome_深度阅读报告.md
└── 深度阅读汇总.md
```

## 分析要点

论文分析时关注以下要点：

1. **科学问题**：作者真正想回答什么问题？这个问题的价值在哪里？
2. **方法论**：技术路线为什么这样设计？有什么优劣势？
3. **逻辑链**：假设→实验→结论的推理是否严密？
4. **创新性**：真正的新贡献是什么？与现有方法的本质区别？
5. **局限性**：哪些问题没有解决？改进空间在哪里？

## 技术栈

- Python 3.8+
- pdfplumber - PDF文本提取
- CrossRef API - DOI元数据查询

## 文件结构

```
paper-reader-deep/
├── SKILL.md                         # 技能定义
├── README.md                        # 说明文档
├── config/
│   ├── analysis_framework.md        # 分析框架
│   ├── report_template.md           # 报告模板
│   └── section_config.yaml          # 章节配置
├── templates/
│   ├── section_understanding.md     # 理解性分析模板
│   ├── section_critique.md          # 批判性分析模板
│   └── section_relevance.md         # 与用户研究关联模板
└── scripts/
    └── deep_reader.py               # 主程序
```

## 注意事项

- 报告中的"与用户研究的关联"部分需要用户自行补充
- 建议用户根据自己的研究方向填写这部分内容
- MEMORY.md仅记录阅读行为，不记录报告内容

## 许可证

MIT License
