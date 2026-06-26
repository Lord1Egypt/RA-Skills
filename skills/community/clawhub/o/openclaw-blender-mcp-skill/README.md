# openclaw-blender-mcp skill

Blender MCP (Model Context Protocol) integration skill for OpenClaw. Allows OpenClaw to directly control Blender for 3D modeling, scene creation, and manipulation.

## Features

- 🎨 Full control over Blender through the BlenderMCP socket interface
- 🧩 Can execute arbitrary Blender Python code from OpenClaw
- 📐 Create accurate architectural models like Hagia Sophia (example included!)
- 🎬 Supports camera animation and rendering
- 🌳 Includes helper scripts for connection testing

## Requirements

- Blender 3.0+ installed on your machine
- blender-mcp addon installed in Blender
- uv package manager installed (`brew install uv` on macOS)

## Installation

### 1. Install BlenderMCP server

BlenderMCP is automatically available via uvx:
```bash
uvx blender-mcp
```

### 2. Install Blender addon

1. Download `addon.py` from https://github.com/ahujasid/blender-mcp
2. In Blender: `Edit > Preferences > Add-ons > Install` select `addon.py`
3. Enable the "Interface: Blender MCP" addon
4. In the 3D View sidebar (press N), find BlenderMCP tab
5. Click "Connect to Claude" to start the socket server on `localhost:9876`

### 3. Install this skill in OpenClaw

```bash
# In OpenClaw skills directory
mkdir -p ~/.openclaw/skills/
cp -r this-repo ~/.openclaw/skills/blender-mcp
```

## Usage

1. In Blender, start the BlenderMCP socket server (sidebar → BlenderMCP → Connect)
2. In OpenClaw, you can now:
   - Create 3D models
   - Modify existing scenes
   - Execute Python code in Blender
   - Render still images and animations

## Included Scripts

- `scripts/start-server.sh` - Start the Blender MCP server via uvx
- `scripts/test-connection.py` - Test connection to Blender socket server

## Example: Hagia Sophia

This skill was tested by creating a full architectural model of Hagia Sophia in Istanbul, Turkey:
- Correct architectural dimensions: 77m × 71m
- 4 minarets at each corner (correct final configuration)
- Central dome 32m diameter
- Semi-domes at east and west ends
- Sultanahmet Square with 3 ancient monuments
- North/South gardens with cypress trees
- Camera animation from far → move in → 360° orbit

## Author

Created by [your name here] for OpenClaw based on the original BlenderMCP by [@ahujasid](https://github.com/ahujasid/blender-mcp)

## License

MIT License - feel free to use and modify!
