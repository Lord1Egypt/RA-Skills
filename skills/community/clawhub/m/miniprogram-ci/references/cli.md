# CLI Command Reference

## Global Options

```bash
miniprogram-ci <command> [options]
```

## Common Options

| Param | Full Name | Required | Description |
|-------|-----------|----------|-------------|
| `--pp` | `--project-path` | ✅ | Project path |
| `--pkp` | `--private-key-path` | ✅ | Private key path |
| `--appid` | `--appid` | ✅ | Mini program appid |
| `--type` | `--project-type` | ❌ | Project type, defaults to miniProgram |
| `--uv` | `--upload-version` | ❌ | Custom version number |
| `--ud` | `--upload-desc` | ❌ | Custom description |
| `--r` | `--robot` | ❌ | CI robot number (1-30) |
| `--proxy` | `--proxy` | ❌ | Proxy address |

## upload Command

```bash
miniprogram-ci upload \
  --pp ./miniprogram \
  --pkp ./private.key \
  --appid wx0000000000000000 \
  --uv 1.0.0 \
  --ud "Version description" \
  --r 1
```

## preview Command

```bash
miniprogram-ci preview \
  --pp ./miniprogram \
  --pkp ./private.key \
  --appid wx0000000000000000 \
  --uv 1.0.0 \
  --ud "Preview description" \
  --qrcode-format image \
  --qrcode-output-dest ./preview.jpg \
  --page-path "pages/index/index" \
  --search-query "id=123"
```

preview-specific options:

| Param | Description |
|-------|-------------|
| `--qrcode-format` | QR code format: image / base64 / terminal (default) |
| `--qrcode-output-dest` | QR code save path (required) |
| `--page-path` | Preview page path |
| `--search-query` | Page launch parameters |
| `--scene` | Scene value, default 1011 |

## Compile Settings via CLI

Pass through `--setting-xxx` parameters:

```bash
miniprogram-ci upload \
  --pp ./miniprogram \
  --pkp ./private.key \
  --appid wx0000000000000000 \
  --uv 1.0.0 \
  --setting-minify \
  --setting-es6 \
  --setting-minify-wxml \
  --setting-minify-wxss \
  --setting-es7 \
  --setting-code-protect \
  --setting-auto-prefix-wxss
```