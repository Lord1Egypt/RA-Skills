# FreeCAD MCP Skill

Enable AI agents to control FreeCAD via the Model Context Protocol (MCP). Create 3D models programmatically, generate parts from descriptions, and automate CAD workflows.

## Features

- 🦾 Full FreeCAD control via RPC server
- Create 3D objects from 2D drawings
- Automatic constraint solving
- Part library integration
- Compatible with LangChain and Google ADK agents

## Requirements

- FreeCAD 0.21+ installed
- Python 3.10+
- MCP-enabled AI agent

## Installation

### 1. Install the skill
```
npx clawhub install openclaw-freecad-mcp
```

### 2. Install the FreeCAD addon
Copy the `addon/FreeCADMCP` folder to your FreeCAD addons directory:
- **macOS**: `~/Library/Application Support/FreeCAD/Mod`
- **Linux**: `~/.FreeCAD/Mod`
- **Windows**: `%APPDATA%\FreeCAD\Mod`

### 3. Start the RPC server
In FreeCAD, go to Workbenches → FreeCAD MCP → Start RPC Server

### 4. Configure your agent
Add the MCP server endpoint to your agent configuration:
```json
{
  "mcpServers": {
    "freecad": {
      "url": "http://localhost:9876"
    }
  }
}
```

## Usage

Example agent prompts:
- "Create a 50x50x10 mm cube with a centered 20mm hole"
- "Turn this 2D sketch into a 3D printable model"
- "Design a toy car body with integrated axles"

## Examples

See the `examples/` directory for:
- LangChain React agent example
- Google ADK agent example

## Author

[mars720816](https://github.com/mars720816)

## License

MIT
