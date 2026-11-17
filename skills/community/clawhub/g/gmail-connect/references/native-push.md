# Existing native Gmail push: recovery and migration notes

This is an **advanced reference**, not an automated mode of the bundled wizard. Prefer direct polling unless low-latency native hook delivery is a firm requirement. Preserve an existing working native connection until the replacement is verified.

## What the supplied incident proves

The user supplied OpenClaw 2026.9.6 gateway logs from 2026-09-26. Gmail plugin cleanup exceeded its retirement budget. Later starts failed specifically because `hooks.allowedSessionKeyPrefixes` did not allow the generated `hook:` namespace when no default session key was configured. These are distinct observations; the logs do not prove the cleanup error caused the invalid configuration.

The user subsequently corrected the existing hooks object to include:

```json
"allowedSessionKeyPrefixes": ["hook:"]
```

Then restarted the existing service:

```bash
systemctl --user restart openclaw-gateway.service
openclaw gateway status
```

The user confirmed:

```text
Runtime: running
Connectivity probe: ok
Listening: 127.0.0.1:18789
gateway/ws chat.history successful
```

This confirms recovered gateway startup and chat-history access. It does not alone prove Google push delivery, watch renewal, successful model execution, or Telegram delivery. Do not describe the entire email chain as verified based on this result.

## Native topology and ownership

Gmail watch → Google Pub/Sub → public HTTPS `/gmail-pubsub` → local watcher (commonly 127.0.0.1:8788) → authenticated local `/hooks/gmail` → configured OpenClaw reader agent.

The Cloud project must be consistent with the OAuth client used for the Gmail watch. Enable Gmail and Pub/Sub APIs, create the topic and subscription, and grant Gmail's publisher principal `gmail-api-push@system.gserviceaccount.com` the Pub/Sub publisher role on that topic. Confirm the actual subscription and endpoint, not just that a topic exists.

Only one owner may run the watcher. If OpenClaw manages it, do not also launch `gog gmail watch serve`, `openclaw webhooks gmail run`, or a second systemd watcher on the same port. Identify listeners without killing unknown processes:

```bash
ss -ltnp
systemctl --user status openclaw-gateway.service
```

## Conservative setup sequence

1. Inspect installed tool versions and help. Use official OpenClaw, gog, Google Cloud CLI, and Tailscale distribution channels. Never silently upgrade the running gateway as part of Gmail setup.
2. Back up the actual active OpenClaw configuration and related includes, along with a hash. Treat the backup as secret. Record current service and Funnel state. The file is JSON5-capable; do not parse it with a strict-JSON rewrite that discards comments/includes or other settings.
3. Authenticate Google Cloud and the Gmail account separately. Confirm that downloaded Desktop OAuth credentials and Pub/Sub resources refer to the intended project.
4. Before running the native wizard, review the current OpenClaw Gmail documentation and configure a restricted mail-reader agent and matching session policy. Preserve existing channel bindings and hook mappings. Do not paste a whole example config over a live config.
5. For the recorded broad policy, retain `hook:`. For a deliberately narrower new policy, use a matching `defaultSessionKey`, such as `hook:gmail:ingress`, and an allowlist containing `hook:gmail:`. Payload-derived session keys also require the applicable request-session-key permission. Validate all existing non-Gmail hooks before narrowing any shared allowlist.
6. Run `openclaw config validate` before a gateway restart. An invalid candidate must not replace a known-good configuration. A production native wizard should validate a staged configuration with the installed version's documented alternate-config mechanism before committing it; this release avoids the transaction entirely by not implementing native mutation.
7. Configure Gmail transport through the supported native setup command, rather than guessing private config fields. The transcript's successful externally managed ingress form was:

```bash
openclaw webhooks gmail setup \
  --account YOUR_GMAIL_ADDRESS \
  --project YOUR_GOOGLE_PROJECT_ID \
  --tailscale off \
  --push-endpoint "https://YOUR_APPROVED_FUNNEL_HOST/gmail-pubsub"
```

   Verify these flags using `openclaw webhooks gmail setup --help` on the installed version. Setup is a mutating operation and can print secrets; do not paste its raw output into public issues.
8. If using Funnel, expose only the watcher route. Keep the gateway dashboard, port 18789, and this package's setup wizard private. Tailscale Serve alone is private to the tailnet and is not a public Google push endpoint. Obtain tailnet administrator enablement if Funnel is disallowed. Do not reset or replace unrelated Funnel routes.
9. Keep the Pub/Sub-to-watcher credential distinct from the watcher-to-hook token and from gateway authentication. Confirm the generated subscription includes the authentication expected by the watcher. A bare public URL is not evidence of authenticated delivery.
10. Restart once after successful validation if required, verify gateway health, and verify that exactly one watcher started. If the gateway fails, restore only the backed-up files if their current hashes still match this setup's writes; otherwise stop and reconcile the concurrent changes. Restore the previously recorded service state, not a guessed one.

## Native delivery acceptance

Use a manually sent inbound test message with a unique subject from another account. Verify every stage separately: Gmail watch registration, Pub/Sub delivery, watcher forwarding, gateway admission, reader completion, and selected channel delivery. A hook HTTP 200/run ID proves admission, not necessarily completion. Keep email content untrusted and constrain the reader's tools.

Gmail watches expire and need periodic renewal; inspect the real expiration and renewal logs. Plan for duplicate/out-of-order notifications and gaps with durable history cursors. Pub/Sub retries and Gmail reconciliation should not produce duplicate outgoing messages. Record a reboot test and a token-revocation test before calling native integration reliable.

If replacing native push with this package, verify direct read access first. Then explicitly choose which automatic notification path owns delivery. Remove or disable only the old Gmail integration's resources once authorized; do not delete the entire project, all Pub/Sub resources, the whole hooks section, or all Tailscale routes.

## Another no-tunnel alternative

Pub/Sub pull can receive Gmail events using outbound connections, removing Funnel while retaining watch/topic/IAM/subscription complexity. It needs subscriber credentials, acknowledgement management and watch renewal. It is an architectural option for a later release, not implemented here. For this single-user Ubuntu application, direct polling has fewer setup components.

## Primary references

- https://docs.openclaw.ai/automation/cron-jobs/gmail
- https://docs.openclaw.ai/gateway/config-hooks
- https://docs.openclaw.ai/cli/webhooks
- https://developers.google.com/workspace/gmail/api/guides/push

The incident facts and the broad `hook:` recovery above come from the user's supplied terminal excerpts and final validation, not a reproduced experiment in this build environment.
