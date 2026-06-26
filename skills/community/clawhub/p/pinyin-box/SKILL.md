---
name: pinyin-box
description: |
  汉字小助手 - 将文字或图片中的文字转换为拼音格或米字格练习纸。
  当用户需要：(1) 把文字转换成练字帖或米字格，(2) 提取图片中的文字并生成拼音格，
  (3) 生成汉字书写练习材料，(4) 把任何内容做成拼音格或米字格格式时，使用此 Skill。
  支持文字输入、图片 OCR 识别，输出 PNG 或 PDF 格式。
---

# 汉字小助手

将用户提供的文字或图片中的文字，转换为带拼音的标准拼音格练习纸。

## 环境准备

在使用本 Skill 前，需要先安装依赖：

### 使用 pip 安装

```bash
cd ~/.openclaw/workspace/skills/pinyin-box
pip install -r requirements.txt
```

### 使用 uv 安装

```bash
cd ~/.openclaw/workspace/skills/pinyin-box
# 创建虚拟环境
uv venv
# 激活虚拟环境
source .venv/bin/activate
# 安装依赖
uv pip install -r requirements.txt
```

## 工作流程

1. **接收输入**
   - 用户直接发送文字
   - 用户发送包含文字的图片

2. **提取文字**
   - 如果是图片：使用 image 工具识别其中的文字内容
   - 如果是文字：直接使用

3. **格式化文本**
   - 去除无关内容（如页眉页脚、状态栏、时间等）
   - 保留核心文字内容
   - 适当分段，每行不要太长

4. **生成拼音格**
   - 调用 pinyin-box CLI 工具生成练习纸
   - 默认使用 medium 尺寸
   - 输出 PNG 格式（也可按需求输出 PDF）

5. **发送结果**
   - 返回生成的图片文件
   - 告知用户文件路径和基本信息（字数、页数）

## 使用工具

### 图片文字识别
```python
# 使用 image 工具分析图片中的文字
image(image_path, prompt="请识别这张图片中的中文文字内容，完整提取出来")
```

### 生成拼音格
```bash
# 基本命令
pinyin-box -t "文本内容" -s medium -o ~/.openclaw/workspace/pinyin-box/output/pinyin_img1.png

# 参数说明
# -t: 文本内容（支持 \n 换行）
# -s: 尺寸 small/medium/large
# -o: 输出路径
# --tone-color: 声调着色
# --no-pinyin: 不显示拼音
```

> 💡 提示：可以使用 `pinyin-box --help` 查看完整的命令参数说明。

## 输出路径

所有生成的文件默认保存在：

```~/.openclaw/workspace/pinyin-box/output/```

## 示例场景

### 场景1：用户发送文字
用户："帮我把这段话做成练字帖：床前明月光"
→ 直接提取文字，生成拼音格

### 场景2：用户发送图片
用户：发送一张包含文字的图片
→ 识别图片文字，格式化后生成拼音格

### 场景3：生成 PDF 打印版
用户："生成 PDF 格式方便打印"
→ 使用 .pdf 扩展名输出

### 场景4：大字版书法练习
用户："要大字版的"
→ 使用 -s large 参数

## 注意事项

- 自动过滤图片中的 UI 元素（时间、电量、导航栏等）
- 文本较长时会自动分页，无需担心
- 默认输出 PNG，如需 PDF 请根据用户需求指定
- 生成完成后告知用户字数和页数
- 使用相对路径 MEDIA:./filename.png 发送图片
