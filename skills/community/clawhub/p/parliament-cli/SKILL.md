---
name: parliament-cli
description: UK Parliament CLI — search bills, divisions, members, and written questions from official UK Parliament APIs, with stable JSON envelopes for agents. Use when looking up UK Parliament bills, members, votes/divisions, written questions, or when an agent needs structured Parliament API results.
homepage: https://www.parliment-cli.xyz
metadata:
  {
    "openclaw":
      {
        "emoji": "🏛️",
        "requires": { "bins": ["parliament"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "node",
              "package": "@shan8851/parliament-cli",
              "bins": ["parliament"],
              "label": "Install parliament-cli (npm)",
            },
          ],
      },
  }
---

# parliament-cli

Use `parliament` for UK Parliament data: bills, members, divisions/votes, and written questions.

Setup

- `npm install -g @shan8851/parliament-cli`
- No API key or auth required

Bills

- By id: `parliament bill 3973`
- By title: `parliament bill "renters rights"`
- Search: `parliament search bills "energy"`

Divisions and Votes

- Search divisions: `parliament divisions "budget"`
- Lookup by id: `parliament divisions 2211`
- Alias: `parliament votes 2211`

Members

- By name: `parliament member "Keir Starmer"`
- By id: `parliament member 4514`

Written Questions

- Search: `parliament questions "transport"`
- Lookup by id or UIN query: `parliament questions 902178`

Output

- Defaults to text in a TTY and JSON when piped
- Force JSON: `parliament bill 3973 --json`
- Success envelope: `{ ok, schemaVersion, command, requestedAt, data }`
- Error envelope: `{ ok, schemaVersion, command, requestedAt, error }`

Agent Notes

- Ambiguous text queries return `AMBIGUOUS_QUERY` with candidate hints in `error.details`
- No auth setup needed, so agents can use it immediately
- Exit codes are explicit and errors stay structured in JSON mode

Notes

- Official sources include the Bills, Members, Written Questions, and Commons Votes APIs
- `votes` is an alias of `divisions`
