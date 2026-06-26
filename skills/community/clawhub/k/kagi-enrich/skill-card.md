## Description: <br>
Searches Kagi's non-commercial web (Teclis) and non-mainstream news (TinyGem) enrichment indexes for independent, ad-free content such as small-web sites, independent blogs, niche discussions, and non-mainstream news. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joelazar](https://clawhub.ai/user/joelazar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to retrieve independent web and non-mainstream news results from Kagi enrichment indexes when they need source discovery rather than a synthesized answer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The wrapper can download and immediately run an unverified prebuilt release binary. <br>
Mitigation: Prefer building from the included Go source. If using a prebuilt binary, verify the release checksum or signature before running it. <br>
Risk: The skill requires a paid Kagi API key and may incur per-query charges. <br>
Mitigation: Use KAGI_API_KEY only in a controlled environment, monitor Kagi API billing, and apply result limits where appropriate. <br>


## Reference(s): <br>
- [Kagi Enrichment API documentation](https://help.kagi.com/kagi/api/enrich.html) <br>
- [ClawHub Kagi Enrich listing](https://clawhub.ai/joelazar/kagi-enrich) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text result lists or structured JSON; documentation is Markdown with bash examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires KAGI_API_KEY; supports web/news index selection, result limits, JSON output, and request timeout.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
