# Activities and Timeline

A CRM's value comes from recording every interaction with customers. This reference covers designing the activity tracking system — the polymorphic timeline that captures calls, emails, meetings, notes, tasks, and any other touchpoint.

## The Activity Model

### Core Design: Polymorphic Activity Table

Activities can relate to any CRM entity (contact, account, opportunity, lead). Use a polymorphic reference pattern:

```sql
CREATE TABLE `activities` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,

    -- What type of activity
    `activity_type` ENUM('call', 'email', 'meeting', 'note', 'task',
                          'sms', 'chat', 'social', 'document', 'status_change',
                          'stage_change', 'assignment', 'system') NOT NULL,

    -- What entity this activity relates to (polymorphic)
    `entity_type` VARCHAR(50) NOT NULL COMMENT 'contact, account, opportunity, lead',
    `entity_id` BIGINT UNSIGNED NOT NULL,

    -- When it happened
    `activity_date` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),

    -- Who performed the activity
    `user_id` BIGINT UNSIGNED NULL DEFAULT NULL COMMENT 'CRM user who performed this',

    -- Content
    `subject` VARCHAR(500) NULL DEFAULT NULL,
    `body` TEXT NULL DEFAULT NULL,
    `body_html` MEDIUMTEXT NULL DEFAULT NULL COMMENT 'Rich text version for emails',

    -- Activity-specific metadata stored as JSON
    `metadata` JSON NULL DEFAULT NULL,

    -- Duration tracking (for calls, meetings)
    `duration_minutes` INT UNSIGNED NULL DEFAULT NULL,

    -- Task-specific fields
    `is_completed` TINYINT(1) NULL DEFAULT NULL COMMENT 'Only for tasks',
    `due_date` DATETIME NULL DEFAULT NULL COMMENT 'Only for tasks',
    `priority` ENUM('low', 'medium', 'high', 'urgent') NULL DEFAULT NULL,

    -- Associations (an activity can also link to secondary entities)
    `account_id` BIGINT UNSIGNED NULL DEFAULT NULL COMMENT 'Denormalized for fast account timeline queries',
    `contact_id` BIGINT UNSIGNED NULL DEFAULT NULL COMMENT 'Specific contact involved',
    `opportunity_id` BIGINT UNSIGNED NULL DEFAULT NULL COMMENT 'Related deal',

    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `deleted_at` TIMESTAMP NULL DEFAULT NULL,
    `created_by` BIGINT UNSIGNED NULL DEFAULT NULL,

    PRIMARY KEY (`id`),
    INDEX `idx_activities_entity` (`entity_type`, `entity_id`, `activity_date` DESC),
    INDEX `idx_activities_user` (`user_id`, `activity_date` DESC),
    INDEX `idx_activities_type` (`activity_type`, `activity_date` DESC),
    INDEX `idx_activities_account` (`account_id`, `activity_date` DESC),
    INDEX `idx_activities_contact` (`contact_id`, `activity_date` DESC),
    INDEX `idx_activities_opportunity` (`opportunity_id`, `activity_date` DESC),
    INDEX `idx_activities_due_date` (`due_date`, `is_completed`),
    INDEX `idx_activities_deleted_at` (`deleted_at`),

    CONSTRAINT `fk_activities_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_activities_account` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_activities_contact` FOREIGN KEY (`contact_id`) REFERENCES `contacts` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_activities_opportunity` FOREIGN KEY (`opportunity_id`) REFERENCES `opportunities` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_activities_created_by` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### Why Denormalized Association Columns?

The `account_id`, `contact_id`, and `opportunity_id` columns on the activities table are intentionally denormalized. Here is why:

- The most common CRM query is "show me the timeline for account X" — having `account_id` directly on activities avoids a JOIN through the polymorphic entity reference.
- An activity might relate to multiple entities simultaneously (a call with Contact A about Opportunity B at Account C).
- The denormalized FKs enable proper foreign key constraints, which the polymorphic `entity_type` + `entity_id` pattern cannot.

