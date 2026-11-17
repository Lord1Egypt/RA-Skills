# Things that have actually gone wrong on real Kannaka nodes

Each of these cost someone hours. The script encodes the fix where it can; the rest are
here so you recognise them on sight.

**SELinux confines a binary by its label, not by the user.** A systemd unit that
executes `~/bin/kannaka` or `~/.local/bin/kannaka` on an Enforcing host runs in a
confined domain and gets `Permission denied` reading `~/.kannaka/config.toml` even with
perfect ownership and mode. Put the binary in `/usr/local/bin`, `restorecon` it, point
`ExecStart` there.

**`%h` in a system unit is root's home.** `%h`, `%u` and friends resolve before `User=`
applies. Write absolute paths in units installed under `/etc/systemd/system`.

**One writer.** The store has a single-writer lock. The listening node writes; a
concurrent `kannaka dream`, `remember` or `triage` from a shell contends with it. Read
with `KANNAKA_READONLY=1`; dream by stopping the node first (the timer does this); the
`serve` unit is read-only by construction.

**Never `cp` over a running binary.** The running process's file gets truncated under
it on some filesystems. `mv old old.previous && cp new old`, then restart. Same for
`kannaka update` on a box with a system copy: update `~/.local/bin`, then move-aside and
copy into `/usr/local/bin`.

**`git stash -u` sweeps the untracked service wrapper.** On nodes that run from a source
checkout, the runner script is deliberately untracked. A stash with `--include-untracked`
before a pull removed it twice and left the unit in a `status=127` restart loop that was
misdiagnosed as a memory leak for half an hour. Plain `git stash`, or commit it.

**fail2ban self-ban.** Many short ssh sessions in a row trip the sshd jail on the host,
even with successful logins, and the ban lasts an hour while every other service is
fine. Multiplex: `ssh -o ControlMaster=auto -o ControlPath=~/.ssh/cm-%r@%h -o
ControlPersist=10m`. If banned, do not reboot anything; verify the box through any
public surface it has and wait.

**`pkill -f` kills your own ssh.** `pkill -f "run.py"` matches the ssh command line
that contains `run.py`, kills the remote shell, and the rest of your command never
runs. Bracket the pattern: `pkill -f "[r]un.py"`.

**Credentials are shell input.** `~/.kannaka-nats.env` is sourced. An unquoted value
containing `$( )` executes. The script writes it single-quoted and refuses a password
that contains a single quote rather than writing it unsafely.

**Anonymous membership is quiet, not broken.** Without credentials the join succeeds,
phase is published, sync works, and the journal says the presence stream is
unavailable and that the node will not appear in `swarm peers`. The second half is
stale whenever the presence stream already exists on the bus, which on a running swarm
it does: the node is listed on other hosts. What the identity cannot do is create that
stream or `serve` recall. The `(unverified)` tag next to a peer is unrelated to
credentials: each host tags every peer missing from its own
`[swarm_trust].trusted_agents` allowlist that way. That is the expected shape; tell the
human, do not chase it.

**Disk full strands saves.** Atomic saves write `kannaka.hrm.tmp.*` then rename. On a
full disk the rename fails and the temp files stay, each the size of the store, making
the disk fuller. Free space, delete temps older than a few hours, then look at why the
store grew (usually a perception stream with no retention rule).

**`--version | head -1` says "Broken pipe".** The binary prints more than one line and
`head` closes the pipe. Harmless. Anything that *mutates* must never be piped into
`head`, for the same reason: it may be killed mid-write.

**The installer's rc file.** On a fresh account with no `.bashrc`/`.profile`, the
installer creates one so that `~/.local/bin` is on `PATH` for the next login. The unit
does not depend on `PATH` at all; it uses absolute paths.

**Your probes can have side effects.** `kannaka swarm join`, `listen` and `serve` do
not take `--help`; they run. Running them "to see the usage" on a host creates a store
and announces a random agent id on the bus. Read this skill instead.

## Re-running the installer while kannaka is running

Seen 2026-09-11 on a user's Ubuntu box. The user had `kannaka-tui` open; `install` re-ran the
installer, which downloads straight onto `~/.local/bin/kannaka`. Linux refuses to write an
executing file (`Text file busy`), the installer treated that as a failed download and removed
the destination, and the user's binary was gone until the installer ran again with nothing
holding the path, and the next run did the same to `kannaka-tui`. `provision.sh install`
now checks whether any of `~/.local/bin/{kannaka,kannaka-tui,kannaka-hdl}` is being
executed (`fuser`, else `/proc/*/exe`) and stops, naming the file, instead of running the
installer. It tests the files, not a process name, so the node service's copy in
`/usr/local/bin` never blocks an update. Before any install on a box a human uses
interactively: `fuser ~/.local/bin/kannaka*`.
