## Description: <br>
When the user wants to conduct industry research, keyword research for a campaign, search demand analysis, intent mapping, audience research, or understand what people are searching for. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mariokarras](https://clawhub.ai/user/mariokarras) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing, SEO, and campaign strategy teams use this skill to research search demand, keyword intent, audience questions, content gaps, and competitor positioning before planning campaigns or content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research may send client or market context to Exa, Firecrawl, or Ahrefs. <br>
Mitigation: Confirm those services are approved for the client data and research scope before running the skill. <br>
Risk: The skill reads product-marketing context files when present and creates or updates a report under .agents. <br>
Mitigation: Review the generated report path and contents before sharing or reusing the research artifact. <br>
Risk: Keyword volume, SERP, and audience findings can become stale or unavailable when tools or API credentials are missing. <br>
Mitigation: Use the per-section research timestamps and documented fallback notes to decide when a refresh or manual validation is needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mariokarras/industry-research) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown research brief with keyword tables, audience findings, content gap analysis, competitor landscape, and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a scoped research report under .agents with per-section research timestamps; target size is 3,000-5,000 words.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