### Metadata by Activity Type

The `metadata` JSON column stores activity-type-specific data. Document the expected structure per type:

**Call:**
```json
{
    "direction": "outbound",
    "phone_number": "+1-555-0123",
    "outcome": "connected",
    "recording_url": "https://...",
    "voicemail_left": false
}
```

**Email:**
```json
{
    "direction": "outbound",
    "from": "rep@company.com",
    "to": ["client@example.com"],
    "cc": [],
    "message_id": "<abc123@mail>",
    "thread_id": "thread_456",
    "has_attachments": true,
    "opened": true,
    "opened_at": "2026-04-01T10:30:00Z",
    "clicked": false
}
```

**Meeting:**
```json
{
    "location": "Zoom",
    "meeting_url": "https://zoom.us/j/123",
    "attendees": [
        {"email": "client@example.com", "status": "accepted"},
        {"email": "rep@company.com", "status": "accepted"}
    ],
    "calendar_event_id": "cal_abc123",
    "outcome": "completed"
}
```

**Stage Change (system-generated):**
```json
{
    "old_stage_id": 3,
    "new_stage_id": 4,
    "old_stage_name": "Proposal",
    "new_stage_name": "Negotiation",
    "pipeline_id": 1
}
```

### Multi-Entity Activity Associations

An activity can relate to multiple entities. For example, a meeting might involve three contacts from two accounts about one opportunity. Use a junction table for additional associations beyond the primary:

```sql
CREATE TABLE `activity_associations` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `activity_id` BIGINT UNSIGNED NOT NULL,
    `entity_type` VARCHAR(50) NOT NULL,
    `entity_id` BIGINT UNSIGNED NOT NULL,
    `association_type` VARCHAR(50) NULL DEFAULT NULL COMMENT 'e.g., attendee, mentioned, related',
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (`id`),
    UNIQUE INDEX `uq_activity_assoc` (`activity_id`, `entity_type`, `entity_id`),
    INDEX `idx_activity_assoc_entity` (`entity_type`, `entity_id`, `created_at` DESC),

    CONSTRAINT `fk_activity_assoc_activity` FOREIGN KEY (`activity_id`)
        REFERENCES `activities` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## Notes

Notes are a subset of activities but are so commonly queried independently that some CRM systems give them their own table:

```sql
CREATE TABLE `notes` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `entity_type` VARCHAR(50) NOT NULL,
    `entity_id` BIGINT UNSIGNED NOT NULL,
    `title` VARCHAR(255) NULL DEFAULT NULL,
    `body` TEXT NOT NULL,
    `is_pinned` TINYINT(1) NOT NULL DEFAULT 0,
    `user_id` BIGINT UNSIGNED NULL DEFAULT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `deleted_at` TIMESTAMP NULL DEFAULT NULL,

    PRIMARY KEY (`id`),
    INDEX `idx_notes_entity` (`entity_type`, `entity_id`, `is_pinned` DESC, `created_at` DESC),
    INDEX `idx_notes_user` (`user_id`),
    FULLTEXT INDEX `ft_notes_search` (`title`, `body`),

    CONSTRAINT `fk_notes_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## Tasks

Tasks deserve their own table when the CRM has a dedicated task management workflow (assigned tasks, due dates, reminders, recurring tasks).

```sql
CREATE TABLE `tasks` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `title` VARCHAR(500) NOT NULL,
    `description` TEXT NULL DEFAULT NULL,
    `status` ENUM('open', 'in_progress', 'completed', 'cancelled') NOT NULL DEFAULT 'open',
    `priority` ENUM('low', 'medium', 'high', 'urgent') NOT NULL DEFAULT 'medium',
    `due_date` DATETIME NULL DEFAULT NULL,
    `completed_at` DATETIME NULL DEFAULT NULL,

    -- Who is responsible
    `assignee_id` BIGINT UNSIGNED NULL DEFAULT NULL,
    `assigned_by_id` BIGINT UNSIGNED NULL DEFAULT NULL,

    -- What entity is this task related to
    `entity_type` VARCHAR(50) NULL DEFAULT NULL,
    `entity_id` BIGINT UNSIGNED NULL DEFAULT NULL,

    -- Recurrence (optional)
    `is_recurring` TINYINT(1) NOT NULL DEFAULT 0,
    `recurrence_rule` VARCHAR(255) NULL DEFAULT NULL COMMENT 'iCal RRULE format',

    -- Reminders
    `reminder_at` DATETIME NULL DEFAULT NULL,

    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `deleted_at` TIMESTAMP NULL DEFAULT NULL,
    `created_by` BIGINT UNSIGNED NULL DEFAULT NULL,

    PRIMARY KEY (`id`),
    INDEX `idx_tasks_assignee` (`assignee_id`, `status`, `due_date`),
    INDEX `idx_tasks_entity` (`entity_type`, `entity_id`),
    INDEX `idx_tasks_due_date` (`due_date`, `status`),
    INDEX `idx_tasks_status` (`status`),
    INDEX `idx_tasks_reminder` (`reminder_at`, `status`),
    INDEX `idx_tasks_deleted_at` (`deleted_at`),

    CONSTRAINT `fk_tasks_assignee` FOREIGN KEY (`assignee_id`) REFERENCES `users` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_tasks_assigned_by` FOREIGN KEY (`assigned_by_id`) REFERENCES `users` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_tasks_created_by` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## Attachments / Files

