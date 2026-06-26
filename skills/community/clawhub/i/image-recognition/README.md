# Image Recognition Skill

图片识别技能 - 使用通义千问视觉模型识别图片内容

## 快速开始

### 1. 安装依赖

```bash
pip3 install requests Pillow
```

### 2. 配置 API Key（可选）

默认已配置，如需修改：

```bash
export BAILIAN_API_KEY="sk-sp-your-api-key"
```

### 3. 使用

```bash
# 识别图片
python3 recognize.py /path/to/image.jpg

# 指定问题
python3 recognize.py /path/to/image.jpg "提取图片中的所有文字"
```

## 在 OpenClaw 中集成

### 方法一：作为外部命令调用

```python
import subprocess

result = subprocess.run(
    ["python3", "~/.openclaw/skills/image-recognition/recognize.py", image_path],
    capture_output=True,
    text=True
)
print(result.stdout)
```

### 方法二：直接导入函数

```python
from recognize import recognize_image

result = recognize_image("/path/to/image.jpg")
print(result)
```

## 文件说明

- `SKILL.md` - 技能说明文档
- `recognize.py` - 主脚本
- `README.md` - 本文件
- `usage-guide.md` - 使用指南（可选）
- `examples/` - 示例（可选）

## 支持的图片格式

- JPEG/JPG
- PNG
- GIF（静态）
- WebP
- BMP

## API 端点

**正确端点：**
```
https://coding.dashscope.aliyuncs.com/v1/chat/completions
```

## 模型

- `qwen3.5-plus` - 默认，支持视觉
- `qwen-vl-max` - 专业视觉模型（需要单独开通）

## 故障排除

### API Key 无效

检查：
1. API Key 是否正确（`sk-sp-` 开头）
2. 端点是否正确（`coding.dashscope.aliyuncs.com`）
3. API Key 是否已开通视觉模型权限

### 图片太大

建议压缩到 2MB 以内，或调整分辨率。

### 识别不准确

- 确保图片清晰
- 文字不要太模糊
- 尝试调整问题提示

## 更多信息

查看 `SKILL.md` 获取完整文档。
