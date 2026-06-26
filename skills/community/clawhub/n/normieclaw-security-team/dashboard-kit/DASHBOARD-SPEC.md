# Dashboard Spec: Security Team

This document provides a complete specification for Dashboard Builder to consume and render a Security Operations Center (SOC) dashboard for the Security Team skill.

## Core Purpose

"Your agent runs silent audits. Your dashboard shows the bigger picture — trends, health at a glance, and issue management in one panel."

---

## Design System

### Theme: SOC Dark Mode
- **Background:** Deep black `#0a0a0a`
- **Surface/Card:** Dark gray `#141414`
- **Surface elevated:** `#1a1a1a`
- **Border/Divider:** `#262626`
- **Text primary:** `#e5e5e5`
- **Text secondary:** `#a3a3a3`
- **Healthy/Passed (green):** `#10b981`
- **Warning/Medium (amber):** `#f59e0b`
- **Critical/Alert (red):** `#ef4444`
- **Info/Accent (blue):** `#3b82f6`
- **Font:** `"JetBrains Mono", "Fira Code", monospace` for data/scores, `"Inter", system-ui, sans-serif` for labels and body text
- **Border radius:** `8px` (cards), `4px` (badges/tags)
- **Shadows:** Subtle, dark — `0 1px 3px rgba(0,0,0,0.5)`

### Vibe
Think: a security operations center at 2 AM. Dense, information-rich, dark. Green means safe, red means act now. Every pixel earns its place.

---

## Components

### 1. Overall Security Score (Hero Card)

A large, centered score display at the top.

- **Current score** displayed as a large number (e.g., "7.2") with `/10`
- **Score ring:** Circular progress indicator, color-coded:
  - 0-4: red fill
  - 5-7: amber fill  
  - 8-10: green fill
- **Trend arrow:** ↑ ↓ → compared to 7-day average
- **Last scan timestamp:** "Last scan: 2h ago" in muted text
- **Sub-scores row:** Three smaller score badges below: 🛡️ Security: 6.5 | ⚙️ Platform: 8.0 | 🧠 Memory: 9.0

### 2. Security Score Timeline (Line Chart)

A 30-day line chart showing overall score over time.

- **X-axis:** Dates (last 30 days)
- **Y-axis:** Score (0-10)
- **Lines:** Overall score (white/primary), with optional toggleable lines for each council (security=blue, platform=amber, memory=green)
- **Background bands:** Subtle horizontal bands for score zones — red (0-4), amber (5-7), green (8-10)
- **Tooltip:** Hover shows date, score, and finding count
- **Data source:** `security_audits` table, ordered by `run_date`

### 3. System Health Grid

A dense grid of micro status cards — one per monitored endpoint/service.

- **Card layout:** 3-4 columns, each card ~120px wide
- **Per card:**
  - Service/domain name (truncated if long)
  - Status dot: 🟢 green (up) / 🔴 red (down) / 🟡 amber (degraded)
  - Response time or status code (small text)
  - Last checked timestamp
- **Data source:** Latest `security_audits.raw_log` → platform council findings, cross-referenced with config services/domains

### 4. Active Issues Table

Sortable, filterable table of all known issues.

| Column | Type | Notes |
|--------|------|-------|
| Severity | Badge | Red "CRITICAL" or Amber "MEDIUM" |
| Council | Badge | "Security" / "Platform" / "Memory" |
| Description | Text | Truncated with expand-on-click |
| Location | Code text | File path or URL |
| First Seen | Date | When first detected |
| Last Seen | Date | Most recent occurrence |
| Status | Badge | "Open" (red outline) / "Accepted Risk" (gray) |
| Actions | Buttons | "Accept Risk" / "Reopen" |

- **Filters:** Severity dropdown, Council dropdown, Status dropdown
- **Sort:** Default by severity (CRITICAL first), then by first_seen
- **Data source:** `security_issues` table

### 5. Memory Stats Panel

A sidebar or bottom panel showing memory system vitals.

