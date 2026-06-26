# Core CRM Entities

This reference covers the foundational tables that every CRM system needs. These entities form the backbone of customer relationship management: tracking who your customers are, how you acquire them, and what business you do with them.

## Entity Overview

A well-designed CRM revolves around these core entities and their relationships:

- **Accounts** (companies/organizations) — the central entity everything connects to
- **Contacts** (people) — individuals associated with accounts
- **Leads** (unqualified prospects) — potential customers not yet converted
- **Opportunities** (deals) — revenue-bearing objects tied to accounts
- **Products** — what you sell, referenced by opportunities
- **Pipeline Stages** — the stages a deal moves through
- **Users** (CRM users/sales reps) — the people who use the CRM system

## Table Designs

### Users (CRM System Users)

The users table represents sales reps, managers, admins — anyone who logs into the CRM. This is not the same as contacts or customers.

```sql
CREATE TABLE `users` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `email` VARCHAR(255) NOT NULL,
    `password_hash` VARCHAR(255) NOT NULL,
    `first_name` VARCHAR(100) NOT NULL,
    `last_name` VARCHAR(100) NOT NULL,
    `phone` VARCHAR(30) NULL DEFAULT NULL,
    `avatar_url` VARCHAR(500) NULL DEFAULT NULL,
    `role` ENUM('admin', 'manager', 'sales_rep', 'support_agent', 'read_only') NOT NULL DEFAULT 'sales_rep',
    `is_active` TINYINT(1) NOT NULL DEFAULT 1,
    `timezone` VARCHAR(50) NOT NULL DEFAULT 'UTC',
    `last_login_at` DATETIME NULL DEFAULT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `deleted_at` TIMESTAMP NULL DEFAULT NULL,

    PRIMARY KEY (`id`),
    UNIQUE INDEX `uq_users_email` (`email`),
    INDEX `idx_users_role` (`role`),
    INDEX `idx_users_is_active` (`is_active`),
    INDEX `idx_users_deleted_at` (`deleted_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

Design notes:
- `email` is unique and serves as the login identifier. Never use email as a primary key — use a surrogate BIGINT.
- `password_hash` stores bcrypt/argon2 output, never plaintext.
- `role` uses ENUM for a fixed set of roles. If you need more flexible RBAC, see `security-and-multitenancy.md`.
- `is_active` is separate from `deleted_at`. A user can be deactivated but still exist for historical reference.

### Accounts (Companies / Organizations)

Accounts are the primary entity in B2B CRM. In B2C, this may be optional or represent household groupings.

