# Voyage Schemas

## TripPlan
```json
{"plan_id":"string","destination":"string","dates":{"start":"string","end":"string"},"travelers":"number","constraints":"object","days":["ItineraryDay"],"reservations":["ReservationItem"],"status":"string"}
```

## ItineraryDay
```json
{"date":"string","items":[{"time":"string","type":"string — lodging|food|activity|transit","name":"string","location":"string","notes":"string","reservation_status":"string"}]}
```

## ReservationItem
```json
{"item_id":"string","type":"string","name":"string","datetime":"string","confirmation":"string|null","status":"string — planned|booked|confirmed|cancelled"}
```
