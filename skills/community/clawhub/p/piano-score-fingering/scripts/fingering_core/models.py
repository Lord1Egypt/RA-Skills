"""Typed data models used across the pianoplayer package."""

from __future__ import annotations

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class INote:
    """Internal note representation used by readers, optimizer, and output writers."""

    name: str | None = None
    isChord: bool = False
    isBlack: bool = False
    pitch: int | float = 0
    octave: int = 0
    x: float = 0.0
    time: float = 0.0
    duration: float = 0.0
    fingering: int | str = 0
    is_anchor: bool = False
    measure: int = 0
    staff: int = 0
    chordnr: int = 0
    NinChord: int = 0
    chordID: int = 0
    noteID: int = 0
    cost: float = 0.0
    note21: Any = None
    chord21: Any = None


_kb_layout = {
    "C": 0.5,
    "D": 1.5,
    "E": 2.5,
    "F": 3.5,
    "G": 4.5,
    "A": 5.5,
    "B": 6.5,
    "B#": 0.5,
    "C#": 1.0,
    "D#": 2.0,
    "E#": 3.5,
    "F#": 4.0,
    "G#": 5.0,
    "A#": 6.0,
    "C-": 6.5,
    "D-": 1.0,
    "E-": 2.0,
    "F-": 2.5,
    "G-": 4.0,
    "A-": 5.0,
    "B-": 6.0,
    "C##": 1.5,
    "D##": 2.5,
    "F##": 4.5,
    "G##": 5.5,
    "A##": 6.5,
    "D--": 0.5,
    "E--": 1.5,
    "G--": 3.5,
    "A--": 4.5,
    "B--": 5.5,
}


def keypos_midi(n):  # position of notes on keyboard
    """Return horizontal key position from MIDI pitch (in cm)."""
    keybsize = 16.5  # cm
    k = keybsize / 7.0  # 7 notes
    # Key centres within one octave, expressed in white-key-width units.
    # MIDI octave 0 begins at C-1, hence the ``- 1`` below.
    centres = (0.5, 1.0, 1.5, 2.0, 2.5, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5)
    pitch = int(n.pitch)
    octave = (pitch // 12) - 1
    return keybsize * octave + centres[pitch % 12] * k


def keypos(n):  # position of notes on keyboard
    """Return horizontal key position from note name/octave (in cm)."""
    name = str(n.name or "")
    if not name or name[0] not in "CDEFGAB":
        logger.warning("Note not found in keyboard layout: %s", n.name)
        return 0.0
    base_pc = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}[name[0]]
    accidental = name[1:].count("#") - name[1:].count("-")
    midi = (int(n.octave) + 1) * 12 + base_pc + accidental
    return keypos_midi(INote(pitch=midi))
