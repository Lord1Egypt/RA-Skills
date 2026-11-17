# Jev with LangChain

Use Jev as the typed control layer around a LangChain agent. The chat model
still handles open-ended planning, explanation, and generation; Jev handles
small bounded judgments such as routing, tool-risk classification, completion
checks, or escalation.

## Package and stability

The official integration is the optional Python package
[`langchain-typesafe`](https://pypi.org/project/langchain-typesafe/). Install
the experimental agent middleware extra only when you need middleware:

```bash
python -m pip install "langchain-typesafe[experimental]"
```

The classifier is a beta/alpha-style integration and the middleware namespace
is explicitly experimental. Pin and test versions in production; do not make
the Jev call the only authorization layer.

## Direct typed classification

`TypeSafeClassifier` is a LangChain Runnable. It accepts text, structured JSON,
or LangChain messages as `state` and returns typed response objects:

```python
from langchain_typesafe import Choice, Noul, Score, TypeSafeClassifier

classifier = TypeSafeClassifier(model="jev-latest")
response = classifier.invoke(
    {
        "state": {
            "message": "The deploy failed twice and customers see 500s.",
            "service": "checkout",
        },
        "questions": {
            "urgent": Noul(instructions="Does this need attention right now?"),
            "team": Choice(
                instructions="Which team should handle this?",
                criteria={
                    "infra": "Outages, deployments, or reliability failures.",
                    "product": "A product behavior or feature issue.",
                    "other": "No listed team fits.",
                },
            ),
            "severity": Score(
                instructions="How severe is the customer impact?",
                criteria=["Minor", "Material", "Critical"],
            ),
        },
    }
)

if response.nouls["urgent"].noul >= 0.8:
    print("prioritize")
```

Batch independent questions in one call when they share the same state. Keep
thresholds, arithmetic, permissions, and side effects in application code.

## Model routing

`ModelRouterMiddleware` classifies the latest human message once before the
agent run, stores the complete `ChoiceAnswer` in agent state, and uses the
selected model for the run. It is not a license to switch models on every
step without measuring the extra control-plane cost.

```python
from langchain.agents import create_agent
from langchain_typesafe.experimental.middleware import (
    ModelChoice,
    ModelRouterMiddleware,
)

router = ModelRouterMiddleware(
    choices={
        "fast": ModelChoice(
            model="openai:YOUR_FAST_MODEL",
            criteria="Simple lookups, extraction, and localized changes.",
        ),
        "strong": ModelChoice(
            model="openai:YOUR_STRONG_MODEL",
            criteria="Complex debugging, architecture, or high-impact work.",
        ),
    },
    instructions="Choose the least costly model that can safely complete the task.",
)

agent = create_agent(
    "openai:YOUR_DEFAULT_MODEL",
    middleware=[router],
)
```

The model identifiers above are placeholders. Use identifiers supported by the
LangChain provider configured in your environment.

## Pre-tool risk gating

`AutoModeMiddleware` checks configured tools immediately before execution. A
risk probability at or above its threshold returns an error `ToolMessage` and
does not call the tool; unlisted tools bypass the middleware. Classifier errors
are fail-closed in the current integration, but this still does not replace
deterministic authorization.

```python
from langchain.agents import create_agent
from langchain_typesafe.experimental.middleware import AutoModeMiddleware

guard = AutoModeMiddleware(
    tools=["bash", "delete_record"],
)

agent = create_agent(
    "openai:YOUR_AGENT_MODEL",
    tools=[read_record, delete_record, bash],
    middleware=[guard],
)
```

Treat tool arguments, file contents, web pages, and model output as hostile
state. Keep path allowlists, credential boundaries, spend caps, user approval,
and irreversible-action policy in code. The Jev gate is a learned signal, not
an authorization grant. The stock middleware blocks; it does not open a human
approval UI.

## Provider-neutral policy adapter

If you are not using the optional LangChain middleware, or want a deterministic
boundary around it, import the dependency-free helpers from
[`scripts/jev_control.py`](../scripts/jev_control.py):

```python
from jev_control import assess_tool_call, judge_typed_answers, route_choice

route = route_choice(
    classifier_response,
    {"fast": "openai:gpt-4.1-mini", "strong": "openai:o3"},
    question_id="complexity",
    min_confidence=0.80,
    min_margin=0.10,
)

tool_decision = assess_tool_call(
    tool_name,
    classifier_response,
    question_id="risk",
    protected_tools={"bash", "delete_record"},
    authorized=deterministic_authorizer(tool_name, arguments),
)

grade = judge_typed_answers(classifier_response, {
    "correct": {"type": "noul", "threshold": 0.80, "weight": 2},
    "grounded": {"type": "noul", "threshold": 0.80},
    "cited": {"type": "noul", "threshold": 0.80},
})
```

The route helper recomputes confidence from the distribution and requires a
margin over the runner-up. The tool helper blocks protected tools when the
classifier fails or returns malformed output, and returns `review` when the
caller has not supplied deterministic authorization. The judge helper is an
online-eval decision, not a replacement for sampled human review.

## Local-provider boundary

`langchain-typesafe` calls the hosted TypeSafe API. It does not automatically
use this repository's `openjev`, `openjev-hf`, `localjev`, `von`, `litjev`, or
`simple-jev` providers. Those
providers remain available through `scripts/jev_harness.py` for local golden
set evaluation. If an application needs a local LangChain Runnable, wrap the
same typed request contract in an application-owned adapter and keep its
calibration report separate from hosted Jev.

## Evaluation

Evaluate two layers:

1. The decision layer: accuracy, calibration, review rate, latency, and
   adversarial/metamorphic slices using Jev Skill's harness.
2. The agent layer: whether the selected model solved the task, whether risky
   tools were blocked, whether safe tools remained usable, and whether code
   policy overrode unsafe model advice.

Do not infer agent safety from classifier accuracy alone. Keep traces and
tool-call metadata non-sensitive, and avoid sending secrets or unnecessary
conversation history to a classifier.
