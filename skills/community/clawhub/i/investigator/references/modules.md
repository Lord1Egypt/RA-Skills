# Modules

Use only the modules relevant to the target.

## Username module
- direct profile URL checks
- username variants
- platform-specific presence checks
- public profile links and obvious profile metadata

## Email module
- Gravatar/public avatar clues when applicable
- web search for public mentions
- optional HIBP breach check when configured
- domain MX / domain-level context when useful

## Web search module
Use targeted web search to confirm or enrich weak platform findings.
Examples:
- `"username" site:github.com`
- `"username" site:reddit.com`
- `"email@example.com"`
- `"username" "display name"`

## Correlation module
Use to compare:
- handle overlap
- display name overlap
- website overlap
- bio overlap
- avatar reuse
- explicit cross-links

## Export module
Use JSON output when the user wants structured output or machine-readable results.
