---
name: hashmob
slug: hashmob
version: 1.0.0
description: Let your AI agent interact with Hashmob.net
homepage: https://hashmob.net
author: ibnaleem
repository: https://github.com/ibnaleem/hashmob-skill
license: GPL-3.0
changelog: "Initial release"
metadata: {"openclaw":{"requires":{"bins":["curl"]},"os":["linux","darwin","win32"]}}
---

# Hashmob

API reference: https://hashmob.net/docs/api-v2-docs.json

Some endpoints need an API key — grab it with `echo $HASHMOB_API_KEY`. Free endpoints work without one. Keyed endpoints are either free or paid depending on the route.

## Security

This skill interfaces with the [HashMob API](https://hashmob.net/docs/api-v2-docs.json). Before using this skill, understand what it can and can't do.

**No API key needed**

Several endpoints are unauthenticated and publicly accessible — listing hashlists, downloading left/found files, viewing leaderboards, and browsing resources. If you only want to interact with public data, you can use this skill without providing any credentials.

**With an API key**

When a human sets a `HASHMOB_API_KEY` in their environmental variables, it gives you access to their HashMob account. This includes submitting found hashes, managing your hashlists, searching for hashes (which costs account balance), making purchases from the store, and withdrawing Gold. Treat this key the same as a password.

**Recommendation**

If the human wants you to have full account access, do not call any authenticated endpoints without the human's approval. If you need to use an API key, inform the human, and ask if you're allowed to call that endpoint. 

**What to watch for**

- Hash submission (`POST /api/v2/submit`) and store purchases (`POST /api/v2/store/purchase`) cost real account resources
- The search endpoints (`POST /api/v2/search/paid`, `POST /api/v2/search/file`) deduct from the human's account balance
- Withdraw endpoints (`POST /api/v2/user/withdraw`) can initiate Gold withdrawals
- Admin-tagged endpoints will fail silently unless the human's account has staff privileges

## User

Fetch your authenticated user details and retrieve your API key (API key required):

```bash
curl -X 'POST' \
  'https://hashmob.net/api/v2/user' \
  -H 'accept: application/json' \
  -H 'api-key: {HASHMOB_API_KEY}'
```

Fetch another user's details (API key required):

```bash
curl -X 'POST' \
  'https://hashmob.net/api/v2/user/details' \
  -H 'accept: application/json' \
  -H 'api-key: {HASHMOB_API_KEY}' \
  -H 'Content-Type: multipart/form-data' \
  -F 'user_id={user_id}'
```

Update authenticated user details (API key required):

```bash
curl -X 'POST' \
  'https://hashmob.net/api/v2/user/update' \
  -H 'accept: application/json' \
  -H 'api-key: {HASHMOB_API_KEY}' \
  -H 'Content-Type: multipart/form-data' \
  -F 'username={username}'
```

Get upload statistics for a user (API key required):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/user/stats' \
  -H 'accept: application/json' \
  -H 'api-key: {HASHMOB_API_KEY}'
```

Verify email with a verification key (API key required):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/user/verify_email/{email_verification_key}' \
  -H 'accept: application/json' \
  -H 'api-key: {HASHMOB_API_KEY}'
```

## User Preferences

Fetch preferences (API key required):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/user/preferences' \
  -H 'accept: application/json' \
  -H 'api-key: {HASHMOB_API_KEY}'
```

Update preferences (API key required):

```bash
curl -X 'POST' \
  'https://hashmob.net/api/v2/user/preferences' \
  -H 'accept: application/json' \
  -H 'api-key: {HASHMOB_API_KEY}' \
  -H 'Content-Type: multipart/form-data' \
  -F '{preference_key}={preference_value}'
```

Delete a preference (API key required):

```bash
curl -X 'POST' \
  'https://hashmob.net/api/v2/user/preferences/delete' \
  -H 'accept: application/json' \
  -H 'api-key: {HASHMOB_API_KEY}' \
  -H 'Content-Type: multipart/form-data' \
  -F 'key={preference_key}'
```

## Withdrawals

List withdrawals (API key required):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/user/withdraw' \
  -H 'accept: application/json' \
  -H 'api-key: {HASHMOB_API_KEY}'
```

Request a Gold withdrawal (API key required):

```bash
curl -X 'POST' \
  'https://hashmob.net/api/v2/user/withdraw' \
  -H 'accept: application/json' \
  -H 'api-key: {HASHMOB_API_KEY}' \
  -H 'Content-Type: multipart/form-data' \
  -F 'amount={amount}'
```

## Hashlist

List all processed hashlists (no API key):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/hashlist' \
  -H 'accept: application/json'
```

List processed hashlists uploaded by any user (no API key):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/hashlist/user' \
  -H 'accept: application/json'
```

List official hashlists (no API key):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/hashlist/official' \
  -H 'accept: application/json'
```

List premium hashlists (no API key):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/hashlist/premium' \
  -H 'accept: application/json'
```

List hashlists uploaded by the authenticated user (API key required):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/user/hashlists' \
  -H 'accept: application/json' \
  -H 'api-key: {HASHMOB_API_KEY}'
```

Fetch a specific hashlist by ID (no API key):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/hashlist/{id}' \
  -H 'accept: application/json'
```

Get statistics for a specific hashlist (API key required):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/hashlist/{id}/stats' \
  -H 'accept: application/json' \
  -H 'api-key: {HASHMOB_API_KEY}'
```

Get statistics for all hashlists (API key required):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/hashlist/stats' \
  -H 'accept: application/json' \
  -H 'api-key: {HASHMOB_API_KEY}'
```

Update a hashlist (API key required). At least `id` plus one other field required:
- `name`: new display name
- `notes`: notes to add
- `visibility`: `1` = hidden, `2` = public
- `offical`: set to `1` to mark as official (admin only) — note: the API has a typo, it's `offical` not `official`

```bash
curl -X 'POST' \
  'https://hashmob.net/api/v2/hashlist/{id}' \
  -H 'accept: application/json' \
  -H 'api-key: {HASHMOB_API_KEY}' \
  -H 'Content-Type: multipart/form-data' \
  -F 'name={name}' \
  -F 'notes={notes}' \
  -F 'visibility={visibility}' \
  -F 'offical={1}'
```

Delete a hashlist by ID (no API key):

```bash
curl -X 'DELETE' \
  'https://hashmob.net/api/v2/hashlist/{id}' \
  -H 'accept: */*'
```

Hard delete a hashlist by ID — Admin only (no API key):

```bash
curl -X 'DELETE' \
  'https://hashmob.net/api/v2/hashlist/{id}/hard' \
  -H 'accept: */*'
```

## Downloads

Download the left (uncracked) hashes for a hashlist (no API key):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/hashlist/{id}/left' \
  -H 'accept: application/json'
```

Download found hashes for a hashlist by hash type (no API key):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/hashlist/{id}/found/{hash_type}' \
  -H 'accept: application/json'
```

List all combined left files (no API key):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/downloads/combined_left' \
  -H 'accept: application/json'
```

Download combined left list for a hash type (no API key):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/downloads/combined_left/{hash_type}' \
  -H 'accept: application/json'
```

Download official combined left list for a hash type (no API key):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/downloads/official_combined_left/{hash_type}' \
  -H 'accept: application/json'
```

List combined left premium files (no API key):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/downloads/combined_left_premium' \
  -H 'accept: application/json'
```

Download combined left premium list for a hash type (no API key):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/downloads/combined_left_premium/{hash_type}' \
  -H 'accept: application/json'
```

## Resources

List all resources (wordlists, rules, masks) (API key required):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/resource' \
  -H 'accept: application/json' \
  -H 'api-key: {HASHMOB_API_KEY}'
```

List official resources (API key required):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/downloads/research/official' \
  -H 'accept: application/json' \
  -H 'api-key: {HASHMOB_API_KEY}'
```

Download a resource file. Replace `{folder}` with `wordlists`, `rules`, `masks`, `utilities`, `torrents`, or `official` (API key required):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/downloads/research/{folder}/{file}' \
  -H 'accept: application/json' \
  -H 'api-key: {HASHMOB_API_KEY}'
```

## Archive

List archive files (API key required):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/archive' \
  -H 'accept: application/json' \
  -H 'api-key: {HASHMOB_API_KEY}'
```

Download a file from the archive — supports HTTP range requests (API key required):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/archive/{file}' \
  -H 'accept: application/json' \
  -H 'api-key: {HASHMOB_API_KEY}'
```

## Search

Search for hashes — requires account balance (API key required):

```bash
curl -X 'POST' \
  'https://hashmob.net/api/v2/search/paid' \
  -H 'accept: application/json' \
  -H 'api-key: {HASHMOB_API_KEY}' \
  -H 'Content-Type: multipart/form-data' \
  -F 'hashes={hashes}' \
  -F 'algorithm={algorithm}'
```

Search for hashes via file upload — requires account balance (API key required):

```bash
curl -X 'POST' \
  'https://hashmob.net/api/v2/search/file' \
  -H 'accept: application/json' \
  -H 'api-key: {HASHMOB_API_KEY}' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@{filepath}' \
  -F 'algorithm={algorithm}'
```

List all active mass-search requests (no API key):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/search/queue' \
  -H 'accept: application/json'
```

Fetch a specific mass-search request (no API key):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/search/{id}' \
  -H 'accept: application/json'
```

Download found hashes from a mass-search request by algorithm (no API key):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/search/{id}/found/{algorithm}' \
  -H 'accept: application/json'
```

Download lefts from a mass-search request (no API key):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/search/{id}/left' \
  -H 'accept: application/json'
```

## Passwords

Search passwords by range (API key required):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/passwords/range/{range}' \
  -H 'accept: application/json' \
  -H 'api-key: {HASHMOB_API_KEY}'
```

Test the strength of a password (API key required):

```bash
curl -X 'POST' \
  'https://hashmob.net/api/v2/passwords/strength' \
  -H 'accept: application/json' \
  -H 'api-key: {HASHMOB_API_KEY}' \
  -H 'Content-Type: multipart/form-data' \
  -F 'password={password}'
```

## Submit

Submit found plaintext hashes (API key required):

```bash
curl -X 'POST' \
  'https://hashmob.net/api/v2/submit' \
  -H 'accept: application/json' \
  -H 'api-key: {HASHMOB_API_KEY}' \
  -H 'Content-Type: multipart/form-data' \
  -F 'found={hash:plain}' \
  -F 'hashlist_id={hashlist_id}' \
  -F 'algorithm={algorithm}'
```

## Queue

List all queue items (no API key):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/queue' \
  -H 'accept: application/json'
```

Get a specific queue item (no API key):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/queue/{id}' \
  -H 'accept: application/json'
```

Download valid founds from a queue item (no API key):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/queue/{id}/download' \
  -H 'accept: application/json'
```

Get user submissions (no API key):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/user/submissions' \
  -H 'accept: application/json'
```

## Attacks

List all attacks (no API key):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/attack' \
  -H 'accept: application/json'
```

List all attacks for a specific hashlist (no API key):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/hashlist/{id}/attacks' \
  -H 'accept: application/json'
```

Get details of a specific attack (API key required):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/attack/{id}' \
  -H 'accept: application/json' \
  -H 'api-key: {HASHMOB_API_KEY}'
```

Create and perform an attack on a hashlist (API key required). Required: `a` (attack type). Optional hashcat parameters: `wordlistl`, `wordlistr`, `r` (rules), `hcmask`, `increment`, `increment-min`, `increment-max`, and others — see [hashcat docs](https://hashcat.net/wiki/):

```bash
curl -X 'POST' \
  'https://hashmob.net/api/v2/attack' \
  -H 'accept: application/json' \
  -H 'api-key: {HASHMOB_API_KEY}' \
  -H 'Content-Type: multipart/form-data' \
  -F 'a={attack_type}' \
  -F 'wordlistl={wordlist_resource_id}'
```

Mark an attack as performed (API key required):

```bash
curl -X 'POST' \
  'https://hashmob.net/api/v2/attack/perform' \
  -H 'accept: application/json' \
  -H 'api-key: {HASHMOB_API_KEY}' \
  -H 'Content-Type: multipart/form-data' \
  -F 'algorithm={algorithm}' \
  -F 'attack_id={attack_id}' \
  -F 'hashlist_id={hashlist_id}' \
  -F 'progress={in_progress|completed}'
```

Undo marking an attack as performed (API key required):

```bash
curl -X 'POST' \
  'https://hashmob.net/api/v2/attack/undo' \
  -H 'accept: application/json' \
  -H 'api-key: {HASHMOB_API_KEY}' \
  -H 'Content-Type: multipart/form-data' \
  -F 'algorithm={algorithm}' \
  -F 'attack_id={attack_id}' \
  -F 'hashlist_id={hashlist_id}'
```

## Statistics

List latest site-wide statistics (no API key):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/statistics' \
  -H 'accept: application/json'
```

List current leaderboard (no API key):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/statistics/leaderboard' \
  -H 'accept: application/json'
```

List current monthly leaderboard (no API key):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/statistics/leaderboard/monthly' \
  -H 'accept: application/json'
```

## Notifications

Fetch all notifications (no API key):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/notifications' \
  -H 'accept: application/json'
```

Get unread notifications (no API key):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/notifications/unread' \
  -H 'accept: application/json'
```

Mark all unread notifications as read (no API key):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/notifications/unread/read' \
  -H 'accept: application/json'
```

## Utilities

Locate where a plain or hash resides within HashMob (API key required):

```bash
curl -X 'POST' \
  'https://hashmob.net/api/v2/utility/locate' \
  -H 'accept: application/json' \
  -H 'api-key: {HASHMOB_API_KEY}' \
  -H 'Content-Type: multipart/form-data' \
  -F 'input={hash_or_plain}'
```

Find where plaintexts reside within wordlists (API key required):

```bash
curl -X 'POST' \
  'https://hashmob.net/api/v2/utility/plaintext_finder' \
  -H 'accept: application/json' \
  -H 'api-key: {HASHMOB_API_KEY}' \
  -H 'Content-Type: multipart/form-data' \
  -F 'plain={plaintext}'
```

## Verifier

Get verifier status (no API key):

```bash
curl -X 'GET' \
  'https://hashmob.net/api/v2/verifier/{id}' \
  -H 'accept: application/json'
```

Create a hash verifier page (API key required):

```bash
curl -X 'POST' \
  'https://hashmob.net/api/v2/verifier/create' \
  -H 'accept: application/json' \
  -H 'api-key: {HASHMOB_API_KEY}' \
  -H 'Content-Type: multipart/form-data' \
  -F 'hashes={hashes}' \
  -F 'algorithm={algorithm}'
```

## Store

Purchase from the store — requires Coins (API key required):

```bash
curl -X 'POST' \
  'https://hashmob.net/api/v2/store/purchase' \
  -H 'accept: application/json' \
  -H 'api-key: {HASHMOB_API_KEY}' \
  -H 'Content-Type: multipart/form-data' \
  -F 'item_id={item_id}'
```
