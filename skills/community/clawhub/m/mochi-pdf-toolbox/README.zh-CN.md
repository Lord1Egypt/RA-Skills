# PDF 文件工具箱

[English](README.md)

合并、拆分、选页、排序、旋转和压缩 PDF，支持图片转 PDF、页面预览及空白页检查。

## 功能

合并、拆分、选页、排序、旋转和压缩 PDF，支持图片转 PDF、页面预览及空白页检查。

## 用法示例

安装后，把下面任意一条发给 AI；涉及文件或网址时，一并提供。

```text
把我上传的两份PDF按上传顺序合并，生成新PDF和页面预览。
```

```text
从这份PDF提取第2至5页，把第3页顺时针旋转90度，另存一份。
```

```text
把这些图片按文件名排序转成PDF，检查空白页并列出结果。
```

输出 PDF 或页面图片、处理清单和预览；多文件结果附 ZIP，原文件保留。

## 运行要求

OpenClaw、已连接模型、当前工作区读写权限；Python 3.10+, pypdf 6.10+, pypdfium2 5.14+, Pillow 12.3+

## 安装与开始使用

### MochiLab Skills 助手（推荐）

[首次安装并连接助手](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)，然后发送：

```text
安装 mochi-pdf-toolbox
```

### ClawHub

[打开 Skill 页面](https://clawhub.ai/hznetnewpower/skills/mochi-pdf-toolbox)，或在当前助手工作区执行：

```text
npx clawhub@latest install @hznetnewpower/mochi-pdf-toolbox
```

### GitHub

[打开源码目录](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-pdf-toolbox)。下载仓库 ZIP，将 `skills/mochi-pdf-toolbox` 放入当前助手工作区的 `skills/` 目录。

安装后新建对话。

## 详细操作说明

[查看技能操作契约](SKILL.md)。命令、字段名和文件路径保留原样；按当前助手工作区执行，先核对依赖，再检查实际输出。
