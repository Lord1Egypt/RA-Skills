# Radarr API Reference

Base: `$RADARR_URL/api/v3/`
Auth: Header `X-Api-Key: $RADARR_KEY`

## Movies
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/movie` | List all movies |
| GET | `/movie/{id}` | Get movie by ID |
| GET | `/movie/lookup?term=` | Search TMDB for movies |
| GET | `/movie/lookup/tmdb?tmdbId=` | Lookup by TMDB ID |
| GET | `/movie/lookup/imdb?imdbId=` | Lookup by IMDB ID |
| POST | `/movie` | Add a movie |
| PUT | `/movie/{id}` | Update movie |
| DELETE | `/movie/{id}` | Remove movie |
| GET | `/moviefile?movieId={id}` | Get movie file on disk |
| DELETE | `/moviefile/{id}` | Delete a movie file |

## Queue
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/queue` | Current download queue |
| GET | `/queue?pageSize=20` | Queue with pagination |
| DELETE | `/queue/{id}` | Remove item from queue |
| DELETE | `/queue/{id}?blacklist=true` | Remove + blacklist |

## Wanted
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/wanted/missing` | Monitored but missing movies |
| GET | `/wanted/missing?pageSize=20` | Missing with pagination |
| GET | `/wanted/cutoff` | Movies below quality cutoff |

## Commands
POST `/command` with `{"name": "<CommandName>"}`:
- `MissingMoviesSearch` — search for all missing monitored movies
- `MoviesSearch` — search for specific movies (`{"name":"MoviesSearch","movieIds":[N]}`)
- `RescanMovie` — rescan movie folder (`{"name":"RescanMovie","movieId":N}`)
- `RefreshMovie` — refresh movie metadata (`{"name":"RefreshMovie","movieId":N}`)
- `RenameMovie` — rename movie files (`{"name":"RenameMovie","movieIds":[N]}`)
- `RescanFolders` — rescan all root folders

## Quality Profiles
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/qualityprofile` | List quality profiles |
| GET | `/qualityprofile/{id}` | Get profile by ID |

## Root Folders
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/rootfolder` | List configured root folders |

## Config & System
| Endpoint | Description |
|----------|-------------|
| GET `/system/status` | System info + version |
| GET `/history?pageSize=20` | Recent activity |
| GET `/downloadclient` | Configured download clients |
| GET `/indexer` | Configured indexers |
| GET `/notification` | Configured notifications |

## Pagination
Add `?page=1&pageSize=20&sortKey=sortTitle&sortDir=asc` to list endpoints.

## Add Movie Payload Example
```json
{
  "tmdbId": 603,
  "title": "The Matrix",
  "qualityProfileId": 1,
  "rootFolderPath": "/movies",
  "monitored": true,
  "addOptions": {
    "searchForMovie": true
  }
}
```
