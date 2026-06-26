# SQLite Content Calendar Schema

This document outlines the expected schema for the SQLite database used by Mad SEO Manager to track the content lifecycle (`./shared/mad_seo.db`).

## Table: `content_calendar`

The `content_calendar` table stores all planned, drafted, and published content across the entire pipeline.

### Schema Definition
```sql
CREATE TABLE IF NOT EXISTS content_calendar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    wp_category_id INTEGER,
    funnel_stage TEXT NOT NULL CHECK (funnel_stage IN ('TOFU', 'MOFU', 'BOFU')),
    status TEXT NOT NULL CHECK (status IN ('Idea', 'Draft', 'Review', 'Scheduled', 'Published', 'Repurposed')),
    scheduled_date DATE,
    wp_post_id INTEGER,
    published_url TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Required Agent Operations

#### 1. Inserting New Ideas (Via `mad_seo:plan_strategy`)
When planning content, the agent should insert records with status `Idea` and the correct category ID.
```sql
INSERT INTO content_calendar (title, wp_category_id, funnel_stage, status, scheduled_date)
VALUES ('Title', 10, 'TOFU', 'Idea', '2026-05-01');
```

#### 2. Updating Status (Via WordPress Integration)
When a post is created as a draft on WordPress, store the `wp_post_id`.
```sql
UPDATE content_calendar 
SET status = 'Draft', wp_post_id = [WP_ID], updated_at = CURRENT_TIMESTAMP 
WHERE id = [ID];
```

#### 3. Reviewing the Calendar
The agent can query this database at any time to review what needs to be drafted next or what gaps exist in the funnel.
