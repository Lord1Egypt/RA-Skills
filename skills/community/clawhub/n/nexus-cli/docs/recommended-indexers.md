# Recommended Indexers

Admirarr ships with a curated list of public indexers that provide good coverage across movies, TV, and anime. These are configured in Prowlarr via `admirarr indexers setup` or `admirarr indexers sync`.

The `admirarr status` command checks whether these are configured and flags any that are missing.

## Indexer List

### General (Movies + TV)

| Indexer | FlareSolverr | Notes |
|---------|-------------|-------|
| 1337x | Yes | Largest general public torrent index |
| The Pirate Bay | No | Resilient, wide content coverage |
| TorrentGalaxy | No | Good secondary general indexer |
| Knaben | No | Meta-search aggregator, queries multiple sources |

### Movies

| Indexer | FlareSolverr | Notes |
|---------|-------------|-------|
| YTS | No | Compact encodes (720p/1080p), good for limited storage |

### TV

| Indexer | FlareSolverr | Notes |
|---------|-------------|-------|
| EZTV | No | Largest public TV-focused indexer |

### Anime

| Indexer | FlareSolverr | Notes |
|---------|-------------|-------|
| Nyaa.si | Yes | Primary anime tracker, largest selection |
| SubsPlease | No | Simulcast releases, fast for new episodes |
| Anidex | Yes | Secondary anime tracker |
| Tokyo Toshokan | No | Japanese media aggregator |

## FlareSolverr

Indexers marked with FlareSolverr require Cloudflare bypass. If FlareSolverr is not running, these indexers will be added in a disabled state. Configure FlareSolverr as an indexer proxy in Prowlarr to enable them.

## Customization

You can override which indexers are active in `~/.config/admirarr/config.yaml`:

```yaml
indexers:
  1337x:
    flare: true
  YTS: {}
  "Nyaa.si":
    enabled: false   # disable without removing
    flare: true
```

Run `admirarr indexers sync` to converge Prowlarr to match your config. Indexers not listed in the config will be removed during sync (only known/recommended ones — custom indexers are left untouched).

## Adding Custom Indexers

Indexers not in this list can be added directly in the Prowlarr UI. Admirarr will not touch indexers it doesn't recognize during sync operations.
