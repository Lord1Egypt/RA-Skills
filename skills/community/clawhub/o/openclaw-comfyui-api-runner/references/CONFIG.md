# ComfyUI Safe Connector - Configuration

Connection settings are stored in a small user config file:

`~/.config/openclaw/comfyui-runner.json`

## Schema

```json
{
  "active_profile": "home",
  "profiles": {
    "home": {
      "base_url": "http://127.0.0.1",
      "port": 8188,
      "api_key": "optional",
      "username": "optional",
      "password": "optional"
    }
  }
}
```

## Env overrides

- `COMFYUI_PROFILE`
- `COMFYUI_BASE_URL`
- `COMFYUI_PORT`
- `COMFYUI_API_KEY`
- `COMFYUI_USERNAME`
- `COMFYUI_PASSWORD`

## CLI

```bash
./comfy.sh --list-profiles
./comfy.sh --save-profile home --base-url http://127.0.0.1 --port 8188
./comfy.sh --profile home --health
```

## Notes

- `base_url` can include the scheme, for example `http://127.0.0.1` or `https://host`.
- If `base_url` already contains a port, `port` is ignored.
- API key is optional.
- Basic auth is optional.
- No local viewer is required. The runner returns downloadable files and browser view URLs instead.
