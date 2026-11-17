## Description:

Extract a HackerNews post, including the linked article and comments, into a single clean Markdown document for quick reading or LLM input.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoqiao](https://clawhub.ai/user/guoqiao)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to turn a Hacker News item into a single Markdown document containing the linked article, metadata, and threaded comments for reading or downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch URLs supplied by Hacker News item data, including potentially internal or private addresses.

Mitigation: Run with network egress controls and avoid untrusted JSON inputs in sensitive environments.

Risk: The skill downloads third-party web content and installs Python dependencies through uv when executed.

Mitigation: Review and pin dependencies where required, and run the skill in an environment appropriate for outbound web requests.

Risk: Verbose output can save fetched HTML, extracted text, and item JSON to disk.

Mitigation: Choose output locations deliberately and avoid verbose mode when extracted content should not persist beyond the Markdown result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guoqiao/skills/hn-extract)
- [Skill homepage](https://github.com/guoqiao/skills/blob/main/hn-extract/hn-extract/SKILL.md)
- [Examples](https://github.com/guoqiao/skills/blob/main/hn-extract/examples)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands]

**Output Format:** [Markdown document saved to a file or printed to stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include title, author, source URL, points, Hacker News URL, comment count, extracted article text, and threaded comments.]

## Skill Version(s):

0.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
