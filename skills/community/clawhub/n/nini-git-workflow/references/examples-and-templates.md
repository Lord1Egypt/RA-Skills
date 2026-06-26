# Examples and Templates

## Commit Examples

### Good

```text
feat(gateway): add group control support
```

```text
fix(sensor): correct energy calculation overflow
```

```text
refactor: move register_listener to entity objects

- Add register_listener() to Device/Group/Scene in SDK
- Remove gateway parameter from integration entities
- Simplify all-light creation from 14 lines to 1 line
```

```text
chore(release): bump version to 0.2.0
```

### Bad

```text
refactor: cleanup
```

*Too vague - what was cleaned up?*

```text
fix: bug fixes
```

*Not specific - which bugs?*

```text
feat: implement new authentication system

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>
```

*Contains forbidden AI markers*

## PR Description

**Merge strategy**: Squash and merge.

**Schema (prose-only — no markdown headings):**

```text
<type>(<scope>): <imperative subject>      ← title, ≤72 char

<2-3 declarative sentences explaining *why* this change exists.
Do not restate what the diff already shows.>

<Optional one-liner pointing the reviewer at the load-bearing file.>

Verify: <one line on how you self-tested, or "N/A: docs only">
```

The `Verify:` line is also valid as `验证：` when the body is in Chinese — both languages are first-class.

**Forbidden patterns** (these turn the description into noise):

1. Markdown section headings inside the description body
2. Emoji-as-bullet or emoji-headings: 🔧 ✅ 💡 ⚡ 🚀 📝
3. Commit list / file list / line-count statistics — the diff already shows that
4. AI filler phrases: "本次变更主要包含", "值得注意的是", "综上所述", "希望对你有帮助" (Chinese); "This PR mainly includes", "It is worth noting that", "In summary" (English)
5. Collapsible blocks (`<details>`) or tables substituting for bullets
6. Reflective narration ("I considered A then B but settled on C…") — technical prose is declarative impersonal; design tradeoffs belong in `docs/specs/` or `openspec/changes/`
7. Mention of abandoned alternatives or earlier drafts — describe only what is being shipped, not what was tried and rejected. History of the design lives in spec / OpenSpec change docs, not in the PR description.

### Examples

#### English — small fix

```text
fix(sensor): clamp energy reading at 65535

The old firmware wraps the `wh` field back to 0 when power
exceeds 65W, which breaks HA's historical chart. Clamp at the
device layer so per-entity defenses are unnecessary. SDK API
is untouched.

Verify: feed wh=70000 manually; HA shows 65535, not 0.
```

#### English — refactor

```text
refactor: move register_listener to entity objects

The global gateway listener forced every integration entity to
import the gateway singleton, which broke unit tests that spin
up devices in isolation. Move register_listener() onto
Device/Group/Scene so entities own their own subscription.

Reviewer hint: src/sdk/device.py is the new home; old gateway.py
becomes a thin wrapper.

Verify: pytest tests/unit/test_device_listener.py
```

#### Chinese — illustrating bilingual support

```text
fix(sensor): align HA history with cumulative meter reading

旧逻辑只汇报实时功率，HA 历史图无法回放整月用电。改为汇报
累计 wh，由 HA 自己做 derivative。

验证：让 HA 录 24 小时数据，对比物理表读数误差 < 1%。
```

## CHANGELOG Format

Follow [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format:

```markdown
## [x.y.z] - YYYY-MM-DD

### Added
- New user-facing features

### Fixed
- Important bug fixes (#issue)

### Technical
- Dependency updates, CI/CD improvements, code refactoring
```

### Guidelines

- **Added**: User-facing features
- **Fixed**: Bug fixes with issue references (#123)
- **Technical**: Internal changes (dependencies, CI/CD, refactoring)
  - Include commit hashes (abc1234) for technical changes without issues
- Keep entries concise and user-focused
- Update version links at bottom of changelog

### Example

```markdown
## [0.3.0] - 2025-12-01

### Added
- Group control support for smart home devices (#45)
- Energy monitoring dashboard (#48)

### Fixed
- Energy calculation overflow in sensor component (#52)

### Technical
- Migrate to new SDK API structure (commit: abc1234)
- Update dependencies to latest versions (commit: def5678)

[0.3.0]: https://github.com/owner/repo/compare/v0.2.0...v0.3.0
```
