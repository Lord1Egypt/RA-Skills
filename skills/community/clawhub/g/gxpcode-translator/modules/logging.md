# 日志模块

>  **加载触发器**：翻译完成后 MANDATORY。text 和 PDF 路径共用。

---

## 步骤 N：写日志（静默）

**N.1** 调用 `write_log.py`：

```powershell
$logInput = @{
  source_text = $sourceText
  translated_text = $translatedText
  matches = $matchData.matches
  source_type = $sourceType
  pdf_meta = $pdfMeta
} | ConvertTo-Json -Depth 10 -Compress

& $PythonExe `
  "$SkillDir\write_log.py" `
  --data $logInput
```

**N.2** 日志路径：`{output_dir}/logs/YYYY-MM-DD_HH-MM-SS_trans.md`（`output_dir` 从 `config.json` 读取）

**N.3** 日志内容包含：
- 翻译时间戳
- 原文（前 500 字符摘要 + 完整文本）
- 译文（完整）
- 命中术语列表（en → cn）
- source_type（text / pdf）
- PDF 路径及页数（如为 PDF 输入）

**N.4** 兜底校验：检查所有命中术语的目标译法（cn）是否出现在译文中 → 缺失则在日志中标注 ⚠️
