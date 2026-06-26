---
name: "image-to-code"
description: "将图片（含文字、公式、标题）转换为指定代码格式。自动识别标题级别（title1/title2/title3），文字行转为 $word->body(\"正文=\".$F);，公式转为 $word->formula(\"\");，图片标记为 ![image]"
---

# 图片转代码格式转换器

## 功能概述

将包含文字、公式、图片的文档截图转换为指定的代码格式，支持 OCR 文字识别、公式识别和格式转换。

---

## 输出格式规范

| 内容类型 | 格式模板 | 示例输入 | 示例输出 |
|----------|----------|----------|----------|
| **一级标题** | `$word->title1("标题文字");` | `第一章 项目概述` | `$word->title1("项目概述");` |
| **二级标题** | `$word->title2("标题文字");` | `1.1 项目背景`<br>`(1) 提高效率` | `$word->title2("项目背景");`<br>`$word->title2("提高效率");` |
| **三级标题** | `$word->title3("标题文字");` | `1.1.1 技术路线` | `$word->title3("技术路线");` |
| **文字行** | `$word->body("正文=内容=".$F);` | `这是正文` | `$word->body("正文=这是正文=".$F);` |
| **公式** | `$word->formula("LaTeX 公式");` | `E = mc²` | `$word->formula("E = mc^2");` |
| **图片** | `![image]` | [图表] | `![image]` |
| **空行** | 保持空行 | (空) | (空行) |

### 标题提取规则

| 级别 | 识别模式 | 提取规则 | 示例 |
|------|----------|----------|------|
| **一级标题** | `第 X 章 `、` 第 X 部分`、` 一、` | 去掉编号前缀 | `第一章 总述` → `总述` |
| **二级标题** | `第 X 节`、`1.1`、`(1)`、`（一）` | 去掉编号前缀 | `1.1 背景` → `背景`<br>`(1) 提高` → `提高` |
| **三级标题** | `1.1.1`、`1、` | 去掉编号前缀 | `1.1.1 架构` → `架构` |

---

## 执行流程

### 阶段一：图片预处理

1. **图像增强**
   - 灰度化处理
   - 二值化（文字区域）
   - 去噪点

2. **区域分割**
   - 文字区域检测
   - 公式区域检测
   - 图片区域检测

3. **顺序识别**
   - 从上到下扫描
   - 从左到右排序
   - 保持原始顺序

---

### 阶段二：内容识别

#### 2.1 文字识别 (OCR)
**工具**: PaddleOCR / Tesseract / 视觉 AI

**处理逻辑**:
```python
def process_text_line(text):
    # 清理 OCR 结果
    text = text.strip()
    # 转义特殊字符
    text = text.replace('"', '\\"')
    # 生成代码
    return f'$word->body("正文={text}=".$F);'
```

#### 2.2 公式识别
**工具**: Pix2Tex / MathOCR / 视觉 AI

**识别流程**:
1. 检测公式区域（特殊字体、符号）
2. 转换为 LaTeX 格式
3. 生成 formula 代码

**判断规则**:
- 包含数学符号：∑∫∂∇√∞≈≠≤≥±×÷
- 包含变量：x, y, z, α, β, γ, θ
- 包含上标/下标格式
- 独立成行的数学表达式

#### 2.3 图片识别
**判断规则**:
- 图表区域（坐标轴、图例）
- 流程图/框图
- 非文字非公式的图像内容

---

### 阶段三：格式转换

#### 3.1 文字行处理
```
输入：这是一段测试文字
输出：$word->body("正文=这是一段测试文字=".$F);
```

#### 3.2 公式处理
```
输入：E = mc²
输出：$word->formula("E = mc^2");

输入：∑(i=1 to n) xi
输出：$word->formula("\sum_{i=1}^{n} x_i");
```

#### 3.3 图片处理
```
输入：[图表图像]
输出：![image]
```

---

## 技术实现

### 依赖库
```python
# OCR
paddlepaddle
paddleocr

# 公式识别
pix2tex
latex2sympy

# 图像处理
opencv-python
Pillow
numpy

# 可选：视觉 AI
openai  # GPT-4V
anthropic  # Claude Vision
```

### 核心代码结构

