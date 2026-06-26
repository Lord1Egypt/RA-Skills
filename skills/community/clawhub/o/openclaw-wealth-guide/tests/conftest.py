"""
测试配置和夹具
"""

import pytest
import tempfile
import os
import sys
from pathlib import Path

# 添加src目录到Python路径
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture
def temp_config_file():
    """临时配置文件夹具"""
    config_content = """
    name: "Test Harvester"
    version: "1.0.0"
    log_level: "DEBUG"
    sources:
      test_web:
        name: "Test Web Source"
        type: "web"
        url: "https://test.example.com"
        enabled: true
    
    processing:
      enabled: true
      strategy: ["clean", "transform"]
    
    exports:
      - name: "csv_export"
        format: "csv"
        output_path: "test_output.csv"
        enabled: true
    
    scheduler:
      enabled: false
      timezone: "UTC"
    """
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(config_content)
        temp_path = f.name
    
    yield temp_path
    
    # 清理
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
def sample_data():
    """样本数据夹具"""
    return [
        {"id": 1, "name": "Item 1", "value": 100},
        {"id": 2, "name": "Item 2", "value": 200},
        {"id": 3, "name": "Item 3", "value": 300},
    ]


@pytest.fixture
def mock_web_adapter():
    """模拟Web适配器夹具"""
    from unittest.mock import Mock
    from src.data_harvester.adapters.base import WebAdapter
    from src.data_harvester.config import SourceConfig, DataSourceType
    
    mock_adapter = Mock(spec=WebAdapter)
    mock_adapter.name = "test_web"
    mock_adapter.type = DataSourceType.WEB
    mock_adapter.enabled = True
    mock_adapter.fetch.return_value = {"title": "Test Page", "content": "Test Content"}
    
    return mock_adapter


@pytest.fixture
def mock_csv_exporter():
    """模拟CSV导出器夹具"""
    from unittest.mock import Mock
    from src.data_harvester.exporters.base import CsvExporter
    from src.data_harvester.config import ExportFormat
    
    mock_exporter = Mock(spec=CsvExporter)
    mock_exporter.name = "csv_export"
    mock_exporter.format = ExportFormat.CSV
    mock_exporter.enabled = True
    mock_exporter.export.return_value = True
    
    return mock_exporter