## Description: <br>
Publish podcast episodes from RSS and Notion to Substack with Apple Podcasts embeds and images, then generate LinkedIn-ready companion posts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielfoch](https://clawhub.ai/user/danielfoch) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External creators and publishing operators use this skill to turn podcast episode data and Notion scripts into Substack-ready posts and LinkedIn companion copy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can publish public content or send email distribution without clear approval gates. <br>
Mitigation: Require explicit draft review and approval before Substack publishing, email distribution, or LinkedIn posting. <br>
Risk: The workflow needs access to Notion episode content. <br>
Mitigation: Use a least-privileged Notion token limited to the episode content intended for publication. <br>
Risk: The RSS helper may alter the Python environment by installing feedparser at runtime. <br>
Mitigation: Pre-install or remove the feedparser dependency in a controlled environment before use. <br>


## Reference(s): <br>
- [Substack Embed Playbook](references/substack-embed-playbook.md) <br>
- [LinkedIn Playbook](references/linkedin-playbook.md) <br>
- [The Canadian Real Estate Investor on Apple Podcasts](https://podcasts.apple.com/ca/podcast/the-canadian-real-estate-investor/id1634197127) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated text outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local JSON episode data and downloaded image files when the helper scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