Documents attached to any CRM entity:

```sql
CREATE TABLE `attachments` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `entity_type` VARCHAR(50) NOT NULL,
    `entity_id` BIGINT UNSIGNED NOT NULL,
    `filename` VARCHAR(255) NOT NULL,
    `file_path` VARCHAR(1000) NOT NULL COMMENT 'S3 key or filesystem path',
    `file_size` BIGINT UNSIGNED NOT NULL COMMENT 'Size in bytes',
    `mime_type` VARCHAR(100) NOT NULL,
    `uploaded_by` BIGINT UNSIGNED NULL DEFAULT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `deleted_at` TIMESTAMP NULL DEFAULT NULL,

    PRIMARY KEY (`id`),
    INDEX `idx_attachments_entity` (`entity_type`, `entity_id`),
    INDEX `idx_attachments_uploaded_by` (`uploaded_by`),

    CONSTRAINT `fk_attachments_uploaded_by` FOREIGN KEY (`uploaded_by`)
        REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

Design notes:
- Never store file contents (BLOBs) in MySQL. Store files in object storage (S3, GCS) and keep only the path/key in the database.
- `mime_type` enables the UI to display previews or choose appropriate icons.
- `file_size` allows enforcing storage quotas without querying the file system.

## Building the Unified Timeline Query

The timeline view for any CRM entity aggregates activities, notes, and system events:

```sql
-- Unified timeline for an account
(
    SELECT
        a.id,
        'activity' AS record_type,
        a.activity_type AS event_type,
        a.subject AS title,
        a.body AS description,
        a.activity_date AS event_date,
        a.user_id,
        u.first_name AS user_first_name,
        u.last_name AS user_last_name
    FROM activities a
    LEFT JOIN users u ON u.id = a.user_id
    WHERE a.account_id = :account_id AND a.deleted_at IS NULL
)
UNION ALL
(
    SELECT
        n.id,
        'note' AS record_type,
        'note' AS event_type,
        n.title,
        LEFT(n.body, 200) AS description,
        n.created_at AS event_date,
        n.user_id,
        u.first_name,
        u.last_name
    FROM notes n
    LEFT JOIN users u ON u.id = n.user_id
    WHERE n.entity_type = 'account' AND n.entity_id = :account_id AND n.deleted_at IS NULL
)
ORDER BY event_date DESC
LIMIT 50;
```

For performance, consider a materialized timeline view updated by application events or triggers, especially for accounts with thousands of activities.
