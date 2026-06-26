# Dashboard Spec: Email Assistant

This document outlines the companion dashboard for Email Assistant. While the skill works flawlessly in chat, the dashboard provides a premium visual interface for managing your inbox triage, reviewing drafts, and tracking email analytics.

## Core Purpose
"Your agent triages email via chat. Your dashboard is where you review, manage drafts, and see the big picture."

---

## User Interface Requirements

### 1. Inbox Overview (Main View)
- **Triage Feed:** A clean, real-time list of today's triaged emails organized by priority bucket.
  - Color-coded priority indicators: 🔴 Red (Urgent), 🟡 Amber (Action Needed), 🔵 Blue (FYI), ⚫ Gray (Archive)
  - Each row shows: Sender, Subject, Priority, 1-line AI summary, Timestamp
  - Click a row to expand the full email preview and AI analysis
- **Quick Actions:**
  - "Draft Reply" button on each email row → opens draft editor
  - "Archive" button → moves to archive bucket
  - "Escalate" / "De-escalate" → manually adjust priority
  - "Flag as Phishing" → mark suspicious, remove from feed

### 2. Priority Queue
- **Kanban-style board** with four columns: Urgent, Action Needed, FYI, Archive
- Drag-and-drop to reclassify emails
- Count badges on each column header
- VIP emails marked with a ⭐ badge
- Emails awaiting reply show an ⏰ indicator with days waiting

### 3. Draft Queue
- **Card-based interface** for reviewing AI-generated draft replies
- Each card shows: Original email snippet, Draft reply, Tone match score
- Actions per card:
  - ✅ **Approve** — saves to email Drafts folder
  - ✏️ **Edit** — opens inline editor for tweaks
  - ❌ **Reject** — discards the draft
  - 🔄 **Regenerate** — request a new draft with different parameters
- Filters: All, Pending Review, Approved, Rejected

### 4. Sender Analytics
- **Top Senders Chart:** Horizontal bar chart showing who emails you the most (last 30 days)
- **Actionable vs. Noise:** Pie chart breaking down what percentage of each sender's emails are Urgent/Action vs. FYI/Archive
- **Response Time:** Average time between receiving an Action Needed email and your reply
- **VIP Activity:** Dedicated section showing VIP sender volume and response rates
- **Phishing Summary:** Count of flagged phishing attempts with details

### 5. VIP Manager
- **Toggle list** of all configured VIP senders
- Add/remove VIPs with autocomplete from recent senders
- Per-VIP stats: email volume, % urgent, avg response time
- Domain-level vs. individual VIP toggles
- Drag to reorder priority within VIP tier

### 6. Settings Panel
- **Briefing Cadence:** Visual schedule picker (drag time blocks)
- **Quiet Hours:** Toggle with start/end time pickers
- **Classification Tuning:** Adjust keyword weights for Urgent/Archive classification
- **Triage Rules:** Custom rule builder (IF sender contains X AND subject contains Y THEN classify as Z)
- **Data Retention:** Slider for digest retention period (30-365 days)

---

## Design System

### Theme
Premium dark mode, matching the NormieClaw design language.

### Colors
- **Background:** Very dark gray (`#0f0f0f`)
- **Surface:** Dark gray (`#1a1a1a`)
- **Card Background:** Slightly lighter (`#242424`)
- **Primary Action (buttons, links):** Teal (`#14b8a6`)
- **Urgent Accent:** Red (`#ef4444`)
- **Warning Accent:** Orange (`#f97316`)
- **FYI Accent:** Blue (`#3b82f6`)
- **Archive Accent:** Gray (`#6b7280`)
- **VIP Badge:** Gold (`#eab308`)
- **Text Primary:** White (`#f5f5f5`)
- **Text Secondary:** Light gray (`#a3a3a3`)

### Typography
- **Headings:** Inter or system sans-serif, semibold
- **Body:** Inter or system sans-serif, regular
- **Monospace (email previews):** JetBrains Mono or system monospace

### Layout
- Left sidebar navigation: Inbox, Priority Queue, Drafts, Analytics, VIPs, Settings
- Main content area with responsive card/list views
- Top bar: Search, notification bell, quick-check button ("Check inbox now")

---

## Database Schema

For users scaling beyond local JSON files to a persistent database (e.g., Supabase PostgreSQL):

