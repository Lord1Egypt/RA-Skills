# Plant Doctor Dashboard Companion Kit

## Design System
- **Aesthetic:** Botanical, modern, and clean.
- **Colors:**
  - Background: Cream (`#FBFBF9`)
  - Primary Accents: Forest Green (`#2C5530`)
  - Cards/Secondary: Sage Green (`#8A9A86`)
  - Highlights/Alerts: Warm Terracotta (`#E2725B`)

## DB Schema (Supabase/Prisma/SQL)

```sql
CREATE TABLE Location (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL, -- e.g., "Living Room"
    light_level VARCHAR(50) NOT NULL -- low, bright_indirect, direct
);

CREATE TABLE Plant (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    species VARCHAR(255),
    location_id UUID REFERENCES Location(id),
    acquired_date DATE,
    image_url TEXT,
    toxicity_status BOOLEAN DEFAULT false
);

CREATE TABLE CareSchedule (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    plant_id UUID REFERENCES Plant(id) ON DELETE CASCADE,
    action_type VARCHAR(50) NOT NULL, -- water, fertilize, mist
    frequency_days INT NOT NULL,
    last_completed DATE,
    next_due DATE
);

CREATE TABLE HealthLog (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    plant_id UUID REFERENCES Plant(id) ON DELETE CASCADE,
    log_date DATE NOT NULL DEFAULT CURRENT_DATE,
    photo_url TEXT,
    diagnosis TEXT,
    treatment_applied TEXT
);
```

## Component Descriptions

1. **PlantGallery:**
   - A masonry grid layout displaying the user's entire plant collection.
   - Each card shows the plant's photo, name, and dynamic status badges (e.g., 💧 Needs Water, 🏥 Recovering).
   
2. **CareCalendar:**
   - A monthly calendar view highlighting upcoming care tasks (watering, fertilizing, misting) color-coded by action type.
   
3. **RoomView:**
   - Groups plants by their `Location` (e.g., Living Room, Bedroom).
   - Allows users to easily batch-water plants in the same physical space.

## ⚠️ Security Requirements
- **Authentication:** Implement user authentication (NextAuth.js or Supabase Auth) before deploying. No anonymous access.
- **Row Level Security (RLS):** Enable Supabase RLS on all tables. Users must only see their own plant data.
- **Image Storage:** Store plant photos in a **private** Supabase Storage bucket (not public). Generate signed URLs for display. Photos may contain images of home interiors.
- **Environment Variables:** All Supabase keys, API URLs, and auth secrets must be stored as environment variables — never hardcoded.
