# Museum Skill

A powerful skill for managing museum data collection projects using MySQL.

## Features

- 📊 **List & Query**: Browse museums with filters
- 📈 **Statistics**: Track collection progress
- 🔍 **Data Integrity**: Find incomplete records
- 📤 **Export**: JSON, CSV, or SQL formats
- 🗄️ **Custom Queries**: Direct SQL access

## Installation

```bash
clawhub install museum
```

## Quick Start

1. **Set environment variables**:
```bash
export MYSQL_HOST="your-host"
export MYSQL_USER="your-username"
export MYSQL_PSWD="your-password"
export DATABASE="museumcheck"
```

2. **Start using**:
```bash
museum list
museum stats
museum get "Museum Name"
```

## Commands

| Command | Description |
|---------|-------------|
| `museum list` | List museums with filters |
| `museum get <id>` | Get museum details |
| `museum stats` | View collection statistics |
| `museum check` | Check data integrity |
| `museum export` | Export data (json/csv/sql) |
| `museum query` | Execute custom SQL |

## Use Case

Perfect for:
- Museum data collection projects
- Cultural heritage databases
- Exhibition management systems
- Research data tracking

## License

MIT
