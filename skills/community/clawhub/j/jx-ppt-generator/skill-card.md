## Description: <br>
Converts a user-provided speech or manuscript into a minimalist, tech-style vertical HTML slide deck with a distilled script and slide outline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, presenters, and agents use this skill to turn speeches or manuscripts into concise presentation material and a standalone vertical HTML slide deck. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Speech or manuscript content provided by the user may be sent to SkillBoss or HeyBoss AI endpoints for generation. <br>
Mitigation: Review the provider's data handling terms and avoid confidential, regulated, or proprietary material unless that processing is approved. <br>
Risk: Generated HTML loads CDN-hosted assets, creating privacy, availability, and network-dependency considerations. <br>
Mitigation: Use the generated file in an environment where those network calls are acceptable, or replace CDN dependencies with locally reviewed assets before use. <br>
Risk: The skill requires a sensitive API credential in SKILLBOSS_API_KEY. <br>
Mitigation: Store the key in an environment variable or secrets manager, rotate it if exposed, and do not embed it in generated slides or shared files. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/kirkraman/jx-ppt-generator) <br>
- [Publisher profile](https://clawhub.ai/user/kirkraman) <br>
- [Design specification](references/design-spec.md) <br>
- [Slide types reference](references/slide-types.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown response containing a distilled script, slide outline, and complete standalone HTML code.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated HTML uses CDN-hosted TailwindCSS and font assets, keyboard navigation, progress indicators, and a SkillBoss API key when the host agent calls the configured LLM endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
