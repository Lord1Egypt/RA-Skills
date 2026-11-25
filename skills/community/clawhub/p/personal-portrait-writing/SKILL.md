---
name: personal-portrait-writing
description: Write a personal portrait from the subject's own writings, structured by character lines instead of chronology, with every quote verified verbatim against its source. Use when the user asks for a portrait, profile, or character sketch of a person built from their own writings. Generic version for any agent.
license: MIT-0
metadata:
  version: "1.0.0"
---
# Personal Portrait Writing

A portrait captures character, not a résumé. Build it from the subject's own words, structure it by character lines instead of chronology, and verify every quote word for word against its source.

## A portrait is not a résumé

- A portrait is about the person, not their career history.

- Career takes up only a short section at the end. Everything before it is character, daily life, and how they see the world.

- Do not turn the portrait into a chronological list of events. Dates belong in the source notes after quotes, never as the structure.

## Collect the materials first

- Before writing, proactively ask the user for three kinds of material. Do not wait for them to think of it:
  1. The subject's own social accounts: blogs, tweets, social posts, daily practice notes, letters. Account names, export files, and archive links all count. Prefer official exports when available — they are far more complete than public scraping.
  2. Web-search leads: search the name, screen names, former names, company names, and project names for third-party coverage, event photos, photos taken by others, meeting records, and interviews. Search what others wrote about the subject, not only the subject's own accounts.
  3. Materials the user hands over directly: summaries, documents, diaries, manuscripts, photos, files. Take them in and ask which may be used and which are private and off the record.
- Once the three kinds are in, research and compile before writing: check, deduplicate, sort along a timeline, and write a source list. Do not start writing until the materials are in hand.

## Distill the character lines first

- Read all the material before writing. Do not search and write at the same time.

- Distill three or four character lines from the material. Each line is one sentence that sums the person up.

- Keep only the material that illuminates a line. Cut anything that does not, however interesting it is.

- Contradictions are the skeleton. Put both sides of the same person next to each other instead of picking one side.

## Mine the material

- Start from the subject's own words: blogs, social posts, tweets, daily notes, letters.

- Third-party coverage is background only, never the backbone of the portrait.

- Reposted text and other people's words quoted by the subject do not count as the subject's own words. Do not present them as such.

- If the subject left too little in writing, ask the subject. Do not invent.

## Write with representative episodes and details

- One section, one character line, one or two scenes per section.

- Slow the camera down on a scene: time, place, action, and the subject's own words — not just the facts.

- One detail beats ten facts. A flower, a child's question, a doorbell rung by mistake can carry a scene.

- Do not list facts. Do not write a chronological log of what happened in which year and month. Cut any fact that cannot dissolve into a scene.

## Verify every quote word for word

- Every quote must be found in the original text. Do not change a single word from memory.

- Search the source files with your shell tool and read the surrounding context with your file-reading tool. Confirm the source before writing the quote into the portrait.

- Search both simplified and traditional Chinese. Searching only one form will miss originals.

- Read the whole line before quoting. Do not quote from a half-line caught in a search snippet.

- Tentative wording is not a conclusion. Do not write a question as a decision.

- Do not add a place, time, or cause that is not in the original.

- A post's date is the date it was published, not the date of the event it recalls. For recollections, use the years the subject themselves gives. Do not treat the publishing year as the event year.

- Do not present second-hand accounts as facts.

- Attach the source after each quote — date plus title — so anyone can check it.

## Accept the subject's corrections

- When the subject corrects something, fix it everywhere. Fixing it in one place is the same as not fixing it.

- When the subject rejects a characterization, delete the whole passage. Do not keep it alive under different wording.

- Write titles and roles the way the subject describes them, not as second-hand sources word them.

- When the subject says something is not so, take their word. Do not go checking again.

## Privacy

- Do not write private matters the subject mentioned in passing into any file, unless they ask for them to be recorded.

- Money, donations, and private keys do not go into the portrait unless the subject asks for them.

## Self-check before delivery

- Read the whole text again against the originals and cut anything overstated.

- Append the list of quote sources at the end, with the date and title of every quote.

- When handing it to the user, say what was changed, what was deleted, and why.

## Example

Subject (invented): Mara, a night-shift nurse. Material: her diary and a message to her mother.

Material: "March 3 — The ward was quiet after 2 a.m. I refilled the water jug at bed 7 twice. Nobody noticed, nobody needs to." / "June 18 — My mother asked why I never take the day shift. I said the night lets me think."

Character line distilled: "She does the work nobody sees, and calls that enough."

Scene written: "At two in the morning the ward goes quiet, and Mara does her rounds with a water jug. She refills bed 7 twice. 'Nobody noticed, nobody needs to,' she wrote on March 3. She never asked for the day shift. 'The night lets me think,' she told her mother on June 18."

Sources: diary, March 3; message to her mother, June 18.

## Alternatives for better results

- When the subject left too little in writing, hold one long conversation first. The conversation record becomes the material.

- Show the draft to the subject before finalizing. Finalize only after they approve.

## Available connectors

- If the task needs a service you cannot reach, look on the web for a maintained API or MCP server and set it up, or build a custom connector.
