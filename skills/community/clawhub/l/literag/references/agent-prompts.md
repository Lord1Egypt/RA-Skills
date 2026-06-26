# LiteRAG agent prompt templates

Use these as high-level wrappers when another agent or ACP harness should query LiteRAG without re-inventing the workflow.

## Template: answer from docs only

```text
Use LiteRAG, not builtin memory, for this documentation question.

Target library: <library-id>
Question: <user-question>

Workflow:
1. Run grouped LiteRAG search for the question.
2. Inspect the best matching range from the top result; inspect a second result only if the first is ambiguous.
3. Answer briefly from the inspected evidence only.
4. Include the source_rel_path of the file you used.
5. If evidence is weak or conflicting, say so plainly instead of bluffing.
```

## Template: retrieve exact API/property details

```text
Use LiteRAG against library <library-id>.
Find the exact API/property details for: <thing>

Required behavior:
- Search first, inspect second.
- Prefer definition blocks over References/navigation blocks.
- Return only the exact fields/properties/parameters you can support from inspected text.
- Cite the file path you used.
```

## Template: compare two concepts

```text
Use LiteRAG against library <library-id>.
Compare: <concept-a> vs <concept-b>

Workflow:
- Search for both concepts.
- Inspect the strongest hit for each.
- Return a compact comparison with one citation per side.
- Do not pad with generic background.
```

## Template: agent-executable shell form

Use this when the downstream agent should just run the wrapper script.

```text
In the workspace root, run:
python scripts/literag-query.py <library-id> "<question>" --format agent

Then answer only from the `inspect` payload when available.
If `inspect` is null, answer from the best grouped search hit and say evidence is shallow.
```

## Template: precision inspect by known path/range

```text
In the workspace root, run:
python scripts/literag-query.py inspect <library-id> <absolute-path> --start <n> --end <m> --format agent

Then answer only from that inspected range.
```

## Recommended answer style

- Keep it short
- Lead with the conclusion
- Then give 1-3 supporting facts
- End with `source: <source_rel_path>`

## Bad pattern

Do not do this:
- search 8 times with tiny wording tweaks
- answer from top snippets without inspecting
- dump raw chunks at the user
- mix LiteRAG evidence with unsupported memory guesses