```sql
CREATE TABLE `accounts` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `domain` VARCHAR(255) NULL DEFAULT NULL,
    `industry` VARCHAR(100) NULL DEFAULT NULL,
    `company_size` ENUM('1-10', '11-50', '51-200', '201-500', '501-1000', '1001-5000', '5000+') NULL DEFAULT NULL,
    `annual_revenue` DECIMAL(15, 2) NULL DEFAULT NULL,
    `type` ENUM('prospect', 'customer', 'partner', 'vendor', 'competitor', 'other') NOT NULL DEFAULT 'prospect',
    `status` ENUM('active', 'inactive', 'churned') NOT NULL DEFAULT 'active',
    `phone` VARCHAR(30) NULL DEFAULT NULL,
    `website` VARCHAR(500) NULL DEFAULT NULL,
    `description` TEXT NULL DEFAULT NULL,

    -- Address fields (consider a separate addresses table for multi-address support)
    `billing_address_line1` VARCHAR(255) NULL DEFAULT NULL,
    `billing_address_line2` VARCHAR(255) NULL DEFAULT NULL,
    `billing_city` VARCHAR(100) NULL DEFAULT NULL,
    `billing_state` VARCHAR(100) NULL DEFAULT NULL,
    `billing_postal_code` VARCHAR(20) NULL DEFAULT NULL,
    `billing_country` VARCHAR(2) NULL DEFAULT NULL COMMENT 'ISO 3166-1 alpha-2',

    -- Ownership and hierarchy
    `owner_id` BIGINT UNSIGNED NULL DEFAULT NULL COMMENT 'Sales rep who owns this account',
    `parent_account_id` BIGINT UNSIGNED NULL DEFAULT NULL COMMENT 'For subsidiaries/divisions',

    -- Integration
    `external_id` VARCHAR(255) NULL DEFAULT NULL COMMENT 'ID in external system (ERP, billing, etc.)',
    `external_source` VARCHAR(100) NULL DEFAULT NULL COMMENT 'Name of external system',

    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `deleted_at` TIMESTAMP NULL DEFAULT NULL,
    `created_by` BIGINT UNSIGNED NULL DEFAULT NULL,
    `updated_by` BIGINT UNSIGNED NULL DEFAULT NULL,

    PRIMARY KEY (`id`),
    INDEX `idx_accounts_name` (`name`),
    INDEX `idx_accounts_domain` (`domain`),
    INDEX `idx_accounts_type` (`type`),
    INDEX `idx_accounts_status` (`status`),
    INDEX `idx_accounts_owner_id` (`owner_id`),
    INDEX `idx_accounts_parent_account_id` (`parent_account_id`),
    INDEX `idx_accounts_industry` (`industry`),
    INDEX `idx_accounts_deleted_at` (`deleted_at`),
    INDEX `idx_accounts_external` (`external_source`, `external_id`),

    CONSTRAINT `fk_accounts_owner` FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_accounts_parent` FOREIGN KEY (`parent_account_id`) REFERENCES `accounts` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_accounts_created_by` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_accounts_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

Design notes:
- `parent_account_id` enables account hierarchies (parent company → subsidiaries). Query these with MySQL 8 recursive CTEs.
- `billing_country` uses ISO 3166-1 alpha-2 codes (US, GB, DE). Consider a lookup table for countries if you need names and metadata.
- `owner_id` establishes the primary sales rep responsible. Many CRM systems also use a team/territory assignment table.
- `external_id` + `external_source` together form a composite key for integration deduplication.

### Contacts (People)

Contacts are individual people, typically associated with an account.

```sql
CREATE TABLE `contacts` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `account_id` BIGINT UNSIGNED NULL DEFAULT NULL,
    `first_name` VARCHAR(100) NOT NULL,
    `last_name` VARCHAR(100) NOT NULL,
    `email` VARCHAR(255) NULL DEFAULT NULL,
    `secondary_email` VARCHAR(255) NULL DEFAULT NULL,
    `phone` VARCHAR(30) NULL DEFAULT NULL,
    `mobile_phone` VARCHAR(30) NULL DEFAULT NULL,
    `job_title` VARCHAR(150) NULL DEFAULT NULL,
    `department` VARCHAR(100) NULL DEFAULT NULL,
    `linkedin_url` VARCHAR(500) NULL DEFAULT NULL,
    `is_primary` TINYINT(1) NOT NULL DEFAULT 0 COMMENT 'Primary contact for the account',
    `lifecycle_stage` ENUM('subscriber', 'lead', 'mql', 'sql', 'opportunity', 'customer', 'evangelist', 'other') NOT NULL DEFAULT 'subscriber',
    `lead_source` VARCHAR(100) NULL DEFAULT NULL,
    `status` ENUM('active', 'inactive', 'bounced', 'unsubscribed', 'do_not_contact') NOT NULL DEFAULT 'active',

    -- Communication preferences
    `email_opt_in` TINYINT(1) NOT NULL DEFAULT 0,
    `sms_opt_in` TINYINT(1) NOT NULL DEFAULT 0,
    `preferred_language` VARCHAR(10) NULL DEFAULT NULL COMMENT 'IETF language tag, e.g. en-US',

    -- Mailing address
    `mailing_address_line1` VARCHAR(255) NULL DEFAULT NULL,
    `mailing_address_line2` VARCHAR(255) NULL DEFAULT NULL,
    `mailing_city` VARCHAR(100) NULL DEFAULT NULL,
    `mailing_state` VARCHAR(100) NULL DEFAULT NULL,
    `mailing_postal_code` VARCHAR(20) NULL DEFAULT NULL,
    `mailing_country` VARCHAR(2) NULL DEFAULT NULL,

    -- Ownership
    `owner_id` BIGINT UNSIGNED NULL DEFAULT NULL,

    -- Integration
    `external_id` VARCHAR(255) NULL DEFAULT NULL,
    `external_source` VARCHAR(100) NULL DEFAULT NULL,

    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `deleted_at` TIMESTAMP NULL DEFAULT NULL,
    `created_by` BIGINT UNSIGNED NULL DEFAULT NULL,
    `updated_by` BIGINT UNSIGNED NULL DEFAULT NULL,

    PRIMARY KEY (`id`),
    INDEX `idx_contacts_account_id` (`account_id`),
    INDEX `idx_contacts_email` (`email`),
    INDEX `idx_contacts_name` (`last_name`, `first_name`),
    INDEX `idx_contacts_owner_id` (`owner_id`),
    INDEX `idx_contacts_lifecycle_stage` (`lifecycle_stage`),
    INDEX `idx_contacts_status` (`status`),
    INDEX `idx_contacts_lead_source` (`lead_source`),
    INDEX `idx_contacts_deleted_at` (`deleted_at`),
    INDEX `idx_contacts_external` (`external_source`, `external_id`),

    CONSTRAINT `fk_contacts_account` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_contacts_owner` FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_contacts_created_by` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_contacts_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

