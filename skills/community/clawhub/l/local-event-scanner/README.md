# Event Scanner

An agent skill for discovering, scoring, and shortlisting local events matched to your taste profile.

Supports optional Google Calendar integration for availability checks and adding events.

## How to Install

To use this skill, clone or copy this repository into your project's custom skills directory as a folder named `local-event-scanner`.

For example, using git from your project root:
```bash
git clone https://github.com/TobiasWestholm/local-event-scanner.git .agents/skills/local-event-scanner
```

Your agent will automatically discover the skill and make it available.

## Setup (Optional)

The setup process can be handled automatically by your agent. If the agent does not set it up automatically, or if you prefer to trigger configuration manually, send the prompt below to your agent (replacing the `FILL IN` placeholders with your actual preferences):

```text
Set up the event scanner skill for me.

First, create my personal configuration files by copying the example files in the skill's assets/ folder:
- Copy taste-profile.example.md to taste-profile.md in the same folder
- Copy sources.example.md to sources.md in the same folder

Then replace the <PLACEHOLDER> blocks in both copied files with my preferences below.

Interests to add to my taste profile:
- (FILL IN: eg ceramics, techno, traveling, italian wines, DIY, ...)

Dealbreakers to add:
- (FILL IN: eg age restrictions, audience restrictions, fully booked events, ...)

Default location: (FILL IN: eg your home city)

Primary sources for my default location:
- (FILL IN, optional: URLs where you usually find good local events)

Optional additional location: (FILL IN, optional: eg your work city)
- (FILL IN, optional: sources for that location)

Optional: install the Google Calendar tool so the scanner can check availability and add events when I ask.

Optional: set up a weekly automation that runs every Monday at 09:00 and finds events for the coming week.
```

## Usage

Just ask your agent for event suggestions. Examples:

- *"What's on in Copenhagen this weekend?"*
- *"Find me AI events in the next two weeks."*
- *"Any good things to do in Paris this summer?"*

The agent will invoke the `local-event-scanner` skill, run discovery and scoring, and return a ranked shortlist with source links and caveats. Scan results are saved to the skill's `runs/` directory.

To add a shortlisted event to your calendar, tell your agent explicitly: *"Add X to my calendar."*
