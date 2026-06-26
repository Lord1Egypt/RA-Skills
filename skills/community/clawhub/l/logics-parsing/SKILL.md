---
name: logics-parsing
description: 阿里文档智能解析工具 - 将PDF/图片转结构化HTML。支持复杂布局、公式识别、化学结构、代码块、流程图、乐谱等。
---

# Logics-Parsing 文档解析工具

> 阿里文档智能解析 v1/v2 | GitHub 1.3k ⭐  
> 文档图片 → 结构化 HTML | 复杂布局 | 公式识别 | 化学结构 | 代码块

---

## 一、核心定位

本技能整合阿里巴巴 Logics-Parsing 文档解析工具，核心理念：

> **End-to-End Document Parsing**  
> 从文档图片直接输出结构化结果，无需复杂 pipeline

---

## 二、版本对比

| 维度 | v1 | v2（推荐）|
|------|-----|---------|
| **发布** | 2025-09 | 2026-02 |
| **性能** | 基础 SOTA | 全面领先 |
| **LogicsDocBench** | 基准 | **82.16** 分 |
| **OmniDocBench** | 基准 | **93.23** 分 |
| **Parsing-2.0** | ❌ 不支持 | ✅ 支持 |
| **结构化内容** | 公式/化学 | + 流程图/乐谱/代码 |

---

## 三、核心能力

### 3.1 支持的内容类型

| 类型 | 输出格式 | 说明 |
|------|---------|------|
| **文本段落** | HTML `<p>` | 自动识别标题/页眉/页脚 |
| **表格** | HTML Table | 跨页表格合并 |
| **科学公式** | LaTeX / MathML | 复杂公式精准识别 |
| **化学结构** | SMILES 格式 | 分子式标准化 |
| **流程图** | Mermaid 语法 | v2 新增 |
| **乐谱** | ABC Notation | v2 新增 |
| **代码块** | 语法高亮代码 | v2 新增 |
| **手写内容** | 独立标注 | 区分打印/手写 |

### 3.2 输出结构

```html
<div class="content-block" category="formula" bbox="[x1,y1,x2,y2]">
  <!-- 公式内容 + 坐标 + OCR 文本 -->
</div>
```

每个元素包含：
- **category**: 元素类型（paragraph/table/formula/figure 等）
- **bbox**: 边界框坐标
- **text**: OCR 识别文本

---

## 四、 Benchmarks 性能

### 4.1 LogicsDocBench（自建基准）

| 模型 | 总体分数 |
|------|---------|
| **Logics-Parsing-v2** | **82.16** ✅ |
| GPT-5 | 46.0 |
| Gemini 2.5 pro | 26.0 |
| Qwen2.5VL-72B | 34.9 |
| SmolDocling | 92.7 |

### 4.2 OmniDocBench-v1.5（公开基准）

| 模型 | 总体分数 |
|------|---------|
| **Logics-Parsing-v2** | **93.23** ✅ |
| GPT-5 | 46.0 |
| Gemini 2.5 pro | 46.0 |
| Qwen2VL-72B | 35.9 |
| Doubao-1.6 | 31.7 |

---

## 五、安装方式

### 5.1 基础安装（推荐 v2）

```bash
# 1. 克隆仓库
git clone https://github.com/alibaba/Logics-Parsing.git
cd Logics-Parsing

# 2. 创建环境（Python 3.10）
conda create -n logics-parsing python=3.10
conda activate logics-parsing

# 3. 安装依赖
pip install -r requirements.txt

# 4. 下载模型（Modelscope）
pip install modelscope
python download_model_v2.py -t modelscope

# 或从 HuggingFace
pip install huggingface_hub
python download_model_v2.py -t huggingface
```

### 5.2 快速安装（仅 v1）

```bash
conda create -n logics-parsing python=3.10
conda activate logics-parsing
pip install -r requirements.txt

# 下载模型
python download_model.py -t modelscope
```

---

## 六、快速开始

### 6.1 v2 推理命令

```bash
python3 inference_v2.py \
  --image_path PATH_TO_INPUT_IMG \
  --output_path PATH_TO_OUTPUT \
  --model_path PATH_TO_MODEL
```

