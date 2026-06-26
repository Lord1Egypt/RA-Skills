## Description: <br>
Repurpose a blog post, article, URL, file, or stdin text into X/Twitter threads, LinkedIn posts, Instagram captions, email snippets, and concise summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mariusfit](https://clawhub.ai/user/mariusfit) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Content creators, marketing teams, agencies, and solo entrepreneurs use this skill to turn articles, blog posts, or supplied text into platform-specific social media and newsletter copy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch user-supplied article URLs. <br>
Mitigation: Use trusted URLs and review fetched content before publishing generated posts. <br>
Risk: The skill can read selected text or markdown files and transform their contents. <br>
Mitigation: Do not point it at secrets or private files unless that content is intended for repurposing. <br>
Risk: Saving output can write files such as twitter.txt, linkedin.txt, instagram.txt, email.txt, and summary.txt in the selected output directory. <br>
Mitigation: Choose an output directory where those generated files are expected and acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mariusfit/oc-content-repurposer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text, JSON, or platform-specific text files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can generate Twitter/X threads, LinkedIn posts, Instagram captions, email snippets, and summaries; selected formats may be saved as separate .txt files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
