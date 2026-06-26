## Description: <br>
Search, browse, and rediscover your Kindle highlights <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gofordylan](https://clawhub.ai/user/gofordylan) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users use Hi Lite to import Kindle highlights, store them locally as Markdown, search and browse their personal highlight library, and curate themed collections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Amazon fetch mode stores reusable authenticated Amazon browser session data locally. <br>
Mitigation: Use /hi-lite fetch only on a trusted machine and remove ~/.openclaw/workspace/hi-lite/.browser-data/ when the retained session is no longer needed. <br>
Risk: The Amazon fetch mode opens Amazon and may require manual sign-in before extracting Kindle notebook data. <br>
Mitigation: Prefer manual import and local search for lower-risk use; review the fetch flow before using it with an Amazon account. <br>


## Reference(s): <br>
- [ClawHub Hi Lite release page](https://clawhub.ai/gofordylan/hi-lite) <br>
- [OpenClaw](https://openclaw.org) <br>
- [Amazon Read Notebook](https://read.amazon.com/notebook) <br>
- [Bookcision](https://readwise.io/bookcision) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown responses, local Markdown files, JSON import files, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates files under ~/.openclaw/workspace/hi-lite/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
