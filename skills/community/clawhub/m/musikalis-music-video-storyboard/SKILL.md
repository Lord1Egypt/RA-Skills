---
name: music-video-storyboard
description: Plan a story music video for a song - the story, the cast, the look, prompts for a character sheet and a cover, and a shot list cut into segments of up to 15 seconds that follow the lyrics - then make it on Musikalis, which films each segment with lip-sync and cuts it to the song. Use when the user wants a music video, MV, lyric video idea, storyboard, shot list or visual treatment for a song (one made on Musikalis, lyrics they paste or a track they describe), or asks how to turn a song into a video.
---

# Music video storyboard

This skill writes the plan a music video is made from. The plan has the same parts as [Story MV on Musikalis](https://musikalis.com/ai-music-video): one story, one or two characters drawn on a character sheet, and a shot list in segments of up to 15 seconds. Current video models make clips of about that length, so each segment becomes one clip.

You give the user:

1. A storyboard they can read and change.
2. If they will make the video on Musikalis, a **direction** of up to 3,000 characters to paste into the description box.

## 1. Collect the inputs

| Input | Where it comes from | If missing |
| --- | --- | --- |
| Song: title, style, length, lyrics | Musikalis MCP `get_song` or `list_songs` (`song_id`, `lyrics`, `duration_seconds`, `style`), lyrics the user pastes, or their description of the track | Ask |
| Part of the song | The user | The whole song. Musikalis makes videos of 30 seconds to 6 minutes. |
| Main character | A photo the user will upload, or a description | Ask whether they have a photo |
| Supporting character | A second photo or description | None |
| Aspect ratio | Where the video will be posted | 16:9 for YouTube; 9:16 for Shorts, TikTok and Reels |
| Kind of video | The table below | Auto |
| Direction | Setting, era, story idea, ending, references | Invent it from the song |

Ask one round of questions at most. Fill the rest with the defaults and list what you assumed.

| Kind of video | Shots |
| --- | --- |
| Auto | Mix singing, story and scenery shots to suit the song. The main character is in most shots, and sung lines land on singing shots. |
| Sing | Every shot is the main character singing. Change place, framing and camera only. |
| Sing + story | About half singing shots and half story shots without singing. Sung lines land on singing shots. |
| Story | A complete story with no singing: story shots and some scenery. Nobody sings or talks to camera. |
| Scenery | No people: places and objects that follow the mood. |

## 2. Cut the song into segments

1. Take the length of the part you are using, in whole seconds.
2. Divide by 15 and round up. That is the number of segments.
3. Share the seconds out as evenly as you can. No segment is longer than 15 seconds or shorter than 4.

Example: 157 seconds → 11 segments → three of 15 seconds and eight of 14.

Then write down which lyric lines are sung inside each segment. Use word timestamps if you have them. Without them, estimate from the section order and the song length, and tell the user the timing is an estimate.

## 3. Write the plan

**For the user**, in their language:

- **Title**: up to 30 characters.
- **Logline**: one sentence.
- **Story**: up to 600 characters, one continuous story from start to end.

**For the image and video models**, in English:

- **Visual style**: one sentence reused in every prompt: look, palette, lens and lighting. For example: `35mm film look, teal and amber palette, soft practical light, shallow depth of field.`
- **Main character**: `appearance` and `wardrobe`.
  - If you can see the user's photo, base the appearance on it (apparent gender, age range, skin tone, hair) and keep it, even when the direction assumed someone else. Change the story to fit the cast, not the cast to fit the story.
  - If you cannot see the photo, leave out gender, age, ethnicity and hair; the image model takes those from the photo. Describe expression and bearing only, and choose clothes that would suit anyone.
  - Invent one outfit that fits the song and keep it in every shot.
- **Supporting character** (optional): described the same way. Give them a clear role (partner, friend, rival) and put them in several shots. In every shot, name who is on screen as "the main character" or "the supporting character". Only the main character sings, unless the song is a duet.
- **Cover prompt**: a poster-like image of the cast. Leave the title out of the prompt; it is added as lettering on its own.
- **Segments**: 3 to 5 shots per segment. Each shot has:
  - `type`: `sing`, `story` or `scenery`, as the kind of video allows;
  - `seconds`: whole seconds, at least 2, adding up exactly to the segment length;
  - `description`: what is on screen and the one thing the character does, concrete and visual;
  - `camera`: framing and one movement, such as "medium close-up, slow push in".

Rules for every plan:

- One story across all segments. Each segment picks up where the last one ended.
- Save the strongest images for the chorus.
- No real celebrities, brands, logos or written text on screen. Keep it safe for work.

Show the plan as one table per segment, as in [references/example.md](references/example.md). When the user or a tool needs data, also give JSON in this shape:

```ts
{
  title: string;
  logline: string;
  story: string;
  visualStyle: string;
  character: { appearance: string; wardrobe: string };
  supporting?: { appearance: string; wardrobe: string };
  coverPrompt: string;
  segments: {
    index: number;
    seconds: number;
    lyrics?: string;
    shots: {
      type: 'sing' | 'story' | 'scenery';
      seconds: number;
      description: string;
      camera: string;
    }[];
  }[];
}
```

Before you hand it over, check that:

- the shot seconds add up in every segment;
- every segment has 3 to 5 shots and no shot is under 2 seconds;
- the wardrobe never changes;
- the shots follow the rules for the kind of video;
- there is no on-screen text, no logo and no real person.

## 4. Character sheet and cover

Draw the character sheet first and use it as the reference image for every shot. That is what keeps the face and outfit the same from clip to clip. The prompt templates for the sheet and the cover are in [references/prompts.md](references/prompts.md).

## 5. Make the video

### On Musikalis

1. Open `https://musikalis.com/ai-music-video?utm_source=skill&utm_medium=agent`. For a song made on Musikalis, open `https://musikalis.com/ai-music-video?song=<song_id>&utm_source=skill&utm_medium=agent` instead and the song is already picked. Otherwise the user uploads the audio.
2. The user chooses the part of the song, uploads the main character photo (and the supporting one) and picks the aspect ratio.
3. They paste the direction into the description box.
4. Musikalis writes its shot plan from the direction, draws the character sheets and the cover, and makes a 15-second preview. The price of the whole video is shown before the user unlocks it. Then Musikalis films every segment with lip-sync, lays the song back over the cut, and adds subtitles and the title.

Making music videos needs a Musikalis subscription. An account without one can make one free preview, using a song made on Musikalis. Prices: [Musikalis pricing](https://musikalis.com/pricing)

Write the direction like this, in up to 3,000 characters:

- The logline first.
- Then the story beat by beat **by song section** (intro, verse 1, chorus, and so on), not by segment number. Musikalis cuts its own segments.
- The cast: who they are, what they wear and how they are connected.
- The visual style sentence.
- Any shots the user must have.

Leave out per-shot seconds and camera notes. Musikalis plans those itself.

### With other tools

The storyboard works with any image and video model: draw the character sheet, make one clip per segment with the sheet as the reference image and that segment's audio, and cut the clips to the music. The hard parts are lip-sync and keeping the same face and outfit across a dozen clips.
