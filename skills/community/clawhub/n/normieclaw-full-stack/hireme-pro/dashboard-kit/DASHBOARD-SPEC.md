# HireMe Pro — Dashboard Kit Build Specification

**Purpose:** A visual web application for tracking job applications, managing resume versions, and organizing interview prep. Designed as a companion to the HireMe Pro agent skill.

**Stack:** Next.js 14+ (App Router), Supabase (PostgreSQL), Tailwind CSS, shadcn/ui

**Design Philosophy:** "Clean & Calming." Job hunting is stressful. Use generous whitespace, soft borders (`rounded-xl`), and a calming color palette. No aggressive alerts or anxiety-inducing red badges. Think: reassuring progress, not pressure.

---

## Color Palette

| Token | Value | Usage |
|-------|-------|-------|
| `--primary` | `#2563eb` (blue-600) | Primary actions, active states |
| `--primary-light` | `#eff6ff` (blue-50) | Backgrounds, hover states |
| `--success` | `#059669` (emerald-600) | Offers, positive outcomes |
| `--warning` | `#d97706` (amber-600) | Follow-up reminders, pending items |
| `--danger` | `#94a3b8` (slate-400) | Rejections (muted, not red — reduce sting) |
| `--background` | `#f8fafc` (slate-50) | Page background |
| `--card` | `#ffffff` | Card backgrounds |
| `--text` | `#1e293b` (slate-800) | Primary text |
| `--muted` | `#64748b` (slate-500) | Secondary text, metadata |

---

## Database Schema (Supabase)

### `users`
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  name TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);
```

### `resumes`
```sql
CREATE TABLE resumes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  version_label TEXT, -- e.g., "Master", "TechCorp - Director", "Startup Generic"
  template_id TEXT NOT NULL DEFAULT 'modern', -- clean, modern, executive, creative
  json_content JSONB NOT NULL, -- Full resume-data.json structure
  is_master BOOLEAN DEFAULT false,
  target_company TEXT,
  target_role TEXT,
  pdf_url TEXT, -- Supabase Storage URL
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_resumes_user ON resumes(user_id);
```

### `applications`
```sql
CREATE TABLE applications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  company TEXT NOT NULL,
  role TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'saved',
    -- ENUM: saved, applied, interviewing, offer, rejected, withdrawn, ghosted
  resume_id UUID REFERENCES resumes(id) ON DELETE SET NULL,
  job_description TEXT,
  job_url TEXT,
  cover_letter TEXT,
  salary_range TEXT,
  source TEXT, -- LinkedIn, Indeed, Referral, Company Site, etc.
  contact_name TEXT,
  contact_email TEXT,
  date_applied TIMESTAMPTZ,
  follow_up_date TIMESTAMPTZ,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_applications_user ON applications(user_id);
CREATE INDEX idx_applications_status ON applications(status);
```

### `prep_sessions`
```sql
CREATE TABLE prep_sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  application_id UUID REFERENCES applications(id) ON DELETE CASCADE,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  company_research TEXT, -- Markdown notes on company
  questions JSONB NOT NULL DEFAULT '[]',
    -- Array of { question, category, suggested_answer, user_notes, confidence }
  mock_results JSONB, -- Array of { question, user_answer, feedback, score }
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_prep_sessions_app ON prep_sessions(application_id);
```

### `activity_log`
```sql
CREATE TABLE activity_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  application_id UUID REFERENCES applications(id) ON DELETE SET NULL,
  action TEXT NOT NULL, -- applied, status_changed, interview_scheduled, follow_up_sent, etc.
  details JSONB,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_activity_user ON activity_log(user_id);
CREATE INDEX idx_activity_date ON activity_log(created_at);
```

---

## Row Level Security (RLS)

Enable RLS on ALL tables. Users can only access their own data:

```sql
ALTER TABLE resumes ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users own their resumes" ON resumes
  FOR ALL USING (auth.uid() = user_id);

ALTER TABLE applications ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users own their applications" ON applications
  FOR ALL USING (auth.uid() = user_id);

ALTER TABLE prep_sessions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users own their prep sessions" ON prep_sessions
  FOR ALL USING (auth.uid() = user_id);

ALTER TABLE activity_log ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users own their activity" ON activity_log
  FOR ALL USING (auth.uid() = user_id);
