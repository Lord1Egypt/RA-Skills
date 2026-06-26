# OCR 参数与技巧

- **DPI（分辨率）**：默认 300 DPI 足够中文 OCR，若原始扫描分辨率低于 200，建议先用 `pdf2image` 提升 DPI 再 OCR。
- **语言模型**：`-l chi_sim`（简体中文）或 `-l chi_tra`（繁体中文），可一次指定多个语言，如 `-l chi_sim+eng`。
- **快速模式**：`--skip-text` 可跳过已有文字层的 PDF，避免重复 OCR，适合批处理。
- **图片预处理**：若扫描噪点多，可使用 `--clean` 或 `--deskew` 参数让文字更清晰。
- **错误日志**：ocrmypdf 会把错误写入 STDERR，建议在脚本中捕获并写入 `logs/pdf_ocr_error.log`，如本技能所示。
- **并行**：`ocrmypdf` 本身不支持并行，但可以在脚本外层使用 `xargs -P` 或 PowerShell 并行调用实现多文件并发处理。

以上技巧可在 `ocr_batch.py` 中通过 `--lang`、`--skip-text`、`--clean` 等参数自行扩展。
