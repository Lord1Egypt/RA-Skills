---
name: blender-mcp
description: Integrate Blender MCP (Model Context Protocol) allowing OpenClaw to control Blender for 3D modeling, scene creation, and manipulation. Use when you need to interact with Blender, create 3D models, modify scenes, or generate 3D content.
---

# Blender MCP Skill

This skill enables OpenClaw to control Blender through the BlenderMCP Model Context Protocol integration.

## Prerequisites

1. Blender installed and running
2. BlenderMCP addon installed in Blender
3. blender-mcp Python package installed via uvx

## Usage

### Starting the Connection

1. **In Blender**:
   - Open Blender
   - Press `N` to show the 3D View sidebar
   - Go to "BlenderMCP" tab
   - Click "Connect to Claude" to start the socket server on localhost:9876

2. **In OpenClaw**:
   - Use the `start-server` script to start the MCP server
   - Or run `uvx blender-mcp` manually

### Available Commands

The following tools are available through BlenderMCP:

- `get_scene_info` - Get detailed information about the current Blender scene
- `create_object` - Create a new 3D object (cube, sphere, cylinder, etc.)
- `delete_object` - Delete an existing object
- `modify_object` - Modify object properties (location, rotation, scale, etc.)
- `set_material` - Create/assign a material to an object
- `execute_code` - Execute arbitrary Python code in Blender
- `get_screenshot` - Get a screenshot of the current viewport
- `download_asset_polyhaven` - Download assets from Poly Haven
- `search_sketchfab` - Search and download models from Sketchfab
- `generate_model_3d` - Generate 3D models using Hyper3D Rodin AI

### Example Prompts

- "Create a low poly dungeon scene with a dragon guarding gold"
- "Make a red metallic sphere on top of a cube"
- "Create a studio lighting setup and point the camera at the scene"
- "Get a screenshot of the current scene"
- "Download a grass texture from Poly Haven and apply it to the ground"

## Scripts

- `scripts/start-server.sh` - Start the Blender MCP server
- `scripts/test-connection.py` - Test connection to Blender

## Configuration

By default, connects to:
- Host: `localhost`
- Port: `9876`

To change, set environment variables:
```bash
export BLENDER_HOST=your-host
export BLENDER_PORT=your-port
```

## Troubleshooting

1. **Connection refused**: Make sure Blender is running and the addon is connected
2. **Timeout errors**: Break large requests into smaller steps
3. **Unknown command**: Restart both Blender addon and MCP server
