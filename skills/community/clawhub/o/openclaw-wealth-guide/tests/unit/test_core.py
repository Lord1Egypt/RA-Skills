"""
核心模块测试
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import tempfile
import os

from src.data_harvester.core import DataHarvester, HarvestResult
from src.data_harvester.config import Config, SourceConfig, DataSourceType
from src.data_harvester.exceptions import DataHarvesterError


class TestDataHarvester:
    """DataHarvester测试类"""
    
    def test_harvester_creation(self):
        """测试采集器创建"""
        harvester = DataHarvester()
        
        assert harvester.config is not None
        assert isinstance(harvester.config, Config)
        assert harvester._initialized is False
        
    def test_harvester_with_config_path(self):
        """测试带配置路径的采集器创建"""
        # 创建临时配置文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            config_content = """
            name: "Test Harvester"
            version: "1.0.0"
            sources: {}
            """
            f.write(config_content)
            temp_path = f.name
        
        try:
            harvester = DataHarvester(config_path=temp_path)
            assert harvester.config.name == "Test Harvester"
            assert harvester.config.version == "1.0.0"
            
        finally:
            os.unlink(temp_path)
            
    def test_harvester_initialize(self):
        """测试采集器初始化"""
        harvester = DataHarvester()
        
        # 模拟适配器、处理器、导出器
        with patch('src.data_harvester.core.AdapterFactory') as mock_adapter_factory, \
             patch('src.data_harvester.core.ProcessorFactory') as mock_processor_factory, \
             patch('src.data_harvester.core.ExportFactory') as mock_export_factory, \
             patch('src.data_harvester.core.Scheduler') as mock_scheduler_class:
            
            # 设置模拟对象
            mock_adapter = Mock()
            mock_adapter_factory.create_adapter.return_value = mock_adapter
            mock_adapter_factory.create_adapters_from_configs.return_value = {"test": mock_adapter}
            
            mock_processor = Mock()
            mock_processor_factory.create_processor.return_value = mock_processor
            
            mock_exporter = Mock()
            mock_export_factory.create_exporter.return_value = mock_exporter
            mock_export_factory.create_exporters_from_configs.return_value = {"test": mock_exporter}
            
            mock_scheduler = Mock()
            mock_scheduler_class.return_value = mock_scheduler
            
            # 执行初始化
            harvester.initialize()
            
            assert harvester._initialized is True
            
            # 验证调度器启动（如果启用）
            if harvester.config.scheduler.enabled:
                mock_scheduler.start.assert_called_once()
                
    def test_harvest_result_creation(self):
        """测试采集结果创建"""
        result = HarvestResult(
            success=True,
            data={"test": "data"},
            source="test_source",
            errors=[]
        )
        
        assert result.success is True
        assert result.data == {"test": "data"}
        assert result.source == "test_source"
        assert result.errors == []
        assert result.timestamp is not None
        
    def test_harvest_result_to_dict(self):
        """测试采集结果转换为字典"""
        result = HarvestResult(
            success=True,
            data=[1, 2, 3],
            source="test_source",
            metadata={"count": 3}
        )
        
        result_dict = result.to_dict()
        
        assert result_dict["success"] is True
        assert result_dict["source"] == "test_source"
        assert result_dict["data_count"] == 3
        assert result_dict["metadata"] == {"count": 3}
        
    def test_collect_method_with_mocked_adapter(self):
        """测试使用模拟适配器的收集方法"""
        harvester = DataHarvester()
        
        # 模拟适配器和处理器
        mock_adapter = Mock()
        mock_adapter.fetch.return_value = {"test": "data"}
        
        mock_processor = Mock()
        mock_processor.process.return_value.success = True
        mock_processor.process.return_value.data = {"processed": "data"}
        
        # 设置harvester的内部状态
        harvester._initialized = True
        harvester.adapters = {"test_source": mock_adapter}
        harvester.processors = mock_processor
        
        # 执行收集
        result = harvester.collect("test_source")
        
        assert isinstance(result, HarvestResult)
        assert result.success is True
        assert result.source == "test_source"
        
        # 验证适配器被调用
        mock_adapter.fetch.assert_called_once()
        
    def test_collect_method_with_nonexistent_source(self):
        """测试收集不存在的数据源"""
        harvester = DataHarvester()
        harvester._initialized = True
        harvester.adapters = {}  # 空适配器
        
        result = harvester.collect("nonexistent_source")
        
        assert result.success is False
        assert "未找到数据源适配器" in result.errors[0]
        
    def test_collect_all_method(self):
        """测试收集所有数据源"""
        harvester = DataHarvester()
        
        # 模拟多个适配器
        mock_adapter1 = Mock()
        mock_adapter1.fetch.return_value = {"data1": "value1"}
        
        mock_adapter2 = Mock()
        mock_adapter2.fetch.return_value = {"data2": "value2"}
        
        mock_processor = Mock()
        mock_processor.process.return_value.success = True
        mock_processor.process.return_value.data = {"processed": "data"}
        
        # 设置harvester的内部状态
        harvester._initialized = True
        harvester.adapters = {
            "source1": mock_adapter1,
            "source2": mock_adapter2
        }
        harvester.processors = mock_processor
        
        # 执行收集所有
        results = harvester.collect_all()
        
        assert isinstance(results, dict)
        assert len(results) == 2
        assert "source1" in results
        assert "source2" in results
        assert results["source1"].success is True
        assert results["source2"].success is True
        
    def test_export_method(self):
        """测试导出方法"""
        harvester = DataHarvester()
        
        # 模拟导出器
        mock_exporter = Mock()
        mock_exporter.export.return_value = True
        
        # 设置harvester的内部状态
        harvester._initialized = True
        harvester.exporters = {"csv_export": mock_exporter}
        
        test_data = {"test": "data"}
        
        # 执行导出
        success = harvester.export(test_data, "csv_export")
        
        assert success is True
        mock_exporter.export.assert_called_once_with(test_data)
        
    def test_export_method_with_nonexistent_exporter(self):
        """测试导出到不存在的导出器"""
        harvester = DataHarvester()
        harvester._initialized = True
        harvester.exporters = {}  # 空导出器
        
        success = harvester.export({"test": "data"}, "nonexistent_exporter")
        
        assert success is False
        
    def test_get_status_method(self):
        """测试获取状态方法"""
        harvester = DataHarvester()
        
        # 设置部分初始化的状态
        harvester._initialized = True
        harvester.adapters = {"adapter1": Mock()}
        harvester.processors = Mock(count=2)
        harvester.exporters = {"exporter1": Mock()}
        harvester.scheduler = Mock(running=True, task_count=3)
        
        status = harvester.get_status()
        
        assert status["initialized"] is True
        assert status["adapter_count"] == 1
        assert status["processor_count"] == 2
        assert status["exporter_count"] == 1
        assert status["scheduler_running"] is True
        assert status["active_tasks"] == 3
        
    def test_shutdown_method(self):
        """测试关闭方法"""
        harvester = DataHarvester()
        
        # 模拟调度器
        mock_scheduler = Mock()
        
        harvester.scheduler = mock_scheduler
        harvester._initialized = True
        
        # 执行关闭
        harvester.shutdown()
        
        # 验证调度器关闭被调用
        mock_scheduler.shutdown.assert_called_once()
        assert harvester._initialized is False