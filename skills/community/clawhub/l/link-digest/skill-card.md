## Description: <br>
Processes public links shared in a designated Discord channel by validating and fetching the URL, summarizing the content, creating a Discord thread, and saving synthesized notes to a local knowledge base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zerone0x](https://clawhub.ai/user/zerone0x) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, team members, and community managers use this skill to turn links from an interesting-findings Discord channel into compact thread summaries and structured local knowledge-base notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetching external links can expose the agent to non-public URL access or prompt-injection content. <br>
Mitigation: Validate each URL before fetching, allow only public HTTP(S) hostnames, block private, loopback, metadata, and non-HTTP schemes, and treat fetched content as untrusted. <br>
Risk: Discord and knowledge-base outputs could accidentally reproduce raw untrusted page content. <br>
Mitigation: Write only the agent's synthesized summaries to Discord threads and KB files, and review generated KB commits before pushing or sharing them. <br>
Risk: Knowledge-base commits could include files outside the intended note directory. <br>
Mitigation: Configure KB_DIR as a dedicated folder and commit only files within that directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zerone0x/link-digest) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, Discord thread messages, local knowledge-base entries, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Discord summaries are intended to stay under 500 characters, and KB entries should contain synthesized notes only.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