Design notes:
- `account_id` is nullable because some contacts (individuals, freelancers) may not belong to an account.
- `email` is not UNIQUE because a person might appear in the system via different sources. Deduplication is an application-level concern. If you want uniqueness, add a unique index.
- `lifecycle_stage` tracks where this contact is in the marketing/sales funnel.
- `is_primary` marks the main contact at an account. Enforce only-one-primary per account in application logic or with a filtered unique index.

### Leads (Unqualified Prospects)

Leads are potential contacts that have not yet been qualified. Some CRM systems merge leads into the contacts table with a status flag; others keep them separate. A separate table is cleaner when lead qualification is a distinct workflow.

```sql
CREATE TABLE `leads` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `first_name` VARCHAR(100) NOT NULL,
    `last_name` VARCHAR(100) NOT NULL,
    `email` VARCHAR(255) NULL DEFAULT NULL,
    `phone` VARCHAR(30) NULL DEFAULT NULL,
    `company_name` VARCHAR(255) NULL DEFAULT NULL,
    `job_title` VARCHAR(150) NULL DEFAULT NULL,
    `website` VARCHAR(500) NULL DEFAULT NULL,

    -- Lead qualification
    `source` VARCHAR(100) NULL DEFAULT NULL COMMENT 'e.g., website, trade_show, referral, cold_call, linkedin, advertisement',
    `source_detail` VARCHAR(255) NULL DEFAULT NULL COMMENT 'Specific campaign, event name, or referrer',
    `status` ENUM('new', 'contacted', 'qualified', 'unqualified', 'converted', 'lost') NOT NULL DEFAULT 'new',
    `rating` ENUM('hot', 'warm', 'cold') NULL DEFAULT NULL,
    `score` INT UNSIGNED NULL DEFAULT NULL COMMENT 'Numeric lead score from 0-100',

    -- Conversion tracking
    `converted_at` DATETIME NULL DEFAULT NULL,
    `converted_contact_id` BIGINT UNSIGNED NULL DEFAULT NULL,
    `converted_account_id` BIGINT UNSIGNED NULL DEFAULT NULL,
    `converted_opportunity_id` BIGINT UNSIGNED NULL DEFAULT NULL,

    -- Ownership
    `owner_id` BIGINT UNSIGNED NULL DEFAULT NULL,

    -- Integration
    `external_id` VARCHAR(255) NULL DEFAULT NULL,
    `external_source` VARCHAR(100) NULL DEFAULT NULL,

    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `deleted_at` TIMESTAMP NULL DEFAULT NULL,
    `created_by` BIGINT UNSIGNED NULL DEFAULT NULL,
    `updated_by` BIGINT UNSIGNED NULL DEFAULT NULL,

    PRIMARY KEY (`id`),
    INDEX `idx_leads_email` (`email`),
    INDEX `idx_leads_status` (`status`),
    INDEX `idx_leads_source` (`source`),
    INDEX `idx_leads_owner_id` (`owner_id`),
    INDEX `idx_leads_rating` (`rating`),
    INDEX `idx_leads_score` (`score`),
    INDEX `idx_leads_converted_at` (`converted_at`),
    INDEX `idx_leads_deleted_at` (`deleted_at`),
    INDEX `idx_leads_created_at` (`created_at`),
    INDEX `idx_leads_external` (`external_source`, `external_id`),

    CONSTRAINT `fk_leads_owner` FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_leads_converted_contact` FOREIGN KEY (`converted_contact_id`) REFERENCES `contacts` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_leads_converted_account` FOREIGN KEY (`converted_account_id`) REFERENCES `accounts` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_leads_created_by` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_leads_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

