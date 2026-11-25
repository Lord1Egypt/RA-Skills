# ModelDeck — Local LLM Deployment Workshop

Run open-weight models on your own hardware or intranet and wire them into real work: size the model from a VRAM budget, verify what you downloaded, stand up an inference service, expose an OpenAI-compatible endpoint, and accept the result on throughput, time-to-first-token, and sampled quality. Covers Windows, Linux, and Apple Silicon across Ollama and llama.cpp.

## What This Is

- **The problem it solves**: the weights are on disk, but three questions stall everything — will it run, is it running correctly, and is it safe to put in front of users. This skill turns those into a sequence of steps with explicit pass criteria and failure branches, so deployment stops being trial and error.
- **What you get**: a Deployment and Acceptance Record (Markdown) plus a VRAM budget table, a runnable launch script, raw benchmark data (JSONL), and a rollback procedure.
- **How it differs from asking a general model**: a general answer gives folklore ("just use Q4_K_M"). This skill forces the arithmetic down to your layer count, context length, KV cache precision, and acceptance threshold. Every number is reproducible; every parameter is copy-pasteable. It does not cover training, fine-tuning, or multi-node distributed inference.

## When To Use It

- "I have 16 GB of VRAM and need a model for internal knowledge-base Q&A. Is 14B enough or do I need 32B?"
- "The GGUF downloaded fine, but llama-server OOMs on load and I cannot tell whether it is layers, context, or KV precision."
- "I need the local model behind an OpenAI-compatible endpoint so the application code stays untouched."
- "This network cannot reach the internet. Download, verification, and upgrades all have to work offline."
- "The same model is noticeably faster under Ollama than under llama.cpp. I want to know why and which to pick."
- "I want to run this on an Apple Silicon laptop and do not know how to budget unified memory."

## When NOT to Use

- Training or fine-tuning: inference deployment and sizing only.
- Multi-GPU clusters, tensor parallelism, Kubernetes orchestration: out of scope.
- Guaranteed tok/s figures: estimates and acceptance criteria only.
- Unknown model licence: check LICENSE before recommending any deployment.

## Quick Reference

| Situation | Use |
|---|---|
| How big a model fits on this GPU | `references/hardware-sizing.md` + `scripts/vram_budget.py` |
| Which model of the same size | `references/model-selection.md` |
| Copy-paste launch flags | `references/serving-recipes.md` |
| Real measured speed | `references/benchmarking.md` |

## Inputs and Outputs

| Field | Required | Description |
|---|---|---|
| Host environment | Yes | OS and version, accelerator type, VRAM, system RAM, free space on the target disk |
| Concurrency and latency targets | Yes | Simultaneous requests; acceptable time-to-first-token and minimum output rate |
| Task type | Yes | Q&A, extraction, rewriting, code, summarization; drives quantization tier and context budget |
| Context requirement | Yes | Maximum input tokens per request, including system prompt and history |
| Deployment flavor | Yes | Ollama (low effort) or llama.cpp (full control); default based on VRAM headroom |
| Network conditions | No | Direct registry access, mirror only, or offline media |
| Acceptance thresholds | No | Defaults to "first token under 3 s, 12+ tokens/s single-stream, 4 concurrent without failure" |

**Outputs**:

- `deployment-report.md`: hardware inventory, VRAM budget, selection decision, launch parameters, endpoint self-test, benchmark table, rollback plan.
- `start-<model>.cmd` (Windows) or `start-<model>.sh` (Linux, macOS): one runnable script with every environment variable and flag frozen in place.
- `bench-<model>.jsonl`: one record per request with prompt_tokens, completion_tokens, time-to-first-token, and total wall time.

## Workflow

### Step 1: Inventory Hardware and Requirements

**Do**: collect host facts and restate business needs as measurable thresholds.

