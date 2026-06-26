---
name: md-docx
description: 这是一个用于md文件与docx文件相互转换的技能。支持Markdown转Word文档，以及Word文档转Markdown格式。
---

# Trigger
当用户提到以下关键词时：
- "md转docx"、"markdown转word"、"md to word"
- "docx转md"、"word转markdown"、"docx to md"
- "文件转换"、"格式转换"
- 用户上传了.md文件或.docx文件并请求转换

# Instructions
1. 首先，确认用户的需求是：
   - md → docx（Markdown转Word）
   - docx → md（Word转Markdown）
   - 批量转换（多个文件）

2. 然后，获取文件：
   - 如果用户已经上传了文件，确认文件路径
   - 如果用户没有上传文件，引导用户上传需要转换的文件
   - 检查文件是否存在且有读取权限

3. 执行转换：
   - 调用 `converter.py` 脚本进行转换
   - 脚本会返回转换后的文件路径
   - 如果转换失败，提供详细的错误信息

4. 结果呈现：
   - 告知用户转换成功
   - 提供下载链接或文件路径
   - 询问是否需要继续转换其他文件

5. 特殊说明：
   - 对于md转docx，会保留标题、列表、表格、代码块等格式
   - 对于docx转md，会尽可能保留原有格式结构
   - 如果文件包含图片，确保图片能正确转换

# Environment Variables
- OUTPUT_DIR: 输出目录，默认为当前目录下的 `converted/` 文件夹
- CONVERSION_MODE: 转换模式，可选项为 "standard"(标准) 或 "strict"(严格)，默认为 "standard"
- KEEP_IMAGES: 是否保留图片，默认为 true

# Tools Required
- python_executor
- file_reader
- file_writer
- path_validator
- memory_read
- memory_write

# Examples

## 示例1：MD转DOCX
用户：帮我把这个README.md文件转成Word文档
AI：好的，我将为您把README.md转换为Word文档。
[执行转换后]
AI：转换完成！已生成README.docx文件，您可以点击这里下载。文件保持了原有的标题、列表和代码块格式。

## 示例2：DOCX转MD
用户：我有一个论文.docx需要转成markdown格式
AI：收到，我将为您把论文.docx转换为markdown格式。
[执行转换后]
AI：转换完成！已生成论文.md文件。所有标题格式和图片都已保留。

# Notes
- 建议文件大小不超过50MB，过大文件可能导致转换时间过长
- 转换后的文件默认保存在 `converted/` 文件夹中，并按时间戳命名避免覆盖
- 如果遇到复杂表格或特殊格式，可能会有格式调整的需求
- 技能会自动创建输出目录（如果不存在）