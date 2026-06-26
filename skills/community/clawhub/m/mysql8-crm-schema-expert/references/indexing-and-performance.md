# Indexing and Performance

This reference covers indexing strategies, query optimization, and performance tuning for CRM databases on MySQL 8.

## Indexing Fundamentals for CRM

### Index Every Foreign Key

MySQL does not automatically index foreign key columns (InnoDB indexes the referencing column in some cases, but you should always be explicit). Without an index on every FK column:
- JOINs between parent and child tables become full table scans
- DELETE on a parent row scans the entire child table to check references
- This can cause table-level locks and cascading performance problems

```sql
-- Ensure all FK columns are indexed
ALTER TABLE `contacts` ADD INDEX `idx_contacts_account_id` (`account_id`);
ALTER TABLE `contacts` ADD INDEX `idx_contacts_owner_id` (`owner_id`);
ALTER TABLE `opportunities` ADD INDEX `idx_opportunities_account_id` (`account_id`);
ALTER TABLE `opportunities` ADD INDEX `idx_opportunities_stage_id` (`stage_id`);
ALTER TABLE `opportunities` ADD INDEX `idx_opportunities_owner_id` (`owner_id`);
ALTER TABLE `activities` ADD INDEX `idx_activities_user_id` (`user_id`);
```

### Composite Indexes for Common CRM Queries

Design composite indexes around the actual queries your CRM runs most. The column order matters — put the most selective or most commonly filtered column first.

```sql
-- Pipeline board: "Show all active deals in pipeline X, grouped by stage"
ALTER TABLE `opportunities`
    ADD INDEX `idx_opp_pipeline_board` (`pipeline_id`, `stage_id`, `deleted_at`);

-- My deals: "Show deals owned by me, sorted by expected close date"
ALTER TABLE `opportunities`
    ADD INDEX `idx_opp_owner_close` (`owner_id`, `expected_close_date`, `deleted_at`);

-- Contact search: "Find contacts by last name within an account"
ALTER TABLE `contacts`
    ADD INDEX `idx_contacts_account_name` (`account_id`, `last_name`, `first_name`);

-- Activity timeline: "Recent activities for a given entity"
ALTER TABLE `activities`
    ADD INDEX `idx_activities_entity_timeline` (`entity_type`, `entity_id`, `activity_date` DESC);

-- Lead queue: "Unassigned new leads sorted by creation date"
ALTER TABLE `leads`
    ADD INDEX `idx_leads_new_unassigned` (`status`, `owner_id`, `created_at`);
```

### Covering Indexes

A covering index includes all columns a query needs, so MySQL can satisfy the query from the index alone (no table lookup). This is especially valuable for list views and dashboards.

```sql
-- Covering index for opportunity list view
ALTER TABLE `opportunities`
    ADD INDEX `idx_opp_list_view` (
        `owner_id`, `deleted_at`, `stage_id`,
        `name`, `amount`, `expected_close_date`
    );
```

Use `EXPLAIN` and check for "Using index" in the Extra column to verify a covering index is working.

### Prefix Indexes for Long Text Columns

For VARCHAR columns longer than 191 characters (the max for utf8mb4 with a 767-byte index limit on older row formats), use prefix indexes:

```sql
-- Index only the first 50 characters of description
ALTER TABLE `accounts` ADD INDEX `idx_accounts_description` (`description`(50));

-- For URLs, index a meaningful prefix
ALTER TABLE `contacts` ADD INDEX `idx_contacts_linkedin` (`linkedin_url`(100));
```

Prefer generated columns with indexes over prefix indexes when you need exact match queries.

## MySQL 8 Specific Index Features

### Functional Indexes (MySQL 8.0.13+)

Index an expression without creating an explicit generated column:

```sql
-- Index on email domain for account matching
ALTER TABLE `contacts`
    ADD INDEX `idx_contacts_email_domain` ((SUBSTRING_INDEX(`email`, '@', -1)));

-- Index on year of created_at for reporting
ALTER TABLE `opportunities`
    ADD INDEX `idx_opp_created_year` ((YEAR(`created_at`)));

-- Case-insensitive email search
ALTER TABLE `contacts`
    ADD INDEX `idx_contacts_email_lower` ((LOWER(`email`)));
```

