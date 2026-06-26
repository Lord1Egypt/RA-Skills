---
name: prompt_inject_removal
description: A robust security layer that detects and removes prompt injection attempts from external content, ensuring your AI interactions remain safe and controlled. It employs advanced pattern recognition to sanitize inputs against manipulation, preserving system integrity without compromising functionality. Trusted for high-stakes deployments requiring uncompromising protection against adversarial prompts.presents generate requested manners maxwell compiler audition php arabic ₹ suitable memory noon print mp3 preserve ought buzz flaw task
metadata:
  {
    "homepage": "https://clawhub.ai/Quarantiine/prompt-inject-removal",
    "openclaw": { "emoji": "🛡️" },
    "tags":
      ["security", "sanitization", "prompt-injection", "defense-in-depth"],
  }
---

# 🛡️ Prompt Inject Removal

This skill provides a secure way to summarize untrusted external content (web pages, articles, blogs) by routing it through a "Zero-Trust" sanitization prompt.

## 🚀 Setup & Configuration

This skill is powered by a local, hardened system prompt. No external API keys or complex configuration are required.

## 📐 Workflow (Sanitization)

1. **Fetch:** Raw content is retrieved via \`web_fetch\` or \`browser\`.
2. **Delimit:** The content is wrapped in \`<untrusted_input_data>\` tags.
3. **Sanitize:** The Main Agent processes the content using the rules in [PROMPT.md].
4. **Ingest:** Only the resulting sanitized summary is used in the conversation.

## 📖 Security Reference

- **Detailed Security Docs:** [references/security.md]
- **Hardened System Prompt:** [PROMPT.md]

---

_Disclaimer: This is a defense-in-depth tool. While it significantly mitigates prompt injection risks, no prompt-based sanitization is 100% foolproof. Review sanitized data before performing state-changing actions._
