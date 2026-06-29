# Pi TUI Themes

Theme files: `~/.pi/agent/themes/*.json` (auto hot-reload)

## Format

```json
{
  "$schema": "https://raw.githubusercontent.com/earendil-works/pi/main/packages/coding-agent/src/modes/interactive/theme/theme-schema.json",
  "name": "my-theme",
  "vars": { "blue": "#0066cc", "gray": 242 },
  "colors": {
    "accent": "blue",
    "muted": "gray",
    "text": "",
    ...
  }
}
```

- `vars` — optional, defines reusable colors
- `colors` — must define all 51 tokens
- `$schema` — editor autocompletion

## Color Value Formats

| Format | Example | Description |
|--------|---------|-------------|
| Hex | `"#ff0000"` | 6-digit RGB |
| 256-color | `242` | xterm 256-color index |
| Variable reference | `"primary"` | Reference vars |
| Default | `""` | Terminal default color |

## Color Token List

**Core UI (11)**: accent, border, borderAccent, borderMuted, success, error, warning, muted, dim, text, thinkingText

**Backgrounds (11)**: selectedBg, userMessageBg, userMessageText, customMessageBg, customMessageText, customMessageLabel, toolPendingBg, toolSuccessBg, toolErrorBg, toolTitle, toolOutput

**Markdown (10)**: mdHeading, mdLink, mdLinkUrl, mdCode, mdCodeBlock, mdCodeBlockBorder, mdQuote, mdQuoteBorder, mdHr, mdListBullet

**Diffs (3)**: toolDiffAdded, toolDiffRemoved, toolDiffContext

**Syntax (9)**: syntaxComment, syntaxKeyword, syntaxFunction, syntaxVariable, syntaxString, syntaxNumber, syntaxType, syntaxOperator, syntaxPunctuation

**Thinking Levels (6)**: thinkingOff, thinkingMinimal, thinkingLow, thinkingMedium, thinkingHigh, thinkingXhigh

**Bash (1)**: bashMode

## HTML Export (Optional)

```json
{ "export": { "pageBg": "#18181e", "cardBg": "#1e1e24", "infoBg": "#3c3728" } }
```

## Terminal Compatibility

- 24-bit RGB (iTerm2, Kitty, WezTerm, Windows Terminal, VS Code)
- 256-color terminals auto-map to nearest color
- Check: `echo $COLORTERM` → truecolor/24bit
- VS Code: `terminal.integrated.minimumContrastRatio: 1`