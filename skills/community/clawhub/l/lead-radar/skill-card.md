## Description:

Lead Radar scans Reddit, Hacker News, Indie Hackers, Stack Overflow, Quora, Hashnode, Dev.to, GitHub, and Lobsters for buying-intent posts and sends the top leads to Telegram with draft replies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bencpnd](https://clawhub.ai/user/bencpnd)

### License/Terms of Use:

MIT

## Use Case:

Sales and marketing users configure their offer description so the skill can find warm leads across developer and community platforms. It helps them review ranked opportunities and copy a suggested reply into the original conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Offer descriptions and scraped post snippets are sent to Google Gemini for keyword extraction, intent scoring, and draft replies.

Mitigation: Avoid sensitive offer details, review applicable Google and vendor terms, and install only when this external processing is acceptable.

Risk: License validation contacts the vendor backend and may return a vendor-provided Gemini API key.

Mitigation: Review the vendor license-backend setup and keep local license, Supabase, Gemini, and Telegram secrets restricted to the runtime environment.

Risk: Scraped posts may contain prompt-injection text that affects AI-generated draft replies.

Mitigation: Review every generated reply before posting and add stricter prompt and output guardrails before relying on automated responses.

Risk: Telegram delivery uses HTML parse mode, so formatting and escaping bugs could affect message rendering.

Mitigation: Keep delivery to the intended private chat and harden HTML escaping before broad or shared-channel use.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/bencpnd/skills/lead-radar)
- [Lead Radar product site](https://lead-radar.pro)
- [GitHub REST Search API documentation](https://docs.github.com/en/rest/search)
- [Stack Exchange API documentation](https://api.stackexchange.com/docs)
- [Forem API documentation](https://developers.forem.com/api/v1)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Telegram message text with source links, intent scores, brief rationale, scan status, and draft replies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Daily scheduled delivery; result count depends on source availability, rate limits, and offer specificity.]

## Skill Version(s):

1.3.5 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
