# Bridge And API

Use this when bridge state, API execution, or official package setup matters.

## Preferred Tools

Prefer MCP tools:

- `mcp__easyeda__bridge_status`
- `mcp__easyeda__list_eda_windows`
- `mcp__easyeda__get_current_project_info`
- `mcp__easyeda__execute_in_eda`

## Official Package

- Package URL: `https://image.lceda.cn/files/easyeda-api.zip`
- Extension page: `https://ext.lceda.cn/item/oshwhub/run-api-gateway`
- Bundled bridge script: `scripts/bridge-server.mjs`
- Bundled official API reference: `references/easyeda-api-reference/`
- Bundled official guides: `references/easyeda-official-guides/`
- Bundled official user guide: `references/easyeda-user-guide/`
- Bundled official package manifest: `references/easyeda-official-meta/package.json`
- Node script: `npm run server`
- Port range: `49620-49629`

Endpoints:

| Endpoint | Purpose |
| --- | --- |
| `GET /health` | Check bridge and EDA connection status |
| `GET /eda-windows` | List connected EasyEDA windows |
| `POST /eda-windows/select` | Select active EDA window |
| `POST /execute` | Execute JavaScript in the EasyEDA client |
| `WS /eda` | EasyEDA extension connection |
| `WS /agent` | Agent connection |

## Manual Start On Windows

```powershell
npm install
$wd = (Resolve-Path ".").Path
Start-Process -FilePath "node" -ArgumentList "scripts/bridge-server.mjs" -WorkingDirectory $wd -WindowStyle Hidden -RedirectStandardOutput "bridge-server.log" -RedirectStandardError "bridge-server.err.log"
Invoke-RestMethod http://localhost:49620/health
```

If `edaConnected` is false, tell the user to install/load the Run API Gateway extension in EasyEDA and keep EasyEDA open.

## API Coverage

- `DMT_*`: project, board, folder, schematic/page, editor/document, team/workspace operations.
- `SCH_*`: schematic primitives, components, wires, text, netlists, DRC, selection.
- `PCB_*`: PCB primitives, components, pads, vias, lines, pours, layers, nets, DRC, selection.
- `LIB_*`: device, symbol, footprint, 3D model, CBB, library search and metadata.
- `SYS_*`: messages, dialogs, files, settings, windows, timers, storage, web sockets.

For method names, search the bundled official package in this order:

1. `references/easyeda-api-reference/_quick-reference.md`
2. `references/easyeda-api-reference/_index.md`
3. Specific files under `references/easyeda-api-reference/classes/`
4. Specific files under `references/easyeda-api-reference/enums/`, `interfaces/`, or `types/`

## Execution Rules

Code runs in the EasyEDA browser runtime:

```javascript
return await eda.dmt_Project.getCurrentProjectInfo();
```

- Always `return` useful results; do not rely on `console.log`.
- Await promise-returning API calls.
- Do not use Node APIs like `fs` or `path` inside EasyEDA execution code.
- Use `eda.sys_Message.showToastMessage("...")` for visible completion notices.
- Verify active project and document type before using `SCH_*` or `PCB_*`.
- Schematic coordinates use `0.01 inch`; PCB coordinates use `1 mil`.
- Split complex operations into smaller calls if execution times out.
