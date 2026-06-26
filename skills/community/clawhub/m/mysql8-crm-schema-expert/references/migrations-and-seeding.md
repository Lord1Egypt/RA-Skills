# Migrations and Seeding

This reference covers schema versioning, writing safe migration scripts, and generating realistic CRM test data.

## Migration Best Practices

### File Naming Convention

Use sequential, timestamped filenames:

```
migrations/
├── 001_20260101_000000_create_users_table.sql
├── 002_20260101_000001_create_accounts_table.sql
├── 003_20260101_000002_create_contacts_table.sql
├── 004_20260101_000003_create_leads_table.sql
├── 005_20260101_000004_create_pipelines_and_stages.sql
├── 006_20260101_000005_create_opportunities_table.sql
├── 007_20260101_000006_create_products_and_line_items.sql
├── 008_20260101_000007_create_activities_table.sql
├── 009_20260101_000008_create_notes_and_tasks.sql
├── 010_20260101_000009_create_audit_logs_table.sql
├── 011_20260101_000010_create_tags_table.sql
├── 012_20260101_000011_create_custom_fields.sql
├── 013_20260101_000012_create_attachments_table.sql
└── 014_20260101_000013_add_fulltext_indexes.sql
```

### Migration Tracking Table

Track which migrations have been applied:

