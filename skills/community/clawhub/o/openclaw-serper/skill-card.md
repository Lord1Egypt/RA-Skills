## Description: <br>
Searches Google through Serper and extracts clean readable full-page text from results for web research, current events, factual lookups, product comparisons, technical documentation, and other up-to-date internet questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nesdeq](https://clawhub.ai/user/nesdeq) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Agents and developers use openclaw-serper to run Serper-backed Google searches, fetch result pages, and return extracted page content when a task needs current or external web information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Serper and result pages are fetched from the web. <br>
Mitigation: Avoid searching for secrets, regulated data, or internal-only information unless that network exposure is acceptable. <br>
Risk: Fetched web content can be incomplete, blocked, stale, or misleading. <br>
Mitigation: Verify important claims against more than one source before relying on them. <br>
Risk: The integration requires storing a Serper API key. <br>
Mitigation: Store the key only in the expected local environment file or environment variable and avoid sharing it in prompts, logs, or search queries. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nesdeq/openclaw-serper) <br>
- [Serper API](https://serper.dev) <br>
- [Agent Skills Specification](spec/specification.mdx) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, text] <br>
**Output Format:** [Streamed JSON array with search metadata and extracted page-content result objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Serper API key; default mode returns web results, and current mode combines recent web and news results.] <br>

## Skill Version(s): <br>
3.1.1 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
