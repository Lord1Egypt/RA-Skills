# Project policy contract

The Core is portable. Project-specific facts, vocabulary, voice, safety rules,
and review policy belong in the project, never in the Skill source.

## Discovery

`novelforgectl` treats `<project>/.novelforge/state/project.json` as the machine-readable
profile. Human guidance may live in the nearest `novel-project.md`. If multiple
policy files exist, the project must name the one to use; the Core does not
silently merge conflicting policies.

## Profile fields

```json
{
  "schema": 1,
  "name": "project-defined",
  "engine": "jin-yong",
  "engines": ["jin-yong"],
  "genre": "project-defined",
  "voice": {"person": "third", "distance": "close", "register": "project-defined"},
  "style_detectors": [],
  "policies": {
    "style_detector_mode": "warning",
    "blocking_rules": []
  }
}
```

`engine` is the active engine for the next Context Ticket. `engines` records
installed/approved engines. Unknown project fields are preserved for engine
predicates but do not change Core gates.

## Policy boundaries

- A project may add banned terms, required fields, detector patterns, or review
  checks.
- A detector is advisory unless its rule ID is explicitly listed in
  `blocking_rules`.
- A project may install and activate a new engine without changing Core code.
- A project cannot skip state transitions, weaken source-hash checks, or make a
  missing dependency implicit.
- No project profile can make the Core assume an author, work, genre, or voice
  for another project.

## Missing policy

If `novel-project.md` is absent, continue with the machine profile and report
that no human policy was found. Do not invent a genre, style, character, or
setting. If the machine profile is absent, `project init` must create it before
any chapter workflow starts.
