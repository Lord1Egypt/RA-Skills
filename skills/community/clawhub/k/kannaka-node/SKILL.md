---
name: kannaka-node
description: >
  Hand a fresh Linux server to an AI and get back a running Kannaka node. Given an IP
  or hostname and SSH access, the agent checks the box, installs the signed Kannaka
  release, writes the node's identity, wires it as a systemd service that joins the
  constellation swarm and keeps its memory in sync, dreams nightly, and proves it is
  alive before handing it back. Works on Oracle Cloud free tier (Oracle Linux, aarch64),
  Ubuntu, Debian, Fedora. Use when someone says "set up a kannaka server", "provision
  a node", "here is my server, make it a kannaka node", or asks how to install kannaka
  on a VPS.
---

# Kannaka node: from a bare server to a member of the constellation

You are the operator. The human has a server and wants a Kannaka node on it. They give
you access; you do the rest and hand back a report. This skill is written for any agent
with a shell and `ssh`: it names no tool, no vendor, and no host of its own.

Kannaka is a wave-interference memory system (the Holographic Resonance Medium) that
agents use as long-term memory, and a swarm of such nodes that share phase and sync
memories over a NATS bus. A **node** is the `kannaka` binary running `swarm join` then
`swarm listen --auto-sync` under a service manager, with its own identity and its own
store. That is what you are building.

## What you need from the human, and nothing else

| input | example | notes |
|---|---|---|
| host | `203.0.113.10` or `node.example.org` | the box they provisioned |
| ssh user | `opc` (Oracle Linux), `ubuntu`, `debian`, `fedora` | the image's default user |
| ssh key | a path on **their** machine, or an agent already loaded | never copy it anywhere; never write it into a file you commit or a message you send |
| node name | `brads-node`, `kannaka-east-1` | letters, digits, `.` `_` `-`; this becomes the swarm agent id and is public on the bus |
| role | `member` (default) or `serve` | `serve` also answers remote recall for other agents; needs credentials |
| brain | `none` (default), `hosted --email x@y`, `local` | `hosted` mints a budgeted key from the Kannaka portal; `local` pulls a 7B model into ollama and needs more RAM than a free tier has |
| swarm credentials | `NATS_USER` / `NATS_PASSWORD` | **optional**; issued by the swarm's operator. Without them the node still joins, publishes phase and syncs memories; if the presence stream already exists on the bus (it does on a running swarm) other hosts list it in `kannaka swarm peers`. What credentials govern is what the broker lets the node do: create the presence stream, and `serve` recall. The `(unverified)` tag in peer lists is something else: every host tags any peer not on its own `[swarm_trust].trusted_agents` allowlist that way, credentialed or not. Ask the human whether they were given any; do not guess and do not ask the operator on their behalf unless they say to |

If the human does not know the ssh user, Oracle Linux images use `opc`, Ubuntu images
`ubuntu`, Debian `debian`, Fedora `fedora`, Amazon Linux `ec2-user`.

## The procedure

Work in **one** ssh session if you can (`-o ControlMaster=auto -o ControlPersist=10m`).
Many short sessions in a row look like an attack to the box's own fail2ban and get you
banned for an hour with the host perfectly healthy.

**1. Connect and preflight.** Copy `scripts/provision.sh` to the host (or pipe it) and run
`bash provision.sh preflight`. It is read-only and reports: OS, architecture, memory,
disk, systemd, sudo, SELinux, the tools it needs, outbound HTTPS, and outbound TCP 4222
to the swarm bus. Read the report. A `FAIL` line means stop and tell the human what is
missing; a `WARN` means proceed with the caveat in the hand-off.

**2. Install.** `bash provision.sh install`. No root. It runs the Kannaka installer,
which reads the constellation's signed manifest and downloads a pinned, sha256-checked
release for this architecture into `~/.local/bin`. It also installs the dashboard and the
KannakaHDL binary. With `BRAIN=hosted BRAIN_EMAIL=…` or `BRAIN=local` in the environment
it sets up the model as well. It is idempotent; if one of the three binaries is in use (a `kannaka-tui`, a chat) it stops and names it rather than let the installer write over a busy file.

