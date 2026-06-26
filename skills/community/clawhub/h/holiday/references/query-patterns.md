# Holiday Query Patterns

Use this reference when a holiday question is underspecified or when you need a repeatable lookup pattern.

## Fast Triage

Classify the question first:

1. date to holiday status
2. holiday name to date
3. observed day or substitute day
4. closure impact on banks, schools, markets, or offices
5. regional scope dispute

## Minimal Clarifying Questions

Use short questions only when needed:

- Which country or region do you mean?
- Which year should I use?
- Do you mean an official public holiday, a bank holiday, or a school break?
- Is this nationwide or for a specific state or city?

## Search Patterns

Adapt these patterns to the jurisdiction and year.

### Public Holiday Date

- `<country> public holidays <year> site:gov`
- `<country> official holiday calendar <year>`
- `<holiday name> <country> <year> official`

### Regional Holiday

- `<state/province> public holidays <year> site:gov`
- `<city> holiday calendar <year> official`

### Observed or Substitute Day

- `<country> observed holidays <year> official`
- `<holiday name> observed <country> <year>`
- `<country> substitute holiday rules official`

### Bank or School Closure

- `<country> central bank holiday calendar <year>`
- `<state> school calendar <year> official`
- `<exchange name> holiday calendar <year>`

## Answer Templates

## Specific Date

`<date>` is `<status>` in `<jurisdiction>` for `<year>`.

- Holiday: `<holiday name>`
- Scope: `<nationwide/regional/institution-specific>`
- Note: `<observed-day detail or source caveat>`

## Holiday Date

In `<jurisdiction>`, `<holiday name>` falls on `<date>` in `<year>`.

- Status: `<official/observed/regional>`
- Note: `<substitute day or scope detail>`

## Institution Closure

`<institution>` is `<closed/open/not uniformly closed>` on `<date>` in `<jurisdiction>`.

- Public holiday status: `<status>`
- Institution rule: `<official basis>`

## Common Failure Modes

- The holiday exists culturally but is not a legal holiday.
- The holiday is official only in part of the country.
- The named holiday date differs from the observed closure date.
- Schools, banks, and markets follow separate calendars.
- The official calendar for the requested year is not yet published.

## Escalation Rule

If two authoritative sources disagree:

- prefer the most specific official source for the institution or region in question
- call out the disagreement explicitly
- avoid flattening conflicting rules into one answer
