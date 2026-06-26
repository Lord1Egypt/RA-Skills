# Phone Number Reservation & Management

## Step I: Clarify Intent

| The user wants to… | Go to |
|---|---|
| Reserve any available number | Step II, Path A |
| Browse numbers first (area code or country preference) | Step II, Path B |
| See their currently reserved numbers | Step III — List |
| Release a number | Step IV — Release |

---

## Step II: Find a Number

### Path A — Auto-select (user wants any number)

```bash
curl -sG https://api.pokulabs.com/numbers/available \
  -H "Authorization: Bearer $POKU_API_KEY"
```

Use the first number returned. If the response is empty, tell the user no numbers are currently available.

---

### Path B — Browse first

Ask for any preferences not already stated (area code, country: US or GB).

```bash
curl -sG https://api.pokulabs.com/numbers/available \
  -H "Authorization: Bearer $POKU_API_KEY" \
  --data-urlencode "country=<US|GB>" \
  --data-urlencode "areaCode=<3-digit code>"
```

Omit any params the user didn't specify. Display results as a numbered list and ask the user to pick one. If empty, offer to broaden the search (drop the area code filter, or try the other country).

---

## Step III: List Reserved Numbers

```bash
curl -s https://api.pokulabs.com/numbers \
  -H "Authorization: Bearer $POKU_API_KEY"
```

Display each number's `phoneNumber`, `id`, and `createdAt`.

---

## Step IV: Confirm and Reserve

Before reserving, confirm with the user:

> "I'm going to reserve [number] for you. This will be permanently assigned to your account. Ok to proceed?"

Do not reserve until the user says yes.

```bash
curl -s -X POST https://api.pokulabs.com/numbers/reserve \
  -H "Authorization: Bearer $POKU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"phoneNumber": "<selected E.164 number>"}'
```

On success, display the reserved number and its `id` clearly.

---

## Step V: Release a Number

> ⚠️ Releasing a number is permanent and user-impacting. Always confirm before proceeding.

> "Are you sure you want to release [number]? This cannot be undone."

```bash
curl -s -X DELETE https://api.pokulabs.com/numbers/<RESERVED_NUMBER_ID> \
  -H "Authorization: Bearer $POKU_API_KEY"
```
