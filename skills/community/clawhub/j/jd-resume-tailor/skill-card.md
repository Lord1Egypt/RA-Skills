## Description: <br>
Generates job-specific tailored resumes from a base profile and target job description, producing print-optimized HTML and PDF-ready output in Chinese or English. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[26048608982lp-ai](https://clawhub.ai/user/26048608982lp-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers and career-support agents use this skill to collect resume profile details, compare them against a job description, and generate a tailored resume with match analysis and review guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow stores personal resume data in a local resume-profile.md file. <br>
Mitigation: Keep the workspace private, review the saved profile for sensitive details, and delete it when it is no longer needed. <br>
Risk: Using a job-description URL can expose browsing context or fetch a page the user did not intend to share. <br>
Mitigation: Prefer pasted job descriptions or local files for privacy-sensitive applications. <br>
Risk: Tailored resume content may contain formatting issues, inaccurate dates, or overstated achievements. <br>
Mitigation: Review the generated HTML/PDF before sending and verify contact information, dates, names, and claims. <br>


## Reference(s): <br>
- [HTML Resume Template Guide](references/html-template-guide.md) <br>
- [ClawHub release page](https://clawhub.ai/26048608982lp-ai/jd-resume-tailor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown workflow guidance, self-contained HTML resume code, browser PDF export commands, and generated resume files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a local resume-profile.md and resume HTML/PDF files under the workspace; prompts the user to confirm job-description parsing and tailoring strategy before generation.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