### 6.2 v1 推理命令

```bash
python3 inference.py \
  --image_path PATH_TO_INPUT_IMG \
  --output_path PATH_TO_OUTPUT \
  --model_path PATH_TO_MODEL
```

### 6.3 Python API

```python
from logics_parsing import LogicsParser

# 初始化
parser = LogicsParser(model_path="path/to/model")

# 解析文档
result = parser.parse("document.jpg")

# 输出 HTML
print(result.html)

# 输出结构化 JSON
print(result.to_json())
```

---

## 七、应用场景

### 7.1 学术文档处理

| 场景 | 能力 |
|------|------|
| **论文 PDF 解析** | 提取公式/表格/参考文献 |
| **化学论文** | SMILES 格式分子结构 |
| **数学讲义** | LaTeX 公式精准提取 |
| **教科书** | 复杂布局（多栏/跨页）处理 |

### 7.2 商业文档处理

| 场景 | 能力 |
|------|------|
| **合同解析** | 条款表格结构化 |
| **财务报表** | 数字表格提取 |
| **发票识别** | 表单字段提取 |
| **报纸剪报** | 复杂排版处理 |

### 7.3 Parsing-2.0 场景（v2 新增）

| 场景 | 输出格式 |
|------|---------|
| **流程图** | Mermaid 代码 |
| **乐谱** | ABC Notation |
| **代码块** | 语法高亮代码 |
| **Pseudocode** | 结构化伪代码 |

---

## 八、输出示例

### 8.1 输入
```
[复杂布局学术论文图片，包含多栏文字、跨页表格、化学结构式]
```

### 8.2 结构化输出（HTML）

```html
<div class="content-block" category="paragraph" bbox="[120,340,580,420]">
  <p>We introduce a new document parsing model...</p>
</div>

<div class="content-block" category="formula" bbox="[200,450,400,520]">
  <span class="latex">E = mc^2</span>
</div>

<div class="content-block" category="chemistry" bbox="[100,550,300,700]">
  <span class="smiles">CC(=O)OC(=O)C</span>
</div>

<div class="content-block" category="table" bbox="[50,750,600,900]">
  <table>
    <tr><td>Method</td><td>Score</td></tr>
    <tr><td>Logics-Parsing</td><td>82.16</td></tr>
  </table>
</div>
```

---

## 九、与其他技能关联

| 本技能 | 关联技能 | 关系 |
|--------|---------|------|
| Logics-Parsing | `ai-research-tools` | 论文解析 + 科研自动化 |
| Logics-Parsing | `browser-use` | 网页内容抓取 + 解析 |
| Logics-Parsing | `obsidian-handbook` | 解析结果存入 Obsidian |
| Logics-Parsing | `math-theory-notes` | 数学公式识别 |

---

## 十、常见问题

| 问题 | 解决方案 |
|------|---------|
| **模型下载慢** | 使用 Modelscope（国内推荐）|
| **显存不足** | 减小 `image_size` 参数 |
| **OCR 乱码** | 检查字体配置 |
| **表格识别不准** | 使用 v2 版本性能更优 |

---

## 十一、注意事项

```
⚠️ 注意事项：
- Python 3.10+ required
- 需要 GPU（推荐 8GB+ 显存）
- 模型文件较大（~2GB），下载需要网络
- 部分功能需要额外字体支持
```

---

## 十二、使用方式

### 触发场景

```
用户说「解析这篇 PDF」→ 调用 Logics-Parsing v2
用户说「提取论文公式」→ 调用 Logics-Parsing
用户说「识别化学结构式」→ SMILES 格式输出
用户说「将 PDF 转 HTML」→ 结构化 HTML 输出
用户说「解析乐谱」→ v2 Parsing-2.0 功能
```

### 组合使用

```
用户：「帮我把这篇论文的关键公式和表格提取出来」
→ 使用 Logics-Parsing v2 解析
→ 提取公式（LaTeX）+ 表格（HTML）
→ 存入 Obsidian 或知识库
```

---

*本技能整合阿里 Logics-Parsing 文档解析工具的完整安装与使用指南*
