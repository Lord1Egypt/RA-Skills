# Closure email-state pitfalls: dispatcher re-fire + basename collision

Two pitfalls surfaced during the 2026-07-16T2145Z mixed Mode-C closure (owner `new_emails` + mentor `new_journals` re-detection). Both concern the email second-wave `verified_second_wave` re-affirm step under the documented monitor re-fire bug. They are NOT covered by the older `dispatch-wave-email-state-topology.md` (which says "key on path, not account" — Pitfall B is the *reverse* trap).

## Pitfall A — scheduled dispatcher re-fires mid-closure and clobbers top-level GWS-snapshot files

**Observation:** While a manual closure re-flagged `verified_second_wave=True` on the two top-level gws-snapshot files, the scheduled `dispatcher.py` (and/or `monitor_email.py`) FIRED AGAIN ~60s into the run and rewrote both files as pure gws snapshots (raw `new_threads` payload), dropping the `verified_second_wave` field entirely (Null). The verifier's `[3]` gate then read None.

**Which files survive:** the dispatch-OWNED owner copies — `owner/last_email_check.json` and `last_email_check_owner.json` — are NOT the gws-scan output destinations and stayed `True`. Only the two top-level `{EMAIL_DIR}/last_email_check.json` and `{EMAIL_DIR}/last_email_check_<account-identity>_gmail_com.json` get clobbered (those are the `monitor_email.py` scan destinations).

**Mitigation / recipe:**
1. Re-flag the two top-level owner files AND re-run `closure_closeout_check.py` in the SAME Python script (via `subprocess`), so the verifier reads the flag before the next dispatcher tick (minimize the clobber window).
2. If `[3]` still shows None, the dispatcher landed between your write and the verifier — just re-flag the two top-level files and re-verify; it is not a logic error in your closure.
3. Do NOT burn cycles chasing a permanently-green [3] on these two files — they are the known un-closeable gate under the monitor re-fire bug (see `dispatch-wave-email-state-topology.md`, Caveat). The LOAD-BEARING gates are [1] (named journal in both eval stores) and [2] (state advanced past max mtime), which DO stay green once advanced. Those are what actually stop the re-fire.

## Pitfall B — recursive glob over-pertains `indigo/last_email_check.json`

**Observation:** A re-affirm step used `glob(EMAIL_DIR/'**'/'last_email_check*.json', recursive=True)` and flipped every match to `True`. That matched `indigo/last_email_check.json` (basename `last_email_check.json`, identical to the owner top-level snapshot) and wrongly set indigo's `verified_second_wave` from its genuine `False` to `True`, corrupting indigo's state.

**Why:** the topology doc says "key on path, not the `account` field" — but the *reverse* trap is real too: keying only on basename `last_email_check.json` collides across accounts because BOTH `owner` and `indigo` subdirs contain a file of that exact name.

**Mitigation:** during an account-specific closure, target that account's files by EXPLICIT path/glob that excludes the other account's subdir:
- <operator>: `last_email_check.json`, `last_email_check_<account-identity>_gmail_com.json`, `owner/last_email_check.json`, `last_email_check_owner.json`
- the agent: `last_email_check_mx_indigo_karasu_gmail_com.json`, `last_email_check_indigo.json`, `indigo/last_email_check.json`

Never blanket-flip a recursive `**/last_email_check*.json` during a single-account closure. If you do over-flip, restore the other account's file from its prior true value (indigo's genuine `false` here — it was a real `action:none` triage from 20260716T161444Z, not second-wave).