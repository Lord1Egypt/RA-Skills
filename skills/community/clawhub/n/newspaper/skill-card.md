## Description:

NewsPaper helps agents render structured news articles into styled, responsive HTML newspaper pages with optional ComfyUI-generated imagery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spootmu](https://clawhub.ai/user/spootmu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use NewsPaper to turn collected or generated news, reports, announcements, or narrative content into a shareable newspaper-style HTML page. It is useful when an agent needs to package multiple articles with a masthead, responsive newspaper layout, and at most one optional ComfyUI-generated image.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The service exposes an unauthenticated local web server.

Mitigation: Bind the service explicitly to 127.0.0.1 and add authentication or firewalling before any shared use.

Risk: Image generation and generation parameters may be reachable by untrusted callers.

Mitigation: Disable or tightly limit ComfyUI generation for untrusted callers and constrain timeout, polling, width, and height values.

Risk: Generated output files and logs can create persistent records of prompts, titles, article counts, and rendered content.

Mitigation: Avoid sensitive article text or prompts and manage generated output files and logs as persistent data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spootmu/skills/newspaper)
- [Skill usage guide](artifact/SKILL.md)
- [Agent API guide](artifact/AGENT.md)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [HTML files, JSON API responses, guidance]

**Output Format:** [JSON response containing a local URL to a generated HTML5 newspaper page]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can optionally include ComfyUI image status; rendered HTML is persisted under the service output directory.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
