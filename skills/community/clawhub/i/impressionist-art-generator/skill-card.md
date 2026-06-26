## Description: <br>
Generates impressionist-style artwork from text prompts using the Neta/TalesOfAI image generation API, with optional size selection and reference-image style inheritance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blammectrappora](https://clawhub.ai/user/blammectrappora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, creators, educators, and developers use this skill to generate impressionist-style images for wall art, print concepts, art education, painting references, garden scenes, and portrait studies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, the Neta token, and reference image UUIDs are sent to the Neta/TalesOfAI service. <br>
Mitigation: Use the skill only with a trusted provider and publisher, and prefer scoped or trial tokens where available. <br>
Risk: Long-lived API tokens may be exposed if pasted directly into shared shell history or logs. <br>
Mitigation: Avoid placing long-lived secrets in shared command histories and rotate tokens if exposure is suspected. <br>
Risk: Generated art usage rights may depend on the external provider's terms. <br>
Mitigation: Review the provider's terms before using generated images for commercial or public release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blammectrappora/impressionist-art-generator) <br>
- [Neta Open](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text image URL, with status and error messages on stderr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports landscape, portrait, square, and tall image sizes, plus optional reference-image style inheritance by UUID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
