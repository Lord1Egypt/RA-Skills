# Forecastable Question Design

Use this file to convert vague prompts into something that can actually be predicted and scored.

## A good prediction question is:

- singular: one event, not a bundle of outcomes
- time-bounded: it resolves by a named date or window
- thresholded: it says what counts as success or failure
- externally checkable: someone can later verify the answer
- decision-relevant: the result changes what the user should do

## Rewrite rules

- Replace "Will this go well?" with the concrete event that matters.
- Replace "soon" with a date or maximum delay.
- Replace "big growth" with a numeric threshold.
- Replace multi-part prompts with separate forecasts unless all parts must resolve together.

## Bad vs better

| Bad question | Why it fails | Better version |
|--------------|--------------|----------------|
| Will the launch be successful? | No resolution rule | Will the launch ship to paying users by 2026-09-30? |
| Will revenue improve? | No threshold | Will monthly recurring revenue exceed 120k by 2026-12-31? |
| Is the team on track? | Not forecastable as stated | Will the team close the milestone backlog by the end of May? |
| Will the market like this? | Vague subject | Will the feature reach 25% weekly active adoption within 8 weeks of release? |

## Question checklist

Before assigning odds, confirm:
- what exactly happens
- by when
- at what threshold
- who or what source resolves it
- whether there are multiple scenarios instead of one binary event

If any answer is missing, pause the forecast and fix the question.
