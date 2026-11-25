---
name: macliner
description: "Cleans, updates and checks a Mac in one run: measures, shows a plan with sizes, deletes caches and leftovers for real, asks before anything a person might want, then verifies. Use when someone asks to clean up, free space on, speed up, update or check the security of their Mac."
license: MIT
compatibility: "macOS only. Needs an assistant that runs commands on the Mac itself (a terminal agent) and Python 3 from Apple's command line tools. Uses Homebrew and mas when they are installed. Not for chat apps: they cannot reach the Mac."
---

# Macliner

Cleans, updates and checks a Mac in one run, the way paid cleaner apps do, with
the Mac's own commands and nothing that stays running afterwards. The helper
script `scripts/macliner.py` does the measuring and the deleting; it needs only
Python 3 (standard library) and macOS's own commands.

Answer in the language of the person's message, briefly. A request such as
«clean my Mac» is clear: start at once. Ask only the real choices the plan
names (step 4), never about language, format or where to save.

Rules for the whole run:

- Delete only what a plan line lists, and only through the script. While the
  script is in use, never run `rm` by hand on the person's files (the section «Without the script»
  is the one exception), never empty or «tidy» a folder the plan
  does not name, never use another cleaner app.
- Deleting is for real (no Trash). Lines that need a choice are done only after
  the person says yes to that line.
- Never type or ask for a password and never run `sudo` yourself (the script
  itself only probes `sudo -n true`, which never asks and changes nothing). Lines that
  need an administrator are printed by the script as commands; show them to the
  person to paste into Terminal.
- Never change a setting unless the person asks for that setting. Never install
  macOS updates and never restart the Mac.
- Never install a tool without the person's yes.

## Every run

The script lives in this skill's folder (next to this file), not in the
person's folder: call it by its full path. If that path is not known, find it:

```
find -L ~/.[a-z]* -maxdepth 9 -path '*macliner/scripts/macliner.py' 2>/dev/null | head -1
```

Below, SCRIPT means that full path. Run it with `/usr/bin/python3` (Apple's
Python), not another one.

1. Check that this is a Mac and Python is there: `uname -s` must print
   `Darwin`, and `xcode-select -p` must print a folder. If `xcode-select -p`
   fails, tell the person to run `xcode-select --install` (Apple's installer
   window opens; they click Install), and stop until they say it is done.
   Do not run `/usr/bin/python3` before this check: on a Mac without the
   command line tools it opens that installer window by itself.
2. Make the plan (read-only, 30 seconds to 3 minutes; it changes nothing):

   ```
   /usr/bin/python3 SCRIPT plan
   ```

   Read all of it. Every line ends with its id in square brackets, for
   example `[dev-caches]`. The groups:
   - «Done without asking»: caches, logs, the Trash (items trashed more than a
     day ago), Homebrew's old downloads, unfinished downloads, start-up items
     of removed apps, Xcode build leftovers. All of it comes back by itself
     or was already thrown away.
   - «Needs the person's choice»: the lines step 4 asks about.
   - «Updates»: what is out of date.
   - «Problems found», «Facts», «Already right»: checks of security and
     hardware. Nothing to do; tell the person the problems.
   - «Settings, left as they are unless the person asks».
   - «Never touched»: big folders shown only so the person sees where the
     space is.

   Which steps follow depends on the request. «How much can be freed» or
   «how is my Mac doing»: stop here and report free space, what would go
   without asking (its total), the choices with sizes, problems found. Only
   «update»: skip step 3, ask nothing but the updates (step 4) and go on to
   step 5 with their ids. Otherwise (clean up, speed up, «make it perfect»):
   all steps.

   A group the plan does not print is empty: say «nothing found» for it, not
   that it was not checked. Facts such as «App Store updates were not
   checked: the mas tool is not installed» are reported as they stand; install
   `mas` only with the person's yes (section «Install what is missing»).

   The plan ends with a note on Full Disk Access, on or off. If it is off,
   tell the person in one sentence what was skipped and how to turn it on
   (the note says both), then go on with the plan as it is unless they want
   to do that first.
3. Do the lines that need no choice:

   ```
   /usr/bin/python3 SCRIPT apply
   ```

   It does every «Done without asking» line and prints what it freed. Apps
   that are open are skipped and named; that is normal.
4. If the plan had choices or updates, ask about them in one message: one
   numbered line each, with its size and what it means, grouped (all
   duplicates as one line, all unused apps as one line with their names).
   Take the meaning from the line and its text in brackets. For example:
   «3. Delete the app VideoTool (850 MB), not opened since March, with its
   data?» If the person's request already said to update, do not ask about
   updates: their ids (`upd-brew`, `upd-mas`) go into step 5 as if answered
   yes. For the Safari line, say Safari must be closed and ask the person to
   quit it before they answer; with Safari open the line is skipped. Do not
   ask about settings here. With nothing to ask, go on to step 5
   with the update ids, or to step 6 when there are none.
5. Do the lines the person said yes to, by their ids:

   ```
   /usr/bin/python3 SCRIPT apply --only ID ID ...
   ```

   Write the ids without the square brackets, each in single quotes, because
   some hold spaces: `--only 'app:Video Tool.app' 'dup:3f2a9c01be'`.
   «All duplicates» means every `dup:` id; «yes to everything» means every
   id of step 4. No answer, or «no», means nothing.
6. Check: run `/usr/bin/python3 SCRIPT plan` again. Every line that was done
   must be gone from it. Caches and logs come back a little at once (open
   apps write new ones): those lines count as done when their size fell. If
   another line is still there, look at the «failed» lines of
   the apply output, fix what can be fixed (an app that was open: ask the
   person to quit it, then apply that id again), and name what stays.
