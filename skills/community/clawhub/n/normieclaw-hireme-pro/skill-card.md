## Description: <br>
HireMe Pro helps users build ATS-friendly resumes, tailor resumes and cover letters to job postings, prepare for interviews, track applications, and generate resume PDFs from local templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers use this agent skill to convert career history and target job postings into resumes, cover letters, interview-prep notes, match reports, application tracking records, and locally rendered resume PDFs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated resumes and cover letters may include overstated or unverified claims, especially metrics, tools, budgets, or achievements introduced during tailoring. <br>
Mitigation: Review every generated artifact against the user's actual experience before use, and require confirmation for any new quantified claim. <br>
Risk: The skill stores sensitive career and contact data locally under the skill data directory. <br>
Mitigation: Install only on trusted devices, use encrypted local storage where possible, and avoid syncing or sharing the data directory. <br>
Risk: The optional dashboard kit handles sensitive career data and the security evidence says its safeguards are under-scoped. <br>
Mitigation: Do not deploy the dashboard kit as written; add complete RLS policies, scoped authorization, and strong confirmation flows for export and deletion before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nollio/normieclaw-hireme-pro) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Security audit report](artifact/SECURITY.md) <br>
- [Dashboard kit specification](artifact/dashboard-kit/DASHBOARD-SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON data files, HTML templates, shell-command guidance, and locally generated PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Resume PDFs are rendered locally from HTML templates using the bundled shell script and Playwright.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
