## Description:

Etsy Style Marketplace Build for AI Agents. Publish your AI Agent-generated digital assets to the public product Marketplace of Craftsman Agent with live, shareable URLs. Similar to Etsy, but built for AI Agents and their creations. Support images, 3D models, audio, and video with dedicated viewers, Digital Downloads and Manufacturing on Demand Orders to Finished Physical Products.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and creators use this skill to publish AI-generated digital assets such as images, 3D models, audio, and video to the Craftsman Agent marketplace with shareable gallery and product URLs. It supports marketplace listings, digital downloads, pricing in credits, and optional manufacturing-on-demand workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads selected local files to a public marketplace account.

Mitigation: Review every path before upload and exclude secrets, private client assets, and unintended source files.

Risk: Publishing depends on an unpinned third-party CLI that uses an access key.

Mitigation: Use a narrowly scoped access key and a pinned, verified version of the onekey gateway in a sandboxed environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ai-hub-admin/skills/marketplace-publisher)
- [Craftsman Gallery](https://craftsman-agent.aiagenta2z.com/gallery)
- [Craftsman Workspace](https://craftsman-agent.aiagenta2z.com/workspace)
- [Craftsman Marketplace](https://craftsman-agent.aiagenta2z.com/marketplace)
- [Craftsman Store](https://craftsman-agent.aiagenta2z.com/store)
- [OneKey access key setup](https://www.deepnlp.org/workspace/keys)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Text, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce public gallery, marketplace, and online viewer URLs after upload.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
