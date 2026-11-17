# Editorial PDF Fingering Anchors

Use when a PDF contains readable editorial fingers without matching MusicXML. Keep the source PDF and private reference JSON out of the skill package.

```json
{
  "schema_version": "editorial-pdf-anchors-v1",
  "title": "Example score, page 1",
  "coordinate_unit": "pixel",
  "page_images": [{"page": 1, "width": 992, "height": 1403}],
  "anchors": [
    {"page": 1, "hand": "RH", "note_x": 248.0, "note_y": 318.0, "pitch_midi": 69, "finger": 4}
  ]
}
```

note_x/note_y identify source head centers, not digits. coordinate_unit defaults to pdf_point. Pixel references require actual PNG dimensions in page_images; do not guess sizes or mix units. Optional pitch_midi prevents nearby mismatches. Record only clearly visible digits with unambiguous ownership. compare_editorial_pdf_anchors.py reports head matching and fingering agreement separately.
