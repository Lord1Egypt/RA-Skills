from opendart_cli.cli import main


def test_report_codes(capsys):
    code = main(["report-codes"])
    assert code == 0
    out = capsys.readouterr().out
    assert "11011" in out
    assert "사업보고서" in out


def test_version(capsys):
    try:
        main(["--version"])
    except SystemExit:
        pass
    out = capsys.readouterr().out
    assert "opendart-cli" in out
