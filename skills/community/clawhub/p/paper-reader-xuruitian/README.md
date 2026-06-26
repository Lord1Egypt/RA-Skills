# paper-reader 精读文献 Skill

> 学术论文精读专家 — 深度解读学术论文，自动生成结构化 Word 报告

## 功能特性

- 📄 **多格式支持**：PDF、Word (.docx/.doc)、Excel (.xlsx/.xls)、PPT (.pptx)、TXT / MD / CSV
- 🧠 **六大维度深度分析**：研究目标、新方法、实验验证、未来方向、批判分析、实用建议
- 📊 **Word 报告自动生成**：分析完成后自动输出格式化 Word 文档到桌面
- 🔍 **原文引用**：大量引用论文原文细节，体现分析深度
- ⚠️ **批判视角**：不回避论文不足，提供建设性批评

## 文件结构

```
paper-reader/
├── SKILL.md                          ← Skill 主入口（安装时导入此文件）
├── scripts/
│   ├── extract_text.py               ← 文档文本提取脚本
│   └── generate_report.js            ← Word 报告生成脚本
├── references/
│   └── academic_prompt.md            ← 六维度分析 Prompt 模板
└── data/
    └── .gitkeep                      ← 临时数据目录（可忽略）
```

## 安装方式

### 方式一：WorkBuddy 用户（推荐）
1. 将整个 `paper-reader` 文件夹复制到 `~/.workbuddy/skills/` 目录下
2. 在 WorkBuddy 中刷新技能列表
3. 从"专家"入口搜索 `paper-reader` 即可使用

### 方式二：解压直接使用
1. 解压 ZIP 包
2. 在支持 Skill 的 AI 产品中加载 `SKILL.md`

## 前置依赖

### Python 依赖（文档提取用）
```bash
pip install PyMuPDF pdfplumber python-docx openpyxl xlrd python-pptx
```

### Node.js 依赖（Word 报告生成用）
```bash
npm install -g docx
```

> `docx` 包为全局安装，生成脚本 `generate_report.js` 运行时需要 NODE_PATH 包含全局 npm 目录。
> Windows 上通常为：`C:\Users\<用户名>\AppData\Roaming\npm\node_modules`

### Word `.doc` 格式支持（可选）
- **macOS**：系统自带 `textutil`，无需安装
- **Windows**：需安装 `antiword` 并加入 PATH；或直接将 `.doc` 另存为 `.docx`

## 使用方法

### 完整流程

**第一步**：上传论文文件（PDF/Word/Excel/PPT/TXT）

**第二步**：在支持 Skill 的 AI 产品中启动 `paper-reader`，或发送如下指令：
```
帮我精读这篇论文：<上传文件>
```

**第三步**：Skill 自动完成以下步骤：
1. 自动识别文件格式并提取全文
2. 加载六维度学术分析框架
3. 执行深度分析（引用原文细节）
4. 生成 Markdown 分析报告（显示在对话中）
5. ⭐ **自动生成 Word 文档保存到桌面**

### 手动生成 Word 报告（如需单独生成）

```bash
# JSON 数据模式（推荐）
# 1. 将分析内容保存为 JSON 文件
# 2. 运行：
node scripts/generate_report.js --data data/latest_analysis.json

# 参数模式（简单场景）
node scripts/generate_report.js \
  --title "论文标题" \
  --subtitle "副标题" \
  --author "作者" \
  --output "C:/Users/用户名/Desktop/精读报告.docx"
```

### JSON 格式说明

```json
{
  "title": "论文主标题",
  "subtitle": "副标题",
  "author": "作者名",
  "school": "学校/机构",
  "date": "2026年x月x日",
  "overview": "整体概述内容，可用 \\n 分隔多段",
  "dimensions": [
    { "heading": "维度一：研究目标与实际问题", "content": "内容..." },
    { "heading": "维度二：新思路、方法与模型", "content": "内容..." }
  ],
  "summary": "总结内容",
  "filename": "输出文件名（不含 .docx）"
}
```

## 安全说明

- 本 Skill 仅对用户上传的文件进行**只读文本提取**
- 无网络请求，无危险命令执行
- Word 报告生成脚本为纯本地运行
- 已通过云鼎实验室安全审计（P2 安全等级）

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| 1.0.0 | 2026-03-29 | 首发版，支持六大维度分析 + Word 报告生成 |

## 作者

由 AI Agent 生成，基于 paper-reader Skill 框架。

---

**安装问题请检查**：NODE_PATH 环境变量是否包含 npm 全局模块路径。
