# Liner schedule API (hifleet-schedule)

This skill queries **HiFleet liner schedules** only (general/bulk, Ro-Ro, container). Not for mailbox tonnage or ETA pre-arrival.

---

## Distribution

1. Data from **`api.hifleet.com`** via HTTPS; never substitute mail/SQLite or fabricated rows.  
2. **Full list mandatory**: **`FULL_LIST_POLICY.md`**.  
3. Key: `hifleet_api_key` / `HIFLEET_API_KEY`; never expose full key in chat.

## Schedule types (user wording)

| Category | User may say |
|----------|----------------|
| General / bulk | breakbulk, general cargo liner, 散杂货船期 |
| Ro-Ro | car carrier, PCTC, Ro-Ro, 滚装船期 |
| Container | container line, feeder, 集装箱船期 |

Same API endpoints for all; filter by ports/dates in `params`. If API returns a vessel/line type field, show it **as returned** (do not translate names).

---

## Config

| Item | Default |
|------|---------|
| `{base}` | `https://api.hifleet.com/openclaw/vessel/charter/liner` |

Resolve: `hifleet_liner_api_base` → `HIFLEET_LINER_API_BASE` → default.

---

## 1. Port suggest

**`GET {base}/ports/suggest`**

| | |
|--|--|
| Header `api_key` | user key |
| Query `keyword` | **English** port name (`Shanghai`, not 上海) |
| Query `from` | `0` |
| Query `size` | `1` |
| Query `api_key` | same as header |

Take **`data[0].portId`** for load/discharge. If user names two ports, call §1 **twice** and pass both IDs in one `POST /schedules` (see §2).

**Do not** filter results by port name string after fetch.

---

## 2. Schedule list

**`POST {base}/schedules?sk={url-encoded api_key}`**

| Field | Notes |
|-------|--------|
| `offset` / `limit` | Paginate per **`FULL_LIST_POLICY.md`** |
| `params.portid` | Load port ID from §1 |
| `params.dischargingPortid` | Discharge port ID when user asked both ports |
| `params.isPublic` | e.g. `true` |
| `params.openDateStart` / `openDateEnd` | `yyyy-MM-dd` laycan window |

**“Recent”**: wide window from tomorrow if user did not specify dates.

Each item in `data` must have top-level **`id`** for unlock (`dataId`).

---

## 3. Unlock contact

**`POST {base}/unlock?dataId={id}&typeCode=product_vessel_liner_charter&api_key=...`**

| Query | Notes |
|-------|--------|
| `dataId` | Top-level **`id`** from schedule list row |
| `typeCode` | Fixed **`product_vessel_liner_charter`** |

**User-facing wording**: **获取联系方式** — not 「解锁」. All four charter `typeCode` values: **`references/charter_contact_unlock.md`**.

### Single row

User gives record id or picks a row → one `POST /unlock`.

### All rows (batch)

User says **all** / **全部联系方式** → loop **`dataId`** for **each** `id` from the last schedule list (confirm API points if many rows).

Do not call unlock again for the same `id` in the same session unless the user asks.

Show unlocked fields per **`WORKFLOW_OUTPUT.md`**.

---

## 4. User-visible output

See **`WORKFLOW_OUTPUT.md`**: full list, Laycan one line, empty fields omitted, locked vs unlocked contact rules.

---

## Errors

On HTTP/API errors, show a **short** message in the **user’s locale** (`LOCALIZATION.md` / `scripts/i18n_messages.py`). Do not paste full `api_key` or stack traces.
