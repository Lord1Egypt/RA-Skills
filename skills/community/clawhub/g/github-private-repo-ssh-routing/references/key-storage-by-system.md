# Key Storage by System

Keep one rule across systems: private keys live in the user's SSH directory, not in repos, sync folders, downloads, desktop folders, or plaintext backups.

## Linux

Store keys in:

```bash
~/.ssh/
```

Typical files:

- `~/.ssh/config`
- `~/.ssh/known_hosts`
- `~/.ssh/<private-key>`
- `~/.ssh/<private-key>.pub`

Permissions baseline:

- `~/.ssh` = `700`
- private keys = `600`
- `config` = `600`
- public keys = `644`

Use purpose-based names on servers, for example:

- `github_backup_srv656743_ed25519`
- `github_plugins_srv656743_ed25519`

## macOS

Use the same location:

```bash
~/.ssh/
```

When passphrase-backed keys are used regularly, Keychain integration is often the least painful setup:

```ssh
Host github.com-backup
    HostName github.com
    User git
    IdentityFile ~/.ssh/github_backup_ed25519
    IdentitiesOnly yes
    AddKeysToAgent yes
    UseKeychain yes
```

Avoid storing private keys in iCloud Drive, Desktop, or Documents.

## Windows

### Native OpenSSH

Store keys in:

```powershell
C:\Users\<user>\.ssh\
```

### WSL

Store keys in the Linux home directory used by WSL Git/SSH:

```bash
~/.ssh/
```

Do not casually mix Windows `.ssh` and WSL `.ssh` in the same workflow.
If Git runs in WSL, prefer WSL-managed keys unless there is a deliberate bridge.

## Multi-machine rule

Prefer one private key per machine and per repo/use-case.
Do not copy the same private key across many systems unless there is a very deliberate reason.

Use names that reflect machine or purpose, for example:

- `github_backup_macbook_ed25519`
- `github_backup_wsl_ed25519`
- `github_work_laptop_ed25519`

## Never do this

- commit private keys into a repo
- put private keys in Dropbox / iCloud / Google Drive sync folders
- keep `.txt` copies of private keys
- leave private keys in downloads or temp folders
- assume Windows OpenSSH, WSL OpenSSH, and Git Bash all share one clean SSH environment
