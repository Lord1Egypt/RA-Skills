# keepachangelog

A Claude Code skill for creating and maintaining `CHANGELOG.md` files in
[Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) format. It
covers the full lifecycle: creating a changelog (with backfill from git
tags), recording notable changes into `[Unreleased]`, cutting a release
with a SemVer-inferred version, and auditing an existing changelog against
the format's rules.

## Installation

### Claude Code (plugin marketplace — recommended)

This plugin is distributed through the
[NanookAI/skills](https://github.com/NanookAI/skills) marketplace. Inside
Claude Code, run:

```
/plugin marketplace add NanookAI/skills
/plugin install keepachangelog@nanookai-skills
```

The skill is then available in every project, and `/plugin marketplace update`
picks up new versions.
