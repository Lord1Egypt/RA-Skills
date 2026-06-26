# Relationships and Normalization

This reference covers how to properly establish relationships between CRM entities and ensure the schema follows sound normalization principles.

## Relationship Types in CRM

### One-to-Many (1:N) — The Most Common Pattern

Most CRM relationships are one-to-many. The "many" side holds a foreign key to the "one" side.

| Relationship | Implementation |
|---|---|
| Account → Contacts | `contacts.account_id` → `accounts.id` |
| Account → Opportunities | `opportunities.account_id` → `accounts.id` |
| User → Owned Accounts | `accounts.owner_id` → `users.id` |
| Pipeline → Stages | `pipeline_stages.pipeline_id` → `pipelines.id` |
| Opportunity → Line Items | `opportunity_line_items.opportunity_id` → `opportunities.id` |

Rules for 1:N foreign keys:
- Always create an index on the foreign key column. MySQL does NOT automatically index foreign keys (unlike some other databases).
- Choose the correct ON DELETE behavior:
  - `CASCADE` — child rows deleted when parent is deleted (use for true child entities like line items, stage history)
  - `SET NULL` — FK set to NULL when parent is deleted (use for optional references like owner_id)
  - `RESTRICT` — block parent deletion if children exist (use for critical dependencies like account on an opportunity)

### Many-to-Many (M:N) — Junction Tables

When two entities relate to each other in both directions, use a junction table. Never store comma-separated IDs in a single column.

Common CRM M:N relationships:

```sql
-- Opportunities can involve multiple contacts; contacts can appear in multiple deals
CREATE TABLE `opportunity_contacts` (
    `opportunity_id` BIGINT UNSIGNED NOT NULL,
    `contact_id` BIGINT UNSIGNED NOT NULL,
    `role` VARCHAR(100) NULL DEFAULT NULL,
    PRIMARY KEY (`opportunity_id`, `contact_id`)
);

-- Contacts can belong to multiple accounts (consultants, board members)
CREATE TABLE `account_contacts` (
    `account_id` BIGINT UNSIGNED NOT NULL,
    `contact_id` BIGINT UNSIGNED NOT NULL,
    `relationship_type` VARCHAR(50) NULL DEFAULT NULL,
    PRIMARY KEY (`account_id`, `contact_id`)
);

-- Campaigns target multiple contacts; contacts receive multiple campaigns
CREATE TABLE `campaign_contacts` (
    `campaign_id` BIGINT UNSIGNED NOT NULL,
    `contact_id` BIGINT UNSIGNED NOT NULL,
    `status` ENUM('sent', 'opened', 'clicked', 'responded', 'bounced', 'unsubscribed') NOT NULL DEFAULT 'sent',
    `sent_at` DATETIME NULL DEFAULT NULL,
    PRIMARY KEY (`campaign_id`, `contact_id`)
);
```

Junction table best practices:
- Use a composite primary key on the two FK columns for simple associations.
- Add a surrogate `id` column if you need to reference the junction row from other tables (e.g., activity tracking on a campaign-contact pair).
- Store relationship metadata on the junction table (role, status, timestamps) — not on either parent.
- Always add a reverse index. If the PK is `(opportunity_id, contact_id)`, add an index on `(contact_id)` so lookups from the contact side are fast too.

### Self-Referencing Relationships

CRM uses self-references for hierarchies:

```sql
-- Account hierarchy (parent company → subsidiaries)
ALTER TABLE `accounts`
    ADD COLUMN `parent_account_id` BIGINT UNSIGNED NULL DEFAULT NULL,
    ADD CONSTRAINT `fk_accounts_parent`
        FOREIGN KEY (`parent_account_id`) REFERENCES `accounts` (`id`) ON DELETE SET NULL;

-- User reporting structure (manager → direct reports)
ALTER TABLE `users`
    ADD COLUMN `manager_id` BIGINT UNSIGNED NULL DEFAULT NULL,
    ADD CONSTRAINT `fk_users_manager`
        FOREIGN KEY (`manager_id`) REFERENCES `users` (`id`) ON DELETE SET NULL;
```

Querying hierarchies with MySQL 8 recursive CTEs:

