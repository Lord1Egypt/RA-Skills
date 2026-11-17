# Multi-shot video: worked recipes

Three end-to-end recipes covering the two template dialects. Recipe 1 is a HappyHorse directorial-beats reel (`Begin with / Cut to / End on`). Recipe 2 is a Kling Turbo numbered `shot N, seconds, description;` reel with per-shot seconds summing to `duration`. Recipe 3 is a PixVerse anchor-frame multi-clip bracketed by two stills.

Confirm the AIR is `live` and the field names against the live schema before sending. Run async: the request returns a `taskUUID`, then poll `getResponse` until terminal. The finished reel is at `videoURL`.

All AIRs below are verified against the Runware catalog: `alibaba:happyhorse@1.1` (HappyHorse 1.1), `klingai:kling-video@3.0-turbo` (Kling 3.0 Turbo), `pixverse:1@8` (PixVerse V6, slug `pixverse-v6`).

## 1. Directorial-beats reel (HappyHorse 1.1)

Scenario: a craft brand wants a 14-second hero reel of a master swordsmith forging a katana, cutting between the forge wide, the hands on the blade, the anvil, and the quench. The brief reads like a script, so route to HappyHorse and write it as natural-language storyboard beats.

Establish the subject once at the top. Lead each beat with its directorial cue and a shot-direction phrase. Close with a preservation clause naming what holds across the cuts. Text-to-video mode, so set the aspect through `width`/`height` from the allowed list (here `1920 x 1080`).

```json
[
  {
    "taskType": "videoInference",
    "taskUUID": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "model": "alibaba:happyhorse@1.1",
    "positivePrompt": "A master Japanese swordsmith forging a katana in his firelit forge, the same person across every shot, with a soot-streaked indigo work coat and a grey cloth tied around his forehead. Begin with a wide establishing shot of him at the forge, the firebed glowing orange behind him. Cut to a close shot of his hands lifting a glowing red-hot blade from the coals with iron tongs. Shift to a medium shot at the anvil as he hammers the blade, orange sparks scattering with each strike. Then a slow push-in on his focused weathered face lit by the forge. Cut to a dramatic close-up of the blade plunged into a water trough, dense white steam billowing up. End on a wide static shot of the finished katana laid on a folded indigo cloth. Preserve his soot-streaked indigo work coat, the grey forehead cloth, his weathered hands, and the warm firelit colour grade across every shot.",
    "width": 1920,
    "height": 1080,
    "duration": 14
  }
]
```

Result:

```json
{
  "data": [
    {
      "taskType": "videoInference",
      "taskUUID": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "videoUUID": "9c1b2d3a-4e5f-6789-abcd-ef0123456789",
      "videoURL": "https://vm.runware.ai/video/os/a14d18/ws/2/vi/9c1b2d3a-4e5f-6789-abcd-ef0123456789.mp4"
    }
  ]
}
```

Why it works: six directorial cues mark six hard cuts. The opening line gives the model one identity to hold, and the closing preservation clause keeps the coat, the forehead cloth, and the grade from drifting by the later beats. Each beat leads with its shot-direction phrase (wide establishing, close, medium, push-in, dramatic close-up, wide static), so the model reads them as camera instructions. No per-shot timing field here, HappyHorse paces the cuts itself across the 14 seconds. Match duration to shot count: six beats want close to the 15-second cap.

## 2. Numbered shot-list reel (Kling 3.0 Turbo)

Scenario: a motorsport client wants a 15-second pit-to-podium reel with six tight cuts and full control over how long each one runs. Route to Kling Turbo and budget the seconds per shot first, since the per-shot seconds **must sum to `duration` exactly** or the request is rejected.

Budget: `3 + 2 + 2 + 3 + 3 + 2 = 15`. Each shot is read independently, so repeat the identifying details (dark blue overalls, white fireproof suit, the black race car) in every shot that needs them. Text-to-video mode, so set `width`/`height` from the allowed list.

