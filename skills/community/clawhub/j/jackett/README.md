# Jackett Skill

Search torrent indexers through Jackett from OpenClaw-style workflows.

## What It Does

- Search releases across all configured indexers or a specific indexer
- Run typed Torznab searches for TV, movies, music, and books
- Inspect available indexers
- Inspect indexer capabilities before choosing search parameters
- Return parsed JSON for search results, or raw XML when needed

## Setup

### 1. Find Your Jackett URL And API Key

Jackett default URL is usually:

```bash
http://localhost:9117
```

In the Jackett web UI, open the dashboard and copy the API key.

### 2. Create Credentials File

```bash
mkdir -p ~/.openclaw/credentials/jackett
cat > ~/.openclaw/credentials/jackett/config.json << 'EOF'
{
  "url": "http://localhost:9117",
  "apiKey": "your-jackett-api-key"
}
EOF
```

### 3. Test It

```bash
./skills/jackett/scripts/jackett-api.sh indexers --configured true
```

## Usage Examples

### Inspect indexers

```bash
jackett-api.sh indexers
jackett-api.sh indexers --configured true
jackett-api.sh caps --indexer nyaasi
```

### Search all indexers

```bash
jackett-api.sh search "ubuntu 24.04"
jackett-api.sh search "dune 2024" --limit 10
```

Results are safely capped at `20` by default; use `--limit` and `--offset` to page through more items.

### Search one indexer or filter

```bash
jackett-api.sh search "frieren" --indexer nyaasi
jackett-api.sh search "arch linux" --indexer "tag:public,lang:en"
```

### Query normalization rules

- Prefer English titles for movies, shows, albums, and books
- Prefer common release keywords instead of natural-language descriptions
- Start with core terms, then add `2160p`, `remux`, `x265`, `dv`, `hdr`, `atmos` as needed

Examples:

```bash
# Less reliable
jackett-api.sh search "avatar dolby vision version" --indexer therarbg

# Recommended
jackett-api.sh search "avatar dv" --indexer therarbg
jackett-api.sh search "avatar the way of water 2160p dv atmos" --indexer therarbg
```

### Typed Torznab searches

```bash
jackett-api.sh tvsearch --query "The Last of Us" --season 1 --ep 2
jackett-api.sh movie --query "Dune Part Two" --year 2024
jackett-api.sh music --artist "Daft Punk" --album "Discovery"
jackett-api.sh book --title "The Pragmatic Programmer"
```

### Raw XML

```bash
jackett-api.sh search "foundation s02" --raw
jackett-api.sh caps --indexer nyaasi --raw
```

## Environment Variables (Alternative)

Instead of a config file, you can set:

```bash
export JACKETT_URL="http://localhost:9117"
export JACKETT_API_KEY="your-api-key"
```

## Troubleshooting

**"JACKETT_URL must be set"**  
→ Check your config file exists at `~/.openclaw/credentials/jackett/config.json`

**"JACKETT_API_KEY must be set"**  
→ Copy the API key from the Jackett dashboard and place it in the config file

**Connection refused**  
→ Make sure Jackett is running and reachable on the configured port

**No results returned**  
→ Check whether the target indexer is configured and supports the selected search mode

**Need indexer-specific parameters**  
→ Run `jackett-api.sh caps --indexer <name>` to inspect that indexer's capabilities first

**Output too large**  
→ Narrow with `--indexer` / `--cat`, or page with `--limit` and `--offset` instead of requesting everything at once
