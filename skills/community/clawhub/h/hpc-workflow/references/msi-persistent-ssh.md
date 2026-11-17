# MSI: authenticate once, reuse the connection

This guide describes the transport used by the source MSI installation and how
an agent can adapt it to another user's environment. A trusted, always-on Linux
host retains the authenticated MSI SSH connection. The desktop opens short SSH
calls to that host, which opens channels on the existing MSI connection.

```text
Desktop agent
  -> SSH to an always-on host on the permitted network
       -> tmux msi-transport:ssh
            -> foreground OpenSSH master to one MSI login node
                 -> login tmux: control + GPU allocation holder
                      -> allocated node: job-specific compute tmux
                           -> setup, autosave, named experiment windows
```

The source installation uses native Windows OpenSSH and an always-on lab server.
The agent stays on the desktop. The transport tmux runs on the lab server; login
and compute tmux run on MSI. Closing the desktop terminal or shutting down the
desktop does not own the lab server's SSH process. A healthy retained connection
lets subsequent commands reuse the completed authentication.

## Establish the actual route

Read MSI's [connection requirements](https://msi.umn.edu/getting-started/connecting/connecting-to-msi-systems)
and [SSH key guide](https://msi.umn.edu/getting-started/getting-started-and-access/interactive-connections-faqs/how-do-i-set-up-ssh-keys).
MSI documents campus/VPN access and Duo, including Duo when using registered SSH
keys. A public VPS is not automatically an eligible jump host. Establish a
permitted network route and the user's key registration before adapting this
pattern. Reusing an authenticated connection does not change the site's access
or authentication policy.

Record these facts privately:

- Desktop-to-holder SSH alias, owner and authentication method.
- Holder hostname, network access, OpenSSH/tmux versions and uptime expectations.
- MSI user and a permitted, named login node. The source route pins a named node;
  other users must verify their own node and shared-home service requirements.
- Private configuration, key and control-socket paths on the holder.
- Who performs explicit login, where prompts appear and when an attempt expires.
- The supported ordinary-command wrapper and its no-new-authentication behavior.

`ProxyJump` can provide network routing, but a master running on the desktop still
belongs to the desktop. To retain it across desktop shutdown, run the master on
the always-on host. The desktop and holder authenticate their own respective hops.
Do not depend on forwarding a laptop's SSH agent to keep the holder usable.

## Holder configuration template

All following shell commands run on the holder unless explicitly marked as
desktop commands. Substitute the uppercase placeholders in private files. Merge
with an existing supported installation; do not replace a healthy holder.

Create owner-only directories:

```bash
install -d -m 700 "$HOME/.config/hpc-agent-kit" "$HOME/.ssh/msi-control"
```

Store this in `~/.config/hpc-agent-kit/msi-ssh.conf`:

```sshconfig
Host msi-held
    HostName NAMED_LOGIN_NODE.msi.umn.edu
    User YOUR_MSI_USER
    IdentityFile ~/.ssh/YOUR_REGISTERED_MSI_KEY
    IdentitiesOnly yes
    ControlPath ~/.ssh/msi-control/master.sock
    ControlMaster no
    ControlPersist no
    ServerAliveInterval 30
    ServerAliveCountMax 6
    ConnectTimeout 15
    ForwardAgent no
    StrictHostKeyChecking yes
```

Verify the login node's host key through the site's trusted channel and the
user's normal interactive connection before using `StrictHostKeyChecking yes`.
Keep the configuration and private key mode 600. The socket directory is mode
700: access to the control socket grants use of the authenticated connection.
Choose an available private directory if the suggested path already has another
owner or purpose.

The explicit `ssh -M` below overrides `ControlMaster no` for the holder process.
`ControlPersist no` keeps that process in its tmux pane. Ordinary clients cannot
elect themselves as a new master. See the OpenSSH
[ControlMaster](https://man.openbsd.org/ssh_config.5#ControlMaster),
[ControlPersist](https://man.openbsd.org/ssh_config.5#ControlPersist) and
[ServerAliveInterval](https://man.openbsd.org/ssh_config.5#ServerAliveInterval)
documentation. Keepalive settings detect a broken connection; they cannot
preserve it through host restart, network loss or server-side expiry.

## Explicit login owns authentication

First check the existing master and inspect any existing transport pane:

```bash
ssh -F "$HOME/.config/hpc-agent-kit/msi-ssh.conf" -O check msi-held
tmux -L msi-transport list-windows -a
```

If the master is healthy, reuse it. If the pane is waiting for authentication,
complete that attempt; do not start another. Only after an explicitly requested
login and an inspection showing no healthy or pending holder, create a new one:

```bash
tmux -L msi-transport new-session -d -s msi-transport -n ssh \
  'exec ssh -F "$HOME/.config/hpc-agent-kit/msi-ssh.conf" -M -N msi-held'
```

From the desktop, attach to the holder's prompt using the user's existing alias:

```bash
ssh -tt hpc-jump 'tmux -L msi-transport attach-session -t msi-transport'
```

The user completes any key passphrase, password and Duo interaction in this
terminal. Detach with tmux's `Ctrl-b d`; keep the SSH process running. Confirm
success with `ssh ... -O check` and an actual MSI `hostname`/`id` probe. Merely
seeing a tmux pane or a Duo notification does not establish authentication.

An agent login helper must serialize attempts and inspect only output produced
after the current attempt's marker. It may request one Duo Push, notify the user
immediately when the server confirms it, and allow the stated approval window
(the source workflow uses 60 seconds). On timeout it returns a failure without
another automatic attempt. Do not put passwords or MFA responses in scripts,
profiles, repository files or captured support reports.

## Ordinary calls reuse the master and fail closed

Use the existing site shim when there is one. For a new installation, this
minimal holder-side wrapper shows the required boundary. Save it as
`~/.config/hpc-agent-kit/msi-exec`, mode 700:

```bash
#!/usr/bin/env bash
set -euo pipefail
conf="$HOME/.config/hpc-agent-kit/msi-ssh.conf"
if ! ssh -F "$conf" -O check msi-held >/dev/null 2>&1; then
    printf 'MSI_MASTER_UNAVAILABLE: explicit login required\n' >&2
    exit 3
fi
if (($# == 0)); then
    printf 'Usage: msi-exec COMMAND [ARG...]\n' >&2
    exit 2
fi
printf -v command '%q ' "$@"
exec ssh -F "$conf" -o BatchMode=yes -o ControlMaster=no \
    -o PubkeyAuthentication=no -o HostbasedAuthentication=no \
    -o KbdInteractiveAuthentication=no -o PasswordAuthentication=no \
    -o GSSAPIAuthentication=no msi-held "$command"
```

This wrapper requires Bash on the holder and the MSI command shell. It returns
the remote exit status and forwards stdin/stdout. Literal arguments are quoted
once for the remote shell. For a deployment script on stdin, an example private
profile transport is:

```json
{
  "exec_argv": [
    "ssh", "-o", "BatchMode=yes", "hpc-jump",
    "~/.config/hpc-agent-kit/msi-exec bash -s"
  ]
}
```

This is the `transport` object, not a complete site profile. The desktop's
`hpc-jump` alias belongs to that user; it is not shipped in this repository.
Probe the route with a small identity script before applying a rendered bundle.
For an existing exec/push CLI, use
[`common/shim_exec.py`](../scripts/common/shim_exec.py) as described in
[site probing](site-probing.md).

The source Windows workflow provides `msi login`, `msi exec`, `msi status`,
`msi doctor` and GPU/task commands. Those private native entry shims are not
included in this generic release. An agent creates the user's entry wrapper
around their verified route and the rendered helpers; copying the name `msi`
does not establish a connection. Public profile deployment needs the stdin
transport above, not our private lab host, usernames or keys.

## Recovery and connection capacity

| Observation | Action |
| --- | --- |
| Desktop disconnected; holder master healthy | Reconnect to the holder and reuse the master; inspect queue and routes. |
| Master absent or broken | Ordinary calls return failure. Inspect the transport pane; explicit login may create one new attempt. |
| Authentication pending or timed out | Complete the pending attempt or report its timeout; do not automatically send another Push. |
| Holder restarted or MSI closed the connection | Reauthenticate explicitly, then inspect the existing jobs and tmux hierarchy. |
| Multiplexed channel refused or commands saturate the connection | Bound Agent concurrency and close completed client channels. Record the site's actual channel limits; never fall back to a fresh authenticated connection. |
| SSH recovered, but an allocation holder or compute route is missing | Reconcile the durable request ID with Slurm and the existing tmux state before any replacement allocation. |

Keep SSH transport recovery, Slurm allocation ownership and workspace backup
recovery separate. Retaining an SSH connection does not extend a job's walltime;
losing it does not prove a job ended. Restore only verified, committed workspace
snapshots. Experiment resume requires its own complete checkpoint.

When adapting the pattern, verify that two independent ordinary calls use the
same master, that a disposable client's disconnect leaves it alive, and that
a missing master causes failure with no new authentication. Test connection
loss only against an isolated holder; never terminate the user's healthy master
as a test. Record observed host identities and pending checks in private notes.

## Smaller alternative: local ControlPersist

On a Linux/macOS desktop with a proven SSH route, `ControlMaster auto`, a private
`ControlPath` and `ControlPersist 10m` can retain an idle master after a terminal
closes. It expires after the configured idle interval and belongs to that
desktop. This is useful when desktop lifetime is sufficient. The always-on
holder pattern moves connection ownership away from the desktop and adds an
explicit login/ordinary-call boundary. Choose the variant that matches the
user's actual reliability requirements and permitted access.
