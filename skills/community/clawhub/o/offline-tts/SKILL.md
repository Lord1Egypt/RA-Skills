---
name: offline-tts
description: "Reads a text aloud into an audio file (mp3, m4a or wav) with the computer's own voices, offline: Siri voices on a Mac, Piper or system voices on Linux and Windows, numbers and dates read right. Use when someone wants a text, article, file or chat answer turned into speech to listen to later."
license: MIT
compatibility: "Needs an assistant that runs commands on the person's computer (a terminal agent). Best on macOS 13 or newer; Linux through Piper or espeak-ng; Windows through its built-in voices. Chat apps have no voices in their sandbox."
---

# Offline TTS

Turns a text into an audio file on the person's computer with voices that
are already there or installed once, offline. Answer in the language of the
person's message, briefly.

The audio is made only by running a speech program on the person's
computer. If you cannot run commands here, say in one sentence that this
skill needs an assistant that runs commands on the person's computer, and
stop. Never say a file was made unless the command wrote it and you checked
it, never play the audio unless asked, and never offer your own voice mode,
a summary or a retelling instead of the file.

## Before the first file: ask once

Three choices change the result and only the person can make them. Unless
the request already names them (or says «any voice», «just do it»), do not
start yet: your first reply is only this short message, after you have
listed the voices (step 2 below), with the default for each:

1. Voice: two to four real voices for the text's language, by the names the
   computer uses, with their gender. Default: the best female voice.
2. Speed: normal, or faster or slower (for example 1.5× or 0.8×).
   Default: normal.
3. Where to save it and the format. Default: mp3 next to the text file, or
   in the Downloads folder when the text came in the message.

A reply such as «ok» or «go» takes the defaults. Keep the answers for the
rest of the conversation and do not ask again. If the agent keeps files,
offer once to save the answers in `~/.config/offline-tts.txt` (plain
lines such as `voice: Voice 2`) and read that file before asking next time.

## Every file

1. Find the engine for this computer, once per conversation (section
   «Engines»): macOS with the `tts` command, macOS without it, Linux,
   Windows.
