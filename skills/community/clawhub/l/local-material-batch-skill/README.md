# 本地素材批处理技能

这是一个本地优先的 Codex 技能和起步脚本，用来把已经下载到本地的素材转换成可复用的文本资产。

适合创作者、研究者、运营或内容团队处理一堆杂乱的本地文件，比如视频、音频、截图、图片笔记、Markdown 或纯文本，并且希望有一套可重复执行的收件箱流程。

## 能做什么

- 扫描 `Inbox/`。
- 先给出 dry-run 队列。
- 本地处理文本文件。
- 对未接入后端的图片或媒体，明确记录为待处理/失败项。
- 写出 `text.md`、`text.json`、`manifest.json` 和 `summary.csv`。

## 不能做什么

- 不抓平台内容。
- 不绕过反爬或风控。
- 不依赖某个特定云模型。
- 不直接帮你发布内容。

## 快速开始

```bash
python3 scripts/local_material_batch.py init
python3 scripts/local_material_batch.py run --dry-run
python3 scripts/local_material_batch.py run --limit 3
```

## 可选后端

这个脚本刻意保持保守。它开箱就支持 `.md` 和 `.txt`，而对需要 OCR 或 ASR 的媒体，会明确写出失败占位记录，不会假装已经处理成功。

你可以在 `scripts/local_material_batch.py` 里标出来的函数中接入自己的 OCR 或 ASR 后端。

## 运行环境

- Python 3.10+。
- 第三方依赖：当前版本无强制依赖，标准库即可运行。
- 如果要接入 OCR / ASR 后端，请在自己 fork 的脚本里替换 `scripts/local_material_batch.py` 中标出来的函数。

## 文件

- `README.md`：本文件。
- `LICENSE`：MIT 许可证。
- `SKILL.md`：技能说明。
- `scripts/local_material_batch.py`：最小可运行脚本。
- `references/output-contract.md`：输出结构说明。
- `assets/Inbox/`：示例收件箱结构。
- `assets/example-inbox/`：示例输入。
- `assets/example-output/`：示例输出。
- `assets/outputs/`：脚本一次跑出来的实际产物示例。

## 反馈与贡献

有问题或想贡献，开 Issue 即可。如果想贡献一个 OCR / ASR 后端，建议放成独立文件并在 `scripts/local_material_batch.py` 留接入点，不要把后端逻辑塞进主流程。

## 许可证

MIT。
