# Artifact Delivery Harness

## Purpose

Check whether the skill delivered the requested artifact in the correct form.

the skill may produce strong narrative but still fail if the artifact does not match the requested output.

## Applies To

Use this harness when the user asks for:

```text
README
email
message
proposal
deck outline
script
speech
landing page
GitHub docs
social post
bio
press release
job description
copywriting
documentation
```

## Checkpoints

1. Did the user ask for an artifact or analysis?
2. Did the output provide the artifact directly?
3. Did the artifact match the requested format?
4. Did the output language match the request?
5. Did the response include unnecessary internal reasoning?
6. Did the assistant write a file when the user wanted dialogue output?
7. Did the assistant output dialogue when the user explicitly asked for a file?
8. Is the artifact clean and reusable?

## Artifact vs Analysis

If the user asks:

```text
Please give GitHub README.
Write the email.
Give me the message.
Send it in the dialogue.
```

Then output the artifact directly.

Do not lead with:

```text
Here is my analysis.
I followed the chain.
The design points are...
```

unless the user asks for analysis.

## File Output Rule

Do not save to file unless:

1. user asks to save/write/export;
2. artifact requires file generation;
3. workflow context already established file exchange.

If file is saved, still provide appropriate access or content summary according to environment.

## Reusable Output Rule

The final artifact should not include:

```text
"需要调什么直接说"
"GitHub 上发布前..."
"我建议..."
unless outside the artifact as a separate note
```

If such notes are needed, place them after the artifact and clearly separate them.

## Failure Modes

Hard fail:

1. User asks for dialogue output but assistant only saves file.
2. User asks for a file but assistant only gives text.
3. Artifact contains internal reasoning or UI residue.
4. Output format does not match request.
5. Wrong language.

Soft fail:

1. Too much commentary before artifact.
2. Artifact is usable but not clean.
3. Notes are mixed into artifact.
4. Markdown formatting is broken.

## Rewrite Rule

If failed:

```text
Regenerate only the requested artifact.
Use correct language and format.
Remove internal notes.
Add external notes only after the artifact if needed.
```

## Known Project Artifact Rule

When the artifact is for a known project:

1. Recover project context before drafting.
2. Preserve known positioning.
3. Preserve known exclusions.
4. Mark unknown install/license/deployment details as placeholders.
5. Do not block with basic questions if context is sufficient.

For public README, include:

```text
what it is
who it serves
what problem it solves
what it is not
example use cases
installation placeholders
status
license placeholder if unknown
```

Fail if the skill asks the user to re-explain a known project before drafting.

## Final Rule

the skill should know the difference between helping think and delivering the thing.

## Artifact Contract Priority

When an artifact contract applies, it overrides stylistic preferences.

Priority:

```text
artifact format
language
user terms
claim boundary
markdown cleanliness
then narrative style
```

## Direct Delivery Rule

If the user asks:

```text
Give me a README.
Give me the email.
Send it in the dialogue.
Write the message.
```

output the artifact directly.

Do not only save to a file unless explicitly requested.

## Commentary Control

Do not add commentary before an artifact unless useful and in the same language.

For English artifacts, any necessary note should be in English.

For GitHub README, avoid commentary unless needed for assumptions or placeholders.

## Failure Modes

Hard fail:

1. Writes file when dialogue output was requested.
2. Outputs analysis instead of artifact.
3. Wrong language.
4. Artifact has UI residue.
5. Artifact violates its contract.

Soft fail:

1. Too much preface.
2. Notes are mixed into artifact.
3. Deliverable is usable but not clean.
