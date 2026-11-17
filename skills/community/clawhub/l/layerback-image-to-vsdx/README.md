# LayerBack Image to VSDX Skill

Official agent skill for converting diagram images into genuinely editable
Microsoft Visio files with [LayerBack](https://layerback.com/image-to-visio).
It rebuilds boxes as native shapes, arrows as connectors, and labels as
editable text rather than embedding a flat image inside a VSDX file.

## Use cases

- Flowcharts and process maps
- Architecture and network diagrams
- UML and ER diagrams
- Organization charts
- Diagram screenshots, exports, and whiteboard photos

The official API can return VSDX, PPTX, draw.io, SVG, IR, and preview outputs.

## Install

```bash
npx -y skills@latest add TopLocalAI/layerback-image-to-vsdx-skill \
  --skill layerback-image-to-vsdx \
  --agent codex \
  --global
```

Or give the repository URL to any agent that supports `SKILL.md`:

```text
Please install the LayerBack Image to VSDX skill from https://github.com/TopLocalAI/layerback-image-to-vsdx-skill
```

## API setup

Create a key at [LayerBack API Keys](https://layerback.com/settings/apikeys)
and store it locally:

```bash
export LAYERBACK_API_KEY='YOUR_KEY'
```

Never paste or commit a real API key. The included client uses Python 3
standard-library modules only.

```bash
python3 scripts/layerback_convert.py source.png \
  --out result.vsdx \
  --format vsdx
```

A successful conversion consumes 10 LayerBack credits. The skill asks for
confirmation before uploading a file or starting a credit-consuming request.

## Official links

- [Image to Visio](https://layerback.com/image-to-visio)
- [Online converter](https://layerback.com/convert)
- [API documentation](https://layerback.com/docs/api)
- [OpenAPI specification](https://layerback.com/openapi.yaml)
- [LayerBack MCP server](https://github.com/TopLocalAI/layerback-mcp)

## License

MIT
