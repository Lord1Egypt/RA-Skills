# Agent contract — Public Lattice Gate

When this skill is active, agents MUST:

1. Run `verify` before claiming the public lattice is LIVE.  
2. Treat public endpoints as **mirrors**; local stack (if any) is authority.  
3. Use `propose` only as a draft; do not claim the agent is on the Star Chart until steward ingest.  
4. Never auto-publish, tweet, or push.  
5. Never request secrets for this skill.  
6. On restore, share **public digests/links only**.  

Optional status line after align:

```text
Aligned to LYGO Public Lattice Gate. Public presence readiness checked. Awaiting human consent for any live chart write via lygo-haven-star-chart.
```
