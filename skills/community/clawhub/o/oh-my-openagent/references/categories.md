## Categories

Categories determine which model Sisyphus-Junior uses when `task()` is called with a `category` parameter. Each category is optimized for a specific domain.

### visual-engineering

- Default model: gemini-3.1-pro
- Fallback chain: glm-5 → claude-opus-4-6
- Domain: Frontend, UI/UX, design, styling, animation
- Best paired with skill: frontend-ui-ux

### ultrabrain

- Default model: gpt-5.4 (variant: xhigh)
- Fallback chain: gemini-3.1-pro → claude-opus-4-6
- Domain: Genuinely hard, logic-heavy tasks
- Note: Give clear goals only, not step-by-step instructions

### deep

- Default model: gpt-5.3-codex (variant: medium)
- Fallback chain: claude-opus-4-6 → gemini-3.1-pro
- Domain: Goal-oriented autonomous problem-solving. Thorough research before action.

### artistry

- Default model: gemini-3.1-pro (variant: high)
- Fallback chain: claude-opus-4-6 → gpt-5.4
- Domain: Complex problem-solving with unconventional, creative approaches

### quick

- Default model: claude-haiku-4-5
- Fallback chain: gemini-3-flash → gpt-5-nano
- Domain: Trivial tasks — single file changes, typo fixes, simple modifications

### unspecified-low

- Default model: claude-sonnet-4-6
- Fallback chain: gpt-5.3-codex → gemini-3-flash
- Domain: Tasks that don't fit other categories, low effort required

### unspecified-high

- Default model: claude-opus-4-6 (variant: max)
- Fallback chain: gpt-5.4 (high) → glm-5 → k2p5 → kimi-k2.5
- Domain: Tasks that don't fit other categories, high effort required

### writing

- Default model: gemini-3-flash
- Fallback chain: claude-sonnet-4-6
- Domain: Documentation, prose, technical writing

## Category configuration options

All categories support these override options:

| Option | Type | Description |
|--------|------|-------------|
| model | string | Override default model |
| fallback_models | string[] | Override fallback chain |
| temperature | number | Sampling temperature |
| top_p | number | Nucleus sampling |
| maxTokens | number | Max output tokens |
| thinking | boolean | Enable extended thinking |
| reasoningEffort | string | Reasoning effort level |
| textVerbosity | string | Output verbosity |
| tools | string[] | Restrict available tools |
| prompt_append | string | Append to system prompt |
| variant | string | Cost variant |
| description | string | Category description |
| is_unstable_agent | boolean | Mark as unstable |

Example:
```json
{
  "categories": {
    "quick": {
      "model": "gemini-3-flash",
      "fallback_models": ["gpt-5-nano"]
    },
    "visual-engineering": {
      "model": "claude-opus-4-6",
      "prompt_append": "Always use Tailwind CSS."
    }
  }
}
```

## Using categories in task()

```
task(
  category="visual-engineering",
  load_skills=["frontend-ui-ux"],
  prompt="Redesign the dashboard layout...",
  run_in_background=false
)
```

The category determines the model. Skills inject domain expertise into the prompt.
