# Support

## Where to go

| You want to | Go to |
|---|---|
| Report a broken script or module behaviour | [Bug report issue](https://github.com/JohnSmithfan/github-novel-serialization-skill/issues/new?template=bug-report.yml) |
| Propose a new module, script or capability | [Feature request issue](https://github.com/JohnSmithfan/github-novel-serialization-skill/issues/new?template=feature-request.yml) |
| Report a wrong or contradictory rule in the docs | [Errata issue](https://github.com/JohnSmithfan/github-novel-serialization-skill/issues/new?template=errata.yml) |
| Report missing or unclear documentation | [Docs issue](https://github.com/JohnSmithfan/github-novel-serialization-skill/issues/new?template=docs.yml) |
| Ask an open-ended question | [Discussions](https://github.com/JohnSmithfan/github-novel-serialization-skill/discussions) |
| Report a leaked credential | [SECURITY.md](SECURITY.md) — **never a public issue** |

**This repository is the Skill, not a novel.** Questions about a specific book —
its chapters, setting or characters — belong in that book's own repository.
Registered subprojects are listed in [SUBPROJECTS.md](SUBPROJECTS.md).

## Before you post

1. Search open **and** closed issues.
2. Check [references/subproject-playbook.md](references/subproject-playbook.md) — it
   records what field use actually settled on, and often differs from the generic
   contract in `SKILL.md`.

## Question template

```
Goal:
Tried:
Stuck at: (command + verbatim output, or file + line)
Expected:
```

## Scripts: the two things that trip everyone up

**Run them from the subproject root, not from here.** The scripts take the current
working directory as the project root. They live in this repository and are never
copied into a subproject.

**On Windows, always write text with `newline='\n'`.** `io.open(p, 'w', encoding='utf-8')`
converts LF back to CRLF on write, which silently rewrites an entire Markdown file's
line endings. `.gitattributes` cannot stop it. Details in [scripts/README.md](scripts/README.md).

Quick self-check:

```
python scripts/scan_hygiene.py --root . --fail-on crlf,junk,mojibake
python scripts/check_refs.py --root . --kind NONRELEASE --kind MISSING
```

## Response time

This is a community-maintained project with no fixed schedule. Bug reports on shared
scripts are usually answered within days; feature requests are batched into releases.
