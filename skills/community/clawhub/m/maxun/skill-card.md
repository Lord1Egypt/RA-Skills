## Description:

List and run Maxun web scraping robots. Use when asked to list robots, run a robot, scrape a website, or get robot results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rohitr311](https://clawhub.ai/user/rohitr311)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to list Maxun robots, start scraping runs, inspect robot details, review run history, retrieve run results, and abort in-progress runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad local execution authority for commands that list, run, inspect, retrieve, and abort Maxun robot runs.

Mitigation: Review the skill before installing, use a narrowly scoped execution policy, and keep approval prompts enabled for run and abort actions.

Risk: The helper script can load environment variables from a local .env file and can send the Maxun API key to the configured MAXUN_BASE_URL.

Mitigation: Avoid running the skill from directories containing untrusted .env files, and only set MAXUN_BASE_URL to a trusted Maxun endpoint or self-hosted instance.

## Reference(s):

- [Maxun homepage](https://www.maxun.dev)
- [Maxun app](https://app.maxun.dev)
- [ClawHub skill page](https://clawhub.ai/rohitr311/skills/maxun)

## Skill Output:

**Output Type(s):** [text, shell commands, API calls, configuration, guidance]

**Output Format:** [Markdown with shell command examples and text or JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MAXUN_API_KEY, bash, curl, and python3; can target a self-hosted Maxun instance with MAXUN_BASE_URL.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact metadata says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
