# Step 0: Setup

This step is used to configure user preferences in the files `skills/event-scanner/assets/sources.md` and `skills/event-scanner/assets/taste-profile.md`.

## Procedure
Locate the following files:
- `skills/event-scanner/assets/sources.md`
- `skills/event-scanner/assets/taste-profile.md`

You may freely change these files and these files only, based on the preferences the user tell you about.

If they don't exist, follow the setup procedure below to set up initial user preferences, otherwise ignore it.


## Setup

This procedure shoul only be used if the required files do not exist. Ask the user to give their preferences in the sections marked with `FILL IN` placeholders. Go through the below steps in order. When user input is needed, ask abou one step at a time.

1. First, create their personal configuration files by copying the example files in skills/event-scanner/assets/:
- Copy taste-profile.example.md to taste-profile.md in the same folder
- Copy sources.example.md to sources.md in the same folder

2. Ask the user for what Interests should be added to their taste profile, and replace the relevant <PLACEHOLDER> blocks in both copied files with the preferences you collect:
- (FILL IN: eg ceramics, techno, traveling, italian wines, DIY, ...)

3. Ask the user for what Dealbreakers to add, and replace the relevant <PLACEHOLDER> blocks in both copied files with the preferences you collect:
- (FILL IN: eg age restrictions, audience restrictions, fully booked events, ...)

4. Ask the user for what Default location to add and if they have any primary sources they want you to use for that location, and replace the relevant <PLACEHOLDER> blocks in both copied files with the preferences you collect:  
- (FILL IN: eg your home city)
- (FILL IN, optional: URLs where you usually find good local events)

5. Ask the user if they have any additional location they they want to use as default and save source preferences for, and replace the relevant <PLACEHOLDER> blocks in both copied files with the preferences you collect:  
- (FILL IN, optional: optional additional location, eg your work city)
- (FILL IN, optional: sources for that location)

6. Ask the user if they want to install the google calendar tool so the scanner can check availability and add events when asked. If the answer is yes, ask the user what calendar provider they use and attempt to enable that connector. If you don't succeed, ask the user to enable it themselves.

7. Ask the user if they want to set up a weekly automation. If the answer is yes, collect the below information from the user and set up an automation with the prompt "What interesting events can you find in the next {period}?" that runs on {time}.
- 'period': how far forward should it scan? Default is one week.
- 'time': what day and time should the automation run?

## Output
Adjustments to any of the two files.

When starting this step, explicitly say: "[Configuring preferences]"