Design notes:
- When a lead is converted, set `status = 'converted'`, record `converted_at`, and link to the newly created contact, account, and/or opportunity.
- `score` supports numeric lead scoring (0-100). The scoring rules live in application logic; the database just stores the result.
- `source` + `source_detail` together tell you where the lead came from and the specific campaign or event.

### Pipelines and Pipeline Stages

Most CRMs support multiple sales pipelines (e.g., "New Business", "Renewals", "Upsell"), each with their own stages.

```sql
CREATE TABLE `pipelines` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL,
    `description` TEXT NULL DEFAULT NULL,
    `is_default` TINYINT(1) NOT NULL DEFAULT 0,
    `is_active` TINYINT(1) NOT NULL DEFAULT 1,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `deleted_at` TIMESTAMP NULL DEFAULT NULL,

    PRIMARY KEY (`id`),
    INDEX `idx_pipelines_is_active` (`is_active`),
    INDEX `idx_pipelines_deleted_at` (`deleted_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `pipeline_stages` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `pipeline_id` BIGINT UNSIGNED NOT NULL,
    `name` VARCHAR(100) NOT NULL,
    `display_order` INT UNSIGNED NOT NULL DEFAULT 0,
    `probability` DECIMAL(5, 2) NULL DEFAULT NULL COMMENT 'Win probability percentage, e.g. 75.00',
    `is_won` TINYINT(1) NOT NULL DEFAULT 0 COMMENT 'True for closed-won stage',
    `is_lost` TINYINT(1) NOT NULL DEFAULT 0 COMMENT 'True for closed-lost stage',
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (`id`),
    INDEX `idx_pipeline_stages_pipeline_id` (`pipeline_id`),
    INDEX `idx_pipeline_stages_display_order` (`pipeline_id`, `display_order`),

    CONSTRAINT `fk_pipeline_stages_pipeline` FOREIGN KEY (`pipeline_id`) REFERENCES `pipelines` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

Design notes:
- `display_order` controls the visual left-to-right order of stages in a kanban view.
- `probability` is used to calculate weighted pipeline value (opportunity amount × stage probability).
- `is_won` and `is_lost` are mutually exclusive flags that mark terminal stages. CHECK constraints can enforce this.

### Opportunities (Deals)

Opportunities represent potential revenue. They are the lifeblood of CRM reporting.

