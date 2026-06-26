## Description: <br>
Generate well-structured Linear tickets from bugs, features, and improvements by using the user's requirement and relevant codebase context to draft technical notes, acceptance criteria, and scope. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luduvigo](https://clawhub.ai/user/luduvigo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and product teams use this skill to turn bug reports, feature requests, and improvement ideas into Linear-ready ticket drafts. It can inspect relevant repository files when useful so the ticket includes concrete technical notes, acceptance criteria, out-of-scope items, and follow-up questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may read relevant repository files to draft stronger ticket details, which can surface secrets, customer data, or confidential implementation details in a ticket draft. <br>
Mitigation: Review generated tickets before posting to Linear and remove sensitive or confidential information. <br>
Risk: The skill may make reasonable assumptions and mark uncertain sections with [CONFIRM]. <br>
Mitigation: Resolve [CONFIRM] markers with the requester before treating the ticket as ready for execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/luduvigo/linear-ticket-creator) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/luduvigo) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Analysis] <br>
**Output Format:** [Markdown ticket draft] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include [CONFIRM] markers where user validation is needed before the ticket is finalized.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
