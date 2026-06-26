---
name: prayer-times
description: "Islamic prayer times with reminders, todo list, and journal. Use when: user asks for prayer times (sholat, waktu solat, jadwalsholat), wants to set location, needs reminders, or asks about Islamic productivity."
---

# Prayer Times Skill - OpenClaw

An Islamic prayer times skill that provides prayer schedules, reminders, and connects with todo/journal features.

## Features

### Prayer Times
- Get prayer times for any city or location
- Support for major Indonesian cities and worldwide
- Real-time data from aladhan.com API
- Countdown to next prayer

### Reminders
- Configurable prayer time notifications
- Automatic reminder settings
- Morning and evening notifications

### Todo List
- Add spiritual tasks and goals
- Mark tasks as complete
- Persistent task storage

### Journal
- Daily reflection entries
- Automatic date and time stamping
- Persistent journal storage

## Commands

### Get Prayer Times
```
openclaw, prayer times jakarta
openclaw, waktu sholat surabaya
openclaw, solat bandung
openclaw, jadwal solat
```

### Set Location
```
openclaw, set location to jakarta
openclaw, saya di bandung
openclaw, lokasi surabaya
```

### Todo Commands
```
openclaw, add todo read quran 1 page
openclaw, add todo morning dhikr
openclaw, list todos
openclaw, todos
openclaw, done 1
openclaw, complete 2
```

### Journal Commands
```
openclaw, journal today I am grateful for...
openclaw, journal reflections on the day
openclaw, journal
```

### Reminder Commands
```
openclaw, enable prayer reminders
openclaw, enable reminders
openclaw, ingetin sholat
openclaw, disable reminders
```

### Help
```
openclaw, help
openclaw, prayer times help
```

## Setup

### First Use
1. Set your location: `openclaw, set location to [city]`
2. Test prayer times: `openclaw, prayer times`
3. Optional: Enable reminders: `openclaw, enable prayer reminders`

### Location Support
- **Indonesian cities**: Jakarta, Surabaya, Bandung, Yogyakarta, Medan, Makassar, Denpasar, Semarang, Malang, Palembang, Banjarmasin, Padang, Bengkulu
- **International cities**: Kuala Lumpur, London, New York, Tokyo, Singapore, Dubai, and other major cities

## Storage

All data is stored locally in the OpenClaw memory directory:
- Location: `memory/prayer-times.json`
- Todos: `memory/todos.md`
- Journal: `memory/journal.md`
- Reminder settings: `memory/reminder.json`

## API

This skill uses the free aladhan.com API:
- **Endpoint**: https://api.aladhan.com
- **Method**: ISNA (Islamic Society of North America)
- **Calculation**: Standard school
- **No API key required**
- **Rate limit**: 12 requests per second (generous for personal use)

### Data Flow

1. User sends command (e.g., "prayer times jakarta")
2. Script builds API URL with city parameter
3. Calls aladhan.com API
4. Parses JSON response
5. Formats and displays prayer times

### Fallback Behavior

If the API is unavailable or returns an error:
- Script falls back to general estimation times (based on average Indonesia schedule)
- Shows note that this is estimation not actual calculation
- Does not store or cache wrong data

## Technical Details

- **Language**: Bash script
- **Runtime**: OpenClaw skill system
- **Dependencies**: curl, jq (for JSON parsing)
- **Permissions**: Internet access for API calls
- **Storage**: File-based (JSON/Markdown)
- **Security**: No sensitive data stored, read-only API calls

## Troubleshooting

### Prayer times not showing
- Check your internet connection
- Verify the city name is spelled correctly
- Try a different nearby city

### Reminders not working
- Reminders require cron to be available
- Use manual check: `openclaw, prayer times`

### Todos not saving
- Check that the memory directory exists
- Ensure write permissions are correct

## Version History

- **v1.0.0** - Initial release with prayer times, todos, journal, and reminders

## License

MIT License

## Author

- **Developer**: suluhadi
- **Email**: suluhadi@gmail.com
- **GitHub**: @jrrqd