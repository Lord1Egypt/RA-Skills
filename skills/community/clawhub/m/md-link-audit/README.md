# Markdown Link Auditor / Markdown 链接体检器

## English

Audit Markdown links for 404s and path drift, with CI-friendly external-link timeout handling. Zero-dependency, deterministic output (rc=0/1/2), `--json` machine-readable.

```bash
python scripts/md_link_audit.py README.md
python scripts/md_link_audit.py README.md --json
```

Use rc to set strictness: 0 clean / 1 warning / 2 bad input.

## 中文

查 README/Wiki/技术手册里的 404 与路径漂移，CI 友好的外网超时处理。零依赖，确定性输出（rc=0/1/2），`--json` 机器可读。

```bash
python scripts/md_link_audit.py README.md
python scripts/md_link_audit.py README.md --json
```

用返回码设定严格程度：0 正常 / 1 告警 / 2 输入错误。

## License

MIT
