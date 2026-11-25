# OpenClaw subscription edition

Use this edition for the operator's OpenClaw subscription fleet. It includes
the GPT-only palette and the provider families below. Respect the selected
main model, explicit effort and named specialist bindings. Keep the current
agent when it can complete the work; these choices do not require delegation
or switching providers merely because another model is listed.

## Current model review

Check which models your OpenClaw session can use. The
[17 November pricing review](gpt62-20261117.md#price-comparison-and-effort)
compares model generations. Use higher thinking levels when the task benefits
from more reasoning.

## Task choices

| Work | Starting choice | Effort / native control | Selection boundary |
|---|---|---|---|
| Everyday, well-defined GPT work | GPT-6.2 Sol | medium | Provisional starting point; use low for simple requests and high when sustained reasoning helps. |
| Sustained coordination and integration | GPT-6.2 Sol | high | Preserve the main agent and useful context; no forced coordinator stage. |
| Planning, review and difficult judgment | Claude Opus 5.5 or GPT-6.2 Astra | Opus high; Astra medium | Choose directly for the task and existing context. Use Opus xhigh or Astra xhigh only when the problem warrants deeper work. |
| Hard open-ended technical work and expert consultation | Claude Fable 5.2 or GPT-6.2 Astra | Fable medium/high; Astra medium | Use Fable medium for analysis/consultation and high for demanding technical execution when exposed; xhigh/max only when justified. Live account/adapter availability still needs checking. |
| Routine implementation and debugging | Claude Sonnet 5.5 | xhigh | A quality-oriented starting point for bounded coding; high suits faster, well-specified changes. |
| Complex coding and repository-wide integration | GPT-6.2 Sol or Claude Opus 5.5 | high | Preserve a suitable existing worker; max is exceptional and justified by the work. |
| Small, well-specified execution | Claude Haiku 5.5 or GPT-6 Luna | high | Haiku is the added general execution candidate; Luna remains useful for suitable narrow work and available allowance. |
| Substantial bounded execution | Claude Haiku 5.5 or GPT-6 Luna | xhigh | Choose Sonnet/Sol directly when ambiguity or integration risk needs stronger coding; do not require a failed cheap attempt. |
| Visual detection and identification | GPT-6.1 Terra | low | Fast, economical visual location; use a stronger setting only when it helps the acceptance check. |
| General screenshot/chart interpretation | GPT-6.1 Terra | medium | Use Argon when the task specifically needs more demanding visual interpretation. |
| Difficult OCR, counting and multimodal analysis | Gemini 4 Argon | high | Terra high remains a useful extraction choice; select for workload, latency and allowance. |
| Multistep browser/desktop operation | GPT-6.1 Terra | high | Opus/Sonnet or Argon are alternatives when the actual provider exposes the required image and computer-use tools. Vision accuracy alone is not GUI proof. |
| Professional work across documents and applications | Gemini 4 Argon | high | Terra high is the faster general tool-work choice; compare the required deliverable and account allowance. |
| Long-context analysis, code explanation and multimodal reasoning | Gemini 3.1 Pro | high | Include Pro as a distinct available option; its older benchmarks are not current Argon results. |
| Fast interactive summaries and structured tool work | Gemini 3.8 Flash | low for simple work; medium for tool work | Prefer shallow, checkable tasks; fast token generation does not establish low complete-task cost. |
| High-volume classification, extraction and routing | Gemini 3.5 Flash-Lite | minimal or low, when exposed | Inputs must be narrow and outputs independently checkable; not the default for autonomous administration. |
| Coding within the Cursor/Composer harness | Composer 2.5 | adaptive/provider default | Use through an already-authorized native route that advertises it; do not invent a GPT-style effort value. |
| X/web-grounded work and an additional coding/review perspective | Grok 4.7 | high; xhigh when justified | Live grounding requires actual search tools, not the model name. Low/medium remain useful for simpler work. |

These are operator-selected policies informed by published benchmarks, not
local side-by-side validation of every role. Higher effort can increase
consumption without improving quality. Haiku/Sonnet/Opus max is available for
justified work, not a routine default. Different providers' labels do not
represent equal compute budgets.

## Resolve the actual subscription route

Before dispatch, read the current OpenClaw provider catalog and the capabilities
of the actual target channel. Match model identity, provider/account, subscription
transport, tools and effort support. A listed API model or an available API key
is not evidence that a subscription covers the call.

| Family | Model identity to resolve |
|---|---|
| GPT | gpt-6.2-astra, gpt-6-luna, gpt-6.2-sol, gpt-6.1-terra |
| Anthropic | Claude Fable 5.2, Claude Opus 5.5, Claude Sonnet 5.5, Claude Haiku 5.5 |
| Cursor | Composer 2.5 |
| Grok | Grok 4.7 |
| Gemini | Gemini 4 Argon, Gemini 3.1 Pro, Gemini 3.8 Flash, Gemini 3.5 Flash-Lite |

Treat these as model identities, not universal provider-qualified config IDs.
Resolve aliases and preview suffixes from the live target. For example, a
catalog may expose Gemini Pro as gemini-3.1-pro-preview and a Grok subscription
as an ACP route, rather than their direct API IDs. Preserve that account and
transport identity. Do not use a mutable latest alias as proof of a version.

Use a requested native effort only if the channel actually supports it. Keep
Composer's adaptive control; map Gemini thinking levels and Claude/Grok effort
through the provider's documented interface. A policy preference does not
establish that an adapter forwards the parameter. Report any unsupported
setting rather than silently dropping it or pretending the target accepted it.

The operator reports access through subscriptions. Verify it on the target
without initiating a new paid route, reconnecting accounts or changing credentials.
If a model, quota or required tool is unavailable, report the exact gap and
continue independent work. Use an already-authorized alternative only where
the operator's instructions permit it; preserve explicit selections and native
refusals. Never silently fall back to OpenRouter, direct API billing or a new
subscription.

Carbon is excluded. Mythos is not interchangeable with Fable or presumed to be
included in the account. Fable 5.2 is a candidate for hard technical work;
map its medium/high/xhigh/max controls only where the actual subscription
transport supports them. The live Fable route remains unverified.
An explicit operator selection still prevails.

See the [GPT-6.2 pricing and evidence refresh](gpt62-20261117.md) and the
[6 November baseline](benchmarks-20261106.md) for the other provider families.
