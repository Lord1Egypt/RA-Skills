import pytest
from pathlib import Path
from ghostclaw.core.detector import detect_stack
from ghostclaw.stacks.typescript import TypeScriptAnalyzer
from ghostclaw.stacks import get_analyzer

def test_typescript_detection(tmp_path):
    # Test with tsconfig.json in root
    (tmp_path / "tsconfig.json").write_text("{}")
    assert detect_stack(str(tmp_path)) == 'typescript'
    
    # Test node fallback (package.json but no tsconfig)
    (tmp_path / "tsconfig.json").unlink()
    (tmp_path / "package.json").write_text('{"name": "test"}')
    assert detect_stack(str(tmp_path)) == 'node'

def test_typescript_analyzer_config():
    analyzer = TypeScriptAnalyzer()
    assert '.ts' in analyzer.get_extensions()
    assert '.tsx' in analyzer.get_extensions()
    assert '.js' in analyzer.get_extensions()
    assert analyzer.get_large_file_threshold() == 350

def test_get_typescript_analyzer():
    analyzer = get_analyzer('typescript')
    assert isinstance(analyzer, TypeScriptAnalyzer)
