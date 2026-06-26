## Description: <br>
Turn HiHired (hihired.org) into a resume copilot workflow for building, importing, rewriting, tailoring, or improving resumes, generating matching cover letters, extracting resume data from pasted text, and guiding users into the HiHired builder with the right next steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flychicken123](https://clawhub.ai/user/flychicken123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill for resume and cover letter workflows: drafting resumes from scratch, importing or parsing existing resumes, improving bullets and summaries, tailoring content to job descriptions, and deciding when to continue in the HiHired builder. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The API helper can send sensitive resume and job data to an unencrypted raw backend IP. <br>
Mitigation: Use chat-only drafting or the public HiHired website when users do not want agent-side uploads; prefer a verified HTTPS endpoint and get explicit approval before each upload. <br>
Risk: Resume parsing and generation workflows may process personal, employment, education, and job-search data. <br>
Mitigation: Collect only the data needed for the requested resume task, avoid uploading real resumes unless the user understands where the data is sent, and fall back to local drafting when API calls fail or are not approved. <br>


## Reference(s): <br>
- [HiHired capabilities reference](references/hihired-capabilities.md) <br>
- [HiHired builder](https://hihired.org/builder) <br>
- [HiHired templates](https://hihired.org/templates) <br>
- [HiHired AI resume builder with cover letter guide](https://hihired.org/guides/ai-resume-builder-with-cover-letter) <br>
- [ClawHub release page](https://clawhub.ai/flychicken123/hihired-resume) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown text with optional inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can draft resume sections, cover letters, skills lists, handoff checklists, and API-backed responses when the helper script is explicitly used.] <br>

## Skill Version(s): <br>
0.1.1 (source: release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
