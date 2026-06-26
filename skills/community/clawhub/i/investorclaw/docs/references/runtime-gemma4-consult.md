<!--
v4.x adaptation note: this reference contract is carried forward from
v2.6 essentially unchanged — the engine's input/output schema, holdings
field mapping, and consultative-LLM setup are identical in v4.x. The
only surface change is invocation: replace v2.x `/portfolio X` slash
commands with the equivalent v4.x MCP tool (`portfolio_X`) or a
natural-language query through `portfolio_ask`. Paths like
`~/portfolio_reports/` correspond to the bind-mounted `./reports/`
under your compose project; `portfolios/` corresponds to the
bind-mounted `./portfolios/`.
-->

# gemma4-consult Setup

`gemma4-consult` is the default consultation model referenced by
[contract-output.md](contract-output.md). It must be created on your Ollama
endpoint before enabling consultation. It is built from `gemma4:e4b` using
the Modelfile at `docs/gemma4-consult.Modelfile`.

## Automated setup (recommended)

```bash
# Check what models are available
investorclaw ollama-setup --check --endpoint http://your-ollama-host:11434

# Pull gemma4:e4b base and create gemma4-consult
investorclaw ollama-setup --endpoint http://your-ollama-host:11434

# Set up all InvestorClaw GPU models (e2b, e4b, gemma4-consult)
investorclaw ollama-setup --model all --endpoint http://your-ollama-host:11434
```

## Manual setup

```bash
ollama pull gemma4:e4b
ollama create gemma4-consult -f docs/gemma4-consult.Modelfile
ollama list | grep gemma4-consult
```

## Hardware

- 12+ GB VRAM
- CUDA compute capability ≥ 8.0 (RTX 30xx / A-series / Ada Lovelace or newer)
- Ollama ≥ 0.20.x