2. List the voices for the text's language with that engine's command.
3. Put the text in a plain UTF-8 file in a temporary folder (never change
   the person's own file). Remove what is not meant to be heard: Markdown
   marks, links, code, tables turned into sentences.
4. Unless the engine is `tts`, prepare the text for the ear (section
   «Text for the ear»). `tts` does this itself for Russian and Ukrainian.
5. Run the engine's command with the voice, speed and output path.
6. Check the file (section «Check») and report in one or two lines: name and
   folder, length in minutes, voice, speed.

File name: the text file's name, or the first three or four words of the
text, with the format's extension. If that name exists, add « (2)»; never
overwrite a file.

## Engines

### macOS with `tts` (best)

`tts` is a free open-source command (MIT, github.com/geragarazagh/tts). It
is the only way found for a command to use the Siri voices of macOS; it
also writes numbers, dates, units and abbreviations as words in Russian and
Ukrainian in the right grammatical case and gives each paragraph the voice
of its language.

Find it, in this order, and use the first that prints a line starting with
`usage: tts [-v VOICE]`:

```
/Applications/TTS.app/Contents/Resources/tts -h
tts -h
```

Another program called `tts` (Coqui TTS has one) prints something else: do
not use it. Below, `TTS` stands for the full path of the one that worked.

- Voices: `TTS -L ru` (any language code: `en`, `uk`, `de`). Columns:
  language, name, gender, kind (Siri is best, then premium, enhanced,
  compact), which voice `female` and `male` pick, id. Siri voices are
  named «Voice 1», «Voice 2» in English.
- See the text as it will be read: `TTS -t FILE` (one `[lang]` line per
  paragraph). Use it when numbers or language matter.
- Make the file:

```
TTS -v female -r 1 -o "OUTPUT.mp3" "TEXT.txt"
```

`-v`: `female`, `male`, or a name or id from the list (`"Voice 1"`,
`Milena`; several, comma-separated, one per language). `-r`: speed, 1 =
normal, 0.6 to 3.9 (the voice speaks faster itself, no stretching). `-o`: a
folder or a file path; the extension sets the format (mp3, m4a, wav, aiff).
mp3 needs ffmpeg; without it use `.m4a`. It prints the path and length,
for example `/Users/ann/Downloads/Report.mp3  1:27`.

A language with no Siri voice on the Mac falls back to the best other
voice. Siri voices have to be downloaded once, by the person: System
Settings › Accessibility › Read & Speak (Spoken Content on macOS 13-15) ›
the ⓘ next to System voice (Manage Voices… on 13-15) › the language › a
Siri voice. Mention it once when `-L` shows no Siri voice for the language.

### macOS without `tts`

Offer to install it first (it is much clearer for Russian and Ukrainian and
has Siri voices); see «Install». If the person declines, use the built-in
`say`, which has no Siri voices and reads digits less well:

- Voices: `say -v '?' | grep ru_RU` (the locale: `en_US`, `uk_UA`, `de_DE`).
  Prefer a name with «(Premium)» or «(Enhanced)».
- Make the file, m4a:

```
say -v "Milena" -r 175 -f "TEXT.txt" --file-format=m4af --data-format=aac -o "OUTPUT.m4a"
```

`-r` is words per minute; normal is about 175 to 180. For a speed, multiply:
1.5× is about 265, 2× about 350. For mp3: make a `.wav` with
`--file-format=WAVE --data-format=LEI16`, then
`ffmpeg -i OUTPUT.wav -c:a libmp3lame -q:a 4 OUTPUT.mp3`.

### Linux

Piper (offline neural voices, GPL-3.0; github.com/OHF-Voice/piper1-gpl), or
espeak-ng when Piper cannot be installed (robotic, but everywhere).

- Piper lives in its own virtual environment, `~/.local/share/piper`
  («Install»); its Python is `~/.local/share/piper/bin/python3`. Check:
  `~/.local/share/piper/bin/python3 -m piper --help`.
- Piper voices are downloaded once each (30 to 120 MB). Defaults: English
  `en_US-lessac-medium`; Russian `ru_RU-irina-medium` (female),
  `ru_RU-dmitri-medium` (male); Ukrainian `uk_UA-tetiana-high` (female),
  `uk_UA-mykyta-high` (male). All voices:
  `~/.local/share/piper/bin/python3 -m piper.download_voices`. Download one
  with the person's yes:

```
~/.local/share/piper/bin/python3 -m piper.download_voices --data-dir ~/.local/share/piper-voices ru_RU-irina-medium
```

- Make the file (speed: `--length-scale` is 1 divided by the speed: 1.5× is
  `0.67`, 0.8× is `1.25`):

```
~/.local/share/piper/bin/python3 -m piper --data-dir ~/.local/share/piper-voices -m ru_RU-irina-medium --length-scale 1 -i "TEXT.txt" -f "OUTPUT.wav"
ffmpeg -i "OUTPUT.wav" -c:a libmp3lame -q:a 4 "OUTPUT.mp3"
```

- espeak-ng: `espeak-ng -v ru -s 175 -f "TEXT.txt" -w "OUTPUT.wav"`
  (`-s` words per minute; `espeak-ng --voices=ru` lists them).

### Windows

The built-in voices through Windows PowerShell (`powershell.exe`, part of
every Windows 10 and 11). Russian voices (Irina, Pavel) come with the
Russian speech pack: Settings › Time & language › Speech › Add voices.
Windows has no Ukrainian voice; for Ukrainian use Piper (`python -m pip
install piper-tts`, then the Linux commands with `python` in place of
`~/.local/share/piper/bin/python3`).

Write the lines below to a file `speak.ps1` in the temporary folder, with
the voice name from the list, the paths and the rate filled in, and run it
with `powershell -NoProfile -ExecutionPolicy Bypass -File speak.ps1` (the
bypass applies to this one run). To list the voices (name, language,
gender), run a file with only the first three lines. If no voice of the
text's language is listed, use Piper.

```
Add-Type -AssemblyName System.Speech
$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
$s.GetInstalledVoices() | ForEach-Object { $_.VoiceInfo.Name + ' | ' + $_.VoiceInfo.Culture + ' | ' + $_.VoiceInfo.Gender }
$s.SelectVoice('VOICE NAME FROM THE LIST')
$s.Rate = 0
$s.SetOutputToWaveFile('C:\Users\NAME\Downloads\OUTPUT.wav')
$s.Speak([IO.File]::ReadAllText('C:\path\TEXT.txt', [Text.Encoding]::UTF8))
$s.Dispose()
```

`Rate` is -10 to 10, 0 = normal. How much one step changes the speed
depends on the voice: for a speed other than normal, make the file at
`Rate` 0 and at a first guess (3 for about 1.5×), compare their lengths,
and adjust once. Then mp3 with ffmpeg as above, if it is installed.

### In a chat app

Chat sandboxes have no voices. A throwaway Linux sandbox with internet may
install Piper (`pip install piper-tts`; then the «Linux» commands with
`python3` in place of `~/.local/share/piper/bin/python3`) and download one
voice without asking; give the result as a download and never ask where to
save it. If the install or the download is blocked, say so and stop.

## Text for the ear

Engines other than `tts` read digits and signs badly (measured: macOS
`say` dropped «₴» and «ИИ» and spelled «ГБ» as letters). Before making the
file, rewrite in the prepared copy, in the text's own language:

- every number as words, in the grammatical case the sentence needs
  («с 18 ГБ» → «с восемнадцати гигабайт», «в 2026 году» → «в две тысячи
  двадцать шестом году»); dates, times, money, percentages, ordinals, Roman
  numerals, ranges («2–3 дня» → «два-три дня»);
- signs and abbreviations as words: % $ € ₴ № ~ + = & /, «т. е.», «e.g.»,
  units (GB, km/h), acronyms read as words or letters the way people say
  them;
- links as the site's name; emoji removed.

Change nothing else: do not shorten, translate, correct or retell the
text. For a text over about 20,000 characters, rewrite only the paragraphs
with digits or signs and keep the rest as it is.

## Check

- The file exists and is not empty.
- Its length is plausible: about 1 minute for each 800 to 1,000
  characters at normal speed, divided by the speed. Much under half of
  that means part of the text was lost; say so. Length:
  `ffprobe -v error -show_entries format=duration -of csv=p=0 "FILE"`, on a
  Mac also `afinfo "FILE" | grep duration`.
- One audio stream, the format asked for.

## Publishing the audio

Only when the person says the file is for others (a video, a podcast, a
sale) and the voice is Apple's, say once: the macOS licence allows its
system voices for personal, non-commercial use only and forbids publishing
recordings of them. Piper voices each carry their own licence in their
`MODEL_CARD` file. Then do what the person decides.

## Install

Name the command for the person's system and wait for a yes.

- macOS 13 or newer, Apple Silicon, Homebrew: `brew install
  geragarazagh/tap/tts` (the TTS app; the command is inside it at
  `/Applications/TTS.app/Contents/Resources/tts`). Without Homebrew: the
  TTS.dmg from github.com/geragarazagh/tts/releases. On an Intel Mac, the
  command alone: `mkdir -p ~/.local/bin && curl -fsSL
  https://raw.githubusercontent.com/geragarazagh/tts/v0.5/tts -o
  ~/.local/bin/tts && chmod +x ~/.local/bin/tts`.
- mp3 on a Mac: `brew install ffmpeg`.
- Linux: `sudo apt install ffmpeg espeak-ng python3-venv` (or the system's
  package manager), then Piper in a virtual environment of its own:
  `python3 -m venv ~/.local/share/piper` and
  `~/.local/share/piper/bin/pip install piper-tts`.
- Windows: nothing for the built-in voices; Piper: `python -m pip install
  piper-tts`; ffmpeg: `winget install Gyan.FFmpeg`.

## Known mistakes

- Siri voices are not reachable with `say`: `say -v "Voice 2"` and
  `say -v com.apple.siri…` print no error and quietly use another voice.
  Use `tts` for Siri voices.
- `say -o OUTPUT.m4a` without `--file-format=m4af --data-format=aac` writes
  uncompressed sound into a file named .m4a.
- Piper from pip on macOS (Apple Silicon, versions 1.6.1 to 1.8.0) writes an
  empty file and prints `Error processing file '/Users/runner/…/phontab'`
  (an open Piper bug). On a Mac use `tts` or `say`.
- Piper installed with `pipx` gives only the `piper` command: the voice
  downloader `python3 -m piper.download_voices` then fails with «No module
  named 'piper'». Install it into its own virtual environment («Install»).
- `pip install piper-tts` under the newest Python can fail with
  «conflicting dependencies» (seen with Python 3.15: its speech library had
  no build for it yet; 3.12 worked). Use a virtual environment with an
  older Python, for example `uv venv -p 3.12`.
- A text pasted into a command line breaks on quotes and length: always
  write it to a file first and pass the file.
- Never retry a failing command more than twice. Say what failed and what
  the person can do.
