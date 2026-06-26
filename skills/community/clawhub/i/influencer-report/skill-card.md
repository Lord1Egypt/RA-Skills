## Description: <br>
Generate a comprehensive influencer vetting report from a creator profile URL or video URLs, using Memories.ai video intelligence for brand safety and content quality analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shawnshenopeninterx](https://clawhub.ai/user/shawnshenopeninterx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Marketing, partnership, and creator-review teams use this skill to vet influencers by analyzing recent social videos for production quality, content relevance, brand-safety signals, and engagement context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Profile mode can pull unrelated videos from the Memories.ai library into a creator-specific vetting report. <br>
Mitigation: Prefer direct video URLs, or review the profile workflow and report inputs to confirm every analyzed video belongs to the requested creator. <br>
Risk: The skill sends creator profile URLs or video URLs to Memories.ai and requires Memories.ai API keys. <br>
Mitigation: Install only where sharing those URLs with Memories.ai is acceptable, and provide API keys through environment variables with normal secret-handling controls. <br>


## Reference(s): <br>
- [Influencer Report on ClawHub](https://clawhub.ai/shawnshenopeninterx/influencer-report) <br>
- [Influencer Vetting Report Format](references/report-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, configuration] <br>
**Output Format:** [Markdown influencer vetting report, optionally written to a file by the bundled script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MEMORIES_V1_API_KEY and MEMORIES_API_KEY. Accepts a creator profile URL or direct video URLs.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
