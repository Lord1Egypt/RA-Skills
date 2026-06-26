# huisheng.fm API Skill Reference

The installed skill calls the fixed production API:

```text
https://huisheng.fm/api
```

The sandbox must provide exactly one token environment variable:

```text
HUISHENG_API_TOKEN
```

Every request sends:

```http
Authorization: Bearer <HUISHENG_API_TOKEN>
```

The token is the personal Agent access token from the user's dashboard.

## Endpoints

- `GET /feeds`
- `POST /feeds`
- `GET /feeds/{feedKey}`
- `PATCH /feeds/{feedKey}`
- `DELETE /feeds/{feedKey}`
- `GET /feeds/{feedKey}/config`
- `GET /feeds/{feedKey}/episodes`
- `POST /feeds/{feedKey}/episodes`
- `GET /feeds/{feedKey}/episodes/{episodeId}`
- `PATCH /feeds/{feedKey}/episodes/{episodeId}`
- `DELETE /feeds/{feedKey}/episodes/{episodeId}`

All endpoints are user-scoped. A token can only access Podcast Feeds owned by the authenticated dashboard user.
