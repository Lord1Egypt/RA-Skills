# Security and Multi-Tenancy

CRM systems contain sensitive customer data. This reference covers database-level security patterns, role-based access control, and multi-tenant isolation strategies for MySQL 8.

## Role-Based Access Control (RBAC)

### Simple Role System

For most CRMs, an ENUM on the users table is sufficient:

```sql
ALTER TABLE `users`
    ADD COLUMN `role` ENUM('admin', 'manager', 'sales_rep', 'support_agent', 'read_only')
    NOT NULL DEFAULT 'sales_rep';
```

### Advanced RBAC with Permissions

For fine-grained control, implement a roles-and-permissions system:

```sql
CREATE TABLE `roles` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL,
    `description` TEXT NULL DEFAULT NULL,
    `is_system` TINYINT(1) NOT NULL DEFAULT 0 COMMENT 'System roles cannot be deleted',
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (`id`),
    UNIQUE INDEX `uq_roles_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `permissions` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL COMMENT 'e.g., contacts.view, contacts.edit, contacts.delete',
    `entity_type` VARCHAR(50) NOT NULL COMMENT 'e.g., contact, account, opportunity',
    `action` VARCHAR(50) NOT NULL COMMENT 'e.g., view, create, edit, delete, export, import',
    `description` TEXT NULL DEFAULT NULL,

    PRIMARY KEY (`id`),
    UNIQUE INDEX `uq_permissions_name` (`name`),
    INDEX `idx_permissions_entity_action` (`entity_type`, `action`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `role_permissions` (
    `role_id` BIGINT UNSIGNED NOT NULL,
    `permission_id` BIGINT UNSIGNED NOT NULL,

    PRIMARY KEY (`role_id`, `permission_id`),
    INDEX `idx_rp_permission` (`permission_id`),

    CONSTRAINT `fk_rp_role` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_rp_permission` FOREIGN KEY (`permission_id`) REFERENCES `permissions` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `user_roles` (
    `user_id` BIGINT UNSIGNED NOT NULL,
    `role_id` BIGINT UNSIGNED NOT NULL,

    PRIMARY KEY (`user_id`, `role_id`),
    INDEX `idx_ur_role` (`role_id`),

    CONSTRAINT `fk_ur_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_ur_role` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### Record-Level Access (Record Ownership)

CRM commonly restricts data visibility by ownership:
- **Private:** Users see only records they own
- **Team:** Users see records owned by anyone on their team
- **Hierarchy:** Managers see records owned by their direct reports and below
- **Public:** Everyone sees everything

Implement with a teams/territories table:

```sql
CREATE TABLE `teams` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL,
    `description` TEXT NULL DEFAULT NULL,
    `parent_team_id` BIGINT UNSIGNED NULL DEFAULT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (`id`),
    INDEX `idx_teams_parent` (`parent_team_id`),
    CONSTRAINT `fk_teams_parent` FOREIGN KEY (`parent_team_id`) REFERENCES `teams` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `team_members` (
    `team_id` BIGINT UNSIGNED NOT NULL,
    `user_id` BIGINT UNSIGNED NOT NULL,
    `role_in_team` ENUM('member', 'lead', 'manager') NOT NULL DEFAULT 'member',

    PRIMARY KEY (`team_id`, `user_id`),
    INDEX `idx_tm_user` (`user_id`),

    CONSTRAINT `fk_tm_team` FOREIGN KEY (`team_id`) REFERENCES `teams` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_tm_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

Query pattern for team-based visibility:

```sql
-- Get contacts visible to a user based on their teams
SELECT c.* FROM contacts c
WHERE c.deleted_at IS NULL
    AND (
        c.owner_id = :current_user_id  -- own records
        OR c.owner_id IN (              -- team members' records
            SELECT tm2.user_id
            FROM team_members tm1
            INNER JOIN team_members tm2 ON tm2.team_id = tm1.team_id
            WHERE tm1.user_id = :current_user_id
        )
    );
```

For high-traffic CRM systems, cache the set of visible user IDs per user to avoid running this subquery on every request.

## Multi-Tenancy Patterns

### Option 1: Shared Database, Tenant Column (Most Common)

Add a `tenant_id` column to every table and filter every query by it.

```sql
-- Add tenant_id to all CRM tables
ALTER TABLE `accounts` ADD COLUMN `tenant_id` BIGINT UNSIGNED NOT NULL AFTER `id`;
ALTER TABLE `contacts` ADD COLUMN `tenant_id` BIGINT UNSIGNED NOT NULL AFTER `id`;
ALTER TABLE `opportunities` ADD COLUMN `tenant_id` BIGINT UNSIGNED NOT NULL AFTER `id`;
ALTER TABLE `leads` ADD COLUMN `tenant_id` BIGINT UNSIGNED NOT NULL AFTER `id`;
ALTER TABLE `activities` ADD COLUMN `tenant_id` BIGINT UNSIGNED NOT NULL AFTER `id`;

-- Tenants table
CREATE TABLE `tenants` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `domain` VARCHAR(255) NULL DEFAULT NULL,
    `plan` ENUM('free', 'starter', 'professional', 'enterprise') NOT NULL DEFAULT 'free',
    `is_active` TINYINT(1) NOT NULL DEFAULT 1,
    `settings` JSON NULL DEFAULT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (`id`),
    UNIQUE INDEX `uq_tenants_domain` (`domain`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

Critical rules for shared-database multi-tenancy:

1. **Every query includes tenant_id.** No exceptions. A missed filter exposes data across tenants.

2. **tenant_id is the first column in every composite index:**
```sql
-- Correct: tenant_id first
ALTER TABLE `contacts`
    ADD INDEX `idx_contacts_tenant_email` (`tenant_id`, `email`);
ALTER TABLE `contacts`
    ADD INDEX `idx_contacts_tenant_account` (`tenant_id`, `account_id`);

-- Wrong: tenant_id missing or not first
ALTER TABLE `contacts`
    ADD INDEX `idx_contacts_email` (`email`);  -- leaks across tenants
```

3. **Unique constraints include tenant_id:**
```sql
-- Correct: unique per tenant
ALTER TABLE `pipelines`
    ADD UNIQUE INDEX `uq_pipelines_tenant_name` (`tenant_id`, `name`);

-- Wrong: globally unique (tenant A and B can't both have "Sales Pipeline")
ALTER TABLE `pipelines`
    ADD UNIQUE INDEX `uq_pipelines_name` (`name`);
```

4. **Foreign keys should stay within a tenant.** Add application-level checks to ensure cross-table references share the same `tenant_id`.

### Option 2: Separate Schema per Tenant

Each tenant gets their own MySQL schema (database). The application connects to the right schema based on the tenant.

```sql
CREATE DATABASE `crm_tenant_acme`;
CREATE DATABASE `crm_tenant_globex`;
```

Pros:
- Complete isolation — no risk of cross-tenant data leakage
- Easy to back up, restore, or migrate individual tenants
- Per-tenant schema customization is possible

Cons:
- Schema migrations must be applied to every tenant database
- Connection pool management becomes complex
- Harder to run cross-tenant analytics or admin queries
- MySQL has limits on the number of open tables/databases

Best for: Enterprise CRM with strict isolation requirements and fewer than 100 tenants.

### Option 3: Separate Database Server per Tenant

Each tenant gets a dedicated MySQL instance. Maximum isolation but highest operational cost. Only appropriate for very large enterprise customers with regulatory requirements.

## Data Encryption

### Encryption at Rest

Enable InnoDB tablespace encryption:

```sql
-- Enable encryption for a table
ALTER TABLE `contacts` ENCRYPTION='Y';

-- Enable encryption for all new tables by default
SET GLOBAL default_table_encryption = ON;
```

Requires configuring a keyring plugin (e.g., `keyring_file`, `keyring_encrypted_file`, or a KMS-backed keyring like `keyring_aws`).

### Encryption of Sensitive Columns

For columns containing highly sensitive data (SSN, credit card info, health data), consider application-level encryption:

```sql
-- Store encrypted values
ALTER TABLE `contacts`
    ADD COLUMN `ssn_encrypted` VARBINARY(255) NULL DEFAULT NULL,
    ADD COLUMN `ssn_hash` VARCHAR(64) NULL DEFAULT NULL COMMENT 'SHA-256 hash for lookup';
```

Encrypt/decrypt in the application layer using AES-256-GCM or similar. Store a hash for indexed lookups.

**Never store plaintext:** passwords, social security numbers, credit card numbers, bank account numbers, API keys, or authentication tokens.

## Input Validation at Database Level

Use CHECK constraints (MySQL 8.0.16+) to enforce data quality:

```sql
ALTER TABLE `contacts`
    ADD CONSTRAINT `chk_contacts_email` CHECK (
        `email` IS NULL OR `email` REGEXP '^[^@]+@[^@]+\\.[^@]+$'
    ),
    ADD CONSTRAINT `chk_contacts_phone` CHECK (
        `phone` IS NULL OR LENGTH(`phone`) >= 7
    );

ALTER TABLE `opportunities`
    ADD CONSTRAINT `chk_opp_amount_positive` CHECK (
        `amount` IS NULL OR `amount` >= 0
    ),
    ADD CONSTRAINT `chk_opp_probability_range` CHECK (
        `probability` IS NULL OR (`probability` >= 0 AND `probability` <= 100)
    );

ALTER TABLE `accounts`
    ADD CONSTRAINT `chk_accounts_country_code` CHECK (
        `billing_country` IS NULL OR LENGTH(`billing_country`) = 2
    );
```

CHECK constraints are not a substitute for application-level validation, but they provide a last line of defense against bad data.

## MySQL User Privileges

Follow the principle of least privilege for database users:

```sql
-- Application user: read and write to CRM tables only
CREATE USER 'crm_app'@'%' IDENTIFIED BY '<strong_password>';
GRANT SELECT, INSERT, UPDATE, DELETE ON crm.* TO 'crm_app'@'%';

-- Read-only reporting user
CREATE USER 'crm_reports'@'%' IDENTIFIED BY '<strong_password>';
GRANT SELECT ON crm.* TO 'crm_reports'@'%';

-- Migration user: can alter schema
CREATE USER 'crm_migrate'@'%' IDENTIFIED BY '<strong_password>';
GRANT ALL PRIVILEGES ON crm.* TO 'crm_migrate'@'%';

-- Never use root for application connections
```
