# Installing Litmus

## Via ClawHub (recommended)

Ask your OpenClaw agent:
> "Install the litmus skill"

Or from the CLI:
```bash
npx clawhub install litmus
```

## Manual install

```bash
git clone https://github.com/kuberwastaken/litmus ~/.openclaw/skills/litmus
```

## Requirements

- **GPU**: NVIDIA GPU with CUDA (required for training runs)
- **`uv`**: Python package manager — `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **`git`**: For experiment version control and git worktrees
- **`python3`**: For JSON attempt records, leaderboard scripts, and analytics
- **`nvidia-smi`**: Recommended for GPU detection (usually bundled with CUDA drivers)
- OS: Linux or macOS (Windows not supported)

## First-time data setup

After installing the skill, run setup once to download training data (~1 GB):

```bash
bash {baseDir}/scripts/setup.sh
```

This clones Karpathy's [autoresearch](https://github.com/karpathy/autoresearch) training harness,
installs Python deps via `uv`, prepares the dataset, and creates the shared lab git repository at
`~/.litmus/repo/`. Each agent will get its own branch in this shared repo via git worktrees.

Takes ~5 minutes on a good connection.

### What setup creates

```
~/.litmus/
  repo/          ← shared lab git repo (all agents' experiment branches live here)
  harness/       ← training code (cloned from autoresearch)
  shared/
    attempts/    ← one JSON file per experiment (source of truth for leaderboard)
    notes/
      discoveries/
      anomalies/
      moonshots/
      synthesis/
    skills/      ← validated reusable techniques (Skills Library)
  agents/        ← per-agent git worktrees (created by prepare-agents.sh)
```

## Uninstall

```bash
npx clawhub uninstall litmus
rm -rf ~/.litmus   # removes all runtime state, agent workspaces, and results
```
