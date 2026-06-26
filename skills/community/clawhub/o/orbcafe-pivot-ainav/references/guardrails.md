# Pivot + AINav Guardrails

## Pivot constraints

- Prefer controlled mode (`usePivotTable`) when external filters, persistence, or replay are needed.
- `fields` must provide correct `type` (`string/number/...`) or aggregations become invalid.
- For multi-table analytics pages, isolate each pivot config in separate persisted keys.

## Preset constraints

- If presets are business assets, persist server-side via `onPresetsChange` sync.
- If presets are personal preferences only, local storage is acceptable.

## Voice constraints

- `onVoiceSubmit` is required on `CAINavProvider`.
- Keep `ignoreWhenFocusedInput=true` unless explicitly required, to avoid hijacking typing UX.
- `wsUrl` and ASR auth must come from app config, not hardcoded secrets.
- Handle silence threshold and min volume conservatively to reduce false stops.
