# Home Fix-It: Companion Dashboard Spec

## Overview
A clean, utilitarian companion dashboard for homeowners to track maintenance, repair history, tool inventory, and appliance warranties.

## Design System
- **Vibe:** Home Depot meets Apple. High-contrast readability, utilitarian.
- **Color Palette:**
  - Background: Slate grays (#1E293B, #0F172A)
  - Primary accents: Blueprint blues (#2563EB, #3B82F6)
  - Alerts/Warnings: Safety orange (#F97316) / Red (#EF4444)
  - Success/Safe: Green (#22C55E)

## Components
1. **Main Dashboard View:**
   - "Upcoming Maintenance" widget (Next 30 days)
   - "Recent Repairs" summary
   - "Total Money Saved" metric (Pro quote vs. DIY cost)
2. **Appliance Registry:**
   - Grid of appliances with Make, Model, Install Date, Warranty Status.
   - Quick link to manual (Cross-sell: DocuScan integration).
3. **Repair Log:**
   - Timeline of completed fixes with notes, photos, and cost breakdowns.
4. **Tool Inventory:**
   - Checklist-style view of tools owned, categorized (Plumbing, Electrical, General).

## Database Schema (Supabase PostgreSQL)

```sql
-- Home Profile & Settings
CREATE TABLE home_profiles (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id),
  home_type VARCHAR(50), 
  year_built INT,
  hvac_type VARCHAR(50),
  skill_level VARCHAR(20) DEFAULT 'beginner',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tool & Supply Inventory
CREATE TABLE tool_inventory (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id),
  tool_name VARCHAR(100),
  category VARCHAR(50),
  has_tool BOOLEAN DEFAULT false
);

-- Appliance Registry
CREATE TABLE appliances (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id),
  appliance_type VARCHAR(50),
  brand VARCHAR(50),
  model_number VARCHAR(100),
  purchase_date DATE,
  warranty_months INT,
  manual_url TEXT
);

-- Repair History Log
CREATE TABLE repair_logs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id),
  issue_title VARCHAR(150),
  category VARCHAR(50),
  diagnosis TEXT,
  fixed_date DATE,
  diy_cost DECIMAL(10,2),
  pro_quote_estimate DECIMAL(10,2),
  notes TEXT
);

-- Seasonal Maintenance Calendar
CREATE TABLE maintenance_tasks (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id),
  task_name VARCHAR(150),
  frequency_days INT,
  last_completed DATE,
  next_due DATE,
  status VARCHAR(20) DEFAULT 'pending'
);
```

## ⚠️ Security Requirements
- **Authentication:** Implement user authentication (NextAuth.js or Supabase Auth) before deploying. No anonymous access.
- **Row Level Security (RLS):** Enable Supabase RLS on all tables. Users must only see their own home/repair data.
- **Image Storage:** Store repair photos in a **private** storage bucket — photos may reveal home security details (locks, entry points, structural weaknesses).
- **Environment Variables:** All Supabase keys, API URLs, and auth secrets must be stored as environment variables — never hardcoded.