```sql
CREATE TABLE `schema_migrations` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `migration` VARCHAR(255) NOT NULL,
    `applied_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `checksum` VARCHAR(64) NULL DEFAULT NULL COMMENT 'SHA-256 of migration content',
    `execution_time_ms` INT UNSIGNED NULL DEFAULT NULL,

    PRIMARY KEY (`id`),
    UNIQUE INDEX `uq_migrations_name` (`migration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### Writing Safe Migrations

**Always use IF NOT EXISTS / IF EXISTS:**

```sql
-- Safe table creation
CREATE TABLE IF NOT EXISTS `contacts` (
    -- ...
);

-- Safe column addition
-- MySQL does not support IF NOT EXISTS for columns, so check first:
SET @col_exists = (
    SELECT COUNT(*) FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
        AND TABLE_NAME = 'contacts'
        AND COLUMN_NAME = 'linkedin_url'
);
SET @sql = IF(@col_exists = 0,
    'ALTER TABLE `contacts` ADD COLUMN `linkedin_url` VARCHAR(500) NULL DEFAULT NULL',
    'SELECT 1');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
```

**Include both up and down migrations:**

```sql
-- ============================================================
-- Migration: 015_20260415_add_priority_to_opportunities
-- ============================================================

-- UP
ALTER TABLE `opportunities`
    ADD COLUMN `priority` ENUM('low', 'medium', 'high', 'critical')
    NOT NULL DEFAULT 'medium' AFTER `type`;

ALTER TABLE `opportunities`
    ADD INDEX `idx_opportunities_priority` (`priority`);

-- DOWN (rollback)
-- ALTER TABLE `opportunities` DROP INDEX `idx_opportunities_priority`;
-- ALTER TABLE `opportunities` DROP COLUMN `priority`;
```

**Handle large tables carefully:**

For tables with millions of rows, direct ALTER TABLE can lock the table for a long time. Strategies:

1. Use `ALGORITHM=INPLACE, LOCK=NONE` when MySQL supports it:
```sql
ALTER TABLE `activities`
    ADD COLUMN `sentiment` ENUM('positive', 'neutral', 'negative') NULL DEFAULT NULL,
    ALGORITHM=INPLACE, LOCK=NONE;
```

2. For changes that require table rebuild, use pt-online-schema-change or gh-ost:
```bash
# Using Percona pt-online-schema-change
pt-online-schema-change --alter "ADD COLUMN sentiment ENUM('positive','neutral','negative') NULL DEFAULT NULL" \
    D=crm,t=activities --execute
```

3. Create a new table, copy data, and swap (manual online DDL):
```sql
CREATE TABLE `activities_new` LIKE `activities`;
ALTER TABLE `activities_new` ADD COLUMN `sentiment` ENUM('positive','neutral','negative') NULL DEFAULT NULL;
-- Copy data in batches...
RENAME TABLE `activities` TO `activities_old`, `activities_new` TO `activities`;
```

### Execution Order

Migrations must execute in dependency order. The correct order for a CRM schema:

1. `users` — no dependencies
2. `tenants` — no dependencies (if multi-tenant)
3. `teams`, `team_members` — depends on `users`
4. `roles`, `permissions`, `role_permissions`, `user_roles` — depends on `users`
5. `accounts` — depends on `users` (for owner_id)
6. `contacts` — depends on `accounts`, `users`
7. `leads` — depends on `users`, `contacts`, `accounts`
8. `pipelines`, `pipeline_stages` — depends on nothing or `tenants`
9. `products` — no dependencies
10. `opportunities` — depends on `accounts`, `pipelines`, `pipeline_stages`, `users`, `contacts`
11. `opportunity_line_items` — depends on `opportunities`, `products`
12. `opportunity_contacts` — depends on `opportunities`, `contacts`
13. `activities` — depends on `users`, `accounts`, `contacts`, `opportunities`
14. `notes`, `tasks` — depends on `users`
15. `tags`, `taggables` — depends on nothing (polymorphic)
16. `attachments` — depends on `users`
17. `audit_logs` — no FK dependencies (polymorphic)
18. `custom_field_definitions`, `custom_field_values` — no FK dependencies (polymorphic)

## Seed Data

### Generating Realistic CRM Test Data

Seed data should be realistic enough to test query patterns, UI layouts, and reporting.

```sql
-- ============================================================
-- Seed: Users (sales team)
-- ============================================================
INSERT INTO `users` (`email`, `password_hash`, `first_name`, `last_name`, `role`, `timezone`) VALUES
('admin@crm.local', '$2b$12$placeholder_hash', 'Admin', 'User', 'admin', 'America/Chicago'),
('sarah.chen@crm.local', '$2b$12$placeholder_hash', 'Sarah', 'Chen', 'manager', 'America/New_York'),
('james.wilson@crm.local', '$2b$12$placeholder_hash', 'James', 'Wilson', 'sales_rep', 'America/Chicago'),
('maria.garcia@crm.local', '$2b$12$placeholder_hash', 'Maria', 'Garcia', 'sales_rep', 'America/Los_Angeles'),
('alex.johnson@crm.local', '$2b$12$placeholder_hash', 'Alex', 'Johnson', 'sales_rep', 'America/New_York'),
('priya.patel@crm.local', '$2b$12$placeholder_hash', 'Priya', 'Patel', 'support_agent', 'America/Chicago');

-- ============================================================
-- Seed: Accounts
-- ============================================================
INSERT INTO `accounts` (`name`, `domain`, `industry`, `company_size`, `type`, `status`, `owner_id`, `billing_country`) VALUES
('Acme Corporation', 'acme.com', 'Manufacturing', '201-500', 'customer', 'active', 3, 'US'),
('TechStart Inc', 'techstart.io', 'Technology', '11-50', 'prospect', 'active', 4, 'US'),
('Global Logistics Ltd', 'globallogistics.co.uk', 'Transportation', '501-1000', 'customer', 'active', 3, 'GB'),
('Sunrise Healthcare', 'sunrisehealth.org', 'Healthcare', '1001-5000', 'prospect', 'active', 5, 'US'),
('Nordic Design Studio', 'nordicdesign.se', 'Design', '1-10', 'partner', 'active', 4, 'SE'),
('Pacific Financial Group', 'pacificfin.com', 'Finance', '201-500', 'customer', 'active', 5, 'US'),
('RedBridge Consulting', 'redbridge.com.au', 'Consulting', '51-200', 'prospect', 'active', 3, 'AU'),
('MegaRetail Corp', 'megaretail.com', 'Retail', '5000+', 'customer', 'active', 2, 'US');

-- ============================================================
-- Seed: Contacts
-- ============================================================
INSERT INTO `contacts` (`account_id`, `first_name`, `last_name`, `email`, `phone`, `job_title`, `lifecycle_stage`, `owner_id`, `is_primary`) VALUES
(1, 'Robert', 'Smith', 'robert.smith@acme.com', '+1-555-0101', 'VP of Operations', 'customer', 3, 1),
(1, 'Lisa', 'Wang', 'lisa.wang@acme.com', '+1-555-0102', 'Procurement Manager', 'customer', 3, 0),
(2, 'David', 'Kim', 'david.kim@techstart.io', '+1-555-0201', 'CEO', 'sql', 4, 1),
(2, 'Emily', 'Brown', 'emily.brown@techstart.io', '+1-555-0202', 'CTO', 'sql', 4, 0),
(3, 'Oliver', 'Hughes', 'oliver.hughes@globallogistics.co.uk', '+44-20-7123-0001', 'Head of IT', 'customer', 3, 1),
(4, 'Jennifer', 'Martinez', 'j.martinez@sunrisehealth.org', '+1-555-0401', 'CFO', 'mql', 5, 1),
(5, 'Erik', 'Lindqvist', 'erik@nordicdesign.se', '+46-8-123-4567', 'Founder', 'customer', 4, 1),
(6, 'Patricia', 'Adams', 'p.adams@pacificfin.com', '+1-555-0601', 'Director of Technology', 'customer', 5, 1),
(7, 'Michael', 'Thompson', 'm.thompson@redbridge.com.au', '+61-2-8765-4321', 'Managing Partner', 'lead', 3, 1),
(8, 'Catherine', 'Lee', 'c.lee@megaretail.com', '+1-555-0801', 'SVP of Supply Chain', 'customer', 2, 1);

-- ============================================================
-- Seed: Pipelines and Stages
-- ============================================================
INSERT INTO `pipelines` (`name`, `description`, `is_default`) VALUES
('New Business', 'Pipeline for new customer acquisition', 1),
('Renewals', 'Pipeline for contract renewals', 0),
('Upsell', 'Pipeline for upsell and expansion deals', 0);

INSERT INTO `pipeline_stages` (`pipeline_id`, `name`, `display_order`, `probability`, `is_won`, `is_lost`) VALUES
(1, 'Qualification', 1, 10.00, 0, 0),
(1, 'Discovery', 2, 20.00, 0, 0),
(1, 'Proposal', 3, 50.00, 0, 0),
(1, 'Negotiation', 4, 75.00, 0, 0),
(1, 'Closed Won', 5, 100.00, 1, 0),
(1, 'Closed Lost', 6, 0.00, 0, 1),
(2, 'Renewal Pending', 1, 70.00, 0, 0),
(2, 'In Negotiation', 2, 85.00, 0, 0),
(2, 'Renewed', 3, 100.00, 1, 0),
(2, 'Churned', 4, 0.00, 0, 1),
(3, 'Identified', 1, 20.00, 0, 0),
(3, 'Proposed', 2, 50.00, 0, 0),
(3, 'Committed', 3, 90.00, 0, 0),
(3, 'Won', 4, 100.00, 1, 0),
(3, 'Lost', 5, 0.00, 0, 1);

-- ============================================================
-- Seed: Opportunities
-- ============================================================
INSERT INTO `opportunities` (`name`, `account_id`, `pipeline_id`, `stage_id`, `amount`, `expected_close_date`, `type`, `owner_id`, `primary_contact_id`) VALUES
('Acme - Annual License Renewal', 1, 2, 7, 45000.00, '2026-06-30', 'renewal', 3, 1),
('TechStart - Platform Subscription', 2, 1, 3, 120000.00, '2026-05-15', 'new_business', 4, 3),
('Global Logistics - Expansion', 3, 3, 11, 85000.00, '2026-07-01', 'upsell', 3, 5),
('Sunrise Healthcare - Enterprise License', 4, 1, 2, 250000.00, '2026-08-30', 'new_business', 5, 6),
('Pacific Financial - Add-on Modules', 6, 3, 12, 35000.00, '2026-05-30', 'cross_sell', 5, 8),
('RedBridge - Initial Contract', 7, 1, 1, 60000.00, '2026-09-15', 'new_business', 3, 9);

-- ============================================================
-- Seed: Leads
-- ============================================================
INSERT INTO `leads` (`first_name`, `last_name`, `email`, `company_name`, `job_title`, `source`, `status`, `rating`, `score`, `owner_id`) VALUES
('Andrew', 'Taylor', 'a.taylor@bigcorp.com', 'BigCorp Industries', 'IT Director', 'website', 'new', 'hot', 85, 3),
('Sophie', 'Dubois', 's.dubois@paristech.fr', 'ParisTech Solutions', 'COO', 'trade_show', 'contacted', 'warm', 62, 4),
('Raj', 'Sharma', 'raj.sharma@mumbaisoft.in', 'Mumbai Software Labs', 'VP Engineering', 'referral', 'qualified', 'hot', 90, 5),
('Hannah', 'Miller', 'h.miller@greenleaf.eco', 'GreenLeaf Sustainability', 'Founder', 'linkedin', 'new', 'cold', 30, NULL),
('Carlos', 'Reyes', 'c.reyes@latamlogix.mx', 'LatAm Logix', 'Head of Procurement', 'advertisement', 'contacted', 'warm', 55, 4);

-- ============================================================
-- Seed: Activities
-- ============================================================
INSERT INTO `activities` (`activity_type`, `entity_type`, `entity_id`, `activity_date`, `user_id`, `subject`, `body`, `duration_minutes`, `account_id`, `contact_id`, `metadata`) VALUES
('call', 'contact', 1, '2026-03-28 10:00:00', 3, 'Renewal discussion call', 'Discussed renewal terms. Robert is happy with service but wants to negotiate pricing.', 25, 1, 1, '{"direction":"outbound","outcome":"connected"}'),
('email', 'contact', 3, '2026-03-29 14:30:00', 4, 'Proposal follow-up', 'Sent updated proposal with revised pricing tier.', NULL, 2, 3, '{"direction":"outbound","has_attachments":true}'),
('meeting', 'opportunity', 4, '2026-04-01 09:00:00', 5, 'Discovery meeting with Sunrise Healthcare', 'Deep dive into their requirements. They need HIPAA compliance features.', 60, 4, 6, '{"location":"Zoom","attendees":2,"outcome":"completed"}'),
('note', 'account', 8, '2026-04-02 11:00:00', 2, 'Quarterly business review notes', 'MegaRetail is very satisfied. Potential for 30% expansion this year.', NULL, 8, 10, NULL),
('task', 'lead', 1, '2026-04-03 08:00:00', 3, 'Follow up with Andrew Taylor at BigCorp', NULL, NULL, NULL, NULL, NULL);
```

### Volume Testing

For performance testing, generate large volumes of data. Use a stored procedure or an external script:

```sql
-- Generate 10,000 contacts across existing accounts
DELIMITER //
CREATE PROCEDURE seed_contacts(IN num_contacts INT)
BEGIN
    DECLARE i INT DEFAULT 0;
    DECLARE v_account_id BIGINT;
    DECLARE v_owner_id BIGINT;

    WHILE i < num_contacts DO
        SET v_account_id = FLOOR(1 + RAND() * 8);
        SET v_owner_id = FLOOR(2 + RAND() * 4);

        INSERT INTO contacts (account_id, first_name, last_name, email, lifecycle_stage, owner_id)
        VALUES (
            v_account_id,
            ELT(FLOOR(1 + RAND() * 10), 'James','Mary','John','Patricia','Robert','Jennifer','Michael','Linda','David','Elizabeth'),
            ELT(FLOOR(1 + RAND() * 10), 'Smith','Johnson','Williams','Brown','Jones','Garcia','Miller','Davis','Rodriguez','Martinez'),
            CONCAT('contact_', i, '_', FLOOR(RAND() * 10000), '@example.com'),
            ELT(FLOOR(1 + RAND() * 5), 'subscriber','lead','mql','sql','customer'),
            v_owner_id
        );

        SET i = i + 1;
    END WHILE;
END //
DELIMITER ;

-- Run it
CALL seed_contacts(10000);

-- Clean up
DROP PROCEDURE IF EXISTS seed_contacts;
```

### Seed Data Principles

1. Use realistic names, emails, and company names — not "test1", "test2".
2. Create data that exercises all relationship types (accounts with multiple contacts, contacts with multiple opportunities, etc.).
3. Include data in various statuses (active, inactive, converted, closed-won, closed-lost).
4. Include edge cases: contacts without accounts, leads that have been converted, accounts with hierarchies.
5. Use consistent, documented passwords (like `$2b$12$placeholder_hash`) and note that they are not real hashes.
6. Timestamp data should span multiple months/quarters to test reporting.
