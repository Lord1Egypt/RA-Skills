---
name: jiege-imgen
slug: jiege-imgen-user-e866c542
displayName: 杰哥生图
version: 1.0.0
summary: 使用兼容 OpenAI Images API 的网关生成、编辑并接入项目图片素材。
description: 使用兼容 OpenAI Images API 的网关生成、编辑和落地项目图片素材。用户要求生图、画图、改图、修图、换风格、扩图、去背景、抠图，或需要 Logo、应用图标、Banner、封面、插图、背景图、空状态图、宣传图和产品视觉素材时使用；有参考图时必须保留并编辑参考图，无参考图时生成新图。
---

# 杰哥生图

## 目标

把图片需求直接变成项目中可复用的图像文件。单张图片生成、参考图编辑和明确的局部视觉素材请求直接执行，不进入产品需求澄清流程。

## 执行流程

1. 明确主体、用途、构图、风格、画面比例和输出路径；提示词要具体描述必须保留或必须修改的内容。
2. 无参考图时使用 `scripts/generate_image.py` 调用 `/images/generations`；有参考图时传入 `--input-image`，调用标准 multipart `/images/edits`。
3. 默认把结果保存到项目目录：Web 使用 `public/images/`，小程序使用 `miniprogram/assets/images/`，演示材料使用 `docs/images/`。
4. 如果图片用于当前项目，生成后将文件接入实际页面或素材引用；不要只返回提示词，也不要生成页面不使用的装饰图。
5. 运行脚本完成后检查输出文件存在且非空，并报告实际路径、调用路由和失败时的最后错误。

## 快速用法

生成新图：

```bash
python3 scripts/generate_image.py \
  --prompt "清晰描述主体、用途、构图、风格和画面比例" \
  --size 1536x1024 \
  --quality high \
  --output ./public/images/banner.png
```

编辑参考图：

```bash
python3 scripts/generate_image.py \
  --input-image ./source.png \
  --prompt "保留主体构图，改为科幻风格" \
  --size 1024x1024 \
  --quality high \
  --output ./public/images/scifi.png
```

提示词较长时可使用 `--prompt-file ./image-prompt.txt` 替代 `--prompt`。

## 接口与安全约束

- 生图优先且必须使用 Images API 的 `POST /images/generations`；不要改用 Responses API。参考图编辑使用 `POST /images/edits`。
- 默认 API 基址为 `https://token.minapp.xin/v1`，模型为 `gpt-image-2`；使用 `--base-url` 或 `OPENAI_BASE_URL` 覆盖。
- 仅从环境变量 `OPENAI_API_KEY` 读取密钥；也可由用户主动传入 `--auth-file` 指定本地 JSON 文件。默认不会读取任何 Codex 配置文件。
- 每个请求默认最多重试 2 次并指数退避；不得无限重试，也不得因单次超时立即放弃。
- 不得把密钥写入代码、提示词文件、日志、前端文件或最终交付物。
- 生成接口和编辑接口均失败时，报告最后错误及已尝试的接口，不私自切换模型、地址或其他生图服务。
- 产品界面仍使用 DaisyUI 等真实交互组件；不要用图片替代按钮、表单或其他可交互界面。

## 脚本约定

`scripts/generate_image.py` 是可执行的无第三方依赖 Python 脚本，负责认证读取、JSON 或 multipart 请求、图片响应解析、URL 下载、有限重试和 PNG 落盘。保持生成与编辑两个路由的区别，修改脚本后至少运行：

```bash
python3 -m py_compile scripts/generate_image.py
python3 scripts/generate_image.py --help
```
