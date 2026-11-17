# ncbi_datasets — NCBI Datasets API (Genomic & Taxonomy Data)

## What this source has

The NCBI Datasets API provides structured access to genomic and taxonomic data from the National Center for Biotechnology Information. Data includes:

- Gene information (symbol, name, description, genomic context)
- Genome assemblies and annotations
- Taxonomy (organism classification)
- Protein data
- Variant data

Use ncbi_datasets for: gene lookups, organism taxonomy, genomic research, biotech due diligence, and complementing PubMed literature searches with structured biological data.

## Auth

| | |
|---|---|
| Required | none |
| Account | not needed |

Free, no key required. Higher rate limits available with NCBI API key.

## Limits

| | |
|---|---|
| Daily | — |
| Monthly | — |
| Rate | throttle to <3/sec |

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `gene` | Get gene information by symbol and organism | `symbol`, `taxon` |
| `genome` | Get genome assembly data | `accession` |
| `taxonomy` | Get taxonomy information | `taxon_id` |

## Worked examples

```bash
# Get BRCA1 gene info for human
python3 scripts/reach.py query ncbi_datasets gene '{"symbol": "BRCA1", "taxon": "human"}'

# Get genome assembly by accession
python3 scripts/reach.py query ncbi_datasets genome '{"accession": "GCF_000001405.40"}'

# Get taxonomy for an organism
python3 scripts/reach.py query ncbi_datasets taxonomy '{"taxon_id": "9606"}'
```

## Response shape

**Gene** returns:
```json
{
  "genes": [
    {
      "gene": {
        "gene_id": "672",
        "symbol": "BRCA1",
        "description": "BRCA1 DNA repair associated",
        "taxname": "Homo sapiens",
        "chromosome": "17",
        "genomic_ranges": [...]
      }
    }
  ]
}
```

**Taxonomy** returns classification hierarchy with scientific name, rank, and lineage.

## Pitfalls

- **Taxon names must match NCBI taxonomy.** Use scientific names (`Homo sapiens`) or common names (`human`). Mismatches return empty results.
- **Gene symbols are case-sensitive in some species.** Human gene symbols are uppercase (`BRCA1`), mouse is mixed case (`Brca1`).
- **Large responses.** Genome data can be very large. Use specific queries rather than broad searches.
- **Rate limits.** Without an NCBI API key, rate is limited. For heavy usage, register for a free key at https://www.ncbi.nlm.nih.gov/account/.
- **Complements PubMed.** Use PubMed for literature about a gene, NCBI Datasets for structured gene data.

## Source links

- NCBI Datasets API: https://www.ncbi.nlm.nih.gov/datasets/docs/v2/reference/rest-api/
- Gene database: https://www.ncbi.nlm.nih.gov/gene/
- Taxonomy: https://www.ncbi.nlm.nih.gov/taxonomy