```bash
# Windows (PowerShell)
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
Get-CimInstance Win32_ComputerSystem | Select-Object TotalPhysicalMemory
# Linux
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
free -h && nproc && df -h "$MODELDECK_HOME"
# macOS (Apple Silicon)
sysctl -n hw.memsize; sysctl -n hw.ncpu
```

**Pass criteria**: VRAM, RAM, and disk all have concrete numbers, and the latency goal is phrased measurably ("first token under 4 s at 4 concurrent").

**If it fails**: no discrete GPU or under 6 GB VRAM means going CPU or Metal with a 3B-4B model at a mid-to-high quantization tier. Under 16 GB RAM plus a mixture-of-experts model means switching to a dense small model rather than forcing it.

### Step 2: Budget VRAM and Select the Model

**Do**: convert each candidate into a VRAM number with two formulas instead of guessing.

```text
weights GiB ≈ params (billions) × bits per weight × 0.116
KV GiB      ≈ 2 × layers × (kv_heads × head_dim) × bytes per element × context ÷ 1073741824
total       = weights + KV cache + compute buffer (0.3-0.8 GiB) + OS and driver reserve (0.8-1.5 GiB)
```

```bash
python scripts/vram_budget.py --params 8 --layers 32 --kv-heads 8 --head-dim 128 --ctx 8192 --vram 16
```

**Pass criteria**: the budget table holds at least two candidates, and at least one satisfies "total ≤ usable VRAM minus 1 GB".

**If it fails**: walk down in this order and recompute after each step: context length, KV precision (f16 to q8_0 to q4_0), quantization tier, then parameter count. Partial layer offload is the last resort, not the first.

### Step 3: Acquire and Verify

**Do**: prefer pre-quantized GGUF, always download with resume support, and run three checks after landing (byte size, SHA256, GGUF header).

```bash
curl -L -C - --retry 5 --retry-delay 3 -o "$MODELDECK_HOME/models/model-Q4_K_M.gguf" "<MODEL_FILE_URL>"
python scripts/verify_download.py --file "$MODELDECK_HOME/models/model-Q4_K_M.gguf" --sha256 <SHA256> --size <BYTES>
```

For the Ollama path, stage the file outside the model store, write a Modelfile (`FROM <staged gguf>` plus `PARAMETER num_ctx` and `PARAMETER temperature`), and import with `ollama create local-model:q4 -f Modelfile`. Never write directly into the internal blobs directory of `OLLAMA_MODELS`.

**Pass criteria**: all three checks pass, and `ollama list` or `/api/tags` reports the model with its size.

**If it fails**: a hash mismatch means delete and re-download, not "close enough". A bad GGUF header means a truncated file or the wrong format. A quantization validation error on import usually means corrupted source tensors — re-download from the official repo; upgrading the runtime does not fix corrupted weights.

### Step 4: Deploy the Inference Service

**Do**: translate the Step 2 numbers into launch parameters and freeze them into a script.

```bash
# Ollama: environment decides KV precision and concurrency; the Modelfile decides context and offload
export OLLAMA_MODELS="$MODELDECK_HOME/models" OLLAMA_HOST="0.0.0.0:11434"
export OLLAMA_KEEP_ALIVE=30m OLLAMA_NUM_PARALLEL=2 OLLAMA_FLASH_ATTENTION=1 OLLAMA_KV_CACHE_TYPE=q8_0
ollama serve
```

```bash
# llama.cpp: layers, context, KV precision, and parallel slots in one command
"$MODELDECK_HOME/bin/llama-server" -m "$MODELDECK_HOME/models/model-Q4_K_M.gguf" \
  --host 0.0.0.0 --port 8080 -c 8192 -ngl 99 -fa on \
  --cache-type-k q8_0 --cache-type-v q8_0 -np 2 --cont-batching --jinja --metrics
```

**Pass criteria**: `/v1/models` (llama.cpp) or `/api/tags` (Ollama) lists the target model; `nvidia-smi --query-compute-apps=pid,used_memory --format=csv` shows the server process with VRAM within 15 percent of the budget; one real generation succeeds.

