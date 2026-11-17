"""
test_nutrigenomics.py — Automated test suite for Nutrigenomics
Run with: pytest tests/test_nutrigenomics.py -v

Uses a FIXED synthetic patient (synthetic_patient.csv) with known genotypes
so that all assertions are deterministic and reproducible. This file is NOT
meant to showcase the skill — use examples/generate_patient.py for varied demos.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from parse_input import parse_genetic_file
from extract_genotypes import extract_snp_genotypes
from score_variants import compute_nutrient_risk_scores


SYNTHETIC = Path(__file__).parent / "synthetic_patient.csv"
PANEL     = Path(__file__).parent.parent / "data" / "snp_panel.json"


def load_panel():
    with open(PANEL) as f:
        return json.load(f)


# ── Parsing ────────────────────────────────────────────────────────────────────

def test_parse_23andme():
    table = parse_genetic_file(str(SYNTHETIC), fmt="23andme")
    assert len(table) >= 20
    assert "rs1801133" in table
    assert table["rs1801133"] in ("CT", "TC")


def test_all_panel_snps_present():
    panel = load_panel()
    table = parse_genetic_file(str(SYNTHETIC), fmt="23andme")
    calls = extract_snp_genotypes(table, panel)
    found = sum(1 for v in calls.values() if v["status"] == "found")
    assert found == len(panel), f"Expected all {len(panel)} SNPs found, got {found}"


# ── Extraction ─────────────────────────────────────────────────────────────────

def test_mthfr_heterozygous():
    """Fixed patient has MTHFR C677T = CT (1 risk allele)."""
    panel = load_panel()
    table = parse_genetic_file(str(SYNTHETIC), fmt="23andme")
    calls = extract_snp_genotypes(table, panel)
    mthfr = calls["rs1801133"]
    assert mthfr["status"] == "found"
    assert mthfr["risk_count"] == 1


def test_vdr_homozygous_risk():
    """Fixed patient has VDR TaqI = CC (2 risk alleles) → drives Elevated vitamin D score."""
    panel = load_panel()
    table = parse_genetic_file(str(SYNTHETIC), fmt="23andme")
    calls = extract_snp_genotypes(table, panel)
    vdr = calls["rs731236"]
    assert vdr["status"] == "found"
    assert vdr["risk_count"] == 2


def test_aldh2_ref_homozygous():
    """Fixed patient has ALDH2 = GG (0 risk alleles) → Low alcohol risk."""
    panel = load_panel()
    table = parse_genetic_file(str(SYNTHETIC), fmt="23andme")
    calls = extract_snp_genotypes(table, panel)
    aldh2 = calls["rs671"]
    assert aldh2["status"] == "found"
    assert aldh2["risk_count"] == 0


# ── Scoring ────────────────────────────────────────────────────────────────────

def test_scores_structure():
    panel = load_panel()
    table = parse_genetic_file(str(SYNTHETIC), fmt="23andme")
    calls = extract_snp_genotypes(table, panel)
    scores = compute_nutrient_risk_scores(calls, panel)
    assert "folate" in scores
    assert "vitamin_d" in scores
    assert "omega3" in scores
    assert "alcohol" in scores
    for domain, data in scores.items():
        if data["score"] is not None:
            assert 0.0 <= data["score"] <= 10.0
        assert data["category"] in ("Low", "Moderate", "Elevated", "Unknown")


def test_vitamin_d_elevated():
    """VDR TaqI hom risk → Vitamin D expected Elevated."""
    panel = load_panel()
    table = parse_genetic_file(str(SYNTHETIC), fmt="23andme")
    calls = extract_snp_genotypes(table, panel)
    scores = compute_nutrient_risk_scores(calls, panel)
    assert scores["vitamin_d"]["category"] == "Elevated"


def test_alcohol_low():
    """ALDH2 GG ref hom → Alcohol expected Low."""
    panel = load_panel()
    table = parse_genetic_file(str(SYNTHETIC), fmt="23andme")
    calls = extract_snp_genotypes(table, panel)
    scores = compute_nutrient_risk_scores(calls, panel)
    assert scores["alcohol"]["category"] == "Low"


def test_folate_not_low():
    """MTHFR C677T het → Folate should be Moderate or Elevated, not Low."""
    panel = load_panel()
    table = parse_genetic_file(str(SYNTHETIC), fmt="23andme")
    calls = extract_snp_genotypes(table, panel)
    scores = compute_nutrient_risk_scores(calls, panel)
    assert scores["folate"]["category"] in ("Moderate", "Elevated")


# ── Lactase persistence (rs4988235) ───────────────────────────────────────────
# Adapted from a fix contributed by krudo-taco to the ClawBio nutrigx skill
# (ClawBio/ClawBio@1163f49, MIT). Covers both strand orientations, so the
# strand-flip path in extract_genotypes.py is exercised too.

def _lactose_score(genotype: str) -> dict:
    panel = load_panel()
    calls = extract_snp_genotypes({"rs4988235": genotype}, panel)
    scores = compute_nutrient_risk_scores(calls, panel)
    return {"call": calls["rs4988235"], "score": scores["lactose"]}


def test_rs4988235_panel_polarity_and_citation():
    entry = next(s for s in load_panel() if s["rsid"] == "rs4988235")
    assert entry["ref_allele"] == "A"
    assert entry["risk_allele"] == "G"
    assert entry["pmid"] == "11788828"
    assert entry["inheritance"] == "dominant_protective"


def test_rs4988235_aa_and_tt_are_persistent():
    for genotype in ("AA", "TT"):
        result = _lactose_score(genotype)
        assert result["call"]["status"] == "found"
        assert result["call"]["risk_count"] == 0
        assert result["score"]["category"] == "Low"
        assert result["score"]["score"] == 0.0


def test_rs4988235_ag_and_ct_are_persistent_dominant():
    for genotype in ("AG", "GA", "CT", "TC"):
        result = _lactose_score(genotype)
        assert result["call"]["status"] == "found"
        assert result["call"]["risk_count"] == 1
        assert result["score"]["category"] == "Low"
        assert result["score"]["score"] == 0.0


def test_rs4988235_gg_and_cc_are_non_persistent():
    for genotype in ("GG", "CC"):
        result = _lactose_score(genotype)
        assert result["call"]["status"] == "found"
        assert result["call"]["risk_count"] == 2
        assert result["score"]["category"] == "Elevated"
        assert result["score"]["score"] == 10.0


# ── ELOVL2 rs953413: A is the lower-DHA allele ────────────────────────────────
# Tanaka et al. 2009 (PMID 19148276): DHA falls GG > AG > AA in two cohorts, and
# "the presence of the minor (A) allele was associated with higher EPA/DPA and
# lower DHA". The panel previously scored G as the risk allele. G/A is the plus
# strand in GRCh37 and GRCh38; the SNP is not palindromic, so T/C calls on the
# minus strand must resolve to the same counts.

def _rs953413_call(genotype: str) -> dict:
    return extract_snp_genotypes({"rs953413": genotype}, load_panel())["rs953413"]


def test_rs953413_panel_direction_and_citation():
    entry = next(s for s in load_panel() if s["rsid"] == "rs953413")
    assert entry["ref_allele"] == "G"
    assert entry["risk_allele"] == "A"
    assert entry["pmid"] == "19148276"
    assert entry["effect_direction"] == "lower_epa_to_dha_conversion"


def test_rs953413_plus_strand_counts():
    for genotype, expected in (("AA", 2), ("AG", 1), ("GA", 1), ("GG", 0)):
        call = _rs953413_call(genotype)
        assert call["status"] == "found", genotype
        assert call["risk_count"] == expected, f"{genotype}: {call['risk_count']} != {expected}"
        assert call.get("strand_ambiguous") is False


def test_rs953413_minus_strand_counts():
    for genotype, expected in (("TT", 2), ("TC", 1), ("CT", 1), ("CC", 0)):
        call = _rs953413_call(genotype)
        assert call["status"] == "found", genotype
        assert call["risk_count"] == expected, f"{genotype}: {call['risk_count']} != {expected}"


def test_rs953413_gg_scores_lower_omega3_risk_than_aa():
    panel = load_panel()
    gg = compute_nutrient_risk_scores(extract_snp_genotypes({"rs953413": "GG"}, panel), panel)["omega3"]
    aa = compute_nutrient_risk_scores(extract_snp_genotypes({"rs953413": "AA"}, panel), panel)["omega3"]
    assert gg["score"] < aa["score"]


# ── Reproducibility bundle must not leak the input path ───────────────────────
# Regression test for a privacy defect found by the ClawHub security audit of
# 0.3.2: provenance.json and README_reproducibility.txt both echoed the full
# argument namespace, writing the absolute path of the user's genetic data file
# into artefacts that simultaneously claimed "the input file name and path are
# NOT stored in any artefact".

def test_repro_bundle_does_not_record_input_path(tmp_path):
    import json as _json
    from repro_bundle import create_reproducibility_bundle

    secret = tmp_path / "jane_smith_genome_verysecret.csv"
    secret.write_text("rsid\tchromosome\tposition\tgenotype\n", encoding="utf-8")
    out = tmp_path / "out"
    out.mkdir()
    (out / "nutrigenomics_report.md").write_text("# report\n", encoding="utf-8")

    create_reproducibility_bundle(
        input_file=str(secret),
        output_dir=str(out),
        panel_path=str(PANEL),
        args={
            "input": str(secret),
            "output": str(out),
            "format": "23andme",
            "panel": None,
            "no_figures": False,
        },
    )

    for artefact in out.iterdir():
        if artefact.name == "nutrigenomics_report.md":
            continue
        text = artefact.read_text(encoding="utf-8", errors="replace")
        assert str(secret) not in text, f"{artefact.name} leaks the input path"
        assert secret.name not in text, f"{artefact.name} leaks the input filename"
        assert str(tmp_path) not in text, f"{artefact.name} leaks a local path"

    provenance = _json.loads((out / "provenance.json").read_text(encoding="utf-8"))
    assert set(provenance["format_args"]) <= {"format", "no_figures", "custom_panel"}
    assert provenance["version"] != "0.2.8", "version must track the release, not be hardcoded"


# ── Output writes must not follow symlinks ────────────────────────────────────
# Regression test for the ClawHub audit finding "Symlink Following Vulnerability".
# Output filenames are deterministic, so an attacker who can pre-create a symlink
# at one of them could redirect a write outside the validated output directory.

def test_safe_write_refuses_symlink(tmp_path):
    from path_safety import safe_write_text

    target = tmp_path / "escaped.txt"
    link = tmp_path / "report.md"
    link.symlink_to(target)

    try:
        safe_write_text(link, "payload")
    except ValueError as exc:
        assert "symbolic link" in str(exc)
    else:
        raise AssertionError("safe_write_text followed a symlink")

    assert not target.exists(), "write escaped through the symlink"


def test_safe_write_still_overwrites_regular_files(tmp_path):
    from path_safety import safe_write_text

    path = tmp_path / "report.md"
    safe_write_text(path, "first")
    safe_write_text(path, "second")
    assert path.read_text(encoding="utf-8") == "second"


def test_safe_write_refuses_symlinked_parent_directory(tmp_path):
    """O_NOFOLLOW guards only the final component; the parent must be pinned too."""
    from path_safety import safe_write_text

    real_dir = tmp_path / "real"; real_dir.mkdir()
    evil = tmp_path / "evil"; evil.mkdir()
    link_dir = tmp_path / "link"; link_dir.symlink_to(evil)

    try:
        safe_write_text(link_dir / "report.md", "payload")
    except ValueError as exc:
        assert "symbolic link" in str(exc)
    else:
        raise AssertionError("write went through a symlinked parent directory")

    assert not any(evil.iterdir()), "write escaped into the symlink target"

    # a genuine directory is unaffected
    safe_write_text(real_dir / "report.md", "ok")
    assert (real_dir / "report.md").read_text(encoding="utf-8") == "ok"


# ── Input filename must not inject Markdown into the report ───────────────────
# Regression test for the ClawHub audit of 0.3.6, "Untrusted Input Filename
# Embedded in Generated Markdown": the header wraps the filename in a code span,
# so a backtick in the name escaped it and allowed arbitrary Markdown or HTML.

def test_filename_cannot_break_out_of_the_code_span():
    from generate_report import safe_display_filename

    hostile = "/tmp/evil`</code><script>alert(1)</script>`.csv"
    safe = safe_display_filename(hostile)
    for ch in ("`", "<", ">", "/"):
        assert ch not in safe, f"{ch!r} survived sanitisation"


def test_filename_is_truncated_and_path_is_stripped():
    from generate_report import safe_display_filename

    assert safe_display_filename("/home/someone/genome.csv") == "genome.csv"
    assert len(safe_display_filename("/x/" + "a" * 500 + ".csv")) <= 80
    assert safe_display_filename("") == "(not recorded)"


def test_ordinary_filenames_are_left_readable():
    from generate_report import safe_display_filename

    assert safe_display_filename("/data/AncestryDNA (2026).txt") == "AncestryDNA (2026).txt"


# ── Genotype values are untrusted input ───────────────────────────────────────
# Regression test for the ClawHub audit of 0.3.7, "Unvalidated Genotype Values
# Allow Markdown and HTML Report Injection": genotype calls are read from a
# user-supplied file and rendered into a Markdown code span, so a backtick in
# column 4 escaped it exactly as a hostile filename did.

def test_clean_genotype_accepts_real_calls():
    from parse_input import clean_genotype

    assert clean_genotype("CT") == "CT"
    assert clean_genotype("ct") == "CT"
    assert clean_genotype("A-") == "A"
    assert clean_genotype("DI") == "DI"          # 23andMe deletion/insertion
    assert clean_genotype("ACGTACGT") == "ACGTACGT"  # VCF indel run


def test_clean_genotype_rejects_anything_else():
    from parse_input import clean_genotype

    for hostile in ("`</code><script>alert(1)</script>`", "<img src=x onerror=y>",
                    "|**INJECTED**|", "--", "", "XYZ", None, "A" * 40):
        assert clean_genotype(hostile) is None, f"accepted {hostile!r}"


def test_hostile_genotypes_never_reach_the_report(tmp_path):
    from parse_input import parse_genetic_file

    f = tmp_path / "hostile.txt"
    f.write_text(
        "rsid\tchromosome\tposition\tgenotype\n"
        "rs1801133\t1\t11856378\tCT\n"
        "rs4988235\t2\t136608646\tA`</code><script>x</script>`G\n",
        encoding="utf-8",
    )
    table = parse_genetic_file(str(f), fmt="23andme")
    assert table.get("rs1801133") == "CT"
    assert "rs4988235" not in table, "hostile call was parsed instead of discarded"


def test_render_guard_catches_values_bypassing_the_parser():
    """openclaw_adapter and API callers can supply genotypes directly."""
    from generate_report import safe_display_genotype

    out = safe_display_genotype("A`<script>alert(1)</script>`G")
    for ch in ("`", "<", ">", "(", ")"):
        assert ch not in out, f"{ch!r} survived the render guard"
    assert safe_display_genotype(None) == "--"


# ── Resource limits and output collisions ─────────────────────────────────────
# The audit has repeatedly surfaced one instance of a class at a time. These
# tests pin the classes: untrusted input cannot exhaust memory, and concurrent
# runs cannot overwrite each other's report.

def test_oversized_input_is_rejected_with_a_clear_error(tmp_path, monkeypatch):
    import path_safety

    monkeypatch.setattr(path_safety, "MAX_INPUT_BYTES", 1024)
    big = tmp_path / "big.txt"
    big.write_text("x" * 5000, encoding="utf-8")
    try:
        path_safety.check_input_size(big)
    except ValueError as exc:
        assert "above the" in str(exc)
    else:
        raise AssertionError("oversized input was accepted")


def test_variant_count_is_capped(tmp_path, monkeypatch):
    import parse_input

    monkeypatch.setattr(parse_input, "MAX_VARIANTS", 50)
    f = tmp_path / "many.txt"
    f.write_text(
        "rsid\tchromosome\tposition\tgenotype\n"
        + "\n".join(f"rs{i}\t1\t{i}\tCT" for i in range(5000)),
        encoding="utf-8",
    )
    assert len(parse_input.parse_23andme(str(f))) <= 50


def test_absurdly_long_lines_are_skipped_not_buffered(tmp_path, monkeypatch):
    import parse_input

    monkeypatch.setattr(parse_input, "MAX_LINE_BYTES", 100)
    f = tmp_path / "long.txt"
    f.write_text(
        "rsid\tchromosome\tposition\tgenotype\n"
        "rs1801133\t1\t1\tCT\n"
        "rs4988235\t2\t2\t" + "A" * 5000 + "\n",
        encoding="utf-8",
    )
    table = parse_input.parse_23andme(str(f))
    assert table.get("rs1801133") == "CT"
    assert "rs4988235" not in table


def test_panel_derived_text_cannot_inject_markdown():
    from generate_report import safe_display_text

    out = safe_display_text("MTHFR`</code><script>alert(1)</script>`")
    for ch in ("`", "<", ">"):
        assert ch not in out
    assert safe_display_text("FADS1/2") == "FADS1/2"      # legitimate symbols kept
    assert safe_display_text(None) == ""


# ── Palindromic (A/T, C/G) SNPs must never be strand-flipped ──────────────────
# Flipping a palindromic genotype yields the other allele of the same pair, so
# the flip always "succeeds" and converts homozygous reference into homozygous
# risk. At rs9939609 (FTO, T/A) a TT call -- no risk alleles -- was normalised to
# AA and scored 2. Three panel entries are palindromic.

PALINDROMIC = ("rs12934922", "rs9939609", "rs1801282")


def test_palindromic_snps_are_not_flipped():
    panel = load_panel()
    for rsid in PALINDROMIC:
        entry = next(e for e in panel if e["rsid"] == rsid)
        ref, risk = entry["ref_allele"], entry["risk_allele"]
        assert {ref, risk} in ({"A", "T"}, {"C", "G"}), f"{rsid} is not palindromic"
        for genotype, expected in ((ref * 2, 0), (ref + risk, 1), (risk * 2, 2)):
            call = extract_snp_genotypes({rsid: genotype}, panel)[rsid]
            assert call["risk_count"] == expected, (
                f"{rsid} {genotype}: risk_count {call['risk_count']}, expected {expected}"
            )


def test_palindromic_calls_are_flagged_as_strand_ambiguous():
    panel = load_panel()
    entry = next(e for e in panel if e["rsid"] == "rs9939609")
    call = extract_snp_genotypes({"rs9939609": entry["ref_allele"] * 2}, panel)["rs9939609"]
    assert call.get("strand_ambiguous") is True

    non_palindromic = extract_snp_genotypes({"rs1801133": "CC"}, panel)["rs1801133"]
    assert non_palindromic.get("strand_ambiguous") is False


def test_non_palindromic_snps_still_flip():
    """rs4988235 is C/T vs G/A -- flipping is unambiguous and must still work."""
    panel = load_panel()
    for genotype in ("CC", "GG"):          # same call, opposite strands
        call = extract_snp_genotypes({"rs4988235": genotype}, panel)["rs4988235"]
        assert call["risk_count"] == 2, f"{genotype} should be 2 risk alleles"