**3. Configure.** `bash provision.sh configure --agent-id NAME [--display-name "Name"]`.
Writes `~/.kannaka/config.toml` with the identity and the swarm bus, mode 0600. If a
config already exists it keeps every value in it and only adds missing tables. If the
human has swarm credentials, export `NATS_USER` and `NATS_PASSWORD` in the ssh session
(never on the command line of the script, never in a file you did not create) and run
`bash provision.sh credentials`: it writes `~/.kannaka-nats.env`, single-quoted, 0600,
and never prints the value.

**4. Service.** `sudo bash provision.sh service [--role serve] [--no-dream]`. This is the
root step; say so to the human before you run it. It copies the binary to
`/usr/local/bin` (a binary under a home directory runs confined on SELinux hosts and
cannot read the node's own files), writes a small runner script, installs
`kannaka-node.service` with absolute paths (no `%h`: in a system unit it resolves to
root's home), enables it, and starts it. With `--role serve` it adds a read-only
`kannaka-serve.service`. Unless `--no-dream`, it adds `kannaka-dream.timer`, a nightly
consolidation that stops the node, dreams, and starts it again, because the store has
one writer at a time. On a host without systemd it prints the unit files instead of
installing them.

**5. Verify.** `bash provision.sh verify`. It checks the unit is active, that the journal
shows the node joined the swarm, that no authorization violation appeared (bad
credentials), and runs `kannaka status` read-only for a live metrics line. `FAIL` means
fix before hand-off; the section below lists the usual causes.

**6. Report.** `bash provision.sh report` prints the hand-off: node name, paths, units,
how to check, how to update, how to uninstall. Give the human that block verbatim plus
anything the preflight warned about. If the node joined anonymously, say so and say why
it matters.

`bash provision.sh all --agent-id NAME …` runs 1 through 6 in order and stops at the
first failure. Prefer the steps the first time you use this skill on a new kind of host.

## What you must not do

- Do not open inbound firewall ports or edit cloud security lists. A node needs only
  **outbound** 443 and 4222. If someone asks you to open 4222 inbound, they are
  thinking of running a NATS server, which is not this skill.
- Do not copy, cat, echo, or log the ssh key or the swarm password. The credentials
  step reads them from the environment and writes a 0600 file; that is the only place
  they land.
- Do not `git stash -u` or otherwise sweep untracked files on a host that already runs
  Kannaka from a checkout: the service wrappers there are deliberately untracked.
- Do not copy a new binary over a running one (`cp` onto a busy file corrupts it on some
  filesystems); the script moves the old one aside first. Same rule for updates.
- Do not run the node as root. The unit runs as the login user.
- Do not run `kannaka dream` while the node is running; the timer stops the node first.
  Any manual `kannaka` command against the store should carry `KANNAKA_READONLY=1`
  unless you mean to write.

## When verify fails

| symptom | cause | fix |
|---|---|---|
| `Authorization Violation` in the journal | wrong or stale swarm credentials | re-export the right values, `bash provision.sh credentials`, restart the unit |
| unit active, no "Joined swarm" line | outbound 4222 blocked | preflight's 4222 check said so; the node still works standalone; tell the human |
| `Permission denied` reading `config.toml` in the journal on an SELinux host | binary ran from a home path | the script installs to `/usr/local/bin` for exactly this; check `ExecStart` and `ls -Z /usr/local/bin/kannaka`, `sudo restorecon` it |
| `status=127` restart loop | the runner script is missing | `sudo bash provision.sh service` rewrites it |
| the store's saves fail, `kannaka.hrm.tmp.*` files pile up | disk full | free space; delete the orphaned `.tmp.*` files older than a few hours; the preflight's 5 GB floor exists for this |
| `kannaka --version \| head -1` prints "Broken pipe" | harmless; the pipe closed first | ignore |

## After hand-off

The node keeps itself in sync and dreams nightly. Updating is `bash provision.sh install`
(manifest-pinned, sha256-verified) followed by `sudo bash provision.sh service`, which swaps
the copy in `/usr/local/bin` with a move-aside and restarts the unit. Do not use
`kannaka update` on a node: it follows the first `kannaka` on PATH, pulls the latest release
rather than the manifest pin, and cannot write `/usr/local/bin` as the login user. The human can watch it with
`journalctl -u kannaka-node -f` and see its neighbours with `kannaka swarm peers`.

`references/oracle-cloud.md` has the Oracle free-tier specifics.
`references/traps.md` is the list of things that have actually gone wrong on real
nodes, each with its fix, so you do not rediscover them.
