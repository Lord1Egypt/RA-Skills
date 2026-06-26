# Prompt — Citation Generation

## Purpose

Convert an OpenAlex work record into a complete, traceable citation that always includes the **OpenAlex ID/URL** alongside the DOI. **No API key.**

## Reusable template

```
Build a citation from this OpenAlex work record. Use ONLY fields present in the record.

Record fields:
- Title: {{display_name}}
- Authors: {{author_display_names}}     # from authorships[].author.display_name
- Year: {{publication_year}}
- Source: {{primary_location.source.display_name}}
- DOI: {{doi}}
- OpenAlex ID: {{id}}                    # https://openalex.org/W...
- Open access: {{open_access.is_oa}} / {{open_access.oa_url}}

Output format:
{{authors}} ({{year}}). {{title}}. {{source}}. DOI: {{doi}}. OpenAlex: {{id}}
If open access, append: Open access: {{oa_url}}

Rules:
- Never invent or guess missing fields; if a field is absent, omit it and say so.
- Always include the OpenAlex ID/URL.
```

## Variables

| Variable | Source field |
|----------|--------------|
| `{{display_name}}` | `display_name` / `title` |
| `{{author_display_names}}` | `authorships[].author.display_name` |
| `{{publication_year}}` | `publication_year` |
| `{{primary_location.source.display_name}}` | source name |
| `{{doi}}` | `doi` |
| `{{id}}` | `id` (OpenAlex URL) |
| `{{open_access.is_oa}}` / `{{open_access.oa_url}}` | OA flag + link |

## Example

```
Piwowar, H. et al. (2018). The state of OA: a large-scale analysis of the prevalence
and impact of Open Access articles. PeerJ. DOI: 10.7717/peerj.4375.
OpenAlex: https://openalex.org/W2741809807
Open access: https://peerj.com/articles/4375.pdf
```

## Bad

```
"The state of OA" — a well-known 2018 paper. (no DOI, no OpenAlex ID, authors guessed)
```

Wrong: missing DOI and OpenAlex ID; authors not taken from the record; not traceable.

## Good

```
Piwowar, H. et al. (2018). The state of OA…. PeerJ.
DOI: 10.7717/peerj.4375. OpenAlex: https://openalex.org/W2741809807
```

Right: real fields only, DOI **and** OpenAlex ID, fully traceable.

> Verification needed: confirm field names with <https://docs.openalex.org>.
