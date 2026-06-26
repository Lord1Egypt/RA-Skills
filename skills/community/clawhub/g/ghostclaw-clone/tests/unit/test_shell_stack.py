import pytest
from pathlib import Path
from ghostclaw.core.detector import detect_stack
from ghostclaw.stacks.shell import ShellAnalyzer
from ghostclaw.stacks import get_analyzer

def test_shell_detection(tmp_path):
    # Test with .sh file in root
    (tmp_path / "script.sh").write_text("#!/bin/bash")
    assert detect_stack(str(tmp_path)) == 'shell'
    
    # Test with .shellcheckrc
    (tmp_path / "script.sh").unlink()
    (tmp_path / ".shellcheckrc").write_text("")
    assert detect_stack(str(tmp_path)) == 'shell'

def test_shell_analyzer_extension():
    analyzer = ShellAnalyzer()
    assert '.sh' in analyzer.get_extensions()
    assert '.bash' in analyzer.get_extensions()
    assert analyzer.get_large_file_threshold() == 150

def test_get_shell_analyzer():
    analyzer = get_analyzer('shell')
    assert isinstance(analyzer, ShellAnalyzer)
