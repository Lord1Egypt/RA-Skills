# Security policy — OpenClaw Token Optimizer 4.1.1

## Trust boundary

This is a local read-only analysis package. It contains Python standard-library scripts
and a shell launcher. Hermes YAML parsing additionally uses optional PyYAML. There are no install hooks, telemetry,
credential collectors, dynamic code evaluation, or automatic config changes.

## File behavior

- `optimizer_core.py`: pure analysis functions; no files, network or processes.
- `optimizer.py`: reads explicitly supplied JSON/context files and prints selected analysis.
  For the OpenClaw runtime, `--live` invokes only fixed `openclaw --version`, `openclaw models list`, `models status`, and `cron list` read
  commands with `subprocess.run`, argv lists, no shell, and a timeout. The installed OpenClaw
  executable and configured Gateway/providers are trusted dependencies. They may perform
  network requests; therefore we do NOT claim that live mode is offline or network-free.
- `optimize.sh`: resolves its own directory and delegates arguments to optimizer.py.
- Four old script names: migration shims to explicit v4 subcommands; no old writes remain.
- `assets/`: public example policy, empty patch set, review templates; never auto-installed.
- `references/PROVIDERS.md`: policy guidance, not executable setup or credential handling.
- Markdown/license/manifest files: documentation and file integrity metadata only.

## Data handling

Raw config/auth records, job commands/prompts and context contents are not printed.
Only selected findings, model/agent identifiers and file basenames appear. Those selected
identifiers can themselves be private: inspect reports before sharing. Errors deliberately
withhold raw native stderr and invalid input values. No report upload occurs.

Explicit config input can contain secrets; the file is read locally, never modified.
Use sanitized exports where practical. Do not publish real config, session dumps or reports.
Native status is held in process memory only. Live reads may update OpenClaw's own caches
or logs; this package does not promise the native executable has zero side effects.

## Review and integrity

The subprocess adapter may warrant scanner scrutiny: inspect its fixed argv call sites.
A checksum manifest is not proof of safety and cannot guarantee a third-party review pass.
Do not dismiss a scanner finding as a false positive without examining its evidence.

Run `python3 -m unittest discover -s tests -v` from GitHub source and
`sha256sum -c SHA256SUMS.txt` against the distributed package. Tests cover malformed inputs,
missing usage, auth/capability gates, no-shell execution, and read-only behavior.
No paid canary is run by the package. Catalog flags alone are not inference proof.

Maintainer: [Asif2BD](https://github.com/Asif2BD) · [MissionDeck.ai](https://missiondeck.ai)

## Hermes file adapter

Only explicitly selected profile config/jobs files are read. JSON uses the standard library;
YAML uses optional PyYAML safe_load (never unsafe constructors). The adapter does not read
.env or credentials, import Hermes, execute jobs, start schedulers or make network requests.
Selected model identifiers may appear in reports; raw prompts/scripts/config do not.
