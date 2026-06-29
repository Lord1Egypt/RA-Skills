---
name: pptx-batch-fix
description: >
  PPT/PPTX 批量格式化修复工具，涵盖两大核心能力：(1) 字号统一修复 — 全片扫描文字字号，低于阈值的统一调至16pt（可配置），自动启用换行防止溢出，修正超出版面边界的形状；(2) 页码批量删除 — 多格式页码检测与删除（X/Y、纯数字、幻灯片编号占位符），不误删章节标记。
  触发场景：修改PPT字号/调整字体大小/确保不低于16号字；删除页码/去页码/去掉页数；批量PPT格式化/修复PPT排版。
  触发词：字号修复、调整字号、不低于16号字、字体太小、删除页码、去页码、PPT批量处理、修复PPT。
---
# PPTX 批量格式化修复技能

## 功能概览

| 功能 | 脚本 | 说明 |
|------|------|------|
| 字号统一修复 | `scripts/fix_fonts.py` | 扫描全片，<阈值的 run 调至目标字号，启用 word_wrap，修正边界溢出 |
| 页码格式检测 | `scripts/detect_pagenum.py` | 扫描 X/Y、纯数字、幻灯片编号占位符三种页码 |
| 页码批量删除 | `scripts/remove_pagenum.py` | 三步清理：X/Y 格式 → 布局占位符 → 右下角纯数字 |

## 核心原则

1. **只改格式，不动内容** — `run.font.size` 修改，`run.text` 绝不触碰
2. **非破坏性操作** — 始终先输出到工作区，确认后再覆盖原文件
3. **阈值保持层级差异** — 仅调整低于阈值的字号，原本更大的保持不动
4. **不误删页码** — 章节标记（如"01""02"）≠ 页码，位置+格式双重判断

## Python 环境

```bash
C:/Users/admin/.workbuddy/binaries/python/envs/default/Scripts/python.exe
```

已预装 `python-pptx`。若缺失，执行：

```bash
/c/Users/admin/.workbuddy/binaries/python/versions/3.13.12/python.exe -m pip install --target /c/Users/admin/WorkBuddy/{session}/.packages python-pptx
```

---

## 工作流一：字号修复

### Step 1 — 确认需求

询问用户：
- 目标字号（默认 16pt）
- 涉及文件路径
- 是否需要同时检测页码

### Step 2 — 执行修复

```bash
C:/Users/admin/.workbuddy/binaries/python/envs/default/Scripts/python.exe \
  scripts/fix_fonts.py <输入pptx> <输出pptx> [--min-size 16]
```

脚本自动完成：
- `run.font.size < Pt(min_size)` → 设为 `Pt(min_size)`
- 启用 `text_frame.word_wrap = True`
- 修正超出幻灯片边界的形状（宽度/高度约束）

### Step 3 — 验证

修复后逐页校验：
1. 所有 `run.font.size` ≥ `Pt(min_size)`
2. 所有形状 `left + width <= slide_width` 且 `top + height <= slide_height`

验证通过后覆盖桌面原文件。

### 注意事项

- 文本框架的 `auto_size` 在修复后可能失效，因 PPT 渲染引擎会重新计算
- 若部分文本框在修复后文字被截断，需手动微调（约 5% 概率）
- 含有大量嵌入表格的幻灯片，字号修复需单独处理表格单元格

---

## 工作流二：页码删除

### Step 1 — 检测页码

```bash
C:/Users/admin/.workbuddy/binaries/python/envs/default/Scripts/python.exe \
  scripts/detect_pagenum.py <pptx路径>
```

输出：页码格式、所在页面、形状名称、位置坐标、布局占位符信息。

### Step 2 — 执行删除

```bash
C:/Users/admin/.workbuddy/binaries/python/envs/default/Scripts/python.exe \
  scripts/remove_pagenum.py <输入pptx> <输出pptx>
```

安全策略：先输出到工作区，确认无误后覆盖。

### 页码格式与判断规则

| 格式 | 示例 | 判断条件 | 处理方式 |
|------|------|----------|----------|
| X/Y | `1/100`, `2/100` | 正则 `^\d{1,3}\s*/\s*\d{1,4}$` | 删除形状 |
| 纯数字（右下角） | `1`, `2` | `left > W*0.55` 且 `top > H*0.70` | 删除形状 |
| 幻灯片编号占位符 | 母版/布局中的 SLIDE_NUMBER | `placeholder_format.type == 13` | 从布局中删除 |

**不删除的情况**：
- 章节编号（通常位于左上角或内容区，非右下角）
- 内容中的数字（如"2026年""第3章"）
- 非纯数字的文本（如"Page 1"）

---

## 批量处理

当用户提供多个文件时：
1. 逐个执行修复/删除脚本
2. 全部完成后汇总结果
3. 提示用户确认，再统一覆盖

## 错误处理

| 错误 | 处理 |
|------|------|
| 文件被占用 (PermissionError) | 提示关闭 PowerPoint/WPS，换临时路径输出 |
| 未检测到页码 | 用 detect_pagenum.py 全面扫描；或请用户截图说明页码样式 |
| python-pptx 缺失 | 按上方 Python 环境说明安装 |
| 字号修复后文字溢出 | 微调对应文本框宽度，或提示用户手动调整 |
