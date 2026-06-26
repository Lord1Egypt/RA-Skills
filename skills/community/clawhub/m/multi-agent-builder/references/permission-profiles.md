# Permission Profiles (Least Privilege)

Apply least privilege by default; expand only with user confirmation.

## team-leader-standard
- tools: read, write, sessions_send
- exec: disabled by default
- external side effects: controlled by mode policy

## planner-low-risk
- tools: read, write (optional web_search/web_fetch)
- exec: disabled
- external side effects: disabled by default

## architect-standard
- tools: read, write, edit (optional exec)
- exec: allowed non-elevated only when needed
- external side effects: disabled by default

## builder-standard
- tools: read, write, edit, exec, process
- exec: non-elevated by default
- file scope: workspace only
- external side effects: require explicit confirmation

## tester-standard
- tools: read, write, exec (optional browser)
- exec: non-elevated only
- external side effects: disabled by default

## operator-standard
- tools: read, write, web_search, web_fetch (optional browser)
- exec: disabled unless explicitly required
- external side effects: require explicit confirmation

## analyst-low-risk
- tools: read, write (optional web_search/web_fetch)
- exec: disabled
- external side effects: disabled

## Escalation rule
If required capability is blocked by permissions:
1) identify exact missing scope
2) request minimal additional permission
3) re-run only failed step
