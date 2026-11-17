## Description:

AirnodeHub movie skill to choose picks by genre, year, mood, runtime, and ratings using attested MoviesDatabase and non-commercial OMDb data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metobom](https://clawhub.ai/user/metobom)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to narrow movie-night choices by genre, mood, year, runtime, audience constraints, exclusions, and sourced ratings. The agent returns one best pick and up to two alternatives with concise caveats and attribution-sensitive source handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may contact movie-data services, including paid, credentialed, or newly authorized API operations.

Mitigation: Review the requested service, scope, and cost before approving those calls.

Risk: OMDb data is limited to personal or clearly non-commercial use and requires attribution when facts are passed on.

Mitigation: Use OMDb only in permitted contexts, attribute OMDb facts, and skip OMDb for commercial requests.

Risk: Movie metadata, ratings, suitability, or availability can be missing or unsupported by the documented APIs.

Mitigation: Do not guess missing facts; omit unsupported fields or label any fallback suggestions as unsourced.

## Reference(s):

- [MoviesDatabase documentation](https://airnode-moviesdatabase.fly.dev/)
- [OMDb documentation](https://airnode-omdb.fly.dev/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown recommendation summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes sourced movie identity, runtime, named rating sources, one caveat, and clear fallback language when data is unavailable.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