**If it fails**: OOM during load means adjust context first, then KV precision, then layer count — one change at a time. A healthy endpoint with no process in `nvidia-smi` means the binary does not match the CUDA major version your driver supports and has silently fallen back to CPU; swap in a matching build.

### Step 5: Wire Up the OpenAI-Compatible Endpoint

**Do**: present the local service as a standard OpenAI endpoint so application code needs no edits. The official SDK only needs `base_url` with a trailing `/v1` and any non-empty `api_key`; run the call once with `stream=True` as well.

```bash
curl -s http://127.0.0.1:8080/v1/chat/completions -H "Content-Type: application/json" \
  -d '{"model":"local-model","messages":[{"role":"user","content":"Reply OK"}],"max_tokens":16}'
```

**Pass criteria**: one non-streaming and one streaming call both succeed; the response carries token counts under `usage`; non-ASCII text neither garbles nor truncates.

**If it fails**: 404 means `base_url` is missing `/v1`; `model not found` means the name or tag differs from what the server exposes; a stream that never terminates means an intermediate buffer or a missing chunked encoding; a client complaining about a missing API key just needs any non-empty placeholder — local servers do not validate it but client libraries require it.

### Step 6: Benchmark and Sample Quality

**Do**: fix the prompt set, the output cap, and the temperature; warm up once, then take the median of three runs.

- **Performance**: time-to-first-token, decode rate, end-to-end latency, degradation at 4 concurrent, peak VRAM. For llama.cpp, derive these from the cumulative counters at `/metrics` rather than client-side stopwatch math.
- **Quality**: 20-30 items scored 0/1/2, including at least three must-not-fail items (structured output parses, numeric extraction is correct, out-of-scope requests are refused).

**Pass criteria**: all five performance fields and the quality score are on the table; aggregate throughput at 4 concurrent is at least 1.8x single-stream with no OOM and no timeouts; every number is labelled "example environment, measure your own".

**If it fails**: if quality is short, raise the quantization tier first, then consider a larger model, and only then touch the prompt — reversing the order hides the real bottleneck. If concurrency degrades badly, cut parallel slots or context instead of adding hardware.

### Step 7: Harden for Production

**Do**: turn a one-off success into something operable.

- **Concurrency**: the value of `OLLAMA_NUM_PARALLEL` or `-np` is coupled to the VRAM budget — every extra slot is another KV cache. Recompute Step 2 when you change it.
- **KV cache**: when context hits the ceiling, drop KV precision first and context second; `--no-kv-offload` trades VRAM for system RAM by keeping KV on the host.
- **Logging and rollback**: rotate server logs by size and record token counts and latency only, never full prompts; keep the previous working tag and a copy of the launch script so rollback is one command.

**Pass criteria**: a crashed service comes back with one command; the previous version still starts; logs have a rotation policy; the rollback procedure is written down and has been rehearsed once.

**If it fails**: repeated crashes with no log evidence usually mean a leftover process still holding VRAM (two server processes in `nvidia-smi`), or exhausted system commit charge.

## Output Format

```
Hardware inventory: GPU / VRAM / RAM / disk / OS
VRAM budget: weights | KV cache | runtime overhead | headroom
Recommended stack: model + quantisation + context + concurrency
Launch command: ready-to-copy ollama / llama.cpp flags
Acceptance: first-token latency, tok/s, peak VRAM
```

## Quality Gates

- [ ] The VRAM budget is reproducible: given parameter count, quantization tier, layer count, KV head dimension, and context, anyone arrives at the same weight and KV numbers.
- [ ] The launch script works as a single command with no interactive input and no paths hiding outside it.
- [ ] All three verification results are recorded: byte size, SHA256, GGUF header, matching the source's published values.
- [ ] Both endpoint self-tests pass: one non-streaming and one streaming call, each returning a `usage` block.
- [ ] The benchmark table carries all five fields: time-to-first-token, decode rate, end-to-end latency, concurrency degradation, peak VRAM.
- [ ] Every speed and latency figure is labelled "example environment, measure your own" and is not presented as a general result.
- [ ] At least one real failure path is documented: the error, the diagnosis, and the resolution.
- [ ] Rollback completes within 5 minutes and the command is in the report; no secrets, internal addresses, real names, or personal paths appear anywhere.

