# Troubleshooting

## `getaddrinfo ENOTFOUND http`

**Cause:** Either a double `http://http://` prefix in `baseUrl`, or `provider` is set to something other than `"ollama"`.

**Fix:**
- Verify `provider` is exactly `"ollama"` (not `"openai"`)
- Verify `baseUrl` is exactly `http://127.0.0.1:11434` — single `http://` prefix, no `/v1`, no trailing slash

**Wrong:**
```json
{ "provider": "openai", "remote": { "baseUrl": "http://http://127.0.0.1:11434/v1/" } }
```

**Right:**
```json
{ "provider": "ollama", "remote": { "baseUrl": "http://127.0.0.1:11434" } }
```

---

## `provider: "openai"` with Ollama baseUrl Doesn't Work

**Cause:** OpenClaw's `openai` provider uses a different request format than Ollama's native API.

**Fix:** Must use `provider: "ollama"` explicitly. Ollama is supported but not auto-detected — setting `"openai"` won't route to Ollama even with the correct baseUrl.

---

## Empty Results

**Cause:** Memory search is working but the index is empty or not yet built.

**Fix:** This is normal on first run. The index builds over time as you use OpenClaw. Check that Ollama is running and the model is loaded:

```bash
curl http://127.0.0.1:11434/api/tags
```

---

## Ollama Not Running

**Symptom:** `curl http://127.0.0.1:11434/api/tags` times out or returns connection refused.

**Fix:**
```bash
ollama serve
```

Or on macOS, start the Ollama app from Applications.

---

## Model Not Found

**Symptom:** Ollama reports the model doesn't exist.

**Fix:**
```bash
ollama pull nomic-embed-text
```

Verify it downloaded:
```bash
ollama list
```

---

## Config Changes Not Taking Effect

**Fix:** Restart the OpenClaw gateway after any config change:

```bash
openclaw gateway restart
```

---

## Memory Search Still Using Old Provider After Restart

**Cause:** OpenClaw may cache the provider selection at startup.

**Fix:** Full gateway stop and start:

```bash
openclaw gateway stop
openclaw gateway start
```
