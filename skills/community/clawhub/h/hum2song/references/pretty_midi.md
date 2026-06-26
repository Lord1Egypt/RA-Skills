# Pretty MIDI Reference

Pretty MIDI is a Python library for reading, editing, and writing MIDI files. In Hum2Song it is the main utility for cleaning extracted melody data and exporting MIDI for synthesis or DAW editing.

## What It Is Used For

- load extracted MIDI from Basic Pitch
- quantize note timing
- edit note ranges or durations
- build instrument tracks
- export cleaned MIDI for synthesis or arrangement

## Install

```bash
pip install pretty_midi
```

## Minimal Examples

### Create MIDI

```python
import pretty_midi

pm = pretty_midi.PrettyMIDI()
instrument = pretty_midi.Instrument(program=0)
note = pretty_midi.Note(
    velocity=100,
    pitch=60,
    start=0.0,
    end=0.5
)
instrument.notes.append(note)
pm.instruments.append(instrument)
pm.write("output.mid")
```

### Read MIDI

```python
import pretty_midi

pm = pretty_midi.PrettyMIDI("input.mid")
print(pm.get_end_time())
print(pm.estimate_tempo())

for instrument in pm.instruments:
    for note in instrument.notes:
        print(note.pitch, note.start, note.end)
```

## References

- GitHub: https://github.com/craffel/pretty-midi
- Docs: https://craffel.github.io/pretty-midi/
