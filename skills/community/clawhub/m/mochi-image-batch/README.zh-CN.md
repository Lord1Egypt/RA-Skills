# 批量图片处理

[English](README.md)

批量缩放、裁切、留白、压缩、转格式和加水印，输出预览图与图片下载包。

## 功能

批量缩放、裁切、留白、压缩、转格式和加水印，输出预览图与图片下载包。

## 用法示例

安装后，把下面任意一条发给 AI；涉及文件或网址时，一并提供。

```text
把我指定目录的图片缩小到最长边1200像素，保持比例，另存到新目录。
```

```text
把这批图片统一转换成WebP，保留透明背景，生成处理清单。
```

```text
给这些商品图添加我提供的文字水印，先生成两张预览，确认后批量处理。
```

输出处理后的图片、预览图、清单和 ZIP，原图保留。

## 运行要求

OpenClaw、已连接模型、当前工作区读写权限；Python 3.10+, Pillow 12.3+

## 安装与开始使用

### MochiLab Skills 助手（推荐）

[首次安装并连接助手](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)，然后发送：

```text
安装 mochi-image-batch
```

### ClawHub

[打开 Skill 页面](https://clawhub.ai/hznetnewpower/skills/mochi-image-batch)，或在当前助手工作区执行：

```text
npx clawhub@latest install @hznetnewpower/mochi-image-batch
```

### GitHub

[打开源码目录](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-image-batch)。下载仓库 ZIP，将 `skills/mochi-image-batch` 放入当前助手工作区的 `skills/` 目录。

安装后新建对话。

## 详细操作说明

[查看技能操作契约](SKILL.md)。命令、字段名和文件路径保留原样；按当前助手工作区执行，先核对依赖，再检查实际输出。
