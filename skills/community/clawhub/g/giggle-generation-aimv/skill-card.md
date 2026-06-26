## Description: <br>
Creates AI music videos by generating music from text prompts or using custom lyrics with a reference image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patches429](https://clawhub.ai/user/patches429) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run Giggle.pro's MV trustee workflow from an agent: configure a Giggle API key, choose prompt or custom-lyrics mode, submit a reference image and parameters, and receive a completed video download URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default workflow can automatically spend from the user's Giggle account when payment is pending. <br>
Mitigation: Use only after the user approves the spend risk, or require a version that stops at payment, shows price or order details, and asks for explicit approval before calling the pay endpoint. <br>
Risk: The skill requires a Giggle API key that can create projects and pay for MV generation. <br>
Mitigation: Confirm the user is comfortable providing that credential before installation or execution. <br>


## Reference(s): <br>
- [Giggle.pro](https://giggle.pro/) <br>
- [ClawHub skill page](https://clawhub.ai/patches429/giggle-generation-aimv) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; script commands return JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return a signed video download URL when the MV workflow completes.] <br>

## Skill Version(s): <br>
0.0.10 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
