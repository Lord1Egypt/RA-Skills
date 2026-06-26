## Description: <br>
Convert markdown articles to Zhihu (知乎) publishing format and one-click publish articles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejianjun000](https://clawhub.ai/user/xiejianjun000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, developers, and agents use this skill to convert Markdown articles into Zhihu-ready HTML previews or content-only HTML, then publish posts or save them as Zhihu drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores Zhihu login cookies and a browser profile that may grant account access. <br>
Mitigation: Use it only on a trusted single-user machine, and delete the saved cookie file and browser profile when finished. <br>
Risk: Publishing commands can create drafts or publish articles from the user's Zhihu account. <br>
Mitigation: Prefer draft mode first, review generated content in Zhihu, and publish only after confirming account, title, topics, and article body. <br>
Risk: The publishing workflow uses browser login and remote debugging, which increases session exposure if used on shared or untrusted systems. <br>
Mitigation: Close the dedicated browser session after use and avoid running the login or publish workflow on shared machines. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejianjun000/md-to-zhihu) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/xiejianjun000) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated HTML files or content-only HTML when scripts are run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports single-file and directory batch conversion or publishing; publish mode can create drafts or publish to Zhihu using saved cookies.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