- **Total Vectors:** Number with trend (e.g., "15,412 ↑ +23 today")
- **Last Reindex:** Timestamp with freshness indicator (green if <24h, amber if <72h, red if >72h)
- **MEMORY.md Size:** In KB with threshold bar (green under 50KB, amber above)
- **Daily Notes Streak:** "Last 7 days: ✓✓✓✓✓✗✓" — visual streak indicator
- **Data source:** `security_audits.raw_log` → memory council data

### 6. Scan History (Compact Log)

A scrollable log of recent audit runs.

- **Per entry:** Timestamp | Overall score badge | Finding count | "Silent" or "Alerted" indicator
- **Expandable:** Click to see full finding list for that scan
- **Data source:** `security_audits` table, ordered by `run_date` DESC, limited to 50

---

## Database Schema (Supabase/PostgreSQL)

```sql
-- Audit run history
CREATE TABLE security_audits (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users NOT NULL,
  run_date TIMESTAMPTZ DEFAULT NOW(),
  overall_score DECIMAL(4,2),
  security_score DECIMAL(4,2),
  platform_score DECIMAL(4,2),
  memory_score DECIMAL(4,2),
  findings_count INTEGER DEFAULT 0,
  critical_count INTEGER DEFAULT 0,
  medium_count INTEGER DEFAULT 0,
  alerted BOOLEAN DEFAULT false,
  raw_log JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Individual security issues with lifecycle tracking
CREATE TABLE security_issues (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users NOT NULL,
  council TEXT NOT NULL CHECK (council IN ('security', 'platform', 'memory')),
  severity TEXT NOT NULL CHECK (severity IN ('CRITICAL', 'MEDIUM')),
  issue_hash TEXT NOT NULL,
  description TEXT NOT NULL,
  location TEXT,
  remediation TEXT,
  status TEXT DEFAULT 'open' CHECK (status IN ('open', 'resolved', 'accepted_risk')),
  accepted_reason TEXT,
  first_seen TIMESTAMPTZ DEFAULT NOW(),
  last_seen TIMESTAMPTZ DEFAULT NOW(),
  resolved_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, issue_hash)
);

-- Indexes for common queries
CREATE INDEX idx_audits_user_date ON security_audits(user_id, run_date DESC);
CREATE INDEX idx_issues_user_status ON security_issues(user_id, status);
CREATE INDEX idx_issues_user_severity ON security_issues(user_id, severity);
```

### Row Level Security

```sql
ALTER TABLE security_audits ENABLE ROW LEVEL SECURITY;
ALTER TABLE security_issues ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users view own audits"
  ON security_audits FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users insert own audits"
  ON security_audits FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users view own issues"
  ON security_issues FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users insert own issues"
  ON security_issues FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users update own issues"
  ON security_issues FOR UPDATE USING (auth.uid() = user_id);
```

---

## API Endpoints (if building a Next.js dashboard)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/security/audits` | GET | List audit history (paginated) |
| `/api/security/audits/latest` | GET | Get most recent audit |
| `/api/security/issues` | GET | List issues (filterable by status, severity, council) |
| `/api/security/issues/[id]/accept` | POST | Accept risk with reason |
| `/api/security/issues/[id]/reopen` | POST | Reopen an accepted risk |
| `/api/security/trends` | GET | Aggregated score data for charting (30/90 day) |
| `/api/security/ingest` | POST | Receive audit JSON from agent (webhook) |

---

## Responsive Behavior

- **Desktop (1200px+):** Full layout — hero score + timeline top row, health grid + issues table middle, memory panel sidebar
- **Tablet (768-1199px):** Stack timeline below hero, health grid 2-column, issues table scrollable
- **Mobile (< 768px):** Everything stacked. Hero score simplified. Issues as expandable cards instead of table.

---

## Integration Notes

- The agent writes audit results to local JSON files (`security-team/audit-history/`). A webhook endpoint (`/api/security/ingest`) can receive this data and persist it to Supabase for the dashboard.
- If no Supabase is configured, the dashboard can read directly from local JSON files (static mode).
- Chart library recommendation: Chart.js (lightweight) or Recharts (React-native).
