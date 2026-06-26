# Oracle VM Setup

## Current state

`oracle_vm` already has:
- `xvfb-run`
- `ffmpeg`
- `node`
- `npm`
- `python3`

It does not currently have a Unity editor or runtime installed.

## MVP setup target

Install:
- Unity Editor in batch-capable Linux mode
- the Aavegotchi Unity SDK package or a wrapper Unity project that imports it

Expected Unity project location:
- `/home/ubuntu/.openclaw/workspace/skills/gotchi-3d-custom-render/unity/GotchiCustomRenderer`

Expected batch entrypoint:
- method name: `GotchiCustomRenderCLI.RenderFromJson`

Expected invocation shape:

```bash
xvfb-run -a <UNITY_BIN>   -batchmode -nographics -quit   -projectPath /home/ubuntu/.openclaw/workspace/skills/gotchi-3d-custom-render/unity/GotchiCustomRenderer   -executeMethod GotchiCustomRenderCLI.RenderFromJson   --input /tmp/openclaw/custom-gotchi-request.json
```
