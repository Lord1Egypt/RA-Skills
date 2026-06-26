## Description: <br>
Full podcast post-production pipeline that turns a transcript or episode URL into show notes, chapter markers, social media clips, SEO metadata, and a newsletter summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ash2hsa](https://clawhub.ai/user/ash2hsa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Podcasters, editors, marketers, and agent users use this skill to convert a transcript or public episode URL into publishing-ready podcast assets. It is intended for post-production workflows that need show notes, chapters, social posts, SEO fields, and newsletter copy from the same source material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Episode URLs may be fetched over the network and could expose private, internal, paywalled, or confidential content if supplied. <br>
Mitigation: Use pasted transcripts or public episode URLs, and avoid private company links, localhost or internal URLs, paywalled content, and confidential transcripts unless that processing is approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ash2hsa/podcast-workflow) <br>
- [Podcast Workflow README](artifact/README.md) <br>
- [Example output](artifact/example-output.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with structured text sections, timestamp lists, and plain-text social posts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use curl to fetch public episode pages when a URL is provided; no API keys are required.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
