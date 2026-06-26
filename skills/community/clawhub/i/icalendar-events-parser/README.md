This skill helps parse iCalendar (.ics) files, expand recurring events, and filter them based on criteria like title, description, and location. It can read from both local files and remote URLs.

## How to set up

This skill requires a few Node.js dependencies (`icalendar-events` and `luxon`).

**One-time setup** (run this in the terminal after the skill is installed):

```bash
cd ~/.openclaw/workspace/skills/icalendar-events-parser # adjust path if needed
npm install
```

Then, the entry point being a CLI, you need to make it executable:

In the terminal, run:
```bash
chmod +x index.js
```

## How to use 
You can ask the agent with sentences like:
- "Parse this calendar feed: [URL or local path]"
- "List all events from this .ics file: [URL or local path]"
- "Show me all events in this calendar that mention 'meeting' in the title"
- "Expand recurring events in this calendar and list all instances"
- "Filter events in this calendar that occur between [start date] and [end date]"