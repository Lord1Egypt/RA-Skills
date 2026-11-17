# Meeting Scribe

Turns a meeting transcript into structured meeting memory: a dated meeting note, one appended mention
line per entity the transcript actually names, and a recap email drafted for review but never sent.
Files-first, no platform account, no connector required. MIT licensed.

- **Live directory:** https://skillsandagents.co
- **Catalog page:** https://skillsandagents.co/skills/meeting-scribe/
- **License:** [MIT](../LICENSE)

## Credit

Inspired by [USV's Meeting Scribe agent](https://blog.usv.com/meet-the-agents). USV built theirs for
VC deal logs — matching meeting mentions against portfolio companies, founders, and co-investors, and
drafting a recap. This is our own generic version, built independently: it does not reuse USV's code,
prompts, or internal schema, and it drops the VC-specific "themes" table in favor of a general-purpose
entity match against any folder of people/organizations/meetings you already keep.

## What this is

Point the skill at a transcript and a folder of entity files (people, organizations, other meetings).
It reads the transcript, matches every name it finds against your entity files first — never guessing
from context alone — and produces:

1. **A meeting note** with a recap, every matched mention (quote-grounded), any unmatched names as
   proposed new entities, any ambiguous names flagged with all their candidates, and follow-ups with
   owners where stated.
2. **One appended mention line per matched entity file** — date, quote, link back to the meeting note.
   Existing entity files are never rewritten, only appended to.
3. **A recap email, drafted only.** This skill has no mail-sending step. The email is always output
   for a human to copy, edit, and send.

## Worked examples

### VC deal log (the USV source case)

Transcript: a portfolio check-in call. Entity folder: `people/` has the founders you track,
`organizations/` has the portfolio companies and co-investors. The transcript mentions the founder (an
exact match — one mention line appended to their file), a co-investor firm by a nickname (an alias
match, if you've listed it), and a new engineering hire who isn't in your files yet (a proposed new
entity, not written until you confirm). The meeting note ends with follow-ups like "send the updated
cap table" with an owner, and a recap email drafted for the deal team.

### Sales example

Transcript: a discovery call. Entity folder: `people/` has your contacts at target accounts,
`organizations/` has the accounts themselves. The transcript mentions the buyer (exact match), their
company (exact match), and a competitor's product name that happens to share a word with one of your
own tracked accounts (an ambiguity flag — the skill lists both candidates and writes no mention line
rather than guessing). The meeting note's follow-ups list "send pricing" with the rep as owner, and the
recap email drafts a next-steps note for the buyer, ready for the rep to review before sending.

## Entity folder convention

```
<entity-folder>/
  people/           # type: person
  organizations/    # type: organization
  meetings/         # type: meeting
```

Each entity is a markdown file with YAML frontmatter: `type`, `name`, `as_of`, and an optional
`aliases` list used for matching. See `references/sample-entities/` for a working example.

This matches the taxonomy used by the internal "business brain" version of this idea
(`person` / `organization` / `meeting`), so a future platform version of this skill can consume the
same entity files without a schema migration.

## Layout

```
meeting-scribe/
├── SKILL.md                          # The skill
├── references/
│   ├── mention-proposal.md           # JSON shape for one proposed mention (portability contract)
│   ├── sample-transcript.md          # Frozen sample transcript for the eval self-tests
│   └── sample-entities/              # 2 people + 2 organizations, matches the self-tests
└── README.md
```

## Try it

Run the skill by hand against `references/sample-transcript.md` and
`references/sample-entities/`. The self-tests in `SKILL.md`'s Eval Contract describe exactly what the
output should contain: one unmatched name (proposed new entity, no file written), one ambiguous name
(two candidates listed, no mention line written), and matched names each getting one appended, quoted,
dated mention line.

## Usage

Add `SKILL.md` to your Claude project context, point it at your own transcript and entity folder, and
run it after any meeting. For the team's standard circulate-ready notes format instead (with
carry-forward of open action items), see [`meeting-memo`](../meeting-memo/).
