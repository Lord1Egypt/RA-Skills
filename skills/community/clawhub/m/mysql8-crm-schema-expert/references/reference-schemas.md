# Reference Schemas

This file contains complete, ready-to-use CRM database schemas for common scenarios. Copy and adapt as needed.

## Schema A: Minimal CRM (Contacts + Deals)

For small teams that need basic contact and deal tracking. Approximately 8 tables.

```sql
-- ============================================================
-- Minimal CRM Schema
-- MySQL 8.0+
-- ============================================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- Users
CREATE TABLE IF NOT EXISTS `users` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `email` VARCHAR(255) NOT NULL,
    `password_hash` VARCHAR(255) NOT NULL,
    `first_name` VARCHAR(100) NOT NULL,
    `last_name` VARCHAR(100) NOT NULL,
    `role` ENUM('admin','manager','sales_rep','read_only') NOT NULL DEFAULT 'sales_rep',
    `is_active` TINYINT(1) NOT NULL DEFAULT 1,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE INDEX `uq_users_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Accounts
CREATE TABLE IF NOT EXISTS `accounts` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `domain` VARCHAR(255) NULL,
    `industry` VARCHAR(100) NULL,
    `type` ENUM('prospect','customer','partner','other') NOT NULL DEFAULT 'prospect',
    `phone` VARCHAR(30) NULL,
    `owner_id` BIGINT UNSIGNED NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `deleted_at` TIMESTAMP NULL DEFAULT NULL,
    PRIMARY KEY (`id`),
    INDEX `idx_accounts_owner` (`owner_id`),
    INDEX `idx_accounts_deleted_at` (`deleted_at`),
    CONSTRAINT `fk_accounts_owner` FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Contacts
CREATE TABLE IF NOT EXISTS `contacts` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `account_id` BIGINT UNSIGNED NULL,
    `first_name` VARCHAR(100) NOT NULL,
    `last_name` VARCHAR(100) NOT NULL,
    `email` VARCHAR(255) NULL,
    `phone` VARCHAR(30) NULL,
    `job_title` VARCHAR(150) NULL,
    `owner_id` BIGINT UNSIGNED NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `deleted_at` TIMESTAMP NULL DEFAULT NULL,
    PRIMARY KEY (`id`),
    INDEX `idx_contacts_account` (`account_id`),
    INDEX `idx_contacts_email` (`email`),
    INDEX `idx_contacts_name` (`last_name`, `first_name`),
    INDEX `idx_contacts_owner` (`owner_id`),
    INDEX `idx_contacts_deleted_at` (`deleted_at`),
    CONSTRAINT `fk_contacts_account` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_contacts_owner` FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Pipeline Stages
CREATE TABLE IF NOT EXISTS `pipeline_stages` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL,
    `display_order` INT UNSIGNED NOT NULL DEFAULT 0,
    `probability` DECIMAL(5,2) NULL,
    `is_won` TINYINT(1) NOT NULL DEFAULT 0,
    `is_lost` TINYINT(1) NOT NULL DEFAULT 0,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Opportunities
CREATE TABLE IF NOT EXISTS `opportunities` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `account_id` BIGINT UNSIGNED NOT NULL,
    `stage_id` BIGINT UNSIGNED NOT NULL,
    `amount` DECIMAL(15,2) NULL,
    `expected_close_date` DATE NULL,
    `owner_id` BIGINT UNSIGNED NULL,
    `primary_contact_id` BIGINT UNSIGNED NULL,
    `description` TEXT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `deleted_at` TIMESTAMP NULL DEFAULT NULL,
    PRIMARY KEY (`id`),
    INDEX `idx_opp_account` (`account_id`),
    INDEX `idx_opp_stage` (`stage_id`),
    INDEX `idx_opp_owner` (`owner_id`),
    INDEX `idx_opp_close_date` (`expected_close_date`),
    INDEX `idx_opp_deleted_at` (`deleted_at`),
    CONSTRAINT `fk_opp_account` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`id`) ON DELETE RESTRICT,
    CONSTRAINT `fk_opp_stage` FOREIGN KEY (`stage_id`) REFERENCES `pipeline_stages` (`id`) ON DELETE RESTRICT,
    CONSTRAINT `fk_opp_owner` FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_opp_contact` FOREIGN KEY (`primary_contact_id`) REFERENCES `contacts` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Activities (simplified)
