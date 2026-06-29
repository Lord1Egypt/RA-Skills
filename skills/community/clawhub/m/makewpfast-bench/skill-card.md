## Description: <br>
This skill helps agents answer questions about the measured speed impact of WordPress plugins and themes by using the bundled MakeWPFast benchmark CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marcindudekdev](https://clawhub.ai/user/marcindudekdev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site operators, and performance engineers use this skill to look up, compare, or audit the real measured TTFB, memory, query, and speed-grade impact of WordPress.org plugins and themes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a paid MakeWPFast API key and can consume quota when benchmark rows are not cached. <br>
Mitigation: Configure credentials deliberately, check quota before broad audits, prefer cached results, and use batch-aware commands such as compare and audit. <br>
Risk: Local site audits use wp-cli to identify active plugin slugs and may send those slugs to the external benchmark API. <br>
Mitigation: Run audits only on intended WordPress paths and review the cache, calls log, and API-key storage location when tighter operational control is needed. <br>


## Reference(s): <br>
- [MakeWPFast Benchmark API](https://makewpfast.com/api/) <br>
- [MakeWPFast API Reference](references/api.md) <br>
- [Worked Examples](references/examples.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/marcindudekdev/makewpfast-bench) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with inline shell commands and optional JSON parsed from the CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include benchmark grades, TTFB, memory, query deltas, quota status, setup guidance, and faster-alternative guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
