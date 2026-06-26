# md2docx - Markdown 转 Word 文档专家

[![ClawHub Skill](https://img.shields.io/badge/ClawHub-Skill-blue)](https://clawhub.com)
[![Version](https://img.shields.io/badge/version-1.0.6-green)](https://clawhub.com)

**一句话介绍：** 将 Markdown 文档一键转换为专业的 Word 文档，支持中文字体优化和表格边框设置。

---

## 为什么选择 md2docx？

| 痛点 | md2docx 解决方案 |
|------|-----------------|
| ❌ Markdown 写作，但需要提交 Word 格式 | ✅ 一键转换，保持格式完整 |
| ❌ 中文文档格式不美观 | ✅ 自动设置中文字体（微软雅黑/宋体） |
| ❌ 表格没有边框 | ✅ 自动添加表格边框 |
| ❌ 不想手动调整格式 | ✅ 两阶段处理，自动优化 |

---

## 核心功能

### ✅ 支持的 Markdown 语法

| 语法 | 支持 | 说明 |
|------|:----:|------|
| 标题（H1-H6） | ✅ | 自动设置字体大小 |
| 有序/无序列表 | ✅ | 保持缩进层级 |
| 表格 | ✅ | **自动添加边框** |
| 代码块 | ✅ | 语法高亮 |
| 引用块 | ✅ | 保持引用格式 |
| 图片 | ✅ | 自动插入 |
| 链接 | ✅ | 可点击链接 |
| 强调（加粗/斜体） | ✅ | 保持格式 |

### ✅ 中文优化

- **中文字体自动设置**：微软雅黑（标题）/ 宋体（正文）
- **表格边框自动添加**：无需手动设置
- **公文格式支持**：符合中文公文规范

---

## 安装

### 前置要求

| 依赖 | 版本要求 | 检查命令 |
|------|---------|---------|
| **Pandoc** | >= 2.0 | `pandoc --version` |
| **Python** | >= 3.8 | `python --version` |
| **python-docx** | >= 1.2.0 | `pip show python-docx` |

### 安装步骤

**方式一：ClawHub 安装（推荐）**
```bash
clawhub install md2docx
```

**方式二：手动安装**
```bash
# 1. 安装 Pandoc（Windows）
winget install pandoc

# 2. 安装 Python 依赖
pip install python-docx

# 3. 克隆技能
git clone <repo-url> md2docx
```

---

## 快速开始

### 基础使用

```bash
# 转换单个文件
python tools/md2docx.py input.md output.docx
```

### 使用模板

```bash
# 使用标准公文模板
python tools/md2docx.py input.md output.docx --template standard-official
```

### 批量转换

```bash
# 转换文件夹中所有 Markdown 文件
python tools/md2docx.py --batch ./docs ./output
```

---

## 使用案例

### 案例 1：学术论文

**场景：** 用 Markdown 写论文，提交 Word 格式

**步骤：**
```bash
# 1. 用 Markdown 写论文
# 2. 转换为 Word
python tools/md2docx.py thesis.md thesis.docx --template academic

# 3. 提交论文.docx
```

**效果：** 自动设置标题字体、正文宋体、表格边框

---

### 案例 2：项目文档

**场景：** 技术文档需要分享给非技术人员

**步骤：**
```bash
# 转换项目文档
python tools/md2docx.py README.md README.docx
```

**效果：** 代码块保持格式，表格自动边框

---

### 案例 3：会议纪要

**场景：** 会议纪要需要正式格式

**步骤：**
```bash
# 转换会议纪要
python tools/md2docx.py meeting.md meeting.docx --template official
```

**效果：** 公文格式，正式规范

---

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `input_file` | 输入 Markdown 文件路径 | 必填 |
| `output_file` | 输出 Word 文件路径 | 必填 |
| `--template` | 模板名称或路径 | 无 |
| `--batch` | 批量转换模式 | 关闭 |

---

## 模板列表

| 模板 | 说明 | 适用场景 |
|------|------|---------|
| `standard-official` | 标准公文模板 | 公文、报告 |
| `academic` | 学术论文模板 | 论文、研究报告 |
| `minimal` | 极简模板 | 内部文档 |

---

## 常见问题

### Q1: 安装后提示 "pandoc not found"

**原因：** Pandoc 未安装或未加入 PATH

**解决：**
```bash
# Windows
winget install pandoc

# 或下载安装包
# https://pandoc.org/installing.html
```

### Q2: 转换后中文显示为乱码

**原因：** 系统缺少中文字体

**解决：**
- Windows：安装微软雅黑、宋体
- macOS：安装 PingFang SC
- Linux：安装 fonts-wqy-microhei

### Q3: 表格没有边框

**原因：** 版本过低

**解决：** 升级到最新版本
```bash
clawhub update md2docx
```

### Q4: 支持哪些 Markdown 语法？

**回答：** 支持标准 Markdown + GFM（GitHub Flavored Markdown）

**不支持：** 数学公式、Mermaid 图表（计划支持）

---

## 更新日志

### v1.0.6（2026-03-26）
- ✅ **代码规范化**：完整 docstring + 类型注解 + PEP 8 规范
- ✅ **错误提示优化**：友好的错误信息 + 解决建议
- ✅ **测试完善**：增加测试用例 + 边界测试
- ✅ **字体修复**：中文字体自动设置优化
- ✅ **表格边框优化**：自动添加表格边框

### v1.0.5
- ✅ 两阶段转换方案
- ✅ 中文字体自动设置
- ✅ 表格边框自动添加
- ✅ 模板支持

### v1.0.0
- ✅ 基础 Markdown 转 Word 功能

---

## 贡献

欢迎提交 Issue 和 Pull Request！

---

## 许可证

MIT-0 License

---

## 作者

**OpenClaw Team**

---

**让 Markdown 写作更高效！** ✨