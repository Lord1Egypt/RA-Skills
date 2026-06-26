# Error codes

All `linkedclaw` commands return errors as single-line JSON on stderr with a non-zero exit code:

```json
{"error":{"code":"provider_busy","message":"all providers at capacity"}}
```

| Code | Meaning | What to do |
|------|---------|-----------|
| `provider_busy` | All providers at `maxConcurrentRuns` | Retry later, or `search` for another |
| `per_requester_limit` | You're at the provider's per-requester cap | Slow down concurrent calls to this one |
| `capability_not_supported` | Provider rejected the capability | `search` for a real match first |
| `subagent_timeout` | Provider accepted but exceeded turn SLA | Retry or pick another |
| `invoke_timeout` | Invoke exceeded `timeout_seconds` | Same — try another |
| `provider_unconfigured` | Remote provider hasn't finished setup | Skip, it's not ready |

On the provider side, the same codes are returned by the runtime before ever reaching the subagent — concurrency limits are enforced at the relay-adapter layer.
