# Contributing to MindClaw

Thanks for your interest in contributing! Here's how to get started.

## Setup

```bash
git clone https://github.com/Blue8x/Clawtion.git
cd Clawtion
pip install -e ".[dev]"
```

## Running tests

```bash
pytest
```

With coverage:

```bash
pytest --cov=mindclaw --cov-report=term-missing
```

## Code style

- Python 3.10+ type hints everywhere
- Docstrings for public functions
- Keep modules focused: store, search, graph, capture, cli

## Branching

- `main` — stable releases
- `dev` — integration branch
- Feature branches: `feat/<short-name>`
- Bug fixes: `fix/<short-name>`

## Pull requests

1. Fork the repo and create your branch from `dev`
2. Add tests for any new functionality
3. Make sure all tests pass
4. Update `CHANGELOG.md` with your changes
5. Open a PR with a clear description

## Reporting issues

Open an issue on GitHub with:

- A clear title
- Steps to reproduce
- Expected vs actual behavior
- Python version and OS

## ClawHub publishing

To publish a new version to [clawhub.ai](https://clawhub.ai):

1. Bump `version` in `pyproject.toml`, `clawhub.yaml`, and `src/mindclaw/__init__.py`
2. Update `CHANGELOG.md`
3. Tag the release: `git tag v0.x.x`
4. Push: `git push origin main --tags`
5. ClawHub will pick up the new release from the tag

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
