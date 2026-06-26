## Description: <br>
AI image upscaling using Real-ESRGAN. 2x/3x/4x super-resolution for photos and general images. $0.10 USDC via x402. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ntriq-gh](https://clawhub.ai/user/ntriq-gh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to submit jpg, png, or webp images or image URLs to Ntriq for 2x, 3x, or 4x super-resolution. It is useful when an agent needs to improve image resolution through a paid x402 API call. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided images or image URLs to Ntriq for remote processing. <br>
Mitigation: Use it only with images you are comfortable sending to Ntriq, and avoid private, sensitive, or internal-only images unless you trust the provider's data handling. <br>
Risk: Each successful call is expected to spend $0.10 USDC through x402. <br>
Mitigation: Confirm payment headers, wallet limits, and intended spend before execution. <br>


## Reference(s): <br>
- [Ntriq x402 service homepage](https://x402.ntriq.co.kr) <br>
- [Image upscale API endpoint](https://x402.ntriq.co.kr/image-upscale) <br>
- [x402 protocol](https://x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [JSON API response containing base64-encoded PNG image data, with Markdown guidance and shell examples for agents.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an x402 payment header; supports 2x, 3x, or 4x scale and general or photo mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
