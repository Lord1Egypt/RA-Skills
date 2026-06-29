# GC_NARR_015_NARRATIVE_ENTROPY

## Purpose

Test whether the skill can manage narrative entropy: predictability, surprise, cognitive load, and resolution.

## Task

Explain a complex concept to three audiences:

1. general audience
2. technical audience
3. one-on-one collaboration target

## Required Behavior

the skill must:

1. start with familiar ground;
2. introduce one meaningful turn;
3. avoid too many new concepts at once;
4. resolve the turn into a clear value shift;
5. preserve source fidelity;
6. avoid slogans;
7. sound native in Chinese or English.

## Bad Pattern

```text
This system integrates multi-source heterogeneous data into a simulation ontology and uses multi-agent workflows to optimize decision pathways.
```

Why bad:

```text
too much high-entropy information at the opening
no familiar ground
no protagonist
no turn
high cognitive load
```

## Better Pattern

```text
A team can have all the data and still make the wrong decision, because the facts are scattered across systems that do not see each other. The real problem is not missing information. It is disconnected information.
```

Why better:

```text
familiar ground: team has data
high-entropy turn: more data does not mean better judgment
clear value shift: from information volume to information relationship
```

## Acceptance Criteria

Pass if:

1. The opening is accessible.
2. The output contains at least one meaningful turn.
3. The turn changes how the audience sees the problem.
4. The explanation does not overload the audience.
5. The ending resolves the tension.
6. The language feels native, not template-like.
7. The output remains accurate.

Fail if:

1. It is clear but predictable.
2. It is exciting but confusing.
3. It stacks too many metaphors.
4. It uses high-level abstractions too early.
5. It overuses formulaic phrases.
6. It lacks a value shift.
