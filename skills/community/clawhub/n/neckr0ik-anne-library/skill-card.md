## Description: <br>
Automates DOI lookup and academic-library download workflows for books and articles using titles, DOIs, URLs, or reading lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neckr0ik](https://clawhub.ai/user/neckr0ik) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, researchers, and academic support agents use this skill to look up DOIs, process reading lists, and prepare library download attempts for scholarly books and articles. Users should only provide credentials and access content when they are authorized to do so. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to configure institutional library credentials. <br>
Mitigation: Use only credentials you are authorized to use, avoid sharing them with untrusted runtimes, and review the publisher's credential-handling behavior before installation. <br>
Risk: The advertised automation is incomplete and may still require manual download steps. <br>
Mitigation: Treat results as assistance rather than guaranteed downloads, review any suggested source or file manually, and keep organization access-policy checks in the workflow. <br>
Risk: External DOI lookup and library requests can reveal research interests. <br>
Mitigation: Run the skill only in environments where those queries are acceptable and avoid submitting sensitive reading lists unless disclosure risk has been reviewed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and text or JSON status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require Playwright, Python dependencies, institutional library configuration, and network access to DOI and library services.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and claw.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
