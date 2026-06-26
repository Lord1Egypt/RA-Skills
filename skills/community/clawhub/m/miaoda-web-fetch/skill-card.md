## Description: <br>
Helps an agent crawl a specific URL with `miaoda-studio-cli web-crawl` and extract or summarize the page content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nice1234-h](https://clawhub.ai/user/nice1234-h) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a user provides a known webpage URL and needs content fetched, summarized, or extracted. It guides when to use direct crawling versus search first, and shows text or JSON output options for downstream use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to fetch user-provided URLs over the network, which can expose private or sensitive pages if used carelessly. <br>
Mitigation: Use the skill only for URLs the user is comfortable requesting, and avoid private internal pages unless the data path and CLI behavior are understood. <br>
Risk: The behavior depends on `miaoda-studio-cli`, which is not bundled in the artifact. <br>
Mitigation: Install `miaoda-studio-cli` only from a trusted source before using the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nice1234-h/miaoda-web-fetch) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, text, JSON] <br>
**Output Format:** [Markdown with inline bash commands and option tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The referenced CLI can request external URLs over the network and can return text or JSON output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