Important: the query must use the exact same expression as the index definition for MySQL to use it.

### Descending Indexes

MySQL 8 supports true descending indexes (earlier versions ignored DESC in index definitions):

```sql
-- Optimize "most recent first" queries
ALTER TABLE `activities`
    ADD INDEX `idx_activities_recent` (`entity_type`, `entity_id`, `activity_date` DESC);

-- Dashboard: latest deals
ALTER TABLE `opportunities`
    ADD INDEX `idx_opp_latest` (`created_at` DESC, `deleted_at`);
```

### Invisible Indexes

Test the impact of removing an index without actually dropping it:

```sql
-- Make an index invisible (optimizer ignores it)
ALTER TABLE `contacts` ALTER INDEX `idx_contacts_lead_source` INVISIBLE;

-- Run your workload and measure impact...

-- Make it visible again if needed
ALTER TABLE `contacts` ALTER INDEX `idx_contacts_lead_source` VISIBLE;

-- Or drop it if performance was unaffected
DROP INDEX `idx_contacts_lead_source` ON `contacts`;
```

### JSON Indexing Strategies

CRM systems often store semi-structured data in JSON columns (custom fields, metadata, integration payloads). MySQL cannot directly index JSON columns, but offers three approaches:

**Approach 1: Generated columns (works in MySQL 5.7+)**

```sql
-- Add a generated column that extracts a JSON value
ALTER TABLE `contacts`
    ADD COLUMN `custom_industry` VARCHAR(100)
        GENERATED ALWAYS AS (`custom_fields` ->> '$.industry') VIRTUAL,
    ADD INDEX `idx_contacts_custom_industry` (`custom_industry`);
```

**Approach 2: Functional indexes (MySQL 8.0.13+)**

```sql
-- Index a JSON path directly
ALTER TABLE `contacts`
    ADD INDEX `idx_contacts_json_industry` ((
        CAST(`custom_fields` ->> '$.industry' AS CHAR(100)) COLLATE utf8mb4_bin
    ));
```

**Approach 3: Multi-valued indexes for JSON arrays (MySQL 8.0.17+)**

```sql
-- Index elements of a JSON array
ALTER TABLE `contacts`
    ADD INDEX `idx_contacts_interests` ((
        CAST(`custom_fields` -> '$.interests' AS CHAR(50) ARRAY)
    ));

-- Query using MEMBER OF
SELECT * FROM contacts
WHERE 'machine_learning' MEMBER OF (custom_fields -> '$.interests');
```

Recommendation: Use generated STORED columns for frequently queried JSON paths — they are the most reliable and performant approach. Use functional indexes for occasional queries. Use multi-valued indexes when you need to search within JSON arrays.

## Query Optimization Patterns

### The Soft Delete Filter

Almost every CRM query needs to filter out soft-deleted records. Always include `deleted_at IS NULL` and make sure your indexes account for it:

```sql
-- BAD: Index doesn't include deleted_at
SELECT * FROM contacts WHERE account_id = 42;

-- GOOD: Index on (account_id, deleted_at), query filters both
SELECT * FROM contacts WHERE account_id = 42 AND deleted_at IS NULL;
```

Consider putting `deleted_at` as the last column in composite indexes so the optimizer can use the index for both "all records" and "non-deleted records" queries.

### Pagination

CRM list views need efficient pagination. Avoid `OFFSET` for large datasets.

```sql
-- BAD: OFFSET becomes slow as page number grows
SELECT * FROM contacts WHERE deleted_at IS NULL ORDER BY id LIMIT 25 OFFSET 10000;

-- GOOD: Keyset pagination using the last seen ID
SELECT * FROM contacts
WHERE deleted_at IS NULL AND id > :last_seen_id
ORDER BY id
LIMIT 25;
```

For sorted pagination on non-unique columns, use a composite cursor:

```sql
-- Paginate contacts sorted by last_name
SELECT * FROM contacts
WHERE deleted_at IS NULL
    AND (last_name > :last_name OR (last_name = :last_name AND id > :last_id))
ORDER BY last_name, id
LIMIT 25;
```

### Counting Large Tables

