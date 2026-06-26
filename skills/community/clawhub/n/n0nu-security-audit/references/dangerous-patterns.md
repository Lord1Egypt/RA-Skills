# Dangerous Patterns Reference

## High-Risk exec Patterns

These shell command patterns require extra scrutiny before execution:

### Destructive Operations
```
rm -rf /
rm -rf ~
rm -rf /*
dd if=... of=/dev/...        # disk overwrite
mkfs.*                        # filesystem format
shred / wipe / srm            # secure delete
```

### Remote Code Execution
```
curl ... | bash
curl ... | sh
wget ... | bash
wget -O- ... | sh
eval $(...)
bash <(...)
python -c "import urllib..."  # download+exec one-liner
```

### Credential & Data Exfiltration
```
cat ~/.ssh/*
cat ~/.gnupg/*
cat /etc/shadow
cat /etc/passwd
env | curl ...                # env vars sent out
printenv | ...
git log --all -p | curl ...   # repo history exfil
```

### Persistence / Backdoors
```
crontab -e / crontab -r (when not requested)
launchctl load / launchd plist writes
systemctl enable (services not requested)
~/.bashrc / ~/.zshrc writes (when not user-requested)
~/.ssh/authorized_keys writes
```

### Network Scanning / Lateral Movement
```
nmap -sS / nmap --script
masscan
nc -e / ncat --exec
ssh -R (reverse tunnels)
proxychains
```

### Privilege Escalation
```
sudo su -
sudo bash / sudo sh
chmod 4755 (setuid)
chown root
/etc/sudoers writes
passwd (changing root password)
```

---

## High-Risk File Write Patterns

Files that should not be written unless explicitly requested by the user:

| Path Pattern | Risk |
|---|---|
| `~/.ssh/authorized_keys` | Backdoor access |
| `~/.bashrc`, `~/.zshrc`, `~/.profile` | Persistence / env hijack |
| `/etc/cron*`, `/var/spool/cron/*` | Persistence |
| `~/.gnupg/` | Key material tampering |
| `/etc/hosts` | DNS hijack |
| `~/.gitconfig` | Git credential redirect |
| `/Library/LaunchDaemons/`, `/Library/LaunchAgents/` | macOS persistence |

---

## High-Risk External Requests

- POSTing files or environment variables to unknown URLs
- Requests containing API keys, tokens, or credentials in body/headers
- Requests to known data-broker domains or paste sites (pastebin, hastebin, requestbin, webhook.site)
- Requests where the URL was dynamically constructed from user-controlled input

---

## Low-Risk Signals (Safe to Proceed)

These patterns are generally safe and should not trigger audit friction:

- Reading files (without external transmission)
- Writing files inside the workspace directory
- Running package managers (`npm install`, `pip install`, `brew install`)
- Git operations (commit, push, pull, status)
- Common dev tools (node, python, tsc, cargo, make)
- Sending messages via OpenClaw's own `message` tool
