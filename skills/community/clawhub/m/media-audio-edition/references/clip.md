# Make the 45-second clip

Use these steps only when the clip is planned: ffmpeg lists the `subtitles` and
`showwaves` filters and the `libx264` encoder, and the episode runs at least 90
seconds. Everything here happens on this computer at no cost. Work in the
episode folder, and keep file names free of spaces and colons.

1. Find the clip in the episode. Its start is 5.6 seconds (the intro sting and
   its gap) plus the lengths of the speech.txt lines before the clip's part;
   its length is that part's length. Measure each file with:

   ```
   ffprobe -v error -show_entries format=duration -of csv=p=0 work/part-03.wav
   ```

2. Write work/clip.srt. The first caption covers the whole clip at the top of
   the frame: the episode title, then "AI voices" on the next line. After it
   come the clip's own words as short captions of at most two lines of 32
   characters. Start each caption at the part's length × (characters before it
   ÷ the part's characters):

   ```
   1
   00:00:00,000 --> 00:00:44,600
   {\an8}Why we killed our free plan
   AI voices

   2
   00:00:00,000 --> 00:00:03,200
   We stopped offering a free plan
   in March.

   3
   00:00:03,200 --> 00:00:06,100
   Within a month, paying customers
   were asking better questions.
   ```

3. Render a 1080 × 1080 clip with a moving waveform and the captions. `-y` may only
   replace a clip-45s.mp4 this run made; never replace an earlier episode's clip:

   ```
   ffmpeg -y -v error -ss <start> -t <length> -i episode.mp3 -f lavfi -i color=c=0x15171c:s=1080x1080:r=30 -filter_complex "[0:a]showwaves=s=1080x300:mode=cline:rate=30:draw=full:colors=white[w];[1:v][w]overlay=0:390:shortest=1,subtitles=work/clip.srt:force_style='Fontsize=16,MarginV=60,MarginL=20,MarginR=20'[v]" -map "[v]" -map 0:a -c:v libx264 -pix_fmt yuv420p -c:a aac -b:a 160k -shortest clip-45s.mp4
   ```

4. Check it:

   ```
   ffprobe -v error -show_entries stream=codec_type:format=duration -of csv=p=0 clip-45s.mp4
   ```

   The output lists `video`, `audio` and a length within 0.3 seconds of the
   part's length.

If a step fails, skip the clip and give the reason in the summary line, for
example "clip skipped: this computer's ffmpeg can't draw captions". The episode
and the other files don't depend on it.
