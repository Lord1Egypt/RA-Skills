## Description: <br>
Generate a weekly Torah portion summary from Sefaria with optional Hebrew text, verse count, sample verses, and JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abeperl](https://clawhub.ai/user/abeperl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to get concise weekly Torah portion overviews, select a named parsha, include Hebrew availability, or produce JSON suitable for downstream workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes internet requests to public Hebcal and Sefaria APIs when used. <br>
Mitigation: Use it only in environments where outbound access to those services is acceptable, and review network access expectations before installation. <br>
Risk: Broad Torah-related triggers may activate the skill during adjacent religious-content discussions. <br>
Mitigation: Confirm the user wants a parsha summary before invoking it when the request is ambiguous. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/abeperl/parsha-summary) <br>
- [Publisher Profile](https://clawhub.ai/user/abeperl) <br>
- [Sefaria API](https://www.sefaria.org/api) <br>
- [Hebcal API](https://www.hebcal.com/hebcal) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands] <br>
**Output Format:** [Plain text summary or JSON object, with command examples documented in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional word limit, named parsha selection, Hebrew availability flag, verse count, and sample verses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
