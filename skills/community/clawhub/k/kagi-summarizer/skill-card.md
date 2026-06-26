## Description: <br>
Summarize any URL or text using Kagi's Universal Summarizer API, with support for multiple engines, bullet-point takeaways, and translation output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joelazar](https://clawhub.ai/user/joelazar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and other users use this skill to summarize articles, papers, PDFs, transcripts, forum threads, or pasted text through Kagi's Universal Summarizer API. It is suited for producing prose summaries, bullet-point takeaways, translated summaries, or JSON-formatted results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The wrapper can download and run a prebuilt GitHub release binary that server security evidence describes as unverified. <br>
Mitigation: Prefer building from the included Go source; if using a prebuilt binary, verify its checksum or signature before running it. <br>
Risk: Summarized content, API keys, token usage, and billing are handled through Kagi's API. <br>
Mitigation: Avoid submitting secrets, internal documents, or regulated data unless Kagi processing is approved, and monitor API-key usage and billing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/joelazar/kagi-summarizer) <br>
- [Kagi Universal Summarizer API](https://help.kagi.com/kagi/api/summarizer.html) <br>
- [Kagi API portal](https://kagi.com/settings/api) <br>
- [Kagi API pricing](https://kagi.com/settings?p=api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text summaries or structured JSON, with optional bullet takeaways and translated output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Token usage and API balance are reported to stderr for non-JSON output; users can choose engine, summary type, language, caching, and timeout options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
