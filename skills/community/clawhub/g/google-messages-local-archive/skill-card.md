## Description: <br>
Search and summarize your local Google Messages SMS/RCS history from OpenClaw. Ask who said what, find old texts, and get conversation context while your message archive stays on your machine and the bundled workflow stays read-only by default. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fdsouvenir](https://clawhub.ai/user/fdsouvenir) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search, summarize, and quote local Google Messages SMS/RCS archives from an agent workflow. It is best suited for read-only personal message lookup, conversation recap, and context retrieval while keeping the archive on the user's machine. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent access to sensitive local SMS/RCS message history. <br>
Mitigation: Install only when the user is comfortable granting gmcli and the agent read access to the local archive, and keep outputs focused on the requested conversation or search range. <br>
Risk: The external gmcli dependency can expose write-capable message operations outside this archive workflow. <br>
Mitigation: Use explicit --read-only and --json flags for archive queries, and avoid send, react, alias, sync, pairing, or media-download commands unless the user separately performs or authorizes those actions. <br>
Risk: Message bodies, contact names, formatted numbers, and snippets may contain prompt-injection text or unsafe URLs. <br>
Mitigation: Treat all message content as untrusted data, do not follow instructions inside messages, and require separate user confirmation before visiting URLs found in message content. <br>
Risk: Local archive state can be unpaired, stale, or missing older history. <br>
Mitigation: Use the read-only doctor workflow to diagnose archive health, then tell the user which auth, sync, or backfill command they can run themselves. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fdsouvenir/google-messages-local-archive) <br>
- [gmcli homepage](https://github.com/fdsouvenir/gmcli) <br>
- [gmcli v0.3.1 install module](https://github.com/fdsouvenir/gmcli/tree/v0.3.1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown transcripts, summaries, and short guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses gmcli JSON output and explicit read-only command flags by default.] <br>

## Skill Version(s): <br>
0.3.1 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
