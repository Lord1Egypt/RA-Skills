# Skill Distiller

**Compress skills by 50-90%** while preserving functionality. Reduces context window usage by removing low-importance sections (examples, explanations) while keeping triggers and core instructions. Stop hitting context limits.

**This skill practices what it preaches** — the main `SKILL.md` ships in formula notation (~400 tokens, ~90% functionality). Full human-readable version available in `SKILL.reference.md`.

## Skill Variants

| Variant | Path | Tokens | Functionality | Use When |
|---------|------|--------|---------------|----------|
| **Default** | `SKILL.md` | ~400 | ~90% | Formula notation — ships by default |
| **Compressed** | `compressed/SKILL.md` | ~975 | ~90% | Prose variant, more readable |
| **One-liner** | `oneliner/SKILL.md` | ~100 | ~70% | Quick reference only |
| **Reference** | `SKILL.reference.md` | ~2,500 | ~90% | Full docs, human reading |

*Token counts are estimates using 4 chars/token heuristic — actual counts vary by model tokenizer. Functionality scores are LLM-estimated, not empirically validated.*

## Prerequisites

- **Agent host**: Claude Code, Cursor, or any Agent Skills-compatible tool
- **For local inference**: `ollama serve` running with llama3.2 or similar
- **For cloud inference**: `GEMINI_API_KEY` or `OPENAI_API_KEY` environment variable set

## Quick Start (30 seconds)

1. **Install**: `openclaw install neon-skill-distiller`
2. **Run**: `/skill-distiller path/to/skill.md`
3. **See output**: Compressed skill + what was removed

**Example**:
```
$ /skill-distiller my-skill/SKILL.md --threshold=0.9

Functionality preserved: ~90% (LLM-estimated)
Tokens: 2500 -> 1000 (60% reduction)
Removed: 5 examples, 3 edge cases, 2 verbose sections
Kept: all triggers, core instructions, constraints

[Compressed skill output follows...]
```

## Installation

**ClawHub (recommended)**:
```bash
openclaw install neon-skill-distiller
```

**Manual (Claude Code users)**:
```bash
# Clone to your Claude Code skills directory
git clone https://github.com/live-neon/skills.git ~/.claude/skills/liveneon
```

## Invocation Methods

| Method | Command | Context |
|--------|---------|---------|
| **Slash command** | `/skill-distiller path/to/skill.md` | Claude Code, Cursor, any Agent Skills-compatible tool |
| **Piped** | `cat skill.md \| /skill-distiller` | Stdin input |

## Usage

