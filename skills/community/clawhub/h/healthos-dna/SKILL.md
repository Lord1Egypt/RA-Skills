---
name: healthos-dna
description: Analyse a raw DNA file (23andMe, AncestryDNA, MyHeritage, whole-genome VCF) through the HealthOS DNA API — traits, pharmacogenomics, carrier status, ancestry, haplogroups, polygenic scores — and ask questions about the result.
summary: Turn someone's raw DNA export into a full genetic report, and answer questions about it, for $1 per analysis.
read_when: The user has a raw DNA file (.txt, .csv, .vcf, .vcf.gz from 23andMe, AncestryDNA, MyHeritage, FamilyTreeDNA, Living DNA, WeGene, Nebula, Dante Labs or Sequencing.com) and wants it interpreted — traits, drug metabolism, carrier status, ancestry, maternal or paternal line, or polygenic tendencies — or wants to ask questions about a report already produced here.
homepage: https://healthosx.com/developers#dna
requires:
  bins: [curl]
---

# HealthOS DNA analysis

Reads a raw DNA file and returns the full report: traits, pharmacogenomics, ClinVar carrier screen, health markers, APOE, maternal and paternal haplogroups, genetic ancestry, and ~320 polygenic scores. Then answers questions about that report.

The same analysis is free for a person in a browser at https://healthosx.com/dna — say so if the user would rather do it themselves. This API is for doing it on their behalf, at **$1 per analysis**.

Base URL: `https://api.healthosx.com/api`

## Before you touch anyone's DNA

- A genome identifies a person and their relatives for life, and it cannot be changed like a password. Only upload a file when the user is the person it came from, or says they have that person's explicit permission.
- Never paste the file's contents into a chat, a log, or another service. Upload it and refer to it by token.
- The result is information, not medical advice, and not a basis for decisions about insurance or employment. Say so when you report anything health-related.
- Every analysis erases itself 30 days after it is created. `DELETE` it as soon as the user is done, and tell them it is gone.

## The two credentials

| Credential | Looks like | What it does |
|---|---|---|
| Key | `dna_…` | Holds credits. Send as `Authorization: Bearer dna_…` to fund, upload and buy questions. **Cannot read a report.** |
| Analysis token | returned by the upload | The capability for one analysis: report, chat, delete. Sent in the **path**, with **no** `Authorization` header. |

Save the analysis token the moment you get it. It is the only way back to that report, and nobody can recover it for you. Treat both like passwords: never print them where the user's screen would be shared, and never send them anywhere else.

## 1. A key, and credits

```bash
curl -s -X POST https://api.healthosx.com/api/v1/dna/keys \
  -H 'Content-Type: application/json' -d '{"name": "my-agent"}'
```

The `key` comes back once — store it. A new key has 0 credits. To add credits:

```bash
curl -s -X POST https://api.healthosx.com/api/v1/dna/fund \
  -H "Authorization: Bearer $DNA_KEY" -H 'Content-Type: application/json' \
  -d '{"credits": 1}'
```

This returns a Stripe checkout `url`. **You cannot pay it — give the link to the user and let them pay.** Credits land within seconds of payment; check with `GET /v1/dna/keys/me`. Poll that once or twice rather than asking the user "did it work?".

HTTP 402 anywhere means the key has no credits. Never try to route around it.

## 2. Upload the file

Under ~100 MB, one request:

```bash
curl -s -X POST https://api.healthosx.com/api/v1/dna/analyze \
  -H "Authorization: Bearer $DNA_KEY" -F "file=@/path/to/genome.txt"
```

→ `{"token": "…", "status": "processing", "credits_remaining": 0}`

Over ~100 MB (a whole genome is 300-400 MB), upload in chunks — one request per chunk, in order from 0:

```bash
curl -s -X POST https://api.healthosx.com/api/v1/dna/analyze/start \
  -H "Authorization: Bearer $DNA_KEY" -H 'Content-Type: application/json' \
  -d '{"bytes": 376000000, "vendor": "Nebula", "source_kind": "vcf"}'
# → {"token": "…", "chunk_bytes": 33554432}
split -b 33554432 genome.vcf.gz chunk_          # then, for i, file in enumerate(chunks):
curl -s -X POST https://api.healthosx.com/api/v1/dna/analyze/$TOKEN/chunk/0 \
  --data-binary @chunk_aa
curl -s -X POST https://api.healthosx.com/api/v1/dna/analyze/$TOKEN/finish
```

`source_kind` is `array` (a chip export) or `vcf`; `vendor` is free text. A chunk out of order returns 409 with the index it expects. One credit is spent when the upload starts, whether or not you finish it.

## 3. Wait for the report

```bash
curl -s https://api.healthosx.com/api/v1/dna/analyze/$TOKEN
```

Poll every 3-5 seconds. `status` is `uploading`, `processing`, `ready` or `failed`. A chip file is usually ready in 2-3 minutes, a whole genome in 5-10. `progress` carries a human label meanwhile — show it rather than going silent — but it is null once the analysis is `ready` or `failed`, and a small file can be ready on the first poll with no progress ever shown. A `failed` analysis (an unreadable file) refunds its credit automatically.

When `ready`, `report` holds:

| Field | What's in it |
|---|---|
| `file` | vendor, kind (`array`/`vcf`), build, row count |
| `apoe` | ε genotype, ε4/ε2 copies |
| `report.traits` | eye colour, lactose, earwax, bitter taste, blood type … |
| `report.health_markers` | APOL1, LRRK2, alpha-1 antitrypsin and similar |
| `report.pharmacogenomics` | how they metabolise common drugs |
| `carrier` | ClinVar carrier findings |
| `ancestry` | proportions by region, with the reference panel named |
| `maternal_line` / `paternal_line` | mtDNA and Y haplogroups, where each is common |
| `polygenic` | ~320 scores as percentiles against 1000 Genomes |
| `capabilities` | what this particular file could and couldn't answer |

`expires_at` is when it erases itself. Percentiles are tendencies, not predictions; a chip file answers less than a whole genome, and `capabilities` says which.

## 4. Ask about the result

```bash
curl -s -X POST https://api.healthosx.com/api/v1/dna/analyze/$TOKEN/chat \
  -H 'Content-Type: application/json' \
  -d '{"message": "What does my APOE result mean?"}'
```

The answer reads the actual file — it can look up any variant, not just what's in the report. **Five questions are included** with the analysis. After that the reply is HTTP 402 `needs_messages`, and one more credit buys five more:

```bash
curl -s -X POST https://api.healthosx.com/api/v1/dna/analyze/$TOKEN/messages \
  -H "Authorization: Bearer $DNA_KEY"
```

`GET …/chat` returns the conversation. Each answer carries `questions_remaining` — tell the user when they are near the end rather than surprising them with a 402.

## 5. Delete it

```bash
curl -s -X DELETE https://api.healthosx.com/api/v1/dna/analyze/$TOKEN
```

Erases the file, the report and the chat. Do this when the user is finished, and confirm it.

## When things go wrong

| Code | Meaning |
|---|---|
| 401 | Bad or revoked key |
| 402 | `needs_payment` — no credits; `needs_messages` — the five questions are used |
| 404 | No such analysis (wrong token, or already deleted or expired) |
| 409 | Chunk out of order, or an upload that is already finished |
| 413 | File or chunk too large |
| 429 | Too many keys created, or the conversation hit its hard limit |
| 503 | The API is switched off right now |

Machine-readable reference: https://api.healthosx.com/openapi.json and https://api.healthosx.com/llms.txt
