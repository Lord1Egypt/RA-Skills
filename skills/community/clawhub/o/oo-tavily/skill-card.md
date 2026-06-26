## Description: <br>
Operates Tavily through the OOMOL oo CLI connector for search, crawl, extract, map, usage, and research workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Tavily search, crawling, extraction, URL mapping, usage lookup, and research workflows through an OOMOL-connected Tavily account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected Tavily account through OOMOL. <br>
Mitigation: Install only when the user is comfortable connecting Tavily through OOMOL; the skill directs agents not to handle raw Tavily tokens. <br>
Risk: Write actions can create Tavily research jobs and may affect account usage or billing. <br>
Mitigation: Confirm the exact payload and intended effect with the user before running write actions such as create_research. <br>
Risk: Search, crawl, extract, and research actions can return untrusted web content. <br>
Mitigation: Treat returned web content as external source material and review results before relying on them for downstream decisions. <br>


## Reference(s): <br>
- [Tavily homepage](https://tavily.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub listing](https://clawhub.ai/oomol/oo-tavily) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before payload construction.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
