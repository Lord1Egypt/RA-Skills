---
name: innerwarden-security
description: Install, verify and run InnerWarden on the machine this OpenClaw agent runs on. InnerWarden Community (free, 1.6.11 or newer) screens this agent's own exec, process, write, edit and apply_patch calls before they run, through its innerwarden-guard plugin on OpenClaw's before_tool_call hook (OpenClaw 2026.9.7 or newer), and the calls it makes to its MCP servers through the proxy. Monitor first; enforce is the owner's choice. InnerWarden Pro (paid, Linux) adds the host layer with the kernel Execution Gate. Use when your owner asks to install InnerWarden, check what it protects here, see what it refused, ask whether a command is safe to run, turn on enforce, upgrade it, or remove it.
user-invocable: true
metadata: {"openclaw":{"always":false,"emoji":"🛡️","requires":{"bins":["curl"]},"os":["linux","darwin"]}}
---

# InnerWarden, from inside OpenClaw

InnerWarden puts a verdict (**allow**, **review** or **deny**, with reasons) in
front of what an AI agent tries to run. You are that agent. This skill helps
your owner install it, prove it works, and run it, without you ever weakening
it.

Full documentation, kept current: <https://github.com/InnerWarden/innerwarden-skill>.
Read `--help` on the installed binary before trusting any list, including this
one.

## Your rules, before anything else

1. **Never lower, pause, remove or loosen the guard yourself.** Monitor mode,
   disconnecting, `allow`, `mute`, `contain`, disarming a kernel control,
   stopping InnerWarden's services and uninstalling are your owner's to type,
   in their own terminal. Give them the exact line and one sentence on why, and
   wait. If a command is refused, do not retry it another way: no unset
   variables, no wrapper scripts, no other launcher. One exception: Community
   1.6.12 or newer also refuses, with the same message, a line that names
   InnerWarden's tools and runs a program from a variable (`$TOOL ...`),
   because it cannot read which program runs. Write that line with the
   program named in plain sight and run it again; if the plain line is
   refused too, it is your owner's. Never touch the
   `innerwarden-guard` plugin: its files in `~/.openclaw/extensions`, its
   entry in `openclaw.json`, or OpenClaw's commands that disable or remove a
   plugin. In enforce it refuses that anyway.
2. **Ask before installing anything.** Show your owner the command first.
3. **Never ask for a password, a private key or an API token**, and never echo
   one back. Hand your owner the command that needs it.
4. **Never use `curl -k`** against InnerWarden: if its certificate does not
   verify, treat the answer as `review`.

## What it is

