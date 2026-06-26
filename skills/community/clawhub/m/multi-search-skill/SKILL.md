---
name: multi-domain-search
description: Search 8 knowledge domains in one query — live web, 250M academic papers, 150M scholarly works, arXiv preprints, 36M biomedical papers, chemical compounds, government datasets, and dictionary. Goes beyond web search into academic, scientific, and public data via x402.
version: 1.0.0
homepage: https://github.com/plagtech/multi-domain-search-skill
metadata:
  openclaw:
    primaryEnv: RESEARCH_API_KEY
    envVars:
      - name: RESEARCH_API_KEY
        required: true
        description: API key or x402 subscription key for the gateway.
      - name: RESEARCH_GATEWAY_URL
        required: false
        description: Gateway URL. Defaults to https://gateway.spraay.app
    requires:
      bins:
        - curl
        - python3
---

# Multi Domain Search

Search across 8 knowledge domains from a single agent — not 8 web engines, 8 completely different databases. One query can search the live web, academic papers, preprints, biomedical literature, chemical compounds, scholarly works, government datasets, and the dictionary simultaneously.

## How to call endpoints

```bash
bash {baseDir}/scripts/search.sh METHOD ENDPOINT '{"key":"value"}'
```

## Search strategy

When the user asks you to search for something, decide which domains are relevant and fan out across them. Don't search every domain for every query — be smart about it.

**General knowledge questions** — start with `web_search` and `web_qna`, add `scholarly_search` if the topic has academic depth.

**Scientific or medical questions** — lead with `biomedical_search` and `papers_search`, supplement with `preprints_search` for cutting-edge work, then `web_search` for recent news coverage.

**Chemistry questions** — start with `chemistry_compound`, then `biomedical_search` for related drug/pharma research, then `papers_search` for fundamental science.

**Data and statistics** — check `demographics_datasets` for government data, `scholarly_search` for published studies with data, `web_search` for recent reports.

**Word meanings and language** — use `dictionary_define` and `dictionary_synonyms` for precise definitions, then `web_search` for usage context.

**Comprehensive research** — fan out across all relevant domains, then synthesize. Start broad, then drill into the most promising domain.

Always tell the user which domains you searched and what each returned. Cite sources with DOIs, PMIDs, URLs, or arXiv IDs.

## Available search domains (8 engines, 15 endpoints)

### 1. Live Web (Tavily)

**Web Search** — $0.02
Search the live web. Returns ranked URLs with titles and snippets.
```bash
bash {baseDir}/scripts/search.sh POST /api/v1/search/web '{"query":"CRISPR gene therapy 2026 breakthroughs"}'
```

**Web Extract** — $0.02
Extract clean text from URLs found via web search.
```bash
bash {baseDir}/scripts/search.sh POST /api/v1/search/extract '{"urls":["https://example.com/article"]}'
```

**Web Q&A** — $0.03
Direct answers from the web with sources. Best for factual questions.
```bash
bash {baseDir}/scripts/search.sh POST /api/v1/search/qna '{"query":"How many people use AI tools for research in 2026?"}'
```

### 2. Academic Papers (OpenAlex — 250M papers)

**Search Papers** — $0.002
Full-text search across 250 million academic papers. Returns titles, abstracts, authors, DOIs, citation counts.
```bash
bash {baseDir}/scripts/search.sh GET /api/v1/research/papers/search '{"query":"transformer attention mechanisms"}'
```

**By Author** — $0.002
Find all papers by a specific researcher.
```bash
bash {baseDir}/scripts/search.sh GET /api/v1/research/papers/by-author '{"author":"Geoffrey Hinton"}'
```

**Trending** — $0.002
Discover what's trending in any research field right now.
```bash
bash {baseDir}/scripts/search.sh GET /api/v1/research/papers/trending '{"topic":"large language models","days":7}'
```

### 3. Scholarly Works (Crossref — 150M works)

**Search Scholarly** — $0.002
Search across 150 million works — books, conference papers, datasets, journal articles, and more. Broader than OpenAlex.
```bash
bash {baseDir}/scripts/search.sh GET /api/v1/research/scholarly/search '{"query":"reinforcement learning from human feedback"}'
```

**Journal Info** — $0.001
Look up journal metadata, impact, and subject areas by ISSN.
```bash
bash {baseDir}/scripts/search.sh GET /api/v1/research/scholarly/journal-info '{"issn":"0028-0836"}'
```

### 4. Preprints (arXiv)

**Search Preprints** — $0.002
Search arXiv for the latest preprints before they're formally published. Cutting-edge research.
```bash
bash {baseDir}/scripts/search.sh GET /api/v1/research/preprints/search '{"query":"diffusion models image generation","category":"cs.CV"}'
```

**Recent by Category** — $0.002
Browse the latest preprints in any arXiv category.
```bash
bash {baseDir}/scripts/search.sh GET /api/v1/research/preprints/recent '{"category":"cs.AI"}'
```

### 5. Biomedical (PubMed — 36M papers)

**Search Biomedical** — $0.002
Search 36 million biomedical papers — medicine, biology, pharmacology, public health, genetics, neuroscience.
```bash
bash {baseDir}/scripts/search.sh GET /api/v1/research/biomedical/search '{"query":"mRNA vaccine long term immunity"}'
```

**Related Articles** — $0.002
Find conceptually similar papers to a known PMID.
```bash
bash {baseDir}/scripts/search.sh GET /api/v1/research/biomedical/related '{"pmid":"33116299"}'
```

### 6. Chemistry (PubChem)

**Compound Search** — $0.002
Search PubChem by compound name, formula, or CID. Returns structure, properties, identifiers.
```bash
bash {baseDir}/scripts/search.sh GET /api/v1/research/chemistry/compound '{"query":"ibuprofen"}'
```

**Similar Compounds** — $0.002
Find structurally similar compounds for drug discovery and chemical research.
```bash
bash {baseDir}/scripts/search.sh GET /api/v1/research/chemistry/similarity '{"cid":"2244"}'
```

### 7. Government Data (Data.gov + Census)

**Dataset Search** — $0.001
Search open government datasets across Data.gov.
```bash
bash {baseDir}/scripts/search.sh GET /api/v1/research/demographics/datasets '{"query":"renewable energy production by state"}'
```

**Census Data** — $0.001
US Census data by state, county, or zip code. Population, income, education, housing.
```bash
bash {baseDir}/scripts/search.sh GET /api/v1/research/demographics/census '{"location":"California"}'
```

### 8. Dictionary

**Define** — $0.001
Full definition with phonetics, part of speech, and examples.
```bash
bash {baseDir}/scripts/search.sh GET /api/v1/research/dictionary/define '{"word":"epistemology"}'
```

**Synonyms** — $0.001
Synonyms and antonyms. Also useful for expanding search queries across other domains.
```bash
bash {baseDir}/scripts/search.sh GET /api/v1/research/dictionary/synonyms '{"word":"innovative"}'
```

## Cost per domain

| Domain | Endpoints | Cost per call |
|--------|-----------|---------------|
| Live Web | 3 | $0.02–$0.03 |
| Academic Papers | 3 | $0.002 |
| Scholarly Works | 2 | $0.001–$0.002 |
| Preprints | 2 | $0.002 |
| Biomedical | 2 | $0.002 |
| Chemistry | 2 | $0.002 |
| Government Data | 2 | $0.001 |
| Dictionary | 2 | $0.001 |

A typical multi-domain search across 3-4 domains costs $0.006–$0.04.

Data sourced from Tavily, OpenAlex, Crossref, arXiv, PubMed, PubChem, Data.gov, US Census Bureau.
