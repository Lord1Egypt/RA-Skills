---
name: translator-pdf2zh
description: 用统一脚本执行 pdf2zh-next。支持单/多PDF、目录批处理、按 glob 筛选；未指定 provider 时按 config.toml 生效；指定 provider 时按官方 --<Services> 参数传给主程序；支持实时监控与并行翻译。
---

# translator-pdf2zh

## 1) 强制安全边界
1. 只允许读取 `skills/translator-pdf2zh/config.toml`（相对路径，跨电脑可识别）。
2. 禁止读取 `openclaw.json` 或任何 agent 内部配置。
3. 禁止读写全局 `~/.config/pdf2zh/config.v3.toml`。
4. 运行子进程时必须隔离 HOME/USERPROFILE/XDG_CONFIG_HOME。
5. 不做运行时 `pip install`。

## 2) 审计声明（避免误判“隐式下载”）
- 本脚本不内置外部下载逻辑。
- `pdf2zh-next/babeldoc` 首次运行可能下载模型/字体/cmap（上游行为）。

## 3) 输入能力
- `--input-file`（可重复）
- `--input-dir`（可重复）
- `--include-glob`（可重复）
- `--workers N`（并行，N>=1）
- `--visible-monitor`（实时进度）

## 4) Provider 规则
- 不传 `--provider`：完全按 `config.toml`。
- 传 `--provider`：
  - 先校验 provider 在 `config.toml` 顶层存在；
  - 再校验主程序存在官方 `--<Services>` 参数；
  - 通过后仅传官方参数。

## 5) 命令模板
```bash
python skills/translator-pdf2zh/scripts/run_pdf2zh_pipeline.py \
  --input-file "{PDF路径}" \
  --output-dir "{输出目录}" \
  --provider "{可选: openai|deepseek|siliconflow|openaicompatible|...}" \
  --config-path "skills/translator-pdf2zh/config.toml" \
  --visible-monitor \
  --workers 1
```
## 6) 帮助
- 如果Agent无法将用户的需求正确转化为pdf2zh_next主程序所能读懂的参数，Agent需要使用参数`-h`功能运行主程序，读取pdf2zh_next主程序输出的参数说明，确定参数的正确用法。或者是读取官方参考文档`https://pdf2zh-next.com/zh/advanced/advanced.html`