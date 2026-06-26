---
name: knowledge-gaps
description: Track questions Hans failed to answer and flag missing knowledge
---

# Knowledge Gap Detection Skill

When Hans cannot answer a question or says "I don't know" / "nicht in meiner Wissensdatenbank", he should:

## Steps

1. **MUST ACTUALLY RUN THIS COMMAND** — Log the failed question using the gap logger:
```bash
exec python3 ./scripts/log-knowledge-gap.py "The question the user asked" "What knowledge was missing"
```

2. **Check the output** — The script will print `✅ Logged to knowledge-gaps.md` with the entry. If it prints an error, report it.

3. **ONLY AFTER seeing the ✅ confirmation**, respond: "Das weiß ich leider nicht. Ich habe die Frage in meinem Knowledge-Gap-Log gespeichert, damit ATTi sie nachträglich ergänzen kann."

> ⚠️ **CRITICAL:** Do NOT say "Ich habe die Frage gespeichert" unless you actually ran the exec command AND saw the ✅ output. Never hallucinate this action.

## Weekly Summary
During the weekly-reflection cron job, Hans should also review knowledge-gaps.md and summarize the top gaps for ATTi.

## Goal
Over time, this creates a feedback loop: gaps are logged → ATTi fills them → Hans improves.
