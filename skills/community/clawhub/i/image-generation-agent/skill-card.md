## Description: <br>
Image Generation Agent helps agents create or edit images from text prompts and optional reference images through AgentPMT-hosted Google Gemini image generation actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Designers, marketers, e-commerce operators, content creators, and agents use this skill to generate or edit images from prompts and up to four reference images. It supports draft previews and 0.5K to 4K final renders for product visuals, social graphics, ad creative, concept art, icons, and brand assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, reference images, and public image URLs are sent to AgentPMT and its image provider. <br>
Mitigation: Do not submit confidential, regulated, or private images unless account terms and retention controls fit the use case. <br>
Risk: Generated files are returned through signed URLs and stored in AgentPMT File Manager for the configured expiration period. <br>
Mitigation: Use the shortest practical expiration period and manage generated files according to the user's retention needs. <br>
Risk: Using the tool may require AgentPMT account credentials or payment-related setup. <br>
Mitigation: Use the setup skills for credential handling and never place secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs. <br>


## Reference(s): <br>
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/image-generation-agent) <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/image-generation-agent) <br>
- [Action schema](artifact/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Images, JSON, Guidance] <br>
**Output Format:** [Markdown guidance and JSON tool-call responses with signed image URLs and file metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated image bytes are saved to AgentPMT File Manager rather than returned inline; outputs include file_id, filename, signed URL, MIME type, size, width, and height.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
