# Structured story forecast prompt

Use this optional prompt after `context build`. It is a thinking aid, not a
source of facts and not a replacement for blueprint validation.

```text
You are forecasting one chapter from the supplied Context Ticket.

Chapter: <chapter-id>
Project profile: <voice, genre, and format fields>
Engine Snapshot: <selected card IDs and source hashes>
Blueprint: <goal, scenes, dependencies, and settlement expectations>
Prior Settlement: <accepted changes and unresolved questions>

Produce two or three possible paths. For each path, state:
1. which declared character choice starts it;
2. what information or resource changes;
3. which hook or relationship moves;
4. what cost and next question remain.

Do not invent facts outside the ticket. Mark any assumption as an assumption.
Do not imitate an author or copy existing prose. The builder chooses a path and
updates the blueprint before writing.
```
