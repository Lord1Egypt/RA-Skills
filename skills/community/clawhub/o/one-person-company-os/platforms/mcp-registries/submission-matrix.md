# MCP Registry Submission Matrix

Version: 1.0.3

Common package:

- `platforms/mcp-server/server.py`
- `platforms/mcp-server/server.json`
- `platforms/mcp-server/README.md`

Common description:

One Person Company OS exposes a local MCP adapter for building and advancing a visual operating cockpit for an AI-native one-person company. The tools help initialize a founder-approved workspace, update the current focus, generate formal artifact text, and validate the release package.

Common safety notes:

- The server uses stdio transport.
- Persistent files are limited to the founder-approved workspace.
- The server does not auto-install system packages.
- High-risk customer-facing, legal, pricing, budget, and launch actions require founder approval.

| Registry | Status | Required submission material | Evidence before `published` |
| --- | --- | --- | --- |
| MCP Registry | ready-to-submit | publisher namespace, `server.json`, repository URL, package description | official registry listing or API record |
| Smithery | ready-to-submit | Smithery account/API key or hosted endpoint, MCP package metadata | Smithery listing URL |
| Glama | ready-to-submit | public GitHub repository metadata or indexing submission | Glama listing URL |
| PulseMCP | ready-to-submit | manual/API submission metadata, package URL, summary | PulseMCP listing URL |

Recommended tool list:

- `preflight_check`
- `init_business`
- `update_focus`
- `generate_artifact_document`
- `validate_release`
