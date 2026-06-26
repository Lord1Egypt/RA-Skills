# REST API Reference

Use this file when the user wants to register animals, query the herd, or
interact with the assistant via HTTP rather than through conversational context.

Base URL: `http://localhost:3000` (configurable via `PORT` env var)

---

## Health Check

```
GET /health
```

Response: `{ "status": "ok", "service": "openclaw-livestock-assistant" }`

---

## AI Assistant

### Create a session
```
POST /api/assistant/sessions
```
Response: `{ "sessionId": "<uuid>", "welcome": "<bienvenida>" }`

### Send a message
```
POST /api/assistant/sessions/:sessionId/messages
Content-Type: application/json

{ "message": "¿Cómo prevenir la mastitis en vacas lecheras?" }
```
Response: `{ "response": "...", "sessionId": "...", "tokens": 142 }`

### Get message history
```
GET /api/assistant/sessions/:sessionId/history
```
Response: `{ "sessionId": "...", "history": [{ "role": "user", "content": "..." }, ...] }`

### Delete a session
```
DELETE /api/assistant/sessions/:sessionId
```
Response: `204 No Content`

---

## Animals

### Register an animal
```
POST /api/animals
Content-Type: application/json

{
  "name": "Lola",
  "species": "bovine",
  "breed": "Holstein Friesian",
  "sex": "female",
  "birthDate": "2022-03-15",
  "weight": 420
}
```
Required fields: `name`, `species`, `breed`, `sex`, `birthDate`, `weight`

Response: `201 Created` — full animal object

### List animals
```
GET /api/animals
GET /api/animals?species=bovine
GET /api/animals?status=active
GET /api/animals?species=ovine&status=quarantine
```
Response: `{ "total": 3, "animals": [...] }`

### Herd statistics
```
GET /api/animals/stats
```
Response:
```json
{
  "total": 12,
  "bySpecies": { "bovine": 10, "ovine": 2 },
  "bySex": { "males": 2, "females": 10 },
  "byStatus": { "active": 11, "quarantine": 1 },
  "byHealth": { "healthy": 10, "in_treatment": 2 }
}
```

### Get a single animal
```
GET /api/animals/:id
```
Response: animal object or `404`

### Update an animal
```
PATCH /api/animals/:id
Content-Type: application/json

{ "weight": 450, "healthStatus": "in_treatment" }
```
Updatable fields: `name`, `breed`, `weight`, `status`, `healthStatus`, `reproductiveStatus`, `notes`

### Remove an animal
```
DELETE /api/animals/:id
```
Response: `204 No Content`

---

## Field Values

| Field | Allowed values |
|---|---|
| `species` | `bovine` `ovine` `caprine` `porcine` `equine` `poultry` |
| `sex` | `male` `female` |
| `status` | `active` `sold` `dead` `quarantine` |
| `healthStatus` | `healthy` `sick` `in_treatment` `recovered` |
| `reproductiveStatus` | `open` `pregnant` `lactating` `in_heat` `served` `not_applicable` |
