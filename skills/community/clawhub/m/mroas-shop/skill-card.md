## Description: <br>
Personal Agent shopping skill for OpenClaw and agentic commerce hosts that converts shopping or gifting intent plus summarized local preference context into SellToAI product recommendation cards with creator evidence and attribution-tracked buy links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zxlie](https://clawhub.ai/user/zxlie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let personal agents respond to shopping and gifting requests by calling SellToAI and rendering concise product cards with price, creator proof, personalization rationale, and buy or video actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shopping intent and summarized preference or recipient context may be sent to SellToAI. <br>
Mitigation: Send only compact preference and constraint summaries that the host already permits, and do not send raw notes, chat history, private profile text, or full memory documents. <br>
Risk: The installer can persistently install remote skill instructions into multiple local agent environments. <br>
Mitigation: Prefer manually installing a reviewed SKILL.md into the single agent environment intended for use. <br>
Risk: Buy and video links intentionally preserve attribution query parameters. <br>
Mitigation: Review returned commerce links before use and preserve the original URLs when showing them so attribution and creator credit remain intact. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/zxlie/mroas-shop) <br>
- [SellToAI Homepage](https://selltoai.ai) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline curl commands, JSON request shapes, and product-card rendering instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use summarized personal-agent context, never raw memory; preserves returned attribution URLs and can guide A2UI JSONL rendering when supported by the host.] <br>

## Skill Version(s): <br>
0.1.4 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
