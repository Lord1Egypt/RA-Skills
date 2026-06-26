---
name: prd-export
description: PRD 导出工具 - 基于 document-assistant 的 export_engine，专为 prd-workflow 优化。支持 Markdown → Word 转换，智能图片插入，PRD 专用样式。
---

# PRD Export（PRD 导出工具）v1.0

**版本**: v1.0  
**创建日期**: 2026-03-31  
**基于**: document-assistant/export_engine.py v1.0  
**优化**: 针对 prd-workflow 的 PRD 导出场景

---

## 🎯 技能定位

**专为 prd-workflow 设计的 PRD 导出工具**

- ✅ 基于 document-assistant 的成熟 export_engine.py
- ✅ 针对 PRD 文档结构优化（9 章结构）
- ✅ 自动插入流程图/原型图
- ✅ PRD 专用样式（标题/表格/图注）
- ✅ 金融合规样式支持

---

## 🚀 核心功能

### 1. Markdown → Word 转换

**支持**：
- ✅ 标题层级（# / ## / ### → Heading 1/2/3）
- ✅ 表格（Markdown 表格 → Word 表格）
- ✅ 列表（有序/无序）
- ✅ 段落样式
- ✅ 中文字体（宋体 + Times New Roman）

### 2. 智能图片插入

**自动插入**：
- ✅ 流程图（business-flow.png, recommendation-flow.png, compliance-flow.png）
- ✅ 原型图（homepage.png, etc.）
- ✅ 架构图

**图片样式**：
- 最大宽度：6.5 英寸
- 最大高度：5.0 英寸
- 自动保持宽高比
- 居中显示
- 图注格式：`图 X-Y 标题`

### 3. PRD 专用样式

**标题样式**：
- 标题 1：宋体 16pt 粗体
- 标题 2：宋体 15pt 粗体
- 标题 3：宋体 14pt 粗体
- 正文：宋体 12pt

**表格样式**：
- Table Grid
- 表头：宋体 10pt 粗体
- 表格内容：宋体 10pt

**图注样式**：
- 宋体 10pt 粗体
- 居中
- 格式：`图 X-Y 标题`

---

## 💬 使用方法

### 方式 1：命令行调用

```bash
# 基础用法
python3 engines/export_engine.py PRD.md -o PRD.docx

# 带图片目录
python3 engines/export_engine.py PRD.md -o PRD.docx --images ./diagrams/

# 批量导出
python3 engines/export_engine.py *.md --images ./images/
```

### 方式 2：被 prd-workflow 调用

```javascript
// prd-workflow/workflows/export_integration.js
const exportEngine = path.join(__dirname, '../skills/prd-export/engines/export_engine.py');

execSync(`python3 "${exportEngine}" "${markdownPath}" -o "${outputPath}"`, {
  stdio: 'inherit'
});
```

### 方式 3：Python 模块调用

```python
from engines.export_engine import markdown_to_word

result = markdown_to_word(
    markdown_path='PRD.md',
    output_path='PRD.docx',
    images_dir='./diagrams/'
)

print(f"✅ 导出成功：{result['output_path']}")
print(f"📊 文件大小：{result['file_size']}")
print(f"📄 段落数：{result['paragraphs']}")
```

---

## 📋 输出示例

### 输入（Markdown）

```markdown
# 招商证券投资者陪伴 AI 助手 PRD

## 1. 需求背景

### 1.1 业务痛点

- 股票用户转化率低
- 投资者认知不足
- 缺乏系统引导

### 1.2 产品目标

| 目标类型 | 目标描述 | 衡量指标 |
|---------|---------|---------|
| 业务目标 | 提高财富管理业务规模 | AUM 增长 |
| 转化目标 | 提升股票用户 ETF 转化率 | 转化率提升 |
```

### 输出（Word）

```
PRD_v1.0.docx
├── 标题：招商证券投资者陪伴 AI 助手 PRD（宋体 22pt）
├── 章节 1：需求背景（宋体 16pt 粗体）
│   ├── 小节 1.1：业务痛点（宋体 15pt 粗体）
│   │   └── 列表项（宋体 12pt）
│   └── 小节 1.2：产品目标（宋体 15pt 粗体）
│       └── 表格（Table Grid，表头宋体 10pt 粗体）
└── 页脚：PRD 文档（宋体 9pt）
```

---

## 🔧 配置选项

### 页面设置

```python
DEFAULT_CONFIG = {
    "page": {
        "margin": {
            "top": Cm(2.54),      # 上边距 2.54cm
            "bottom": Cm(2.54),   # 下边距 2.54cm
            "left": Cm(3.17),     # 左边距 3.17cm
            "right": Cm(3.17)     # 右边距 3.17cm
        }
    },
    ...
}
```

### 字体设置

```python
"font": {
    "chinese": "宋体",
    "size": {
        "title": Pt(22),      # 文档标题
        "heading1": Pt(16),   # 一级标题
        "heading2": Pt(15),   # 二级标题
        "heading3": Pt(14),   # 三级标题
        "body": Pt(12)        # 正文
    }
}
```

### 图片设置

```python
"image": {
    "max_width": Inches(6.5),   # 最大宽度 6.5 英寸
    "max_height": Inches(5.0)   # 最大高度 5.0 英寸
}
```

---

## 📁 文件结构

```
prd-export/
├── SKILL.md                      # 本文件
├── engines/
│   └── export_engine.py          # 核心导出引擎（基于 document-assistant）
├── scripts/
│   └── export-prd.sh             # 快速导出脚本（可选）
└── examples/
    └── image_map.json            # 图片映射示例
```

---

## 🧪 测试

### 测试 1：基础导出

```bash
cd ~/.openclaw/workspace/skills/prd-workflow/skills/prd-export
python3 engines/export_engine.py test.md -o test.docx
```

### 测试 2：带图片导出

```bash
python3 engines/export_engine.py PRD.md -o PRD.docx --images ./diagrams/
```

### 测试 3：通过 prd-workflow 调用

```
用 prd-workflow 生成 PRD，包含 Word 导出
```

---

## 📊 性能

| 指标 | 数值 |
|------|------|
| 转换速度 | ~1 秒/万字符 |
| 文件大小 | 40-50 KB（纯文本 PRD） |
| 图片插入 | ~0.5 秒/张 |
| 内存占用 | < 50 MB |

---

## 🐛 常见问题

### 中文显示方框

**原因**：字体不支持中文  
**解决**：export_engine.py 已使用宋体，无需额外配置

### 图片被截断

**原因**：图片太高  
**解决**：限制高度<5 英寸，export_engine.py 已自动处理

### 表格格式错乱

**原因**：Markdown 表格格式不正确  
**解决**：确保表格使用标准格式（`| 列 1 | 列 2 |`）

---

## 📝 变更历史

### v1.0 (2026-03-31)
- ✅ 基于 document-assistant/export_engine.py v1.0
- ✅ 针对 PRD 导出优化
- ✅ 集成到 prd-workflow v2.3.2

---

## 🔗 相关技能

- **document-assistant** - 原文档管理助手（export_engine 来源）
- **prd-workflow** - PRD 完整工作流（调用本技能）
- **mermaid-flow** - 流程图生成（生成图片供本技能插入）
- **htmlPrototype** - HTML 原型生成（生成截图供本技能插入）

---

**版本**: 1.0  
**创建日期**: 2026-03-31  
**基于**: document-assistant v2.0  
**作者**: gotomanutd（基于 wealth-coordinator 团队工作）
