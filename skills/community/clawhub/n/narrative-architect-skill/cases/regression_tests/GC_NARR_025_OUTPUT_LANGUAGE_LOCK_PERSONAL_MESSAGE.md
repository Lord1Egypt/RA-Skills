# GC_NARR_025_OUTPUT_LANGUAGE_LOCK_PERSONAL_MESSAGE

## Purpose

Test whether the skill respects latest-user-message language and correctly routes personal romantic communication.

## Scenario

Conversation history is mostly Chinese.

User asks in English:

```text
Please introduce me to a girl. I am geek and super smart, but might not talk well in front of her.
```

## Required Behavior

the skill must:

1. Answer in English.
2. Use Personal Communication Mode.
3. Not treat the task as a pitch.
4. Provide a sendable message.
5. Avoid pickup artist tone.
6. Avoid self-pity.
7. Preserve the user's geeky/smart personality.
8. Suggest a low-pressure context.
9. Include short notes in English.
10. Avoid Chinese unless explicitly requested.

## Bad Output

```text
这个不用 pitch。你不需要把自己"卖"出去。
```

Why bad:

```text
Wrong language.
```

## Better Output

```text
You do not need to sell yourself.

Your problem is not that you are not interesting. It is that you may not show your best self in a setting built around effortless small talk.

So do not choose a setting built around small talk. Choose a setting where your real self can show up naturally.
```

## Sendable Message Example

```text
I should be honest: I am much better when we are doing something than when I am trying to act smooth. I am a geek, I think fast, and sometimes I talk slower when I actually care about making a good impression.

If you are open to it, maybe we can start with something low-pressure — like [place/activity you genuinely like].
```

## Acceptance Criteria

Pass if:

1. Output is English.
2. Message is sendable.
3. Advice is practical.
4. The user's awkwardness is not framed as a defect.
5. The user is not told to perform confidence.
6. No manipulation tactics appear.
7. Private notes are English.
8. The next step is low-pressure.
9. The answer is not overlong.
10. The output feels like personal communication, not sales.

Fail if:

1. Output is Chinese.
2. It becomes a pitch.
3. It over-strategizes romance.
4. It sounds like pickup advice.
5. It makes the user sound needy.
6. It lacks a concrete message.

## Golden Principle

Latest user language controls delivery.
Personal communication should make the user more real, not more performative.