CREATE TABLE IF NOT EXISTS `activities` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `activity_type` ENUM('call','email','meeting','note','task') NOT NULL,
    `entity_type` VARCHAR(50) NOT NULL,
    `entity_id` BIGINT UNSIGNED NOT NULL,
    `subject` VARCHAR(500) NULL,
    `body` TEXT NULL,
    `activity_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `user_id` BIGINT UNSIGNED NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `deleted_at` TIMESTAMP NULL DEFAULT NULL,
    PRIMARY KEY (`id`),
    INDEX `idx_activities_entity` (`entity_type`, `entity_id`, `activity_date` DESC),
    INDEX `idx_activities_user` (`user_id`),
    CONSTRAINT `fk_activities_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tags
CREATE TABLE IF NOT EXISTS `tags` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE INDEX `uq_tags_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `taggables` (
    `tag_id` BIGINT UNSIGNED NOT NULL,
    `taggable_type` VARCHAR(50) NOT NULL,
    `taggable_id` BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY (`tag_id`, `taggable_type`, `taggable_id`),
    INDEX `idx_taggables_target` (`taggable_type`, `taggable_id`),
    CONSTRAINT `fk_taggables_tag` FOREIGN KEY (`tag_id`) REFERENCES `tags` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;

-- Default pipeline stages
INSERT INTO `pipeline_stages` (`name`, `display_order`, `probability`, `is_won`, `is_lost`) VALUES
('Qualification', 1, 10.00, 0, 0),
('Discovery', 2, 20.00, 0, 0),
('Proposal', 3, 50.00, 0, 0),
('Negotiation', 4, 75.00, 0, 0),
('Closed Won', 5, 100.00, 1, 0),
('Closed Lost', 6, 0.00, 0, 1);
```

## Schema B: Full-Featured CRM

For teams that need the complete CRM stack: contacts, accounts, leads, multi-pipeline deals, products, activities, tasks, notes, audit trail, custom fields, RBAC, and tags. This builds on Schema A and adds all the enterprise features.

Tables included (in creation order):
1. `users`
2. `roles`, `permissions`, `role_permissions`, `user_roles`
3. `teams`, `team_members`
4. `accounts`
5. `contacts`
6. `leads`
7. `pipelines`, `pipeline_stages`
8. `products`
9. `opportunities`
10. `opportunity_line_items`
11. `opportunity_contacts`
12. `activities`
13. `activity_associations`
14. `notes`
15. `tasks`
16. `attachments`
17. `tags`, `taggables`
18. `custom_field_definitions`, `custom_field_values`
19. `audit_logs`

See the individual reference files for the complete CREATE TABLE statements for each. Combine them in the order listed above to produce a full migration script.

## Schema C: Multi-Tenant SaaS CRM

Extends Schema B with a `tenant_id` column on every table. Key differences:

```sql
-- Add to every CRM table:
ALTER TABLE `accounts` ADD COLUMN `tenant_id` BIGINT UNSIGNED NOT NULL AFTER `id`;
ALTER TABLE `contacts` ADD COLUMN `tenant_id` BIGINT UNSIGNED NOT NULL AFTER `id`;
-- ... repeat for all tables

-- Modify every index to be tenant-scoped:
ALTER TABLE `contacts` DROP INDEX `idx_contacts_email`;
ALTER TABLE `contacts` ADD INDEX `idx_contacts_tenant_email` (`tenant_id`, `email`);

-- Modify unique constraints to be tenant-scoped:
ALTER TABLE `pipelines` ADD UNIQUE INDEX `uq_pipelines_tenant_name` (`tenant_id`, `name`);
```

See `security-and-multitenancy.md` for the complete multi-tenancy implementation guide.

## Common CRM Queries Reference

These are the most commonly run queries in a CRM, useful for verifying that your schema and indexes support them efficiently:

