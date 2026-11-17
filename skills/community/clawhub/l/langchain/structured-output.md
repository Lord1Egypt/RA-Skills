# Structured Output — Schemas, Parsers, and Failure Paths

Scope: getting typed objects out of a model inside LangChain. Cross-provider constrained decoding theory is the `structured-output` skill.

## The Default Path

```python
from pydantic import BaseModel, Field

class Ticket(BaseModel):
    """A support ticket extracted from a message."""      # the docstring is sent to the model
    severity: str = Field(description="one of: low, medium, high")
    summary: str = Field(description="one sentence, no names")

structured = model.with_structured_output(Ticket)
ticket = structured.invoke("my payment failed twice today")
```

- Field descriptions and the class docstring go to the provider as part of the schema. An undescribed field is guesswork; enums belong in the description or as a `Literal` type.
- `method=` selects the mechanism: `"function_calling"` (widest support), `"json_schema"` (strict schema enforcement where the provider offers it), `"json_mode"` (valid JSON, schema NOT guaranteed). Default in `config.yaml` is `structured_output_method`.
- Optional fields need real defaults (`Optional[str] = None`). A required field the source text does not contain forces the model to invent one.

## Always Have A Failure Path

```python
structured = model.with_structured_output(Ticket, include_raw=True)
out = structured.invoke(text)
if out["parsing_error"]:
    log(out["raw"].content)          # the actual model output — the only useful evidence
    ticket = fallback(text)
else:
    ticket = out["parsed"]
```

Without `include_raw=True`, a parse failure raises and you lose the raw text that would have explained it. With it, you get `{"raw", "parsed", "parsing_error"}` and can decide per case (SKILL.md Output Gates).

## Parsers, And When They Are Still Right

| Parser | Use when |
|---|---|
| `StrOutputParser` | You want the text; also the streaming-friendly terminator of most chains |
| `JsonOutputParser` | JSON without a strict schema, or you need partial objects while streaming |
| `PydanticOutputParser` | The model has no tool/schema support (many local models) — prompt-side only |
| `OutputFixingParser` | Repair pass over a malformed output; costs an extra model call every time it fires |
| `RetryOutputParser` | Retries with the ORIGINAL prompt plus the failure, which fixes cases the fixer cannot |
| `.with_structured_output` | Everything else — provider-side enforcement beats prompt-side pleading |

Prompt-side parsing requires the format instructions actually reaching the prompt:

```python
parser = PydanticOutputParser(pydantic_object=Ticket)
prompt = ChatPromptTemplate.from_template(
    "Extract a ticket.\n{format_instructions}\n\n{text}"
).partial(format_instructions=parser.get_format_instructions())
```

Forgetting `.partial(...)` is the most common cause of "the parser never works": the model was never told the format. Note the instructions contain literal braces — passing them as a variable, as above, avoids the escaping problem (SKILL.md Core Rule 2).

## Diagnosing A Failure

1. Read the raw output. Three distinct diseases: prose wrapped around correct JSON, a fenced code block, or a near-miss schema (right keys, wrong types).
2. Prose or fences → switch to `with_structured_output` / tool calling; do not add a regex.
3. Type mismatches (`"3"` vs `3`, a list where an object was declared) → tighten the field description and add an example in the prompt.
4. Empty or `None` result → the model refused or produced an empty tool call; check `finish_reason` and whether `max_tokens` truncated it mid-object.
5. Only under load → truncation from `max_tokens`, or a fallback model with weaker schema support silently substituting.

## Schema Design That Survives Contact

- Flat beats nested. Every level of nesting is another chance to mis-nest; two calls with flat schemas often beat one deep schema.
- Give the model an escape: `confidence` or `unknown_fields`, so it does not fabricate to satisfy a required field.
- Enums as `Literal["low","medium","high"]` — validated locally, so a hallucinated value fails fast instead of flowing into a comparison.
- Lists of objects are where token budgets explode: cap the count in the description ("at most 10 items") and validate the length.
- Pydantic v2 is the assumption in current versions. A v1 `BaseModel` (including one imported from a library that still bundles v1) produces a `ValidationError` that reads like a model failure.

## Validation Beyond The Schema

The schema proves shape, not truth. For extraction that feeds anything consequential, add a cheap deterministic check after parsing — dates parse, ids exist in your database, numbers sum. Route failures back for one retry with the specific complaint, and stop after that: a second failure means the input, not the model, is the problem.