| | what it protects | where |
|---|---|---|
| **InnerWarden Community** (free, Apache-2.0) | for OpenClaw (Community 1.6.11 or newer, OpenClaw 2026.9.7 or newer): its own `exec`, `process`, `write`, `edit` and `apply_patch` through the plugin `innerwarden-guard`, and calls to its MCP servers through the proxy (section 3) | Linux, macOS (Windows experimental) |
| **InnerWarden Pro** (paid, per protected agent, <https://innerwarden.com/pricing>) | the host underneath: sensor, detectors, response, and the kernel Execution Gate, Secret Read Guard and DNS Guard | Linux only |

Pro is source-available and paid, not open source; only Community is. Kernel
enforcement exists on Linux only. InnerWarden is not an EDR replacement and not
a compliance certificate.

## 1. See what is there

```sh
command -v innerwarden && innerwarden --version        # Community (also names Pro if present)
command -v innerwarden-ctl && innerwarden-ctl --version # Pro host layer
innerwarden agents list                                # is openclaw guarded, and how; "OpenClaw's own tools: screened, <mode>"
innerwarden status                                     # is it on (its OpenClaw coverage line is wrong from 1.6.11 to 1.6.13, section 3)
```

## 2. Install Community (with your owner's OK)

```sh
curl -fsSL https://innerwarden.com/free | sh    # signed binary, checked before install, no root, ~/.local/bin
innerwarden --version                           # 1.6.11 or newer screens your own tools
```

An older one upgrades with `innerwarden upgrade` (your owner's OK first).

If it is not found afterwards, `~/.local/bin` is not on PATH: call it as
`~/.local/bin/innerwarden`, and tell your owner to add `~/.local/bin` to PATH.

## 3. Wire OpenClaw, and say exactly what that covers

Put the choice to your owner:

- **Monitor first (recommended for a week):** they run, in their own terminal,
  `innerwarden agents connect openclaw --monitor`. It records and refuses
  nothing.
- **Enforce now:** you may run `innerwarden agents connect openclaw` and then
  `innerwarden enforce`, once they have chosen it (`connect` alone leaves the
  plugin in monitor).

Either way `connect` installs the plugin `innerwarden-guard` in **monitor**
(it records what enforce would refuse and refuses nothing) and wraps the local
MCP servers in `~/.openclaw/openclaw.json`. Then your owner restarts the
OpenClaw gateway ("Quit OpenClaw and start it again"): the gateway loads the
plugin, and reads its mode, only when it starts. The same restart follows
`innerwarden enforce` and `innerwarden dry-run`. Restarting it yourself ends
this conversation before you can report.

**What this covers for OpenClaw, in plain words:**

- **Your own tools.** Each call to `exec`, `process`, `write`, `edit` and
  `apply_patch` is screened before it runs, on OpenClaw 2026.9.7 or newer.
  In enforce a denied call does not run and you are told only "Refused by
  InnerWarden."; a review asks your owner to allow it once or deny it, and no
  answer is a refusal. In enforce the plugin also refuses any attempt to
  remove, disable or rewrite it. Since 1.6.11 the CLI also recognises your
  exec shell as an agent's, so the commands that lower the guard refuse there.
  Since 1.6.13 the same rules, in enforce, also refuse starting another agent
  without the hook that screens it, and a container that hands an agent the
  host. Those are your owner's.
- **Your MCP servers.** Calls to them go through InnerWarden's proxy, and
  since 1.6.13 so does what the servers send back and list: in enforce a
  secret-shaped value in an answer is masked, and a description that gives
  you orders is replaced with a short notice. If `openclaw.json` has no local
  MCP servers, `connect` says so and still installs the plugin.
- **The limits, which you say too.** The plugin runs inside the OpenClaw
  gateway process, so it is as trustworthy as that process. A `write` or
  `edit` with a relative path is judged from the gateway's working directory.
  Your other tools, your own file reads among them, are not screened by it.
  On an OpenClaw older than 2026.9.7, do not describe your own tools as
  screened.

`innerwarden status` from 1.6.11 to 1.6.13 still says "Its built-in tools are
not screened by this edition" for OpenClaw, even with the plugin installed. That is a known
error: do not repeat it. The accurate line is the one `innerwarden agents list`
prints, "OpenClaw's own tools: screened, monitor" (or `enforce`).

Optional, for the record: `innerwarden observe install` (your owner runs it,
then restarts the gateway) records dangerous asks that reach you in
conversation, including ones you refuse. It is observation, not enforcement.
It grants a small plugin `allowConversationAccess`; tell your owner that before
they agree.

## 4. Prove it

```sh
innerwarden check "rm -rf /"       # must come back deny
innerwarden check "ls -la"         # must come back allow
innerwarden agents list            # "OpenClaw's own tools: screened, monitor|enforce"
```

For the full proof, your owner can run `scripts/verify-install.sh` from
<https://github.com/InnerWarden/innerwarden-skill>. Its last step, after the
gateway restart, is for you to run `echo <the token it prints>` with your own
`exec` tool: the plugin screens it, and the script finds it in the record. Do
not report "protected" until that run says "Screening confirmed".

## 5. Ask before you act

Your own tools are screened by the plugin, and in monitor nothing is refused
yet. You can still choose to ask before a command that could do damage:

```sh
innerwarden check "<the exact command>"
```

On a Pro host the same question goes to the host, which also knows what has
happened on it today:

```sh
curl -s --cacert /var/lib/innerwarden/dashboard-cert.pem \
  -X POST https://127.0.0.1:8787/api/agent/check-command \
  -H 'content-type: application/json' \
  -d '{"command": "<the exact command>", "agent_name": "openclaw"}'
```

- `deny`: do not run it. Tell your owner what you were about to do and why it
  was refused.
- `review`: ask your owner before running it.
- `allow`: it matched no rule. That is not a safety judgement; use your own.
- No answer, an error or a certificate failure: treat it as `review`.

Asking is a habit, not a control: it only covers what you remember to ask
about. The control is the guard itself, and on Linux with Pro, the kernel.

## 6. Day to day, for your owner

```sh
innerwarden agents list       # what is guarded, and the plugin's mode
innerwarden graph             # what was screened, and how each ended
innerwarden notify --test     # do alerts arrive (your owner sets the channel)
innerwarden enforce           # when your owner decides: denials become real; then they restart OpenClaw
innerwarden upgrade --check   # is there a newer release
```

A verdict your owner disagrees with is theirs to teach, at their own terminal:
`innerwarden allow "<glob>"`. Going back to monitor (`innerwarden dry-run`) is
theirs too.

## 7. InnerWarden Pro on a Linux host

Installing Pro needs the licence file from the purchase email and root, and it
can edit the bootloader (with a reboot your owner decides on). It is your
owner's step, or a coding agent's following
<https://github.com/InnerWarden/innerwarden-skill/blob/master/docs/pro-on-a-server.md>.
A host that must send nothing out has an opt-in offline mode since Pro
0.17.19; that page says how, and what it does not cover yet.

Once Pro is there, it can follow OpenClaw's gateway (your owner runs this):

```sh
sudo innerwarden-ctl agent connect --unit <OpenClaw's systemd unit>
```

That scopes the Execution Gate and the userns guard to OpenClaw. Armed in
enforce, the Execution Gate then refuses, in the kernel, a program OpenClaw's
processes try to run that was not authorised in advance, whichever tool started
it. In observe or rehearse it records and blocks nothing. Arming
is a deliberate step after a week of watching; read
<https://github.com/InnerWarden/innerwarden-skill/blob/master/docs/managing-pro.md>.
Health on a Pro host: `sudo innerwarden-ctl get status` and
`sudo innerwarden-ctl arm --check` (the second changes nothing).

Since Pro 0.17.19 `agent connect` also prints a line saying agent profiles
are off. That is the default, and they are a preview: turning them on is your
owner's choice. Do not turn them on or suggest it.

## 8. Removing it

Your owner runs these, in this order:

```sh
innerwarden agents disconnect --all   # first, while the binary exists: it also takes the plugin out
# restart OpenClaw
innerwarden uninstall
rm -rf ~/.config/innerwarden
```

The order matters here: `innerwarden uninstall` leaves the plugin in place, and
in enforce a plugin that cannot reach the binary refuses every one of your own
tool calls.

On a Pro host, every kernel control comes off first (the full list is in
<https://github.com/InnerWarden/innerwarden-skill/blob/master/docs/managing-pro.md>,
"Removing it"), then `sudo innerwarden-ctl uninstall`.