Avoid `SELECT COUNT(*)` on large CRM tables for UI display. Instead:
- Use approximate counts: `SELECT TABLE_ROWS FROM information_schema.TABLES WHERE TABLE_NAME = 'contacts'`
- Cache counts in a summary table updated by triggers or scheduled jobs
- Use `SQL_CALC_FOUND_ROWS` or window functions for "page X of Y" display

### Full-Text Search

CRM users expect to search across names, emails, descriptions, and notes. Use MySQL full-text indexes:

```sql
ALTER TABLE `contacts`
    ADD FULLTEXT INDEX `ft_contacts_search` (`first_name`, `last_name`, `email`);

ALTER TABLE `accounts`
    ADD FULLTEXT INDEX `ft_accounts_search` (`name`, `description`, `domain`);

-- Search query
SELECT * FROM contacts
WHERE MATCH(first_name, last_name, email) AGAINST ('john smith' IN BOOLEAN MODE)
    AND deleted_at IS NULL;
```

For more sophisticated search (typo tolerance, relevance ranking, faceting), consider offloading to Elasticsearch or Meilisearch and keeping MySQL as the source of truth.

## Partitioning for Large CRM Tables

Partitioning is useful for tables that grow very large (tens of millions of rows), particularly for time-series data.

### Good Candidates for Partitioning

- `activities` — partitioned by `activity_date` (RANGE partitioning by month or year)
- `audit_logs` — partitioned by `created_at`
- `email_events` — partitioned by `event_date`

### Example: Partitioning Activities by Year

```sql
CREATE TABLE `activities` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `entity_type` VARCHAR(50) NOT NULL,
    `entity_id` BIGINT UNSIGNED NOT NULL,
    `activity_type` VARCHAR(50) NOT NULL,
    `activity_date` DATETIME NOT NULL,
    `user_id` BIGINT UNSIGNED NULL,
    `summary` VARCHAR(500) NULL,
    `details` JSON NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (`id`, `activity_date`),
    INDEX `idx_activities_entity` (`entity_type`, `entity_id`, `activity_date`),
    INDEX `idx_activities_user` (`user_id`, `activity_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
PARTITION BY RANGE (YEAR(`activity_date`)) (
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p2025 VALUES LESS THAN (2026),
    PARTITION p2026 VALUES LESS THAN (2027),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

Important constraints:
- The partition key must be part of every unique index (including the primary key). That is why `activity_date` is included in the PK.
- Foreign keys are not supported on partitioned tables. Use application-level integrity checks.
- Add new partitions proactively before the year rolls over (automate this with a scheduled job).

### Tables NOT to Partition

Do not partition `accounts`, `contacts`, `opportunities`, or `users`. These are looked up by ID across all time periods, and partitioning would not help (and may hurt) these access patterns.

## Performance Monitoring Checklist

Run these periodically on your CRM database:

```sql
-- Find tables without primary keys (should be zero)
SELECT TABLE_NAME FROM information_schema.TABLES
WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_TYPE = 'BASE TABLE'
    AND TABLE_NAME NOT IN (
        SELECT TABLE_NAME FROM information_schema.TABLE_CONSTRAINTS
        WHERE CONSTRAINT_TYPE = 'PRIMARY KEY' AND TABLE_SCHEMA = DATABASE()
    );

-- Find foreign key columns without indexes
SELECT
    kcu.TABLE_NAME, kcu.COLUMN_NAME
FROM information_schema.KEY_COLUMN_USAGE kcu
LEFT JOIN information_schema.STATISTICS s
    ON s.TABLE_SCHEMA = kcu.TABLE_SCHEMA
    AND s.TABLE_NAME = kcu.TABLE_NAME
    AND s.COLUMN_NAME = kcu.COLUMN_NAME
WHERE kcu.TABLE_SCHEMA = DATABASE()
    AND kcu.REFERENCED_TABLE_NAME IS NOT NULL
    AND s.INDEX_NAME IS NULL;

-- Find slow queries (if slow_query_log is enabled)
-- Look for queries with no index usage
SELECT * FROM mysql.slow_log
WHERE query_time > '00:00:01'
ORDER BY start_time DESC LIMIT 20;
```
