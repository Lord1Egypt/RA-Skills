# Language Match Harness

## Purpose

Check whether the skill's output language matches the user's latest request and target artifact.

This harness runs before final output for all public-facing, developer-facing, or reusable artifacts.

## Checkpoints

1. What language did the user use?
2. What language should the final artifact use?
3. Did the user request a specific language?
4. Does the artifact convention imply a language?
5. Does the output switch languages without reason?
6. Does the final artifact sound native in the target language?

## Rules

### English User Request

If the latest user request is in English:

```text
respond in English by default
generate the artifact in English
avoid Chinese commentary
```

### Chinese User Request

If the latest user request is in Chinese:

```text
respond in Chinese by default
generate English artifacts only if requested or conventional
```

### Artifact Priority

If the user says:

```text
Give me a GitHub README
Write a README
Create package docs
Write API docs
```

then the artifact should usually be English unless the user requests Chinese.

## Native English Checklist

For English output, check:

```text
natural phrasing
short active sentences
no translated Chinese structure
no unnecessary grandiosity
consistent terminology
```

## Native Chinese Checklist

For Chinese output, check:

```text
自然语序
少用翻译腔
不要堆"核心是、本质上、赋能、闭环"
根据场景控制正式度
```

## Failure Modes

Hard fail:

1. User asks in English and output is Chinese.
2. Final artifact uses the wrong language.
3. Chinese analysis is inserted into an English README.
4. The output ignores user-requested bilingual mode.

Soft fail:

1. The language is correct but not native.
2. The title is English but body is Chinese.
3. The answer includes unnecessary meta-commentary in another language.

## Rewrite Rule

If failed:

```text
Regenerate the deliverable in the correct target language.
Preserve the user's selected name and requested structure.
Remove unrelated commentary.
```

## Output Rule

Do not expose this harness to the user unless they ask for analysis or debugging.

## Artifact Language Enforcement

For artifact requests, language match is mandatory.

If user request is in English and artifact is developer-facing, final response must be English.

Applies to:

```text
GitHub README
README.md
API docs
package docs
open-source docs
developer instructions
CLI docs
```

Hard fail if:

```text
the answer begins in Chinese
Chinese commentary appears before an English README
Chinese follow-up notes appear after an English README without request
```

Acceptable only if:

```text
the user requested bilingual output
the user asked for Chinese analysis
the artifact itself is meant for Chinese readers
```

## Repair Rule

If language mismatch occurs, regenerate the entire response in the target language.

Do not partially translate.
