# Tools — Definition, Schemas, Errors, Safety

The tool's name, description, and argument schema ARE the prompt the model reads about it. Most "the agent won't call my tool" bugs are documentation bugs.

## Defining

```python
from langchain_core.tools import tool
from pydantic import BaseModel, Field

@tool
def search_orders(customer_id: str, status: str = "open") -> str:
    """Look up a customer's orders. Use for questions about order state, shipping, or refunds.

    Args:
        customer_id: Internal customer id, format CUS-12345.
        status: One of open, shipped, cancelled.
    """
    ...
```

- The docstring becomes the description; type hints become the schema. No docstring → no description → the model guesses.
- `@tool(parse_docstring=True)` lifts the `Args:` section into per-argument descriptions, which is where you constrain formats and enums in words.
- For anything non-trivial, declare `args_schema=MyModel` with `Field(description=...)` — richer than hints and validated before your code runs.
- Explicit name when the function name is ugly: `@tool("search_orders")`. Provider constraint: names match `^[a-zA-Z0-9_-]{1,64}$` — spaces and dots are rejected at the API, not at import.
- `response_format="content_and_artifact"` lets a tool return `(text_for_the_model, raw_object)` so a big payload stays out of the transcript while your code keeps the object.

## Writing Descriptions The Model Acts On

- State the trigger, not the implementation: "Use when the user asks about order state" beats "Wrapper around the orders API".
- Say when NOT to use it. With two similar tools, the disambiguating sentence in each description is what stops coin-flip routing.
- Name the units and formats in the argument descriptions (`ISO date`, `USD cents`, `CUS-` prefix) — otherwise the model invents plausible values.
- Stay under the canonical ceiling of ~20 tools bound to one agent (`agent-loop.md` Dynamic Tool Selection); past it, route to sub-agents or select tools per turn via middleware instead of adding another description.

## Errors

```python
from langchain_core.tools import ToolException

@tool
def fetch(url: str) -> str:
    """Fetch a URL."""
    if not url.startswith("https://"):
        raise ToolException("Only https URLs are allowed. Retry with an https URL.")
```

- A raised `ToolException` with `handle_tool_error=True` (or a string/callable) is returned to the model as a `ToolMessage` — the agent can correct itself.
- Any other exception propagates and kills the run. That is the right default for programmer errors; make the recoverable ones explicit.
- Error text is a prompt: say what to do next ("retry with an https URL"), not just what went wrong. `KeyError: 'id'` teaches the model nothing.
- Cap what a failing tool can cost: a tool that returns a 50k-character stack trace poisons every subsequent step of the loop.

## Output Size Discipline

Tool output is resent on every following step (SKILL.md cost formula). Rules that pay for themselves:

- Truncate deliberately inside the tool and say so: `f"{rows[:20]}\n… 380 more rows; refine the filter"`.
- Return the summary the model needs, not the raw API response. Dead payload = 1 − (fields used ÷ fields returned): returning 40 fields when 3 matter is 1 − 3/40 ≈ 92% waste, resent on every following step.
- Big blobs go out of band: write to a file or a store and return the handle (`content_and_artifact`).

## Safety

Arguments the model must never supply (`InjectedToolArg`), approval interrupts on destructive tools, allowlisting per role, sandboxing code-execution tools, and tools that carry injection → `security.md`.

## Testing Tools Independently

- Call `my_tool.invoke({"customer_id": "CUS-1"})` directly — it is a Runnable, so it batches, streams (if it returns a generator), and traces like any other step.
- Assert the schema the model will see: `my_tool.args_schema.model_json_schema()`. A missing description here is the bug behind "it never calls it".
- Bind and inspect without paying for a full loop: `model.bind_tools([t]).invoke("…").tool_calls` shows exactly what the model chose and with which arguments.