```python
#!/usr/bin/env python3
"""
图片转代码格式转换器
将图片中的文字、公式、图表转换为指定代码格式
"""

import cv2
import numpy as np
from pathlib import Path
from paddleocr import PaddleOCR
from typing import List, Tuple, Dict


class ImageToCodeConverter:
    def __init__(self, ocr_lang='ch'):
        """初始化 OCR 引擎"""
        self.ocr = PaddleOCR(use_angle_cls=True, lang=ocr_lang)
        
    def detect_content_type(self, image_region: np.ndarray) -> str:
        """
        检测内容类型
        返回：'text' | 'formula' | 'image'
        """
        # 分析区域特征
        # 公式：特殊符号密度高、字体变化大
        # 图片：颜色丰富、边缘复杂
        # 文字：规则排列、对比度高
        pass
    
    def ocr_text(self, image: np.ndarray) -> List[Dict]:
        """执行 OCR 识别"""
        result = self.ocr.ocr(image, cls=True)
        return result
    
    def formula_to_latex(self, formula_image: np.ndarray) -> str:
        """公式图像转 LaTeX"""
        # 使用 pix2tex 或视觉 AI
        pass
    
    def convert_line(self, line_text: str, content_type: str) -> str:
        """
        转换单行内容为代码格式
        """
        if content_type == 'text':
            # 转义双引号
            escaped = line_text.replace('"', '\\"')
            return f'$word->body("正文={escaped}=".$F);'
        
        elif content_type == 'formula':
            latex = self.formula_to_latex(formula_image)
            return f'$word->formula("{latex}");'
        
        elif content_type == 'image':
            return '![image]'
        
        return ''
    
    def process_image(self, image_path: str, output_path: str = None):
        """
        处理整张图片
        """
        # 读取图片
        image = cv2.imread(image_path)
        
        # OCR 识别
        ocr_result = self.ocr.ocr(image, cls=True)
        
        # 按行处理
        output_lines = []
        for line in ocr_result:
            if line:
                for text_box in line:
                    bbox = text_box[0]
                    text = text_box[1][0]
                    confidence = text_box[1][1]
                    
                    # 提取区域图像
                    x_coords = [p[0] for p in bbox]
                    y_coords = [p[1] for p in bbox]
                    x_min, x_max = min(x_coords), max(x_coords)
                    y_min, y_max = min(y_coords), max(y_coords)
                    
                    region = image[y_min:y_max, x_min:x_max]
                    
                    # 检测内容类型
                    content_type = self.detect_content_type(region)
                    
                    # 转换为代码格式
                    code_line = self.convert_line(text, content_type, region)
                    output_lines.append(code_line)
        
        # 输出结果
        output = '\n'.join(output_lines)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(output)
        
        return output


def main():
    import sys
    
    if len(sys.argv) < 2:
        print("用法：python image_to_code.py <图片路径> [输出路径]")
        sys.exit(1)
    
    image_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    converter = ImageToCodeConverter()
    result = converter.process_image(image_path, output_path)
    
    if not output_path:
        print(result)


if __name__ == '__main__':
    main()
```

---

## 使用示例

### 示例 1：含标题的文档

**输入图片内容**:
```
第一章 项目概述
1.1 项目背景
本项目旨在开发一个智能系统
用于自动化文档处理
(1) 减少人工操作
(2) 提高准确性
```

**输出代码**:
```php
$word->title1("项目概述");
$word->title2("项目背景");
$word->body("正文=本项目旨在开发一个智能系统=".$F);
$word->body("正文=用于自动化文档处理=".$F);
$word->title2("减少人工操作");
$word->title2("提高准确性");
```

---

### 示例 2：含公式和标题

**输入图片内容**:
```
第三章 物理公式
3.1 牛顿第二定律
F = ma
力的单位：牛顿 (N)

3.2 万有引力
F = G(m₁m₂)/r²
```

**输出代码**:
```php
$word->title1("第三章 物理公式");
$word->title2("3.1 牛顿第二定律");
$word->formula("F = ma");
$word->body("正文=力的单位：牛顿 (N)=".$F);
$word->title2("3.2 万有引力");
$word->formula("F = G\frac{m_1 m_2}{r^2}");
```

---

### 示例 3：含图表的图片
**输入图片内容**:
```
销售数据对比
[柱状图]
结论：Q4 增长明显
```

**输出代码**:
```php
$word->body("正文=销售数据对比=".$F);
![image]
$word->body("正文=结论：Q4 增长明显=".$F);
```

---

## 命令行接口

```bash
# 基本用法
python image_to_code.py input.png

# 指定输出文件
python image_to_code.py input.png output.txt

# 批量处理
python image_to_code.py *.png --output-dir ./output

# 使用视觉 AI（更准确的公式识别）
python image_to_code.py input.png --use-vision-ai
```

---

## 配置选项

```json
{
  "ocr_engine": "paddleocr",
  "ocr_lang": "ch",
  "formula_detection": "auto",
  "formula_engine": "pix2tex",
  "vision_ai": {
    "enabled": false,
    "provider": "openai",
    "model": "gpt-4-vision-preview"
  },
  "output": {
    "encoding": "utf-8",
    "line_ending": "\n"
  }
}
```

---

## 质量标准

- [ ] 文字识别准确率 > 95%
- [ ] 公式识别准确率 > 85%
- [ ] 内容类型判断准确率 > 90%
- [ ] 输出格式完全符合规范
- [ ] 支持中文、英文、数字混合
- [ ] 支持批量处理
- [ ] 保持原始顺序和结构

---

## 注意事项

1. **图片质量**: 建议使用清晰截图（300dpi 以上）
2. **公式复杂度**: 复杂公式可能需要人工校对
3. **特殊符号**: 部分罕见符号可能识别不准确
4. **手写体**: 暂不支持手写文字识别
5. **多栏排版**: 需要额外处理阅读顺序

---

## 扩展功能（可选）

### 1. 视觉 AI 增强
使用 GPT-4V/Claude Vision 提高公式识别准确率

### 2. 上下文校正
根据前后文自动校正 OCR 错误

### 3. 格式保持
- 标题层级（H1/H2/H3）
- 列表格式（有序/无序）
- 表格转换

### 4. 批量处理
支持文件夹批量转换

---

## 测试用例

| 测试类型 | 输入 | 预期输出 |
|----------|------|----------|
| 纯中文 | "你好世界" | `$word->body("正文=你好世界=".$F);` |
| 中英文混合 | "Hello 世界" | `$word->body("正文=Hello 世界=".$F);` |
| 简单公式 | "a + b = c" | `$word->formula("a + b = c");` |
| 复杂公式 | "∫₀^∞ e^(-x²)dx" | `$word->formula("\int_{0}^{\infty} e^{-x^2}dx");` |
| 图片 | [图表] | `![image]` |
| 空行 | (空) | (空行) |

---

## 版本历史

- **v1.0.0**: 基础功能（OCR+ 格式转换）
- **v1.1.0**: 公式识别（pix2tex）
- **v1.2.0**: 视觉 AI 支持
- **v1.3.0**: 批量处理

---

*图片转代码，让文档处理更高效* 🐘
