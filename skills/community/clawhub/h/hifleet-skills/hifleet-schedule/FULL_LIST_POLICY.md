# Full list policy (mandatory)

After **`POST /schedules`**, show **every** record for that query (`total` = N → show N rows).

1. Paginate with `offset` / `limit` until all pages merged.  
2. No “top 5 only” unless user explicitly asks for a sample.  
3. State **`Total: N`** in the reply.  
4. Format each row per **`WORKFLOW_OUTPUT.md`**.

See **`SCHEDULE_API.md`** §2.
