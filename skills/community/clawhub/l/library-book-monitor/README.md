# Library Book Monitor Skill

An OpenClaw skill to monitor library book availability and get notified when books become available for borrowing.

## Features

- 📚 **Book Management** - Add, remove, and track books you want to borrow
- 🔍 **Availability Check** - Query book availability at Shenzhen Library
- ⏰ **Scheduled Monitoring** - Automatically check book status on a schedule
- 🔔 **Smart Notifications** - Get notified when books become available
- ⚙️ **Configurable** - Support for different library configurations

## Installation

```bash
npx clawhub@latest install openclaw-community/skill-library-book-monitor
```

Or install via npm:

```bash
npm install -g @openclaw-community/skill-library-book-monitor
```

## Prerequisites

Before using this skill, ensure you have:

1. Python 3.8+ installed
2. Required Python dependencies:
   ```bash
   pip install requests pyyaml
   ```
3. Configuration file set up (see Configuration section)

## Usage

### Adding a Book

```
Add book "Python Programming" by "Guido van Rossum" with monitoring enabled
```

### Listing All Books

```
List all monitored books
```

### Checking Availability

```
Check availability of all books
```

### Removing a Book

```
Remove book with ID abc123
```

### Toggling Monitoring

```
Toggle monitoring for book abc123
```

### Starting Scheduled Monitoring

```
Start monitoring scheduler
```

## Configuration

Create a `config.yaml` file in your project directory:

```yaml
library:
  name: "Shenzhen Library"
  base_url: "https://www.szlib.org.cn/"
  search_url: "https://www.szlib.org.cn/opac/"
  timeout: 30

scheduler:
  enabled: true
  interval_minutes: 30
  retry_on_failure: true
  max_retries: 3

notification:
  enabled: true
  methods:
    - console
    - email
  email:
    smtp_server: smtp.qq.com
    smtp_port: 587
    sender: your_email@qq.com
    password: your_smtp_password
    recipients:
      - recipient@example.com
```

## How It Works

1. **Book Addition**: When you add a book, the skill stores the book information and searches the library catalog
2. **Availability Check**: The skill queries the library's API to check if the book is available for borrowing
3. **Location Tracking**: If available, the skill records which library locations have copies
4. **Scheduled Monitoring**: The skill can automatically recheck availability on a schedule
5. **Notifications**: When a book becomes available, the skill sends notifications via configured channels

## Extending to Other Libraries

The skill is designed to be extensible. To add support for a new library:

1. Create a new scraper class inheriting from `LibraryScraper`
2. Implement the `search_book` method
3. Add the new scraper to the configuration

Example:

```python
class MyLibraryScraper(LibraryScraper):
    def search_book(self, book: Book) -> Tuple[bool, List[str], str]:
        # Implement library-specific search logic
        pass
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenClaw community for the skill framework
- Shenzhen Library for providing the API
- Contributors and users of this skill

## Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/openclaw-community/skill-library-book-monitor/issues) page
2. Join the [OpenClaw Discord](https://discord.gg/openclaw)
3. Submit a new issue with details about your problem

---

**Happy Reading!** 📚