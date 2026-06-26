# Custom Fields and Flexibility

CRM systems must accommodate user-defined fields. Sales teams want to track industry-specific data, marketing wants custom segmentation attributes, and every client has unique requirements. This reference covers the three main approaches to custom fields in MySQL 8 and when to use each.

## Approach 1: Entity-Attribute-Value (EAV)

The EAV pattern stores custom field definitions and values in separate tables rather than adding columns to the entity table.

### Schema

```sql
-- Define available custom fields
CREATE TABLE `custom_field_definitions` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `entity_type` VARCHAR(50) NOT NULL COMMENT 'e.g., contact, account, opportunity, lead',
    `field_name` VARCHAR(100) NOT NULL,
    `field_label` VARCHAR(200) NOT NULL,
    `field_type` ENUM('text', 'number', 'decimal', 'boolean', 'date', 'datetime',
                       'select', 'multi_select', 'email', 'url', 'phone') NOT NULL,
    `is_required` TINYINT(1) NOT NULL DEFAULT 0,
    `default_value` VARCHAR(500) NULL DEFAULT NULL,
    `options` JSON NULL DEFAULT NULL COMMENT 'For select/multi_select: ["opt1","opt2","opt3"]',
    `validation_rules` JSON NULL DEFAULT NULL COMMENT '{"min_length":1,"max_length":500,"regex":"..."}',
    `display_order` INT UNSIGNED NOT NULL DEFAULT 0,
    `is_active` TINYINT(1) NOT NULL DEFAULT 1,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (`id`),
    UNIQUE INDEX `uq_cfd_entity_field` (`entity_type`, `field_name`),
    INDEX `idx_cfd_entity_type` (`entity_type`, `is_active`, `display_order`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Store custom field values (one row per entity-field pair)
CREATE TABLE `custom_field_values` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `field_definition_id` BIGINT UNSIGNED NOT NULL,
    `entity_type` VARCHAR(50) NOT NULL,
    `entity_id` BIGINT UNSIGNED NOT NULL,
    `value_text` TEXT NULL DEFAULT NULL,
    `value_number` DECIMAL(20, 6) NULL DEFAULT NULL,
    `value_boolean` TINYINT(1) NULL DEFAULT NULL,
    `value_date` DATE NULL DEFAULT NULL,
    `value_datetime` DATETIME(3) NULL DEFAULT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (`id`),
    UNIQUE INDEX `uq_cfv_entity_field` (`field_definition_id`, `entity_type`, `entity_id`),
    INDEX `idx_cfv_entity` (`entity_type`, `entity_id`),
    INDEX `idx_cfv_value_text` (`field_definition_id`, `value_text`(100)),
    INDEX `idx_cfv_value_number` (`field_definition_id`, `value_number`),
    INDEX `idx_cfv_value_date` (`field_definition_id`, `value_date`),

    CONSTRAINT `fk_cfv_definition` FOREIGN KEY (`field_definition_id`)
        REFERENCES `custom_field_definitions` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### Querying EAV Data

Pivoting EAV data into columns for display:

```sql
-- Get all custom fields for a specific contact
SELECT
    cfd.field_name,
    cfd.field_label,
    cfd.field_type,
    COALESCE(cfv.value_text, cfv.value_number, cfv.value_boolean,
             cfv.value_date, cfv.value_datetime) AS value
FROM custom_field_definitions cfd
LEFT JOIN custom_field_values cfv
    ON cfv.field_definition_id = cfd.id
    AND cfv.entity_type = 'contact'
    AND cfv.entity_id = :contact_id
WHERE cfd.entity_type = 'contact'
    AND cfd.is_active = 1
ORDER BY cfd.display_order;

-- Filter contacts by a custom field value
SELECT c.*
FROM contacts c
INNER JOIN custom_field_values cfv
    ON cfv.entity_type = 'contact' AND cfv.entity_id = c.id
INNER JOIN custom_field_definitions cfd
    ON cfd.id = cfv.field_definition_id
WHERE cfd.field_name = 'preferred_language'
    AND cfv.value_text = 'Spanish'
    AND c.deleted_at IS NULL;
```

### EAV Pros and Cons

**Pros:**
- Unlimited custom fields without schema changes
- Users can create fields at runtime
- No ALTER TABLE needed (no table locks, no downtime)
- Clean separation between core schema and customizations

**Cons:**
- Complex queries — pivoting and filtering require JOINs
- Harder to enforce data types at the database level
- Reporting becomes more complex
- Cannot use standard SQL constraints (NOT NULL, CHECK, UNIQUE) on values
- Performance degrades with heavy filtering across multiple custom fields

**Best for:** SaaS CRM where tenants define their own fields, systems with 50+ custom fields, fields that change frequently.

## Approach 2: JSON Columns

Store custom fields as a JSON document directly on the entity table.

### Schema

```sql
ALTER TABLE `contacts`
    ADD COLUMN `custom_fields` JSON NULL DEFAULT NULL,
    ADD CONSTRAINT `chk_contacts_custom_fields` CHECK (
        `custom_fields` IS NULL OR JSON_VALID(`custom_fields`)
    );
```

### Example Data

```json
{
    "preferred_language": "Spanish",
    "shirt_size": "L",
    "nps_score": 8,
    "renewal_date": "2026-03-15",
    "interests": ["AI", "cloud", "security"],
    "custom_notes": "Prefers morning calls"
}
```

### Indexing JSON for Performance

```sql
-- Generated column approach (most reliable)
ALTER TABLE `contacts`
    ADD COLUMN `cf_preferred_language` VARCHAR(50)
        GENERATED ALWAYS AS (`custom_fields` ->> '$.preferred_language') STORED,
    ADD INDEX `idx_contacts_cf_language` (`cf_preferred_language`);

