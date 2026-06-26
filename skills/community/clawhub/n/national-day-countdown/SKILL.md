# Days to National Day Skill

## Description

Calculate how many days remain until China's National Day (October 1st).

## When to use

Use this skill when:

* The user asks how many days remain until National Day
* The user asks about countdown to October 1st
* The user asks for time remaining before a specific holiday (National Day)

## When NOT to use

* When user asks about other holidays (e.g. Spring Festival, Christmas)
* When user asks for historical dates or past calculations

## Input

No input is required.

## Output

Returns:

* today's date
* target National Day date
* number of days remaining
* a human-readable message

## Examples

### Example 1

User: 还有多少天到国庆节？
Assistant: (calls this skill)

### Example 2

User: How many days until October 1st?
Assistant: (calls this skill)

## Notes

* If the current date is after October 1st, calculate for next year's National Day
* Always return a non-negative integer
