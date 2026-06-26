"""
notes_builder.py — Speaker notes injection for slides.

python-pptx natively supports notes:
  https://python-pptx.readthedocs.io/en/latest/user/notes.html
"""


def add_notes(slide, notes_text):
    """Add speaker notes to a slide.

    notes_text: plain text string for the notes pane.
    """
    if not notes_text:
        return
    notes_slide = slide.notes_slide
    notes_slide.notes_text_frame.text = notes_text


def add_notes_from_manifest(prs, slides_data):
    """Add notes to all slides from manifest data.

    Each slide in slides_data can have a "notes" key with the text.
    """
    for idx, slide_data in enumerate(slides_data):
        notes = slide_data.get("notes")
        if notes and idx < len(prs.slides):
            add_notes(prs.slides[idx], notes)
