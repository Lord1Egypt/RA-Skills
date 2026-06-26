# Audit Trails and Soft Deletes

CRM data has legal, compliance, and business intelligence value. Deleting records permanently destroys historical context. This reference covers patterns for preserving data integrity, tracking changes, and meeting compliance requirements.

## Soft Deletes

### The Pattern

Instead of `DELETE FROM contacts WHERE id = 42`, set a deletion timestamp:

```sql
UPDATE contacts SET deleted_at = NOW(), updated_by = :user_id WHERE id = 42;
```

Every CRM entity table should include:

```sql
`deleted_at` TIMESTAMP NULL DEFAULT NULL,
```

And an index to support filtering:

```sql
INDEX `idx_tablename_deleted_at` (`deleted_at`)
```

### Query Discipline

Every query that fetches active records must include the soft delete filter:

```sql
-- Always filter for active records
SELECT * FROM contacts WHERE account_id = 42 AND deleted_at IS NULL;

-- For admin/compliance views that need to see deleted records
SELECT * FROM contacts WHERE account_id = 42;

-- To see only deleted records
SELECT * FROM contacts WHERE account_id = 42 AND deleted_at IS NOT NULL;
```

Consider creating views for active records to avoid forgetting the filter:

```sql
CREATE VIEW `active_contacts` AS
SELECT * FROM `contacts` WHERE `deleted_at` IS NULL;

CREATE VIEW `active_accounts` AS
SELECT * FROM `accounts` WHERE `deleted_at` IS NULL;

CREATE VIEW `active_opportunities` AS
SELECT * FROM `opportunities` WHERE `deleted_at` IS NULL;
```

### Handling Unique Constraints with Soft Deletes

Problem: if `email` has a UNIQUE index and a contact is soft-deleted, no new contact can be created with the same email.

Solutions:

**Option A: Partial unique index (not natively supported in MySQL)**
MySQL does not support partial/filtered unique indexes. Use Option B or C.

**Option B: Unique on (email, deleted_at) with a sentinel value**
```sql
-- Use a fixed date for active records, actual deletion time for deleted ones
-- This allows the same email to exist once as active plus multiple times as deleted
ALTER TABLE `contacts`
    ADD UNIQUE INDEX `uq_contacts_email_active` (`email`, `deleted_at`);
```
This works because `deleted_at = NULL` is treated as unique by MySQL (each NULL is distinct). However, it means two active records with the same email are both allowed since `(email, NULL)` and `(email, NULL)` are not considered duplicates. This approach has limitations.

**Option C: Application-level uniqueness check (most practical)**
```sql
-- Add a non-unique index for performance
ALTER TABLE `contacts` ADD INDEX `idx_contacts_email` (`email`);
```
Check uniqueness in application code: `SELECT id FROM contacts WHERE email = :email AND deleted_at IS NULL LIMIT 1`. This is the most common approach in production CRM systems.

**Option D: Generated column approach**
```sql
ALTER TABLE `contacts`
    ADD COLUMN `email_unique_check` VARCHAR(255)
        GENERATED ALWAYS AS (IF(`deleted_at` IS NULL, `email`, NULL)) STORED,
    ADD UNIQUE INDEX `uq_contacts_email_active` (`email_unique_check`);
```
This creates a generated column that is non-NULL only for active records, allowing a unique index that only applies to active rows. Multiple NULL values in a unique index are allowed.

### Restore (Undelete)

```sql
UPDATE contacts SET deleted_at = NULL, updated_by = :user_id WHERE id = 42;
```

### Cascading Soft Deletes

When an account is soft-deleted, should its contacts and opportunities also be soft-deleted? This depends on business rules. Common approaches:
- Soft-delete only the parent, and filter children by joining to the parent's `deleted_at`
- Cascade the soft delete in application code or a trigger
- Leave children active but orphaned, and let a cleanup job handle them

## Audit Trail

### Audit Log Table

