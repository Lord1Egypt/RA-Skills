#!/usr/bin/env python3
"""Regression checks for MusicXML facts that affect PDF/image placement.

The fixture deliberately uses a left-hand staff printed in treble clef and a
leading rest.  Both are common in elementary arrangements.  If either fact is
lost, visual anchoring can drift vertically or horizontally even when the
fingering solver itself is correct.
"""

from __future__ import annotations

import json
import struct
import subprocess
import sys
import tempfile
from unittest.mock import patch
import zlib
from zipfile import ZIP_DEFLATED, ZipFile
from pathlib import Path

from validate_recognition import validate_recognition
from run_fingering_pipeline import preserve_source_score
from run_optional_omr import audiveris_command, bounded_geometry_payload
from extract_audiveris_anchor_candidates import candidate_note_count, musicxml_measure_note_counts


FIXTURE = """<?xml version="1.0" encoding="UTF-8"?>
<score-partwise version="3.1">
  <part-list><score-part id="P1"><part-name>Piano</part-name></score-part></part-list>
  <part id="P1"><measure number="1">
    <attributes><divisions>1</divisions><time><beats>3</beats><beat-type>4</beat-type></time>
      <staves>2</staves><clef number="1"><sign>G</sign><line>2</line></clef>
      <clef number="2"><sign>G</sign><line>2</line></clef></attributes>
    <note><pitch><step>C</step><octave>5</octave></pitch><duration>3</duration><type>half</type><dot/><staff>1</staff></note>
    <backup><duration>3</duration></backup>
    <note><rest/><duration>1</duration><type>quarter</type><staff>2</staff></note>
    <note><pitch><step>G</step><octave>4</octave></pitch><duration>2</duration><type>half</type><staff>2</staff></note>
    <note><chord/><pitch><step>B</step><octave>4</octave></pitch><duration>2</duration><type>half</type><staff>2</staff></note>
  </measure><measure number="2">
    <note><rest/><duration>1</duration><type>16th</type><staff>1</staff></note>
    <note><pitch><step>C</step><octave>5</octave></pitch><duration>1</duration><type>16th</type><staff>1</staff></note>
    <note><pitch><step>E</step><octave>5</octave></pitch><duration>1</duration><type>16th</type><staff>1</staff></note>
    <note><pitch><step>G</step><octave>5</octave></pitch><duration>1</duration><type>16th</type><staff>1</staff></note>
    <note><pitch><step>C</step><octave>6</octave></pitch><duration>4</duration><type>quarter</type><staff>1</staff></note>
    <backup><duration>8</duration></backup><note><rest/><duration>8</duration><type>half</type><staff>2</staff></note>
  </measure></part>
</score-partwise>
"""

# A common real-world export: two vocal lines plus a piano grand staff.  The
# piano importer must select P3, rather than treating the first Voice part as
# the right hand and all remaining parts as the left hand.
VOICE_AND_PIANO_FIXTURE = """<?xml version="1.0" encoding="UTF-8"?>
<score-partwise version="3.1"><part-list>
 <score-part id="P1"><part-name>Voice</part-name><score-instrument id="P1-I1"><instrument-name>Voice Oohs</instrument-name></score-instrument></score-part>
 <score-part id="P2"><part-name>Voice</part-name></score-part>
 <score-part id="P3"><part-name>Piano</part-name><score-instrument id="P3-I1"><instrument-name>Acoustic Grand Piano</instrument-name></score-instrument></score-part>
</part-list>
<part id="P1"><measure number="1"><attributes><divisions>1</divisions></attributes><note><pitch><step>C</step><octave>5</octave></pitch><duration>1</duration></note></measure></part>
<part id="P2"><measure number="1"><attributes><divisions>1</divisions></attributes><note><pitch><step>E</step><octave>5</octave></pitch><duration>1</duration></note></measure></part>
<part id="P3"><measure number="1"><attributes><divisions>1</divisions><staves>2</staves><clef number="1"><sign>G</sign><line>2</line></clef><clef number="2"><sign>F</sign><line>4</line></clef></attributes>
<note><pitch><step>G</step><octave>4</octave></pitch><duration>1</duration><staff>1</staff></note><backup><duration>1</duration></backup><note><pitch><step>C</step><octave>3</octave></pitch><duration>1</duration><staff>2</staff></note>
</measure></part></score-partwise>"""

# Some exports encode right and left hands as two anonymous one-staff parts.
# This must only be imported when both sides are explicitly routed.
SPLIT_HAND_FIXTURE = """<?xml version="1.0" encoding="UTF-8"?>
<score-partwise version="3.1"><part-list><score-part id="P1"><part-name>Part 1</part-name></score-part><score-part id="P2"><part-name>Part 2</part-name></score-part></part-list>
<part id="P1"><measure number="1"><attributes><divisions>1</divisions></attributes><note><pitch><step>C</step><octave>5</octave></pitch><duration>1</duration></note></measure></part>
<part id="P2"><measure number="1"><attributes><divisions>1</divisions></attributes><note><pitch><step>C</step><octave>3</octave></pitch><duration>1</duration></note></measure></part>
</score-partwise>"""