-- Functional index approach (MySQL 8.0.13+)
ALTER TABLE `contacts`
    ADD INDEX `idx_contacts_cf_nps` ((
        CAST(`custom_fields` ->> '$.nps_score' AS SIGNED)
    ));

-- Multi-valued index for arrays (MySQL 8.0.17+)
ALTER TABLE `contacts`
    ADD INDEX `idx_contacts_cf_interests` ((
        CAST(`custom_fields` -> '$.interests' AS CHAR(100) ARRAY)
    ));
```

### Querying JSON Custom Fields

```sql
-- Simple filter
SELECT * FROM contacts
WHERE custom_fields ->> '$.preferred_language' = 'Spanish'
    AND deleted_at IS NULL;

-- Numeric comparison
SELECT * FROM contacts
WHERE CAST(custom_fields ->> '$.nps_score' AS SIGNED) >= 8
    AND deleted_at IS NULL;

-- Array membership
SELECT * FROM contacts
WHERE 'AI' MEMBER OF (custom_fields -> '$.interests')
    AND deleted_at IS NULL;

-- Check if a field exists
SELECT * FROM contacts
WHERE JSON_CONTAINS_PATH(custom_fields, 'one', '$.renewal_date')
    AND deleted_at IS NULL;

-- Update a single field without replacing the entire document
UPDATE contacts
SET custom_fields = JSON_SET(
    COALESCE(custom_fields, '{}'),
    '$.nps_score', 9,
    '$.last_survey_date', '2026-04-01'
)
WHERE id = :contact_id;
```

### JSON Pros and Cons

**Pros:**
- Simple to implement — just one column
- Read performance is good for fetching a single record's custom data
- MySQL 8 partial update optimization for JSON_SET (no full document rewrite)
- Natural fit for application frameworks with JSON serialization
- Flexible schema — any structure without ALTER TABLE

**Cons:**
- Cannot enforce field-level constraints (required fields, data types, allowed values)
- Indexing requires explicit generated columns or functional indexes
- Complex cross-record filtering on JSON fields is slower than regular columns
- No built-in field definitions or validation at database level
- JSON documents should stay under a few KB — avoid storing large blobs

**Best for:** Small to moderate number of custom fields (under 20), systems where custom fields are rarely filtered or sorted, metadata and preferences storage.

## Approach 3: Hybrid (Recommended for Most CRMs)

Combine fixed columns for well-known fields with JSON for truly custom/flexible data.

### Schema Pattern

```sql
CREATE TABLE `contacts` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,

    -- Fixed, well-known columns (indexed, typed, constrained)
    `first_name` VARCHAR(100) NOT NULL,
    `last_name` VARCHAR(100) NOT NULL,
    `email` VARCHAR(255) NULL DEFAULT NULL,
    `phone` VARCHAR(30) NULL DEFAULT NULL,
    `account_id` BIGINT UNSIGNED NULL DEFAULT NULL,
    `lifecycle_stage` ENUM('subscriber','lead','mql','sql','opportunity','customer','evangelist','other') NOT NULL DEFAULT 'subscriber',

    -- JSON for custom/flexible fields
    `custom_fields` JSON NULL DEFAULT NULL,

    -- Generated columns to index frequently queried custom fields
    `cf_preferred_language` VARCHAR(50)
        GENERATED ALWAYS AS (`custom_fields` ->> '$.preferred_language') STORED,

    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `deleted_at` TIMESTAMP NULL DEFAULT NULL,

    PRIMARY KEY (`id`),
    INDEX `idx_contacts_cf_language` (`cf_preferred_language`),
    -- ... other indexes
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### When to Promote a JSON Field to a Column

A custom field should graduate from JSON to a dedicated column when:
- It is queried in WHERE or ORDER BY clauses frequently
- It needs database-level constraints (NOT NULL, UNIQUE, CHECK, FK)
- It is used in JOINs
- It appears in reports or dashboards
- It is present on more than 80% of records
- It has a fixed, well-defined data type

### Decision Matrix

| Factor | Use Fixed Column | Use JSON | Use EAV |
|--------|-----------------|----------|---------|
| Known at design time | Yes | — | — |
| Used in WHERE/JOIN | Yes | Maybe (with gen col) | Possible but slow |
| Needs FK constraint | Yes | No | No |
| User-defined at runtime | — | Yes (small count) | Yes (large count) |
| Per-tenant schema | — | Yes | Yes |
| 50+ custom fields | — | — | Yes |
| Reporting/analytics | Yes | With gen columns | Complex |

### Metadata for JSON Custom Fields

Even with the JSON approach, maintain a field definitions table so the UI knows what fields exist and how to render them:

```sql
CREATE TABLE `custom_field_metadata` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `entity_type` VARCHAR(50) NOT NULL,
    `json_path` VARCHAR(200) NOT NULL COMMENT 'Path in JSON document, e.g. $.preferred_language',
    `field_label` VARCHAR(200) NOT NULL,
    `field_type` ENUM('text','number','decimal','boolean','date','datetime',
                       'select','multi_select','email','url','phone') NOT NULL,
    `options` JSON NULL DEFAULT NULL,
    `is_required` TINYINT(1) NOT NULL DEFAULT 0,
    `display_order` INT UNSIGNED NOT NULL DEFAULT 0,
    `is_active` TINYINT(1) NOT NULL DEFAULT 1,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (`id`),
    UNIQUE INDEX `uq_cfm_entity_path` (`entity_type`, `json_path`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

This gives you the flexibility of JSON storage with the discoverability of EAV field definitions.