```sql
-- 1. Pipeline board (kanban view)
SELECT o.*, ps.name AS stage_name, a.name AS account_name
FROM opportunities o
INNER JOIN pipeline_stages ps ON ps.id = o.stage_id
INNER JOIN accounts a ON a.id = o.account_id
WHERE o.pipeline_id = :pipeline_id AND o.deleted_at IS NULL
ORDER BY ps.display_order, o.updated_at DESC;

-- 2. My open deals
SELECT o.*, a.name AS account_name
FROM opportunities o
INNER JOIN accounts a ON a.id = o.account_id
WHERE o.owner_id = :user_id
    AND o.deleted_at IS NULL
    AND o.stage_id NOT IN (SELECT id FROM pipeline_stages WHERE is_won = 1 OR is_lost = 1)
ORDER BY o.expected_close_date;

-- 3. Account 360 view
SELECT a.*,
    (SELECT COUNT(*) FROM contacts c WHERE c.account_id = a.id AND c.deleted_at IS NULL) AS contact_count,
    (SELECT COUNT(*) FROM opportunities o WHERE o.account_id = a.id AND o.deleted_at IS NULL) AS deal_count,
    (SELECT SUM(o.amount) FROM opportunities o
     INNER JOIN pipeline_stages ps ON ps.id = o.stage_id
     WHERE o.account_id = a.id AND ps.is_won = 1 AND o.deleted_at IS NULL) AS total_won_revenue
FROM accounts a
WHERE a.id = :account_id;

-- 4. Lead conversion funnel
SELECT
    source,
    COUNT(*) AS total_leads,
    SUM(CASE WHEN status = 'converted' THEN 1 ELSE 0 END) AS converted,
    ROUND(SUM(CASE WHEN status = 'converted' THEN 1 ELSE 0 END) / COUNT(*) * 100, 1) AS conversion_rate
FROM leads
WHERE deleted_at IS NULL AND created_at >= :start_date
GROUP BY source
ORDER BY total_leads DESC;

-- 5. Sales forecast
SELECT
    ps.name AS stage_name,
    COUNT(*) AS deal_count,
    SUM(o.amount) AS total_value,
    SUM(o.amount * COALESCE(o.probability, ps.probability) / 100) AS weighted_value
FROM opportunities o
INNER JOIN pipeline_stages ps ON ps.id = o.stage_id
WHERE o.pipeline_id = :pipeline_id
    AND o.deleted_at IS NULL
    AND ps.is_won = 0 AND ps.is_lost = 0
    AND o.expected_close_date BETWEEN :start_date AND :end_date
GROUP BY ps.id, ps.name, ps.display_order
ORDER BY ps.display_order;

-- 6. Activity leaderboard (rep productivity)
SELECT
    u.first_name, u.last_name,
    COUNT(*) AS total_activities,
    SUM(CASE WHEN a.activity_type = 'call' THEN 1 ELSE 0 END) AS calls,
    SUM(CASE WHEN a.activity_type = 'email' THEN 1 ELSE 0 END) AS emails,
    SUM(CASE WHEN a.activity_type = 'meeting' THEN 1 ELSE 0 END) AS meetings
FROM activities a
INNER JOIN users u ON u.id = a.user_id
WHERE a.activity_date BETWEEN :start_date AND :end_date
    AND a.deleted_at IS NULL
GROUP BY u.id, u.first_name, u.last_name
ORDER BY total_activities DESC;

-- 7. Contacts due for follow-up (no activity in 30 days)
SELECT c.*, a.name AS account_name,
    MAX(act.activity_date) AS last_activity_date
FROM contacts c
LEFT JOIN accounts a ON a.id = c.account_id
LEFT JOIN activities act ON act.contact_id = c.id AND act.deleted_at IS NULL
WHERE c.deleted_at IS NULL
    AND c.lifecycle_stage IN ('lead', 'mql', 'sql', 'opportunity')
GROUP BY c.id
HAVING last_activity_date < DATE_SUB(NOW(), INTERVAL 30 DAY)
    OR last_activity_date IS NULL
ORDER BY last_activity_date ASC
LIMIT 50;

-- 8. Overdue tasks
SELECT t.*, u.first_name, u.last_name
FROM tasks t
LEFT JOIN users u ON u.id = t.assignee_id
WHERE t.status IN ('open', 'in_progress')
    AND t.due_date < NOW()
    AND t.deleted_at IS NULL
ORDER BY t.due_date ASC;
```

Run `EXPLAIN` on each of these queries against your schema to verify index usage. If any show `type: ALL` (full table scan) or missing indexes, revisit `indexing-and-performance.md`.
