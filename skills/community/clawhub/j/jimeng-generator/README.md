# Jimeng Generator

Image generation powered by VolcEngine Jimeng AI 4.0.

Jimeng 4.0 combines text-to-image, image editing, and multi-image composition in a unified framework. It supports up to 10 input images, outputs up to 15 images per request, and offers smart aspect-ratio detection with 4K output.

## Setup

```bash
npm install
```

### Credentials

| Variable | Required | Description |
|----------|----------|-------------|
| `VOLCENGINE_AK` | Yes | VolcEngine Access Key |
| `VOLCENGINE_SK` | For permanent keys | VolcEngine Secret Key |
| `VOLCENGINE_TOKEN` | For STS | Security Token (temporary credentials) |

```bash
export VOLCENGINE_AK="<your-ak>"
export VOLCENGINE_SK="<your-sk>"
```

Get credentials: [VolcEngine Console](https://console.volcengine.com/) → Access Control → Key Management.

## Usage

```bash
npx ts-node scripts/generate.ts "a cute cat sitting on a windowsill"
```

The script submits the task, polls until completion, and saves images to `./output/`.

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `--images <url,...>` | Reference image URLs (comma-separated, up to 10) | — |
| `--width <n>` | Output width | auto |
| `--height <n>` | Output height | auto |
| `--size <n>` | Output area (e.g. `4194304` = 2048×2048) | auto |
| `--scale <0-1>` | Text influence vs image influence | `0.5` |
| `--single` | Force single image output | `false` |
| `--out <dir>` | Output directory | `./output` |
| `--no-save` | Skip saving, print URLs only | `false` |
| `--interval <ms>` | Poll interval | `3000` |
| `--timeout <ms>` | Max wait time | `180000` |
| `--debug` | Debug logging | `false` |

### Examples

**Text-to-image with smart ratio:**

```bash
npx ts-node scripts/generate.ts "watercolor landscape, mountains and lake, 16:9"
```

**4K output:**

```bash
npx ts-node scripts/generate.ts "abstract art" --size 16777216
```

**Image editing (change background):**

```bash
npx ts-node scripts/generate.ts "change background to a concert stage" \
  --images "https://example.com/photo.jpg"
```

**Multiple reference images:**

```bash
npx ts-node scripts/generate.ts "combine into a group photo" \
  --images "https://a.jpg,https://b.jpg,https://c.jpg"
```

**Custom dimensions:**

```bash
npx ts-node scripts/generate.ts "cyberpunk city" --width 2560 --height 1440
```

## Output

```json
{
  "success": true,
  "taskId": "7392616336519610409",
  "prompt": "a cute cat",
  "count": 1,
  "files": ["./output/1.png"],
  "urls": ["https://..."]
}
```

Error:

```json
{
  "success": false,
  "error": {
    "code": "FAILED",
    "message": "error description"
  }
}
```

## How It Works

1. Script signs the request using HMAC-SHA256 (VolcEngine Header authentication)
2. Submits an async task to `CVSync2AsyncSubmitTask`
3. Polls `CVSync2AsyncGetResult` until status is `done`
4. Decodes base64 image data and saves as PNG files

## Project Structure

```
jimeng-generator/
├── scripts/
│   └── generate.ts      # Generator script (auth + API + CLI)
├── docs/
│   ├── jimengv4.md       # Jimeng 4.0 API reference
│   └── authorization.md  # VolcEngine auth reference
├── package.json
├── tsconfig.json
├── skill.yaml
└── _meta.json
```

## License

MIT
