# Vision Hub — Sample Routing Logic

Paste this into your hub Discord channel's AGENTS.md (or merge with your existing one).

---

## 👁️ Vision Ingress Protocol

When you receive a message containing an image URL forwarded from WhatsApp (look for `[Ingress:WhatsApp]` prefix or a bare image URL), do the following:

1. **Do NOT** describe or analyze the image yourself
2. **Immediately** classify the image intent from the URL context or any accompanying text:
   - 🍷 **Wine** — bottle, label, glass, wine list
   - 🍵 **Tea** — tea tin, tea cake, tea leaves, packaging
   - 🚬 **Cigar** — cigar band, humidor, cigar box
   - 👤 **Contacts** — face, business card, name badge, event badge
   - 📄 **Other** — anything else; log it and ask for clarification
3. **Preview** the detected category and the exact allowlisted destination.
4. **Ask for confirmation** before cross-session forwarding or any persistent database/channel write, unless the user has explicitly enabled automatic routing for that named destination.
5. **Forward** using `sessions_send` only after the confirmation boundary is satisfied.
6. **Reply** with the actual result: e.g. "🍷 Routed to the approved Wine Bot destination."

### Example routing call (adapt session keys to your own setup)

```
sessions_send(
  sessionKey = "<your-wine-channel-session-key>",
  message = "[Vision Router] New image.\nType: Wine\nImage: <image_url>\n\nINSTRUCTION: Post the image to the channel, then analyze and log to your database."
)
```

### Rules
- One classification per image — pick the most likely category
- If intent is ambiguous, default to **Other** and ask the user
- Never store the image URL yourself — forward it immediately
- All destination session keys must be pre-configured by the user; never infer or guess them
- Do not route third-party or sensitive photos without appropriate consent
- Treat destination writes as external side effects and keep them visible to the user
