## Description: <br>
Generates Morgan Stanley-style stock research report Word documents for sell-side and buy-side research workflows, including initiation, earnings update, industry deep dive, valuation, and investment memo reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yjkj999999](https://clawhub.ai/user/yjkj999999) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers, analysts, and fund managers can use this skill to generate structured DOCX equity research report templates from JSON data for review, editing, and internal workflow support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may falsely appear to be authentic Morgan Stanley research because the skill embeds Morgan Stanley branding, source lines, entity defaults, and disclosures. <br>
Mitigation: Remove or replace Morgan Stanley source lines, entity defaults, logo text, and disclosures before distribution, and clearly label outputs as user-generated templates not affiliated with Morgan Stanley. <br>
Risk: Financial report outputs could be mistaken for institutionally authored investment research. <br>
Mitigation: Require human financial, legal, and compliance review before sharing generated reports outside the user's organization. <br>


## Reference(s): <br>
- [MS Research Report ClawHub Release](https://clawhub.ai/yjkj999999/ms-research-report) <br>
- [Publisher Profile](https://clawhub.ai/user/yjkj999999) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Code, Shell commands, Guidance] <br>
**Output Format:** [DOCX report files with optional Python API usage and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates local .docx equity research reports; matplotlib charts are optional and fall back to text placeholders when unavailable.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release metadata, README) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
