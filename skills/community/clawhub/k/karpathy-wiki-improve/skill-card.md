## Description: <br>
Karpathy Wiki Improve helps an agent maintain a local markdown knowledge wiki with ingest, query, relink, lint, and deep-research workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangmengyang](https://clawhub.ai/user/zhangmengyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and external agents use this skill to organize bookmarks and research material into a traceable markdown wiki, answer questions from that wiki, and maintain links, quality checks, and research gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or update markdown wiki files and maintain bidirectional links, so an overly broad wiki root could affect files outside the intended knowledge base. <br>
Mitigation: Configure the wiki root narrowly and review planned file changes before ingest, relink, lint, or research runs. <br>
Risk: Deep-research and query workflows may use web search or fetched sources, which can introduce outdated, incorrect, or untrusted material into the wiki. <br>
Mitigation: Review cited URLs and generated pages before relying on them, and keep source URLs attached to claims for later verification. <br>
Risk: Periodic maintenance wording could lead to automatic lint, relink, or quality checks if the agent environment enables scheduled activity. <br>
Mitigation: Enable periodic maintenance only when automatic checks are desired and confirm write actions before they modify the wiki. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/zhangmengyang/karpathy-wiki-improve) <br>
- [Andrej Karpathy LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with structured plans, wiki page templates, reports, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or write local wiki files under the configured wiki root and may use web research to supplement wiki content.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
