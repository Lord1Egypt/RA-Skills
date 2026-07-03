---
name: kannaka-quantum
description: Run Kannaka's memory operations on real quantum hardware, and drive qBraid Lab compute + autonomous remote coding agents. Use for quantum circuits, true quantum random numbers, and resonance recall as amplitude amplification — on qBraid's free simulator (default, $0) or real QPUs (IonQ/Rigetti/IQM/AQT via qBraid or OpenQuantum) — plus qBraid Lab operations: list/manage environments, provision GPU/CPU compute, and launch/drive coding agents on remote instances over SSH. Invoke when asked to run a quantum circuit, draw quantum entropy, list QPUs, execute Kannaka recall on a quantum backend, spin up Lab compute, or run a remote agent on provisioned hardware.
---

# Kannaka Quantum

Kannaka's memory is a *Holographic Resonance Medium* — recall is wave interference, and *"attention acts as gravity: wavefronts whose phase/amplitude align with the query are pulled forward."* That is, almost verbatim, **quantum amplitude amplification**. This skill makes the correspondence literal: it runs Kannaka's recall, plus general circuits and a true-entropy source, on actual quantum backends.

## Two surfaces — same core

You can drive the bridge either way; prefer whichever is wired in this session.

1. **MCP tools** (if the `kannaka-quantum` MCP server is connected): `quantum_devices`, `run_circuit`, `quantum_random`, `resonance_recall`. Call them directly.
2. **JSON CLI** — shell out to the `kannaka-quantum` command. Every subcommand prints **one JSON object** to stdout (errors included), so parse it directly.

If neither is available, install the package: `pip install kannaka-quantum` (or `pip install -e .` from the repo). Python ≥ 3.10. If a spawned process can't find Python, set `KANNAKA_QUANTUM_PYTHON` to the interpreter path.

## ⚠️ Spend safety — read first

- The **default device is the free qBraid simulator** `qbraid:qbraid:sim:qir-sv` (30 qubits, no credits). Casual/agent use never spends money.
- A **real QPU runs only when you opt in explicitly**: pass a hardware `device=` AND `allow_spend=true` (CLI: `--allow-spend`). A `max_credits` ceiling guards every paid run (default ≈ $2).
- **Never** run on a per-minute-billed device. The native `rigetti:rigetti:qpu:cepheus-1-108q` on qBraid bills **$120/min** — the bridge refuses per-minute devices outright. For a cheap real gate QPU use `aws:rigetti:qpu:cepheus-1-108q` (~$0.41 for 256 shots) or an OpenQuantum backend like `openquantum:iqm:garnet`.
- On paid QPUs keep `shots` low — `resonance_recall` defaults to 1024 shots.

## Tools

| tool / subcommand | what it does |
|---|---|
| `quantum_devices` / `devices [--online]` | List QPUs + simulators across providers (status, qubits, cost). Discover before running. |
| `run_circuit` / `run` | Execute an **OpenQASM 3** program (`include "stdgates.inc"`; declare `qubit[]`/`bit[]`, apply gates, measure). Returns measurement counts. CLI reads QASM from `--qasm`, `--qasm-file`, or stdin. |
| `quantum_random` / `qrng` | True quantum random bits from measurement collapse (not a PRNG) — entropy for the medium's irrationality (Ξ) and dream noise. Returns bitstring, integer, and a float in [0,1). |
| `resonance_recall` / `recall` | **The showcase.** Amplitude-encode candidate memory resonances into a quantum state and amplitude-amplify toward the strongest — Kannaka's recall, run as interference on a quantum computer. Returns the measured distribution plus quantum vs classical top pick. |

## CLI examples

```bash
kannaka-quantum devices --online
kannaka-quantum run --qasm-file bell.qasm --shots 200
kannaka-quantum qrng --bits 16
kannaka-quantum recall --amplitudes 0.1,0.9,0.2,0.15 --labels alpha,beta,gamma,delta
```

Resonance recall output:

