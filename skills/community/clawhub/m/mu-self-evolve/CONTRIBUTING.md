# Contributing to mu-self-evolve

Thanks for your interest in contributing! This project keeps things simple — Python standard library only, no external dependencies.

## Reporting Issues

- Search [existing issues](https://github.com/muippt/mu-self-evolve/issues) before opening a new one.
- Use the provided **Bug Report** or **Feature Request** template.
- Include enough detail to reproduce: Agent type, OS, Python version, and relevant logs.

## Submitting Pull Requests

1. Fork the repo and create a branch from `main`:
   ```bash
   git checkout -b feat/your-feature
   ```
2. Make your changes. Keep scripts dependency-free (Python 3.8+ standard library only).
3. Run the test suite — all 5 checks must pass:
   ```bash
   python3 scripts/bias_audit.py
   ```
   Expected output: `5/5 PASS`.
4. Update `CHANGELOG.md` if your change is user-facing.
5. Commit using [Conventional Commits](https://www.conventionalcommits.org/):
   | Type | Use for |
   |------|---------|
   | `feat` | New feature |
   | `fix` | Bug fix |
   | `docs` | Documentation only |
   | `refactor` | Code restructure, no behavior change |
   | `test` | Adding or fixing tests |
   | `chore` | Tooling, CI, etc. |

   Example: `feat: add timeout config to env_detect`
6. Open a PR against `main` and fill in the PR template.

## Code Style

- **Python**: Follow [PEP 8](https://peps.python.org/pep-0008/). No external packages — if you need a third-party library, discuss it in an issue first.
- Keep functions small and focused. Add docstrings for public functions.
- No hardcoded secrets, API keys, or internal identifiers.

## Project Structure

```
scripts/
  env_detect.py       # Environment detection
  vfm_verify.py       # Deterministic verification
  eviction_score.py   # Scoring & decay-based eviction
  bias_audit.py       # Bias audit test suite (5 checks)
```

## License

By contributing, you agree that your contributions are licensed under the [MIT License](LICENSE).
