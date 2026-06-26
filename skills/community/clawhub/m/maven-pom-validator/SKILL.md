---
name: maven-pom-validator
description: Validate and lint Maven pom.xml files for structure, dependencies, plugins, and best practices. Use when asked to lint, validate, check, or audit pom.xml files, verify Maven configuration, or ensure POM quality. Triggers on "lint pom", "validate pom.xml", "check maven", "maven best practices".
---

# Maven POM Validator

Validate and lint Maven `pom.xml` files for structural correctness, dependency hygiene, plugin configuration, and best practices.

## Commands

### lint — Full lint pass (all 20+ rules)

```bash
python3 scripts/maven_pom_validator.py lint pom.xml
python3 scripts/maven_pom_validator.py lint pom.xml --strict
python3 scripts/maven_pom_validator.py lint pom.xml --format json
python3 scripts/maven_pom_validator.py lint pom.xml --format markdown
```

### dependencies — Audit dependency declarations

```bash
python3 scripts/maven_pom_validator.py dependencies pom.xml
python3 scripts/maven_pom_validator.py dependencies pom.xml --format json
```

### plugins — Audit plugin declarations

```bash
python3 scripts/maven_pom_validator.py plugins pom.xml
python3 scripts/maven_pom_validator.py plugins pom.xml --format markdown
```

### validate — Quick structural validation only

```bash
python3 scripts/maven_pom_validator.py validate pom.xml
python3 scripts/maven_pom_validator.py validate pom.xml --strict
```

## Flags

| Flag | Description |
|------|-------------|
| `--strict` | Exit code 1 on warnings (CI mode) |
| `--format text` | Human-readable output (default) |
| `--format json` | Machine-readable JSON |
| `--format markdown` | Markdown report |

## Lint Rules

### Structure (5 rules)
1. Valid XML — file must be well-formed XML
2. Required elements — groupId, artifactId, version, modelVersion must be present
3. modelVersion must be "4.0.0"
4. groupId format — must follow reverse-domain convention (e.g. `com.example`)
5. packaging value must be valid (jar, war, pom, ear, rar, maven-plugin)

### Dependencies (6 rules)
6. No duplicate dependencies (same groupId:artifactId)
7. No SNAPSHOT versions in release POMs
8. Version must be defined (not missing)
9. No wildcard/range versions (LATEST, RELEASE, [1.0,))
10. Scope must be valid (compile, test, provided, runtime, system, import)
11. system-scoped deps must have `<systemPath>`

### Plugins (5 rules)
12. Plugin versions must be pinned
13. No duplicate plugins (same groupId:artifactId)
14. Plugin groupId should be specified
15. Known deprecated plugins flagged
16. Configuration elements checked for common issues

### Best Practices (6 rules)
17. Properties used for version management (DRY check)
18. dependencyManagement used in parent POMs
19. UTF-8 encoding specified (project.build.sourceEncoding)
20. Java source/target version set (maven.compiler.source/target or release)
21. No hardcoded absolute paths in configuration
22. SCM section present

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | No errors (warnings OK unless --strict) |
| 1 | Errors found (or warnings with --strict) |
| 2 | Script usage error |