## Scope and Limits

- No training, fine-tuning, or distillation, and no evaluation of models with unreleased weights.
- No speed promises: every tok/s and latency number is either measured on the stated host or labelled an estimate, and does not transfer across machines.
- No multi-node distributed inference or GPU cluster orchestration; multi-GPU coverage stops at basic tensor-split parameters.
- No legal judgment on model licenses; commercial use is decided by the LICENSE file in the model repository and the actual grant.
- Not a substitute for domain quality review: this skill supplies the sampling method and thresholds, but business correctness still needs a domain owner.

## Common Traps

- **Parameter count without quantisation**: 7B-Q4 and 7B-FP16 differ by more than 2x VRAM.
- **Forgetting KV cache**: at long context it can exceed the weights.
- **Vendor tok/s as measured**: always benchmark on the target machine.
- **Single-request sizing**: leave headroom for two concurrent requests.

## Delivery Example

**Input**:

```text
Host: Linux, 24 GB VRAM discrete GPU, 64 GB RAM, 200 GB free on the data disk
Task: internal knowledge-base Q&A, up to ~6000 input tokens, 4 concurrent users
Constraint: no application code changes, OpenAI-compatible endpoint
```

**Output skeleton** (`deployment-report.md`):

```markdown
# Local Inference Deployment and Acceptance Record
## 1 Hardware and requirements
Linux / 24 GB VRAM / 64 GB RAM / 200 GB free; target: 4 concurrent, first token under 3 s.
## 2 VRAM budget
| Candidate | Quant | Weights | KV@8K | Buffer+reserve | Total | Verdict |
|---|---|---|---|---|---|---|
| 14B class | Q4_K_M | 7.9 GiB | 1.5 GiB | 1.6 GiB | 11.0 GiB | Comfortable, 16K viable |
| 32B class | Q4_K_M | 18.1 GiB | 2.0 GiB | 1.6 GiB | 21.7 GiB | Borderline, 8K only |
## 3 Selection and parameters
14B class Q4_K_M at 16K; -ngl 99 -c 16384 -fa on --cache-type-k q8_0 -np 2 (see start-llm.sh).
## 4 Endpoint self-test
Non-streaming OK / streaming OK / usage block OK / no garbled text
## 5 Benchmark (example environment, measure your own)
First token 0.6 s (1.9 s at 4 concurrent); decode 31 tok/s (78 tok/s aggregate); peak VRAM 12.1 / 18.4 GB.
## 6 Quality sample and rollback
22 items, 39/44; must-not-fail 3/3. Rollback: switch back to the previous tag and restart, about 40 s.
```

## Related Skills

- **ChartAtelier (paid)**: chart VRAM budgets and benchmark results.
- **SkillForge (paid)**: package your deployment know-how as a reusable skill.

## Reference Files

- `references/hardware-sizing.md`: inventory commands for all three platforms, the VRAM and context budget math, and the unified-memory and commit-charge traps.
- `references/model-selection.md`: parameter count vs quantization vs context, dense against mixture-of-experts, and license plus chat-template checks.
- `references/serving-recipes.md`: parameter templates for Ollama and llama.cpp, systemd and Windows service wrappers, and a troubleshooting matrix.
- `references/benchmarking.md`: benchmark methodology, metric definitions, concurrency test procedure, and the quality scoring sheet.
- `scripts/vram_budget.py`: stdlib-only VRAM budget calculator that sweeps quantization tiers and context sizes; `scripts/verify_download.py` checks byte size, SHA256, and the GGUF header.
