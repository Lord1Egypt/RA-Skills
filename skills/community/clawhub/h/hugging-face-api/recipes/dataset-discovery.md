# Recipe — Dataset Discovery

## Goal

Find and inspect datasets on the Hugging Face Hub for training, evaluation, or RAG corpora.

## When

You need data for a model, a benchmark, or a knowledge base, and want to discover what exists.

## Inputs

- A topic / keyword.
- Optional: desired size, language, license.

## Steps

1. **Search (free).** `hf_search_datasets` with a `search` term and small `limit`.
2. **Inspect (free).** Use `hf_request` to fetch full details for a candidate: `{"api":"hub","path":"/api/datasets/{id}"}`. Check `cardData.license` and structure.
3. **Decide.** Confirm license and suitability before downstream use.

## Output

A shortlist of datasets with their ids and licenses.

## Example

```json
{ "tool": "hf_search_datasets", "arguments": { "search": "question answering", "limit": 5 } }
```

```json
[{ "id": "rajpurkar/squad", "downloads": 98765, "likes": 540 }]
```

Inspect details:

```json
{ "tool": "hf_request", "arguments": { "api": "hub", "path": "/api/datasets/rajpurkar/squad" } }
```

```json
{ "id": "rajpurkar/squad", "cardData": { "license": "cc-by-sa-4.0" } }
```

## Edge cases

- **No results**: broaden the search term or drop filters.
- **Gated dataset**: access may require accepting terms.
- **License mismatch**: if the license forbids your use, pick another dataset.

## Production notes

- Dataset discovery is **free** (Hub) — explore broadly.
- Record the dataset id and license alongside any derived artifacts for provenance.
- Re-check the license before redistribution or commercial use.