```bash
# Threshold mode (preserve 90% functionality, default)
/skill-distiller path/to/skill.md --threshold=0.9

# Aggressive compression (80% - use when context is tight)
/skill-distiller path/to/skill.md --threshold=0.8

# Token target mode
/skill-distiller path/to/skill.md --tokens=500

# One-liner mode
/skill-distiller path/to/skill.md --mode=oneliner

# Dry run (analyze without outputting compressed skill)
/skill-distiller path/to/skill.md --dry-run

# Verbose output (show section-by-section analysis)
/skill-distiller path/to/skill.md --verbose
```

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--mode` | `threshold` | Compression mode: threshold, tokens, oneliner |
| `--threshold` | `0.9` | Functionality target (0.0-1.0) |
| `--tokens` | - | Target token count |
| `--provider` | `auto` | LLM provider: ollama, gemini, openai |
| `--verbose` | `false` | Show section-by-section analysis |
| `--dry-run` | `false` | Analyze without outputting compressed skill |

**Note**: `--threshold` sets the preservation target (default 0.9). `--mode=threshold` is implicit when using `--threshold`. Use `--mode=tokens` or `--mode=oneliner` for other modes.

## Compression Modes

### Threshold Mode (Default)

Preserve X% of functionality, compress as much as possible.

```bash
/skill-distiller skill.md --threshold=0.9
```

**Why 0.9 default**: Skill functionality is normally distributed. Wide tails mean some "low importance" sections occasionally carry critical value. At 0.9, you preserve more of the tail while still achieving 10-20% token reduction.

### Token Target Mode

Compress to exact token budget.

```bash
/skill-distiller skill.md --tokens=500
```

**Token estimation**: Uses 4 chars/token heuristic. Accuracy: +/-20% vs actual provider tokenization.

### One-Liner Mode

Extreme compression for quick reference.

```bash
/skill-distiller skill.md --mode=oneliner
```

Output format:
```
TRIGGER: [activation conditions]
ACTION: [core behavior]
RESULT: [expected output]
```

### Formula Mode (default)

The main skill uses formula notation — legend + math that the LLM executes directly.

**Benefits**:
- ~400 tokens (vs ~975 for compressed prose)
- Mathematically precise — no ambiguity
- Executable — formula IS the algorithm

See `SKILL.md` for the formula, `SKILL.reference.md` for full prose documentation.

## Protected Patterns

These patterns are **never removed** even if they look verbose:

| Pattern | Why Protected |
|---------|---------------|
| YAML `name`/`description` | REQUIRED by Agent Skills spec |
| Task creation | Compaction resilience |
| N-count tracking | Observation workflow |
| Checkpoint/state | State recovery |
| BEFORE/AFTER markers | Self-calibration |

If a protected pattern is removed, the functionality score is penalized (-10% per pattern).

## Calibration

The skill learns from usage:

- **First run (N=0)**: Uses LLM-only scoring, wide confidence interval
- **After 5+ compressions**: Historical data narrows confidence interval

To improve calibration, report actual outcomes:
```bash
/skill-distiller feedback --id=c1 --actual=85 --outcome="worked"
```

## Related

- [Agent Skills Spec](https://agentskills.io/specification) - Required fields, size constraints
- [skill-distiller-llm.md](../../go-pbd/docs/plans/2026-04-14-skill-distiller-llm.md) - Implementation plan (Complete)
- [skill-compression-support.md](../../go-pbd/docs/plans/2026-04-14-skill-compression-support.md) - CLI-based compression (Option B, Draft)

## Directory Structure

```
skill-distiller/
├── SKILL.md              # Default (formula, ~400 tokens, 89%)
├── SKILL.reference.md    # Full reference (~2,500 tokens, 91%)
├── compressed/SKILL.md   # Prose variant (~975 tokens, 88%)
├── oneliner/SKILL.md     # Minimal variant (~100 tokens, 72%)
├── test_integration.sh   # Ollama-based tests (3/9 SKIP - require skill deployment)
└── testdata/             # Test fixtures
```

**ClawHub**: `openclaw install neon-skill-distiller`

**Calibration data**: `.learnings/skill-distiller/calibration.jsonl`

## Model Compatibility

The formula notation has been validated with:

| Model | Status | Notes |
|-------|--------|-------|
| Claude (Opus 4.5, Sonnet 4) | Tested | Formula notation understood and executed correctly |
| GPT-4 / GPT-5 | Community feedback welcome | Should work (MetaGlyph paper validates math notation) |
| Llama 3.2 | Community feedback welcome | Used for integration tests, formula not specifically validated |
| Gemini 2.5 Pro | Community feedback welcome | Should work (supports math notation) |

**Help us improve**: If you test with a model not listed, please report results via GitHub issues.

## Manual Testing

Since integration tests require deployed skill invocation (3/9 SKIP), use this manual procedure:

```bash
# 1. Test basic compression
/skill-distiller testdata/minimal.md --threshold=0.9

# 2. Verify protected patterns are kept
/skill-distiller testdata/minimal.md --verbose | grep -i "protected"

# 3. Test one-liner mode
/skill-distiller testdata/minimal.md --mode=oneliner

# 4. Verify JSONL is written
cat .learnings/skill-distiller/calibration.jsonl | tail -1 | jq .
```

**Expected results**:
- Compression achieves 10-50% token reduction
- Protected patterns (yaml.name, N-count) are preserved
- One-liner produces TRIGGER/ACTION/RESULT format
- Calibration entry is appended with `actual: null`

## License

MIT License
