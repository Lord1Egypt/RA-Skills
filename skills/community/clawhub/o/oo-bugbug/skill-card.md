## Description:

Use the OOMOL-connected oo CLI to read BugBug suites, tests, profiles, and run history, and to run tests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA teams use this skill to inspect BugBug workspaces, retrieve test details and run history, and execute selected tests through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup executes downloaded code without verification or explicit installation approval.

Mitigation: Install a reviewed, pinned oo CLI yourself and require approval for host changes. Review its automatic skill synchronization; set OO_SKILLS_SYNC_DISABLED=1 to disable startup sync.

Risk: Running a BugBug test changes remote workspace state.

Mitigation: Review the requested test run and retain confirmation before executing it.

## Reference(s):

- [BugBug API documentation: running tests via API](https://docs.bugbug.io/running-tests/running-via-api)
- [BugBug](https://bugbug.io)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [BugBug skill on ClawHub](https://clawhub.ai/oomol/skills/oo-bugbug)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured JSON results with text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The returned records and status depend on the selected BugBug action.]

## Skill Version(s):

1.0.6 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
