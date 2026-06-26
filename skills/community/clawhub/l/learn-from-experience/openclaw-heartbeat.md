## Learn-from-Experience Check (OpenClaw)

- Read `./skills/learn-from-experience/heartbeat-rules.md`
- Use `~/learn-from-experience/heartbeat-state.md` for last-run markers and action notes
- If no file inside `~/learn-from-experience/` changed since the last reviewed change, return `HEARTBEAT_OK`
- Check cross-session sync status in `~/learn-from-experience/index.md`; if `stale`, trigger global config sync

Note: OpenClaw uses the same memory directory (`~/learn-from-experience/`) and the same sync protocol as all other agent products.
