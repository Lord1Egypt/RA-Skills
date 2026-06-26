# Contributing to InvAssistant

Thank you for your interest in contributing to InvAssistant!

## How to Contribute

### Reporting Issues

- Search existing issues before creating a new one
- Include clear steps to reproduce the problem
- Specify your Python version and OS

### Adding New Strategy Types

1. Define the strategy logic in `scripts/redline_engine.py`
2. Add the dispatch logic in `scripts/portfolio_checker.py`
3. Add default parameters in `scripts/init_config.py`
4. Update `SKILL.md` with the new strategy description

### Adding Push Channels

1. Create `scripts/send_<channel>.py` following the existing patterns
2. Add a `push_signal(report_text, webhook_url, secret)` function
3. Add the adapter config to `scripts/init_config.py`
4. Update `SKILL.md` push section

### Code Style

- Python 3.8+ compatible
- UTF-8 encoding with BOM-less files
- Use `urllib.request` for HTTP calls in push scripts (zero extra dependencies)
- Chinese comments for business logic, English for technical infrastructure

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
