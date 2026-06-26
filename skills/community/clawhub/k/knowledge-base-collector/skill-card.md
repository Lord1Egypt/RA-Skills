## Description: <br>
Collects and organizes a personal knowledge base from web, X/Twitter, WeChat URLs, and screenshots, with local storage, tagging, search helpers, and fallback handling for blocked WeChat fetches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reed1898](https://clawhub.ai/user/reed1898) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and personal knowledge workers use this skill to save URLs, screenshots, notes, tags, and searchable metadata into a local knowledge base. It is suited to agent-assisted capture, later search, and digest preparation for user-selected material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved URLs, screenshots, notes, OCR text, and search metadata can persist sensitive personal or credential-bearing content in the local knowledge base. <br>
Mitigation: Redact tokens, verification codes, private links, screenshots, and OCR text before ingesting; use an appropriate KB_ROOT location and access controls for the saved files. <br>
Risk: URL ingestion can send saved URLs and extracted content through r.jina.ai, which may be inappropriate for private or authenticated material. <br>
Mitigation: Only ingest links that are acceptable to process through that extraction service, and avoid tokenized, private, or login-gated URLs unless the user has reviewed the exposure. <br>
Risk: The WeChat fallback may depend on a connected macOS node and can run node-side fetch commands on a user-controlled device. <br>
Mitigation: Confirm the exact target device and command before using the connected-node fallback, and fall back to placeholder entries when node access is unavailable or uncertain. <br>
Risk: WeChat Official Account pages may be blocked or incomplete due to verification controls. <br>
Mitigation: Accept placeholder entries with blocked status and manual-review tags, then backfill content only after a successful user-approved fetch. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/reed1898/knowledge-base-collector) <br>
- [r.jina.ai extraction service](https://r.jina.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, plus local content.md, meta.json, and index.jsonl files produced by the skill scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores entries under a configurable KB_ROOT and uses a deterministic local index for search and digest workflows.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
