---
name: moodle-connector
description: "Moodle REST API client, batch downloader, and MCP server for Claude Code integration"
metadata: { "author": "Jabir Iliyas Suraj-Deen", "license": "MIT", "homepage": "https://github.com/Jabir-Srj/moodle-connector", "repository": "https://github.com/Jabir-Srj/moodle-connector.git", "tags": ["moodle", "education", "lms", "api", "batch-download", "mcp", "claude-code"] }
---

# Moodle Connector

**Full-featured Moodle REST API client with batch downloading and MCP protocol support for Claude Code and OpenCode.**

## Features

**Complete Moodle API Access**
- List courses, check grades, track assignments
- Fetch materials, deadlines, announcements
- Download files with aggressive caching

**Multiple Integration Modes**
- **CLI:** `python moodle_connector.py courses`
- **Python Library:** `from moodle_connector import MoodleConnector`
- **MCP Protocol:** Native integration with Claude Code, OpenCode

**Generic Batch Downloader**
- JSON-driven configuration (zero code modification)
- Works with any Moodle module
- Auto-organized by course name

**Security**
- Encrypted credentials (PBKDF2 + Fernet)
- Token management built-in
- No secrets in git history
- MIT licensed

## Installation

Once installed via `clawhub install moodle-connector`:

```bash
cd ./skills/moodle-connector
pip install -r requirements.txt
playwright install chromium
```

## Quick Start

### 1. Setup Moodle Token

```bash
cp config.template.json config.json
# Edit config.json with your Moodle web service token
```

### 2. Use CLI

```bash
python moodle_connector.py courses        # List all courses
python moodle_connector.py grades         # Check grades
python moodle_connector.py assignments    # View assignments
python moodle_connector.py materials --course-id 44864
python moodle_connector.py download "https://mytimes.taylors.edu.my/..." --output myfile.pdf
python moodle_connector.py summary        # Full markdown export
```

### 3. Use Python Library

```python
from moodle_connector import MoodleConnector
from pathlib import Path

connector = MoodleConnector(
    config_path=Path('config.json'),
    password='encryption-password'
)

courses = connector.courses()
grades = connector.grades()
assignments = connector.assignments()
materials = connector.materials()
deadlines = connector.deadlines()
announcements = connector.announcements()
content = connector.summary()

# Download with caching
file_content = connector.download("https://...")
```

### 4. Batch Download (Any Module)

```bash
cp downloads.example.json downloads.json
# Edit downloads.json to add modules and file URLs
python batch_downloader.py
```

**Output Structure:**
```
downloads/
├── Your_Module_Name_1/
│   ├── file1.pdf
│   ├── file2.zip
│   └── ...
└── Your_Module_Name_2/
    ├── lecture.pdf
    └── ...
```

## MCP Integration (Claude Code / OpenCode)

**REQUIRED:** Set `MOODLE_CRED_PASSWORD` environment variable before starting Claude Code.

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "moodle-connector": {
      "command": "python",
      "args": ["./skills/moodle-connector/mcp_server.py"],
      "env": {
        "MOODLE_CRED_PASSWORD": "your-encryption-password"
      }
    }
  }
}
```

**Important:** Replace `your-encryption-password` with your actual encryption password used in `config.json`.

Restart Claude Code. All 8 Moodle functions are now available as native MCP tools:
- `courses()` — List enrolled courses
- `grades()` — Get grades
- `assignments()` — Get assignments
- `materials()` — Get course materials
- `deadlines()` — Get upcoming deadlines
- `announcements()` — Get course news
- `download(url, output?)` — Download files
- `summary()` — Get complete data export

## Configuration

### Moodle Token (`config.json`)
```json
{
  "moodle": {
    "base_url": "https://mytimes.taylors.edu.my",
    "web_service_token": "YOUR_TOKEN_HERE"
  },
  "cache": {
    "api_ttl_seconds": 300
  }
}
```

### Batch Downloader (`downloads.json`)
```json
{
  "downloads": [
    {
      "module": "Machine Learning",
      "course_id": 44864,
      "files": [
        {
          "name": "Week1.zip",
          "url": "https://mytimes.taylors.edu.my/webservice/pluginfile.php/..."
        }
      ]
    }
  ]
}
```

## Requirements

- Python 3.10+
- requests ≥2.31.0
- cryptography ≥41.0.0
- playwright ≥1.40.0
- mcp ≥0.1.0 (for MCP server)

## Supported Moodle Instances

Tested with:
- Taylor's University (mytimes.taylors.edu.my)
- Should work with any Moodle 3.x+ instance

## Security Notes

- **Environment-enforced:** `MOODLE_CRED_PASSWORD` is **required** — no hardcoded defaults
- **Error sanitization:** MCP server sanitizes errors, no internal details leaked to clients
- **Encrypted credentials:** PBKDF2 (480K iterations) + Fernet encryption
- **Safe for headless:** Use `MOODLE_CRED_PASSWORD` env var for automation
- **Git-safe:** Never commit `config.json` with real tokens
- **No telemetry:** No external data transmission or logging

## Troubleshooting

### "Invalid parameter value detected" for calendar API
Use `assignments()` instead — gets same deadline info.

### Browser MFA not triggering
Run: `python moodle_connector.py login` for manual token retrieval.

### File download stuck
Check network. Increase timeout in code or clear cache: `rm -rf cache/`

## License

MIT — See LICENSE file for details. You are free to use, modify, and distribute this software.

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request
4. Agree to license your work under GPLv3

## Author

**Jabir Iliyas Suraj-Deen**
- GitHub: https://github.com/Jabir-Srj
- Email: jabirsrj8@protonmail.com
- Taylor's University, Kuala Lumpur, Malaysia

---

**GitHub:** https://github.com/Jabir-Srj/moodle-connector
**Release:** v1.0.0 (March 17, 2026)
 `python moodle_connector.py login` for manual token retrieval.

### File download stuck
Check network. Increase timeout in code or clear cache: `rm -rf cache/`

## License

MIT — See LICENSE file for details. You are free to use, modify, and distribute this software.

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request
4. Agree to license your work under MIT

## Author

**Jabir Iliyas Suraj-Deen**
- GitHub: https://github.com/Jabir-Srj
- Email: jabirsrj8@protonmail.com
- Taylor's University, Kuala Lumpur, Malaysia

---

**GitHub:** https://github.com/Jabir-Srj/moodle-connector
**Release:** v1.0.0 (March 17, 2026)
** v1.0.0 (March 17, 2026)
