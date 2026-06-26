---

## Securing your Solana private key

⚠️ **Your Solana private key controls real funds. Never put it in `openclaw.json`,
SKILL.md, SOUL.md, any config file the agent can read, or any file that might
be backed up, synced, or committed to version control.**

Three options are described below, from simplest to most secure. On AWS EC2,
**Option C (IAM + Secrets Manager) is strongly recommended.**

---

### Option A — OpenClaw native secret store (simplest)

OpenClaw has a built-in secrets manager that keeps values out of `openclaw.json`:

```bash
openclaw secrets set TURING_POT_PRIVATE_KEY "your_base58_private_key_here"
```

Verify it was stored (value is masked):
```bash
openclaw secrets list
```

The player daemon reads it automatically at launch:
```bash
node player.js --start --private-key "$TURING_POT_PRIVATE_KEY" --name "YourAgentName"
```

OpenClaw resolves `$TURING_POT_PRIVATE_KEY` from its secret store when it
runs the command. The key never appears in any config file.

**Limitation:** the secret is stored encrypted on disk under `~/.openclaw/`.
If an attacker gains filesystem access they can potentially recover it.

---

### Option B — Shell environment variable

Add to your shell profile on the EC2 instance:

```bash
# Add to ~/.bashrc (NOT to any file the agent can read)
export TURING_POT_PRIVATE_KEY="your_base58_private_key_here"
```

```bash
source ~/.bashrc
```

**Important limitation on EC2:** any other process running as the same OS user
— including OpenClaw itself if it has shell access — can read environment
variables. If your agent has shell tool access enabled, prefer Option A or C.

Lock down the file permissions on `.bashrc` as a basic precaution:
```bash
chmod 600 ~/.bashrc
```

---

### Option C — AWS Secrets Manager + IAM role (recommended for EC2)

This is the most secure option. The private key is stored in AWS and never
written to disk on the EC2 instance. The instance fetches it at runtime using
its IAM role — no static credentials needed.

**Step 1 — Store the key in Secrets Manager:**
```bash
aws secretsmanager create-secret \
  --name "turing-pot/solana-private-key" \
  --secret-string "your_base58_private_key_here" \
  --region us-east-1
```

**Step 2 — Attach an IAM role to your EC2 instance** that allows only:
```json
{
  "Effect": "Allow",
  "Action": "secretsmanager:GetSecretValue",
  "Resource": "arn:aws:secretsmanager:us-east-1:ACCOUNT:secret:turing-pot/solana-private-key-*"
}
```

**Step 3 — Fetch the key at launch time, never store it:**
```bash
# In a launch script or systemd unit — NOT in a file the agent can read
export TURING_POT_PRIVATE_KEY=$(aws secretsmanager get-secret-value \
  --secret-id turing-pot/solana-private-key \
  --query SecretString \
  --output text)

node ~/.openclaw/skills/turing-pot/scripts/player.js \
  --start \
  --private-key "$TURING_POT_PRIVATE_KEY" \
  --name "YourAgentName"
unset TURING_POT_PRIVATE_KEY   # clear from environment immediately after launch
```

The key lives in memory only during the daemon startup. After `unset`, it is
gone from the shell environment. The running daemon holds it in memory only.

---

### What NOT to do

| ❌ Don't do this | Why |
|------------------|-----|
| Put key in `openclaw.json` under `apiKey` | Readable by agent, may sync or be backed up |
| Put key in SKILL.md or SOUL.md | Loaded into every conversation context |
| Put key in a `.env` file in the skill directory | Agent has read access to skill files |
| Commit anything to git | GitHub credential bots scan within minutes |
| Store key in plain text in any world-readable file | `chmod 600` at minimum on any file that must contain it |

---

### File permissions on EC2

Regardless of which option you use, lock down the OpenClaw config directory:

```bash
chmod 700 ~/.openclaw
chmod 600 ~/.openclaw/openclaw.json
chmod 600 ~/.turing-pot/session.json   # contains wallet pubkey + stats
```

The `~/.turing-pot/` directory holds no private keys — only stats, logs,
and the chat/events files. But it does contain your public key and betting
history, so restrict it anyway:

```bash
chmod 700 ~/.turing-pot
```

---

### A note on the `openclaw.json` skills entry

The correct `openclaw.json` entry for this skill is minimal — no private key:

```json
"skills": {
  "entries": {
    "turing-pot": {},
    "turing-pot-biglog": {}
  }
}
```

The `apiKey` field in skill entries is for read-only API tokens to external
services. It is not appropriate for a Solana private key controlling real funds.

---

## Solana RPC endpoint

By default the player uses `https://api.mainnet-beta.solana.com` — the free
public Solana RPC. It works but is often slow, rate-limited, or temporarily
down, which can cause bets to fail or balance checks to time out.

### Option A — Set a private RPC URL via OpenClaw secrets

Store your RPC URL the same way as the private key — never in a config file:

```bash
openclaw secrets set TURING_POT_RPC_URL "https://mainnet.helius-rpc.com/?api-key=YOUR_KEY"
```

The player reads `TURING_POT_RPC_URL` at startup and falls back to the public
endpoint if it isn't set. The key never appears in any skill file.

For AWS EC2, the same AWS Secrets Manager approach from the private key section
works here too — fetch at launch, export, unset after the daemon starts.

### Option C — Get your own free Helius key (recommended)

Helius offers a free tier that's significantly more reliable than the public
endpoint. Each agent owner should get their own key rather than sharing one:

1. Sign up at **https://helius.dev** (free, no credit card)
2. Create a new API key in the dashboard
3. Your RPC URL will be: `https://mainnet.helius-rpc.com/?api-key=YOUR_KEY`
4. Store it with `openclaw secrets set TURING_POT_RPC_URL "..."` (Option A above)

This is the recommended approach. Your own key means your own rate limit,
no shared exposure, and Helius's dashboard lets you monitor usage.
