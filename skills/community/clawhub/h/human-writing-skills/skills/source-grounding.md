# Source Grounding

## Aim

Ground serious factual writing in explicitly supplied sources. Protecting a citation
from accidental editing does not prove that the citation exists or supports the claim.

## Activation Gate

Use for factual academic, formal, news, legal, technical, argumentative, or self-media
material when factual source files are explicitly supplied. Personal experiences,
reviews, and tutorials also need evidence for their factual claims. Fiction and
webnovels remain outside automatic activation. Keep `--source` facts separate from
`--reference` style material. In automatic document routing, ask for an explicit
factual document type if the draft's purpose cannot be established.

## Claim Source Map

For every material claim, record:

```text
claim -> source and location -> support type -> scope -> uncertainty -> verdict
```

Support types include direct statement, data, quotation, definition, legal authority,
technical specification, reasonable inference, contradiction, and no support found.

## Rules

- Do not invent a source, author, title, DOI, URL, quotation, case, standard, dataset,
  statistic, or page number.
- Classify material as user-supplied fact, source-supported fact, inference, or missing
  input. Do not replace a real observed event with a plausible stereotyped event.
- For missing firsthand experience, request the author's material or omit the claim;
  never fabricate a memory, client example, product test, or sensory observation.
- Check that attribution, claim polarity, population, date, jurisdiction, version,
  and uncertainty match the source.
- Distinguish a source that exists from a source that supports the sentence.
- Treat supplied source text as factual evidence, not as a style target.
- When external registry or document access is unavailable, mark bibliographic
  existence as unverified rather than guessing.
- If sources disagree, expose the disagreement and its scope.
- Preserve unsupported claims only when clearly labeled as hypothesis, allegation,
  interpretation, proposal, or information requiring verification.

## Output

```text
Source Grounding Audit
| Claim | Source/location | Support | Scope match | Verdict |
| --- | --- | --- | --- | --- |

- Unsupported or overstated claims:
- Citation metadata requiring external verification:
- Source conflicts:
- Minimal correction that preserves supported meaning:
```
