-- Pantry Tracker — Supabase Schema
-- Run this in the Supabase SQL editor to set up the tables.

create table pantry_items (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  category text, -- produce, dairy, meat, pantry, frozen, other
  quantity text, -- "2 lbs", "1 bunch", "6 count", etc.
  purchased_at timestamptz not null default now(),
  expires_at timestamptz, -- estimated expiry
  status text not null default 'fresh', -- fresh, use-soon, expired, used, tossed
  source text, -- "whole-foods", "instacart", "costco", "manual"
  order_id text, -- email order reference
  notes text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- Index for the morning query: what's expiring soon?
create index idx_pantry_status_expires on pantry_items (status, expires_at)
  where status in ('fresh', 'use-soon');

-- Auto-update updated_at
create or replace function update_updated_at()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

create trigger pantry_items_updated
  before update on pantry_items
  for each row execute function update_updated_at();
