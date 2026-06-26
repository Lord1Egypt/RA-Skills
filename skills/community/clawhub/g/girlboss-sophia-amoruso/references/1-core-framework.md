# Core Framework — How Kickbacks.ai Works

> Source: kickbacks.ai product documentation and VS Code Marketplace listing

## The Spinner Economy

Kickbacks turns the "thinking" spinner in Claude Code and Codex into a live advertising slot. Here's the full flow:

### 1. Installation & Setup

```bash
# In VS Code Quick Open (Ctrl+P):
ext install Kickbacksai.kickbacks-ai
```

**Steps:**
1. Install from VS Code Marketplace (search "Kickbacks").
2. Click "Kickbacks: Sign in" in the status bar.
3. Authenticate with Google.
4. Start using Claude Code or Codex. Earnings begin automatically.

**Before you sign in** you'll see real sponsored lines — a live preview. Preview impressions don't earn. Sign in to start earning your share.

### 2. What Gets Replaced

Claude Code has a random verb spinner: "Discombobulating...", "Baking...", "Grokking...", "Quantizing...", etc.

Kickbacks replaces that verb with a short sponsored line — e.g. "Ramp · save time and money" — while preserving all other UI elements. The ad is clickable.

### 3. CLI Support

| Environment | Ad Placement | Since |
|---|---|---|
| VS Code (Claude Code ext) | Spinner verb text | Launch |
| VS Code (Codex ext) | Spinner verb text | Launch |
| Terminal CLI (Claude Code) | Status bar line | Launch |
| Terminal CLI (Claude Code 2.1.143+) | Spinner verb text + status bar | v2.1.143 |

> **Case: Terminal vs Extension** (Product): Terminal Claude Code shows the ad as a clickable line in the status bar for all versions. Version 2.1.143 and newer also show the ad as the verb text inside the spinner itself. The terminal verb refreshes when you start a new `claude` session.

### 4. The Revenue Loop

```
Developer installs → Uses AI tool → Tool thinks (spinner) → Ad shown → 
Ad generates $ → 50% to developer, 50% to Kickbacks
```

> **Case: Real-time Balance** (Product): Your balance is always visible in the VS Code status bar: `Kickbacks ($0.42 today · $7.11)`. It updates in real-time as impressions and clicks accrue.

### 5. Status Bar States

| Status | Meaning |
|---|---|
| `Kickbacks: Sign in` | Not signed in yet. Click to authenticate. |
| `Kickbacks ($X today · $Y)` | Signed in and earning. |
| `Kickbacks: Off` | You disabled Kickbacks. Click to re-enable. |
| `Kickbacks incompatible` | Your Claude Code version isn't supported yet. |
| `Kickbacks offline` | Backend is temporarily unreachable. |
