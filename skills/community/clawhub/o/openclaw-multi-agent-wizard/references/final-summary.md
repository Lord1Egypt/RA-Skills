# Final Summary

End every successful run with a short beginner-friendly handoff.

## Required sections

Always include these items:

1. chosen mode
2. created agents
3. Feishu bot or group mapping
4. whether the gateway was restarted
5. the exact next test
6. the exact fallback step if no reply appears

## Suggested template

Use wording close to this:

```text
Setup complete.

Current mode:
- [mode name]

Agents created:
- [agent 1]
- [agent 2]

Current mapping:
- [bot or Feishu group] -> [agent]
- [bot or Feishu group] -> [agent]

Gateway:
- [restarted automatically / restart not needed]

Next test:
- Go to [target Feishu group or bot] and send: [simple test sentence]

If there is no reply:
- Tell me and I will check the local gateway status and logs for you.
```

## Tone

- concise
- reassuring
- no jargon unless needed

## Helper script

If you want a fast structured draft, use:

```bash
python scripts/render_setup_summary.py --mode "多 bot 多 agent" --agents 产品助理,研发助理 --mapping "产品机器人->产品助理" "研发机器人->研发助理" --gateway restarted
```
