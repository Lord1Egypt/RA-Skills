# permissions.json Schema

## Categories and Sensitivity Levels

Each category has numbered levels (1 = low sensitivity, higher = more sensitive):

### personal_facts
- **1**: Full name, nationality
- **2**: Birthday, age
- **3**: Home address, phone number

### health
- **1**: General wellness ("feeling sick today")
- **2**: Ongoing conditions (allergies, common conditions)
- **3**: Specific diagnoses, medications
- **4**: Mental health details
- **5**: Full medical history

### schedule
- **1**: General availability (free/busy)
- **2**: Event names and times
- **3**: Event details, locations, attendees

### financial
- **1**: Employment status
- **2**: General financial comfort
- **3**: Salary, specific amounts
- **4**: Bank details, investments

### relationships
- **1**: Relationship status (single, married, etc.)
- **2**: Partner's name, number of children
- **3**: Relationship details, family dynamics

### location
- **1**: Country, city
- **2**: Neighborhood, workplace area
- **3**: Exact address, real-time location

### work
- **1**: Job title, company
- **2**: Projects, responsibilities
- **3**: Internal company info, performance

### preferences
- **1**: Hobbies, favorite food/music
- **2**: Political/religious views
- **3**: Deeply personal opinions

## Relationship Access Matrix (Defaults)

Number = max level accessible per category. 0 = no access.

| Category | partner | family | close_friend | friend | colleague | acquaintance | stranger |
|---|---|---|---|---|---|---|---|
| personal_facts | 3 | 3 | 2 | 2 | 1 | 1 | 0 |
| health | 5 | 4 | 3 | 1 | 1 | 0 | 0 |
| schedule | 3 | 3 | 3 | 2 | 2 | 1 | 0 |
| financial | 4 | 2 | 1 | 1 | 1 | 0 | 0 |
| relationships | 3 | 3 | 2 | 1 | 1 | 0 | 0 |
| location | 3 | 2 | 2 | 1 | 1 | 1 | 0 |
| work | 3 | 2 | 2 | 1 | 2 | 1 | 0 |
| preferences | 3 | 2 | 2 | 1 | 1 | 1 | 0 |

Users can adjust these defaults and add per-contact overrides.

## Structure

```json
{
  "categories": { ... },
  "relationship_access": {
    "partner": { "personal_facts": 3, "health": 5, ... },
    "stranger": { "personal_facts": 0, "health": 0, ... }
  },
  "policy_overrides": {
    "overrides": [
      {
        "contact_id": "alice",
        "category": "schedule",
        "level": 3,
        "reason": "User approved on 2026-03-28"
      }
    ]
  }
}
```

Per-contact overrides take precedence over relationship defaults.
