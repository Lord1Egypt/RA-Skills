# Deployment: OpenClaw Skill

The Modern Portfolio Theory optimizer can run as an OpenClaw skill, allowing users to invoke it conversationally via `/modern-portfolio-theory`.

## Prerequisites

- OpenClaw installed and running on the host machine
- Python 3.10+ available on the same machine (the skill executes Python locally)
- The project must be cloned and its dependencies installed on the same machine running OpenClaw

## 1. Install the Project on the Host

```bash
git clone https://github.com/user/modern-portfolio-theory.git
cd modern-portfolio-theory
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Verify the CLI works:

```bash
python3 -m mpt_portfolio list
```

## 2. Register the Skill

The project ships with a `SKILL.md` at the repository root. OpenClaw discovers skills by scanning for `SKILL.md` files in configured skill directories or workspaces.

Option A -- symlink into the OpenClaw skills directory:

```bash
ln -s /path/to/modern-portfolio-theory /path/to/openclaw/skills/modern-portfolio-theory
```

Option B -- add the project directory as a workspace in your OpenClaw configuration so it is scanned automatically.

Option C -- copy `SKILL.md` into an existing skills directory alongside the full project:

```bash
cp -r /path/to/modern-portfolio-theory /path/to/openclaw/skills/modern-portfolio-theory
```

The key requirement is that OpenClaw can find the `SKILL.md` file and that the full project (including `mpt_portfolio/`, `portfolios/`, and `scripts/`) is in the same directory tree.

## 3. Verify the Skill Loads

Restart or reload OpenClaw, then confirm the skill is recognized:

```
/skills
```

You should see `modern-portfolio-theory` in the skill list with its description and the chart emoji.

## 4. Invoke the Skill

Start a conversation and type:

```
/modern-portfolio-theory
```

The skill will walk you through portfolio setup, optimization, backtesting, and rebalancing interactively. All CLI commands are executed behind the scenes.

## 5. Portfolio State

Portfolio data is stored in the `portfolios/` directory within the project. Each portfolio gets its own subdirectory with configuration, cached data, and reports. These persist between sessions.

## Important Notes

- **Python must be on the host**: OpenClaw invokes `python3` directly. The skill will not work if Python is unavailable or if the dependencies are not installed.
- **File paths are local**: The skill reads and writes to the local filesystem. If OpenClaw runs in a container, the project directory must be mounted into that container with read-write access.
- **No network services**: The skill only needs outbound HTTPS to Yahoo Finance for market data. It does not open any ports or run a server.
- **Cron is separate**: Scheduled rebalancing via `scripts/cron_rebalance.sh` must be set up independently on the host using cron or systemd timers. The OpenClaw skill handles interactive use, not scheduling.
