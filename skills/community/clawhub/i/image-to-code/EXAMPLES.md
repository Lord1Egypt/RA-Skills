# 使用示例

## 示例 1：含标题的文档

### 输入图片内容
```
第一章 项目概述
1.1 项目背景
本项目旨在开发一个智能系统
用于自动化文档处理
1.2 项目目标
提高文档处理效率
(1) 减少人工操作
(2) 提高准确性
```

### 输出代码
```php
$word->title1("第一章 项目概述");
$word->title2("1.1 项目背景");
$word->body("正文=本项目旨在开发一个智能系统=".$F);
$word->body("正文=用于自动化文档处理=".$F);
$word->title2("1.2 项目目标");
$word->body("正文=提高文档处理效率=".$F);
$word->title2("(1) 减少人工操作");
$word->title2("(2) 提高准确性");
```

---

## 示例 2：多级标题

### 输入图片内容
```
第一部分 总则
一、指导思想
1.1 基本原则
(1) 市场导向
(2) 创新驱动
1.2 发展目标
二、主要任务
```

### 输出代码
```php
$word->title1("第一部分 总则");
$word->title1("一、指导思想");
$word->title2("1.1 基本原则");
$word->title2("(1) 市场导向");
$word->title2("(2) 创新驱动");
$word->title2("1.2 发展目标");
$word->title1("二、主要任务");
```

---

## 示例 3：三级标题

### 输入图片内容
```
第三章 技术方案
3.1 技术路线
3.1.1 前端架构
3.1.2 后端架构
3.2 实施步骤
1、需求分析
2、系统设计
```

### 输出代码
```php
$word->title1("第三章 技术方案");
$word->title2("3.1 技术路线");
$word->title3("3.1.1 前端架构");
$word->title3("3.1.2 后端架构");
$word->title2("3.2 实施步骤");
$word->title3("1、需求分析");
$word->title3("2、系统设计");
```

---

## 示例 2：含数学公式

### 输入图片内容
```
质能方程
E = mc²
其中：
E - 能量
m - 质量
c - 光速 (3×10^8 m/s)
```

### 输出代码
```php
$word->body("正文=质能方程=".$F);
$word->formula("E = mc^2");
$word->body("正文=其中：=".$F);
$word->body("正文=E - 能量=".$F);
$word->body("正文=m - 质量=".$F);
$word->body("正文=c - 光速 (3×10^8 m/s)=".$F);
```

---

## 示例 3：含复杂公式

### 输入图片内容
```
高斯积分公式
∫_{-∞}^{∞} e^{-x²} dx = √π

证明：
令 I = ∫_{-∞}^{∞} e^{-x²} dx
则 I² = (∫_{-∞}^{∞} e^{-x²} dx)(∫_{-∞}^{∞} e^{-y²} dy)
```

### 输出代码
```php
$word->body("正文=高斯积分公式=".$F);
$word->formula("\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}");
$word->body("正文=证明：=".$F);
$word->body("正文=令 I = ∫_{-∞}^{∞} e^{-x²} dx=".$F);
$word->body("正文=则 I² = (∫_{-∞}^{∞} e^{-x²} dx)(∫_{-∞}^{∞} e^{-y²} dy)=".$F);
```

---

## 示例 4：含图表

### 输入图片内容
```
2024 年销售数据
[柱状图：Q1-Q4 销售额对比]
结论：
Q4 销售额最高
同比增长 25%
```

### 输出代码
```php
$word->body("正文=2024 年销售数据=".$F);
![image]
$word->body("正文=结论：=".$F);
$word->body("正文=Q4 销售额最高=".$F);
$word->body("正文=同比增长 25%=".$F);
```

---

## 示例 5：混合内容

### 输入图片内容
```
第三章 物理公式
3.1 牛顿第二定律
F = ma
力的单位：牛顿 (N)

3.2 万有引力
F = G(m₁m₂)/r²
其中 G 为引力常数
```

### 输出代码
```php
$word->body("正文=第三章 物理公式=".$F);
$word->body("正文=3.1 牛顿第二定律=".$F);
$word->formula("F = ma");
$word->body("正文=力的单位：牛顿 (N)=".$F);
$word->body("正文=3.2 万有引力=".$F);
$word->formula("F = G\frac{m_1 m_2}{r^2}");
$word->body("正文=其中 G 为引力常数=".$F);
```

---

## 命令行示例

```bash
# 基本用法
python3 image_to_code.py document.png

# 保存到文件
python3 image_to_code.py document.png output.txt

# 使用英文 OCR
python3 image_to_code.py english_doc.png -l en

# 使用视觉 AI（更准确的公式识别）
python3 image_to_code.py complex_formula.png --vision-ai

# 查看帮助
python3 image_to_code.py --help
```

---

## 批处理示例

```bash
#!/bin/bash
# 批量转换当前目录所有 PNG 文件

for file in *.png; do
    output="${file%.png}.txt"
    echo "处理：$file -> $output"
    python3 image_to_code.py "$file" "$output"
done

echo "批量处理完成！"
```

---

## 输出格式说明

| 元素类型 | 格式模板 | 说明 |
|----------|----------|------|
| 文字行 | `$word->body("正文=内容=".$F);` | 普通文本段落 |
| 公式 | `$word->formula("LaTeX");` | 数学公式（LaTeX 格式） |
| 图片 | `![image]` | 图表、流程图等 |
| 空行 | (空行) | 保持段落间距 |

---

## 特殊字符转义

| 原始字符 | 转义后 | 示例 |
|----------|--------|------|
| `"` | `\"` | `正文=\"引用内容\"` |
| `\` | `\\` | `公式=\\frac{a}{b}` |
| `$` | `\$` | `价格=\$100` |

---

## 常见问题

### Q: 公式识别不准确怎么办？
A: 可以尝试以下方法：
1. 使用 `--vision-ai` 参数（需配置视觉 AI API）
2. 手动校对输出的 LaTeX 公式
3. 提高图片清晰度

### Q: 中文识别有乱码？
A: 确保：
1. 使用 `-l ch` 参数指定中文 OCR
2. 输出文件使用 UTF-8 编码

### Q: 如何调整输出格式？
A: 修改 `image_to_code.py` 中的 `convert_line()` 函数

---

*更多示例请参考 SKILL.md 文档* 🐘
