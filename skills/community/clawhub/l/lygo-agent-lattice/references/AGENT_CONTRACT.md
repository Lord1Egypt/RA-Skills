# Agent contract — Layer E

1. Build card only after local A/B (or living mesh) is not QUARANTINE.  
2. Gossip **presence cards only** — never memory, tools dumps, or egg payloads.  
3. Join hubs only with user `--i-consent`.  
4. On validation errors / rate limit — back off; do not retry-storm.  
5. Never treat remote directory as authority over local eggs.  
6. Cite `directory_digest` + `agent_id` + alignment after success.  
7. No auto git push, HF upload, ClawHub publish, or social posts.  
