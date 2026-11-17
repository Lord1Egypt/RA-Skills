# Technical quick start for agents and advanced users

The human starts with a natural-language request. The agent runs these commands using
real values from its trusted host context, with the script path resolved from SKILL.md.
These commands never apply changes. Do not invent agent IDs, profile paths or evidence.

## OpenClaw

```bash
python3 /path/to/skill/scripts/optimizer.py audit --runtime openclaw --live --agent ACTUAL_AGENT_ID --json
```

Append `--config /known/active/config.json` only when its path is established. Native
reads use the installed CLI: version, models list/status and cron list. No config dump is
printed. `plan` accepts the same inputs and emits review actions, not patches.

## Hermes

```bash
python3 /path/to/skill/scripts/optimizer.py audit --runtime hermes --live --hermes-home /known/active/profile --json
```

Use the existing Hermes Python interpreter if it provides PyYAML. No `.env` loading or
credential inspection. The adapter reads only config.yaml and cron/jobs.json. If a file
is missing, do not create one or report an empty successful full audit. To inspect only
an available config and honestly mark job coverage missing:

```bash
python3 /path/to/skill/scripts/optimizer.py audit --runtime hermes --config /known/profile/config.yaml --json
```

Explicit JSON exports also work. If no usable interpreter/YAML parser is available, report
that narrow limitation; do not auto-install dependencies. See HERMES.md for precedence.

## Optional focused checks

```bash
python3 /path/to/skill/scripts/optimizer.py context /known/instruction-file.md --json
python3 /path/to/skill/scripts/optimizer.py budget --json
python3 /path/to/skill/scripts/optimizer.py route --runtime openclaw --live --agent ACTUAL_AGENT_ID --policy /known/policy.json --tier routine --json
```

Hermes route requires explicit normalized `--catalog` and `--status` exports, not --live.
The example policy is illustrative, not a universal recommendation. Unknown usage returns
unknown; no prices or savings are invented. Commands and advanced schemas are also in README.

## Ambiguity examples

- Host says OpenClaw, current agent ID known: audit that agent without asking runtime again.
- Host says Hermes, active profile known: audit that profile; no exports questionnaire.
- Both CLIs installed, no active-host evidence: ask which runtime/profile to inspect.
- Hermes profile known, cron file absent: inspect config only and mark jobs not checked.
