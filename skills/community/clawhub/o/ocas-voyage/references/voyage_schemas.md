# Voyage Data Schemas

## Trip Plan

```json
{
  "plan_id": "uuid",
  "destination": "string",
  "dates": { "start": "YYYY-MM-DD", "end": "YYYY-MM-DD" },
  "constraints": {
    "budget": { "min": 0, "max": 0, "currency": "USD" },
    "diet": "vegetarian|vegan|omnivore|etc",
    "pace": "relaxed|moderate|intense",
    "travelers": 1
  },
  "status": "draft|confirmed|active|completed|cancelled",
  "created_at": "ISO8601",
  "updated_at": "ISO8601"
}
```

## Itinerary

```json
{
  "itinerary_id": "uuid",
  "plan_id": "uuid (references trip_plan.plan_id)",
  "day_number": 1,
  "date": "YYYY-MM-DD",
  "items": [
    {
      "time": "HH:MM",
      "type": "flight|lodging|food|activity|transit",
      "entity_id": "uuid (references entity)",
      "status": "planned|reserved|cancelled",
      "notes": "string"
    }
  ]
}
```

## Lodging Recommendation

```json
{
  "entity_id": "uuid",
  "type": "Place/Lodging",
  "name": "string",
  "source": "expedia|marriott|marriott_ai|google_hotels",
  "total_cost": { "amount": 0, "currency": "USD", "includes_fees": false },
  "cancellation": "free|partial|non-refundable",
  "location_fit": "central|suburban|airport",
  "loyalty_points": { "program": "points_value", "eligible": true }
}
```

## Flight Option

```json
{
  "entity_id": "uuid",
  "type": "Concept/Action/Flight",
  "flight_number": "XX1234",
  "airline": "string",
  "origin": "IATA",
  "destination": "IATA",
  "departure": "ISO8601",
  "arrival": "ISO8601",
  "duration_minutes": 0,
  "stops": 0,
  "cabin": "economy|premium|business|first",
  "price": { "amount": 0, "currency": "USD" },
  "bags": { "carry_on": true, "checked": 0 },
  "emissions_kg": 0,
  "retrieved_at": "ISO8601"
}
```

## Entity Observations

All entities encountered during planning are recorded in the Action Journal `decision.payload.entities_observed` field. Entity types: Place (venues, airports, hotels, restaurants), Concept/Event (trips, departures, arrivals), Concept/Action (bookings, cancellations), Entity/Person (travel companions). Each entity includes `user_relevance`: `user` | `agent_only` | `unknown`.
