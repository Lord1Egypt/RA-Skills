# image-to-code 技能 - 使用指南

## 📋 技能概述

将图片（含文字、公式、标题）转换为指定的代码格式，使用 Tesseract OCR 引擎进行文字识别。

**特点**：
- ✅ 免费开源，无需 API Key
- ✅ 离线运行，保护隐私
- ✅ 自动识别标题级别
- ✅ 自动提取标题文本（去掉编号）
- ⚠️ 中文识别准确率约 70-80%

---

## 🚀 快速开始

### 1. 安装依赖

```bash
# 安装 Tesseract OCR 引擎
yum install -y tesseract tesseract-langpack-chi_sim tesseract-langpack-eng

# 安装 Python 依赖
pip install pytesseract opencv-python-headless numpy Pillow
```

### 2. 使用技能

```bash
# 基本用法
python3 image_to_code.py input.png

# 转换并保存
python3 image_to_code.py input.png output.txt

# 批量处理
for file in *.png; do
    python3 image_to_code.py "$file" "${file%.png}.txt"
done
```

---

## 📝 输出格式

### 标题格式

| 输入 | 输出 |
|------|------|
| `第一章 总述` | `$word->title1("总述");` |
| `第一部分 总则` | `$word->title1("总则");` |
| `一、项目背景` | `$word->title1("项目背景");` |
| `1.1 项目背景` | `$word->title2("项目背景");` |
| `第一节 技术方案` | `$word->title2("技术方案");` |
| `(1) 减少成本` | `$word->title2("减少成本");` |
| `（一）战略规划` | `$word->title2("战略规划");` |
| `1.1.1 前端架构` | `$word->title3("前端架构");` |
| `1、需求分析` | `$word->title3("需求分析");` |

### 文字格式

```
输入：这是正文内容
输出：$word->body("正文=这是正文内容=".$F);
```

### 公式格式

```
输入：E = mc²
输出：$word->formula("E = mc^2");
```

### 图片格式

```
输入：[图表]
输出：![image]
```

---

## 🎯 最佳实践

### 1. 图片质量要求

- **分辨率**: 建议 300dpi 以上
- **尺寸**: 宽度至少 1200px
- **格式**: PNG（无损压缩）> JPG
- **对比度**: 文字清晰，背景干净

### 2. 拍摄/截图技巧

✅ **推荐**：
- 使用扫描仪或扫描 APP
- 截图保存为 PNG 格式
- 保证文字水平对齐
- 充足的光线

❌ **避免**：
- 手机拍照（透视畸变）
- 低分辨率截图
- 倾斜角度拍摄
- 阴影遮挡文字

### 3. 识别优化

**如果识别效果不好，尝试：**

```bash
# 1. 调整图片对比度
convert input.png -contrast-stretch 2%x1% enhanced.png
python3 image_to_code.py enhanced.png

# 2. 放大图片
convert input.png -resize 200% enlarged.png
python3 image_to_code.py enlarged.png

# 3. 转换为灰度图
convert input.png -colorspace Gray gray.png
python3 image_to_code.py gray.png
```

---

## ⚙️ 配置选项

### 修改 image_to_code.py

```python
# 调整 OCR 配置
config = '--oem 3 --psm 6 -l chi_sim+eng'

# 参数说明：
# --oem 3: 使用 LSTM + Legacy 引擎
# --psm 6: 假设是统一文本块
# -l chi_sim+eng: 简体中文 + 英文

# 其他常用配置：
# --psm 3: 自动页面分割
# --psm 4: 假设是单列文本
# --psm 11: 稀疏文本
```

---

## 🔧 故障排除

### 问题 1：中文识别有空格

**现象**：`核 算 压 力 降`

**解决**：技能已内置空格清理功能，会自动移除中文字符间的空格。

### 问题 2：标题被分割成多行

**现象**：`(2)` 和 `核算压力降` 分成两行

**解决**：
1. 提高图片分辨率
2. 使用 `--psm 4` 配置
3. 手动合并输出结果

### 问题 3：公式识别不准确

**现象**：`24p` 识别为 `zap`

**解决**：
1. 公式部分手动校对
2. 使用视觉 AI 辅助识别
3. 截图时保证公式清晰

### 问题 4：Tesseract 无法启动

**错误**：`tesseract is not installed`

**解决**：
```bash
# 检查安装
which tesseract
tesseract --version

# 重新安装
yum install -y tesseract tesseract-langpack-chi_sim
```

---

## 📊 性能基准

### 测试环境
- **CPU**: Intel Xeon
- **内存**: 2GB
- **Tesseract**: 5.3.2
- **图片**: 980x376 PNG

### 识别速度
- **小图片** (<1MB): ~2-3 秒
- **中图片** (1-5MB): ~5-8 秒
- **大图片** (>5MB): ~10-15 秒

### 识别准确率
- **清晰截图**: 85-90%
- **普通扫描**: 75-85%
- **手机拍照**: 60-70%

---

## 💡 使用技巧

### 技巧 1：批量转换

```bash
#!/bin/bash
# batch_convert.sh

input_dir="$1"
output_dir="$2"

mkdir -p "$output_dir"

for file in "$input_dir"/*.png; do
    filename=$(basename "$file" .png)
    echo "处理：$filename"
    python3 image_to_code.py "$file" "$output_dir/$filename.txt"
done

echo "批量转换完成！"
```

### 技巧 2：后处理校对

```python
# post_process.py
import re

def fix_common_errors(text):
    """修复常见 OCR 错误"""
    corrections = {
        ' zap ': ' 24p ',
        ' QD ': ' OD ',
        ' am ': ' an ',
        # 添加更多纠正规则
    }
    
    for wrong, correct in corrections.items():
        text = text.replace(wrong, correct)
    
    return text

# 使用
with open('output.txt', 'r') as f:
    content = f.read()

fixed = fix_common_errors(content)

with open('output_fixed.txt', 'w') as f:
    f.write(fixed)
```

### 技巧 3：增量转换

对于大文档，分页面转换：

```bash
# 转换第 1-10 页
for i in {1..10}; do
    python3 image_to_code.py page_$i.png page_$i.txt
done

# 合并结果
cat page_*.txt > full_document.txt
```

---

## 📚 示例

### 完整示例

**输入图片**：`document.png`
```
第一章 项目概述
1.1 项目背景
本项目旨在开发智能系统
(1) 提高效率
(2) 减少错误
1.2 技术方案
1.2.1 前端设计
```

**执行命令**：
```bash
python3 image_to_code.py document.png output.txt
```

**输出结果**：
```php
$word->title1("项目概述");
$word->title2("项目背景");
$word->body("正文=本项目旨在开发智能系统=".$F);
$word->title2("提高效率");
$word->title2("减少错误");
$word->title2("技术方案");
$word->title3("前端设计");
```

---

## 🆚 与其他方案对比

| 特性 | Tesseract | 百度 OCR | 腾讯 OCR |
|------|-----------|----------|----------|
| **费用** | 免费 | 付费 | 付费 |
| **准确率** | 70-80% | 95%+ | 95%+ |
| **速度** | 中等 | 快 | 快 |
| **离线** | ✅ | ❌ | ❌ |
| **隐私** | ✅ | ❌ | ❌ |
| **配置** | 简单 | 需 API Key | 需 API Key |

---

## 📞 支持

**问题反馈**：
- 查看 TEST_REPORT.md 了解测试详情
- 检查 EXAMPLES.md 查看更多示例
- 参考 SKILL.md 了解技能规范

---

*最后更新：2026-03-07*
*版本：v1.0.0*
