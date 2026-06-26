# Implementation plan 0.2.0

## Phase 1 — Foundation

1. add install-state data model
2. add host/port selection helper
3. add credential generation helper
4. add web-service config loader
5. define onboarding vs managed UI states

## Phase 2 — Install bootstrap

1. implement `install_web_app.py`
2. detect `9527` then `12138`, then fallback port
3. generate admin password
4. generate/update service config
5. print install summary with SSH tunnel command

## Phase 3 — Web onboarding UX

1. add `service/app.py`
2. add onboarding page when auth is missing
3. add environment status page
4. add import-auth action
5. add minimal HTTP Basic Auth protection
6. hide advanced actions until takeover is complete

## Phase 4 — Runtime integration

1. wire existing doctor/env/inspect data into the web UI
2. keep switch/rollback actions behind managed mode
3. preserve external state-dir support
4. verify no pollution of the public source tree

## Phase 5 — Edge-case handling

1. no-systemd fallback mode
2. occupied-port fallback
3. broken runtime messaging
4. SSH-only guidance
5. verify generated systemd unit paths against real workspace layout

## Phase 6 — Validation

Current implementation landing:

- installer now records richer `systemd --user` service state instead of relying on port-open only
- installer performs `systemctl --user reset-failed` before enable/start to reduce restart-loop leftovers on reinstall
- installer uses `enable` + `restart` after `daemon-reload` so changed unit env/port is actually applied on reinstall
- installer gracefully falls back when the systemd template is missing instead of crashing the install command
- status output now includes `service_mode`, `service_ready`, and `systemd_status`
- preview page now surfaces `ActiveState`, `SubState`, and `log_path` to make first-run diagnosis human-readable
- runtime/status now prefers live `systemd` state over stale install-info when deciding displayed service mode


Test these scenarios:

1. Linux machine with working auth
2. Linux machine without auth
3. 9527 occupied
4. 9527 + 12138 both occupied
5. no systemd user-service support
6. install + uninstall + reinstall path

## Shipping recommendation

- keep `0.1.x` as script-first baseline
- ship `0.2.0` only after the web-first onboarding flow is verified on a clean machine