```

---

## Component Breakdown

### 1. Application Tracker (Kanban Board)

**Route:** `/applications`

**Component:** `KanbanBoard`

Drag-and-drop columns for application statuses:
- **Saved** (slate-200 header) — Jobs bookmarked but not yet applied
- **Applied** (blue-100 header) — Submitted applications
- **Interviewing** (amber-100 header) — In active interview process
- **Offer** (emerald-100 header) — Received offers
- **Rejected** (slate-100 header, muted styling) — Rejections
- **Ghosted** (slate-100 header) — No response past follow-up window

Each card shows:
- Company name (bold)
- Role title
- Days since applied (subtle counter)
- Follow-up indicator (amber dot if follow-up date has passed)
- Source icon (LinkedIn, Indeed, etc.)

**Drag behavior:** Dragging a card between columns updates the `status` field and logs to `activity_log`.

**Quick actions on card click:**
- View/edit details
- Open job posting (external link)
- View linked resume version
- View cover letter
- Start interview prep
- Add notes

### 2. Resume Vault

**Route:** `/resumes`

**Component:** `ResumeVault`

Grid view of all resume versions:
- Card per resume showing: title, template preview thumbnail, target company/role, last updated
- "Master" badge on the master resume
- Actions: **Preview** (PDF render), **Duplicate** (create tailored copy), **Edit** (opens editor), **Download PDF**, **Delete** (with confirmation)
- **Create New** button → starts from master or blank
- Filter by: template, target company, date range

### 3. Job Matcher (Split Pane)

**Route:** `/match`

**Component:** `JobMatcher`

Split-pane view:
- **Left panel:** Select a saved resume version from dropdown
- **Right panel:** Paste a job description (or select from saved applications)
- **Center:** Match analysis results
  - Overall match percentage (circular progress indicator, calming blue)
  - Strong matches (✅ green check)
  - Partial matches (🔄 amber)
  - Gaps (⚠️ muted, not alarming)
  - Missing ATS keywords (listed with suggestion to incorporate)
- **Action button:** "Create Tailored Version" → generates a new resume entry pre-filled with suggested changes

### 4. Interview Prep Hub

**Route:** `/prep/:applicationId`

**Component:** `PrepSession`

- Company research notes (rich text editor, markdown support)
- Question bank organized by category tabs: Behavioral, Technical, Situational, Company-Specific
- Each question card shows: question text, why they'll ask it, suggested answer framework, user's notes, confidence level (1-5 stars)
- **Mock Mode:** Button to start a mock interview — shows one question at a time, records user's answer (text input), provides AI feedback
- Timer for mock interview practice (optional, for time-pressure simulation)

### 5. Dashboard Home

**Route:** `/`

**Component:** `DashboardHome`

Overview stats:
- Total active applications (excluding rejected/withdrawn)
- Applications this week
- Interviews scheduled
- Response rate (applications → interviews)
- Follow-ups due today

Activity timeline:
- Recent actions (applied, status changed, prep session created)
- Follow-up reminders (highlighted in amber)

Quick action buttons:
- "New Application" → opens add application modal
- "Upload Resume" → opens resume intake
- "Paste Job Description" → opens job matcher

### 6. Settings

**Route:** `/settings`

- Profile (name, email)
- Default template preference
- Follow-up reminder days (default: 7)
- Export all data (JSON download)
- Delete all data (with confirmation, GDPR-compliant)

---

## API Routes

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/api/applications` | List all applications (filterable by status) |
| POST | `/api/applications` | Create new application |
| PATCH | `/api/applications/:id` | Update application (status, notes, etc.) |
| DELETE | `/api/applications/:id` | Delete application |
| GET | `/api/resumes` | List all resume versions |
| POST | `/api/resumes` | Create new resume version |
| PATCH | `/api/resumes/:id` | Update resume content |
| DELETE | `/api/resumes/:id` | Delete resume version |
| POST | `/api/resumes/:id/pdf` | Generate PDF for a resume version |
| GET | `/api/prep/:applicationId` | Get prep session for an application |
| POST | `/api/prep` | Create prep session |
| PATCH | `/api/prep/:id` | Update prep session |
| GET | `/api/activity` | Get activity log (paginated) |
| POST | `/api/match` | Run job match analysis |

---

## Deployment

- **Hosting:** Vercel (Next.js optimized)
- **Database:** Supabase (managed PostgreSQL)
- **Storage:** Supabase Storage for PDF files
- **Auth:** Supabase Auth (email + magic link — no passwords to remember)
- **Environment Variables:**
  - `NEXT_PUBLIC_SUPABASE_URL`
  - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
  - `SUPABASE_SERVICE_ROLE_KEY` (server-side only)

---

## Mobile Responsiveness

- Kanban board collapses to a list view on mobile (< 768px)
- Resume vault switches from grid to single-column cards
- Job matcher stacks panels vertically
- All touch targets minimum 44px
- Bottom navigation bar on mobile

---

*This spec is designed to be handed to any developer (or AI coding agent) and produce a complete, deployable dashboard without additional context.*
