# Port ID resolution (`GET {liner}/ports/suggest`)

**Mandatory** for **`hifleet-schedule`** and **`hifleet-opentonnages`** when the user names a port and the list API needs **`portid`**.

**Do not** use `portguide/getPort/token` or other port-guide APIs for these skills — use **`ports/suggest`** only.

---

## Endpoint

**`GET https://api.hifleet.com/openclaw/vessel/charter/liner/ports/suggest`**

| Item | Value |
|------|--------|
| `{liner}` | `https://api.hifleet.com/openclaw/vessel/charter/liner` |
| Resolve | `hifleet_liner_api_base` → `HIFLEET_LINER_API_BASE` → default |

| | |
|--|--|
| Header `api_key` | user key |
| Query `keyword` | **English** port name (`Tianjin`, not 天津) |
| Query `from` | `0` |
| Query `size` | `1` (use `5` if user must pick among hits) |
| Query `api_key` | same as header |

**Take `data[0].portId`** (string) → **`params.portid`** (schedule, open cargo load port) or **`params.dischargingPortid`** (open cargo discharge port).

If user names **two** ports (e.g. schedule load + discharge), call suggest **twice** with separate keywords.

Multiple hits → ask user to confirm; **never** guess portid.

---

## CLI

| Skill | Command |
|-------|---------|
| Open vessel/cargo | `hifleet-opentonnages/scripts/opentonnages_tool.py ports-suggest --keyword Tianjin` |

Schedule: agent calls HTTP directly (see **`hifleet-schedule/SCHEDULE_API.md`** §1).

---

## Skill-specific usage

| Skill | List API field |
|-------|----------------|
| `hifleet-schedule` | `params.portid`, `params.dischargingPortid` |
| `hifleet-opentonnages` (vessel) | `params.portid` and/or `params.openPort` per API |
| `hifleet-opentonnages` (cargo) | `params.portid`, `params.dischargingPortid` |
