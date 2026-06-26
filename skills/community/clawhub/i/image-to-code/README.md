# image-to-code

图片转代码格式转换器 - 将图片中的文字、公式、图表转换为指定代码格式

## 安装

```bash
# 进入技能目录
cd ~/.openclaw/workspace/skills/image-to-code

# 安装依赖
pip install -r requirements.txt
```

## 依赖

- paddlepaddle (OCR 引擎)
- paddleocr (中文 OCR)
- opencv-python (图像处理)
- numpy
- Pillow

## 用法

### 基本用法

```bash
# 转换单张图片（输出到终端）
python image_to_code.py input.png

# 转换并保存到文件
python image_to_code.py input.png output.txt

# 指定 OCR 语言（英文）
python image_to_code.py input.png -l en
```

### 输出格式

```php
// 文字行
$word->body("正文=第一章 项目概述=".$F);

// 公式
$word->formula("E = mc^2");

// 图片
![image]
```

## 示例

### 输入图片内容
```
能量方程
E = mc²
其中 m 为质量，c 为光速
```

### 输出代码
```php
$word->body("正文=能量方程=".$F);
$word->formula("E = mc^2");
$word->body("正文=其中 m 为质量，c 为光速=".$F);
```

## 配置

编辑 `config.json` 自定义设置：

```json
{
  "ocr_engine": "paddleocr",
  "ocr_lang": "ch",
  "formula_detection": "auto",
  "output": {
    "encoding": "utf-8",
    "line_ending": "\n"
  }
}
```

## 注意事项

1. 图片应清晰（建议 300dpi 以上）
2. 复杂公式可能需要人工校对
3. 暂不支持手写文字识别

## 故障排除

### OCR 识别不准确
- 确保图片清晰
- 调整图片对比度
- 尝试使用视觉 AI 模式（需配置 API）

### 公式识别错误
- 复杂公式使用 `--vision-ai` 参数
- 手动校对 LaTeX 输出

## License

MIT
