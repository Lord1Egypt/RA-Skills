## Description: <br>
Recommend suitable high-impact factor or domain-specific journals for manuscript submission based on abstract content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Researchers, manuscript authors, and research-support agents use this skill to rank candidate journals for a paper abstract by field fit, scope alignment, impact-factor constraints, and output format needs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan marks the skill suspicious because its file-handling scope is broader than the stated purpose and the documentation may overstate path safety. <br>
Mitigation: Only provide abstract files that are intended for journal matching, avoid untrusted file paths, and review the file path before running with --file. <br>
Risk: The skill can read local files explicitly passed as abstract input and may write output in the current workspace. <br>
Mitigation: Run it in a controlled workspace, avoid passing sensitive manuscripts unless appropriate, and check the destination before sharing generated outputs. <br>


## Reference(s): <br>
- [Journal Matchmaker ClawHub listing](https://clawhub.ai/AIPOCH-AI/journal-matchmaker) <br>
- [fields.json](references/fields.json) <br>
- [journals.json](references/journals.json) <br>
- [scoring_weights.json](references/scoring_weights.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, guidance] <br>
**Output Format:** [Console table, JSON, or Markdown recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes ranked journals with impact factor, open-access status, relevance score, and match reasons.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
