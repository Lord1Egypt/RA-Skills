# Operations, release, and acceptance guide

## Contents

1. Scope and requirements
2. Install and connect
3. Remote Ubuntu / SSH
4. Everyday use and background checks
5. Privacy and trust boundaries
6. Recovery and uninstall
7. Publishing
8. Acceptance gates
9. Sources

## 1. Scope and requirements

Release: 0.1.3 preview. Target: Ubuntu 22.04/24.04/26.04 with Python 3.10+, an existing OpenClaw installation, and host execution access under the same Unix account. OpenClaw's latest published release resolved to 2026.9.6 on 2026-09-26. This code uses the Agent Skills folder contract and ordinary host exec, not the gateway plugin API. There was no live OpenClaw or Gmail account available in the build environment, so those platforms remain acceptance-test targets rather than certified configurations.

This is a working source implementation of the recommended **direct Gmail API** path. Google project and consent configuration stay in the Google website. OAuth uses a Desktop client, PKCE, a short-lived state value, and a loopback callback. No Tailscale, public ingress, Pub/Sub, gog, gcloud, npm packages, Python packages, or OpenClaw configuration changes are required for this mode.

The wizard does not repair an already broken gateway. Diagnose and restore that gateway separately before claiming the overall assistant is working.

## 2. Install and connect

From an extracted source directory containing `gmail-connect/SKILL.md`:

```bash
openclaw skills install ./gmail-connect
```

This uses OpenClaw's own local skill installer. Check any install-policy warnings; do not bypass them automatically. Use `openclaw skills info gmail-connect` to locate the installed skill. Ask the assistant: **“Use Gmail Connect to connect my Gmail account.”** It launches the wizard, which opens a local browser. If automatic launch is unavailable, run:

```bash
python3 /ABSOLUTE/INSTALLED/SKILL/PATH/scripts/gmail_connect.py wizard
```

Keep that process alive during setup. This one launcher is the only routine terminal command after installation. Do not run it with sudo. If port 8766 is occupied, use `wizard --port 8767`; do not kill an unknown listener.

After this skill is actually published, installation becomes:

```bash
openclaw skills install @YOUR_CLAWHUB_OWNER/gmail-connect --version 0.1.3
```

The owner is a placeholder. No ClawHub listing is claimed to exist.

In the wizard:

1. Open Google Cloud and create or choose your project. Enter its actual project ID.
2. Follow the Gmail API link and enable it in that same project.
3. Complete Google Auth Platform branding, audience and data access. For a personal Gmail account use External. If in Testing, add your account as a test user. Request `gmail.readonly`; optionally request `gmail.send`.
4. Create a Desktop app OAuth client and download the JSON. The wizard rejects Web clients and service accounts.
5. Upload the JSON directly to the local wizard. Click Connect with Google, choose the intended mailbox, and approve scopes. Return to the original tab and refresh status.
6. Confirm the displayed account. Click Verify Gmail, then ask OpenClaw to search one known email. These are distinct verification steps.
7. Optionally enable background checks. No sending occurs during verification.

Google may require a Workspace administrator's approval or restrict an organizational project. Do not work around organization policy. External Testing refresh tokens with Gmail scopes normally expire after seven days. Production status can remove that specific testing lifetime, but is not a promise of permanent credentials or a substitute for Google's verification requirements. Reauthorization is a normal recovery path after revocation or expiry.

Every person who installs this release supplies their own Desktop client. A universal “Sign in with Google” app would require a publisher-operated OAuth project, suitable consent/verification and distribution arrangements, privacy documentation, and potentially additional restricted-scope obligations. No shared OAuth client or secret is bundled.

## 3. Remote Ubuntu / SSH

The browser's `127.0.0.1` must reach the Ubuntu wizard. A browser inside NoMachine on Ubuntu is the simplest route.

For a browser on a separate Windows, macOS, or Linux workstation, open a local SSH forward on that workstation:

```bash
ssh -N -L 8766:127.0.0.1:8766 YOUR_USER@YOUR_UBUNTU_HOST
```

Then launch the Ubuntu wizard with `--no-browser`, and open its printed private URL in the workstation browser. Use the same local and remote port. Keep the SSH session and wizard running through the OAuth callback. If changing ports, change both sides and `wizard --port` consistently. Never bind the wizard to `0.0.0.0`, publish it with Funnel, or paste its private capability link into a public chat.

## 4. Everyday use and background checks

