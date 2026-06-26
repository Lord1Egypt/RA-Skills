---
name: graduation-project-workflow
version: 1.0.0
description: 软件技术专业毕业设计全流程工作流。从需求分析、系统设计、原型设计到文档生成的完整指导，包含PDF原型图生成、Word文档格式规范、图表制作等最佳实践。
license: MIT
metadata:
  openclaw:
    requires:
      bins: [python]
    install:
      - id: python-packages
        kind: pip
        packages: [python-docx, reportlab]
---

# 毕业设计全流程工作流

软件技术专业毕业设计从选题到文档交付的完整工作流。

## 何时使用

- 软件技术/计算机专业毕业设计
- 需要生成规范的毕业设计文档
- 需要制作系统原型图、用例图、架构图
- 需要统一Word文档格式

## 核心工作流

### Phase 1: 需求分析

**输出物清单：**
- [ ] 选题申请表
- [ ] 开题报告
- [ ] 需求规格说明书

**关键检查点：**
- 选题具有实际应用价值
- 技术栈明确（前端/后端/数据库）
- 功能范围适中（3-5个核心模块）

### Phase 2: 系统设计

**输出物清单：**
- [ ] 系统架构图
- [ ] 功能模块图
- [ ] 数据库ER图
- [ ] 用例图（用户端+管理端）
- [ ] 时序图（核心业务流程）
- [ ] 类图（核心模块）

**图表规范：**
```python
# 配色方案 - 学术风格
COLORS = {
    'primary': '#9B2335',    # 深红 - 主色
    'secondary': '#C5963A',  # 金褐 - 强调
    'text': '#2D1F14',       # 深褐 - 文字
    'bg': '#FBF7F0',         # 暖白 - 背景
    'border': '#E0D5C5',     # 浅棕 - 边框
}
```

### Phase 3: 原型设计

**移动端原型（用户端）：**
- [ ] 启动页
- [ ] 登录/注册页
- [ ] 首页
- [ ] 核心功能页（如答题中心）
- [ ] 个人中心

**Web端原型（管理端）：**
- [ ] 登录页
- [ ] 仪表盘
- [ ] 数据管理页（用户/课程/题库）
- [ ] 数据统计页

**PDF生成脚本模板：**
```python
# scripts/generate_prototype.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 注册中文字体
pdfmetrics.registerFont(TTFont('STXIHEI', r'C:\Windows\Fonts\STXIHEI.TTF'))

def draw_phone_frame(c, x, y, w, h):
    """绘制手机外框"""
    c.setFillColor('#ccc7c0')
    c.roundRect(x-5, y-5, w+10, h+10, 12, fill=1, stroke=0)
    c.setFillColor('#ffffff')
    c.roundRect(x, y, w, h, 8, fill=1, stroke=1)

def add_title(c, fig_num, title):
    """添加图标题"""
    c.setFont('STXIHEI', 12)
    c.drawCentredString(105*mm, 280*mm, f'图{fig_num} {title}')
```

### Phase 4: 文档整理

**格式规范（依据学校模板）：**

| 元素 | 格式 |
|------|------|
| 正文 | Times New Roman, 10.5pt, 首行缩进2字符 |
| 一级标题 | Times New Roman, 15pt, 加粗 |
| 二级标题 | Arial, 14pt |
| 三级标题 | Times New Roman, 12pt |
| 图表标题 | 等线 Light, 10pt |
| 页边距 | 上下3.4/3.0cm, 左右3.2cm |

**Word格式批量修复脚本：**
```python
# scripts/fix_word_format.py
from docx import Document
from docx.shared import Pt, Cm

def apply_standard_format(doc_path, output_path):
    doc = Document(doc_path)
    
    # 设置样式
    doc.styles['Normal'].font.name = 'Times New Roman'
    doc.styles['Normal'].font.size = Pt(10.5)
    
    # 正文段落首行缩进
    for para in doc.paragraphs:
        if len(para.text.strip()) > 20:
            para.paragraph_format.first_line_indent = Cm(0.74)
    
    doc.save(output_path)
```

## 项目目录结构

```
project/
├── docs/                    # 文档输出
│   ├── 图2-1_xxx.pdf       # 系统设计图
│   ├── 图3-1_xxx.pdf       # 架构图
│   ├── 图4-1_xxx.pdf       # 原型图
│   └── 第三章_系统设计全套图表.pdf
├── frontend/               # 前端源码
├── backend/                # 后端源码
├── admin/                  # 管理端源码
├── sql/                    # 数据库脚本
├── 毕业设计作品.docx        # 主文档
└── scripts/                # 辅助脚本
    ├── generate_diagrams.py
    ├── generate_prototypes.py
    └── fix_word_format.py
```

## 快速命令

```bash
# 生成所有原型图
python scripts/generate_prototypes.py

# 合并PDF
python -m PyPDF2 merge docs/*.pdf output.pdf

# 修复Word格式
python scripts/fix_word_format.py input.docx output.docx
```

## 常见陷阱

1. **字体问题**：Windows用STXIHEI，Mac用STHeiti，Linux用WenQuanYi
2. **图片分辨率**：PDF中图片至少150dpi，避免模糊
3. **版本控制**：docx文件用Git管理时差异大，建议同时保存markdown备份
4. **格式漂移**：不同Word版本打开可能样式变化，定稿前用PDF确认

## 检查清单

提交前逐项检查：

- [ ] 封面信息完整（姓名/学号/导师）
- [ ] 页码连续（摘要罗马数字，正文阿拉伯数字）
- [ ] 图表编号连续（图2-1, 图2-2...）
- [ ] 参考文献格式统一（GB/T 7714）
- [ ] 代码截图清晰（高亮语法）
- [ ] 数据库表名统一（小写下划线）
- [ ] API接口文档完整（请求/响应/状态码）