A central audit log records every significant change to CRM data.

```sql
CREATE TABLE `audit_logs` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `entity_type` VARCHAR(50) NOT NULL COMMENT 'Table name: contact, account, opportunity, etc.',
    `entity_id` BIGINT UNSIGNED NOT NULL,
    `action` ENUM('create', 'update', 'delete', 'restore', 'merge', 'convert', 'assign') NOT NULL,
    `user_id` BIGINT UNSIGNED NULL DEFAULT NULL COMMENT 'User who made the change, NULL for system actions',
    `changes` JSON NULL DEFAULT NULL COMMENT 'Field-level diff: {"field": {"old": "x", "new": "y"}}',
    `metadata` JSON NULL DEFAULT NULL COMMENT 'Additional context: IP address, source, request_id',
    `created_at` TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),

    PRIMARY KEY (`id`),
    INDEX `idx_audit_entity` (`entity_type`, `entity_id`, `created_at`),
    INDEX `idx_audit_user` (`user_id`, `created_at`),
    INDEX `idx_audit_action` (`action`, `created_at`),
    INDEX `idx_audit_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

Use `TIMESTAMP(3)` for millisecond precision — important when multiple changes happen in rapid succession.

### What to Log

Log all changes to core CRM entities. The `changes` JSON should capture:

```json
{
    "first_name": {"old": "Jon", "new": "John"},
    "email": {"old": "jon@acme.com", "new": "john@acme.com"},
    "lifecycle_stage": {"old": "lead", "new": "mql"}
}
```

For create actions, log the initial values:
```json
{
    "first_name": {"old": null, "new": "John"},
    "email": {"old": null, "new": "john@acme.com"}
}
```

For delete actions, log the key identifying fields:
```json
{
    "first_name": {"old": "John", "new": null},
    "email": {"old": "john@acme.com", "new": null}
}
```

### Implementation: Application Level vs. Triggers

**Application-level logging (recommended):**
- Captured in the service layer before/after save
- Has access to the current user, request context, and business logic
- Can batch audit entries and write asynchronously
- Easier to test and maintain

**Trigger-based logging:**
- Catches all changes including direct SQL and admin operations
- Does not know who made the change (no user context in MySQL triggers)
- Adds overhead to every write operation
- Harder to debug and maintain

Recommendation: Use application-level logging as the primary mechanism. Add database triggers only if you need to catch out-of-band changes (direct SQL access, migration scripts, etc.).

### Example Trigger (for reference)

```sql
DELIMITER //

CREATE TRIGGER `trg_contacts_after_update`
AFTER UPDATE ON `contacts`
FOR EACH ROW
BEGIN
    DECLARE v_changes JSON DEFAULT JSON_OBJECT();

    IF OLD.first_name != NEW.first_name OR (OLD.first_name IS NULL) != (NEW.first_name IS NULL) THEN
        SET v_changes = JSON_SET(v_changes, '$.first_name',
            JSON_OBJECT('old', OLD.first_name, 'new', NEW.first_name));
    END IF;

    IF OLD.email != NEW.email OR (OLD.email IS NULL) != (NEW.email IS NULL) THEN
        SET v_changes = JSON_SET(v_changes, '$.email',
            JSON_OBJECT('old', OLD.email, 'new', NEW.email));
    END IF;

    IF OLD.lifecycle_stage != NEW.lifecycle_stage THEN
        SET v_changes = JSON_SET(v_changes, '$.lifecycle_stage',
            JSON_OBJECT('old', OLD.lifecycle_stage, 'new', NEW.lifecycle_stage));
    END IF;

    -- Only insert if something actually changed
    IF JSON_LENGTH(v_changes) > 0 THEN
        INSERT INTO audit_logs (entity_type, entity_id, action, user_id, changes)
        VALUES ('contact', NEW.id, 'update', NEW.updated_by, v_changes);
    END IF;
END //

DELIMITER ;
```

