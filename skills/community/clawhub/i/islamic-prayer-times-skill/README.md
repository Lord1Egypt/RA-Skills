# Prayer Times Skill

An OpenClaw skill that provides Islamic prayer times with spiritual productivity tools including todo lists and journal integration.

## Overview

This skill enables users to:
- Get accurate prayer times for any city worldwide
- Manage spiritual tasks and goals
- Track daily reflections through journaling
- Enable prayer time reminders

## Features

### Prayer Times
- Real-time prayer schedules via aladhan.com API
- Support for all major Indonesian cities and worldwide locations
- Automatic calculation using ISNA method

### Todo Management
- Add spiritual tasks and goals
- List and complete tasks
- Persistent storage in memory

### Journal
- Daily reflection entries
- Automatic date/time stamping
- Persistent storage

### Reminders
- Configurable prayer time notifications
- Settings saved for future sessions

## Installation

```bash
clawhub install prayer-times
```

Or manually copy to your skills directory.

## Usage

### Get Prayer Times

```
openclaw, prayer times jakarta
openclaw, jadwal solat surabaya
openclaw, solat bandung
```

### Set Location

```
openclaw, set location to jakarta
openclaw, saya di bandung
```

### Todo Management

```
openclaw, add todo read quran 1 page
openclaw, list todos
openclaw, done 1
```

### Journal

```
openclaw, journal grateful for today
openclaw, journal today was productive
openclaw, journal
```

### Reminders

```
openclaw, enable prayer reminders
openclaw, disable reminders
```

### Help

```
openclaw, help
```

## Configuration

### Location Storage
Location is stored in: `memory/prayer-times.json`

### Data Storage
- Todos: `memory/todos.md`
- Journal: `memory/journal.md`
- Reminder settings: `memory/reminder.json`

## API

Uses free prayer times APIs:
- aladhan.com API (free, no key required)
- Method: ISNA (Islamic Society of North America)
- Calculation: Standard school

## Supported Cities

### Indonesia
Jakarta, Surabaya, Bandung, Yogyakarta, Medan, Makassar, Denpasar, Semarang, Malang, Palembang, Banjarmasin, Padang, Bengkulu

### International
Kuala Lumpur, London, New York, Tokyo, Singapore, Dubai, and other major cities

## Technical Details

- **Language**: Bash script
- **API**: aladhan.com (REST)
- **Storage**: File-based (markdown/JSON)
- **Permissions**: Internet access for API calls

## License

MIT License

## Author

- **Developer**: suluhadi
- **Email**: suluhadi@gmail.com
- **GitHub**: @jrrqd

## Related

- [Islamic Prayer Times Chrome Extension](https://github.com/jrrqd/islamic-prayer-times-journal)
- [Airdrop Tracker Extension](https://github.com/jrrqd/crypto-airdrop-tracker)