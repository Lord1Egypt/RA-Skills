---
name: local-material-batch
description: 通过收件箱、dry-run、运行和清单输出流程，把已下载到本地的视频、音频、图片和文本笔记转换成可复用文本资产。适用于用户想要一个本地优先、不中台抓取的平台无关素材 intake 流程。
---

# 本地素材批处理

当用户已经有本地素材文件，希望把它们转成可复用文本资产时，就用这个技能。

这个技能不会抓平台、不会绕风控，也不会直接发布内容。它只从用户已经拥有的文件开始。

## 支持的输入

- 音频或视频文件。
- 图片或截图文件夹。
- Markdown 或纯文本文件。

## 默认目录结构

```text
local-material-batch/
  Inbox/
  outputs/
  work/
  scripts/
```

## 工作流

1. 把素材放进 `Inbox/`。
2. 先跑 dry-run 看队列。
3. 先处理一小批。
4. 每个条目写一个输出目录。
5. 写出 `outputs/manifest.json` 和 `outputs/summary.csv`。
6. 把生成的 `text.md` 接到下一步内容工作流里。

## 后端策略

后端必须可替换。

可用以下方式之一：

- 对 `.md` 和 `.txt` 直接本地复制文本
- 图片可选 OCR 后端
- 音频或视频可选 ASR 后端

如果 OCR 或 ASR 后端没接上，就在清单里把该条目标成失败，而不是假装成功。

## 输出约定

每个处理后的条目应生成：

```text
outputs/items/<item_id>/
  text.md
  text.json
```

整批处理应生成：

```text
outputs/manifest.json
outputs/summary.csv
```

## 规则

- 不抓账号内容，也不抓平台内容。
- 不要在没有 dry-run 的情况下直接处理完整个收件箱。
- 不要隐藏失败项。
- 除非用户明确要求 `--force`，否则不要覆盖已有输出。
- 同一种后端失败连续出现两次后，先停下来诊断。
