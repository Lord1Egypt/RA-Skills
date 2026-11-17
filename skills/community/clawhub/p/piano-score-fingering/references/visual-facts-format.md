# Visual Facts Input

create_visual_facts_template.py combines per-page proposed-regions.json files into a skeleton. The multimodal host fills it from the original score. create_plan_from_visual_facts.py is not OCR: it compiles reviewed facts into MIDI, keyboard geometry, stable IDs, and chord relationships, and records absolute PNG paths, dimensions, and SHA-256. Changed source pages invalidate the plan.

```json
{
  "source": {"type": "pdf", "path": "source.pdf", "coordinate_unit": "pixel_top_left", "render_dpi": 144},
  "pages": [{"page": 1, "width": 1180, "height": 1634, "image": "page-1.png"}],
  "recognition": {
    "scope": "page 1, measures 1-4",
    "measure_scope": [{"page": 1, "measure_start": 1, "measure_end": 4, "hands": ["RH", "LH"]}],
    "systems": [],
    "measure_regions": [],
    "measure_symbol_checks": [{
      "region_id": "p1-m001-rh", "page": 1, "measure": 1, "hand": "RH",
      "verified": true, "duration_verified": true,
      "source": "independent_visual_review",
      "evidence_crop": "score-crops/page-1/p1-m001-rh.png",
      "expected_noteheads": 6, "expected_rests": 1,
      "expected_attack_events": 5, "expected_chord_sizes": [1, 1, 2, 1, 1]
    }],
    "key_signatures": [{"page": 1, "measure_index": 1, "staff": 0, "fifths": -2, "mode": "major"}]
  },
  "notes": [{
    "page": 1, "measure_index": 1, "staff": 1, "voice": "1", "hand": "RH",
    "onset": 0, "duration": 1, "pitch_step": "G", "pitch_alter": 0, "pitch_octave": 4,
    "page_x": 186.5, "page_y": 314.0,
    "staff_geometry_id": "p1-system1-rh", "clef": "treble",
    "anchor_verified": true, "pitch_geometry_verified": true,
    "symbol_class": "notehead", "notehead_shape_verified": true,
    "origin": "direct_visual_notehead", "chord_member_verified": true,
    "recognition_passes": 2
  }],
  "rests": []
}
```

Supply observed spelling, effective alteration, octave, duration, hand, page, and head center. Store keys/key changes in recognition.key_signatures; staff=0 applies to all staves on that page. Do not manually supply computed pitch_midi, keyboard_x_cm, note_id, chord_id, chord_row, chord_size, key_signature_alter, or key_fifths.

The default anchor_method for verified visual heads is visual_notehead. Declare another method only for an appropriate reliable layout source.

Use separate crop directories per page. Set extract_score_regions.py --first-measure to that page's actual first measure. Complete notes/rests/keys/counts after template creation; drafts cannot go directly to formal generation.

source.render_dpi must equal the actual PNG rendering DPI. It controls physical font size, clearance, coordinate scaling, and drift thresholds. Record it through --render-dpi at creation rather than guessing later. Optional authorized OMR supplies candidate semantics only; counts and coordinates still need independent confirmation.

Each measure_region needs exactly one measure_symbol_check. Reopen the raw crop without consulting the filled notes list, then independently record noteheads, rests, attack events, and left-to-right chord sizes. [1,2,1] means three attacks with a middle dyad; the sum equals head count. Simultaneous notes in different voices on one staff are one physical attack.

The compiler enables coverage, independent passes, rest inventory, head-shape evidence, chord membership, and dense/sparse checks. Complete visual output cannot disable these via input JSON. Recompile older plans from retained visual facts when current gates are missing; do not manually insert a passed status.
