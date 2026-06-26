# Sonarr API Reference

Base: `$SONARR_URL/api/v3/`
Auth: Header `X-Api-Key: $SONARR_KEY`

## Series
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/series` | List all series |
| GET | `/series/{id}` | Get series by ID |
| GET | `/series/lookup?term=` | Search TVDB for series |
| POST | `/series` | Add a series |
| PUT | `/series/{id}` | Update series |
| DELETE | `/series/{id}` | Remove series |

## Episodes
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/episode?seriesId={id}` | List episodes for a series |
| GET | `/episode/{id}` | Get episode by ID |
| PUT | `/episode/{id}` | Update episode (e.g. monitored flag) |
| GET | `/episodefile?seriesId={id}` | List episode files on disk |
| DELETE | `/episodefile/{id}` | Delete an episode file |

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
| GET | `/wanted/missing` | Monitored but missing episodes |
| GET | `/wanted/missing?pageSize=20` | Missing with pagination |
| GET | `/wanted/cutoff` | Episodes below quality cutoff |

## Commands
POST `/command` with `{"name": "<CommandName>"}`:
- `MissingEpisodeSearch` — search for all missing monitored episodes
- `SeriesSearch` — search for specific series (`{"name":"SeriesSearch","seriesId":N}`)
- `SeasonSearch` — search for a season (`{"name":"SeasonSearch","seriesId":N,"seasonNumber":N}`)
- `EpisodeSearch` — search for specific episodes (`{"name":"EpisodeSearch","episodeIds":[N]}`)
- `RescanSeries` — rescan series folder (`{"name":"RescanSeries","seriesId":N}`)
- `RefreshSeries` — refresh series metadata (`{"name":"RefreshSeries","seriesId":N}`)
- `RenameFiles` — rename episode files (`{"name":"RenameFiles","seriesId":N,"files":[N]}`)
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
| GET `/languageprofile` | Language profiles |

## Pagination
Add `?page=1&pageSize=20&sortKey=airDateUtc&sortDir=desc` to list endpoints.

## Add Series Payload Example
```json
{
  "tvdbId": 81189,
  "title": "Breaking Bad",
  "qualityProfileId": 1,
  "rootFolderPath": "/tv",
  "monitored": true,
  "seasonFolder": true,
  "seasons": [],
  "addOptions": {
    "ignoreEpisodesWithFiles": false,
    "ignoreEpisodesWithoutFiles": false,
    "searchForMissingEpisodes": true
  }
}
```
