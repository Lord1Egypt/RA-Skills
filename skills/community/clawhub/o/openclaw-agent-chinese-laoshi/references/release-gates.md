# Release Gates

Use this reference before any public GitHub or ClawHub publication step.

## Public surface rule

ClawHub is public. Published skills and their `SKILL.md` content are visible to
everyone.

Source:
- https://docs.openclaw.ai/tools/clawhub

## The bundle must fail closed on

- placeholder text such as `TODO`, `TBD`, `replace me`, or sample URLs
- absolute local paths from macOS, Linux, or Windows home directories
- loopback or debugging endpoints such as `localhost`, `127.0.0.1`, `ws://`,
  `wss://`, or `devtools/browser`
- secret-shaped strings such as API keys, GitHub personal access tokens, or
  inline passwords
- known Drive file IDs copied from the project manifests
- drift between the public skill copy and the bundled plugin copy
- missing or incomplete `references/course-data` in either skill copy
- missing or drifted public system prompts in `prompts/system` or
  `references/system-prompts`
- vague fallback authority when audited repository commands are missing
- public-skill Drive, transcription, or vision lanes that ask for secrets,
  browser sessions, or cloud auth
- public-skill repository command execution without explicit command
  confirmation

## Gate Handling

- Run the checked-out repository's documented publication gate before release.
- Do not publish if the gate fails or if no audited publication gate is
  documented for the public bundle.
- Do not publish if the standalone public skill and plugin skill carry different
  course data files or byte-different course data.
- Do not publish if the public repo prompt pack and the skill prompt mirrors
  carry different file lists or byte-different prompt files.
