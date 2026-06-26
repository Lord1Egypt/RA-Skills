---
name: html_ppt_zc
description: 自动生成 PPT（或 HTML 演示） 的技能，接受标题和正文，使用 python-pptx 库快速生成 .pptx 文件，可选导出为 HTML。
metadata:
  openclaw:
    emoji: 📊
    requires:
      bins: [python]
      config: {}
---

# Guizang PPT Skill

## 功能概述
- **生成 PPT**：依据提供的标题和文本内容，自动拆分成幻灯片，每段落生成一页，支持标题页、目录页和内容页。
- **可选导出 HTML**：使用内置模板将 PPT 转换为可在浏览器直接展示的 HTML 演示文稿。
- **自定义样式**：可通过可选参数指定配色、字体大小、页眉页脚等基础样式。

## 环境依赖
- **Python**（系统已安装）。
- **python-pptx** 库：`pip install -U python-pptx`。
- **jinja2**（用于 HTML 导出，可选）：`pip install -U jinja2`。

确保上述库已安装，`python -c "import pptx"` 不会报错即表示可用。

## 使用方法（Windows CMD / PowerShell）

### 1. 生成 PPT（默认）
```bash
python "%USERPROFILE%\.openclaw\workspace\skills\guizang_ppt\generate_ppt.py" \
  --title "<演示标题>" \
  --text "<每行代表一段落的正文>" \
  --output "C:\\Path\\to\\output.pptx"
```
- `--title`：演示标题（将生成封面页）。
- `--text`：多行文字，脚本会按换行拆分为幻灯片内容，每行生成一个要点列表；若段落之间留空行，会产生新幻灯片。
- `--output`：生成的 `.pptx` 文件路径。

### 2. 导出 HTML 演示
```bash
python "%USERPROFILE%\.openclaw\workspace\skills\guizang_ppt\generate_ppt.py" \
  --title "<演示标题>" \
  --text "<正文>" \
  --output "C:\\Path\\to\\output.html" \
  --html
```
添加 `--html` 参数将把 PPT 转为 HTML（使用简易模板），便于在浏览器直接查看。

## 常见问题
- **缺少 python-pptx**：运行 `pip install -U python-pptx` 安装。
- **生成的 PPT 打不开**：确保 `--output` 路径所在的文件夹已存在且有写入权限。
- **文本过长**：脚本会自动换行，若单行文字超过幻灯片可容纳宽度，会自动换行为多个要点。

## 注意事项
- 本技能仅用于个人学习、内部汇报等合法场景，生成的 PPT 如需对外发布，请自行确认内容版权。
- 若需要更高级的动画、模板或图表，请在生成的 PPT 基础上手动编辑。
