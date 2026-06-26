# Home Assistant MCP Skill

## Description
This skill provides structured access to Home Assistant via its native MCP (Model Context Protocol) integration. It provides tools and context for interacting with devices, sensors, and cameras in the smart home.

## Credentials
The MCP server endpoint is `http://220.0.0.5:8123/api/mcp`.
Ensure the connection is configured with the correct Long-Lived Access Token.

## Best Practices

1. **Camera Snapshots:**
   **MCP tools for cameras (video_garage, homeassistant___XXXXX) DO NOT WORK!**
   Always use `exec` with `curl` to the REST API to get camera snapshots:
   `curl -s -H "Authorization: Bearer <TOKEN>" "http://220.0.0.5:8123/api/camera_proxy/camera.<entity_id>" -o /home/clawd/.openclaw/workspace/<filename>.jpg`
   After fetching, verify it's a JPEG with `file`, then display it using the `MEDIA:<path>` directive.

2. **Garage Operations:**
   - The garage ESPHome logic is inverted: `HassTurnOff` = OPEN, `HassTurnOn` = CLOSE.
   - Wait 30-50 seconds after a command before checking the position.
   - True garage door position is determined by endstops, not just `current_position: 0` or state.
   - Ignore `Garage 2 Motion` as it produces false positives.

3. **Device Control:**
   - **NEVER** turn devices on or off without explicit user request.
   - Do not use the `homeassistant__forced` tool.

4. **Status Checks:**
   - Use `homeassistant__GetLiveContext` to get a snapshot of all exposed entities.
   - If MCP tools timeout, fallback to the REST API: `curl -H "Authorization: Bearer <TOKEN>" http://220.0.0.5:8123/api/states/<entity_id>`

## Key Entities
Review `/home/clawd/.openclaw/workspace/memory/home-assistant-entities.md` for a full list of areas and key entities.