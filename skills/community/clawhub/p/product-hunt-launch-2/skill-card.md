## Description: <br>
Product Hunt Launch helps agents plan and optimize Product Hunt launches with listing specs, gallery strategy, tagline guidance, maker comments, research commands, and launch-day tactics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okaris](https://clawhub.ai/user/okaris) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External makers, startup teams, and launch operators use this skill to prepare Product Hunt listing assets, research comparable launches, draft maker comments, and coordinate launch-day engagement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes an external curl-to-shell installer workflow for inference.sh. <br>
Mitigation: Use the documented manual checksum verification path before installing, and run installer commands only in an environment where the user accepts that dependency. <br>
Risk: Research and image-generation prompts may send launch plans, product details, or other sensitive information to an external service. <br>
Mitigation: Avoid submitting confidential launch plans, credentials, customer data, or unreleased product details unless the service's data handling and billing terms are acceptable. <br>
Risk: Launch guidance can become inaccurate as Product Hunt policies, listing limits, or norms change. <br>
Mitigation: Review final launch copy and tactics against current Product Hunt requirements before publishing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/okaris/product-hunt-launch-2) <br>
- [inference.sh](https://inference.sh) <br>
- [inference.sh CLI installer](https://cli.inference.sh) <br>
- [inference.sh CLI checksums](https://dist.inference.sh/cli/checksums.txt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with tables, checklists, and inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include inference.sh CLI commands for research and image generation.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
