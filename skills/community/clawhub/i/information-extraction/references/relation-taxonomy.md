# Relation Taxonomy

Use controlled predicates whenever possible.

## Core predicates

- `is_a`
- `part_of`
- `has_attribute`
- `located_in`
- `occurs_at`
- `belongs_to`
- `works_for`
- `created`
- `published`
- `participated_in`
- `caused`
- `used_for`
- `owns`
- `mentions`
- `related_to`

## Guidelines

### Prefer stable predicates

Choose one predicate form and reuse it across records.

Good:
- `published`
- `located_in`
- `works_for`

Avoid mixing:
- `publish`
- `published_by`
- `was_published`

### Use `related_to` as a fallback

If the relation is real but the exact predicate is not stable, use `related_to` and preserve evidence.

### Keep direction consistent

Examples:
- `(Alice, works_for, OpenAI)`
- `(Paris, located_in, France)`
- `(Paper_A, mentions, GPT-4)`

### Distinguish relation vs attribute

Use a relation when both sides are entities.
Use an attribute when the right-hand side is primarily a value.

Example:
- relation: `(Alice, works_for, OpenAI)`
- attribute-derived triple: `(OpenAI, founded_year, 2015)`
