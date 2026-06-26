from pathlib import Path

from scripts.html_quality_gate import validate_html_text


ROOT = Path(__file__).resolve().parent.parent


def test_html_quality_gate_rejects_handrolled_regular_lumen_shell():
    html = """
<!DOCTYPE html>
<html lang="zh" data-template="kai-report-creator" data-version="1.23.0" data-theme="regular-lumen">
<head>
<style>
/* regular-lumen theme CSS */
body {
  font-family: system-ui, -apple-system, sans-serif;
  background-color: var(--bg);
  padding: 2rem;
  max-width: 1200px;
}
</style>
</head>
<body>
<script type="application/json" id="report-summary">{"title":"T","sections":[],"kpis":[]}</script>
<h1>报告</h1>
</body>
</html>
""".strip()
    report = validate_html_text(html)
    codes = {finding["code"] for finding in report["findings"]}
    messages = "\n".join(finding["message"] for finding in report["findings"])

    assert report["status"] == "invalid"
    assert "shell.missing_id" in codes
    assert "theme.fingerprint_mismatch" in codes
    assert "theme.regular_lumen_body_layout" in codes
    assert "body max-width/padding" in messages
    assert "Playfair Display" in messages
    assert ".report-wrapper" in messages


def test_html_quality_gate_rejects_placeholder_and_status_kpi_values():
    html = """
<!DOCTYPE html>
<html data-template="kai-report-creator" data-version="1.23.0" data-theme="corporate-blue">
<head><style>/* Theme: corporate-blue */ --font-sans: x; body { font-family: var(--font-sans) }</style></head>
<body>
<script type="application/json" id="report-summary">
{"title":"T","sections":[],"kpis":[{"label":"会议数","value":"[数据待填写]"}]}
</script>
<button id="toc-toggle-btn"></button><nav id="toc-sidebar"></nav>
<button id="card-mode-btn"></button><div id="sc-overlay"></div>
<div id="edit-hotzone"></div><button id="edit-toggle"></button>
<button id="export-btn"></button><div id="export-menu"></div>
<button id="export-print"></button><button id="export-png-desktop"></button>
<button id="export-png-mobile"></button><button id="export-im-share"></button>
<div class="kpi-value">通过</div>
</body>
</html>
""".strip()
    report = validate_html_text(html, theme_fidelity=False)
    codes = [finding["code"] for finding in report["findings"]]

    assert report["status"] == "invalid"
    assert "kpi.invalid_value" in codes
    assert "summary.invalid_kpi_value" in codes


def test_html_quality_gate_accepts_regular_lumen_theme_fidelity_without_shell_check():
    html = (ROOT / "templates" / "zh" / "regular-lumen.html").read_text(encoding="utf-8")
    report = validate_html_text(html, standard_shell=False)

    assert report["status"] == "valid"


def test_html_quality_gate_accepts_fangsong_theme_fidelity_without_shell_check():
    theme_css = (ROOT / "templates" / "themes" / "fangsong.css").read_text(encoding="utf-8")
    html = f"""
<!DOCTYPE html>
<html data-template="kai-report-creator" data-version="1.23.0" data-theme="fangsong">
<head><style>{theme_css}</style></head>
<body>
<script type="application/json" id="report-summary">{{"title":"T","sections":[],"kpis":[]}}</script>
</body>
</html>
""".strip()

    report = validate_html_text(html, standard_shell=False)

    assert report["status"] == "valid"
