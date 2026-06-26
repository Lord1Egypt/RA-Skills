# NoteTaker Pro — Dashboard Companion Kit

**Upsell:** "Works great in chat alone. Add a Dashboard Starter Kit for the full visual experience."

---

## Design Language

- **Theme:** Premium dark mode
- **Background:** Deep charcoal (`#1a1a2e`, `#16213e`)
- **Primary accent:** Vibrant teal (`#14b8a6`) — interactive elements, links, tag pills
- **Alert accent:** Sharp orange (`#f97316`) — priority badges, action item counts
- **Text:** White (`#f8fafc`) primary, muted gray (`#94a3b8`) secondary
- **Cards:** Slightly lighter charcoal (`#1e293b`) with subtle border (`#334155`)
- **Font:** Inter (headings), JetBrains Mono (metadata/tags)

---

## Dashboard Pages

### 1. Notes Browser (Main View)

**Layout:** Two-column — sidebar (tags/categories) + main content (note list)

**Features:**
- **Search bar** — Anchored at top, full width. Placeholder: "Search your notes..." Filters as you type.
- **Note cards** — Each card shows: title, date, category badge, tag pills, 2-line content preview, priority indicator (colored dot), action item count (if any).
- **Sort controls** — By: date created (default), date updated, title (A-Z), priority.
- **Filter bar** — Category dropdown, tag multi-select, date range picker, source type filter (text/voice/photo).
- **Infinite scroll** — Load 20 notes at a time.

### 2. Tag Cloud & Category Sidebar

**Tag Cloud:**
- Visual tag cloud where size = usage frequency.
- Click a tag → filter notes list to that tag.
- Color: teal pills with white text.

**Category List:**
- Vertical list below tag cloud.
- Each category shows name + note count.
- Click → filter notes list.
- Icon per category (customizable).

### 3. Note Detail View

**Opens when clicking a note card:**
- Full note content rendered as rich Markdown.
- Embedded images displayed inline (for visual captures).
- Original photo shown alongside extracted text (side-by-side on desktop, stacked on mobile).
- Action items as interactive checkboxes.
- Related notes shown as linked cards at bottom.
- Edit button → opens note in edit mode.
- Metadata footer: created date, updated date, source type, word count.

### 4. Activity Stats

**Top-of-page stats bar:**
- Total notes (lifetime count)
- Notes this week (with +/- vs last week)
- Most active category
- Top 5 tags

**Weekly activity chart:**
- Bar chart showing notes captured per day (last 4 weeks).
- Teal bars, orange highlight for today.

### 5. Quick-Add Modal

**Triggered by floating "+" button:**
- Title field (optional — auto-generated if blank)
- Content textarea (Markdown supported)
- Category dropdown
- Tag input (comma-separated, auto-suggest from existing tags)
- Priority selector (low/normal/high)
- Template dropdown (loads template fields when selected)
- Save button → creates note via API, updates dashboard in real-time.

---

## Database Schema (Supabase/Postgres)

### Table: `notes`

| Column | Type | Description |
|--------|------|-------------|
| `id` | `text` PRIMARY KEY | Format: `note_YYYYMMDD_NNN` |
| `user_id` | `uuid` NOT NULL | References auth.users |
| `title` | `text` NOT NULL | Note title (≤ 200 chars) |
| `content_summary` | `text` | Short summary (≤ 500 chars) |
| `content_full` | `text` | Full note content |
| `category` | `text` NOT NULL | Category slug |
| `tags` | `text[]` DEFAULT '{}' | Array of tag strings |
| `priority` | `text` DEFAULT 'normal' | low, normal, high |
| `source_type` | `text` DEFAULT 'text' | text, voice, paste, photo |
| `source_image_url` | `text` | URL to stored image (if visual capture) |
| `action_items` | `jsonb` DEFAULT '[]' | Array of action item objects |
| `related_notes` | `text[]` DEFAULT '{}' | Array of related note IDs |
| `enhanced` | `boolean` DEFAULT false | Whether AI enhancement was applied |
| `word_count` | `integer` DEFAULT 0 | Content word count |
| `created_at` | `timestamptz` DEFAULT now() | Creation timestamp |
| `updated_at` | `timestamptz` DEFAULT now() | Last update timestamp |

**Indexes:**
```sql
CREATE INDEX idx_notes_user_id ON notes(user_id);
CREATE INDEX idx_notes_category ON notes(category);
CREATE INDEX idx_notes_created_at ON notes(created_at DESC);
CREATE INDEX idx_notes_priority ON notes(priority);
CREATE INDEX idx_notes_tags ON notes USING GIN(tags);
CREATE INDEX idx_notes_search ON notes USING GIN(to_tsvector('english', title || ' ' || coalesce(content_full, '')));
```

### Table: `tags`

| Column | Type | Description |
|--------|------|-------------|
| `id` | `serial` PRIMARY KEY | Auto-increment |
| `user_id` | `uuid` NOT NULL | References auth.users |
| `tag_name` | `text` NOT NULL | Tag string (e.g., `#meeting-notes`) |
| `usage_count` | `integer` DEFAULT 1 | Number of notes using this tag |
| `last_used_at` | `timestamptz` DEFAULT now() | Last time tag was applied |

**Unique constraint:** `(user_id, tag_name)`

### Table: `note_templates`

| Column | Type | Description |
|--------|------|-------------|
| `id` | `serial` PRIMARY KEY | Auto-increment |
| `user_id` | `uuid` NOT NULL | References auth.users |
| `name` | `text` NOT NULL | Template name |
| `fields` | `jsonb` NOT NULL | Array of field names |
| `is_builtin` | `boolean` DEFAULT false | Built-in vs custom |
| `created_at` | `timestamptz` DEFAULT now() | Creation timestamp |

---

## Row Level Security (RLS)

```sql
-- Users can only see their own notes
ALTER TABLE notes ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users see own notes" ON notes
  FOR ALL USING (auth.uid() = user_id);

ALTER TABLE tags ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users see own tags" ON tags
  FOR ALL USING (auth.uid() = user_id);

ALTER TABLE note_templates ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users see own templates" ON note_templates
  FOR ALL USING (auth.uid() = user_id);
```

---

## API Endpoints (Next.js API Routes)

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/api/notes` | List notes (paginated, filterable) |
| GET | `/api/notes/[id]` | Get single note |
| POST | `/api/notes` | Create note |
| PUT | `/api/notes/[id]` | Update note |
| DELETE | `/api/notes/[id]` | Delete note (soft delete) |
| GET | `/api/notes/search?q=` | Full-text search |
| GET | `/api/tags` | List all tags with counts |
| GET | `/api/stats` | Activity stats & aggregations |
| GET | `/api/templates` | List templates |
| POST | `/api/templates` | Create custom template |

---

## Sync Architecture

**Chat → Dashboard flow:**
1. Agent captures note in chat → writes to local `data/notes/` JSON files.
2. Sync script reads local JSON → upserts to Supabase via REST API.
3. Dashboard reads from Supabase in real-time.

**Dashboard → Chat flow:**
1. User creates/edits note in dashboard → writes to Supabase.
2. Agent reads from local files (primary) + can query Supabase for dashboard-created notes.

**Sync frequency:** On-demand (triggered after each note capture) or periodic (every 5 minutes via background process).

---

*This spec is designed for the NormieClaw Dashboard Builder integration. The dashboard is a separate purchase ($9.99) that plugs into the NoteTaker Pro data layer.*