```json
[
  {
    "taskType": "videoInference",
    "taskUUID": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
    "model": "klingai:kling-video@3.0-turbo",
    "positivePrompt": "shot 1, 3, A team of race mechanics in dark blue overalls rolling fresh slick tyres across the polished pit lane garage floor at dawn; shot 2, 2, A racing driver in a white fireproof suit pulling on a black full-face helmet outside the garage; shot 3, 2, A close shot of a gloved hand operating a pit board, flipping the number panel to signal the driver; shot 4, 3, A black race car launching from the starting grid in a cloud of tyre smoke; shot 5, 3, The same black race car carving through a high-speed banking corner, low afternoon sun behind it; shot 6, 2, A marshal waving a black-and-white checkered flag as the lead black race car crosses the finish line;",
    "width": 1920,
    "height": 1080,
    "duration": 15
  }
]
```

Result:

```json
{
  "data": [
    {
      "taskType": "videoInference",
      "taskUUID": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
      "videoUUID": "1a2b3c4d-5e6f-7890-abcd-ef0987654321",
      "videoURL": "https://vm.runware.ai/video/os/a14d18/ws/2/vi/1a2b3c4d-5e6f-7890-abcd-ef0987654321.mp4"
    }
  ]
}
```

Why it works: each `shot N, seconds, description;` entry is one cut, and the six seconds values sum to the 15-second `duration`, so the request validates. The template carries no hidden continuity, so the black race car is named in shots 4, 5, and 6 to read as the same car across the cuts. Front-loading the short two-second shots with the action already in motion keeps them from feeling like setups with no payoff. To lock the opening frame instead of describing it, pass one anchor still in `inputs.frameImages` pinned to the first frame, which drops the prompt cap to 2500 characters and switches the request to image-to-video mode.

## 3. Anchor-frame multi-clip (PixVerse V6)

Scenario: a vineyard wants a 10-second reel of a single harvest day that opens on a misty sunrise still and closes on a hero shot of a glass of wine, both supplied as exact stills. The opening and closing look must match the supplied frames, and the model invents the cuts between them. Route to PixVerse, pass both stills as anchors, and flip `settings.multiClip` on.

Pin each still with its position (`frame: "first"` / `"last"`). Write the prompt as four beats (`Start with / Cut to / Shift to / End on`) and reference the anchors directly in the bracketing beats. In anchor mode the aspect comes from the stills, so set `resolution` rather than `width`/`height`. With two anchors, `settings.thinking` must be `"enabled"` or `"disabled"` (not `"auto"`).

```json
[
  {
    "taskType": "videoInference",
    "taskUUID": "c3d4e5f6-a7b8-9012-cdef-123456789012",
    "model": "pixverse:1@8",
    "positivePrompt": "A cinematic multi-shot sequence following a single harvest day at a Mediterranean hillside vineyard. Start with the misty sunrise establishing shot from the first frame, low fog hanging between the rows of grapevines. Cut to a lower tracking angle of weathered hands clipping ripe grape clusters into the woven wicker basket. Shift to a mid shot of the full basket being lifted from the rows toward the warm light. End on the closing scene from the second frame image: the tall stemmed glass of deep ruby wine on the weathered wooden table at golden hour. Preserve the same warm color grade, the woven wicker basket, and the soft sunlit atmosphere across every shot.",
    "inputs": {
      "frameImages": [
        { "image": "https://example.com/vineyard-sunrise.jpg", "frame": "first" },
        { "image": "https://example.com/wine-glass-golden-hour.jpg", "frame": "last" }
      ]
    },
    "duration": 10,
    "resolution": "1080p",
    "settings": {
      "multiClip": true,
      "audio": true,
      "thinking": "enabled"
    }
  }
]
```

Result:

```json
{
  "data": [
    {
      "taskType": "videoInference",
      "taskUUID": "c3d4e5f6-a7b8-9012-cdef-123456789012",
      "videoUUID": "2b3c4d5e-6f70-8901-bcde-f10987654321",
      "videoURL": "https://vm.runware.ai/video/os/a14d18/ws/2/vi/2b3c4d5e-6f70-8901-bcde-f10987654321.mp4"
    }
  ]
}
```

Why it works: `multiClip: true` plus the four-beat prompt is what produces cuts. A caption-style mood prompt with the flag on still renders a single take. The two anchors bracket the reel, so the open matches the sunrise still and the close matches the wine still without the model redrawing them, and the middle two shots are invented from the beats. The preservation clause holds the color grade and the basket across the cuts. `audio: true` carries one synced ambient bed across the cuts and earns its surcharge on an atmospheric reel like this. To drop to a single supplied anchor, pass one `frameImages` entry pinned `first`, keep `multiClip: true`, and `thinking` can return to `"auto"`.
