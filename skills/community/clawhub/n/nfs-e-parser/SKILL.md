---
name: nfs-e-parser
description: NFS-e field extractor for Brazilian agents. 100% field accuracy on São Paulo NFS-e invoices (auxiliar-nfs-e + Surya). Extracts CNPJ, prestador, tomador, valor, código do serviço, ISS. For bookkeeping, reimbursement batching, accountant handoff.
version: 0.1.1
emoji: 🧾
homepage: https://auxiliar.ai/solve/nfs-e-extraction/
metadata:
  openclaw:
    requires:
      env: []
      bins: [python3, git]
---

# nfs-e-parser

**Brazilian NFS-e (Nota Fiscal Eletrônica de Serviços) field extraction for agents.** When your Claude Code / OpenClaw agent needs to extract structured fields from a São Paulo NFS-e PDF — for bookkeeping, reimbursement, accountant handoff — install this skill + Surya OCR. **100% field accuracy (41/41 fields) on the published corpus.**

Raw OCR (Tesseract, Surya, Google Document AI) gives you text. This skill turns that text into typed JSON: `prestador_cnpj`, `tomador_cnpj`, `valor_servico`, `codigo_servico`, `codigo_verificacao`, `data_emissao`, ISS fields, retenções, and más.

## When to invoke this skill

Use `nfs-e-parser` when the agent:

- Receives a Brazilian NFS-e PDF and needs structured fields, not raw text
- Is doing bookkeeping for a Brazilian SMB
- Needs to validate CNPJ check digits before writing to a ledger
- Batches invoices for accountant handoff (tomador summary per month, total valor_servico per prestador, etc.)
- Needs the `codigo_servico` (LC 116/2003 code) for ISS reconciliation

## How it works

### Step 1. Install dependencies

```bash
# Python + Surya OCR (best accuracy, ~22s/page on CPU)
python3 -m venv .venv && source .venv/bin/activate
pip install surya-ocr 'transformers<5.0.0'

# Clone the parser (PyPI publish pending)
git clone https://github.com/Tlalvarez/Auxiliar-ai.git /tmp/auxiliar
cp /tmp/auxiliar/scripts/walkthroughs/nfs-e-extraction/parser.py ./nfse_parser.py
```

### Step 2. OCR the PDF

```bash
surya_ocr path/to/nfse.pdf --output_dir /tmp/ocr/
```

### Step 3. Parse + validate

```python
import json
from nfse_parser import parse, validate_cnpj

with open('/tmp/ocr/nfse/nfse.txt', 'r') as f:
    text = f.read()

result = parse(text)

# Validate CNPJs before writing to ledger
if result.prestador.cpf_cnpj and not validate_cnpj(result.prestador.cpf_cnpj):
    print("WARNING: prestador CNPJ check digits invalid — OCR may have misread")

if result.missing_fields:
    print(f"WARNING: missing fields: {result.missing_fields}")

print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
```

### What you get back (shape illustration with fictitious data)

> **All values in this example are fictitious and for structure illustration only.** CNPJs `11.222.333/0001-81` and `12.345.678/0001-95` are well-known test values with valid check digits but no real-world registration.

```json
{
  "numero_nota": "00000001",
  "codigo_verificacao": "ABCD-1234",
  "data_emissao": "01/01/2026",
  "hora_emissao": "12:00:00",
  "municipio_emissor": "São Paulo",
  "chave_acesso": "20260101u11222333000181",
  "prestador": {
    "nome": "EXEMPLO SERVIÇOS LTDA",
    "cpf_cnpj": "11.222.333/0001-81",
    "inscricao_municipal": "1.234.567-8",
    "endereco": "AV EXEMPLO 100, CONJ 1 - CENTRO - CEP: 01000-000",
    "cep": "01000-000",
    "municipio": "São Paulo",
    "uf": "SP"
  },
  "tomador": {
    "nome": "EMPRESA FICTÍCIA LTDA",
    "cpf_cnpj": "12.345.678/0001-95",
    "inscricao_municipal": "1.111.111-1",
    "endereco": "AV EXEMPLO 200 - CEP: 01000-001",
    "municipio": "São Paulo",
    "uf": "SP"
  },
  "valor_servico": "R$ 1.000,00",
  "iss": {
    "codigo_servico": "01234",
    "descricao_servico": "Serviço genérico de exemplo",
    "aliquota": "*",
    "valor_iss": "0,00"
  },
  "retencoes": {
    "inss": "0,00",
    "irrf": "0,00",
    "csll": "0,00",
    "cofins": "0,00",
    "pis_pasep": "0,00",
    "ipi": "0,00"
  },
  "missing_fields": []
}
```

