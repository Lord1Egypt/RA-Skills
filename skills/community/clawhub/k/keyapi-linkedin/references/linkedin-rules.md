# LinkedIn Rules

Use this file for platform-level routing boundaries, identifier discipline, and output expectations. Use module files for scenario-specific workflows.

## Entity Scope

people, companies, jobs, posts, comments, videos, images, experience, education, skills, certifications, publications, honors, recommendations, interests, followers, connections, and contact information

## Identifier Discipline

- Keep person profile identifiers, company identifiers, and job identifiers distinct.
- Use search people before profile section calls when the exact profile target is unknown.
- Fetch company profile before employees, posts, or jobs when the company identity is ambiguous.

## Scenario Module Routing

- Use `linkedin-user-rules.md` for people search, user profile/about/contact, career sections, social proof, posts, comments, media, and interests.
- Use `linkedin-company-rules.md` for company profile, employees, company posts, and company hiring footprint.
- Use `linkedin-jobs-rules.md` for company job counts, company jobs, and job detail.
- If a request spans multiple modules, load the smallest set of module files needed and confirm report scope before broad multi-endpoint execution.

## Documentation Hints

- Filter `https://docs.keyapi.ai/llms.txt` for links under `https://docs.keyapi.ai/en/linkedin/`.
- Treat endpoint titles as search hints, not stable tool names.
- Extract the current REST method and `/v1/...` path from the endpoint docs page before calling the API.
- Use examples from the docs page only after replacing sample identifiers with user-provided or resolved identifiers.

## Output Guidance

- For people reports, group facts by profile baseline, career background, content activity, and contact/social proof.
- For company reports, separate company profile, employee list, posts, and hiring data.
- For job reports, distinguish job count, listing summaries, and selected job detail.
- For reports, organize findings by entity, evidence, limitations, and recommended follow-up calls.
