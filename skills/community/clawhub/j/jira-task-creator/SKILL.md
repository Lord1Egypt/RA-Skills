# Jira Task Creator - Professional Edition

A complete Jira task management skill with natural language parsing, smart user search, batch operations, and intelligent analytics.

## Core Features

### 1. Intelligent Task Creation
- **Natural language parsing**: Supports Chinese and English task descriptions
- **Flexible field configuration**: All standard Jira fields supported
- **Smart date handling**: Relative dates ("tomorrow", "next week", "end of month")

### 2. Smart User Search
- **Multiple search methods**: Name, open_id, email
- **Assignable user query**: Only returns users assignable to specific project
- **User cache mechanism**: 5-minute TTL, reduces API calls
- **User mapping management**: Maintains Feishu-Jira user mapping

### 3. Batch Task Creation
- **CSV import**: Bulk task creation from CSV files
- **Task templates**: Bug report, feature request, technical research
- **Variable replacement**: Dynamic template content filling

### 4. Task Analytics
- **Multi-dimensional statistics**: Status, priority, project, assignee
- **Completion rate calculation**: Success task ratio
- **Overdue task identification**: Overdue, due soon (3 days)
- **Formatted reports**: Markdown statistics reports

## Installation

```bash
pip install requests python-dateutil
```

## Configuration

### Environment Variables

```bash
# Required
export JIRA_BASE_URL="http://your-jira.com"
export JIRA_BEARER_TOKEN="your-token-here"

# Optional
export JIRA_DEFAULT_PROJECT="ERP"
export JIRA_DEFAULT_ASSIGNEE="Cloud"
export JIRA_CACHE_ENABLED="true"
export JIRA_CACHE_TTL="300"
```

### Config File (config.json)

```json
{
  "jira": {
    "baseUrl": "http://your-jira.com",
    "bearerToken": "your-token-here",
    "defaultProject": "ERP",
    "defaultAssignee": "Cloud",
    "timeout": 30
  },
  "cache": {
    "enabled": true,
    "ttl": 300,
    "maxSize": 1000
  },
  "logging": {
    "level": "INFO",
    "saveToFile": true,
    "logDirectory": "logs/"
  }
}
```

## Quick Start

### Create a Task

```python
from jira_task_creator import create_issue

result = create_issue(
    summary="Fix login bug",
    description="Users cannot login to system",
    project_key="ERP",
    issue_type_name="Bug",
    priority="High"
)
```

### Natural Language Task Creation

```python
from jira_task_creator import create_issue_natural

result = create_issue_natural(
    user_instruction="Complete API development by next Wednesday, high priority",
    project="ERP"
)
```

### Search User

```python
from jira_task_creator import search_user

user = search_user("贾小丽", "ERP")
print(f"Username: {user['name']}")
print(f"Display name: {user['displayName']}")
```

### Batch Creation

```python
from batch_creator import BatchTaskCreator

creator = BatchTaskCreator(base_url, token)
results = creator.create_from_csv("tasks.csv")
```

### Task Analytics

```python
from task_analyzer import TaskAnalyzer

tasks = fetch_tasks("assignee = currentUser() AND status != Done")
analysis = TaskAnalyzer.analyze_tasks(tasks)
report = TaskAnalyzer.generate_report(analysis)
print(report)
```

## API Reference

### create_issue()

Creates a Jira issue with specified fields.

**Parameters:**
- `summary` (str): Task title (required)
- `description` (str): Task description
- `project_key` (str): Project key (e.g., "ERP")
- `issue_type_name` (str): Issue type (e.g., "Bug", "Story")
- `priority` (str): Priority (High, Medium, Low)
- `assignee` (str): Assignee username
- `due_date` (str): Due date (ISO 8601 format)

**Returns:**
- `dict`: Created issue data or error information

### search_user()

Searches for users assignable to a project.

**Parameters:**
- `query` (str): Search query (name, open_id, email)
- `project_key` (str): Project key

**Returns:**
- `dict`: User information or None if not found

### create_issue_natural()

Creates an issue from natural language instruction.

**Parameters:**
- `user_instruction` (str): Natural language task description
- `project` (str): Project key

**Returns:**
- `dict`: Creation result

## Task Templates

### Bug Report Template

```python
from batch_creator import BatchTaskCreator

creator = BatchTaskCreator(base_url, token)
result = creator.create_from_template("bug_report", {
    "title": "Login page error",
    "description": "Error 500 when logging in",
    "priority": "High"
})
```

### Feature Request Template

```python
result = creator.create_from_template("feature_request", {
    "title": "Add dark mode",
    "description": "Support dark mode theme",
    "priority": "Medium"
})
```

## Error Handling

### Common Errors

**401 Unauthorized:**
- Check Bearer Token validity
- Verify token format

**404 Not Found:**
- Project key is incorrect
- User does not exist

**422 Unprocessable Entity:**
- Invalid field values
- Missing required fields

### Troubleshooting

1. **Check connection**:
   ```bash
   ping your-jira-server.com
   ```

2. **Verify token**:
   ```python
   import requests
   response = requests.get("https://your-jira.com/rest/api/3/myself",
                        headers={"Authorization": f"Bearer {token}"})
   print(response.status_code)
   ```

3. **Enable debug logging**:
   ```json
   {
     "logging": {
       "level": "DEBUG"
     }
   }
   ```

## License

MIT License

## Version

1.0.0 - Initial release
