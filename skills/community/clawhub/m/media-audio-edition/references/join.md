# Join, trim and check the episode

Everything here happens on this computer at no cost. Work in the episode folder.

Without ffmpeg or ffprobe, don't join. Hand over the parts and the music in order and say
plainly: "I couldn't join the parts or trim the music because this computer has no ffmpeg.
Play them in this order: …". Loudness: not measured. Clip: skipped.

1. Turn every kept part into the same format, fading its last 50 ms and adding 0.25
   seconds of silence after it (one command per part), and make a 0.6-second gap:

   ```
   ffmpeg -y -v error -i work/part-01.mp3 -af "areverse,afade=t=in:d=0.05,areverse,apad=pad_dur=0.25" -ar 44100 -ac 2 -c:a pcm_s16le work/part-01.wav
   ffmpeg -y -v error -f lavfi -i anullsrc=r=44100:cl=stereo -t 0.6 -c:a pcm_s16le work/gap.wav
   ```

2. Write work/speech.txt from the saved list of parts, in order, with the gap between them
   (`file 'part-01.wav'`, `file 'gap.wav'`, `file 'part-02.wav'` and so on). Join the
   narration at −16 LUFS, then measure it; the speech level is the I under "Integrated loudness":

   ```
   ffmpeg -y -v error -f concat -safe 0 -i work/speech.txt -af loudnorm=I=-16:TP=-1.5:LRA=11 -ar 44100 -c:a pcm_s16le work/speech.wav
   ffmpeg -hide_banner -nostats -i work/speech.wav -af ebur128=framelog=quiet -f null -
   ```

3. Trim the music to a 5-second sting set 2 LU below the speech level (speech at
   −16.2 LUFS gives I=-18.2 below), then check its length: 4.9–5.1 seconds. When reusing,
   use podcast/sting-raw.mp3 as the input. If the music came back shorter than 5 seconds,
   keep its length, start the fade 0.6 seconds before its end, and report the real length.

   ```
   ffmpeg -y -v error -i work/sting-raw.mp3 -af "atrim=0:5,afade=t=out:st=4.4:d=0.6,loudnorm=I=-18.2:TP=-2:LRA=7" -ar 44100 -ac 2 -c:a pcm_s16le work/sting-5s.wav
   ffprobe -v error -show_entries format=duration -of csv=p=0 work/sting-5s.wav
   ```

4. Write work/join.txt with five lines, `file 'sting-5s.wav'`, `file 'gap.wav'`,
   `file 'speech.wav'`, `file 'gap.wav'` and `file 'sting-5s.wav'`, then join and re-encode.
   `-y` may only replace an episode.mp3 this run made; if the folder holds one from an
   earlier episode, stop and use a new folder instead (see What the user gets):

   ```
   ffmpeg -y -v error -f concat -safe 0 -i work/join.txt -ar 44100 -c:a libmp3lame -b:a 128k episode.mp3
   ```

5. Check:
   - speech.txt names every part once, in order;
   - speech.wav is within 0.3 seconds of its speech.txt lines added up, and episode.mp3 of
     its join.txt lines (measure each with the ffprobe command above);
   - `ffmpeg -v error -i episode.mp3 -f null -` prints nothing;
   - the ebur128 command above, run on episode.mp3, shows I between −17 and −15 LUFS; run
     with `-t 5` (intro) and `-sseof -5` (outro) before `-i`, it shows each sting 1 to 3 LU
     below the speech level. Report the figures. Without the loudness filters, leave out
     the loudnorm options and say loudness wasn't set or measured.

A failed join is local: fix it and run it again; never pay to remake audio because of it.

Copy work/sting-raw.mp3 to podcast/sting-raw.mp3 and write podcast/show.json (show name,
format, voices with their voice_ids, tool_id and the share of list price the narration
settled at).
