# Prompts — Templates, Placeholders, Few-Shot, Storage

Scope: the LangChain mechanics of building prompts. What to write inside them is the `prompting` skill.

## Templates

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer only from the context. Say you do not know otherwise."),
    ("placeholder", "{history}"),           # shorthand for MessagesPlaceholder
    ("human", "Context:\n{context}\n\nQuestion: {question}"),
])
```

- `ChatPromptTemplate` for chat models, `PromptTemplate` for completion models. Passing a `PromptTemplate` to a chat model wraps everything into one human message and quietly loses the system instruction.
- `MessagesPlaceholder("history", optional=True)` lets a chain run without history on the first turn; without `optional`, a missing key raises.
- Templates are Runnables: `prompt.invoke(vars)` returns the message list, and `prompt | model` is a chain. Inspect before blaming the model: `prompt.invoke(vars).to_string()`.
- `prompt.input_variables` lists what it demands — this is where a phantom variable from an unescaped brace shows up (SKILL.md Core Rule 2).

## Escaping And Template Formats

- Default format is f-string: every literal `{` must be `{{`. JSON examples, code samples, and regex in a prompt are the usual casualties.
- Cleanest fix: pass the example as a variable instead of embedding it. A variable's VALUE is never re-parsed for braces, so no escaping is needed.
- `template_format="jinja2"` avoids brace collisions but renders templates as code. Never build a jinja2 template from user input — it is a code-execution surface, not a formatting convenience.
- Never build prompts with f-strings over user input: you lose the schema check, the trace shows one opaque blob, and the input can silently reshape the instructions.

## Partials

```python
prompt = base.partial(format_instructions=parser.get_format_instructions())
prompt = base.partial(today=lambda: date.today().isoformat())   # callable = evaluated per call
```

- A partial value fixed at build time (format instructions, tenant name) removes it from `input_variables`, so the chain no longer needs it passed.
- Use the callable form for anything time-dependent. A date baked in at import time is wrong from the second day, and — because it changes the prompt string — a static one is also what keeps the response cache warm.

## Few-Shot

```python
from langchain_core.prompts import FewShotChatMessagePromptTemplate

example_prompt = ChatPromptTemplate.from_messages([("human", "{input}"), ("ai", "{output}")])
few_shot = FewShotChatMessagePromptTemplate(examples=examples, example_prompt=example_prompt)
prompt = ChatPromptTemplate.from_messages([("system", "…"), few_shot, ("human", "{input}")])
```

- Examples as real human/AI message pairs beat examples pasted into the system prompt: the model reads them as demonstrated turns and imitates the shape.
- Format matters more than count: a handful of examples in one identical shape outperforms a longer bank whose formatting drifts, because drift teaches the model that the shape is optional. Every example is also resent on every request — few-shot is a permanent token bill, so add one only to fix an observed failure.
- Cover the edge cases you care about, especially the refusal or empty-result case. A model that has never seen "no answer found" in an example will invent one.
- Dynamic selection when the example bank is large: `SemanticSimilarityExampleSelector` (backed by a vector store) picks the k most similar to the current input; `LengthBasedExampleSelector` fits as many as the budget allows. Both replace `examples=` with `example_selector=`.
- With a schema-constrained call, few-shot is usually unnecessary — the schema already carries the format (SKILL.md Choosing The Abstraction).

## Where Prompts Live

| Option | Fits | Cost |
|---|---|---|
| Inline in code | Small apps, prompts that change with the code | Diffable and reviewable; no way to change one without a deploy |
| YAML/text files loaded at startup | Non-engineers editing copy | Needs a schema check at load, or a typo ships as a missing variable |
| A prompt registry/hub | Teams iterating faster than they deploy | Network dependency at startup and an untracked change surface; pin versions |

Whichever you choose: version prompts, and treat a prompt edit as a code change that must pass the eval set before shipping. There is no compiler for prose.

## Dynamic Prompts

- Per-request variation belongs in variables, not in string surgery: one template with a `{tone}` or `{persona}` variable stays inspectable and cacheable.
- For an agent, per-step instruction changes belong in a `before_model` middleware hook so they apply on every pass of the loop, not just the first.
- Do not concatenate retrieved documents into the system message. Keep them in a delimited context variable in the human turn, so an injected instruction inside a document does not read as system policy.

## Checks Before Shipping A Prompt

- `prompt.input_variables` matches exactly what the chain passes — no extras, no phantoms.
- Rendered output inspected once with real data (`prompt.invoke(vars).to_string()`), not just the template.
- Every literal brace doubled, or the content passed as a variable.
- Untrusted text confined to a delimited block, with the instruction that it is data, not instructions.
- Few-shot examples counted against the token budget at expected traffic.
