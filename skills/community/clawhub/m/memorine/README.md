# Memorine

[![PyPI](https://img.shields.io/pypi/v/memorine)](https://pypi.org/project/memorine/)
[![Python](https://img.shields.io/pypi/pyversions/memorine)](https://pypi.org/project/memorine/)
[![License](https://img.shields.io/pypi/l/memorine)](https://github.com/osvfelices/memorine/blob/main/LICENSE)

Memory for AI agents that actually works like memory.

Not a vector database. Not an embedding store. Not another RAG pipeline.
Memorine gives your agents memory that behaves the way yours does. Things you
use often stay sharp. Things you ignore fade away. And when something turns out
to be wrong, you fix it.

## The problem

Every "memory" solution out there is really just a search engine with extra
steps. Store some text, turn it into vectors, retrieve the closest match.
That works for document search. It does not work for memory.

Actual memory:
- **Fades over time** unless you keep using it
- **Gets stronger with repetition**
- **Catches contradictions** before they cause trouble
- **Links things together** so one thought leads to another
- **Tracks what happened and why**, not just isolated facts
- **Learns from past mistakes** so you stop repeating them

Memorine does all of this. No API keys, no GPU, no Docker, no vector database,
no external services. Pure Python, SQLite under the hood, and some well-tested
math for the decay curves.

## Install

```bash
pip install memorine
```

Done. Zero dependencies. Nothing else to configure.

Want semantic search (find "server in Europe" when you stored "hosted in Frankfurt")?

```bash
pip install memorine[embeddings]
```

Want the terminal dashboard?

```bash
pip install memorine[ui]
```

Everything? `pip install memorine[all]`. The base install stays at zero dependencies
and works on its own. The extras are optional layers on top.

## Quick start

```python
from memorine import Mind

brain = Mind("alice")

# Store facts
brain.learn("The deploy script is at /opt/deploy/run.sh")
brain.learn("Production DB runs on port 5432")

# Search memory
results = brain.recall("deploy")
# [{'fact': 'The deploy script is at /opt/deploy/run.sh', ...}]
```

Each time you recall a fact, it gets a little stronger. Facts you never touch
gradually fade, just like they would in your own head.

## What it can do

### Facts that catch problems

```python
brain.learn("Redis is on port 6379")

# Later, something conflicting comes in
fid, contradictions = brain.learn("Redis is on port 6380")
# contradictions = [{'fact': 'Redis is on port 6379', 'similarity': 0.87}]

# Fix mistakes when you find them
brain.correct(fid, "Redis was moved to port 6380")

# Connect related facts
brain.connect(fact_a, fact_b, relation="same_service")
```

The contradiction detection uses token-level similarity. No LLM calls, no
embeddings. It just compares what you already know against what you are trying
to store, and flags overlaps that do not match.

### Events and causality

```python
e1 = brain.log("DNS timeout on api.example.com")
e2 = brain.log("Health check failed", caused_by=e1)
e3 = brain.log("Autoscaled to 3 replicas", caused_by=e2)

# Why did we autoscale?
chain = brain.why(e3)
# DNS timeout -> health check failed -> autoscaled

# What else happened because of the DNS timeout?
consequences = brain.consequences(e1)

# Filter by tags and text
brain.events(query="timeout", tags=["dns"])
```

### Procedures that get better over time

```python
with brain.procedure("deploy_production") as run:
    run.step("run tests", success=True)
    run.step("build image", success=True)
    run.step("push to registry", success=False, error="auth expired")

# Next time, before starting:
advice = brain.anticipate("deploy to production")
# {
#   'warnings': ["'push to registry' fails 40% of the time..."],
#   'errors_to_avoid': [{'step': 'push to registry', 'error': 'auth expired'}]
# }
```

After enough runs, Memorine automatically flags steps that fail too often and
tells you what went wrong before. Your agents stop making the same mistakes.

### Multi-agent sharing

```python
alice = Mind("alice")
bob = Mind("bob")

# Alice shares a finding
alice.share("Staging server moved to eu-west-1")

# Bob sees it
shared = bob.shared_with_me()
# [{'fact': 'Staging server moved to eu-west-1', 'from_agent': 'alice'}]

# Everyone sees team-wide knowledge
team = bob.team_knowledge()
```

### Cognitive profile

```python
print(brain.profile())
```

Generates a plain-text summary of everything the agent knows: top facts, recent
events, team knowledge, procedure track records. Drop it into a system prompt
and your agent has full context with zero retrieval calls.

## How the decay works

Based on the Ebbinghaus forgetting curve. Each fact has a weight that changes
over time:

- **One access**: fades within a few days
- **Ten accesses**: holds for weeks
- **Twenty or more**: stays for months

The formula: `retention = e^(-days / stability)` where stability grows each
time you access the fact. Simple, predictable, and it matches how human memory
actually works according to about 140 years of research.

Run `brain.cleanup()` to prune dead memories, or just let them decay on their
own. Either way, your agents focus on what matters.

## MCP server

Memorine includes an MCP server for tool-based integration. After install, the
`memorine` command speaks JSON-RPC 2.0 over stdio.

Any MCP-compatible client can connect. Add to your client config:

```json
{
    "mcpServers": {
        "memorine": {
            "command": "python3",
            "args": ["-m", "memorine.mcp_server"]
        }
    }
}
```

For OpenClaw, see the [integration guide](docs/openclaw.md).

### Available tools

| Tool | Purpose |
|------|---------|
| `memorine_learn` | Store a fact, detect contradictions |
| `memorine_recall` | Search by text, ranked by weight and recency |
| `memorine_correct` | Fix a wrong fact |
| `memorine_log_event` | Record something that happened |
| `memorine_events` | Search past events |
| `memorine_share` | Share with another agent or the team |
| `memorine_team_knowledge` | Get shared team knowledge |
| `memorine_profile` | Full cognitive summary |
| `memorine_anticipate` | Pre-task advice based on past runs |
| `memorine_procedure_start` | Begin tracking a procedure |
| `memorine_procedure_step` | Log a step outcome |
| `memorine_procedure_complete` | Finish a procedure run |
| `memorine_stats` | Database statistics and embedding status |
| `memorine_learn_batch` | Bulk-learn multiple facts at once |

## Semantic search (optional)

With `pip install memorine[embeddings]`, recall goes from keyword matching to
meaning matching. Under the hood it uses FastEmbed (ONNX, no PyTorch) and
sqlite-vec for vector storage inside the same SQLite file.

```python
brain.learn("The production server is hosted in Frankfurt, Germany")

# Without embeddings: no results (no keyword overlap)
# With embeddings: finds it
brain.recall("where is our infrastructure in Europe")
```

If embeddings are not installed, everything works exactly the same as before
with FTS5 keyword search. When they are installed, recall blends semantic
results with keyword results automatically.

Backfill embeddings for an existing database:

```python
brain.reindex_embeddings()
```

Or from the CLI: `memorine reindex --agent alice`

## Terminal dashboard (optional)

With `pip install memorine[ui]`, you get a live terminal dashboard:

```bash
memorine ui --agent alice
```

Shows facts with decay weights, event timeline, procedure success rates, and a
search bar. Keyboard driven. Read-only (it does not modify the database).

## CLI

```
memorine              Start the MCP server (default)
memorine ui           Launch the terminal dashboard
memorine stats        Print database statistics
memorine reindex      Rebuild embeddings for all facts
memorine --help       Show available commands
```

## Under the hood

- **SQLite + FTS5** for storage and full-text search. Zero dependencies needed.
- **FastEmbed + sqlite-vec** for optional semantic search. ONNX runtime, no
  PyTorch, no GPU. A 45MB model that runs on a Raspberry Pi.
- **Jaccard similarity** on word tokens for contradiction detection. No model,
  no API, deterministic results.
- **Ebbinghaus decay** with access-count stability. Math, not magic.
- **Single file storage**. Your entire memory is one `.db` file. Vectors,
  facts, events, procedures, everything in one place. Copy it, back it up,
  move it between machines.

## Storage

Default location: `~/.memorine/memorine.db`. All agents share the same file but
each has its own namespace, so they do not step on each other.

Override it:

```python
brain = Mind("alice", db_path="/path/to/custom.db")
```

## Requirements

- Python 3.9 or later
- Base install: zero dependencies (just Python stdlib + SQLite)
- `memorine[embeddings]`: fastembed + sqlite-vec (~200MB including the model)
- `memorine[ui]`: textual (~1MB)

## License

MIT
