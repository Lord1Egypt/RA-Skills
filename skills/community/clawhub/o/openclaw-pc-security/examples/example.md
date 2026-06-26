# Example / 示例

## Local audit only / 仅本机审计
```bash
python src/main.py --audit --npm-view-latest-openclaw --out-dir openclaw-pc-security/output
```

## Scan local OpenClaw / 扫描本机 OpenClaw（授权环境）
```bash
python src/main.py 127.0.0.1 --ports 18789,18790,18792 --out-dir openclaw-pc-security/output
```
