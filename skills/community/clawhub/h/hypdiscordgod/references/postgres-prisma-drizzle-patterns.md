# Postgres, Prisma, and Drizzle Patterns

Use this reference when a Discord bot project is outgrowing SQLite or needs stronger relational modeling.

## When to Move to Postgres

Choose Postgres when:
- multiple services read/write shared state
- dashboard, API, workers, and bot all need the same database
- migrations and schema discipline matter
- query complexity is increasing

## ORM Selection

- Use Prisma when the project values schema-driven DX and generated client ergonomics.
- Use Drizzle when the project prefers SQL-like control, lightweight tooling, and explicit query composition.
- Follow the existing repo if one ORM already exists.

## Safe Rules

- keep migrations versioned
- index guild/user/channel identifiers
- store Discord snowflakes as strings
- separate config, operational records, and audit logs when useful
