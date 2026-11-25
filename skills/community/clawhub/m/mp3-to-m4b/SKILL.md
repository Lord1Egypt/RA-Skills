---
name: mp3-to-m4b
description: "Joins a folder of audio files, such as the mp3 parts of an audiobook, into one .m4b with chapters, cover and book tags that Apple Books, BookPlayer and other players read. Use when someone wants to make an audiobook or m4b from mp3 files, merge audiobook parts, or add chapters and a cover."
license: MIT
compatibility: "Needs an assistant that runs commands on the person's computer (a terminal agent) with ffmpeg; Python 3 for the helper script, which is optional. Chat apps only when their sandbox has ffmpeg and the files fit the upload limit."
---

# MP3 to M4B

Turns a folder of audio files (mp3 parts of an audiobook, or m4a, ogg, flac,
wav) into one `.m4b` file: the parts joined in the right order, one chapter
per part with real chapter names, the cover, title, author and narrator.
Apple Books, BookPlayer, Smart AudioBook Player, VLC and most players read it.

Answer in the language of the person's message, briefly. When the message
names the folder (or the files are attached), start at once and ask nothing.
Ask only when it is unclear which files make the book.

The job is done only by running ffmpeg on the files. If you cannot run
commands here, say so in one sentence and stop. Never read the book aloud
with a voice, generate audio, or retell it instead. Never change, rename or
delete the person's files; write only the new `.m4b`. Never say the book is
ready unless the check in step 5 passed.

## Every book

The helper script `scripts/m4b.py` lives in this skill's folder, not in the
person's folder: call it by its full path. It needs only Python 3 and
ffmpeg. Without Python, use «Without the script» below.

1. Check the tools once per conversation: `ffmpeg -version` and
   `python3 --version` (on Windows `python --version`). If one is missing,
   see «Install» and wait for a yes.
2. Look at the plan:

   ```
   python3 /full/path/to/skills/mp3-to-m4b/scripts/m4b.py plan "FOLDER"
   ```

   It prints the parts in the order they will be joined, the length of each,
   the chapter name each part gets, the book title and author from the
   files' tags, the cover it found and the sound settings. It changes
   nothing and takes no options except `--order tags`; titles, cover and
   chapters are given to `build`.
