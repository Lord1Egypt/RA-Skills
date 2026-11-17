## Description:

Your AI career companion. Scan your situation, map possible paths, simulate futures, and track progress week by week - with interactive charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hectormeta](https://clawhub.ai/user/hectormeta)

### License/Terms of Use:

MIT

## Use Case:

External users use Pacer to explore career transitions, startup paths, student career planning, and one-person-company decisions through a guided scan, path mapping, future simulation, and weekly progress tracking workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill collects and stores sensitive career, resume, financial-runway, and weekly progress information in local memory.

Mitigation: Use explicit memory opt-in, collect only necessary details, avoid secrets or unnecessary personal data in uploaded CVs, and provide clear deletion controls.

Risk: User-derived data is inserted into executable HTML chart templates.

Mitigation: Encode and validate chart values before rendering, and render generated chart HTML only in a sandboxed viewer or iframe.

Risk: Broad triggers and weekly heartbeat behavior may activate career tracking or memory updates when the user did not intend it.

Mitigation: Confirm activation before starting tracking, allow heartbeat pause or disable controls, and ask before updating persistent progress records.

Risk: Installation guidance references moving targets such as latest CLI installs and a repository URL without server-resolved provenance for this release.

Mitigation: Review the ClawHub release record and pin installation to the intended skill version before deployment.

## Reference(s):

- [Pacer Skill on ClawHub](https://clawhub.ai/hectormeta/skills/pacer)
- [hectormeta Publisher Profile](https://clawhub.ai/user/hectormeta)
- [Chart.js 4.4.0 CDN dependency](https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with generated HTML chart templates and local-memory tracking notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May parse uploaded PDF, DOCX, DOC, or TXT resumes up to 10 MB when supported by the host agent; uses weekly heartbeat and local memory for progress tracking.]

## Skill Version(s):

0.1.2 (source: frontmatter, skill.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
