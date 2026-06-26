# End-to-end test: persona-service → Clawbot → Telegram → result

Use your own persona-service base URL and `client_id` (from `skills.entries["persona-consent-telegram-hub"].env`) in the commands below.

## 1. Create a request (use `client_id` for your Clawbot)

From any machine (e.g. your Mac):

```bash
curl -s $PERSONA_SERVICE_URL/persona/requests \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "<your-client-id>",
    "requester_id": "test-client",
    "reason": "testing persona flow",
    "user_context": {"foo": "bar"}
  }'
```

Use the same `client_id` you set in `skills.entries["persona-consent-telegram-hub"].env` (e.g. `PERSONA_CLIENT_ID`). Replace `$PERSONA_SERVICE_URL` with your persona-service base URL (e.g. `https://persona-service.example.com`).

Expected: `{"request_id":"<uuid>","status":"pending"}`

Save the `request_id` for step 3.

**Important:** `client_id` must match the value in your Clawbot’s `openclaw.json` for this skill (`PERSONA_CLIENT_ID`). The persona-client on the Clawbot polls for work for that `client_id` only.

---

## 2. What happens on the Clawbot

- The **persona-client** (`persona_client.sh`) polls `GET $PERSONA_SERVICE_URL/persona/client/next?client_id=<your-client-id>` every few seconds.
- When persona-service returns `status: "pending"` with that request, the script runs `request_persona.sh` with `requester_id` and `reason`.
- You get a **Telegram** message (from the approval bot) with **Approve** / **Deny**.
- Tap **Approve** (or **Deny**).
- The script POSTs the result to persona-service at `/persona/client/responses`.

---

## 3. Check request status

Using the `request_id` from step 1:

```bash
curl -s $PERSONA_SERVICE_URL/persona/requests/<request_id>
```

- While waiting for you to approve/deny: `"status":"pending"`.
- After you approve: `"status":"completed","allowed":true,"persona_md":"..."`.
- After you deny (or timeout): `"status":"completed","allowed":false,"message":"author did not authorize"`.

---

## 4. If your first curl used `clawbot_url` instead of `client_id`

That request likely failed validation (422) or was created with a wrong/missing `client_id`, so the Clawbot’s persona-client will never pick it up. Create a new request with the curl in step 1 (with your `client_id`) and run the flow again.

---

## Troubleshooting: approved in Telegram but status stays "pending"

If you approved (or denied) in Telegram but `GET /persona/requests/<request_id>` still shows `"status":"pending"`, the persona-client is probably **failing to POST** the result to persona-service.

### A. Persona-service requires a shared secret

If persona-service is run with `PERSONA_CLIENT_SHARED_SECRET` set, it rejects POSTs without the header. The Clawbot must send the same secret.

- On the **persona-service** host, check: `echo $PERSONA_CLIENT_SHARED_SECRET`
- In **Clawbot** `~/.openclaw/openclaw.json`, under `skills.entries["persona-consent-telegram-hub"].env`, add (or set):
  ```json
  "PERSONA_CLIENT_SHARED_SECRET": "same-value-as-on-persona-service"
  ```
- Restart the wrapper (so the persona-client restarts with the new env). Then run the flow again with a **new** request.

### B. Confirm the request was for this Clawbot

The persona-client only receives work for the `client_id` configured in your skill env. If the request was created with a different or missing `client_id`, a different Clawbot would have to submit the result. Create a new request with the curl in step 1 (using your `client_id`) and test again.

### C. See persona-client logs (why POST might be failing)

Run the persona-client in the foreground so you see its stderr:

1. Stop the wrapper (Ctrl+C in the terminal where it’s running), or stop only the persona-client if you run it separately.
2. From the Clawbot server, in a terminal (set env to match your `openclaw.json` skill entry):
   ```bash
   cd ~/.openclaw/workspace/skills/persona-consent-telegram-hub
   export PERSONA_SERVICE_URL="<your-persona-service-base-url>"
   export PERSONA_CLIENT_ID="<your-client-id>"
   # If persona-service uses a secret:
   export PERSONA_CLIENT_SHARED_SECRET="<your-secret>"
   bash scripts/persona_client.sh
   ```
3. From another machine, create a new request (step 1). In this terminal you should see either:
   - `[persona-client] handling request_id=...` then `[persona-client] submitted result for request_id=...` (success), or
   - `[persona-client] failed to submit result for request_id=..., retrying in Xs` (POST is failing; check secret, URL, and network).
4. Restart the wrapper when done so the gateway and persona-client run again as before.

---

## No Telegram approval when creating a request

If you create a request with the curl but never get the Approve/Deny in Telegram, run these on the **Clawbot server** (as the user that runs the wrapper).

### 1. Is the persona-client running?

```bash
ps aux | grep persona_client
```

You should see a line with `persona_client.sh`. If not, you started only `openclaw gateway` instead of the wrapper. Restart with:

```bash
cd ~/.openclaw/workspace/skills/persona-consent-telegram-hub
node scripts/run-gateway-with-persona-client.js -- --port 18789
```

### 2. Can the Clawbot reach persona-service?

From the Clawbot server:

```bash
curl -s "$PERSONA_SERVICE_URL/persona/client/next?client_id=$PERSONA_CLIENT_ID"
```

(Set `PERSONA_SERVICE_URL` and `PERSONA_CLIENT_ID` to match your skill env, or substitute the URL and client_id in the path.)

- If you get `{"status":"idle"}` or `{"status":"pending",...}` → network is fine.
- If you get "Connection refused" or timeout → the Clawbot cannot reach your persona-service (firewall, wrong URL, or persona-service not listening). Fix network or run persona-service so it’s reachable from the Clawbot.

### 3. After creating a request, does the next poll return it?

From your Mac (or wherever you run curl): create a request and note the `request_id`. Then on the Clawbot server, within a few seconds run:

```bash
curl -s "$PERSONA_SERVICE_URL/persona/client/next?client_id=$PERSONA_CLIENT_ID"
```

You should see `{"status":"pending","request_id":"...","requester_id":"...","reason":"..."}`. If you see `{"status":"idle"}` instead, the request was created with a different `client_id` or persona-service lost it.

### 4. Run persona-client in the foreground (to see logs)

Stop the wrapper (Ctrl+C). In a terminal on the Clawbot server, export the skill env (copy the values from `~/.openclaw/openclaw.json` for `persona-consent-telegram-hub`) and run:

```bash
cd ~/.openclaw/workspace/skills/persona-consent-telegram-hub
export PERSONA_SERVICE_URL="<your-persona-service-base-url>"
export PERSONA_CLIENT_ID="<your-client-id>"
export TELEGRAM_BOT_TOKEN="<from openclaw.json>"
export TELEGRAM_OWNER_CHAT_ID="<from openclaw.json>"
export PERSONA_PATH="$HOME/.openclaw/persona.md"
export ALLOWED_PERSONA_PATH="$HOME/.openclaw/persona.md"
bash scripts/persona_client.sh
```

From elsewhere, create a request with the curl. You should see `[persona-client] handling request_id=...` and then get the Telegram approval. If you see "error contacting persona-service" or no "handling" line, the problem is network or wrong URL/client_id.

If (1)–(3) pass and you still don’t get Telegram when using the wrapper, the approval bot token or chat ID may be wrong; check `TELEGRAM_BOT_TOKEN` and `TELEGRAM_OWNER_CHAT_ID` in `skills.entries["persona-consent-telegram-hub"].env`.
