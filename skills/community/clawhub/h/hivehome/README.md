# Hive Home

Control Hive Home (UK) thermostats, hot water, lights and devices via the unofficial API from your agent. This skill follows the [Agent Skills](https://agentskills.io/home) format (SKILL.md, scripts/, references/).

## What it does

- **Heating:** Read and set mode (SCHEDULE, HEAT, OFF), target temperature, boost (duration + temperature).
- **Hot water:** Read and set mode, boost duration.
- **Lights:** Read state, brightness, colour temp; control via Pyhiveapi session (custom code; not in CLI).
- **Auth:** First-time login with SMS 2FA; device credentials for subsequent runs (no 2FA).

The skill includes **bundled scripts** (`scripts/hive_control.py`) for status, set-temp, mode, boost, and hot water. The agent runs these by default. For lights or custom logic it uses the [Pyhiveapi](https://github.com/Pyhass/Pyhiveapi) library. Hive does not provide a public API; Pyhiveapi talks to the same backend as the Hive app.

## How to use

1. **Install dependency:** `pip install "pyhiveapi>=1.0.0"` (script uses current session API; if you see errors, run `pip install -U pyhiveapi`).
2. **Set credentials** (env or OpenClaw config): see [references/CREDENTIALS.md](references/CREDENTIALS.md) or SKILL.md “Credentials” section.
3. **Enable the skill** in OpenClaw (workspace skills or ClawHub install).
4. Ask the agent to control heating, set temperature, boost hot water, etc. It will **run the bundled scripts** (e.g. `python scripts/hive_control.py status` or `set-temp 21`). For lights or custom behaviour it may generate Pyhiveapi code.

See [SKILL.md](SKILL.md) for script usage and code examples. Detailed API reference: [references/REFERENCE.md](references/REFERENCE.md).

## Requirements

- Python 3
- `pyhiveapi>=1.0.0` (`pip install "pyhiveapi>=1.0.0"`)
- Hive (UK) account – [my.hivehome.com](https://my.hivehome.com)
- Network access (to Hive’s servers)

## Troubleshooting

- **Attribute/method errors:** Script targets pyhiveapi 1.0.x session API. Run `pip install -U pyhiveapi` and try again.
- **SMS 2FA:** First login requires a code from Hive; run the first-time login snippet once and store device data for later.
- **Login errors:** Ensure username/password are correct and env vars are set. For device login, all three device keys must match the stored values from first login.
- **No devices:** Call `session.startSession()` before using `session.deviceList`; ensure your Hive account has devices linked.

## External services

This skill uses the **Pyhiveapi** library, which communicates with Hive’s backend (e.g. beekeeper.hivehome.com). Credentials and device commands are sent only to Hive. See the “External endpoints” and “Trust statement” sections in [SKILL.md](SKILL.md).

## License

MIT.
