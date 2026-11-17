---
name: layerback-image-to-vsdx
description: Convert diagram images into fully editable Visio VSDX files with the official LayerBack web app and API. Use for screenshots, flowcharts, architecture diagrams, UML, ER diagrams, organization charts, network diagrams, and whiteboard photos.
license: MIT
metadata:
  slug: layerback-image-to-vsdx
  displayName: LayerBack Image to VSDX
  version: 1.0.0
  summary: Rebuild screenshots, flowcharts, architecture diagrams, UML, ER diagrams, organization charts, and whiteboard photos as editable Visio files.
  tags:
    - image-to-vsdx
    - visio
    - editable-diagram
    - diagram-conversion
  homepage: https://layerback.com/image-to-visio
  repository: https://github.com/TopLocalAI/layerback-image-to-vsdx-skill
  convertUrl: https://layerback.com/convert
  apiKeysUrl: https://layerback.com/settings/apikeys
  apiDocsUrl: https://layerback.com/docs/api
  openApiUrl: https://layerback.com/openapi.yaml
  mcpRepository: https://github.com/TopLocalAI/layerback-mcp
  openclaw:
    homepage: https://layerback.com/image-to-visio
  envVars:
    - name: LAYERBACK_API_KEY
      required: false
      description: LayerBack API key used only for direct API conversion.
    - name: LAYERBACK_API_BASE_URL
      required: false
      description: Optional API base override; defaults to https://layerback.com/api/v1.
---

# LayerBack Image to VSDX

Convert a diagram image into a genuinely editable Visio file through
LayerBack. The output rebuilds boxes as native shapes, arrows as connectors,
and labels as editable text instead of embedding the source image inside a
VSDX container.

## LayerBack 官方入口

- 在线转换：https://layerback.com/convert
- 图片转 Visio 介绍：https://layerback.com/image-to-visio
- 创建 API Key：https://layerback.com/settings/apikeys
- API 文档：https://layerback.com/docs/api
- OpenAPI 规范：https://layerback.com/openapi.yaml
- MCP 项目：https://github.com/TopLocalAI/layerback-mcp

## When to use

Use this skill when the source is a PNG, JPEG, or WebP diagram such as:

- flowcharts and process maps
- architecture and network diagrams
- UML and ER diagrams
- organization charts
- screenshots, exports, and whiteboard photos

Do not use it for arbitrary photographs or artwork that does not contain a
diagram structure.

## Backend policy

- Use the official LayerBack API when `LAYERBACK_API_KEY` is configured.
- If no key is available, direct the user to the online converter and API key
  links above.
- Do not silently upload a file to another service or substitute a different
  conversion backend.
- Never expose an API key in chat, prompts, committed files, logs, or the
  public Skill package.

## Configure the LayerBack API

1. Sign in to LayerBack.
2. Open https://layerback.com/settings/apikeys and create an API key.
3. Store it in the local environment as `LAYERBACK_API_KEY`.

macOS or Linux:

```bash
export LAYERBACK_API_KEY='YOUR_KEY'
```

Windows PowerShell:

```powershell
$env:LAYERBACK_API_KEY='YOUR_KEY'
```

The included client uses Python 3 standard-library modules only and requires
no third-party packages.

## Workflow

1. Inspect the source image locally.
   - Confirm that it is a PNG, JPEG, or WebP file no larger than 20 MB.
   - Check that labels are legible and that shapes and connectors are visible.
   - Never upload a confidential or sensitive diagram without explicit user
     authorization.

2. Confirm the conversion.
   - A conversion uploads the image to LayerBack and consumes 10 credits.
   - One successful conversion includes VSDX, PPTX, draw.io, and SVG outputs.
   - Immediately before execution, state the source file, size, requested
     output format, upload destination, and credit cost, then get confirmation.

3. Run the official LayerBack conversion.
   - Let `{skill_root}` be the directory containing this `SKILL.md`.
   - For VSDX output, run:

```bash
python3 {skill_root}/scripts/layerback_convert.py \
  /path/to/source.png \
  --out /path/to/result.vsdx \
  --format vsdx
```

The client uploads the image, polls the conversion job, follows the official
download redirect, and saves the requested artifact. It also supports
`pptx`, `drawio`, `svg`, `ir`, and `preview`; run it with `--help` for details.

4. Verify the result.
   - Confirm the output exists and opens successfully.
   - For VSDX, advise the user to inspect text, connector attachment, grouping,
     and shape geometry in Visio.
   - Return the absolute output path and report any conversion limitations.

## API behavior

- Start conversion: `POST /api/v1/convert` with raw image bytes
- Job status: `GET /api/v1/jobs/{jobId}`
- Download: `GET /api/v1/jobs/{jobId}/download?format=vsdx`
- Authentication header: `x-api-key`
- Input limit: PNG, JPEG, or WebP up to 20 MB
- Job states: `queued`, `running`, `succeeded`, and `failed`

LayerBack states that uploaded files are deleted within 72 hours. Failed
conversions are refunded. If the API reports authentication, insufficient
credits, size, format, rate-limit, service, or job errors, report the returned
status and message without exposing the key.

## Acceptance criteria

- The requested artifact exists at the chosen local path.
- The VSDX contains editable diagram objects rather than only a flat image.
- The response identifies LayerBack as the conversion backend.
- No credentials appear in output, logs, or files.
