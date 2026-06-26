---
name: mood-color-mapper
description: Translate a user's felt state into a color-based mood map with body cues, possible emotion words, likely needs, and one gentle next step under 10 minutes. Use when the user struggles to name emotions directly and responds better to colors, shades, or visual metaphors than strict feeling labels.
---

# Mood Color Mapper

## Overview

Use this skill when a color-first check-in feels easier than naming emotions directly. It starts with the body, lets the user choose a color or texture, translates that palette into possible feeling words, and ends with one small response that respects the emotion instead of suppressing it.

This skill is descriptive only. It is not diagnosis, therapy, or crisis support.

## Trigger

Use this skill when the user wants to:
- describe an emotional state through color
- find feeling words without forcing one exact label
- separate body sensation from self-judgment
- understand what an emotion might need right now
- choose a gentle regulation step under 10 minutes

### Example prompts
- "I cannot name my mood, but it feels dark blue"
- "Map my emotions with colors instead of labels"
- "Help me understand this mixed restless and heavy feeling"
- "Give me a gentle emotional check-in"

## Workflow

1. Start with body sensation and energy level.
2. Choose a primary color, shade, or texture.
3. Add a secondary color if the feeling is mixed.
4. Translate the palette into possible emotion words.
5. Identify what the emotion might need.
6. Suggest one small next step that respects the state.

## Inputs

The user can provide any mix of:
- body sensations
- energy level
- explicit color words
- emotion words
- mixed or conflicting feelings
- context about stress, sadness, anger, or calm
- a wish for a gentle check-in instead of analysis

## Outputs

Return a markdown mood map with:
- current palette
- body cue summary
- possible emotion words
- likely need
- one gentle next step under 10 minutes

## Safety

- Separate feelings from self-judgment and story loops.
- Offer language options instead of pretending one exact label is always possible.
- During intense distress, bias toward grounding, rest, and human support language.
- Do not present the skill as mental health diagnosis or emergency care.

## Acceptance Criteria

- Return markdown text.
- Include at least one body cue and one need statement.
- Support mixed states with a secondary color when useful.
- End with one small next step, not a giant fix.
