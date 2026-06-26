---
name: openweather-cli
description: Use this skill when the user wants to run, troubleshoot, or extend the owget CLI for geocoding, current weather, and 5-day forecasts with OpenWeatherMap.
homepage: https://github.com/ParinLL/OpenWeatherMap-script
requires:
  env:
    - OPENWEATHER_API_KEY
  bins:
    - go
metadata: {"openclaw":{"homepage":"https://github.com/ParinLL/OpenWeatherMap-script","requires":{"env":["OPENWEATHER_API_KEY"],"bins":["go"]},"primaryEnv":"OPENWEATHER_API_KEY"}}
---

# OpenWeather CLI Skill

Instruction-only skill document for using and troubleshooting `owget` (OpenWeather CLI).

## Skill Purpose and Trigger Scenarios

- The user wants current weather, forecast, or geocoding (`geo`) results.
- The user asks how to run `owget` commands or use parameters.
- The user reports API key issues, HTTP errors, or city lookup failures.

## Install from GitHub

- GitHub: https://github.com/ParinLL/OpenWeatherMap-script

Recommended install:

```bash
git clone https://github.com/ParinLL/OpenWeatherMap-script.git
cd OpenWeatherMap-script
go install .
```

This installs `owget` into your Go bin directory (for example, `$GOPATH/bin` or `$HOME/go/bin`).

## Required Environment Variables / Permissions

Required environment variable:

```bash
export OPENWEATHER_API_KEY="your-api-key"
```

- Requires the `go` toolchain for build/install.
- System-wide installation into protected directories (for example, `/usr/local/bin`) requires admin privileges and prior source review.
- Never expose full API keys in outputs; debug request logs should redact credential query params (for example, `appid`).

## How to Use the Binary

After installation, make sure `owget` is available in your shell:

```bash
owget --help
```

If your shell cannot find it, add your Go bin path to `PATH`:

```bash
export PATH="$PATH:$(go env GOPATH)/bin"
```

Core command patterns:

- Current weather by coordinates:
  - `owget weather <lat> <lon>`
  - Example: `owget weather 25.0330 121.5654`
- Current weather by city:
  - `owget city "<City,Country>"`
  - Example: `owget city "Taipei,TW"`
- 5-day forecast:
  - `owget forecast <lat> <lon>`
  - Example: `owget forecast 25.0330 121.5654`
- 5-day forecast by city:
  - `owget city "<City,Country>" forecast`
  - Example: `owget city "Taipei,TW" forecast`
- Geocoding lookup:
  - `owget geo "<query>"`
  - Example: `owget geo "New York,US"`

Useful flags:

- `--detail`: show extended fields (for example pressure, wind, sunrise/sunset, visibility).
- `--debug`: print HTTP debug information for troubleshooting. Sensitive query parameters are redacted.

Common usage flow:

1. Export `OPENWEATHER_API_KEY`.
2. Run `owget geo "<City,Country>"` if you need to verify location naming.
3. Use `owget weather ...` or `owget forecast ...` for actual weather data.
4. Add `--detail` for richer output, and `--debug` only when troubleshooting.

## Common Troubleshooting

- `error: OPENWEATHER_API_KEY env is required`
  - The env var is not set. Run `export OPENWEATHER_API_KEY="..."` first.
- API returns `401`
  - API key is invalid, expired, or mistyped. Re-check your OpenWeatherMap key.
- API returns `404` or city not found
  - Use `City,Country` format (for example, `Taipei,TW`) and verify with `owget geo "<query>"` first.
- Concern about credential leakage while using debug mode
  - Debug request URLs are redacted for sensitive params, but avoid long-running debug in shared/logged environments.
