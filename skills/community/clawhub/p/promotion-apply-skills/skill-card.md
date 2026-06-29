## Description: <br>
Helps agents create, query, copy, update, change status for, and manage creatives and related materials for Lingqu banner promotions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cloudmusiccio](https://clawhub.ai/user/cloudmusiccio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Promotion operators and their agents use this skill to manage Lingqu banner promotion workflows, including creation, reservation, copying, status changes, creative material updates, image validation, and promotion lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change real promotion and administrator state. <br>
Mitigation: Use it only in controlled environments with expected MWS access, require explicit user intent before create, copy, update, status, or admin actions, and review write actions before execution. <br>
Risk: Helper scripts can automatically install packages while processing images. <br>
Mitigation: Preinstall and pin Pillow and requests in the runtime environment instead of allowing runtime package installation. <br>
Risk: Image processing can fetch user-supplied URLs. <br>
Mitigation: Restrict image URLs to trusted sources where possible and validate images before upload or promotion material updates. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cloudmusiccio/skills/promotion-apply-skills) <br>
- [Creative Dynamic Material Reference](artifact/references/creative-dynamic-material.md) <br>
- [Image Upload NOS Reference](artifact/references/image-upload-nos.md) <br>
- [MWS Shared Reference](artifact/references/mws-shared.md) <br>
- [Phase One Reserve Reference](artifact/references/phase-one-reserve.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON payload examples, and Python helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local intermediate files for promotion details, payload validation, and image resizing.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
