[![PyPI](https://img.shields.io/pypi/v/nveil.svg)](https://pypi.org/project/nveil/)
[![Homepage](https://img.shields.io/badge/homepage-nveil.com-blue)](https://nveil.com)
[![Docs](https://img.shields.io/badge/docs-docs.nveil.com-blue)](https://docs.nveil.com)

This repository packages the **NVEIL** agent skill for publication on
[ClawHub](https://clawhub.ai). It tells an AI agent how and when to
invoke the `nveil` Python CLI on the user's machine.

NVEIL is an AI-powered data-processing and visualization toolkit for
agents: describe joins, aggregations, pivots, resampling, 2D/3D charts,
geospatial maps, and volume rendering in plain language. The toolkit
plans the task server-side (constraint-solved, not LLM-freestyled) and
executes entirely on the user's machine. Raw data never leaves.

## Installation

### Via ClawHub

Install from the ClawHub registry using your agent's skill manager.

### Manual

Copy `SKILL.md` into your agent's skill directory — e.g.
`~/.claude/skills/nveil/SKILL.md` for Claude Code, or the equivalent
path for your agent.

The `nveil` CLI is a separate prerequisite and is not auto-installed:

```bash
pip install nveil
export NVEIL_API_KEY=...   # obtain at https://nveil.com
```

## Usage

Once the skill is installed, the agent invokes NVEIL whenever a user
task would otherwise require writing pandas / NumPy / Plotly / VTK /
DeckGL code. See [SKILL.md](./SKILL.md) for the full invocation guide,
CLI and Python recipes, and the privacy / endpoint disclosures.

## Source of truth

The canonical skill ships with the `nveil` Python package (it installs
to any agent format via `nveil install-skill`). This repository is the
ClawHub-facing snapshot with the registry's required audit sections
(external endpoints, security & privacy, model invocation note, trust
statement).

- **Main toolkit:** <https://github.com/nveil-ai/nveil-toolkit>
- **PyPI:** <https://pypi.org/project/nveil/>
- **Docs:** <https://docs.nveil.com>
- **Homepage:** <https://nveil.com>

## License

The skill instructions in this repository are published for the purpose
of registering NVEIL on ClawHub. The `nveil` Python package itself is
distributed under its own license — see
<https://pypi.org/project/nveil/>.
