# Gusnais API Endpoint Mapping (Homeland API Compatible)

Base:
- Site: `https://gusnais.com`
- API base: `/api/v3`

OAuth:
- GET  `/oauth/authorize`
- POST `/oauth/token`
- POST `/oauth/revoke`

## Root
- GET `/api/v3/hello`

## Users
- GET  `/api/v3/users`
- GET  `/api/v3/users/:id`
- GET  `/api/v3/users/me`
- GET  `/api/v3/users/:id/replies`
- GET  `/api/v3/users/:id/topics`
- POST `/api/v3/users/:id/block`
- POST `/api/v3/users/:id/unblock`
- GET  `/api/v3/users/:id/blocked`
- POST `/api/v3/users/:id/follow`
- POST `/api/v3/users/:id/unfollow`
- GET  `/api/v3/users/:id/following`
- GET  `/api/v3/users/:id/followers`
- GET  `/api/v3/users/:id/favorites`

## Nodes
- GET `/api/v3/nodes`
- GET `/api/v3/nodes/:id`

## Topics
- GET    `/api/v3/topics`
- GET    `/api/v3/topics/:id`
- POST   `/api/v3/topics`
- PUT    `/api/v3/topics/:id`
- DELETE `/api/v3/topics/:id`
- POST   `/api/v3/topics/:id/replies`
- GET    `/api/v3/topics/:id/replies`
- POST   `/api/v3/topics/:id/follow`
- POST   `/api/v3/topics/:id/unfollow`
- POST   `/api/v3/topics/:id/favorite`
- POST   `/api/v3/topics/:id/unfavorite`
- POST   `/api/v3/topics/:id/action?type=:type`

Topic list params:
- `type`: `last_actived|recent|no_reply|popular|excellent` (default `last_actived`)
- `node_id`: optional node filter
- `offset`: default `0`
- `limit`: default `20`, range `1..150`

## Replies
- GET    `/api/v3/replies/:id`
- POST   `/api/v3/replies/:id`
- DELETE `/api/v3/replies/:id`

## Photos
- POST `/api/v3/photos` (multipart form, field: `file`)

## Likes
- POST   `/api/v3/likes`
- DELETE `/api/v3/likes`

Like params:
- `obj_type`: `topic|reply`
- `obj_id`: integer

## Notifications
- GET    `/api/v3/notifications`
- POST   `/api/v3/notifications/read`
- GET    `/api/v3/notifications/unread_count`
- DELETE `/api/v3/notifications/:id`
- DELETE `/api/v3/notifications/all`

Common pagination:
- `offset` default `0`
- `limit` default `20`

Common status semantics:
- `200/201` success
- `400` validation/request error
- `401` auth missing/expired
- `403` forbidden
- `404` resource not found
- `500` server error

## Plugin API surface (read/write contract)

> Goal: keep plugin capability parity with web endpoints and permission checks.
> On deployments that have not mounted plugin API endpoints yet, these paths may return 404.

### Press (`press-master`)

Web routes observed:
- `GET /posts`
- `GET /posts/upcoming`
- `GET /posts/:id`
- `POST /posts`
- `PUT /posts/:id`
- `DELETE /posts/:id`
- `PUT /posts/:id/publish`
- `POST /posts/preview`
- `GET /admin/posts`

API contract used by this skill:
- `GET /api/v3/press/posts`
- `GET /api/v3/press/posts/upcoming`
- `GET /api/v3/press/posts/:id`
- `POST /api/v3/press/posts`
- `PUT /api/v3/press/posts/:id`
- `DELETE /api/v3/press/posts/:id`
- `PUT /api/v3/press/posts/:id/publish`
- `POST /api/v3/press/posts/preview`

### Note (`note-master`)

Web routes observed:
- `GET /notes`
- `GET /notes/:id`
- `POST /notes`
- `PUT /notes/:id`
- `DELETE /notes/:id`
- `POST /notes/preview`
- `GET /admin/notes`

API contract used by this skill:
- `GET /api/v3/note/notes`
- `GET /api/v3/note/notes/:id`
- `POST /api/v3/note/notes`
- `PUT /api/v3/note/notes/:id`
- `DELETE /api/v3/note/notes/:id`
- `POST /api/v3/note/notes/preview`

### Site (`site-master`)

Web routes observed:
- `GET /sites`
- `POST /sites`
- `GET /admin/sites`
- `POST /admin/sites/:id/undestroy`
- `GET /admin/site_nodes`

API contract used by this skill (deployment-verified):
- `GET /api/v3/site/sites`
- `GET /api/v3/site/sites/:id`
- `POST /api/v3/site/sites`
- `PUT /api/v3/site/sites/:id`
- `DELETE /api/v3/site/sites/:id`
- `GET /api/v3/site/site_nodes`

Notes:
- `undestroy` and site_node write APIs are not mounted in the current deployment and should be treated as unavailable unless server routes are explicitly added later.
- `favorite` field is not present on current `Site` model; client payload should use `{name, desc, url, site_node_id}`.

### Jobs (`jobs-master`)

Jobs plugin is node-driven in web app (`/jobs`) and backed by core Topics at builtin node `25`.

API mapping used by this skill:
- List jobs: `GET /api/v3/topics?node_id=25&type=last_actived`
- Create job topic: `POST /api/v3/topics` with `node_id=25`
- Detail/update/delete: core topic endpoints (`/api/v3/topics/:id`)