```sql
-- Get full account hierarchy from a given parent
WITH RECURSIVE account_tree AS (
    SELECT id, name, parent_account_id, 0 AS depth
    FROM accounts
    WHERE id = :root_account_id

    UNION ALL

    SELECT a.id, a.name, a.parent_account_id, t.depth + 1
    FROM accounts a
    INNER JOIN account_tree t ON a.parent_account_id = t.id
    WHERE t.depth < 10  -- safety limit to prevent infinite loops
)
SELECT * FROM account_tree;
```

### Polymorphic Relationships

Some CRM data relates to multiple entity types. Tags, notes, activities, and attachments commonly use this pattern.

```
taggable_type = 'contact'  + taggable_id = 42  → contacts row with id=42
taggable_type = 'account'  + taggable_id = 7   → accounts row with id=7
taggable_type = 'opportunity' + taggable_id = 15 → opportunities row with id=15
```

Tradeoffs:
- **Pro:** One table handles all entity types. No proliferation of junction tables.
- **Con:** MySQL cannot enforce foreign keys on polymorphic references. Referential integrity relies on application code.
- **Mitigation:** Use a CHECK constraint to restrict `taggable_type` to known values. Add application-level validation. Consider periodic integrity checks via scheduled queries.

## Normalization Guide for CRM

### First Normal Form (1NF)

Every column stores a single atomic value. No comma-separated lists, no JSON arrays in place of proper relationships.

**Violation:** Storing multiple phone numbers as `"555-1234, 555-5678"` in a single column.
**Fix:** Use a separate `contact_phones` table or dedicated columns (`phone`, `mobile_phone`, `work_phone`).

**Violation:** Storing tag names as `"enterprise, hot-lead, east-coast"` in a tags column.
**Fix:** Use a `tags` table and `taggables` junction table.

### Second Normal Form (2NF)

Every non-key column depends on the entire primary key (relevant for composite keys).

**Violation:** In an `opportunity_contacts` junction table with PK (`opportunity_id`, `contact_id`), storing `contact_email` — this depends only on `contact_id`, not the full key.
**Fix:** Remove `contact_email`; look it up via JOIN to `contacts`.

### Third Normal Form (3NF)

No transitive dependencies. Every non-key column depends directly on the primary key, not on another non-key column.

**Violation:** Storing both `stage_id` and `stage_name` on the `opportunities` table. `stage_name` depends on `stage_id`, not on `opportunity.id`.
**Fix:** Store only `stage_id` on `opportunities`. Look up `stage_name` via JOIN to `pipeline_stages`.

**Acceptable denormalization:** Storing `total_price` as a generated column on `opportunity_line_items`. This is technically a 3NF violation (it depends on `quantity`, `unit_price`, `discount_percent`), but as a generated column, MySQL keeps it consistent automatically.

### When to Deliberately Denormalize

Denormalize only when you have measured evidence of a performance problem, and document the decision:

1. **Cached aggregates.** Store `deal_count` and `total_revenue` on `accounts` if you frequently display account summaries. Update via triggers or application events.

2. **Snapshot values.** Store `unit_price` on `opportunity_line_items` separately from `products.unit_price` because the price at the time of the quote matters, not the current list price.

3. **Reporting tables.** Create materialized summary tables updated by scheduled jobs for dashboard queries. Keep these separate from operational tables.

## Foreign Key Strategy

### Rules of Thumb

1. Every foreign key column gets its own index.
2. Use `ON DELETE RESTRICT` as the default. Only use CASCADE for true child/dependent entities.
3. Use `ON DELETE SET NULL` for optional relationships (owner_id, assigned_to).
4. Never use `ON DELETE CASCADE` on core business entities (accounts, contacts, opportunities). Soft delete instead.
5. Use `ON UPDATE CASCADE` sparingly — if you're updating primary keys, reconsider your schema design.

### FK Index Pattern

```sql
-- For every FK column, create a dedicated index
ALTER TABLE `contacts` ADD INDEX `idx_contacts_account_id` (`account_id`);
ALTER TABLE `contacts` ADD INDEX `idx_contacts_owner_id` (`owner_id`);
ALTER TABLE `opportunities` ADD INDEX `idx_opportunities_account_id` (`account_id`);
ALTER TABLE `opportunities` ADD INDEX `idx_opportunities_stage_id` (`stage_id`);
```

Without these indexes, DELETE operations on parent tables will cause full table scans on child tables to check for references — this can lock the table and cause severe performance issues.