3. Read the plan as an editor and fix what is wrong before building:
   - Order. Parts must follow the book: 1, 2, … 9, 10, not 1, 10, 2 (the
     script sorts numbers in names as numbers). If the file names and the
     track numbers disagree, the plan warns: run plan again with
     `--order tags`, and use the order whose chapter names follow the book.
   - Chapter names. Good: «The Happy Prince», «Chapter 3», «Part Two,
     Chapter 1». Bad: file-name leftovers such as «hp 01 wilde 64kb», or
     the same name on every part. When they are bad, write a text file with
     one chapter name per line, one line per part, in order, and pass it as
     `--chapters FILE`. Take names from the file names, the tags or the
     book's table of contents; do not invent titles. If you do not know
     them, use «Chapter 1», «Chapter 2», …. Write the chapters file in a
     temporary folder (not among the person's files) and delete it at the end.
   - Several parts make one chapter, or one long file holds several
     chapters: write the chapters file as lines `PART Title` (the chapter
     starts at that part, counted from 1; parts without a line continue the
     chapter before) or `PART+SECONDS Title` (it starts that many seconds
     into the part). Use exact times only when the person gave them or the
     file names them.
   - Title and author: taken from the tags (album, artist). If they are
     missing or wrong, pass `--title "…"` and `--author "…"`. Add
     `--narrator "…"` and `--year` when known.
   - Cover: an image named cover, folder or front in the folder, else the
     only or largest image there, else the art inside the files. Another
     image: `--cover FILE`. None: the book is made without a cover; say so.
4. Build:

   ```
   python3 /full/path/to/skills/mp3-to-m4b/scripts/m4b.py build "FOLDER" -o "OUT.m4b" --title "…" --author "…"
   ```

   Put the `.m4b` next to the folder (in the folder that contains it), named
   after the book: `The Happy Prince and Other Tales.m4b`. Use another place
   when the person named one. If the name is taken, add « (2)». A ten-hour
   book takes a few minutes; wait for it.
5. Check:

   ```
   python3 /full/path/to/skills/mp3-to-m4b/scripts/m4b.py check "OUT.m4b" --parts NUMBER_OF_CHAPTERS
   ```

   It must end with `ok`. Read every «warning» and «problem» line. A
   warning that a part «plays» shorter than its header says means a file is
   cut off (often an unfinished download): tell the person which one.
6. Report in three or four lines: the file and its folder, length, size,
   number of chapters, cover yes or no, and what you decided or guessed
   (order, names, title).

## Sound settings

The script chooses these; set them yourself only on request or without the
script.

- AAC in an `.m4b`, the same sample rate as the parts. Mono when the parts
  are mono or their two channels carry the same sound (common in
  audiobooks; half the size). 64 kbps per channel at most and never above
  the source: re-encoding cannot add quality, and 64 kbps mono is plenty
  for a voice. `--bitrate` and `--channels` override.
- Encoder: `aac_at` (Apple's, on macOS) when ffmpeg lists it, else
  `libfdk_aac`, else ffmpeg's own `aac`.
- One encode of the whole book from the decoded parts, so the chapter
  marks fall on the exact sample where each part starts.

## Without the script

The same result with ffmpeg alone, for an assistant without Python or a
host that does not allow scripts. Make a temporary folder (TEMP below) for
the working files; the person's folder gets nothing but the finished book.

1. List the parts in the book's order (numbers in names sorted as numbers)
   into `TEMP/list.txt`, one line each with the part's full path:
   `file '/full/path/happyprince_01.mp3'`. In a name with an apostrophe,
   write it as `'\''`.
2. Measure each part:
   `ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "PART"`.
   A chapter starts at the sum of the lengths of the parts before it.
3. Write `TEMP/chapters.txt`, times in milliseconds, one block per chapter:

   ```
   ;FFMETADATA1
   title=The Happy Prince and Other Tales
   album=The Happy Prince and Other Tales
   artist=Oscar Wilde
   album_artist=Oscar Wilde
   genre=Audiobook
   [CHAPTER]
   TIMEBASE=1/1000
   START=0
   END=1433208
   title=The Happy Prince
   [CHAPTER]
   TIMEBASE=1/1000
   START=1433208
   END=2370412
   title=The Nightingale and the Rose
   ```

   The last chapter ends at the total length. A `=`, `;`, `#` or `\` inside
   a title needs a `\` before it.
4. Join and encode (mono 64 kbps; for stereo parts whose channels differ use
   `-ac 2 -b:a 128k`; on macOS use `-c:a aac_at`):

   ```
   ffmpeg -f concat -safe 0 -i TEMP/list.txt -vn -ac 1 -c:a aac -b:a 64k TEMP/audio.m4a
   ```
5. Add chapters, cover and tags without encoding again:

   ```
   ffmpeg -i TEMP/audio.m4a -i TEMP/chapters.txt -i "COVER.jpg" -map 0:a -map 2:v -disposition:v:0 attached_pic -map_metadata 1 -map_chapters 1 -c copy -metadata media_type=2 -movie_timescale 1000 -f mp4 -brand "M4B " "OUT/BOOK TITLE.m4b"
   ```

   OUT is the folder that contains the book's folder (step 4 above). The
   cover is an image file (a .jpg or .png in the folder); without one, leave
   out `-i "COVER.jpg" -map 2:v -disposition:v:0 attached_pic`.
6. Check: `ffprobe -v error -show_chapters -show_streams "OUT/BOOK TITLE.m4b"`
   must list every chapter and, besides the audio, a stream with
   `codec_tag_string=text` (the chapter track Apple's players read). Delete
   the TEMP folder.

Header lengths of mp3 files can be wrong (a cut-off download, a broken
VBR header): if the total length of the result differs from the sum in
step 2 by more than a second or two, the chapter marks drift; say so, or
use the script, which measures the decoded sound.

## Known mistakes

- ffmpeg 9 drops the chapter track that Apple Books and BookPlayer read
  when the cover is copied straight out of an mp3 (`-i part.mp3 -map 0:v -c
  copy`) and a chapter is longer than about eight minutes; only the Nero
  chapters stay, which Apple's players ignore (ffmpeg issue 25317; on 9.0.2
  Apple's AVFoundation saw 0 of 5 chapters). `-movie_timescale 1000` keeps
  it (5 of 5). Always pass it; the check reports a missing chapter track.
- Sorting names as text puts «Track 10» before «Track 2». Sort numbers as
  numbers, then compare with the track numbers in the tags.
- The extension decides: Apple Books on the Mac treats the same file as a
  song when it ends in `.m4a` and as an audiobook with chapters when it
  ends in `.m4b`.
- Joining with `-c copy` (mp3 into an mp4 container, or m4a parts with
  their own encoder delay) gives small gaps or clicks at every join and
  chapter times that drift; encode the joined sound once.
- A «stereo» file whose two channels are the same doubles the size for
  nothing; check before choosing stereo.
- More than 255 chapters: the Nero chapter list, which some players use,
  holds only 255. Join short parts into longer chapters.
- Titles from tags often carry the track number or the book's name
  («01 - The Happy Prince», «Moby Dick - Chapter 1»); the script strips
  what every title shares and leading numbers. Check the result anyway.

## Install

- macOS: `brew install ffmpeg` (Homebrew from brew.sh). Python 3 comes with
  the Xcode command line tools: `xcode-select --install`.
- Windows: `winget install Gyan.FFmpeg` and `winget install Python.Python.3.13`.
- Linux: ffmpeg and python3 from the system's package manager, for example
  `sudo apt install ffmpeg python3`.

Name the command, wait for the person's yes, then go on. Install nothing
else: the script uses only Python's standard library.
