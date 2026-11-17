## Description:

Searches Longgang 325802 job postings by preference, collects listing and contact details, saves the results, and emails them to a configured recipient.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ttzuozhe](https://clawhub.ai/user/ttzuozhe)

### License/Terms of Use:


## Use Case:

External job seekers and agents assisting them use this skill to search Longgang-area job postings on the 325802 recruitment site, filter listings by job preference, and collect contact details for follow-up.

### Deployment Geography for Use:

Global; job-search content is specific to Longgang, Zhejiang, China.

## Known Risks and Mitigations:

Risk: The skill can automatically email scraped job results to a hardcoded default mailbox using exposed SMTP credentials.

Mitigation: Remove hardcoded SMTP credentials, require secrets from a protected configuration source, and require an explicit recipient plus confirmation before sending email.

Risk: The skill scrapes recruitment listings and writes collected job and contact details to jobs_result.txt.

Mitigation: Review collected results before sharing, respect the recruitment site's access expectations, and limit stored output to job-search data needed by the user.

Risk: The security guidance says dependencies should be updated.

Mitigation: Update dependencies before installation and rerun the release security scan.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ttzuozhe/skills/longgang-job-hunter)
- [325802 talent recruitment site](http://www.325802.net/ucregs/indexlist.asp)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration guidance]

**Output Format:** [Plain text job listings saved to jobs_result.txt and sent as email body text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results include company name, position, address, phone, work experience, education requirement, and optional job description.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
