---
name: map-address-query
description: Map service address lookup and distance-query workflow. MUST use this skill when the user asks for coordinates (坐标), latitude/longitude, POI locations (e.g., specific buildings, shops, or addresses like "北京市朝阳区望京街10号的坐标"), or when calculating route distance and time between places. Supports converting physical locations or names into GPS coordinates.current support Tencent map.
---

# Map Address Query

First, run `./scripts/qq_map_cli.sh` (or `.\scripts\qq_map_cli.bat` on Windows) to download the CLI tool.
Then, use `./scripts/bin/qq-map-cli` (or `.\scripts\bin\qq-map-cli.exe` on Windows) to query Tencent Location Service from the terminal.

## Quick Start

- If the global config file does not exist, create one first:

```bash
# On Mac/Linux
./scripts/bin/qq-map-cli setup --config ~/.qq_map_cli_config.json

# On Windows (CMD/PowerShell)
.\scripts\bin\qq-map-cli.exe setup --config %USERPROFILE%\.qq_map_cli_config.json
```

- If the user already has a Tencent Location Service key, write it directly during setup:

```bash
./scripts/bin/qq-map-cli setup --config ~/.qq_map_cli_config.json --key "your-key"
# Windows: .\scripts\bin\qq-map-cli.exe setup --config %USERPROFILE%\.qq_map_cli_config.json --key "your-key"
```

- The CLI reads the key from one of these places: `--key`, `QQ_MAP_KEY`, `--config` file path.
- Always append the global config flag: `--config ~/.qq_map_cli_config.json` (or `--config %USERPROFILE%\.qq_map_cli_config.json` on Windows) to all commands.
- Run the bundled CLI from the skill directory: `./scripts/bin/qq-map-cli <subcommand> ...` (or `.\scripts\bin\qq-map-cli.exe` on Windows).
- Prefer `--json` when another script or workflow needs structured output.

## How to get Tencent Location Service key
- visit https://lbs.qq.com/dev/console/application/mine 
- click "创建应用" button to create a new application
- click "添加key" button to add a new key
- copy the "Key" value to the `--key` flag

## Commands

### Geocode One Address

Use `geocoder` when the user wants latitude/longitude or structured address fields for one place.

```bash
./scripts/bin/qq-map-cli geocoder \
  --config ~/.qq_map_cli_config.json \
  --address "北京市海淀区彩和坊路海淀西大街74号"
# Windows: .\scripts\bin\qq-map-cli.exe geocoder --config %USERPROFILE%\.qq_map_cli_config.json --address "..."
```

### Measure Distance Between Two Named Addresses

Use `address-distance` when the user asks for the distance or travel time between two address names.

```bash
./scripts/bin/qq-map-cli address-distance \
  --config ~/.qq_map_cli_config.json \
  --from-address "北京市海淀区中关村大街27号" \
  --to-address "北京市朝阳区望京街10号" \
  --mode driving
# Windows: .\scripts\bin\qq-map-cli.exe address-distance --config %USERPROFILE%\.qq_map_cli_config.json ...
```

### Run Coordinate or Matrix Queries

Use `distance-matrix` when the user already has coordinates, needs one-to-many or many-to-many queries, or wants raw `from` and `to` payload control.

```bash
./scripts/bin/qq-map-cli distance-matrix \
  --config ~/.qq_map_cli_config.json \
  --origin 39.984154,116.307490 \
  --destination 39.908692,116.397477 \
  --mode walking
# Windows: .\scripts\bin\qq-map-cli.exe distance-matrix --config %USERPROFILE%\.qq_map_cli_config.json ...
```

## Workflow

1. Check whether a global config already exists at `~/.qq_map_cli_config.json` (or `%USERPROFILE%\.qq_map_cli_config.json`) or `QQ_MAP_KEY`.
2. If neither exists, run `setup` with the global `--config` flag to create the config file in the user's home directory.
3. If the user can provide the Tencent key immediately, prefer `setup --config ~/.qq_map_cli_config.json --key "..."` so the config is complete in one step.
4. If the key is still missing after setup, stop and ask the user for the Tencent Location Service key instead of trying live queries.
5. After the user provides the key, immediately persist it globally by running `setup --config ~/.qq_map_cli_config.json --key "..." --force`.
6. Treat `~/.qq_map_cli_config.json` as a globally persistent config so the user does not need to configure it again for queries in other directories.
7. Start with the fullest address available, including city and district, to improve geocoder accuracy.
8. Use `address-distance` by default for natural-language requests like "这两个地址相距多远".
9. Switch to `distance-matrix` for batch routing, coordinate-based inputs, or advanced raw payloads.
10. Retry with `--policy 1` when the user gives a shorter or fuzzier address and strict parsing looks too brittle.
11. Change `--mode` to `walking`, `bicycling`, or `straight` when the user asks for non-driving results.
12. Keep API keys in the user's workspace config or environment variables, not inside the skill folder.

## Output Notes

- Default output is human-readable and suited to chat replies.
- `--json` returns raw API responses for downstream automation.
- `address-distance --json` returns both geocoder responses and the final distance-matrix response in one object.

## Troubleshooting

- **SSL Certificate Error on macOS**: If you see `[SSL: CERTIFICATE_VERIFY_FAILED]`, run the downloaded binary with `SSL_CERT_FILE=/etc/ssl/cert.pem ./scripts/bin/qq-map-cli ...` to manually point to macOS's certificates.
