---
name: plc-job-scraper
version: "1.0.0"
description: "Automaticky vyhledává PLC, automation a SCADA pracovní nabídky z LinkedIn, Indeed a dalších job boardů. Ideální pro PLC programátory a automation inženýry hledající nové projekty."
---

# PLC Job Scraper

Automatický scraper pro PLC a automatizační pracovní nabídky.

## Použití

### Konfigurace (nastav před spuštěním)
```bash
# Cílové job boardy
export JOB_BOARDS="linkedin,indeed,glassdoor"

# Klíčová slova
export SEARCH_TERMS="PLC programmer,automation engineer,SCADA"

# Lokace (volitelné)
export LOCATIONS="Germany,Austria,Czech Republic"

# Typ úvazku
export JOB_TYPE="full-time,contract"
```

### Spuštění scrapingu
```bash
# Použij Apify Actor pro scraping
apify run caisik/plc-job-scraper

# Nebo použij web_search + web_fetch
```

### Export výsledků
```bash
# Export do CSV
python export_to_csv.py --input jobs.json --output plc_jobs.csv

# Export do Google Sheets
python export_to_sheets.py --input jobs.json
```

## Výstupní formát

Scraper vytváří JSON/CSV s následujícími poli:

| Pole | Popis |
|------|-------|
| title | Název pozice |
| company | Název firmy |
| location | Lokace |
| salary | Plat (pokud dostupný) |
| description | Popis pozice |
| url | Odkaz na inzerát |
| date_posted | Datum zveřejnění |
| job_type | Typ úvazku |
| required_skills | Požadované skills |

## Automatizace

### Cron pro pravidelný scraping
```bash
# Spusť každý den v 8:00
0 8 * * * apify run caisik/plc-job-scraper --quiet
```

### Notifikace
```bash
# Pošli Telegram zprávu s novými nabídkami
python notify.py --jobs jobs.json --telegram
```

## Tipy

- Používej proxy rotation pro避开 rate limiting
- Nastav delay mezi requesty (min 2s)
- Ukládej výsledky do Google Sheets pro snadný přístup
- Filtruj podle platového minima (např. €50k+)
- Hledej "Siemens", "S7", "TIA Portal", "Beckhoff" v popisech