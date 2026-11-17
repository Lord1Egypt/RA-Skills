# ⚙️ Voyage

  <img src="./assets/readme/hero.jpg" width="100%" alt="Voyage">

Travel planning, itinerary construction, reservation management, lodging

**Skill name:** `ocas-voyage`
**Version:** 2.9.0
**Type:** 
**Layer:** Execution
**Author:** <agent-name>

---

## 📖 Overview

Travel planning, itinerary construction, reservation management, lodging

---

## 🔧 Capabilities

- `voyage.plan.trip` — create a full trip plan from destination, dates, and constraints
- `voyage.recommend.lodging` — parallel lodging search across Expedia, Marriott Strider, Marriott AI, Google Hotels, and 1Stay. Returns unified comparison table with total-cost breakdown and booking-gate summary.
- `voyage.recommend.flights` — search Google Flights for one-way, round-trip, multi-city, or date-range queries. Returns structured flight options with pricing, timing, and airline details.
- `voyage.recommend.food` — restaurant recommendations based on route and preferences
- `voyage.recommend.activities` — activity recommendations based on interests and logistics
- `voyage.optimize.itinerary` — optimize an existing itinerary for feasibility and logistics
- `voyage.status` — current plan state, pending reservations, open decisions
- `voyage.journal` — write journal for the current run; called at end of every run
- `voyage.update` — pull latest from GitHub source; preserves journals and data
- `entities_observed` — list of entities encountered (Place, Concept/Event, Concept/Action, Entity/Person), each with type, name, and context
- `relationships_observed` — connections between entities (e.g., a person associated with a trip, a restaurant located in a destination)
- `preferences_observed` — user preferences inferred from planning choices (e.g., budget range, dietary needs, pace preference)
- `user` — entity is directly related to the user's world (destinations, hotels, companions, reservations). Most Voyage entities are `user`-relevant since they represent the user's actual travel plans and destinations.
- `agent_only` — entity encountered incidentally (e.g., a landmark mentioned only as a routing waypoint, not as a destination)
- `unknown` — relevance is unclear

---

## 📊 Outputs

See `SKILL.md` for outputs, journals, and persistence rules.

---

## 📄 Files

| File | Purpose |
|---|---|
| `SKILL.md` | Skill definition |
| `references/` | Supporting documentation |
| `scripts/` | Helper scripts |


## Changelog

- [2.7.5] - 2026-04-12
- Changed
- [2026-04-05] Parallel lodging stack + GoPlaces cooperation
- Added
- Changed
- Validation
- [2026-04-04] Spec Compliance Update
- Changes

---

## 📚 Documentation

Read `SKILL.md` for operational details, schemas, and validation rules.

Read `references/` for detailed specifications and examples.


---

## 📄 License

MIT License — see `LICENSE` for details.