### Partitioning Audit Logs

Audit logs grow unboundedly. Partition by time period:

```sql
CREATE TABLE `audit_logs` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `entity_type` VARCHAR(50) NOT NULL,
    `entity_id` BIGINT UNSIGNED NOT NULL,
    `action` ENUM('create','update','delete','restore','merge','convert','assign') NOT NULL,
    `user_id` BIGINT UNSIGNED NULL,
    `changes` JSON NULL,
    `metadata` JSON NULL,
    `created_at` TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),

    PRIMARY KEY (`id`, `created_at`),
    INDEX `idx_audit_entity` (`entity_type`, `entity_id`, `created_at`),
    INDEX `idx_audit_user` (`user_id`, `created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
PARTITION BY RANGE (UNIX_TIMESTAMP(`created_at`)) (
    PARTITION p2025_q1 VALUES LESS THAN (UNIX_TIMESTAMP('2025-04-01')),
    PARTITION p2025_q2 VALUES LESS THAN (UNIX_TIMESTAMP('2025-07-01')),
    PARTITION p2025_q3 VALUES LESS THAN (UNIX_TIMESTAMP('2025-10-01')),
    PARTITION p2025_q4 VALUES LESS THAN (UNIX_TIMESTAMP('2026-01-01')),
    PARTITION p2026_q1 VALUES LESS THAN (UNIX_TIMESTAMP('2026-04-01')),
    PARTITION p2026_q2 VALUES LESS THAN (UNIX_TIMESTAMP('2026-07-01')),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

Benefits:
- Old partitions can be archived or dropped without affecting active data
- Queries that filter by date range automatically prune irrelevant partitions
- Maintenance operations (OPTIMIZE, ANALYZE) can target individual partitions

## GDPR and Data Privacy Compliance

### Right to Erasure

GDPR requires the ability to permanently delete personal data on request. Soft deletes alone are not sufficient.

Implement a "hard purge" process:

```sql
-- Step 1: Anonymize the contact record
UPDATE contacts SET
    first_name = 'REDACTED',
    last_name = 'REDACTED',
    email = CONCAT('redacted_', id, '@deleted.invalid'),
    phone = NULL,
    mobile_phone = NULL,
    mailing_address_line1 = NULL,
    mailing_address_line2 = NULL,
    mailing_city = NULL,
    mailing_state = NULL,
    mailing_postal_code = NULL,
    mailing_country = NULL,
    linkedin_url = NULL,
    custom_fields = NULL,
    deleted_at = NOW()
WHERE id = :contact_id;

-- Step 2: Anonymize related audit log entries
UPDATE audit_logs SET
    changes = JSON_OBJECT('redacted', true, 'reason', 'gdpr_erasure_request')
WHERE entity_type = 'contact' AND entity_id = :contact_id;

-- Step 3: Log the erasure event itself
INSERT INTO audit_logs (entity_type, entity_id, action, user_id, metadata)
VALUES ('contact', :contact_id, 'delete', :admin_user_id,
    JSON_OBJECT('reason', 'gdpr_erasure_request', 'request_date', NOW()));
```

Key points:
- Anonymize rather than DELETE to preserve referential integrity and aggregate reporting.
- The anonymized email uses a pattern (`redacted_42@deleted.invalid`) that is unique and clearly non-functional.
- Keep the audit log entry documenting that erasure happened (the erasure itself is a compliance event).

### Data Retention Policies

Define retention periods per data type:

| Data Type | Suggested Retention | Action After Expiry |
|-----------|-------------------|-------------------|
| Active CRM records | Indefinite | N/A |
| Soft-deleted records | 90 days | Hard purge or archive |
| Audit logs | 2-7 years | Archive to cold storage |
| Activity logs | 1-3 years | Archive or aggregate |
| Email/campaign events | 1-2 years | Aggregate into summary tables |

Implement automated retention jobs that run daily or weekly to enforce these policies.