```json
{"distribution": {"alpha": 2, "beta": 775, "gamma": 240, "delta": 7},
 "quantum_top": "beta", "classical_top": "beta", "agree": true,
 "qubits": 2, "candidates": 4, "amplified": true,
 "device": "qbraid:qbraid:sim:qir-sv"}
```

Amplitude amplification sharpens the prepared resonance state toward the strongest memory; on the free simulator the quantum pick agrees with the classical argmax.

## Real-hardware run (deliberate, spends credits)

```bash
kannaka-quantum recall --amplitudes 0.1,0.9,0.2,0.15 --labels a,b,c,d \
  --device aws:rigetti:qpu:cepheus-1-108q --shots 256 --allow-spend --max-credits 50
```

Authentication: qBraid resolves a key from `QBRAID_API_KEY`, `~/.qbraid/qbraidrc`, or `~/Downloads/QBraid.txt`. OpenQuantum (real QPUs, no free simulator) uses OAuth client-credentials at `~/.openquantum/sdk-key.json` or `OPENQUANTUM_CLIENT_ID`/`OPENQUANTUM_SECRET`.

## qBraid Lab & compute (v0.2+)

Beyond circuits, the bridge exposes **qBraid Lab operations** as `lab-*` CLI subcommands — inspect environments, provision GPU/CPU compute, and launch autonomous coding agents on remote instances over SSH. (These are the surface the Kannaka Rust agent's `lab_*` tools shell out to.)

**Free — inspect (no spend):**

| subcommand | what it does |
|---|---|
| `lab-credits` | qBraid credit balance |
| `lab-list-profiles [--available-only]` | compute profiles + per-minute credit cost |
| `lab-compute-status` / `lab-compute-usage` | Lab server status / usage + credit rates |
| `lab-list-instances` / `lab-list-kernels` | on-demand instances / local Jupyter kernels |
| `lab-list-envs` / `lab-env-info <slug>` | qBraid environments / one env's metadata |

**Free — environment management (in-Lab only):** `lab-create-env`, `lab-delete-env`, `lab-pip-install`, `lab-pip-freeze`, `lab-add-kernel`, `lab-remove-kernel`.

**PAID — compute (bills per wall-clock minute):**

| subcommand | what it does |
|---|---|
| `lab-compute-up <profile>` / `lab-compute-down` | start / stop the Lab server on a profile |
| `lab-provision-instance` / `lab-start-instance` / `lab-stop-instance` | provision / resume / pause an on-demand instance (stop preserves disk) |

**Autonomous remote agents (over SSH):** `lab-ssh-configure <instance>` → alias; `lab-agent-setup` (inject API key + onboarding + model so a remote `claude`/`codex` runs autonomously); `lab-agent-launch` / `lab-agent-list` / `lab-agent-read` / `lab-agent-send`. On Windows, `ssh-bridge` is the websocket↔stdio ProxyCommand shim.

### ⚠️ Lab spend safety — SEPARATE gate from circuits

Paid compute bills **per wall-clock minute until you stop it** — a different risk shape from a one-off circuit run, so it has its own opt-in:

- Requires `--allow-spend` **and** a `--max-credits` ceiling, or `KANNAKA_LAB_ALLOW_SPEND=1` — **distinct from** `KANNAKA_QUANTUM_ALLOW_SPEND` (a circuit-shot opt-in must never silently authorize open-ended compute).
- `max_credits` is the balance you accept to *risk* (runway = `min(max_credits, balance) / rate`), **not** an automatic cutoff — stop compute explicitly with `lab-compute-down` / `lab-stop-instance`.
- Refuses to start if the balance can't cover even one minute of burn.

## Notes

- Bitstrings from qBraid are big-endian; the bridge reverses them for qiskit's little-endian indexing internally — you get labeled results, not raw bits.
- All errors surface as a JSON object (`{"error": ..., "type": ...}`) so you can branch on failures without scraping text.
- The lab tools are CLI-only (the MCP server exposes the four quantum tools); drive them via `kannaka-quantum lab-*` or the Kannaka agent's `lab_*` tools.