```sql
CREATE TABLE `opportunities` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `account_id` BIGINT UNSIGNED NOT NULL,
    `pipeline_id` BIGINT UNSIGNED NOT NULL,
    `stage_id` BIGINT UNSIGNED NOT NULL,
    `amount` DECIMAL(15, 2) NULL DEFAULT NULL COMMENT 'Deal value in base currency',
    `currency` VARCHAR(3) NOT NULL DEFAULT 'USD' COMMENT 'ISO 4217 currency code',
    `probability` DECIMAL(5, 2) NULL DEFAULT NULL COMMENT 'Override of stage probability if set',
    `expected_close_date` DATE NULL DEFAULT NULL,
    `actual_close_date` DATE NULL DEFAULT NULL,
    `type` ENUM('new_business', 'renewal', 'upsell', 'cross_sell', 'other') NULL DEFAULT NULL,
    `priority` ENUM('low', 'medium', 'high', 'critical') NOT NULL DEFAULT 'medium',
    `loss_reason` VARCHAR(255) NULL DEFAULT NULL,
    `description` TEXT NULL DEFAULT NULL,
    `next_step` VARCHAR(500) NULL DEFAULT NULL,

    -- Ownership
    `owner_id` BIGINT UNSIGNED NULL DEFAULT NULL,

    -- Primary contact on the deal
    `primary_contact_id` BIGINT UNSIGNED NULL DEFAULT NULL,

    -- Integration
    `external_id` VARCHAR(255) NULL DEFAULT NULL,
    `external_source` VARCHAR(100) NULL DEFAULT NULL,

    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `deleted_at` TIMESTAMP NULL DEFAULT NULL,
    `created_by` BIGINT UNSIGNED NULL DEFAULT NULL,
    `updated_by` BIGINT UNSIGNED NULL DEFAULT NULL,

    PRIMARY KEY (`id`),
    INDEX `idx_opportunities_account_id` (`account_id`),
    INDEX `idx_opportunities_pipeline_id` (`pipeline_id`),
    INDEX `idx_opportunities_stage_id` (`stage_id`),
    INDEX `idx_opportunities_owner_id` (`owner_id`),
    INDEX `idx_opportunities_expected_close` (`expected_close_date`),
    INDEX `idx_opportunities_amount` (`amount`),
    INDEX `idx_opportunities_type` (`type`),
    INDEX `idx_opportunities_deleted_at` (`deleted_at`),
    INDEX `idx_opportunities_created_at` (`created_at`),
    INDEX `idx_opportunities_external` (`external_source`, `external_id`),
    -- Composite index for pipeline reporting
    INDEX `idx_opportunities_pipeline_stage` (`pipeline_id`, `stage_id`, `deleted_at`),

    CONSTRAINT `fk_opportunities_account` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`id`) ON DELETE RESTRICT,
    CONSTRAINT `fk_opportunities_pipeline` FOREIGN KEY (`pipeline_id`) REFERENCES `pipelines` (`id`) ON DELETE RESTRICT,
    CONSTRAINT `fk_opportunities_stage` FOREIGN KEY (`stage_id`) REFERENCES `pipeline_stages` (`id`) ON DELETE RESTRICT,
    CONSTRAINT `fk_opportunities_owner` FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_opportunities_primary_contact` FOREIGN KEY (`primary_contact_id`) REFERENCES `contacts` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_opportunities_created_by` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_opportunities_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

Design notes:
- `account_id` is NOT NULL and uses ON DELETE RESTRICT. Opportunities should never exist without an account, and deleting an account with active deals should be blocked.
- `amount` uses DECIMAL(15,2) for precision. Never use FLOAT or DOUBLE for monetary values.
- `currency` stores the ISO 4217 code. Multi-currency CRMs need a currency conversion table or integrate with a rate API.
- The composite index on `(pipeline_id, stage_id, deleted_at)` optimizes the most common CRM query: "show me all active deals by pipeline stage."

### Opportunity Contact Roles (Junction Table)

Deals involve multiple contacts playing different roles (decision maker, influencer, end user, etc.).

```sql
CREATE TABLE `opportunity_contacts` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `opportunity_id` BIGINT UNSIGNED NOT NULL,
    `contact_id` BIGINT UNSIGNED NOT NULL,
    `role` VARCHAR(100) NULL DEFAULT NULL COMMENT 'e.g., decision_maker, influencer, champion, end_user, evaluator',
    `is_primary` TINYINT(1) NOT NULL DEFAULT 0,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (`id`),
    UNIQUE INDEX `uq_opportunity_contacts` (`opportunity_id`, `contact_id`),
    INDEX `idx_opportunity_contacts_contact_id` (`contact_id`),

    CONSTRAINT `fk_opp_contacts_opportunity` FOREIGN KEY (`opportunity_id`) REFERENCES `opportunities` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_opp_contacts_contact` FOREIGN KEY (`contact_id`) REFERENCES `contacts` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### Products and Opportunity Line Items

```sql
CREATE TABLE `products` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `sku` VARCHAR(100) NULL DEFAULT NULL,
    `description` TEXT NULL DEFAULT NULL,
    `unit_price` DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    `currency` VARCHAR(3) NOT NULL DEFAULT 'USD',
    `is_active` TINYINT(1) NOT NULL DEFAULT 1,
    `product_category` VARCHAR(100) NULL DEFAULT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `deleted_at` TIMESTAMP NULL DEFAULT NULL,

    PRIMARY KEY (`id`),
    INDEX `idx_products_sku` (`sku`),
    INDEX `idx_products_is_active` (`is_active`),
    INDEX `idx_products_category` (`product_category`),
    INDEX `idx_products_deleted_at` (`deleted_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `opportunity_line_items` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `opportunity_id` BIGINT UNSIGNED NOT NULL,
    `product_id` BIGINT UNSIGNED NOT NULL,
    `quantity` DECIMAL(10, 2) NOT NULL DEFAULT 1.00,
    `unit_price` DECIMAL(15, 2) NOT NULL COMMENT 'Price at time of quote, may differ from product list price',
    `discount_percent` DECIMAL(5, 2) NOT NULL DEFAULT 0.00,
    `total_price` DECIMAL(15, 2) GENERATED ALWAYS AS (
        `quantity` * `unit_price` * (1 - `discount_percent` / 100)
    ) STORED,
    `description` VARCHAR(500) NULL DEFAULT NULL,
    `sort_order` INT UNSIGNED NOT NULL DEFAULT 0,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (`id`),
    INDEX `idx_opp_line_items_opportunity_id` (`opportunity_id`),
    INDEX `idx_opp_line_items_product_id` (`product_id`),

    CONSTRAINT `fk_opp_line_items_opportunity` FOREIGN KEY (`opportunity_id`) REFERENCES `opportunities` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_opp_line_items_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

Design notes:
- `unit_price` on line items is separate from the product's `unit_price` because the quoted price may differ from the list price (discounts, negotiated rates, pricing at time of quote).
- `total_price` is a STORED generated column — MySQL computes it automatically and it can be indexed if needed.
- `discount_percent` stores the percentage discount. Some systems prefer storing `discount_amount` instead. Choose one convention and be consistent.

### Tags (Flexible Categorization)

Tags provide lightweight, user-defined categorization across multiple entity types.

```sql
CREATE TABLE `tags` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL,
    `color` VARCHAR(7) NULL DEFAULT NULL COMMENT 'Hex color code, e.g. #FF5733',
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (`id`),
    UNIQUE INDEX `uq_tags_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `taggables` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `tag_id` BIGINT UNSIGNED NOT NULL,
    `taggable_type` VARCHAR(50) NOT NULL COMMENT 'e.g., account, contact, lead, opportunity',
    `taggable_id` BIGINT UNSIGNED NOT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (`id`),
    UNIQUE INDEX `uq_taggables` (`tag_id`, `taggable_type`, `taggable_id`),
    INDEX `idx_taggables_target` (`taggable_type`, `taggable_id`),

    CONSTRAINT `fk_taggables_tag` FOREIGN KEY (`tag_id`) REFERENCES `tags` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

Design notes:
- The `taggables` table uses a polymorphic pattern — `taggable_type` + `taggable_id` point to any entity. This avoids creating a separate junction table for every entity type.
- The tradeoff is that MySQL cannot enforce a foreign key on the polymorphic reference. Application logic must validate that `taggable_id` exists in the referenced table.
- The composite unique index prevents duplicate tag assignments on the same entity.
