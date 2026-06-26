import pytest
from pathlib import Path
from ghostclaw.core.detector import detect_stack
from ghostclaw.stacks.docker import DockerAnalyzer
from ghostclaw.stacks import get_analyzer

def test_docker_detection(tmp_path):
    # Test with Dockerfile in root
    (tmp_path / "Dockerfile").write_text("FROM alpine")
    assert detect_stack(str(tmp_path)) == 'docker'
    
    # Test with docker-compose.yml
    (tmp_path / "Dockerfile").unlink()
    (tmp_path / "docker-compose.yml").write_text("version: '3'")
    assert detect_stack(str(tmp_path)) == 'docker'

def test_docker_analyzer_config():
    analyzer = DockerAnalyzer()
    assert 'Dockerfile' in analyzer.get_extensions()
    assert analyzer.get_large_file_threshold() == 100

def test_get_docker_analyzer():
    analyzer = get_analyzer('docker')
    assert isinstance(analyzer, DockerAnalyzer)

def test_go_analyzer_still_works():
    # Ensure Go analyzer is still registered correctly
    analyzer = get_analyzer('go')
    assert analyzer is not None
    assert '.go' in analyzer.get_extensions()
