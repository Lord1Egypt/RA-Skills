---
name: linkedin-search-posts
description: Search LinkedIn posts by keywords using the Apify actor harvestapi/linkedin-post-search. Use when the user wants to search, scrape, or retrieve LinkedIn posts matching specific keywords. Accepts search queries, optional profile/company filters, date filter, and sort options. Requires APIFY_API_TOKEN env variable.
---

# LinkedIn Posts Search

Search LinkedIn posts via Apify actor `harvestapi~linkedin-post-search`.

## Prerequisites

Env variable `APIFY_API_TOKEN` must be set (configured in `openclaw.json` under `skills.entries.linkedin-search-posts.env`).

## Input schema

### Requis
- `searchQueries`: **array of strings** — liste des requêtes de recherche (max 85 caractères par requête). Supporte les opérateurs booléens LinkedIn. Ex : `["La Base Programme idéation Nantes"]`

### Optionnels — filtres auteurs
- `targetUrls`: liste d'URLs de profils/pages LinkedIn dont on veut les posts
- `authorsPublicIdentifiers`: liste d'identifiants publics LinkedIn (ex: `["williamhgates"]`)
- `authorsIds`: liste d'IDs LinkedIn (ex: `["ACoAAA8BYqEBCGLg_vT_ca6mMEqkpp9nVffJ3hc"]`)
- `authorsCompanyPublicIdentifiers`: liste d'identifiants de sociétés LinkedIn (ex: `["google", "microsoft"]`)

### Optionnels — pagination / volume
- `maxPosts`: nombre max de posts par requête (0 = tout scraper). Prioritaire sur `scrapePages`.
- `scrapePages`: nombre de pages à scraper si `maxPosts` non défini (~50 posts/page avec keywords, ~90-100 sans)
- `startPage`: page de départ (défaut: 1)

### Optionnels — contenu enrichi
- `scrapeReactions`: scraper les réactions (défaut: `false`). Chaque réaction est comptée comme un post séparé (facturation).
- `maxReactions`: nombre max de réactions par post (0 = toutes)
- `scrapeComments`: scraper les commentaires (défaut: `false`). Chaque commentaire est compté comme un post séparé (facturation).
- `maxComments`: nombre max de commentaires par post (0 = tous)

### Optionnels — tri / date
- `sortBy`: `"relevance"` (par pertinence, défaut) ou `"date"` (plus récents en premier)
- `postedLimit`: ancienneté max des posts. Valeurs acceptées : `'1h'`, `'24h'`, `'week'`, `'month'`, `'3months'`, `'6months'`, `'year'`

## Run the actor

```bash
curl --request POST \
  --url "https://api.apify.com/v2/acts/harvestapi~linkedin-post-search/runs?token=$APIFY_API_TOKEN" \
  --header 'Content-Type: application/json' \
  --data '{
    "searchQueries": ["<search query>"],
    "maxPosts": 50,
    "sortBy": "date",
    "postedLimit": "month"
  }'
```

La réponse contient :
- `data.id` — run ID
- `data.defaultDatasetId` — dataset ID pour récupérer les résultats
- `data.status` — statut initial (`READY` → `RUNNING` → `SUCCEEDED`)

## Poll until complete

```bash
curl "https://api.apify.com/v2/acts/harvestapi~linkedin-post-search/runs/<RUN_ID>?token=$APIFY_API_TOKEN"
```

Vérifier `data.status` == `SUCCEEDED`.

## Fetch results

```bash
curl "https://api.apify.com/v2/datasets/<DATASET_ID>/items?token=$APIFY_API_TOKEN"
```

Retourne un tableau JSON. Chaque item contient :
- `type` — `"post"` (ou `"reaction"` / `"comment"` si activés)
- `id` — ID du post
- `linkedinUrl` — URL du post
- `content` — texte du post
- `author.name`, `author.publicIdentifier`, `author.linkedinUrl`, `author.avatar.url`
- `postedAt.date`, `postedAt.timestamp`, `postedAt.postedAgoText`
- `postImages[]` — images du post
- `engagement.likes`, `engagement.comments`, `engagement.shares`, `engagement.reactions[]`
- `reactions[]` — détail des réactions (si `scrapeReactions: true`)
- `comments[]` — détail des commentaires (si `scrapeComments: true`)

## Pricing

$2 per 1000 posts (PAY_PER_EVENT). Réactions et commentaires comptent chacun comme un post séparé.

## Known limitations

- Chaque requête est limitée à 85 caractères par LinkedIn
- Les réactions et commentaires doublent/triplent le coût si activés
- Les résultats LinkedIn ne sont pas exhaustifs
