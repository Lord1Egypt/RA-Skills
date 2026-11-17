## Description:

Multi-lender mortgage rate comparison that scrapes lender websites and national benchmarks, ranks rates from lowest to highest, and tracks day-over-day changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seang1121](https://clawhub.ai/user/seang1121)

### License/Terms of Use:

MIT-0

## Use Case:

External users and automation operators use this skill to gather current mortgage rates for a configured ZIP code, compare lender and benchmark rates, and generate a plain text report for scheduled delivery or manual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts multiple lender and benchmark websites and may submit the configured ZIP code to those third-party sites.

Mitigation: Review the target sites before use, use only ZIP codes suitable for disclosure, and run the skill in an environment where outbound network access is expected.

Risk: Browser automation and local browser connection behavior can expose active browsing context or run against pages that change unexpectedly.

Mitigation: Inspect the script before installing, make browser and CDP access explicit opt-in for routine use, and avoid running it against sensitive browser sessions.

Risk: Dependency installation details are inconsistent between the Python requirement and the declared Node package installation.

Mitigation: Verify the required Patchright installation path and Chromium browser setup before scheduling or relying on recurring reports.

Risk: The skill stores local mortgage-rate history for trend comparison.

Mitigation: Review the generated data directory and delete or rotate history files when local retention is not desired.

## Reference(s):

- [Project homepage](https://github.com/seang1121/Multi-Lender-Mortgage-Rate-Lookup)
- [Freddie Mac PMMS history CSV](https://www.freddiemac.com/pmms/docs/PMMS_history.csv)
- [Mortgage News Daily mortgage rates](https://www.mortgagenewsdaily.com/mortgage-rates)
- [ClawHub skill page](https://clawhub.ai/seang1121/skills/mortgage-rate-lookup)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text report with setup and command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script writes a rolling local history file for day-over-day comparisons.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
