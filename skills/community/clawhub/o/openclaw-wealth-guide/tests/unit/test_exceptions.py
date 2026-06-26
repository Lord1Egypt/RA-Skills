"""
异常模块测试
"""

import pytest

from src.data_harvester.exceptions import (
    DataHarvesterError,
    ConfigurationError,
    AdapterError,
    FetchError,
    ProcessingError,
    ExportError,
    SchedulerError,
    ValidationError,
    ResourceError,
    AuthenticationError,
    RateLimitError,
    TimeoutError,
    RetryExhaustedError,
    DataQualityError,
    IntegrationError
)


class TestExceptions:
    """异常测试类"""
    
    def test_base_exception(self):
        """测试基础异常"""
        error = DataHarvesterError("Test error")
        assert str(error) == "Test error"
        
    def test_configuration_error(self):
        """测试配置错误"""
        error = ConfigurationError("Config error")
        assert isinstance(error, DataHarvesterError)
        assert str(error) == "Config error"
        
    def test_adapter_error(self):
        """测试适配器错误"""
        error = AdapterError("Adapter error")
        assert isinstance(error, DataHarvesterError)
        assert str(error) == "Adapter error"
        
    def test_fetch_error(self):
        """测试获取错误"""
        error = FetchError("Fetch error")
        assert isinstance(error, AdapterError)
        assert isinstance(error, DataHarvesterError)
        assert str(error) == "Fetch error"
        
    def test_processing_error(self):
        """测试处理错误"""
        error = ProcessingError("Processing error")
        assert isinstance(error, DataHarvesterError)
        assert str(error) == "Processing error"
        
    def test_export_error(self):
        """测试导出错误"""
        error = ExportError("Export error")
        assert isinstance(error, DataHarvesterError)
        assert str(error) == "Export error"
        
    def test_scheduler_error(self):
        """测试调度器错误"""
        error = SchedulerError("Scheduler error")
        assert isinstance(error, DataHarvesterError)
        assert str(error) == "Scheduler error"
        
    def test_validation_error(self):
        """测试验证错误"""
        error = ValidationError("Validation error")
        assert isinstance(error, DataHarvesterError)
        assert str(error) == "Validation error"
        
    def test_resource_error(self):
        """测试资源错误"""
        error = ResourceError("Resource error")
        assert isinstance(error, DataHarvesterError)
        assert str(error) == "Resource error"
        
    def test_authentication_error(self):
        """测试认证错误"""
        error = AuthenticationError("Authentication error")
        assert isinstance(error, DataHarvesterError)
        assert str(error) == "Authentication error"
        
    def test_rate_limit_error(self):
        """测试速率限制错误"""
        error = RateLimitError("Rate limit error")
        assert isinstance(error, DataHarvesterError)
        assert str(error) == "Rate limit error"
        
    def test_timeout_error(self):
        """测试超时错误"""
        error = TimeoutError("Timeout error")
        assert isinstance(error, DataHarvesterError)
        assert str(error) == "Timeout error"
        
    def test_retry_exhausted_error(self):
        """测试重试耗尽错误"""
        previous_error = Exception("Previous error")
        error = RetryExhaustedError("Retry exhausted", previous_error)
        
        assert isinstance(error, DataHarvesterError)
        assert str(error) == "Retry exhausted"
        assert error.last_exception == previous_error
        
    def test_data_quality_error(self):
        """测试数据质量错误"""
        error = DataQualityError("Data quality error", 0.5)
        
        assert isinstance(error, DataHarvesterError)
        assert str(error) == "Data quality error"
        assert error.quality_score == 0.5
        
    def test_integration_error(self):
        """测试集成错误"""
        error = IntegrationError("Integration error")
        assert isinstance(error, DataHarvesterError)
        assert str(error) == "Integration error"
        
    def test_exception_chaining(self):
        """测试异常链"""
        try:
            try:
                raise ValueError("Inner error")
            except ValueError as e:
                raise ConfigurationError("Configuration failed") from e
        except ConfigurationError as e:
            assert str(e) == "Configuration failed"
            assert e.__cause__ is not None
            assert isinstance(e.__cause__, ValueError)
            assert str(e.__cause__) == "Inner error"