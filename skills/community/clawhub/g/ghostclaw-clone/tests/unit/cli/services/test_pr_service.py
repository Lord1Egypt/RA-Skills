import pytest
from pathlib import Path
from ghostclaw.cli.services import PRService
import subprocess

@pytest.mark.asyncio
async def test_pr_service_create_pr(mocker):
    service = PRService(repo_path=".")

    mock_run = mocker.patch("ghostclaw.cli.services.subprocess.run")
    mock_run.return_value = mocker.MagicMock(stdout="https://github.com/user/repo/pull/1", returncode=0)

    report_file = Path("dummy_report.md")

    await service.create_pr(report_file, "Title", "Body")

    assert mock_run.call_count == 5

@pytest.mark.asyncio
async def test_pr_service_create_pr_failure(mocker):
    service = PRService(repo_path=".")

    mock_run = mocker.patch("ghostclaw.cli.services.subprocess.run")
    mock_run.side_effect = subprocess.CalledProcessError(1, "git")

    report_file = Path("dummy_report.md")

    with pytest.raises(subprocess.CalledProcessError):
        await service.create_pr(report_file, "Title", "Body")
