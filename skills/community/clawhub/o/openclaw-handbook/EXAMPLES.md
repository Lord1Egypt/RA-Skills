# Worked Routing Examples

Canonical question → decision tree branch → fetch → citation.
These are few-shot anchors, not answers. Always run `scripts/fetch.sh <path>` before replying.

---

**Q: "How do I write a good SOUL.md?"**
Branch: IDENTITY → `concepts/soul.md`
Fetch: `scripts/fetch.sh concepts/soul`
Cite: `https://docs.openclaw.ai/concepts/soul.md`
Anti-pattern check: don't conflate with AGENTS.md.

---

**Q: "Can two agents share the same agentDir?"**
Branch: MULTI-AGENT → `concepts/multi-agent.md`
Fetch: `scripts/fetch.sh concepts/multi-agent`
Cite: `https://docs.openclaw.ai/concepts/multi-agent.md`
Anti-pattern check: sharing agentDir → auth/session collisions.

---

**Q: "Does `openclaw cron add` keep a persistent session by default?"**
Branch: AUTOMATION → `automation/cron-jobs.md`
Fetch: `scripts/fetch.sh automation/cron-jobs`
Cite: `https://docs.openclaw.ai/automation/cron-jobs.md`
Anti-pattern check: default is `isolated`, not persistent.

---

**Q: "How do I set up Telegram as a channel?"**
Branch: CHANNELS → `channels/telegram.md`
Fetch: `scripts/fetch.sh channels/telegram`
Cite: `https://docs.openclaw.ai/channels/telegram.md`

---

**Q: "How does vector memory (QMD) differ from active memory?"**
Branch: MEMORY → `concepts/memory-qmd.md` (primary), `concepts/active-memory.md` (comparison)
Fetch two pages (one extra allowed by Behavior Contract step 5).
Cite both URLs.

---

**Q: "What is dreaming in OpenClaw?"**
Branch: MEMORY → `concepts/dreaming.md`
Fetch: `scripts/fetch.sh concepts/dreaming`
Cite: `https://docs.openclaw.ai/concepts/dreaming.md`

---

**Q: "How does session pruning work and when does it trigger?"**
Branch: SESSIONS → `concepts/session-pruning.md`
Fetch: `scripts/fetch.sh concepts/session-pruning`
Cite: `https://docs.openclaw.ai/concepts/session-pruning.md`

---

**Q: "How do I install a skill from clawhub?"**
Branch: TOOLS / SKILLS → `tools/skills.md`
Fetch: `scripts/fetch.sh tools/skills`
Cite: `https://docs.openclaw.ai/tools/skills.md`

---

**Q: "Which AI providers does OpenClaw support?"**
Branch: PROVIDERS — ambiguous specific, start with discovery.
Run: `scripts/find.sh provider` → pick top result → fetch.
Cite fetched URL.

---

**Q: "How is the gateway sandbox network configured?"**
Branch: GATEWAY → `gateway/sandboxing.md` (primary), `gateway/network-model.md` (related)
Fetch primary; fetch secondary only if primary doesn't cover the question.

---

**Q: "My Telegram bot isn't responding — where do I start?"**
Branch: CHANNELS → `channels/troubleshooting.md`
Fetch: `scripts/fetch.sh channels/troubleshooting`
Cite: `https://docs.openclaw.ai/channels/troubleshooting.md`

---

**Q: "Can I run OpenClaw on a Raspberry Pi?"**
Branch: INSTALL — two candidates: `install/raspberry-pi.md` and `pi.md`.
Default to `install/raspberry-pi.md` (more specific). If it 404s or lacks content, fall back to `pi.md`.

---

**Q: "Is there an OpenAPI spec for the HTTP API?"**
Branch: WEB / API → `api-reference/openapi.json`
Fetch: `scripts/fetch.sh api-reference/openapi.json`
Cite: `https://docs.openclaw.ai/api-reference/openapi.json`

---

**Q: "How do I install the iOS app and pair it with my gateway?"**
Branch: PLATFORMS → `platforms/ios.md`
Fetch: `scripts/fetch.sh platforms/ios.md`
Cite: `https://docs.openclaw.ai/platforms/ios.md`

---

**Q: "How do I publish a skill to ClawHub?"**
Branch: CLAWHUB → `clawhub/publishing.md` (primary). If question is about the manifest fields, fetch `clawhub/skill-format.md` instead.
Fetch: `scripts/fetch.sh clawhub/publishing`
Cite: `https://docs.openclaw.ai/clawhub/publishing.md`

---

**Q: "Which environment variables does OpenClaw read at startup?"**
Branch: HELP / FAQ → `help/environment.md`
Fetch: `scripts/fetch.sh help/environment`
Cite: `https://docs.openclaw.ai/help/environment.md`

---

**Q: "Can I send a voice note from WhatsApp and have the agent transcribe it?"**
Branch: NODES → `nodes/audio.md` (primary), `nodes/media-understanding.md` (transcription/understanding context).
Fetch primary first; fetch secondary only if the answer is incomplete.
Cite the URL(s) actually used.

---

**Q: "Why did BlueBubbles support get removed and what do I do instead?"**
Branch: ANNOUNCEMENTS → `announcements/bluebubbles-imessage.md` (context), then CHANNELS → `channels/imessage.md` (new path).
Fetch both; this is an explicit two-page case.
Cite both URLs.

---

**Q: "Where can I see what the default AGENTS.md ships with?"**
Branch: REFERENCE → `reference/AGENTS.default.md`
Fetch: `scripts/fetch.sh reference/AGENTS.default`
Cite: `https://docs.openclaw.ai/reference/AGENTS.default.md`

---

**Negative example — out of scope**

Q: "How do I configure hooks in Claude Code?"
Response: "Claude Code hooks are not covered here. For OpenClaw automation hooks see `automation/hooks.md`."
Do NOT extrapolate OpenClaw docs to explain Claude Code.