The CLI provides status, live profile check, search with pagination, plain-text reads, local draft creation, history synchronization, and a recent-events feed. `python3 scripts/gmail_connect.py --help` lists commands.

The optional monitor is a separate **user service**, `openclaw-gmail-connect.service`. It checks about every 60 seconds, slows down on provider/network errors, and stops without tying up OpenClaw's gateway shutdown. It binds no port. The browser wizard need not remain open after setup.

The monitor is not a scheduler for model runs or a Telegram delivery service. For proactive notifications, configure OpenClaw's heartbeat or automation through its current UI, select a known private destination, and instruct it to read `events`, ignore snapshot records, deduplicate message IDs, and summarize without obeying email instructions. The skill deliberately does not create this external messaging automation silently.

The first connection and a lost-history recovery capture up to 100 recent inbox messages. Ordinary checks page through history, recording newly observed inbox messages. The local feed retains at most 5,000 records for at most 30 days and is not a mail archive, full replica, or exactly-once queue. Search/read fetch Gmail directly. Older mail can be searched even when absent from the feed.

User services normally follow the user login manager. Optional unattended boot support requires the user's terminal:

```bash
sudo loginctl enable-linger "$USER"
```

This does not prevent suspend, restore internet, or change gateway startup settings. A laptop can miss timely alerts while asleep; history catch-up happens after resuming, subject to Google's retention.

## 5. Privacy and trust boundaries

State defaults to `~/.local/share/openclaw-gmail-connect/`. `GMAIL_CONNECT_HOME` is an optional override and must stay outside the skill's distributed folder. The directory is mode 0700; credential files are atomic mode-0600 writes. Tokens are **not encrypted at rest**. Use Ubuntu disk encryption if needed; do not describe Unix file permissions as encryption.

Secrets are never returned by the diagnostic CLI, wizard status API, or callback logs. The UI loads no CDN assets. It binds only IPv4 loopback, validates Host and Origin, requires a per-launch bearer capability for API requests, disallows framing, and renders email only as text. Google endpoint URLs are fixed in code, rather than trusted from imported JSON. Proxy environment variables are ignored for authenticated Google requests; corporate networks requiring an outbound proxy need a reviewed deployment adaptation.

Read-only permission is the default. Optional sending grants only the additional `gmail.send` scope; Gmail modify/delete scopes are not requested. Drafts are local, immutable records. Only the UI exposes sending, following exact-message review. A draft is marked in flight before contacting Gmail. Failed or interrupted sends remain uncertain rather than being retried and potentially duplicated; inspect Gmail Sent.

This is a workflow safeguard, not an isolation boundary from an agent or attacker who already has arbitrary execution under the same Unix account. Such a process can read those user's files or change the program. For higher-assurance separation, use a separate credential-owning OS service account and a reviewed narrow IPC broker. Do not claim the skill alone makes a broadly privileged agent immune to email prompt injection.

## 6. Recovery and uninstall

- **OAuth blocked:** verify the selected project, Desktop client type, test user, API enabled status, selected account and administrator policy. Reconnect; do not repeatedly regenerate clients.
- **Repeated reconnect after a week:** inspect OAuth Testing/Production status.
- **Network/429:** the monitor backs off. The wizard shows the failure without printing response bodies or tokens.
- **Wrong account/client:** disconnect first, then import the intended client and reconnect. Account changes clear old cached events and drafts.
- **Unknown send outcome or `sending` after interruption:** check Gmail Sent before preparing any replacement. There is no automatic retry.
- **No background service:** run from an ordinary Ubuntu user login session with `systemctl --user` available. Minimal containers and some remote sessions do not have a user manager.
- **Wizard already running:** reuse its link or choose a different wizard port; do not modify gateway port 18789 or watcher port 8788.
- **Old native integration still active:** this app does not disable it. Leave it in place during a controlled read-only test, then retire it deliberately to avoid duplicated workflows.

For removal, click Stop checks or Disconnect in the wizard. Disconnect removes local tokens, events, cursors and drafts, but retains your imported client JSON. Also revoke the app in Google Account → Connections if desired. To remove the remaining app-owned files after stopping:

```bash
systemctl --user disable --now openclaw-gmail-connect.service
rm -f "$HOME/.config/systemd/user/openclaw-gmail-connect.service"
systemctl --user daemon-reload
```

Delete the private state directory only after confirming it is this app's directory and any drafts are no longer needed. Remove the skill through OpenClaw's supported skill management workflow. Do not delete the whole `.openclaw` directory or disable lingering if other user services need it.

