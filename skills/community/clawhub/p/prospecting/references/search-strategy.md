# Search Strategy Framework

## Core Principles

| Principle | Description |
|-----------|-------------|
| **Multi-center** | Large cities: 3-6 search centers to avoid missing suburbs |
| **Keyword matrix** | 4-6 keyword combinations per center |
| **Pagination** | Scroll and load 3 times per search |
| **Deduplication** | Cross-center, cross-keyword deduplication |
| **Data integrity** | All data must come from real sources, no fabrication |

---

## 1. Center Point Selection

| City Size | Centers | Radius | Examples |
|-----------|---------|--------|----------|
| < 500k | 1 (downtown) | 30mi | Small cities |
| 500k-2M | 2-3 | 20mi | Austin, Seattle |
| > 2M | 4-6 | 15mi | Houston, Dallas, LA |

### Houston Example
- Downtown (core)
- Katy (west)
- Sugar Land (southwest)
- The Woodlands (north)
- Baytown (east industrial)
- Cypress (northwest)

### Dallas Example
- Downtown Dallas
- Plano (north)
- Fort Worth (west)
- Arlington (south)
- Frisco (northeast)

---

## 2. Keyword Matrix

### 2.1 Structure

| Type | Purpose | Examples |
|------|---------|----------|
| **Core** | Industry standard | auto body shop, collision repair |
| **Service** | Sub-services | paint shop, body work, refinishing |
| **Equipment** | Equipment needs | spray booth, frame machine, car lift |
| **Brand** | Chain brands | Caliber, CARSTAR, Maaco, Crash Champions |
| **Scene** | Customer type | fleet repair, commercial vehicle, dealer |

### 2.2 By Industry

**Auto Body / Collision**
```
auto body shop
auto body repair
collision repair
collision center
paint shop
auto paint shop
```

**Manufacturing / CNC**
```
machine shop
CNC machining
metal fabrication
fabrication shop
precision machining
```

**HVAC**
```
HVAC contractor
heating and cooling
air conditioning service
commercial HVAC
```

---

## 3. Pagination Protocol

```
Search keyword → wait 5s → extract first 8
    ↓
Scroll → wait 3s → extract new 5-8
    ↓
Scroll → wait 3s → extract new 5-8
    ↓
Scroll → wait 3s → extract any remaining
    ↓
Done
```

**Key**: Wait 2-3s after each scroll for Google Maps to load.

---

## 4. Deduplication Rules

| Case | Criteria | Action |
|------|----------|--------|
| Exact duplicate | Same name + address | Keep more complete |
| Chain multi-location | Same name + different address | Keep (mark as chain) |
| Address reuse | Same address + different name | Keep (may be different business) |
| Closed | Maps shows "permanently closed" | Remove |
| Wrong industry | e.g. pure car wash | Remove |

---

## 5. Data Integrity Markers

### Markers

| Marker | Meaning | Use When |
|--------|---------|----------|
| `verified` | Verified real | Phone/address from Google Maps |
| `restricted_view` | Limited view | Review count, website URL not available |
| `unverified` | Not verified | Needs confirmation |
| `placeholder` | Placeholder | **DO NOT use for calling** |

### Field Annotation Example

```json
{
  "phone": "(713) 668-3639",
  "phone_status": "verified",
  "rating": "4.8",
  "rating_source": "visible_in_feed",
  "reviews_count": null,
  "reviews_count_note": "restricted_view",
  "raw_notes": "Google Maps restricted view. Phone and rating visible. Reviews count hidden."
}
```

---

## 6. Execution Checklist

```
□ Step 1: Determine city size → select center count
□ Step 2: Determine industry → select keyword matrix (4-6 keywords)
□ Step 3: Center 1 search
    □ Keyword 1: search → paginate 3x → extract
    □ Keyword 2: search → paginate 3x → extract
    □ ...
□ Step 4: Center 2 search (same as above)
□ Step 5: ... all centers
□ Step 6: Deduplicate
    □ Same name+address: keep one
    □ Mark chain brands
    □ Remove closed/non-target
□ Step 7: Validate
    □ Mark field sources
    □ Mark restricted fields
    □ Check for placeholder phones
□ Step 8: Score and tier
    □ Chain/large (🔴 high)
    □ Mid independent (🟡 medium)
    □ Small independent (🟢 low)
□ Step 9: Generate output
    □ index.json
    □ P###.json
    □ call-list.csv
□ Step 10: Archive
    □ candidates-raw.txt
    □ Note search time, keywords, centers
```

---

## 7. Prohibitions (Enforced)

| Prohibition | Rule |
|-------------|------|
| ❌ Fake phones | No (XXX) 555-XXXX format |
| ❌ Fake addresses | Must come from Maps extraction |
| ❌ Fake ratings | Must be visible in Maps |
| ❌ Fake review counts | Must be from Maps or marked restricted |
| ❌ Fake websites | Must be extracted or marked unavailable |

---

## 8. Cross-City / Cross-Industry

### Cities

| City | Centers |
|------|---------|
| Dallas | Downtown, Plano, Fort Worth, Arlington, Frisco |
| Austin | Downtown, Round Rock, Cedar Park, South Austin |
| Miami | Downtown, Fort Lauderdale, West Palm Beach |

### Industries

| Industry | Core Keywords | Service Keywords | Equipment Keywords |
|----------|-------------|------------------|-------------------|
| Auto Body | auto body shop, collision repair | paint shop, body work | spray booth, frame machine |
| Manufacturing | machine shop, CNC machining | metal fabrication, welding | CNC mill, lathe |
| HVAC | HVAC contractor, heating cooling | air conditioning, furnace | commercial HVAC |
| Dental | dental lab, dental clinic | orthodontic, prosthodontic | CAD/CAM, 3D printing |

---

## 9. FAQ

**Q: Google Maps restricted view?**
A: Mark restricted status. Try: login to Maps, visit website, use Yelp/Yellow Pages.

**Q: Too few results?**
A: Check: center too remote? keywords too narrow? enough pagination? expand radius?

**Q: Chain brands?**
A: Keep all locations (different address = different customer). Mark as chain. Priority contact.

---

## File Naming

```
prospect-data/
├── {city}-{state}-{date}/
│   ├── profile-{customer-name}.json
│   ├── candidates-raw.txt
│   ├── candidates.json
│   ├── index.json
│   ├── P001.json ~ P0XX.json
│   └── call-list.csv
```

---

## Version

- **Version**: 1.0.0
- **Date**: 2026-05-22
- **Scope**: All B2B proactive prospecting projects
