# Search Policy

Search before fixing bugs so agents do not repeat old investigation.

## Query Shape

Use a compact query with:

- product area
- visible symptom
- error keywords
- relevant file or component names
- failed command or endpoint

Good:

```bash
python3 "$DEVHUB_HOME/bin/devhub.py" search \
  --project music-agent \
  --query "voice audio ack continuation no speech frontend scheduler"
```

Weak:

```bash
python3 "$DEVHUB_HOME/bin/devhub.py" search --project music-agent --query "bug"
```

## How To Read Results

Read in this order:

1. `Pitfalls`: traps and forbidden approaches.
2. `Playbooks`: diagnosis order and evidence requirements.
3. `Bugfixes`: old root causes and verification.
4. `Decisions`: constraints that explain why the system is shaped this way.
5. `Areas`: code paths and risk level.

## When Search Is Optional

Skip search for tiny mechanical edits that cannot plausibly repeat a past bug, such as typo fixes or formatting-only changes. Still write an AI Run or Release when the work reaches a commit or main push gate.
