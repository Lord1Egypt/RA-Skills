# Examples

## Example 1: New project bootstrap

User intent:
- “我想新建一本小说。”

Good response shape:
- confirm what is already known and what is missing
- stop at the bootstrap gate if title / genre / audience / length / taboo list / premise / execution mode are not locked
- ask for the missing items instead of inventing defaults
- create the project scaffold only after the required inputs are confirmed

## Example 1b: Take over an old draft project

User intent:
- “这是我写到一半的小说，帮我接管。”

Good response shape:
- treat it as resume/bootstrap hybrid, not a clean new start
- capture resumeFrom, resumeMode, and latestChapterIndex in the scaffold
- create a resume note or checkpoint summary
- do not reset canon just because the project is being scaffolded again
- ask for the last stable chapter or truncation if it is not provided

## Example 2: Style sampling request

User intent:
- “先给我 5 种文风试写，之后我选一种统一全书。”

Good response shape:
- verify the premise and core tone are already locked
- state the fixed scene
- provide 5 clearly different excerpts
- label each style
- end with a short comparison grid in bullets
- ask the user to pick one

## Example 3: Single chapter writing request

User intent:
- “写第 12 章。”

Good response shape:
- confirm the current batch outline and relevant canon slice already exist
- chapter goal
- batch outline used
- draft
- review notes
- revision summary
- memory update

## Example 4: Multi-chapter continuation

User intent:
- “从第 20 章写到第 23 章。”

Good response shape:
- confirm batch size (10 chapters)
- confirm the chapter plan exists for the batch
- show batch outline for the batch
- draft batch 1
- review and archive
- checkpoint before batch 2

## Example 5: Fixing drift

User intent:
- “角色写偏了，帮我拉回来。”

Good response shape:
- identify the exact drift
- show the canonical behavior
- suggest the smallest fix
- if the fix would change hard canon, ask the author before retconning
- avoid rewriting unrelated chapters

## Example 6: Truncated draft resume

User intent:
- “上次写到一半断了，接着写。”

Good response shape:
- identify it as resume mode, not a fresh chapter task
- read the last stable checkpoint, outline, recent summaries, and partial draft first
- summarize the recovered state in 3–5 bullets
- state what is known and what remains unknown
- continue from the last stable sentence or beat
- do not rewrite earlier unrelated text
- if the fragment is too short to infer the scene safely, ask for the missing paragraph or chapter summary instead of inventing a bridge
