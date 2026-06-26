# Multilingual Semantic Bridge

A bridge method for cases where the user is clear, the answer already exists, but retrieval still misses because the wording and the stored technical target do not line up well enough.

## The user problem first

One phrasing hits.
Another phrasing misses.
A synonym misses.
A more natural sentence misses.
A different language misses.

That does not always mean the answer is absent.
Very often it means the retrieval path did not connect the user's wording to the right technical target.

This skill is meant to reduce that gap.

## Example user languages
Typical outward-facing examples for this project include:
- Chinese
- French
- Japanese
- Korean
- Spanish
- Russian
- Arabic
- English mentioned separately when helpful

## What this skill does

This skill is the **core bridge method**.
It helps the assistant:
- preserve the original wording
- recover canonical intent
- map the phrasing to the system's terminology
- route toward the right technical target

## Relationship to the plugin

The plugin is the lighter automatic entry point.
This skill is the deeper method.

So:
- this skill works on its own
- the plugin can make activation more automatic
- the strongest current setup is **skill + plugin together**

## Where vector retrieval fits

This skill is highly relevant to semantic search, vector retrieval, and memory retrieval.
But it is not the vector database itself.
It is the bridge layer that helps retrieval hit the right target more often.

## Public links
- GitHub: https://github.com/ChriX-Goh/multilingual-semantic-bridge
- ClawHub skill: https://clawhub.ai/chrix-goh/multilingual-semantic-bridge
