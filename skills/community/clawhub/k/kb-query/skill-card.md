## Description: <br>
Answers simple lookup and factual Q&A questions from Java-specified personal or team Research KB repositories with source-grounded citations for a desktop source list. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[myd2002](https://clawhub.ai/user/myd2002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge-base users use this skill to answer simple factual questions from one or two Java-selected personal or team Research KB repositories. It reads relevant Markdown pages from the selected repositories and returns answers with structured citations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Gitea credential for repository reads without enforcing its own repository allowlist. <br>
Mitigation: Install only when the Java backend tightly controls kbTargets and the Gitea credential is a read-only token scoped to intended KB repositories. <br>
Risk: Private or business-sensitive knowledge bases could be exposed if transport, repository scope, or dependencies are not controlled. <br>
Mitigation: Confirm repository allowlisting, HTTPS configuration, and pinned dependencies before using the skill with sensitive knowledge bases. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/myd2002/skills/kb-query) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, guidance] <br>
**Output Format:** [JSON object with answer text, citations, used scopes, read pages, and errors] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Citations must reference pages read during the task; insufficient evidence responses return empty citations and label general guidance as non-KB.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
