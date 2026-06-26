Jira Task Creator - Professional Edition

Version 1.0.0

## Core Features

- Intelligent task creation with natural language parsing
- Smart user search with caching and mapping
- Batch task creation from CSV or templates
- Task analytics with multi-dimensional statistics
- Smart reminder system for due dates

## Installation

```bash
pip install requests python-dateutil
```

## Configuration

Set environment variables:
```bash
export JIRA_BASE_URL="http://your-jira.com"
export JIRA_BEARER_TOKEN="your-token-here"
```

## Quick Start

```python
from jira_task_creator import create_issue

result = create_issue(
    summary="Fix login bug",
    description="Users cannot login to system",
    project_key="ERP",
    priority="High"
)
```

## Documentation

- SKILL.md - Complete skill documentation
- README.md - Usage guide and API reference

## License

MIT License