## Example: bookkeeping batch

Agent workflow: *"For all NFS-e PDFs in the monthly folder, extract fields and produce a summary per prestador."*

```python
from pathlib import Path
import subprocess
from nfse_parser import parse, validate_cnpj
from collections import defaultdict

pdfs = Path("Contabilidade/2026/03-Março/Notas-Fiscais-Recebidas/").glob("*.pdf")
by_prestador = defaultdict(list)
warnings = []

for pdf in pdfs:
    subprocess.run(["surya_ocr", str(pdf), "--output_dir", "/tmp/ocr/"], check=True)
    text = Path(f"/tmp/ocr/{pdf.stem}/{pdf.stem}.txt").read_text()
    result = parse(text)

    if result.missing_fields:
        warnings.append((pdf.name, "missing:", result.missing_fields))
    if result.prestador.cpf_cnpj and not validate_cnpj(result.prestador.cpf_cnpj):
        warnings.append((pdf.name, "invalid CNPJ:", result.prestador.cpf_cnpj))

    key = result.prestador.cpf_cnpj or "unknown"
    by_prestador[key].append(result)

for cnpj, invoices in by_prestador.items():
    total = sum(float(r.valor_servico.replace("R$", "").replace(".", "").replace(",", ".").strip()) for r in invoices if r.valor_servico)
    print(f"{cnpj}: {len(invoices)} invoices, R$ {total:,.2f}")
```

## Eval scorecard

On a 2-doc São Paulo NFS-e corpus (private — real business documents, gitignored at source; only aggregate metrics published):

| OCR upstream | Field accuracy | Notes |
|---|:---:|---|
| **Surya** | **100% (41/41)** | Best. Preserves line-level ordering the parser relies on. |
| Google Document AI | 87.8% (36/41) | ~$0.002/page, 1000 pages/mo free tier |
| Tesseract | 63.4% (26/41) | Fastest, but retention table reorders break positional parsing |

Full methodology at https://auxiliar.ai/solve/nfs-e-extraction/

## Known limitations (v0.1)

- **São Paulo only.** Other municipalities' NFS-e forms have different layouts. Contributions welcome for Rio, Curitiba, Belo Horizonte, etc.
- **Retention values for non-zero retentions not end-to-end tested.** The current corpus has all-zero retentions (Simples Nacional prestadores). Parser handles position-based logic but hasn't been validated against non-Simples documents.
- **CPF (11-digit) vs CNPJ (14-digit) tomadores.** Both supported; CNPJ is the common case for business invoices.
- **No XML API integration.** This is a PDF-first parser. For direct Prefeitura queries, use the SP NFS-e API.

## Related

- **`auxiliar-solve`** — the meta-ranker skill that directs agents to this skill for NFS-e queries
- **`auxiliar-mcp`** — the MCP server exposing `solve_task(task_slug="nfs-e-extraction")` for in-loop queries
- **`/solve/nfs-e-extraction`** — the full methodology page: https://auxiliar.ai/solve/nfs-e-extraction/
- **`/solve/pdf-text-extraction-mcp`** — the upstream OCR ranking (for choosing the OCR engine)

## License

MIT (parser code + this skill). Your NFS-e PDFs remain yours; this parser runs locally.
