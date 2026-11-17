# File Structure

> For maintenance/troubleshooting only. SKILL.md runtime does not require reading this.

```
powpow-publisher/
├── SKILL.md                          # main file (kept lean; details in references/)
├── config.json                       # platformUrl + optional user's Unsplash key (NO secrets; read-only)
├── scripts/
│   ├── doctor.js                     # first-run self-check (node/config/network/session)
│   ├── login.js                      # username/password → JWT (password never stored, hidden prompt)
│   ├── compose.js                    # ONE-COMMAND post HTML assembly (the only supported way; fully local)
│   ├── publish.js                    # upload local images + POST /api/posts as the logged-in user
│   ├── verify.js                     # verify post by ID via platform API
│   ├── delete-post.js                # delete own post (test cleanup)
│   ├── geocode.js                    # place name → WGS-84 candidates (user confirms)
│   ├── list-digital-humans.js        # list/search with health filtering
│   ├── match-digital-human.js        # topic → ranked healthy candidates
│   ├── create-digital-human.js       # create a map digital human (2 badges, 30-day expiry; avatar: generate/upload/URL)
│   ├── search-image.js               # Unsplash (user's own key, optional; also resolves photo-page links)
│   ├── upload-image.js               # local image → platform storage → public URL (used by publish.js)
│   └── lib/
│       ├── api-client.js             # platform API client (JWT, pinned headers)
│       ├── dh-match.js               # shared DH health filter + topic ranking (name 3x, desc 1x, discipline-term masking)
│       ├── coord-transform.js        # GCJ-02 ↔ WGS-84 conversion (iterative inverse)
│       └── html-formatter.js         # HTML components + CJK-aware word count
└── references/
    ├── changelog.md                  # version history (this package: 1.0.3; inherited: 5.3 → 5.7.3)
    ├── security.md                   # security architecture + platform API list
    ├── screenshots.md                # product screenshot inventory + external links
    └── file-structure.md             # this file
```

Note: the login session (`session.json`) is **never written into the skill bundle**;
it lives in the user's state directory (`POWPOW_STATE_DIR`, default `~/.powpow/`)
and expires after ~7 days (the skill keeps a 6-day re-login margin).

Scripts in this package are byte-identical to `powpow-simple-en` v1.0.0 and
`powpow-simple` v5.7.3 — only documentation and metadata differ.
