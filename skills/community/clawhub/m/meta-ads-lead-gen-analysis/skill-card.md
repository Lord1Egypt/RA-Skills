## Description: <br>
[Didoo AI] Specialized analysis module for Meta lead generation campaigns when CPL is elevated, lead quality is unclear, or downstream lead conversion needs diagnosis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elias-didoo](https://clawhub.ai/user/elias-didoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketers, operators, and agents use this skill to analyze Meta lead-generation campaigns when CPL is high, lead quality is unclear, or downstream conversion is weak. It focuses on CAPI status, audience fit, funnel stage, and lead-gen-specific benchmarks rather than e-commerce conversion logic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Meta access token and ad account ID for ad-performance analysis. <br>
Mitigation: Use a Meta token limited to the read-only ads_read scope and avoid granting broader permissions. <br>
Risk: Downstream recommendation workflows may propose or make changes after this analysis. <br>
Mitigation: Review any downstream recommendation skill separately before allowing it to modify campaigns or spend. <br>
Risk: Lead quality and CPL conclusions can be misleading when offline lead data is not sent back through CAPI. <br>
Mitigation: Verify CAPI and offline lead data status before treating CPL as actual lead cost or prioritizing campaign changes. <br>


## Reference(s): <br>
- [Didoo AI Blog](https://didoo.ai/blog) <br>
- [ClawHub skill page](https://clawhub.ai/elias-didoo/meta-ads-lead-gen-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/elias-didoo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, analysis, configuration, guidance] <br>
**Output Format:** [Markdown analysis with diagnostic sections and session context keys] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes lead-generation diagnostic context keys for downstream recommendation skills.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