# A tied triad may receive an additional lower note at the continuation.  The
# first chord must reserve the later slots; otherwise the tie repair and the
# unique-finger chord requirement contradict one another.
TIED_CHORD_FIXTURE = """<?xml version="1.0" encoding="UTF-8"?>
<score-partwise version="3.1"><part-list><score-part id="P1"><part-name>Piano</part-name></score-part></part-list><part id="P1"><measure number="1"><attributes><divisions>1</divisions></attributes>
<note><pitch><step>D</step><octave>5</octave></pitch><duration>2</duration><tie type="start"/></note><note><chord/><pitch><step>G</step><octave>5</octave></pitch><duration>2</duration><tie type="start"/></note><note><chord/><pitch><step>B</step><alter>-1</alter><octave>5</octave></pitch><duration>2</duration><tie type="start"/></note>
<backup><duration>1</duration></backup><note><pitch><step>G</step><octave>4</octave></pitch><duration>1</duration></note><note><chord/><pitch><step>D</step><octave>5</octave></pitch><duration>1</duration><tie type="stop"/></note><note><chord/><pitch><step>G</step><octave>5</octave></pitch><duration>1</duration><tie type="stop"/></note><note><chord/><pitch><step>B</step><alter>-1</alter><octave>5</octave></pitch><duration>1</duration><tie type="stop"/></note>
</measure></part></score-partwise>"""

VISUAL_FACTS = {
    "source": {"type": "image", "path": "fixture.png", "coordinate_unit": "pixel_top_left"},
    "pages": [{"page": 1, "width": 300, "height": 300, "image": "fixture.png"}],
    "recognition": {
        "scope": "one reviewed visual measure",
        "key_signatures": [{"page": 1, "measure_index": 1, "staff": 0, "fifths": 0}],
        "measure_scope": [{"page": 1, "measure_start": 1, "measure_end": 1, "hands": ["RH", "LH"]}],
        "systems": [
            {"system_id": "p1-rh", "page": 1, "staff": 1, "clef": "treble", "staff_line_y": [100, 110, 120, 130, 140]},
            {"system_id": "p1-lh", "page": 1, "staff": 2, "clef": "bass", "staff_line_y": [200, 210, 220, 230, 240]},
        ],
        "measure_regions": [
            {"region_id": "p1-m001-rh", "page": 1, "measure": 1, "hand": "RH", "bbox": [0, 80, 200, 170], "evidence_crop": "rh.png"},
            {"region_id": "p1-m001-lh", "page": 1, "measure": 1, "hand": "LH", "bbox": [0, 180, 200, 260], "evidence_crop": "lh.png"},
        ],
        "measure_symbol_checks": [
            {"region_id": "p1-m001-rh", "page": 1, "measure": 1, "hand": "RH", "expected_noteheads": 1, "expected_rests": 0, "expected_attack_events": 1, "expected_chord_sizes": [1], "duration_verified": True, "source": "independent_visual_review", "evidence_crop": "rh.png", "verified": True},
            {"region_id": "p1-m001-lh", "page": 1, "measure": 1, "hand": "LH", "expected_noteheads": 0, "expected_rests": 1, "expected_attack_events": 0, "expected_chord_sizes": [], "duration_verified": True, "source": "independent_visual_review", "evidence_crop": "lh.png", "verified": True},
        ],
        "verification": {gate: True for gate in ("scope_complete", "staff_geometry", "pitch_geometry", "key_signature", "accidentals", "rhythm", "ties", "chords", "anchors", "pitch_spelling")},
    },
    "notes": [{
        "page": 1, "measure_index": 1, "staff": 1, "voice": "1", "hand": "RH", "onset": 0, "duration": 1,
        "pitch_step": "G", "pitch_alter": 0, "pitch_octave": 4, "page_x": 100, "page_y": 130,
        "staff_geometry_id": "p1-rh", "anchor_verified": True, "pitch_geometry_verified": True,
        "symbol_class": "notehead", "notehead_shape_verified": True, "origin": "direct_visual_notehead",
        "chord_member_verified": True, "recognition_passes": 2, "sparse_symbol_verified": True,
    }],
    "rests": [{
        "page": 1, "measure_index": 1, "hand": "LH", "page_x": 100, "page_y": 220,
        "rest_type": "whole", "duration": 1, "rest_shape_verified": True,
        "symbol_class": "rest",
    }],
}


