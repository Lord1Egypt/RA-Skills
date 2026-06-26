# Job Query Templates

## Production / Film / TV

| Query | Best Source |
|-------|-------------|
| `film producer` | Indeed, ZipRecruiter |
| `video editor` | Indeed, ZipRecruiter |
| `production assistant` | Indeed, ProductionHUB |
| `documentary producer` | LinkedIn, Indeed |
| `post-production supervisor` | ZipRecruiter |
| `freelance video editor` | ProductionHUB |

## Sports Production

| Query | Best Source |
|-------|-------------|
| `sports producer` | Indeed, LinkedIn |
| `broadcast producer` | Indeed, ZipRecruiter |
| `remote producer` | Indeed |
| ` ESPN producer` | LinkedIn |
| `NBC Sports freelance` | Indeed |

## Web3 / Crypto

| Query | Best Source |
|-------|-------------|
| `blockchain developer` | Indeed, LinkedIn |
| `crypto content creator` | Indeed |
| `web3 community manager` | LinkedIn |
| `nft producer` | Indeed |

## Streaming / Digital

| Query | Best Source |
|-------|-------------|
| `streaming producer` | Indeed |
| `ott content` | LinkedIn |
| `youtube producer` | Indeed |
| `digital content manager` | ZipRecruiter |

## Remote-Friendly Queries

Append `remote` to any query on Indeed:
```
https://www.indeed.com/jobs?q=film+producer+remote&l=Remote
```

## Cron Examples

Weekly film/job leads — every Monday 10am:
```bash
cd ~/.openclaw/skills/job-lead-radar && python scripts/scrape.py all "film producer" >> logs/weekly.log 2>&1
```

Daily sports production — every morning:
```bash
cd ~/.openclaw/skills/job-lead-radar && python scripts/scrape.py all "sports producer" >> logs/daily_sports.log 2>&1
```

One-shot — film + sports combined:
```bash
python scripts/scrape.py indeed "film producer"
python scripts/scrape.py ziprecruiter "sports producer"
```
