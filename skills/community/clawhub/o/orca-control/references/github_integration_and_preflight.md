# Orca GitHub Integration & Preflight Diagnostics

## Architecture Overview
Orca does not implement an isolated internal OAuth flow for GitHub; instead, its backend runtime (`orca-serve` / Electron process) invokes the system's GitHub CLI (`gh`) via preflight checks (`preflight.check` RPC).

The UI setup checklist and integrations page evaluate:
1. `gh.installed`: Whether the `gh` binary is accessible in PATH.
2. `gh.authenticated`: Exit status of `gh auth status`. If authenticated, UI displays "Connected" (`connected`). Otherwise, "Not Connected" (`not-authenticated`).

---

## Common Pitfalls & Solutions

### 1. User Context Mismatch (`orca` vs `root` / shell user)
* **Problem**: Running `gh auth login` as `root` (or regular SSH user) writes credentials to `/root/.config/gh/hosts.yml`. However, the Orca daemon (`orca-serve`) runs under the dedicated system user `orca` (`HOME=/home/orca`).
* **Fix**: Authenticate as the `orca` user or copy valid credentials:
```bash
# Option A: Login directly as user orca
su - orca -s /bin/bash -c "gh auth login"

# Option B: Copy existing hosts.yml from root
mkdir -p /home/orca/.config/gh
cp /root/.config/gh/hosts.yml /home/orca/.config/gh/hosts.yml
chown -R orca:orca /home/orca/.config/gh
chmod 600 /home/orca/.config/gh/hosts.yml

# Setup Git credential helper for user orca
su - orca -s /bin/bash -c "gh auth setup-git"
```

### 2. In-Memory Preflight Cache
* **Problem**: The Orca server caches preflight results in memory (`cached$1`). If `gh auth login` is performed while `orca-serve` is already running, the UI continues showing "Not Connected" until the cache expires or is invalidated.
* **Fix**: Restart the service or trigger a forced preflight check:
```bash
systemctl restart orca-serve
```
Or trigger forced preflight via Node.js runtime RPC:
```bash
node -e "
const { RuntimeClient } = require('/opt/orca/squashfs-root/resources/app.asar.unpacked/out/cli/runtime-client.js');
process.env.HOME = '/home/orca';
const client = new RuntimeClient();
client.call('preflight.check', { force: true }).then(r => console.log('Preflight status:', r.gh));
"
```

### 3. Projects Showing `no-provider`
* **Problem**: In `orca project list`, a project displays `no-provider` instead of GitHub integration details.
* **Reason**: Orca determines provider identity from git remotes (`origin`). If the directory has no remote or if `git config --global --add safe.directory <path>` is missing, Orca treats it as a generic folder without GitHub repo linking.
* **Fix**:
```bash
# Add safe directory for user orca
su - orca -s /bin/bash -c "git config --global --add safe.directory /path/to/project"

# Ensure git origin remote points to GitHub
cd /path/to/project
git remote add origin https://github.com/<owner>/<repo>.git
```

### 4. Orca Desktop (Local Machine) vs Remote Server
* If using the Orca Desktop App installed locally on macOS/Windows, the app checks `gh auth status` on the local workstation by default. Ensure `gh auth login` is completed on the local machine if working with local environments.
