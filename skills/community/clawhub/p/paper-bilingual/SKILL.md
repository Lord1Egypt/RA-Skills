---
name: paper-bilingual
description: 将PDF论文转换为双语Markdown。对用户提供PDF URL或本地PDF文件，提取文本转为Markdown，保留图片，逐段插入中文翻译。用于学术论文研读、翻译对比。
---

# Paper Bilingual

将PDF论文转换为中英双语Markdown，保留原文格式和图片，逐段提供中文翻译。

## 触发条件

用户要求以下操作时使用此skill：
- "翻译这篇论文"
- "把PDF转成双语MD"
- "论文中英对照"
- "下载论文转Markdown带翻译"
- 提供PDF URL并要求翻译

## 输入

支持两种输入方式：
1. **URL输入**：PDF的下载链接（http/https开头）
2. **本地路径**：本地PDF文件的绝对或相对路径

## 处理流程

### 步骤1：下载PDF

- 如果是URL，使用PowerShell下载：
```powershell
Invoke-WebRequest -Uri "URL" -OutFile "$env:TEMP\paper.pdf"
```
- 如果是本地路径，直接使用

### 步骤2：PDF转Markdown

使用Python + PyMuPDF将PDF转为Markdown并提取图片：

```python
import fitz
import os
from PIL import Image

pdf_path = "paper.pdf"
images_dir = "images"
figures_dir = "figures"
os.makedirs(images_dir, exist_ok=True)
os.makedirs(figures_dir, exist_ok=True)

doc = fitz.open(pdf_path)
pages = []

for page_num, page in enumerate(doc):
    # 提取文本
    text = page.get_text("text")
    
    # 提取图片
    images = []
    for img_index, img in enumerate(page.get_images()):
        xref = img[0]
        pix = fitz.Pixmap(doc, xref)
        if pix.n - pix.alpha > 0:  # 跳过透明图片
            img_name = f"page{page_num + 1}_img{img_index}.png"
            pix.save(os.path.join(images_dir, img_name))
            images.append(img_name)
        pix = None
    
    pages.append({'text': text, 'images': images})
```

### 步骤3：提取完整图表（推荐方法）

使用整页渲染+坐标裁剪提取完整图表：

```python
import fitz
from PIL import Image

pdf_path = "paper.pdf"
OUTPUT_DIR = "figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)

doc = fitz.open(pdf_path)
fig_count = 0

for page_num in range(len(doc)):
    page = doc[page_num]
    # 2x缩放渲染页面为高清图片
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
    img = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
    
    # 获取页面上的图片对象和位置
    images = page.get_images()
    
    for img_index, img_info in enumerate(images):
        xref = img_info[0]
        rects = page.get_image_rects(xref)
        for rect in rects:
            # 缩放坐标 (2x)
            x0 = max(0, int(rect.x0 * 2) - 20)
            y0 = max(0, int(rect.y0 * 2) - 20)
            x1 = min(pix.width, int(rect.x1 * 2) + 20)
            y1 = min(pix.height, int(rect.y1 * 2) + 20)
            
            # 过滤太小的图片碎片
            if x1 - x0 < 80 or y1 - y0 < 80:
                continue
            
            # 裁剪完整图表
            cropped = img.crop((x0, y0, x1, y1))
            fig_name = f'fig_p{page_num+1}_{img_index+1}.png'
            cropped.save(os.path.join(OUTPUT_DIR, fig_name))
            fig_count += 1

print(f"Extracted {fig_count} figures")
```

**关键点**：
- PDF里的图表可能被拆成多个小图片块（tiles）压缩
- 直接提取会得到碎片，需要用坐标裁剪方法
- 先渲染整页，再按图片坐标裁剪，确保图表完整

### 步骤4：翻译并生成双语MD

**输出目录结构**：
```
memory/paper-bilingual/
└── YYYY-MM-DD-paper-name/
    ├── index.md          # 双语Markdown
    ├── images/           # 整页截图（可选）
    └── figures/          # 裁剪后的图表
```

**输出格式**：
```markdown
# 主标题
中文主标题

## Section 1
中文标题

原文段落...
中文翻译段落...

![Figure 1](figures/fig_p3_1.png)

原文段落...
中文翻译段落...
```

**规则**：
1. **主标题**（#）：英文后换行加中文
2. **二级标题**（##）：英文后换行加中文
3. **普通段落**：原文后直接加翻译
4. **图片**：使用裁剪后的图表 `figures/`

### 步骤5：翻译实现

使用当前会话的LLM翻译，逐段调用：

```
将以下英文翻译成中文，保持自然段落格式：
[段落内容]
```

### 步骤6：保存输出

- 根据PDF文件名或URL生成输出目录名
- 保存到：`memory/paper-bilingual/YYYY-MM-DD-[论文名]/`
- 清理临时文件

## 核心原则

1. **每篇论文一个文件夹**：避免不同论文文件冲突
2. **原文完全保留**：图片、代码、公式、表格等与源文件完全一致
3. **逐段翻译**：每段正文后插入该段的中文翻译
4. **标题翻译**：所有级别的标题都需要翻译
5. **格式一致**：翻译采用与原文相同的格式
6. **完整图表**：使用坐标裁剪方法提取完整图表，避免碎片

## 依赖

- Python 3.8+
- PyMuPDF (`pip install pymupdf`)
- Pillow (`pip install pillow`)
- LLM翻译（当前会话）

## 错误处理

- URL无效：提示用户检查链接
- PDF加密：提示需要解密
- 翻译失败：跳过该段，保留原文
