## Description: <br>
A documentation-only meta-skill that teaches AI agents how to generate secure, zero-exposure skills using MGC Blackbox for credential management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zkeviny](https://clawhub.ai/user/zkeviny) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this documentation-only meta-skill to design skills that interact with credentialed services while keeping secrets outside the model. It provides guidance for Zero-Exposure skill structure, MGC Blackbox credential storage, and local-script boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Skills generated from this guidance may mishandle credential stores, print secrets, or perform sensitive actions without explicit user approval. <br>
Mitigation: Review generated skills before use and verify that secrets stay in MGC Blackbox, local scripts do not expose credentials, and sensitive actions require clear user approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zkeviny/key-safe-skill-generator) <br>
- [Publisher profile](https://clawhub.ai/user/zkeviny) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with conceptual pseudocode and package structure examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; no executable runtime entrypoint.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
