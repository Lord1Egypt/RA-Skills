import pytest
import json
from pathlib import Path
from ghostclaw.cli.services import ConfigService

def test_config_service_init_project(tmp_path):
    ConfigService.init_project(str(tmp_path))
    config_file = tmp_path / ".ghostclaw" / "ghostclaw.json"

    assert config_file.exists()

    data = json.loads(config_file.read_text())
    assert data["use_ai"] is True
    assert data["ai_provider"] == "openrouter"

def test_config_service_init_project_existing(tmp_path):
    config_file = tmp_path / ".ghostclaw" / "ghostclaw.json"
    config_file.parent.mkdir(parents=True)
    config_file.write_text("{}")

    with pytest.raises(FileExistsError):
        ConfigService.init_project(str(tmp_path))
