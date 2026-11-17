# Why it works this way (and the bugs that taught us)

Every rule here started as a real failure on a real Windows box running a
multi-agent assistant. They are written host-agnostically: the failure mode is
the same whether your stack is one process or twelve.

---

## 1. State file drives the watchdogs, not the switch command

**The design:** switching writes one file (`modes_state.json`), and both the
switcher and the watchdogs read that file to decide what *should* be running.
The mode is never passed to a watchdog as an argument, never stored in an env
var, never duplicated as a hardcoded list per script.

**Why:** the moment two components each hold their own idea of the current
mode, they fight. Real sequence that broke it:

1. You switch to `game`: the switcher stops the tunnel and the background agents.
2. A watchdog that hardcodes "work" (or was launched with the old mode) sees
   the tunnel down and helpfully reconnects it, then restarts the agents.
3. The user is back in work mode, on a tunnel they explicitly disabled, and
   nothing in the log says why.

**Write the state BEFORE mutating.** If the machine dies mid-switch (and it
will: killing a process that owns the network path can take the shell with it),
the state file already says "game", so every watchdog aims at the new mode
instead of resurrecting the old one. The reverse order leaves a window where a
half-switched machine is guarded by the old mode's rules — and that window is
exactly when things go wrong.

Corollary: the state file has **one writer per file**. The switcher owns
`modes_state.json`; each watchdog keeps its own counter/throttle file. Two
writers on one JSON file means lost updates — the throttle counter of one
writer overwrites the outage marker of the other, and a real outage gets
silently cleared.

Corollary: **read it fail-open, but validate the value domain.** A missing or
corrupt file falls back to a configured default mode. But an *unknown string*
must also fall back — if `"game "` (trailing space) or a half-written mode name
slips through, a watchdog that trusts it may decide "no VPN needed" and
disconnect a tunnel that every channel rides on.

---

## 2. PID files lie — verify before you trust one

`gateway.pid` (or any pidfile) is a hint, not a fact. Windows reuses PIDs
quickly, and a stale pidfile is indistinguishable from a healthy service if you
only ask "does this PID exist?":

* **False alive** → the switcher skips starting an agent that is not running.
  "Everything is up" and the user's assistant is simply gone.
* **False target** → the switcher sends a kill to a PID now owned by something
  entirely unrelated. This is the worse failure: you killed the wrong process.

Two checks close both:

1. the PID must exist, **and**
2. when the pidfile records a start time, it must match the live process's
   creation time within a tolerance (we use 300 s).

Watch out for **unit mismatch**: pidfiles record whatever the writer felt like
— epoch seconds, centiseconds, milliseconds. Compare against all three scales
(`t*1`, `t*10`, `t*1000`) or the start-time check silently never matches and
never fires. (This was a live bug for days: the guard existed and did nothing.)

If a pidfile has no start time at all, fall back to a PID-only check and accept
the reuse risk knowingly — do not delete a pidfile of a live instance. Deleting
it means the next instance cannot see the running one, so it either refuses to
start (conflict) or starts a duplicate; and if it refuses, nothing rewrites the
file, so the state you just deleted stays gone forever.

Always **re-check after killing** (poll for a few seconds). A `kill` that
returned 0 does not mean the process is gone, and the next step of the switch
usually assumes it is.

---

## 3. Stop by port or pidfile — never by process name

`pkill python`, `taskkill /IM python.exe`, "find everything named *agent*": all
of these eventually kill something that is not yours, including the process
doing the killing. The precise handles are:

* **by listening port** for services, with an **exact port match** —
  `:3001` must not match `:30010`. Split on the last `:` and compare the final
  token; a naive substring match on `:3001` kills the wrong service on a busy
  machine and the symptom is "my dashboard randomly dies when I switch modes".
* **by pidfile** for agents you wrote the pidfile for.

If a port is up but no owning PID can be found, leave it alone and say so in
the log. Guessing at that point is how a mode switch turns into a support
ticket.

---

## 4. VPN switching is the step that can cut your own throat

If the assistant's only channel to you (chat gateway, remote shell, tunnel) runs
**through** the VPN you are about to change, then:

* you may lose contact with the machine mid-switch, and
* if the switch dies there, the state file already says what you wanted (see §1)
  — which is the only reason this is recoverable.

Three rules fell out of that:

1. **`keep` is a first-class value.** Not every mode has an opinion about the
   tunnel. `vpn: keep` means "do not touch it", and it must be implemented as a
   genuine no-op, not as "compute a boolean and toggle".
2. **Ask the CLI what it thinks, then wait.** `connect` returns immediately;
   the tunnel is not up yet. Sleep a few seconds (`vpn.settle_s`) before any
   reachability probe, or the probe reports a false failure and the watchdog
   starts "repairing" a tunnel that is already coming up.
3. **A status query that fails is not "disconnected".** Three outcomes, not
   two: up / down / *unknown*. If the VPN service itself is dead, a two-state
   model reads "down" and reconnects forever, spamming alerts about a client
   that is not even running. Treat unknown as its own state, report it once,
   and don't act.

---

## 5. One-way watchdogs

The watchdog **starts** what should be running. It does not kill what should
not.

Reason: "should not be running" and "is running right now" are only the same
thing while the switcher is healthy. If the state file is stale, or the user
started something by hand, a watchdog with kill rights becomes a process
assassin that acts on information that is no longer true. Killing is the
switcher's job, and it kills only what the mode it was just told about excludes.

Also rate-limit repairs. A service that refuses to start will otherwise be
restarted every watchdog tick, and a per-minute cron turns into 1440 launches a
day, each one possibly leaving a zombie. We use "at most N repairs per hour",
with the timestamps kept in the watchdog's own state file; past the budget the
watchdog reports and waits.

---

## 6. Alerts must be honest and finite

* **The alert channel may be dead exactly when you need it.** If alerts go out
  through the same tunnel/network you are watching, the alert fails silently at
  the worst moment. Keep a second, dumber channel (a file on disk, a desktop
  notice) and make the primary best-effort. Never let a failed alert raise an
  exception and kill the watchdog.
* **One alert per incident, not per tick.** Track `reported` per incident and
  clear it on recovery, or a 20-minute outage produces 20 identical messages and
  the user stops reading them.
* **Retract the local marker on recovery.** A desktop "network is down" file
  that says it deletes itself when the network returns, but does not, is worse
  than no file at all — the user learns to ignore it.

---

## 7. Idempotence and cheap rounds

Every step must be safe to run twice and cheap when nothing changed:

* already running → log "running", touch nothing
* already stopped → log "offline", touch nothing
* a quiet round should repair nothing, call nothing remote, and alert nothing.
  It still prints one overview line and refreshes the watchdog's own counter
  file — that counter is its heartbeat, and without it a dead watchdog is
  indistinguishable from a quiet one. Otherwise the log is unreadable exactly
  when you need it, and the watchdog itself becomes a background load.

Probes that need the network are gated: probe only when a marker exists, a
failure count is non-zero, or the last probe is older than the cadence. "Poll
the world every tick" is how a watchdog turns into a source of outages instead
of a cure.

---

## 8. Launching background processes

* **Detach, and give up the console.** A background child that inherits a
  console window will pop a black window on every switch, or die when the
  parent's console closes.
* **Set the child's working directory.** Agents almost always resolve their own
  state relative to cwd; inheriting the switcher's cwd makes two instances of
  the same agent write to two different places.
* **Never pass a relative interpreter path.** "python" resolves to whatever is
  on PATH — the launcher shell's, the Windows Store stub, the wrong venv. Use
  an absolute interpreter path in the config, or you will spend an evening on
  "it runs when I launch it by hand".
* **Starting a process is not the same as it working.** After launch, verify by
  the same signal you will use later (port open, pidfile written) and log the
  result, including the negative case ("did NOT come up").

---

## 9. Distribution: keep the kit host-free

This kit has no machine names, no absolute paths, no personal identifiers and
no private job IDs in it. Everything host-specific lives in `modes.yaml`.

That is not politeness, it is a functional requirement: a template with a
personal path or hostname baked in is unusable for everyone else, and a leaked
path/ID in a published artifact cannot be unpublished. Put a real, runnable
fake-stack test in the kit (`--selftest`) so a stranger — and your reviewer —
can prove it works before editing a line of config.
