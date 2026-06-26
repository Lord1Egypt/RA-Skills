# Supercharged Memory — Dashboard Companion Kit

Spec for the Dashboard Builder skill to consume. Generates a visual interface for browsing, searching, and exploring the agent's memory system.

---

## Overview

The Memory Dashboard gives users a visual interface to see exactly what their AI knows about them. Browse memories chronologically, search across all layers, visualize topic clusters, and monitor system health — all from a clean web UI.

---

## Components

### 1. Memory Browser

**Purpose:** Search and browse all stored memories with filters.

**UI Elements:**
- Search bar (full-text, powered by QMD or direct file search)
- Filter chips: Topic, Person, Project, Preference, Decision, All
- Results list with:
  - Memory content (truncated to 2 lines, expandable)
  - Source file path (e.g., `memory/2026-03-07.md`)
  - Date captured
  - Category badge (colored pill: preference=blue, decision=green, person=purple, project=orange, fact=gray)
- Pagination (20 results per page)
- "Edit" button per entry → opens inline editor to modify the memory
- "Delete" button per entry → removes from source file (with confirmation)

**Data Source:** Parse all files in `memory/` directory + `MEMORY.md`. Each bullet point or section is a "memory entry."

**Search:** If QMD is available, use `qmd query` for search. Fallback: grep across files.

### 2. Memory Timeline

**Purpose:** Chronological feed showing when memories were formed.

**UI Elements:**
- Vertical timeline (newest at top)
- Each entry shows:
  - Date and time
  - Memory content (brief)
  - Category icon
  - Source (daily notes, MEMORY.md, semantic file)
- Date range picker to filter timeline
- "Today" / "This Week" / "This Month" quick filters
- Expandable entries — click to see full context from source file

**Data Source:** Parse `memory/YYYY-MM-DD.md` files. Extract timestamps from `## Session Start — HH:MM` headers and individual entries.

### 3. Topic Clusters

**Purpose:** Visual overview of what the AI knows organized by topic density.

**UI Elements:**
- Bubble chart or treemap layout
- Each bubble represents a topic (derived from semantic files + MEMORY.md sections)
- Bubble size = number of memories in that topic
- Bubble color = category (using the category color scheme from Memory Browser)
- Click a bubble → filtered view of all memories in that topic
- Topics with no semantic file show as smaller, lighter bubbles

**Data Source:**
- Primary: `memory/semantic/*.md` file names and sizes
- Secondary: `MEMORY.md` section headers (## Preferences, ## Active Projects, etc.)
- Tertiary: Frequency analysis of daily notes (most mentioned topics)

**Clustering Logic:**
1. Each semantic file = 1 topic cluster
2. Each MEMORY.md section = 1 cluster
3. Size = character count of all content in that cluster
4. Orphan entries (in daily notes but no semantic file) grouped under "Uncategorized"

### 4. Stats Panel

**Purpose:** Quick-glance health and usage metrics.

**UI Elements:**
- Card grid (2x2 or responsive)
- Cards:
  - **Total Memories** — count of all entries across all files
  - **Memory Freshness** — "Last updated X hours ago" with green/yellow/red indicator
  - **MEMORY.md Size** — current chars / target chars with progress bar
  - **QMD Collections** — count and last reindex time
- Optional (if Vector DB enabled):
  - **Vector Count** — total vectors in Qdrant
  - **Capture Status** — last Mem0 capture time

**Data Source:** `memory/health-state.json` + direct file stats

---

## Design System

### Colors
```
Background:     #0F172A (slate-900)
Surface:        #1E293B (slate-800)
Surface Hover:  #334155 (slate-700)
Border:         #475569 (slate-600)
Text Primary:   #F8FAFC (slate-50)
Text Secondary: #94A3B8 (slate-400)
Accent:         #38BDF8 (sky-400)
Success:        #4ADE80 (green-400)
Warning:        #FBBF24 (amber-400)
Error:          #F87171 (red-400)
```

### Category Colors
```
Preference:     #60A5FA (blue-400)
Decision:       #4ADE80 (green-400)
Person:         #C084FC (purple-400)
Project:        #FB923C (orange-400)
Fact:           #94A3B8 (slate-400)
Lesson:         #FBBF24 (amber-400)
```

### Typography
```
Font Family:    Inter, system-ui, sans-serif
Headings:       600 weight
Body:           400 weight
Monospace:      JetBrains Mono, monospace (for file paths and code)
```

### Spacing
```
Card padding:   24px
Card gap:       16px
Section gap:    32px
Border radius:  12px (cards), 8px (buttons), 20px (pills)
```

---

## DB Schema (Supabase — Optional)

For users who want persistent dashboard state and cross-device access. This is NOT required for the memory system itself — it's only for the dashboard UI.

### Table: `memories`
```sql
CREATE TABLE memories (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id TEXT NOT NULL,
  content TEXT NOT NULL,
  category TEXT CHECK (category IN ('preference', 'decision', 'person', 'project', 'fact', 'lesson')),
  source_file TEXT NOT NULL,
  source_date DATE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  last_accessed TIMESTAMPTZ,
  embedding VECTOR(1536),  -- optional, for semantic search in dashboard
  metadata JSONB DEFAULT '{}'
);

CREATE INDEX idx_memories_user ON memories(user_id);
CREATE INDEX idx_memories_category ON memories(user_id, category);
CREATE INDEX idx_memories_date ON memories(user_id, source_date DESC);
CREATE INDEX idx_memories_search ON memories USING gin(to_tsvector('english', content));
```

### Table: `memory_stats`
```sql
CREATE TABLE memory_stats (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id TEXT NOT NULL,
  date DATE NOT NULL DEFAULT CURRENT_DATE,
  total_memories INTEGER DEFAULT 0,
  memory_md_chars INTEGER DEFAULT 0,
  qmd_collections INTEGER DEFAULT 0,
  vector_count INTEGER DEFAULT 0,
  last_reindex TIMESTAMPTZ,
  last_consolidation TIMESTAMPTZ,
  alerts JSONB DEFAULT '[]',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, date)
);
```

### RLS Policies
```sql
-- Users can only see their own memories
ALTER TABLE memories ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users see own memories" ON memories
  FOR ALL USING (auth.uid()::text = user_id);

ALTER TABLE memory_stats ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users see own stats" ON memory_stats
  FOR ALL USING (auth.uid()::text = user_id);
```

### Sync Strategy
The dashboard reads directly from workspace files (primary) and optionally syncs to Supabase for:
- Cross-device dashboard access
- Historical stats tracking
- Full-text search via Postgres GIN index
- Optional embedding-based search in the dashboard UI

Sync runs on a schedule (e.g., hourly) or on-demand when the user opens the dashboard.

---

## Implementation Notes

- **Rendering:** Dashboard Builder should generate a self-contained HTML file or a Next.js page component
- **No server required for basic use:** The dashboard can read files directly from the workspace via the agent
- **Supabase is optional:** Dashboard works without it (reads files directly). Supabase adds persistence and cross-device access.
- **Responsive:** Must work on mobile (the stats panel and memory browser are the most useful on mobile)
- **Accessible:** WCAG 2.1 AA minimum. Sufficient color contrast on dark background. Focus indicators on interactive elements.
