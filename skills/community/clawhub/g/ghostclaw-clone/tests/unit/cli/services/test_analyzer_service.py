import pytest
from ghostclaw.cli.services import AnalyzerService

@pytest.mark.asyncio
async def test_analyzer_service_initialization():
    service = AnalyzerService(
        repo_path=".",
        config_overrides={"use_ai": False},
        use_cache=False,
        json_output=True,
        benchmark=False
    )
    assert service.repo_path == "."
    assert service.config_overrides == {"use_ai": False}
    assert service.use_cache is False

@pytest.mark.asyncio
async def test_analyzer_service_run_mocked(mocker):
    mock_agent = mocker.patch("ghostclaw.cli.services.GhostAgent")
    mock_instance = mock_agent.return_value
    mock_instance.run = mocker.AsyncMock(return_value={"vibe_score": 90, "metadata": {"cache_hit": False}})
    mock_instance.on = mocker.MagicMock()

    service = AnalyzerService(
        repo_path=".",
        config_overrides={"use_ai": False},
        use_cache=False,
        json_output=True,
        benchmark=False
    )
    report = await service.run()
    assert report["vibe_score"] == 90
    assert report["_synthesis_streamed"] is False

@pytest.mark.asyncio
async def test_analyzer_service_invalid_config(mocker):
    mock_config_load = mocker.patch("ghostclaw.cli.services.GhostclawConfig.load")
    mock_config_load.side_effect = Exception("Invalid config")

    service = AnalyzerService(
        repo_path=".",
        config_overrides={"use_ai": False},
        use_cache=False,
        json_output=True,
        benchmark=False
    )

    with pytest.raises(Exception, match="Analysis Error: Configuration Error: Invalid config"):
        await service.run()
