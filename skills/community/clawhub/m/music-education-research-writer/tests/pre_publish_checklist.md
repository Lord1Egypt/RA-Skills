# Pre-Publish Checklist

Use this checklist before uploading the package to SkillHub or ClawHub.

## Package identity

- Folder name is exactly `music-education-research-writer`
- `SKILL.md` exists in the root
- `SKILL.md` frontmatter contains only `name` and `description`
- `name` is exactly `music-education-research-writer`
- `description` clearly explains when to use the skill

## Content integrity

- `SKILL.md` contains all required sections
- `SKILL.md` contains `Token Efficiency Protocol`
- references files are complete
- templates files are complete
- example files are complete
- test files are complete
- no placeholder TODO text remains

## Academic integrity

- no fabricated authors
- no fabricated years
- no fabricated journals
- no fabricated DOI values
- no fabricated policy documents
- no paragraphs that hide weak evidence with vague academic language
- evidence classes `A` to `E` are clearly described
- `需要补充的文献清单` is supported for low-evidence cases
- large-corpus scenarios are handled by screening before deep analysis

## Safety

- no symlinks exist in the package
- no remote download logic exists
- no hidden credential-reading logic exists
- no automatic shell execution logic exists
- no full-disk scanning logic exists
- no automatic upload logic exists
- no token-wasting default behavior is implied by the examples or templates

## Packaging

- `python3 scripts/validate_skill.py .` passes
- `python3 scripts/package_skill.py . --format zip` passes
- `python3 scripts/package_skill.py . --format skill` passes
- `dist/music-education-research-writer.zip` exists
- `dist/music-education-research-writer.skill` exists
- opening either archive shows the root directory `music-education-research-writer/`

## Hub submission

- README is readable by humans
- SKILL description is short enough for hub listings
- examples are realistic
- token-efficiency behavior is visible in SKILL, README, examples, and tests
- package does not overclaim APIs or integrations
- upload notes state that the skill relies on user-provided corpora
