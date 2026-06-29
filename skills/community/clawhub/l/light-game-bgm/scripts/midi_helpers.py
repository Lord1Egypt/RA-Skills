#!/usr/bin/env python3
"""
Reusable building blocks for writing *expressive* MIDI with `mido`.

Import these from a per-song script so you don't re-derive the machinery
each time:

    from midi_helpers import (midi, NoteBuilder, realize, NB)

The point of this module is the expression layer — humanized timing,
CC11 dynamic swells, legato/held common tones, panning — which is what
makes sampled (soundfont) instruments stop sounding like the stiff,
stock General-MIDI cliché.  Requires: pip install mido
"""
import random
import math
from mido import Message, MetaMessage, MidiFile, MidiTrack, bpm2tempo

NB = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}


def midi(name):
    """'F#3' / 'Bb4' / 'C5'  ->  MIDI note number."""
    n = NB[name[0]]
    i = 1
    if len(name) > 1 and name[1] in '#b':
        n += 1 if name[1] == '#' else -1
        i = 2
    return 12 * (int(name[i:]) + 1) + n


def realize(pcs, base=60):
    """Pitch-class names -> ascending MIDI notes from `base` (good for arps)."""
    out, prev = [], base - 1
    for pc in pcs:
        v = NB[pc[0]] + (1 if len(pc) > 1 and pc[1] == '#' else 0)
        m = prev + 1
        while m % 12 != v:
            m += 1
        out.append(m)
        prev = m
    return out


class NoteBuilder:
    """
    Accumulates events for one MIDI channel, then bakes a MidiTrack with
    correct delta times.  Construct one per instrument/voice.

    pan/vib/rev are GM controllers applied once at the top:
      pan  = CC10 (0 left .. 64 center .. 127 right)
      vib  = CC1  modulation depth (a little vibrato wakes up strings)
      rev  = CC91 reverb send (set low if you do reverb in post)
    """

    def __init__(self, channel, program, tpb=480, pan=64, vib=0, rev=18, vol=100, seed=None):
        self.ch = channel
        self.tpb = tpb
        self.ev = []
        self.rng = random.Random(seed)
        self._head = [Message('program_change', channel=channel, program=program, time=0)]
        for cc, val in [(10, pan), (1, vib), (91, rev), (7, vol)]:
            self._head.append(Message('control_change', channel=channel, control=cc, value=val, time=0))

    def _hum(self, t, amt):
        return max(0, t + self.rng.randint(-amt, amt))

    def note(self, beat, name, dur_beats, vel=80, gate=0.95, hum=14, vvar=6):
        """Place one note at absolute `beat`. gate<1 shortens; >1 ties/legato."""
        m = name if isinstance(name, int) else midi(name)
        a = int(beat * self.tpb)
        b = a + int(dur_beats * self.tpb * gate)
        v = max(1, min(120, vel + self.rng.randint(-vvar, vvar)))
        self.ev.append((self._hum(a, hum), Message('note_on', channel=self.ch, note=m, velocity=v)))
        self.ev.append((b, Message('note_off', channel=self.ch, note=m, velocity=0)))

    def line(self, items, vel=80, gate=0.95, hum=14, vvar=6):
        """items: iterable of (beat, name, dur_beats)."""
        for beat, name, dur in items:
            self.note(beat, name, dur, vel, gate, hum, vvar)

    def swell(self, total_beats, base=70, amp=35, period_bars=8, beats_per_bar=4):
        """
        CC11 expression curve — the 'breathing' that kills block-chord
        stiffness.  Writes a smooth value every 1/4 beat.
        """
        step = self.tpb // 4
        t = 0
        total = int(total_beats * self.tpb)
        while t <= total:
            ph = (t / (self.tpb * beats_per_bar)) % period_bars / period_bars
            val = int(max(15, min(120, base + amp * math.sin(2 * math.pi * (ph - 0.25)))))
            self.ev.append((t, Message('control_change', channel=self.ch, control=11, value=val)))
            t += step

    def track(self):
        tr = MidiTrack()
        for m in self._head:
            tr.append(m)
        for at, msg in sorted(self.ev, key=lambda e: e[0]):
            prev = getattr(self, '_prev', 0)
            tr.append(msg.copy(time=max(0, at - prev)))
            self._prev = at
        return tr


def held_runs(voicing_per_bar, beats_per_bar=4):
    """
    Turn per-bar chord voicings into SUSTAINED notes: any pitch present in
    consecutive bars becomes one long held note (legato / held common
    tones) instead of being re-attacked every bar.  Returns a list of
    (start_beat, pitch, dur_beats) — the secret to un-stiff string pads.
    """
    nbars = len(voicing_per_bar)
    sets = [set(midi(n) if isinstance(n, str) else n for n in v) for v in voicing_per_bar]
    pitches = sorted({p for s in sets for p in s})
    out = []
    for p in pitches:
        b = 0
        while b < nbars:
            if p not in sets[b]:
                b += 1
                continue
            start = b
            while b < nbars and p in sets[b]:
                b += 1
            out.append((start * beats_per_bar, p, (b - start) * beats_per_bar))
    return out


def new_midi(bpm, tpb=480):
    """Return (MidiFile, append_track_fn) with tempo/time-sig meta set."""
    mid = MidiFile(ticks_per_beat=tpb)
    meta = MidiTrack()
    meta.append(MetaMessage('set_tempo', tempo=bpm2tempo(bpm), time=0))
    meta.append(MetaMessage('time_signature', numerator=4, denominator=4, time=0))
    mid.tracks.append(meta)
    return mid
