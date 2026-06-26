"""
配置模块测试
"""

import pytest
import tempfile
import os
import yaml
import json
from pathlib import Path

from src.data_harvester.config import Config, SourceConfig, ProcessingConfig, ExportConfig, SchedulerConfig
from src.data_harvester.config import DataSourceType, ExportFormat, ProcessingStrategy


class TestConfig:
    """配置测试类"""
    
    def test_config_default_creation(self):
        """测试默认配置创建"""
        config = Config()
        
        assert config.name == "Data Harvester"
        assert config.version == "1.0.0"
        assert config.sources == {}
        assert config.processing is not None
        assert config.exports == []
        assert config.scheduler is not None
        
    def test_source_config_creation(self):
        """测试数据源配置创建"""
        source_config = SourceConfig(
            name="test_source",
            type=DataSourceType.WEB,
            url="https://example.com",
            enabled=True
        )
        
        assert source_config.name == "test_source"
        assert source_config.type == DataSourceType.WEB
        assert source_config.url == "https://example.com"
        assert source_config.enabled is True
        
    def test_processing_config_creation(self):
        """测试处理配置创建"""
        processing_config = ProcessingConfig(
            enabled=True,
            strategy=[ProcessingStrategy.CLEAN, ProcessingStrategy.TRANSFORM]
        )
        
        assert processing_config.enabled is True
        assert ProcessingStrategy.CLEAN in processing_config.strategy
        assert ProcessingStrategy.TRANSFORM in processing_config.strategy
        
    def test_export_config_creation(self):
        """测试导出配置创建"""
        export_config = ExportConfig(
            name="csv_export",
            format=ExportFormat.CSV,
            output_path="output.csv"
        )
        
        assert export_config.name == "csv_export"
        assert export_config.format == ExportFormat.CSV
        assert export_config.output_path == "output.csv"
        
    def test_scheduler_config_creation(self):
        """测试调度器配置创建"""
        scheduler_config = SchedulerConfig(
            enabled=True,
            timezone="Asia/Shanghai",
            max_workers=4
        )
        
        assert scheduler_config.enabled is True
        assert scheduler_config.timezone == "Asia/Shanghai"
        assert scheduler_config.max_workers == 4
        
    def test_config_yaml_roundtrip(self):
        """测试YAML配置往返"""
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            config_data = {
                "name": "Test Harvester",
                "version": "2.0.0",
                "sources": {
                    "test_web": {
                        "name": "Test Web",
                        "type": "web",
                        "url": "https://test.example.com"
                    }
                },
                "processing": {
                    "enabled": True,
                    "strategy": ["clean", "transform"]
                }
            }
            yaml.dump(config_data, f)
            temp_path = f.name
        
        try:
            # 加载配置
            config = Config.load(temp_path)
            
            assert config.name == "Test Harvester"
            assert config.version == "2.0.0"
            assert "test_web" in config.sources
            assert config.sources["test_web"].name == "Test Web"
            assert config.processing.enabled is True
            
            # 保存配置
            new_temp_path = temp_path + ".new.yaml"
            config.save(new_temp_path)
            
            # 验证保存的配置
            assert os.path.exists(new_temp_path)
            
            # 清理
            os.unlink(new_temp_path)
            
        finally:
            # 清理临时文件
            os.unlink(temp_path)
            
    def test_config_json_roundtrip(self):
        """测试JSON配置往返"""
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            config_data = {
                "name": "Test Harvester JSON",
                "version": "3.0.0",
                "sources": {
                    "test_api": {
                        "name": "Test API",
                        "type": "api",
                        "url": "https://api.test.example.com"
                    }
                }
            }
            json.dump(config_data, f)
            temp_path = f.name
        
        try:
            # 加载配置
            config = Config.load(temp_path)
            
            assert config.name == "Test Harvester JSON"
            assert config.version == "3.0.0"
            assert "test_api" in config.sources
            assert config.sources["test_api"].type == DataSourceType.API
            
        finally:
            # 清理临时文件
            os.unlink(temp_path)
            
    def test_invalid_config_file(self):
        """测试无效配置文件"""
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("This is not a valid config file")
            temp_path = f.name
        
        try:
            # 应该抛出异常
            with pytest.raises(ValueError):
                Config.load(temp_path)
                
        finally:
            # 清理临时文件
            os.unlink(temp_path)
            
    def test_missing_config_file(self):
        """测试不存在的配置文件"""
        with pytest.raises(FileNotFoundError):
            Config.load("/non/existent/path/config.yaml")