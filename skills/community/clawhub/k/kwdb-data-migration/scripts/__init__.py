"""
scripts package for KWDB data migration.

This package contains all necessary scripts for performing heterogeneous
database migration to KaiwuDB via KDTS REST API.

Modules:
- api_client.py: KDTS REST API client
- data_source.py: Data source configuration management
- migration_task.py: Migration workflow orchestration
- config_validator.py: Configuration validation
- error_handler.py: Error code handling
- config.py: Multi-layer configuration management
"""

from .api_client import (KDTSClient, build_source_config, build_target_config,
                         build_table_mapping, build_influxdb_mapping,
                         build_added_column, build_manual_metadata,
                         mark_time_series_columns)
from .data_source import (
    DataSourceManager,
    Engine,
    SourceType,
    SourceCapability,
)
from .migration_task import (
    MigrationWorkflowManager,
    MigrationWorkflow,
    MigrationStep,
    MigrationStatus,
    create_workflow_manager,
)
from .config_validator import ConfigValidator
from .error_handler import ErrorHandler
from .config import (
    KDTSConfig,
    resolve_base_url,
    get_environment_info,
)

__all__ = [
    # api_client
    "KDTSClient",
    "build_source_config",
    "build_target_config",
    "build_table_mapping",
    "build_influxdb_mapping",
    "build_added_column",
    "build_manual_metadata",
    "mark_time_series_columns",
    # data_source
    "DataSourceManager",
    "Engine",
    "SourceType",
    "SourceCapability",
    # migration_task
    "MigrationWorkflowManager",
    "MigrationWorkflow",
    "MigrationStep",
    "MigrationStatus",
    "create_workflow_manager",
    # config_validator
    "ConfigValidator",
    # error_handler
    "ErrorHandler",
    # config
    "KDTSConfig",
    "resolve_base_url",
    "get_environment_info",
]

__version__ = "1.0.0"
