# Hardcover Bookshelf Skill

Talk to your **Hardcover** bookshelf in natural language.

This OpenClaw skill lets you do things like:
- mark a book as started
- mark a book as finished
- see what's on your **Want to Read** shelf
- count how many books you read last year

Under the hood, the skill uses the **Hardcover GraphQL API** and a small bundled TypeScript client so the logic is reusable, testable, and easier to extend.

## What this skill supports

Example prompts:
- `what's on my reading list`
- `i started reading the complete maus`
- `i finished reading dune`
- `how many books did i read last year`

Current supported flows:
- **Reading list** → maps to **Want to Read**
- **Start reading** → marks a title as **Currently Reading**
- **Finish reading** → marks a title as **Read**
- **Yearly stats** → counts books finished last calendar year

## Required setup

This skill requires:

- `HARDCOVER_TOKEN`

### Token format

Use the token exactly as shown on Hardcover's API settings page, including the `Bearer ` prefix.

Example:

```bash
export HARDCOVER_TOKEN='Bearer eyJ...'
```

Get it from:
- <https://hardcover.app/account/api>

If the token is missing or malformed, the client will fail fast with a helpful error.

## Installation

### From a packaged `.skill` file

Install the packaged artifact with your normal OpenClaw skill install flow.

### From source

Clone this repo into your skills directory or copy the folder into:

```bash
~/.agents/skills/hardcover-bookshelf
```

Then install dependencies:

```bash
npm install
```

## Repository layout

```text
.
├── SKILL.md
├── README.md
├── LICENSE.md
├── package.json
├── tsconfig.json
├── src/
│   ├── cli.ts
│   ├── client.ts
│   ├── client.test.ts
│   └── types.ts
└── references/
    ├── graphql-patterns.md
    └── schema-quirks.md
```

## Commands

```bash
npx tsx src/cli.ts list [--limit 20] [--json]
npx tsx src/cli.ts start --title "The Complete Maus" [--json]
npx tsx src/cli.ts finish --title "The Complete Maus" [--json]
npx tsx src/cli.ts count-last-year [--json]
```

These commands call the local TypeScript client and keep auth, status handling, and schema quirks in one place.

## Behavior notes

### Reading list
- Uses **Want to Read** (`status_id=1`)

### Start reading
- Checks currently-reading entries first
- Falls back to Hardcover search
- Avoids creating duplicates if the book is already marked as currently reading

### Finish reading
- Prefers an existing currently-reading entry for the book
- Otherwise updates the most recent existing `user_book` entry
- Uses `last_read_date` as the finish-date field

### Count last year
- Counts books with status **Read** (`status_id=3`)
- Uses `last_read_date` in the previous calendar year

## Caveats

- Hardcover's GraphQL schema has a few quirks; see `references/schema-quirks.md`.
- `finish` is currently a **best-effort** implementation based on the live schema tested so far.
- If Hardcover changes field names or exposes a better canonical finish-date field later, the client should be updated accordingly.

## Development

Install dependencies:

```bash
npm install
```

Run commands:

```bash
npx tsx src/cli.ts list --limit 5
npx tsx src/cli.ts start --title "The Complete Maus"
npx tsx src/cli.ts finish --title "The Complete Maus"
npx tsx src/cli.ts count-last-year
```

Run tests:

```bash
npm test
```

## License

MIT-0