### Tables

```sql
-- Triaged emails
CREATE TABLE email_triage (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users NOT NULL,
    message_id VARCHAR(255) NOT NULL,
    thread_id VARCHAR(255),
    sender_email VARCHAR(255) NOT NULL,
    sender_name VARCHAR(255),
    subject TEXT NOT NULL,
    summary TEXT,
    priority VARCHAR(20) NOT NULL DEFAULT 'fyi', -- urgent, action_needed, fyi, archive
    is_vip BOOLEAN DEFAULT false,
    is_phishing BOOLEAN DEFAULT false,
    is_addressed BOOLEAN DEFAULT false,
    has_attachments BOOLEAN DEFAULT false,
    received_at TIMESTAMP WITH TIME ZONE NOT NULL,
    triaged_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Draft replies
CREATE TABLE email_drafts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users NOT NULL,
    triage_id UUID REFERENCES email_triage(id),
    original_subject TEXT NOT NULL,
    original_sender VARCHAR(255) NOT NULL,
    draft_body TEXT NOT NULL,
    tone_score DECIMAL(3,2), -- 0.00 to 1.00 style match confidence
    status VARCHAR(20) DEFAULT 'pending', -- pending, approved, rejected, sent
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    reviewed_at TIMESTAMP WITH TIME ZONE
);

-- VIP senders
CREATE TABLE vip_senders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users NOT NULL,
    email VARCHAR(255),
    domain VARCHAR(255),
    label VARCHAR(100) NOT NULL,
    escalation VARCHAR(20) DEFAULT 'action_needed', -- urgent, action_needed
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT email_or_domain CHECK (email IS NOT NULL OR domain IS NOT NULL)
);

-- Digest archives
CREATE TABLE email_digests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users NOT NULL,
    digest_date DATE NOT NULL,
    digest_type VARCHAR(10) DEFAULT 'daily', -- daily, weekly
    total_received INTEGER DEFAULT 0,
    urgent_count INTEGER DEFAULT 0,
    action_count INTEGER DEFAULT 0,
    fyi_count INTEGER DEFAULT 0,
    archive_count INTEGER DEFAULT 0,
    phishing_count INTEGER DEFAULT 0,
    content_md TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Row Level Security

```sql
ALTER TABLE email_triage ENABLE ROW LEVEL SECURITY;
ALTER TABLE email_drafts ENABLE ROW LEVEL SECURITY;
ALTER TABLE vip_senders ENABLE ROW LEVEL SECURITY;
ALTER TABLE email_digests ENABLE ROW LEVEL SECURITY;

-- Users can only access their own data (applied to all tables)
CREATE POLICY "Users access own email_triage"
    ON email_triage FOR ALL
    USING (auth.uid() = user_id);

CREATE POLICY "Users access own email_drafts"
    ON email_drafts FOR ALL
    USING (auth.uid() = user_id);

CREATE POLICY "Users access own vip_senders"
    ON vip_senders FOR ALL
    USING (auth.uid() = user_id);

CREATE POLICY "Users access own email_digests"
    ON email_digests FOR ALL
    USING (auth.uid() = user_id);
```

### Indexes

```sql
CREATE INDEX idx_triage_user_priority ON email_triage(user_id, priority);
CREATE INDEX idx_triage_user_received ON email_triage(user_id, received_at DESC);
CREATE INDEX idx_triage_thread ON email_triage(thread_id);
CREATE INDEX idx_drafts_user_status ON email_drafts(user_id, status);
CREATE INDEX idx_vip_user ON vip_senders(user_id);
CREATE INDEX idx_digests_user_date ON email_digests(user_id, digest_date DESC);
```

### Data Security Notes
- **Encryption at rest:** Standard on Supabase/AWS. No additional column-level encryption needed for email summaries.
- **Email body storage:** Store AI-generated summaries, NOT full email bodies. Full content should be fetched from the email provider on demand.
- **PII handling:** Sender emails and names are PII — ensure RLS is enforced and no public API endpoints expose this data.
- **Draft content:** Drafts may contain sensitive business information. Enforce `chmod 600` equivalent access (RLS) and consider TTL-based auto-deletion for rejected drafts.
- **Image/attachment storage:** This dashboard does NOT store email attachments. All attachment access goes through the email provider.
