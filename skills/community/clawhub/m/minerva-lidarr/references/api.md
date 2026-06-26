# Lidarr API Reference

Base: `$LIDARR_URL/api/v1/`
Auth: Header `X-Api-Key: $LIDARR_KEY`

## Artists
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/artist` | List all monitored artists |
| GET | `/artist/{id}` | Get artist by ID |
| GET | `/artist/lookup?term=` | Search MusicBrainz for artists |
| POST | `/artist` | Add/monitor an artist |
| PUT | `/artist/{id}` | Update artist |
| DELETE | `/artist/{id}` | Remove artist |

## Albums
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/album` | List all albums |
| GET | `/album?artistId={id}` | List albums for an artist |
| GET | `/album/{id}` | Get album by ID |
| GET | `/album/lookup?term=` | Search MusicBrainz for albums |
| POST | `/album` | Add an album |
| PUT | `/album/{id}` | Update album |
| DELETE | `/album/{id}` | Remove album |

## Tracks
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/track?artistId={id}` | List tracks for an artist |
| GET | `/track?albumId={id}` | List tracks for an album |
| GET | `/track/{id}` | Get track by ID |
| GET | `/trackfile?artistId={id}` | List track files on disk |
| DELETE | `/trackfile/{id}` | Delete a track file |

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
| GET | `/wanted/missing` | Monitored but missing albums |
| GET | `/wanted/missing?pageSize=20` | Missing with pagination |
| GET | `/wanted/cutoff` | Albums below quality cutoff |

## Commands
POST `/command` with `{"name": "<CommandName>"}`:
- `MissingAlbumSearch` — search for all missing monitored albums
- `ArtistSearch` — search for specific artist (`{"name":"ArtistSearch","artistId":N}`)
- `AlbumSearch` — search for specific albums (`{"name":"AlbumSearch","albumIds":[N]}`)
- `RescanArtist` — rescan artist folder (`{"name":"RescanArtist","artistId":N}`)
- `RefreshArtist` — refresh artist metadata (`{"name":"RefreshArtist","artistId":N}`)
- `RescanFolders` — rescan all root folders

## Quality Profiles
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/qualityprofile` | List quality profiles |
| GET | `/qualityprofile/{id}` | Get profile by ID |

## Metadata Profiles
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/metadataprofile` | List metadata profiles |
| GET | `/metadataprofile/{id}` | Get profile by ID |

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

## Pagination
Add `?page=1&pageSize=20&sortKey=title&sortDir=asc` to list endpoints.

## Add Artist Payload Example
```json
{
  "foreignArtistId": "5441c29d-3602-4898-b1a1-b77fa23b8e50",
  "artistName": "David Bowie",
  "qualityProfileId": 1,
  "metadataProfileId": 1,
  "rootFolderPath": "/music",
  "monitored": true,
  "addOptions": {
    "monitor": "all",
    "searchForMissingAlbums": true
  }
}
```

## Add Album Payload Example
```json
{
  "foreignAlbumId": "9a1c5b83-9b4a-47e6-b7bf-2a2a83bc0a37",
  "monitored": true,
  "addOptions": {
    "searchForNewAlbum": true
  }
}
```