def write_white_png(path: Path, width: int, height: int) -> None:
    """Create a tiny dependency-free RGB fixture with exact declared dimensions."""
    raw = b"".join(b"\x00" + b"\xff\xff\xff" * width for _ in range(height))
    def chunk(kind: bytes, payload: bytes) -> bytes:
        return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", zlib.crc32(kind + payload) & 0xffffffff)
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b"")
    )


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    with tempfile.TemporaryDirectory(prefix="piano-recognition-regression-") as raw_dir:
        work = Path(raw_dir)
        source, result, fingered, structured_delivery_dir = work / "fixture.musicxml", work / "plan.json", work / "fingered.json", work / "structured-delivery"
        voice_source, voice_plan = work / "voice-and-piano.musicxml", work / "voice-and-piano-plan.json"
        split_source, split_plan = work / "split-hands.musicxml", work / "split-hands-plan.json"
        tied_source, tied_plan, tied_fingered = work / "tied-chord.musicxml", work / "tied-chord-plan.json", work / "tied-chord-fingered.json"
        mxl_source, mxl_plan, mxl_delivery_dir = work / "fixture.mxl", work / "mxl-plan.json", work / "mxl-delivery"
        musescore_input, fake_renderer, converted_score, conversion_receipt = (
            work / "fixture.mscz", work / "fake-musescore", work / "converted.musicxml", work / "conversion-receipt.json",
        )
        source.write_text(FIXTURE, encoding="utf-8")
        voice_source.write_text(VOICE_AND_PIANO_FIXTURE, encoding="utf-8")
        split_source.write_text(SPLIT_HAND_FIXTURE, encoding="utf-8")
        tied_source.write_text(TIED_CHORD_FIXTURE, encoding="utf-8")
        musescore_input.write_bytes(b"fixture MuseScore content")
        fake_renderer.write_text(
            "#!/usr/bin/env python3\n"
            "import shutil, sys\n"
            "from pathlib import Path\n"
            "target = Path(sys.argv[sys.argv.index('-o') + 1])\n"
            "shutil.copyfile(Path(__file__).with_name('fixture.musicxml'), target)\n",
            encoding="utf-8",
        )
        fake_renderer.chmod(0o755)
        with ZipFile(mxl_source, "w", compression=ZIP_DEFLATED) as archive:
            archive.writestr(
                "META-INF/container.xml",
                """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<container version=\"1.0\"><rootfiles><rootfile full-path=\"score.xml\"/></rootfiles></container>""",
            )
            archive.writestr("score.xml", FIXTURE)
        subprocess.run(
            [sys.executable, str(script_dir / "create_plan_from_musicxml.py"), str(source), "-o", str(result)],
            check=True,
            capture_output=True,
            text=True,
        )
        plan = json.loads(result.read_text(encoding="utf-8"))
        subprocess.run(
            [sys.executable, str(script_dir / "create_plan_from_musicxml.py"), str(voice_source), "-o", str(voice_plan)],
            check=True, capture_output=True, text=True,
        )
        voice_plan_payload = json.loads(voice_plan.read_text(encoding="utf-8"))
        subprocess.run(
            [sys.executable, str(script_dir / "create_plan_from_musicxml.py"), str(split_source),
             "--rh-part-id", "P1", "--lh-part-id", "P2", "-o", str(split_plan)],
            check=True, capture_output=True, text=True,
        )
        split_plan_payload = json.loads(split_plan.read_text(encoding="utf-8"))
        subprocess.run(
            [sys.executable, str(script_dir / "create_plan_from_musicxml.py"), str(tied_source), "-o", str(tied_plan)],
            check=True, capture_output=True, text=True,
        )
        tied_generation = subprocess.run(
            [sys.executable, str(script_dir / "generate_fingering_plan.py"), str(tied_plan),
             "-o", str(tied_fingered), "--ignore-existing", "--quiet"],
            capture_output=True, text=True,
        )
        tied_validation = subprocess.run(
            [sys.executable, str(script_dir / "validate_fingering_plan.py"), str(tied_fingered)],
            capture_output=True, text=True,
        )
        tied_plan_payload = json.loads(tied_fingered.read_text(encoding="utf-8"))
        voice_candidate_count = candidate_note_count(voice_source)
        voice_candidate_counts = musicxml_measure_note_counts(voice_source)
        subprocess.run(
            [
                sys.executable, str(script_dir / "generate_fingering_plan.py"),
                str(result), "-o", str(fingered), "--ignore-existing",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        fingered_plan = json.loads(fingered.read_text(encoding="utf-8"))
        structured_delivery = subprocess.run(
            [
                sys.executable, str(script_dir / "run_fingering_pipeline.py"), str(result),
                "--out-dir", str(structured_delivery_dir), "--stage-timeout", "10", "--run-timeout", "30",
            ],
            capture_output=True, text=True,
        )
        structured_manifest = json.loads((structured_delivery_dir / "run-manifest.json").read_text(encoding="utf-8"))
        write_musicxml_stage = next(
            (stage for stage in structured_manifest["stages"] if stage.get("name") == "write_musicxml"),
            {},
        )
        hand_size_stage = next(
            (stage for stage in structured_manifest["stages"] if stage.get("name") == "hand_size_stability"),
            {},
        )
        hand_size_audit_ok = (
            hand_size_stage.get("status") in {"passed", "failed", "timed_out", "skipped"}
            and (
                hand_size_stage.get("status") in {"timed_out", "skipped"}
                or (
                    (structured_delivery_dir / "hand-size-stability.json").is_file()
                    and "Hand-size sensitivity" in (structured_delivery_dir / "result-report.md").read_text(encoding="utf-8")
                )
            )
        )
        subprocess.run(
            [sys.executable, str(script_dir / "create_plan_from_musicxml.py"), str(mxl_source), "-o", str(mxl_plan)],
            check=True, capture_output=True, text=True,
        )
        mxl_delivery = subprocess.run(
            [
                sys.executable, str(script_dir / "run_fingering_pipeline.py"), str(mxl_plan),
                "--out-dir", str(mxl_delivery_dir), "--stage-timeout", "10", "--run-timeout", "30",
            ],
            capture_output=True, text=True,
        )
        mxl_manifest = json.loads((mxl_delivery_dir / "run-manifest.json").read_text(encoding="utf-8"))
        mxl_write_stage = next(
            (stage for stage in mxl_manifest["stages"] if stage.get("name") == "write_musicxml"),
            {},
        )
        musescore_conversion = subprocess.run(
            [
                sys.executable, str(script_dir / "convert_musescore_score.py"), str(musescore_input),
                "-o", str(converted_score), "--renderer", str(fake_renderer), "--report", str(conversion_receipt),
            ],
            check=True, capture_output=True, text=True,
        )
        conversion = json.loads(conversion_receipt.read_text(encoding="utf-8"))
        # An MXL emitted by the local OMR wrapper sits beside an explicit
        # candidate receipt.  It must not inherit the trust level of a
        # user-provided MusicXML merely because its XML syntax parses.
        omr_dir = work / "omr-candidate"
        omr_dir.mkdir()
        omr_source, omr_plan_path, provisional_omr_plan_path = (
            omr_dir / "fixture.musicxml", omr_dir / "candidate-plan.json", omr_dir / "provisional-fingered.json",
        )
        omr_source.write_text(FIXTURE, encoding="utf-8")
        (omr_dir / "omr-candidate-report.json").write_text(json.dumps({
            "status": "candidate_ready", "candidate": "audiveris",
            "musicxml_candidates": [str(omr_source.resolve())],
            "semantic_risk_signals": [{"code": "rhythm_unresolved"}],
        }), encoding="utf-8")
        subprocess.run(
            [sys.executable, str(script_dir / "create_plan_from_musicxml.py"), str(omr_source), "-o", str(omr_plan_path)],
            check=True, capture_output=True, text=True,
        )
        omr_plan = json.loads(omr_plan_path.read_text(encoding="utf-8"))
        omr_errors, _ = validate_recognition(omr_plan, strict=True)
        provisional_omr = subprocess.run(
            [
                sys.executable, str(script_dir / "generate_fingering_plan.py"), str(omr_plan_path),
                "--provisional-omr", "-o", str(provisional_omr_plan_path), "--quiet",
            ],
            capture_output=True, text=True,
        )
        provisional_omr_plan = json.loads(provisional_omr_plan_path.read_text(encoding="utf-8"))
        visual_facts, visual_draft, visual_locked, visual_fingered, visual_fingered_small, blocked_delivery_dir, semantic_ledger, scoped_semantic_ledger, omr_report = (
            work / "visual-facts.json",
            work / "visual-draft.json",
            work / "visual-locked.json",
            work / "visual-fingered.json",
            work / "visual-fingered-small.json",
            work / "blocked-delivery",
            work / "semantic-ledger.json",
            work / "semantic-ledger-scoped.json",
            work / "omr-candidate-report.json",
        )
        write_white_png(work / "fixture.png", 300, 300)
        visual_facts.write_text(json.dumps(VISUAL_FACTS), encoding="utf-8")
        subprocess.run(
            [sys.executable, str(script_dir / "create_plan_from_visual_facts.py"), str(visual_facts), "-o", str(visual_draft)],
            check=True, capture_output=True, text=True,
        )
        # A draft visual plan is deliberately not eligible for generation.
        # Even so, the coordinator must leave a person with the current plan,
        # a viewable source copy and a readable report rather than a lone
        # non-zero return code.
        blocked_delivery = subprocess.run(
            [
                sys.executable, str(script_dir / "run_fingering_pipeline.py"), str(visual_draft),
                "--out-dir", str(blocked_delivery_dir), "--stage-timeout", "10", "--run-timeout", "30",
            ],
            capture_output=True, text=True,
        )
        blocked_manifest = json.loads((blocked_delivery_dir / "run-manifest.json").read_text(encoding="utf-8"))
        blocked_report = (blocked_delivery_dir / "result-report.md").read_text(encoding="utf-8")
        subprocess.run(
            [sys.executable, str(script_dir / "manage_recognition.py"), "freeze", str(visual_draft), "-o", str(visual_locked)],
            check=True, capture_output=True, text=True,
        )
        subprocess.run(
            [sys.executable, str(script_dir / "generate_fingering_plan.py"), str(visual_locked), "-o", str(visual_fingered)],
            check=True, capture_output=True, text=True,
        )
        subprocess.run(
            [
                sys.executable, str(script_dir / "generate_fingering_plan.py"), str(visual_locked),
                "-o", str(visual_fingered_small), "--hand-size", "S",
            ],
            check=True, capture_output=True, text=True,
        )
        visual_plan = json.loads(visual_locked.read_text(encoding="utf-8"))
        visual_small_plan = json.loads(visual_fingered_small.read_text(encoding="utf-8"))
        # No visual output is allowed to look finished when even one label
        # lacks a verified source notehead.  The caller still receives the
        # fingered MusicXML/plan and review report, but not a drifting PDF.
        unanchored_render = work / "unanchored-render.json"
        unanchored_payload = json.loads(visual_fingered.read_text(encoding="utf-8"))
        unanchored_payload["notes"][0]["anchor_verified"] = False
        unanchored_render.write_text(json.dumps(unanchored_payload), encoding="utf-8")
        render_blocked = subprocess.run(
            [sys.executable, str(script_dir / "render_fingering_pdf.py"), str(unanchored_render),
             "-o", str(work / "unanchored-output.pdf")],
            capture_output=True, text=True,
        )
        visual_pdf_requires_verified_anchors = (
            render_blocked.returncode != 0
            and "requires verified source anchors" in render_blocked.stderr
            and not (work / "unanchored-output.pdf").exists()
        )
        original_source_bytes = (work / "fixture.png").read_bytes()
        source_copy_plan = work / "source-copy-plan.json"
        source_copy_plan.write_text(json.dumps({"source": {"type": "image", "path": str(work / "fixture.png")}}), encoding="utf-8")
        preserved_source = preserve_source_score(source_copy_plan, work)
        source_copy_ok = (
            preserved_source is not None
            and preserved_source.is_file()
            and preserved_source.read_bytes() == original_source_bytes
        )
        subprocess.run(
            [
                sys.executable, str(script_dir / "create_semantic_review_ledger.py"),
                str(source), str(visual_facts), "-o", str(semantic_ledger),
            ],
            check=True, capture_output=True, text=True,
        )
        ledger = json.loads(semantic_ledger.read_text(encoding="utf-8"))
        omr_report.write_text(json.dumps({
            "input": str(work / "source-page-001.png"),
            "semantic_risk_signals": [
                {"code": "anchor_count_mismatch", "count": 1, "examples": ["page 1 measure 1 RH: OMR 3 head(s) vs MXL 2 note(s)"]},
                {"code": "unlinked_symbol", "count": 1, "examples": ["No chord linked to OctaveShiftInter"]},
            ],
        }), encoding="utf-8")
        subprocess.run(
            [
                sys.executable, str(script_dir / "create_semantic_review_ledger.py"),
                str(source), str(visual_facts), "--omr-report", str(omr_report), "-o", str(scoped_semantic_ledger),
            ],
            check=True, capture_output=True, text=True,
        )
        scoped_ledger = json.loads(scoped_semantic_ledger.read_text(encoding="utf-8"))
        # A plan's coordinates are valid only for the exact rendered page it
        # was read from.  Replacing that image must block reuse rather than
        # letting every later label drift together.
        write_white_png(work / "fixture.png", 301, 300)
        stale_asset_errors, _ = validate_recognition(visual_plan, strict=True)
        # The archive traversal has its own cap.  A late geometry diagnostic
        # must never suppress the normal OMR receipt/report after the engine
        # has already exported files.
        with patch("run_optional_omr.subprocess.run", side_effect=subprocess.TimeoutExpired(["geometry"], 1)):
            geometry_timeout = bounded_geometry_payload(work / "missing.omr", work / "missing.mxl", timeout=1)
        # The macOS app bundle must remain genuinely headless.  Without this
        # flag the embedded Java runtime can try to register a GUI application
        # and abort before any score is processed.
        fake_contents = work / "Audiveris.app" / "Contents"
        fake_java = fake_contents / "runtime" / "Contents" / "Home" / "bin" / "java"
        fake_jar = fake_contents / "app" / "audiveris.jar"
        fake_launcher = fake_contents / "MacOS" / "Audiveris"
        for file in (fake_java, fake_jar, fake_launcher):
            file.parent.mkdir(parents=True, exist_ok=True)
            file.touch()
        mac_command, mac_launch_mode = audiveris_command(
            str(fake_launcher), "macos_app_bundle", work, work / "fixture.png"
        )
        # Candidate coordinates are committed per page+measure+hand, never
        # event-by-event.  A later count mismatch must not leave the first
        # half of the same accompaniment group attached.
        map_input, map_anchors, map_output = work / "map-input.json", work / "map-anchors.json", work / "map-output.json"
        map_input.write_text(json.dumps({
            "source": {"type": "omr_candidate"}, "notes": [
                {"note_id": "rh-1", "measure_index": 1, "hand": "RH", "chord_id": "rh-a", "onset": 0, "pitch_midi": 60},
                {"note_id": "rh-2", "measure_index": 1, "hand": "RH", "chord_id": "rh-b", "onset": 1, "pitch_midi": 62},
                {"note_id": "lh-1", "measure_index": 1, "hand": "LH", "chord_id": "lh-a", "onset": 0, "pitch_midi": 48},
            ],
        }), encoding="utf-8")
        map_anchors.write_text(json.dumps({
            "candidate_only": True, "count_consistent": True,
            "pages": [{"page": 1, "target_image": "fixture.png", "target_width": 300, "target_height": 300,
                "candidate_noteheads": [
                    {"page_x": 10, "page_y": 100, "local_measure": 1, "hand": "RH"},
                    {"page_x": 30, "page_y": 96, "local_measure": 1, "hand": "RH"},
                    {"page_x": 10, "page_y": 200, "local_measure": 1, "hand": "LH"},
                    {"page_x": 30, "page_y": 196, "local_measure": 1, "hand": "LH"},
                ]}],
        }), encoding="utf-8")
        subprocess.run(
            [sys.executable, str(script_dir / "attach_audiveris_candidate_anchors.py"), str(map_input), str(map_anchors), "--page", "1", "-o", str(map_output)],
            check=True, capture_output=True, text=True,
        )
        mapped = json.loads(map_output.read_text(encoding="utf-8"))
        # Equal note counts alone are not enough.  A head that is horizontally
        # separated from its intended chord must not make every later note in
        # the scope inherit an offset coordinate.
        topology_input, topology_anchors, topology_output = work / "topology-input.json", work / "topology-anchors.json", work / "topology-output.json"
        topology_input.write_text(json.dumps({
            "source": {"type": "omr_candidate"}, "notes": [
                {"note_id": "rh-low", "measure_index": 1, "hand": "RH", "chord_id": "rh-chord", "onset": 0, "pitch_midi": 60},
                {"note_id": "rh-high", "measure_index": 1, "hand": "RH", "chord_id": "rh-chord", "onset": 0, "pitch_midi": 64},
                {"note_id": "rh-next", "measure_index": 1, "hand": "RH", "chord_id": "rh-next", "onset": 1, "pitch_midi": 67},
                {"note_id": "lh-safe", "measure_index": 1, "hand": "LH", "chord_id": "lh-safe", "onset": 0, "pitch_midi": 48},
            ],
        }), encoding="utf-8")
        topology_anchors.write_text(json.dumps({
            "candidate_only": True, "count_consistent": True,
            "pages": [{"page": 1, "target_image": "fixture.png", "target_width": 300, "target_height": 300,
                "candidate_noteheads": [
                    {"page_x": 10, "page_y": 100, "local_measure": 1, "hand": "RH"},
                    {"page_x": 21, "page_y": 96, "local_measure": 1, "hand": "RH"},
                    {"page_x": 30, "page_y": 92, "local_measure": 1, "hand": "RH"},
                    {"page_x": 10, "page_y": 200, "local_measure": 1, "hand": "LH"},
                ]}],
        }), encoding="utf-8")
        subprocess.run(
            [sys.executable, str(script_dir / "attach_audiveris_candidate_anchors.py"), str(topology_input), str(topology_anchors), "--page", "1", "-o", str(topology_output)],
            check=True, capture_output=True, text=True,
        )
        topology_mapped = json.loads(topology_output.read_text(encoding="utf-8"))
        # A page can end with an all-rest measure.  Its absence from the OMR
        # head list must not shift the next page's global measure range.
        rest_page_input, rest_page_anchors, rest_page_output = (
            work / "rest-page-input.json", work / "rest-page-anchors.json", work / "rest-page-output.json",
        )
        rest_page_input.write_text(json.dumps({
            "source": {"type": "omr_candidate"}, "notes": [
                {"note_id": "page-one", "measure_index": 1, "hand": "RH", "chord_id": "p1", "onset": 0, "pitch_midi": 60},
                {"note_id": "page-two", "measure_index": 3, "hand": "RH", "chord_id": "p2", "onset": 0, "pitch_midi": 62},
            ],
        }), encoding="utf-8")
        rest_page_anchors.write_text(json.dumps({
            "candidate_only": True,
            "pages": [
                {"page": 1, "measure_count": 2, "target_image": "fixture.png", "target_width": 300, "target_height": 300,
                 "candidate_noteheads": [{"page_x": 10, "page_y": 100, "local_measure": 1, "hand": "RH"}]},
                {"page": 2, "measure_count": 1, "target_image": "fixture.png", "target_width": 300, "target_height": 300,
                 "candidate_noteheads": [{"page_x": 20, "page_y": 110, "local_measure": 1, "hand": "RH"}]},
            ],
        }), encoding="utf-8")
        subprocess.run(
            [sys.executable, str(script_dir / "attach_audiveris_candidate_anchors.py"), str(rest_page_input), str(rest_page_anchors), "--page", "1", "--page", "2", "-o", str(rest_page_output)],
            check=True, capture_output=True, text=True,
        )
        rest_page_mapped = json.loads(rest_page_output.read_text(encoding="utf-8"))
    lh = sorted((note for note in plan["notes"] if note["hand"] == "LH"), key=lambda note: note["onset"])
    rests = plan["rests"]
    checks = {
        "left_hand_treble_clef_preserved": [note["clef"] for note in lh] == ["treble", "treble"],
        "voice_parts_are_excluded_from_piano_plan": (
            len(voice_plan_payload["notes"]) == 2
            and {note["part"] for note in voice_plan_payload["notes"]} == {"P3"}
            and {note["hand"] for note in voice_plan_payload["notes"]} == {"RH", "LH"}
            and voice_candidate_count == 2
            and voice_candidate_counts == {(1, "RH"): 1, (1, "LH"): 1}
        ),
        "explicit_split_hand_parts_route_both_hands": (
            split_plan_payload["source"]["piano_part_routing"] == {"P1": "rh", "P2": "lh"}
            and {(note["part"], note["hand"]) for note in split_plan_payload["notes"]} == {("P1", "RH"), ("P2", "LH")}
        ),
        "tied_chord_retains_slots_without_duplicate_fingers": (
            tied_generation.returncode == 0
            and tied_validation.returncode == 0
            and [
                (note["pitch_midi"], note["finger"])
                for note in sorted(
                    (note for note in tied_plan_payload["notes"] if float(note["onset"]) == 0.0),
                    key=lambda note: note["pitch_midi"],
                )
            ] == [(74, 2), (79, 4), (82, 5)]
            and [
                (note["pitch_midi"], note["finger"])
                for note in sorted(
                    (note for note in tied_plan_payload["notes"] if float(note["onset"]) == 1.0),
                    key=lambda note: note["pitch_midi"],
                )
            ] == [(67, 1), (74, 2), (79, 4), (82, 5)]
        ),
        "leading_rest_preserved": any(
            rest["hand"] == "LH"
            and rest["clef"] == "treble"
            and float(rest["onset"]) == 0.0
            for rest in rests
        ),
        "post_rest_chord_onset_preserved": [note["onset"] for note in lh] == [1.0, 1.0],
        "left_hand_third_uses_3_1": [
            note["finger"]
            for note in sorted(
                (note for note in fingered_plan["notes"] if note["hand"] == "LH"),
                key=lambda note: (note["onset"], note["chord_row"]),
            )
        ] == [3, 1],
        # A rest is a real rhythmic boundary.  Post-processing must not use
        # the preceding measure's hand position to shift the fresh C-E-G-C
        # arpeggio from its prepared 1-2-3-5 pattern.
        "rest_boundary_does_not_shift_rh_arpeggio": [
            note["finger"]
            for note in sorted(
                (
                    note for note in fingered_plan["notes"]
                    if note["hand"] == "RH" and int(note["measure_index"]) == 2
                ),
                key=lambda note: note["onset"],
            )
        ] == [1, 2, 3, 5],
        "structured_run_exports_annotated_musicxml": (
            structured_delivery.returncode == 0
            and structured_manifest["status"] == "complete"
            and str(structured_manifest.get("artifacts", {}).get("musicxml", "")).endswith("fingered-score.musicxml")
            and write_musicxml_stage.get("status") == "passed"
            and f"with {len(fingered_plan['notes'])} fingering marks" in str(write_musicxml_stage.get("stdout", ""))
        ),
        "hand_size_sensitivity_audit_is_nonblocking_and_reported": hand_size_audit_ok,
        "mxl_run_exports_portable_annotated_musicxml": (
            mxl_delivery.returncode == 0
            and mxl_manifest["status"] == "complete"
            and str(mxl_manifest.get("artifacts", {}).get("musicxml", "")).endswith("fingered-score.musicxml")
            and mxl_write_stage.get("status") == "passed"
            and f"with {len(fingered_plan['notes'])} fingering marks" in str(mxl_write_stage.get("stdout", ""))
        ),
        "musescore_conversion_uses_local_renderer_and_validates_musicxml": (
            musescore_conversion.returncode == 0
            and conversion["status"] == "converted"
            and conversion["renderer"] == str(fake_renderer.resolve())
            and conversion["remote_upload"] is False
        ),
        "visual_facts_derive_key_and_keyboard_geometry": (
            visual_plan["notes"][0]["pitch_midi"] == 67
            and visual_plan["notes"][0]["key_fifths"] == 0
            and visual_plan["notes"][0]["keyboard_x_cm"] > 0
        ),
        "visual_facts_can_lock_with_full_measure_evidence": visual_plan["recognition"]["status"] == "locked",
        "blocked_visual_run_delivers_plan_source_and_readable_report": (
            blocked_delivery.returncode == 2
            and blocked_manifest["status"] == "review_required"
            and bool(blocked_manifest.get("artifacts", {}).get("source_score"))
            and "Current recognition plan JSON" in blocked_report
            and "Source score copy" in blocked_report
            and "Preserved without added fingerings" in blocked_report
            and "fingering generation has not started" in blocked_report
        ),
        "effective_hand_size_is_recorded_in_output": (
            visual_small_plan["settings"]["hand_size"] == "S"
            and visual_small_plan["generation"]["hand_size"] == "S"
        ),
        "visual_pdf_requires_verified_anchors": visual_pdf_requires_verified_anchors,
        "blocked_run_preserves_viewable_source_score": source_copy_ok,
        "changed_visual_page_blocks_stale_plan": any("content changed" in error for error in stale_asset_errors),
        "semantic_ledger_is_candidate_only": (
            ledger["purpose"].startswith("candidate semantic checklist")
            and all(entry["accepted"] is False and entry["visual_review"] == "required" for entry in ledger["entries"])
        ),
        "omr_candidate_cannot_bypass_recognition": (
            omr_plan["source"]["type"] == "omr_candidate"
            and any("not an authoritative MusicXML source" in error for error in omr_errors)
        ),
        "provisional_omr_is_explicitly_diagnostic_only": (
            provisional_omr.returncode == 0
            and provisional_omr_plan["source"]["type"] == "omr_candidate"
            and provisional_omr_plan["recognition"]["provisional_omr"]["status"] == "diagnostic_only"
        ),
        "omr_risks_are_scoped_without_flooding_review_queue": (
            {(entry["measure"], entry["hand"]) for entry in scoped_ledger["entries"] if entry.get("review_priority") == "high"}
            == {(1, "RH")}
            and [risk["code"] for risk in scoped_ledger["unscoped_omr_risk_signals"]] == ["unlinked_symbol"]
        ),
        "omr_geometry_timeout_returns_promptly": geometry_timeout == {"status": "timed_out", "timeout_seconds": 1},
        "macos_audiveris_batch_is_explicitly_headless": (
            mac_launch_mode == "macos-bundle-java-batch"
            and "-Djava.awt.headless=true" in mac_command
        ),
        "candidate_anchor_scope_is_transactional": (
            sum(1 for note in mapped["notes"] if note.get("anchor_candidate")) == 2
            and not any(note.get("anchor_candidate") for note in mapped["notes"] if note["hand"] == "LH")
            and mapped["recognition"]["candidate_anchor_review"]["blocked_scopes"] == [
                {"page": 1, "measure": 1, "hand": "LH", "reason": "plan has 1 notes; geometry has 2 heads"}
            ]
        ),
        "candidate_anchor_event_topology_blocks_offset_scope": (
            not any(note.get("anchor_candidate") for note in topology_mapped["notes"] if note["hand"] == "RH")
            and next(note for note in topology_mapped["notes"] if note["note_id"] == "lh-safe").get("anchor_candidate") is True
            and any(
                "event x-cluster topology differs" in row["reason"]
                for row in topology_mapped["recognition"]["candidate_anchor_review"]["blocked_scopes"]
            )
        ),
        "trailing_rest_measure_does_not_shift_next_page_anchors": (
            next(note for note in rest_page_mapped["notes"] if note["note_id"] == "page-one")["page"] == 1
            and next(note for note in rest_page_mapped["notes"] if note["note_id"] == "page-two")["page"] == 2
            and next(note for note in rest_page_mapped["notes"] if note["note_id"] == "page-two")["page_x"] == 20.0
        ),
    }
    report = {"checks": checks, "passed": all(checks.values())}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
