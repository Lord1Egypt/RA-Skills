# Setup - Paraguay Skill

## Requirements

No external dependencies. This skill uses file-based knowledge only.

## Memory Configuration

Create `~/paraguay/` for user preferences and trip context:

```bash
mkdir -p ~/paraguay
```

Copy the memory template:

```bash
cp memory-template.md ~/paraguay/memory.md
```

## File Structure

```
paraguay/
├── SKILL.md
├── setup.md
├── memory-template.md
│
├── asuncion.md
├── encarnacion.md
├── ciudad-del-este.md
├── chaco-and-north.md
│
├── itineraries.md
├── accommodation.md
├── money-and-payments.md
├── border-shopping.md
├── apps.md
│
├── food-guide.md
├── yerba-and-drinks.md
├── nightlife.md
│
├── experiences.md
├── beaches-and-waterfronts.md
├── hiking-and-nature.md
│
├── regions.md
├── culture.md
├── with-kids.md
│
├── transport.md
├── telecoms.md
└── emergencies.md
```

## Usage Notes

### When to Load Which File

| User Intent | Files to Load |
|-------------|---------------|
| General Paraguay trip | `SKILL.md` -> `itineraries.md` |
| Asuncion weekend or arrival base | `asuncion.md` |
| Border-shopping question | `ciudad-del-este.md` -> `border-shopping.md` |
| South Paraguay route | `encarnacion.md` -> `experiences.md` |
| Chaco or wildlife | `chaco-and-north.md` -> `hiking-and-nature.md` |
| Money and payment friction | `money-and-payments.md` |
| Food questions | `food-guide.md` -> `yerba-and-drinks.md` |
| Family planning | `with-kids.md` |
| Emergency or safety issue | `emergencies.md` |

### Memory System

User preferences stored in `~/paraguay/memory.md`:
- travel style
- heat tolerance
- budget level
- border comfort level
- visited places
- preferred pace

Check the memory file before making recommendations.

### Quality Standards

Every recommendation should include:
- a specific base or neighborhood
- why that option fits the traveler's goal
- timing or seasonality caveats
- transfer friction when it matters
- what to skip if the schedule is tight

### Updating Information

This skill is most reliable for route logic, food culture, and practical tradeoffs. Verify current opening hours, festival dates, bridge delays, and prices before any high-commitment booking.

## Verification

Test the skill by asking:
1. "I have 6 days in Paraguay, should I do Asuncion and Encarnacion or add Ciudad del Este?"
2. "What is actually worth doing in Ciudad del Este besides shopping?"
3. "How should I plan a summer weekend around San Bernardino or Encarnacion?"

If answers stay generic or ignore route friction, the skill is not being used correctly.
