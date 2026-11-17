---
name: log-line-pattern-miner
description: >
  Cluster pasted log lines by template, count frequencies, and highlight the
  noisiest error signatures. Use when triage needs signal from a log dump.
metadata: {"clawdbot":{"emoji":"📜","requires":{"bins":[]}}}
---

# Log Line Pattern Miner

## Purpose / Overview
Normalize variable tokens in pasted logs so repeated templates and rare
exceptions become visible.

## When to Use
- Incident triage with a noisy paste
- Comparing before/after snippets
- Finding a real error under retry spam

## Usage / Instructions
1. Ask for a log paste or excerpt. Do not request production credentials.
2. Normalize each line:
   - timestamps → `<TS>`
   - UUIDs / long hex IDs → `<ID>`
   - IPv4/IPv6 → `<IP>`
   - filesystem paths → `<PATH>`
   - obvious quantities → `<N>` when helpful
3. Group identical normalized templates and count them.
4. Present ranked rows: count, severity guess, template, one raw example.
5. Highlight the top three templates and whether they look causal or
   symptomatic (retries vs root exception).
6. Collapse indented stack-trace continuations into the parent error when
   possible.
7. Suggest 2–4 follow-up questions (service, deploy time, correlated metric).
8. Optionally propose a greppable regex for the hottest error template.
9. If secrets appear, warn and do not repeat them in examples.
10. Lead with a short summary, then the ranked template list.
11. Keep answers structured with short headings so the user can skim.
12. If information is missing, ask at most two clarifying questions before guessing.
13. Prefer concrete commands or checklists the user can copy.
14. Call out assumptions explicitly when the environment is unknown.
15. Refuse to invent tool output you did not see; ask for a fresh paste instead.
16. When offering optional follow-ups, keep them clearly optional.
17. Stay within this skill's scope; suggest a different task type if the request drifts.
18. End with a brief "done when" criterion so the user knows success.


## Examples
200 timeout lines + one `NullPointerException`
→ timeouts dominate counts; NPE flagged as likely root signal.

## Requirements / Dependencies
None. Pure text analysis on the paste.

## Limitations / Caveats
Heuristic normalization can over-merge. Multi-line JSON logs may need field
extracts from the user.

## Security / Permissions
Do not persist logs outside the conversation. Redact secrets in echoes.

## Description

Cluster pasted log lines by template, count frequencies, and highlight the noisiest error signatures.

## License or terms

Research

## Use case

Use when you are the operator responsible for tasks described as: Cluster pasted log lines by template, count frequencies, and highlight the noisiest error signatures.

## Risks and mitigations

## References

- Regular Expressions.info: https://www.regular-expressions.info/

## Ethical considerations

Illegal use is forbidden. Any application that leads to breaches of country or international law is not acceptable. The publisher will not be accountable for illegal use. Do not employ this skill for cyber-attacks, credential theft, or evasion of lawful investigations. Specifically, using this skill to steal credentials, install covert monitoring, mine cryptocurrency without authorization, or open unauthorized remote shells is illegal and forbidden.
