# Upwork Demo Preset

This preset is designed for proposal/demo scenarios where you want:
- a lead-focused Gmail query,
- fixed agency profile context,
- consistent reply tone.

## Run one-shot demo

```bash
cd skills/gmail-auto-draft/scripts
./run_upwork_demo.sh --auth-mode local --max-emails 5
```

## Run continuous demo monitor

```bash
cd skills/gmail-auto-draft/scripts
POLL_INTERVAL=60 MAX_EMAILS=5 ./run_upwork_demo.sh --mark-read
```

## Edit demo behavior

- Agency profile: `references/upwork-demo/agency_profile.txt`
- Tone rules: `references/upwork-demo/style_rules.txt`
- Lead query: `references/upwork-demo/gmail_query.txt`
