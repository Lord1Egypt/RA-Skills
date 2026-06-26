---
name: linkedin-jobs-scraper
description: Web scraping skill for LinkedIn job postings using public API endpoints. Extract job data without authentication.
---

# LinkedIn Jobs Scraper Skill

Esta skill extrai vagas de emprego do LinkedIn usando a API pública não autenticada. Funciona em VPS sem navegador, apenas com `requests` + `BeautifulSoup`.

**Busca rápida** (título, empresa, local, URL) em segundos.  
**Detalhes completos** (descrição, data) sob demanda por vaga.

## ⚠️ Avisos

- **Legal**: Scraping de dados públicos é legal nos EUA (hiQ v. LinkedIn, 2022), mas viola os ToS do LinkedIn
- **Riscos**: LinkedIn pode bloquear o IP se houver excesso de requisições
- **Volume**: Limite a <100 buscas/dia para uso pessoal
- **Sem login**: Nenhuma autenticação é usada

## Uso via CLI

### Busca rápida (padrão)

```bash
python scraper.py --keywords "python developer" --location "Brazil" --limit 10
```

### Busca com filtros

```bash
python scraper.py \
  --keywords "data scientist" \
  --location "Brazil" \
  --remote only \
  --experience mid-senior \
  --job-type full-time \
  --posted last-week \
  --salary-min 80000 \
  --sort date \
  --limit 20 \
  --output jobs.csv
```

## Uso via Python

```python
from scraper import LinkedInJobsScraper

scraper = LinkedInJobsScraper()

# Busca rápida (retorna em segundos)
jobs = scraper.search_jobs(
    keywords="python developer",
    location="Brazil",
    remote="only",
    limit=25
)

# Cada job tem: title, company, location, url, job_id
for job in jobs:
    print(f"{job['title']} - {job['company']} - {job['location']}")

# Detalhes completos de uma vaga específica (1 request extra)
details = scraper.get_job_details(job_id="4413133140")
print(details['description'][:300])  # descrição completa
print(details['posted_date'])        # ex: "1 week ago"
```

## Parâmetros

| Parâmetro | Valores | Descrição |
|-----------|---------|-----------|
| `--keywords` | texto | Título ou habilidade |
| `--location` | texto | Cidade, estado ou país |
| `--remote` | `only`, `yes`, `no` | Filtro remoto |
| `--experience` | `internship`, `entry`, `associate`, `mid-senior`, `director`, `executive` | Nível |
| `--job-type` | `full-time`, `part-time`, `contract`, `temporary`, `internship` | Tipo |
| `--posted` | `last-24h`, `last-week`, `last-month`, `anytime` | Data |
| `--salary-min` | número (USD) | Salário mínimo |
| `--company` | ID numérico | ID da empresa no LinkedIn |
| `--industry` | ID numérico | ID da indústria no LinkedIn |
| `--sort` | `date`, `relevance` | Ordenação |
| `--limit` | número (default: 25) | Máx. vagas |
| `--output` | arquivo `.csv` ou `.json` | Salvar resultados |

## Dados Retornados

### Busca rápida (`search_jobs`)
```json
{
  "title": "Python Engineer",
  "company": "Nortal",
  "location": "Greater Porto Alegre",
  "url": "https://br.linkedin.com/jobs/view/python-engineer...",
  "job_id": "4413133140"
}
```

### Detalhes completos (`get_job_details`)
```json
{
  "job_id": "4413133140",
  "title": "Python Engineer - Work from home",
  "company": "Nortal",
  "location": "Greater Porto Alegre",
  "posted_date": "1 week ago",
  "description": "Full job description text...",
  "employment_type": "Full-time",
  "seniority_level": "Mid-Senior level",
  "job_function": "Engineering",
  "industries": "Software Development"
}
```

## Exemplos

```bash
# Vagas Python remotas no Brasil
python scraper.py --keywords "python" --location "Brazil" --remote only --limit 10

# Vagas de Data Scientist sênior nesta semana
python scraper.py --keywords "data scientist" --location "United States" --experience mid-senior --posted last-week --limit 5 --output ds_jobs.json

# Vagas com salário mínimo de $100k na Google, ordenadas por data
python scraper.py --keywords "software engineer" --location "United States" --company 1441 --salary-min 100000 --sort date --limit 20

# Remoto na indústria de tecnologia (ID 4)
python scraper.py --keywords "developer" --location "Brazil" --remote only --industry 4 --limit 15
```

```python
from scraper import LinkedInJobsScraper
import pandas as pd

scraper = LinkedInJobsScraper()

# Busca com salário mínimo e ordenação
jobs = scraper.search_jobs(
    "machine learning", "Europe",
    remote="yes",
    salary_min=80000,
    sort="date",
    limit=50
)

df = pd.DataFrame(jobs)
print(df['company'].value_counts().head(10))
```

## Estrutura

```
linkedin-jobs-scraper/
├── SKILL.md
├── scraper.py
├── test_skill.py
├── __init__.py
├── clawhub.json
└── README.md
```

## Dependências

```bash
pip install requests beautifulsoup4
```

`pandas` é opcional (use se quiser analisar os dados).

## Boas Práticas

- Delay de 2-5s entre requisições (automático)
- Máximo ~100 requisições/dia
- User-Agent rotacionado automaticamente
- Cache os resultados (dados públicos mudam pouco)
- Para descrições, chame `get_job_details()` só quando necessário