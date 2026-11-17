# Contributing to P-Todo

Thank you for your interest in P-Todo! 📋

P-Todo is a lightweight, high-performance desktop todo application built with **Java 25 + JavaFX 26 + SQLite**, featuring a mini floating window, 4-level color-coded priority, 9-language i18n, and a full REST API for AI agent integration.

## Ways to Contribute

| Area | What you can add |
|------|-----------------|
| **Bug fixes** | Open an Issue or PR with a minimal reproduction |
| **New features** | View → Controller → Service → DAO (see architecture below) |
| **Translations** | Add a 10th language to `src/main/resources/i18n/` (see i18n guide below) |
| **i18n keys** | Fix missing/incorrect keys (run `tools/check_i18n.py`) |
| **Docs** | Improve `说明.md`, `SKILL.md`, or the REST API docs |
| **Tests** | Add JUnit tests under `src/test/` |

## Architecture

```
View (FXML) → Controller → Service → DAO → SQLite (team-todo.db)
                                ↓
                         REST API (port 9527)
```

- **View→Controller→Service→DAO** layered design
- 5 SQLite tables
- 18 REST endpoints on port 9527 for AI agent control

## Local Development

### Prerequisites

- JDK 25+
- JavaFX 26 (bundled in the all-in-one jar)
- Maven 3.9+

### Build & Run

```bash
# 1. Clone
git clone https://github.com/Pondsi/P-Todo.git
cd P-Todo

# 2. Compile
mvn clean compile

# 3. Run the app
mvn javafx:run

# 4. Package (produces target/team-todo-1.0.0.jar)
mvn clean package

# 5. Verify i18n completeness (9 languages, all keys present)
python tools/check_i18n.py
```

### i18n: Adding a New Language

1. Copy `src/main/resources/i18n/zh_cn.properties` → `xx.properties`
2. Translate all keys (see `check_i18n.py` for the required key list)
3. Register the language in `LanguageManager`
4. Run `python tools/check_i18n.py` to confirm 100% key coverage

> ⚠️ **JDK25 UTF-8 vs AWT GBK gotcha**: When launching on Windows, always pass `-Dfile.encoding=GBK -Dsun.jnu.encoding=GBK` to avoid tray-icon garbled text.

## Pull Request Checklist

- [ ] `mvn clean compile` passes with zero warnings
- [ ] `python tools/check_i18n.py` passes (all languages, all keys)
- [ ] No local absolute paths or personal machine details in added files
- [ ] New i18n keys added to **all** existing languages
- [ ] No `System.out.println` in production code (use the logger)
- [ ] Attribution preserved: `Made with ❤️ by Pondsi` + MIT license remain intact

## Known Pitfalls (from development history)

1. **JavaFX bound value**: never call `setText` on a bound property after `bind()` — throws "A bound value cannot be set".
2. **Enum labelKey**: `t()` is evaluated at class-load time → use a `getLabel()` method instead.
3. **Mini window language**: `buildInstance` rebuild must call `updateMiniTexts()` to override FXML hardcoded Chinese defaults.
4. **Tray encoding**: `-Dfile.encoding=GBK` required on Windows JDK25.

## Code of Conduct

Be kind. This is a desktop tool people actually use every day — test on real Windows machines. 🦞

## License

By contributing, you agree your contributions are licensed under the **MIT License** and may be used by `Pondsi` and downstream users.

---

P-Todo — 桌面待办 · Made with ❤️ by [Pondsi](https://github.com/Pondsi)
