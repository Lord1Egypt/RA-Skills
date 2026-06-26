## Description: <br>
Docmosis helps an agent inspect Docmosis templates, check environment readiness and quota, and render documents through the OOMOL oo CLI connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers with an OOMOL-connected Docmosis account use this skill to list templates, inspect template metadata and structure, check processing environment status, and render Docmosis documents from JSON data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill invokes the OOMOL oo CLI against a Docmosis account using server-side credentials. <br>
Mitigation: Use the intended signed-in OOMOL account, inspect the live action schema, and confirm payloads before running commands that process account data. <br>
Risk: Document rendering can process user-provided JSON and return delivery metadata or base64 output that may contain sensitive business content. <br>
Mitigation: Confirm the selected template and input data before rendering, and handle generated output according to the user's data handling requirements. <br>
Risk: The server security review marked the release suspicious and advises reviewing execution behavior before use. <br>
Mitigation: Review the security guidance before installing or invoking the skill, and avoid broad external-change workflows unless the user explicitly intends them. <br>


## Reference(s): <br>
- [ClawHub Docmosis skill page](https://clawhub.ai/oomol/oo-docmosis) <br>
- [Docmosis homepage](https://www.docmosis.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, JSON, configuration guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON response handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the oo CLI, an OOMOL sign-in, and a connected Docmosis account; action schemas are checked before command payloads are built.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
