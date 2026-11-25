# GPT-only edition

| Profile | Model | Effort | Use |
|---|---|---|---|
| Recommended coordination profile | `gpt-6.1-sol` | `high` | Recommended for sustained coordination, integration and open-ended execution when available; verify the actual host selection separately. |
| Planning, review and difficult decisions | `gpt-6-astra` | `medium` | Habitual Astra setting when its judgment helps. |
| Exceptional reasoning | `gpt-6-astra` | `xhigh` | Rare difficult decisions or unresolved investigations after the task warrants deeper effort. |
| Visual detection and identification | `gpt-6.1-terra` | `low` | Locate or identify elements in an image when additional reasoning does not improve the required result. |
| Visual interpretation | `gpt-6.1-terra` | `medium` | Interpret images, charts, drawings and screenshots. |
| Demanding visual extraction | `gpt-6.1-terra` | `high` | Difficult OCR, structured fields, text localization and demanding counting. |
| Multistep computer use | `gpt-6.1-terra` | `high` | Complete desktop or browser operations with several steps and verify the resulting state; use `xhigh` when the quality gain justifies the added cost and wait. |
| Professional work with tools | `gpt-6.1-terra` | `high` | Starting point for tool-based work with documents, spreadsheets, forms and applications that produces a verifiable deliverable. |
| Exceptional Terra execution | `gpt-6.1-terra` | `max` | Use when demonstrated quality gains justify the additional consumption and latency; not a habitual default. |
| Bounded subtask | `gpt-6-luna` | `high` | Narrow, well-specified work with clear ownership and acceptance checks. |
| Defined execution | `gpt-6-luna` | `xhigh` | Implementation or transformation with a concrete outcome and verification. |
| Substantial execution | `gpt-6-luna` | `max` | Justified when deeper effort materially helps a bounded implementation with observable proof. |

GPT-6.1 Sol high is also available for demanding coding. Use xhigh or max
when the particular task warrants the additional reasoning and wait, rather
than forcing an Astra escalation. Keep high as the coordination default.

Prefer Terra when visual interpretation or operating applications is central
to the work. Keep Luna for suitable bounded execution, Sol for coordination,
integration and complex coding, and Astra when difficult judgment warrants it.
A workflow involving a screenshot does not by itself require Astra. Select
effort for the particular workload and the required accuracy, cost and latency;
do not apply one effort to every Terra task or infer that more reasoning always
improves the result. These profiles do not override a fixed specialist binding
or the operator's selected main model and effort.


This edition recommends only GPT-6 Astra, GPT-6 Luna, GPT-6.1 Sol and
GPT-6.1 Terra. It does not recommend GPT-6 Sol, GPT-5.x or another provider.
An explicit operator selection outside this palette remains authoritative;
report the difference rather than silently rewriting it.

The [November evidence refresh](benchmarks-20261106.md) supplements the dated
launch notes. The selected efforts remain workload recommendations, not a
claim that every higher setting is better.
