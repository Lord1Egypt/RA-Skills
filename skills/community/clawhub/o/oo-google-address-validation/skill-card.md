## Description: <br>
This skill lets an agent validate and standardize postal addresses through an OOMOL-connected Google Address Validation account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to validate and standardize postal addresses through an OOMOL-connected Google Address Validation account, including verdicts, parsed address details, and geocode data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The feedback-sending action can submit the final outcome of a completed validation sequence and is not clearly labeled as state-changing in the artifact. <br>
Mitigation: Review and explicitly approve any provide_validation_feedback payload before execution. <br>
Risk: First-time setup may require optional remote installer commands for the oo CLI. <br>
Mitigation: Review installer commands before approving them, and use an already installed oo CLI when available. <br>


## Reference(s): <br>
- [Google Address Validation documentation](https://developers.google.com/maps/documentation/address-validation) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-google-address-validation) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on live Google Address Validation connector schemas and may include validation verdicts, parsed address details, geocode data, response metadata, or setup guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
