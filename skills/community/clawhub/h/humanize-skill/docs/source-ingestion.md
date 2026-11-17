# Source ingestion

`humanize-skill` can learn from real user writing without becoming a heavy account-ingestion product.

## Preferred order

For the quickest `humanizer`-style flow:

1. A pasted draft only. Use the default natural voice and do not block.

For stronger personal voice matching:

1. Pasted writing sample.
2. Local files selected by the user.
3. Exported account archives selected by the user.
4. Official host connectors, only after explicit permission.
5. Custom or third-party MCP connectors, only after explicit permission.

## Host connector guidance

Connector support is host-specific.

- **Codex**: OpenAI's official skills catalog currently does not provide Gmail, X/Twitter, LinkedIn, Instagram, Facebook, Microsoft 365, or Google Drive personal-voice ingestion skills. Codex can still use pasted samples, local files, exported archives, or custom MCP/skill bundles. Treat inbox and Slack use cases as integrations/workflows unless a concrete tool or connector is exposed in the current environment.
- **Claude / Claude Code**: Claude's official connector ecosystem includes first-party connectors for Gmail, Slack, Google Drive, Google Calendar, GitHub, and Microsoft 365. These can be excellent sources for real-user voice when the user explicitly authorizes access. Claude connectors are MCP-based, so third-party, enterprise, or self-built MCP connectors can extend to other platforms.
- **Social platforms**: no first-party X/Twitter, LinkedIn, Instagram, or Facebook connector should be assumed. Use platform export archives, browser-visible content with user approval, or a custom/third-party MCP connector.

Best voice sources, when available:

1. Sent emails or Gmail history.
2. Slack/DM messages.
3. Long-form docs, notes, essays, or Google Drive files.
4. Social posts and replies.
5. Chat exports.
6. Short pasted samples.

## Agent-supported local sources

The host agent can use whatever local reading tools are available in the environment. In practice, user-controlled sources usually include:

- `.txt`, `.md`, and other plain text files
- `.json` and `.jsonl` exports with text-like fields
- `.csv` and `.tsv` exports with columns such as `text`, `body`, `content`, `message`, and `full_text`
- folders of notes, posts, support replies, newsletters, or chat/email exports selected by the user

This is enough for many X/Twitter archive extracts, chat exports, newsletter drafts, support replies, and note collections after light preprocessing.

## Privacy rules

- Build compact profiles, not raw-message stores.
- Keep source labels and counts for provenance.
- Do not print private sample text in final answers.
- Use only user-controlled data.
- Treat live connectors as optional, explicit, and revocable.

## Compact profile shape

The agent can summarize samples into a compact inspectable profile like this:

```json
{
  "sample_count": 3,
  "sources": ["samples/email.txt", "samples/posts.jsonl"],
  "word_count": 1200,
  "sentence_count": 80,
  "avg_sentence_words": 15.2,
  "sentence_rhythm": "mixed",
  "paragraph_style": "brief",
  "punctuation": { ".": 80, ",": 42 },
  "top_words": ["product", "ship", "users"],
  "likely_tone": ["personal", "technical", "direct"]
}
```

Agents should use this profile as guidance, not as a rigid template.
