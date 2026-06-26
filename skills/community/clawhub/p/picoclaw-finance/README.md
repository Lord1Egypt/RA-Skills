# LinkedIn Jobs Scraper Skill

Skill para extrair vagas de emprego do LinkedIn usando a API pública. Funciona em VPS sem navegador, sem necessidade de login.

## Instalação

```bash
pip install requests beautifulsoup4
```

## Funcionalidades

- 🔍 **Busca rápida** — título, empresa, localização em segundos
- 🏢 **Filtro por empresa** — vagas de uma empresa específica
- 💰 **Filtro por salário** — salário mínimo em USD
- 🏭 **Filtro por indústria** — setor específico
- 📅 **Ordenação** — por data ou relevância
- 📄 **Detalhes completos** — descrição, senioridade, tipo
- 💾 **Exportação** — CSV ou JSON

## Uso Básico

```bash
# Via CLI
python scraper.py \
  --keywords "python developer" \
  --location "Brazil" \
  --remote only \
  --salary-min 80000 \
  --sort date \
  --limit 20 \
  --output jobs.csv
```

```python
# Via Python
from scraper import LinkedInJobsScraper

scraper = LinkedInJobsScraper()

jobs = scraper.search_jobs(
    keywords="data scientist",
    location="United States",
    remote="only",
    experience="mid-senior",
    salary_min=100000,
    company="1441",
    sort="date",
    limit=25
)

scraper.save_to_csv(jobs, "jobs.csv")
```

Veja `SKILL.md` para documentação completa.