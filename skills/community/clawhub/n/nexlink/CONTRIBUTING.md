# Contributing to OpenClaw NexLink

Thank you for your interest in contributing!

## Development Standards

This project follows the [Hardshell Coding Standards](https://github.com/asistent-alex/openclaw-hardshell).

### Quick Reference

- **Security**: Validate all input, no secrets in code, HTTPS everywhere
- **Architecture**: SOLID principles, separation of concerns
- **Testing**: TDD with 70% minimum coverage
- **Git**: Conventional commits, feature branches

## Running Checks

```bash
# Format code
black modules/ tests/

# Lint
ruff check modules/ tests/

# Type check (optional)
mypy modules/

# Run tests
PYTHONPATH=modules/exchange pytest tests/ -v

# Run tests with coverage
PYTHONPATH=modules/exchange pytest tests/ --cov=modules --cov-report=html
```

## Branch Strategy

- `main` - always deployable, protected
- `feature/<slug>` - short-lived feature branches
- `fix/<slug>` - bug fix branches
- `alpha-testing` - integration testing

## Commit Format

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <short description>

Types: feat, fix, docs, style, refactor, test, chore
```

Examples:
- `feat(mail): add attachment support`
- `fix(calendar): handle timezone correctly`
- `docs(readme): update installation instructions`

## Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make changes following Hardshell standards
4. Run tests: `PYTHONPATH=modules/exchange pytest tests/ -v`
5. Run linting: `ruff check modules/ tests/`
6. Submit a pull request

### PR Checklist

- [ ] Code follows Hardshell standards
- [ ] All tests pass
- [ ] New code has tests
- [ ] Documentation updated (if needed)
- [ ] No secrets in code
- [ ] Conventional commit format used

## Code of Conduct

Be respectful, constructive, and inclusive.

## Getting Help

- Open an issue for bugs or feature requests
- Check existing issues before creating new ones
- Provide clear reproduction steps for bugs

## License

By contributing, you agree that your contributions will be licensed under the MIT License.