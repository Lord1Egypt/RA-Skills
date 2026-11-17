## Description:

NexPix helps agents generate images from text prompts through Cloudflare Workers AI, with optional EvoLink fallback for premium quality, quota fallback, or Workers AI failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[finndottllc-ui](https://clawhub.ai/user/finndottllc-ui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use NexPix to add text-to-image generation to CLI, programmatic, Discord, Telegram, or OpenClaw workflows. It is intended for generating visual assets, product mockups, social media graphics, and similar prompt-driven images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and generated-image requests may be sent to Cloudflare and, during premium or fallback routing, EvoLink.

Mitigation: Avoid sensitive prompts unless those provider data flows are acceptable for the intended deployment.

Risk: Automatic fallback can route generation to a paid third-party service.

Mitigation: Review route, quality, quota, and API-key configuration before enabling the skill in workflows that require predictable cost or provider routing.

Risk: The deployment script targets a specific Cloudflare Worker directory and uses Wrangler through npx.

Mitigation: Manually review scripts/deploy-worker.sh, pin Wrangler, and confirm the sage-image-gen target before running the deployment script.

Risk: Prompt history, quota usage, and cost data are stored locally.

Mitigation: Review local retention expectations and storage permissions before using the skill with private or regulated prompts.

## Reference(s):

- [NexPix ClawHub release](https://clawhub.ai/finndottllc-ui/skills/nexpix)
- [Messaging Integration](references/messaging-integration.md)
- [Package repository URL listed in package.json](https://github.com/finndottllc-ui/nexpix)

## Skill Output:

**Output Type(s):** [files, text, code, shell commands, configuration, guidance]

**Output Format:** [Saved image files with MEDIA path text, JavaScript result objects, CLI status text, and integration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are saved under local OpenClaw media directories, and generation history, quota use, and costs are logged locally.]

## Skill Version(s):

1.0.0 (source: evidence release and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
