# OpenClaw skill: omem-memory

Trustworthy, self-hosted memory for an OpenClaw agent, backed by OMEM
(open source, MIT): beliefs with provenance, contradictions kept instead of
overwritten, a branchable belief state, and a why() audit trail.

Install (once published to ClawHub):

```
clawhub install omem-memory
```

Or copy this directory into `~/.openclaw/skills/` or `<workspace>/skills/`.

The skill is one SKILL file plus one stdlib-only Python script whose only
network calls go to the OMEM server you configure. Setup and usage are in
skill.md. Server: `pip install omem-infrastructure && omem-server`.

Publishing (maintainer): `npm i -g clawhub`, then from this directory
`clawhub skill publish . --slug omem-memory --name "OMEM memory" --version 0.1.0`.
