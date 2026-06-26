from scripts.extract_refs import split_reference_entries


def test_split_reference_entries_handles_numeric_styles():
    ref_text = """References
[1] First paper\n[2] Second paper\n3. Third paper\n(4) Fourth paper
"""
    entries = split_reference_entries(ref_text)
    assert len(entries) >= 4
    assert entries[0].startswith("[1] First paper")
    assert any("Third paper" in entry for entry in entries)
