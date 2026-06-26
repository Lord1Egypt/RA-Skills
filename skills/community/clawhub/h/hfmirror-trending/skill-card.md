## Description: <br>
Fetches real-time Hugging Face trending data from the public HF-Mirror API and generates a structured Chinese Markdown report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ddongcui](https://clawhub.ai/user/ddongcui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and AI agents use this skill to answer questions about currently trending Hugging Face models, datasets, and Spaces by fetching HF-Mirror trend data and turning it into a readable Chinese report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts HF-Mirror to fetch public trending data. <br>
Mitigation: Run it only where outbound access to HF-Mirror is acceptable and treat the results as third-party trend data. <br>
Risk: The script can write a Markdown report to a local path. <br>
Mitigation: Use a controlled output path to avoid overwriting unintended files. <br>


## Reference(s): <br>
- [HF-Mirror Trending API](https://hf-mirror.com/api/trending) <br>
- [ClawHub skill page](https://clawhub.ai/ddongcui/hfmirror-trending) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Files] <br>
**Output Format:** [Chinese Markdown report with tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes the report to a caller-selected Markdown file when an output path is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
