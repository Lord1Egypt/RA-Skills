## Description: <br>
Hyperthink runs an unattended triple-perspective research pipeline that scopes a topic, launches Optimist, Analyst, and Critic deep-dives, audits claims, and produces a synthesis plus executive brief. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[inxan3](https://clawhub.ai/user/inxan3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, analysts, and developers use Hyperthink to run a scoped, multi-perspective research workflow that produces section deep-dives, claim audits, a long-form synthesis, and an executive brief after one confirmation step. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unattended batch execution can run for hours and incur material Anthropic API cost. <br>
Mitigation: Confirm scope before launch, use scoped credentials where possible, monitor batch job state, and apply account-level spend limits if available. <br>
Risk: Research outputs and pipeline state are persisted locally under configured output directories. <br>
Mitigation: Avoid sensitive topics unless the output location is appropriate, and restrict access to /data/hyperthink/ and batch job state directories. <br>
Risk: Optional webhook or Telegram notifications can send completion details or deliverables outside the local environment. <br>
Mitigation: Leave notification variables unset unless the destination is trusted and suitable for the report contents. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/inxan3/hyperthink) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown research artifacts, JSON batch job definitions, shell commands, and optional DOCX brief output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces persistent pipeline files under /data/hyperthink/[slug]/; typical runs are long and can incur Anthropic API cost.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