7. Report in a few lines: space freed (the sum of the apply outputs, in GB),
   what was updated, problems found, what is left and why, and one line with
   the settings as facts (for example «Settings left as macOS has them:
   firewall on, AirPlay Receiver on, Remote Login off; any of them can be
   changed on request»). Then the commands that need an administrator, if an
   apply printed any, for the person to paste into Terminal. No list of every
   deleted folder.

A plan is good for 3 hours on the same Mac. If `apply` says the plan is too
old, run step 2 again.

## The choices, explained

- Package caches of developer tools (pip, npm, Yarn, Go and others): safe,
  but the next build downloads them again.
- Large cache: one app's cache over 1 GB; it may hold offline media or
  downloaded models.
- Trash items trashed in the last day; installers (`.dmg`, `.pkg`) and items
  untouched for 90 days in Downloads; files over 1 GB.
- Duplicate: files with the same content. The oldest copy stays; the line
  shows which copy stays and which go.
- Data of an app that is not installed: settings and data left by a removed
  app. A command-line tool can use a name that looks like an app's; say so if
  the name looks like one the person uses.
- App not opened for 180 days (or never): the app and its data. An app that
  only other programs start (for example an office suite used for file
  conversions in the background) shows as «never opened»; say that when it
  fits.
- Recent Items: the lists of recent documents, apps and servers.
- Safari: history, cookies and website data; the person is signed out of
  every site. Tabs, bookmarks and passwords stay. Safari must be closed.
- Unsigned program that starts by itself: not proof of harm; the person
  knows whether they installed it.
- Updates: Homebrew (`upd-brew`) and App Store (`upd-mas`). macOS updates are
  only named: the person installs them in System Settings > General >
  Software Update, because the Mac restarts.

## Settings

The baseline is how macOS ships. The plan names each setting that trades
comfort for safety or privacy (firewall, stealth mode, AirPlay Receiver, Mac
Analytics, automatic macOS updates, File Sharing, Remote Login) with its
state and trade-off. Change one only when the person asks for it: for the
firewall and stealth mode, `apply --only set:firewall` or `set:stealth`
(they need an administrator, so the script prints the command for the
person); for the others, tell the person the place in System Settings that
the line names.

## Remembering answers

If the person wants the same answers next time, offer to keep them:

```
/usr/bin/python3 SCRIPT remember --yes ID ... --no ID ... --protect PATH ...
```

`--yes` choices and updates are then done without asking, `--no` lines are
left, and `--protect` paths are never deleted. Settings cannot be given a
standing yes. The file is
`~/.config/macliner/answers.json`; say where it is. Ids of apps, duplicates
and files are tied to that item, so remember only answers the person meant to
keep («never ask about Safari again»).

## Never touched

The script refuses to delete anything inside these, whatever a line says:
Desktop, Documents, iCloud Drive and other cloud folders, the Photos, Music,
TV, iMovie and Final Cut libraries, Mail, Messages, keychains, iPhone
backups, `~/.ssh`, `~/.gnupg`, `~/.config`, `~/.local`, the folders of AI
assistants and coding agents, virtual machines (Parallels, UTM, Tart,
Docker), Xcode simulators and archives, downloaded AI models (Ollama, LM
Studio, Hugging Face), browsers that test tools keep in cache folders, and
files on other disks (their Trash aside). A path the person names is added
with `remember --protect PATH`.

## Without the script

When only this text is available (pasted into an assistant's instructions),
do the same run by hand, read-only first:

1. Measure: `df -h /System/Volumes/Data`;
   `du -sh ~/Library/Caches/* ~/Library/Logs ~/.Trash 2>/dev/null | sort -h | tail -20`;
   `brew cleanup --prune=all -n` and `brew outdated` if Homebrew is there;
   `softwareupdate --list`.
2. Show the plan with sizes: what goes without asking (caches in
   `~/Library/Caches` except folders starting with `com.apple.`, the logs in
   `~/Library/Logs`, Homebrew's cleanup) and what needs a choice (the Trash,
   Downloads, developer caches, apps).
3. Delete only the exact paths of the plan, each with `rm -rf "PATH"` written
   out in full, never with a variable or a wildcard, never inside the «Never
   touched» list above. Quit an app before deleting its cache.
4. Measure free space again and report the difference.

## Known mistakes

- «Never opened» is Spotlight's «last used» date, which apps started only by
  other programs never get; file access times are no help either (every app
  showed «today»). The line is a question, not a verdict.
- Upgrading a Homebrew app (a cask) can quit that app. If it is the app the
  assistant runs in, the session ends mid-run. The script holds back the
  casks of open apps and says so.
- Folder sizes count shared blocks of copied virtual machine disks (APFS
  clones) twice; one Mac showed 357 GB for VMs that used 239 GB. Free space
  before and after is the measure the report uses.
- Cleaner tools have deleted what people needed: one removed an AI
  assistant's saved memory from its folder in the home folder, others swept
  browsers that test tools keep in `~/Library/Caches`. That is why the
  never-touch list holds them.
- Without Full Disk Access, opening Downloads, the Trash or another app's
  container from a terminal can bring up a permission dialog or fail. The
  script checks first and skips them.
- `sudo` in an assistant has no terminal to type a password into, and a
  password typed in the person's own Terminal does not carry over. The script
  never asks for one: it prints the command for the person.
- Dates from `mdls` carry a narrow no-break space before AM or PM; the script
  reads only the date.
- A Homebrew Python printed nothing from `netstat` on one Mac where Apple's
  Python worked; call the script with `/usr/bin/python3`.

## Install what is missing

- Python 3: `xcode-select --install` (Apple's command line tools).
- Homebrew (optional, brew.sh): the person installs it from that page.
- mas (optional, App Store updates): `brew install mas`.

Name the command, wait for the person's yes, then go on.