## 7. Publishing

Export a clean ClawHub distribution from the source folder. This preserves canonical runtime metadata and includes listing documents while excluding bytecode caches and unrelated root files:

```bash
python3 /ABSOLUTE/INSTALLED/SKILL/PATH/scripts/package_clawhub.py /ABSOLUTE/PUBLISH/PATH/gmail-connect
```

Choose a new destination outside the source directory. Run the test and publishing commands below from its parent. The package contains `SKILL.md`, the listing Markdown documents, `scripts/`, `assets/`, `references/`, and offline tests. Inspect it for private state before publishing. Read [PUBLISHING.md](../PUBLISHING.md) for the exact GitHub folder, catalog fields, and Actions update workflow. Validate on Ubuntu before publishing:

```bash
python3 -m unittest discover -s ./gmail-connect/tests -v
```

After completing the live acceptance gates, sign in to ClawHub and preview the exact folder before publishing:

```bash
clawhub login
clawhub skill publish ./gmail-connect --slug gmail-connect --name "Gmail Connect" --version 0.1.3 --tags latest,preview --categories integrations,productivity,communication --topics gmail,email,oauth,ubuntu,local-first --dry-run
clawhub skill publish ./gmail-connect --slug gmail-connect --name "Gmail Connect" --version 0.1.3 --tags latest,preview --categories integrations,productivity,communication --topics gmail,email,oauth,ubuntu,local-first --changelog "Add ClawHub listing documents and GitHub release publishing"
```

Check the installed ClawHub CLI help if its command surface differs. Use a slug you own; the example name's availability is not verified. Publishing on ClawHub releases the skill under MIT-0. Keep the preview designation until the Ubuntu/Gmail gates pass. ClawHub's audit is separate from local tests; a local test cannot promise three green indicators. After submission, inspect the security audit, findings, and risk level. If blocked, download the exact report with `clawhub scan download gmail-connect --version 0.1.3 --output report.zip`. Fix genuine findings and publish a new version; never hide needed Gmail scopes to improve a score. Never bundle client JSON, user state, logs, session links, or the supplied user's personal transcript. Exclude bytecode caches and development state. No public listing was created during this build.

For upgrades, stop this app's monitor before replacing source files, keep its private state, then relaunch the wizard and enable checks again. Do not move a live service's script path; reinstall its unit through the wizard after moving the skill. The gateway does not need to restart for this service update.

## 8. Acceptance gates

Offline tests are necessary but not proof of a live integration. Before marking a release production-ready, record these results on real Ubuntu:

1. Healthy gateway baseline with its existing chat channels; capture the config hash without exposing its content.
2. Install skill through OpenClaw, run the wizard as the ordinary user, authorize a dedicated test Gmail account.
3. Verify profile access, one known inbox result, full text read, and one multi-page search.
4. Ask the actual OpenClaw agent to perform the same read through this skill under its actual sandbox/tool policy.
5. Enable monitor; send a test message manually from another account, verify one arrival ID, and observe the feed after two poll cycles.
6. Restart the adapter and log out/reboot with the chosen user-manager policy; verify recovery without duplicate send behavior.
7. Revoke Google access, verify a clear reconnect error, reconnect, and retest.
8. With optional sending enabled, prepare one harmless email, approve it manually, verify exactly one copy in Gmail Sent. This is an explicitly authorized test, not automatic setup behavior.
9. Verify gateway health and original chat channels again, and confirm the OpenClaw config hash is unchanged.
10. If proactive delivery was configured, verify the specific intended destination separately. Test an email containing inert instructions; it must be summarized as data, not executed.

## 9. Sources (checked 2026-09-26)

- OpenClaw latest release: https://github.com/openclaw/openclaw/releases/latest
- Skills installation: https://docs.openclaw.ai/cli/skills
- ClawHub format: https://docs.openclaw.ai/clawhub/skill-format
- ClawHub publication: https://docs.openclaw.ai/clawhub/publishing
- Google Desktop OAuth/PKCE: https://developers.google.com/identity/protocols/oauth2/native-app
- Google OAuth expiration: https://developers.google.com/identity/protocols/oauth2
- Google credential setup: https://developers.google.com/workspace/guides/create-credentials
- Gmail synchronization: https://developers.google.com/workspace/gmail/api/guides/sync
- Gmail push and device polling recommendation: https://developers.google.com/workspace/gmail/api/guides/push
