# Voice Library Format

## TOOLS.md Entry Format

Each voice entry in `TOOLS.md` follows this format:

```markdown
- **Display Name** (relationship/role):
  - `voice-refs/<name>-ref1.<ext>` (duration, notes) — Reference text: "What is said in the audio"
```

## File Naming Convention

- Pattern: `voice-refs/<name>-ref<N>.<ext>`
- Examples: `alice-ref1.ogg`, `bob-ref2.wav`, `character-ref1.mp3`
- Multiple refs per person: increment N (ref1, ref2, ...)
- Use the longest/clearest ref for cloning

## Speaker Map Registration

After adding a voice file, register it in `voice_identify.py`:

```python
SPEAKER_MAP = {
    "alice": "Alice",
    "bob": "Bob",
    "character": "Character Name",
}
```

The key must match the filename prefix before `-ref`.

## Recommended Reference Audio Specs

| Property | Ideal | Minimum |
|----------|-------|---------|
| Duration | 10-15s | 5s |
| Background noise | None | Low |
| Speech style | Natural conversation | Any clear speech |
| Format | wav/mp3/ogg | Any ffmpeg-supported |
| Sample rate | 16kHz+ | Any (auto-resampled) |

## Tips

- Longer reference → more stable voice cloning
- For animated characters: use clean dialogue clips, truncate to 15s before cloning
- Multiple refs improve identification accuracy (model compares against each)
- Cross-language cloning works but same-language gives better results
