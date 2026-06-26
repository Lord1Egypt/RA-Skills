# 🛠️ Kuikly Skills

AI Agent Skills for building cross-platform apps with [Kuikly](https://github.com/Tencent-TDS/KuiklyUI).

## Available Skills

| Skill | Description | File |
|-------|-------------|------|
| **Cross-Platform App Builder** | Create, build, preview cross-platform mobile apps via CLI | [SKILL.md](./SKILL.md) |

## How to Use

### For ClawHub / OpenClaw Users

Submit `SKILL.md` to [ClawHub](https://clawhub.ai) — the skill will be available in the marketplace.

### For Cursor Users

Copy `SKILL.md` content into your project's `.cursor/rules/` directory as a `.mdc` file:

```bash
cp SKILL.md your-project/.cursor/rules/kuikly-app-builder.mdc
```

### For ChatGPT / Claude / Other Agents

Paste the content of `SKILL.md` as system instructions or at the beginning of your conversation.

### Direct Download

```bash
curl -O https://raw.githubusercontent.com/wwwcg/kuikly-skills/main/SKILL.md
```

## What Does This Skill Do?

The **Cross-Platform App Builder** skill enables any AI Agent to:

1. **Create** a Kuikly project from scratch (`npx create-kuikly-app create`)
2. **Build** for Android and iOS
3. **Preview** on real devices or simulators with automatic screenshots
4. **Self-repair** build errors using structured diagnostics
5. **Create pages & components** with correct Kuikly patterns

All operations use the [`create-kuikly-app`](https://github.com/wwwcg/create-kuikly-app) CLI tool.

## Related Projects

- [KuiklyUI](https://github.com/Tencent-TDS/KuiklyUI) — The open-source Kotlin Multiplatform UI framework
- [create-kuikly-app](https://github.com/wwwcg/create-kuikly-app) — The CLI tool powering this skill

## License

MIT
