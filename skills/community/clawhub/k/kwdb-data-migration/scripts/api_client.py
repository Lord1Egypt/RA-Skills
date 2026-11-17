"""
api_client.py - Unified KDTS Server API Client

Provides complete REST API interaction with KDTS Server for heterogeneous database migration.
All 10 API endpoints are wrapped with request building, response parsing, and error handling.

Configuration Priority (highest to lowest):
1. Environment variables: KDTS_BASE_URL or KDTS_HOST + KDTS_PORT
2. Explicit parameters passed to constructor
3. Config file: kdts_config.json (in script dir or CWD)
4. Default: http://127.0.0.1:8989

Usage:
    python api_client.py <action> [options]

Actions:
    test_connection     Test data source connectivity
    list_databases      List databases on source
    read_metadata       Read source metadata (tables, columns, etc.)
    preview_ddl         Preview DDL for target KaiwuDB
    execute_ddl         Execute DDL on target KaiwuDB
    build_migration     Build DataX migration script
    execute_migration   Execute built migration scripts
    query_status        Query migration task status
    control_task        Kill or query running task
"""

import requests
import json
import sys
import time
import logging
from typing import Dict, List, Optional, Any

# Handle imports for both package and direct script usage
try:
    from .config import KDTSConfig, resolve_base_url, get_environment_info
    from .data_source import DataSourceManager
except ImportError:
    from config import KDTSConfig, resolve_base_url, get_environment_info
    from data_source import DataSourceManager

logger = logging.getLogger(__name__)


class KDTSClient:
    """
    Unified client for KDTS Server REST API.

    Handles all API interactions including request building,
    response parsing, timeout management, and error code conversion.
    """

    def __init__(self, base_url: Optional[str] = None,
                 timeout: Optional[int] = None,
                 connect_timeout: Optional[int] = None,
                 api_prefix: Optional[str] = None,
                 config_file: Optional[str] = None):
        """
        Initialize KDTS API client with multi-layer configuration.

        Configuration Priority:
        1. Environment variables (KDTS_BASE_URL, KDTS_HOST, etc.)
        2. Explicit constructor parameters
        3. Config file (kdts_config.json)
        4. Default values (127.0.0.1:8989)

        Args:
            base_url: Explicit KDTS Server URL (highest priority)
                     If None, checks environment then config file then default.
            timeout: Read timeout in seconds (default: from config or 30)
            connect_timeout: Connection timeout in seconds (default: from config or 5)
            api_prefix: API path prefix (default: from config or /kdts/api/v1)
            config_file: Optional path to config file

        Example:
            # Use environment variables
            export KDTS_BASE_URL="http://10.0.0.1:8989"
            client = KDTSClient()

            # Or explicit configuration
            client = KDTSClient(base_url="http://127.0.0.1:8989")

            # Or with config file
            client = KDTSClient(config_file="/path/to/kdts_config.json")
        """
        # Initialize configuration manager
        config_manager = KDTSConfig(config_file)

        # Resolve base_url with priority chain
        self.base_url = config_manager.get_base_url(base_url).rstrip('/')

        # Resolve other parameters
        self.api_prefix = api_prefix or config_manager.get_api_prefix()
        self.timeout = timeout or config_manager.get_timeout()
        self.connect_timeout = connect_timeout or config_manager.get_connect_timeout()

        # Log configuration source
        config_source = config_manager.detect_config_source()
        logger.info(f"KDTSClient initialized: base_url={self.base_url}, "
                     f"source={config_source}")

        # Initialize HTTP session
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})

    def _build_url(self, endpoint: str) -> str:
        """Build full API URL from endpoint path."""
        return f"{self.base_url}{self.api_prefix}{endpoint}"

    def _request(self, method: str, endpoint: str,
                 data: Optional[Dict] = None,
                 params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Send HTTP request and parse response.

        Args:
            method: HTTP method (GET, POST)
            endpoint: API endpoint path (e.g., /health, /datasource/validate)
            data: Request body dict (for POST)
            params: Query params dict (for GET)

        Returns:
            Parsed response dict with format: {code, message, timestamp, data}

        Raises:
            requests.exceptions.RequestException: Network errors
        """
        url = self._build_url(endpoint)

        try:
            if method == 'GET':
                response = self.session.get(
                    url, params=params,
                    timeout=(self.connect_timeout, self.timeout)
                )
            elif method == 'POST':
                response = self.session.post(
                    url, json=data,
                    timeout=(self.connect_timeout, self.timeout)
                )
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            # Handle HTTP-level errors (503 for resource exhaustion)
            if response.status_code == 503:
                retry_after = response.headers.get('Retry-After', '60')
                return {
                    "code": 5001,
                    "message": f"Service unavailable. Retry after {retry_after} seconds.",
                    "timestamp": int(time.time() * 1000),
                    "data": None
                }

            response.raise_for_status()
            return response.json()

        except requests.exceptions.ConnectionError as e:
            return {
                "code": 2001,
                "message": f"Connection failed: {str(e)}",
                "timestamp": int(time.time() * 1000),
                "data": None
            }
        except requests.exceptions.Timeout as e:
            return {
                "code": 4003,
                "message": f"Request timeout: {str(e)}",
                "timestamp": int(time.time() * 1000),
                "data": None
            }
        except json.JSONDecodeError as e:
            return {
                "code": 1005,
                "message": f"Response parse error: {str(e)}",
                "timestamp": int(time.time() * 1000),
                "data": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "code": 9999,
                "message": f"Request error: {str(e)}",
                "timestamp": int(time.time() * 1000),
                "data": None
            }

    # ==================== Basic API ====================

    def health_check(self) -> Dict[str, Any]:
        """
        Check KDTS Server health status.

        Returns:
            Response dict with status info.
        """
        return self._request('GET', '/health')

    # ==================== DataSource API ====================

    def test_connection(self, source_config: Dict,
                        is_target: bool = False) -> Dict[str, Any]:
        """
        Test data source connectivity.

        Args:
            source_config: DataSource request dict with engine, type, host, port, username, password
            is_target: If True, marks this as target-side validation

        Returns:
            Validation result dict. On success, data contains 'SUCCEED'.
            NOTE: KDTS returns code=0 even for FAILED validations — the failure text
            is in the `data` field. This method normalizes such responses to
            code=2001 (with the failure message), so callers can rely on `code == 0` meaning success.
        """
        request = source_config.copy()
        request['isTarget'] = is_target
        result = self._request('POST', '/datasource/validate', data=request)
        # Normalize: code=0 with non-SUCCEED data means connection failure (KDTS behavior)
        data = result.get('data')
        if result.get('code') == 0 and not (isinstance(data, str) and data.upper() == 'SUCCEED'):
            result['code'] = 2001
            if not result.get('message'):
                # data may already start with "Connection failed: ..." (e.g. TDengine)
                prefix = "Connection failed: "
                result['message'] = data if str(data).startswith(prefix) else prefix + str(data)
        return result

    def list_databases(self, source_config: Dict) -> Dict[str, Any]:
        """
        List all databases on source.

        Args:
            source_config: DataSource request dict

        Returns:
            Response with data containing list of database names.
        """
        return self._request('POST', '/datasource/databases', data=source_config)

    def read_metadata(self, source_config: Dict,
                      metadata_options: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Read complete source metadata (tables, columns, constraints, etc.).

        Args:
            source_config: DataSource request dict (must include dbName)
            metadata_options: Optional dict with keys (MetaData fields):
                - enable (bool): Enable metadata extraction (default: True)
                - autoDdl (bool): Auto-generate DDL (default: True)
                - primaryKey (bool): Include primary keys (default: True)
                - constraint (bool): Include constraints (default: True)
                - comment (bool): Include column comments (default: True)
                - index (bool): Include indexes (default: True)
                - view (bool): Include views (default: False)

        Returns:
            Response with data containing Database object (tables, columns, etc.)
        """
        # Default metadata options matching MetaData.java
        default_metadata = {
            "enable": True,
            "autoDdl": True,
            "primaryKey": True,
            "constraint": True,
            "comment": True,
            "index": True,
            "view": False
        }

        # Merge with user-provided options
        metadata = {**default_metadata, **(metadata_options or {})}

        request = {
            "source": source_config,
            "metadata": metadata
        }
        return self._request('POST', '/datasource/metadata', data=request)

    # ==================== Metadata API ====================

    def preview_ddl(self, target_config: Dict,
                    source_db: Dict,
                    metadata: Optional[Dict] = None,
                    is_time_series: bool = False) -> Dict[str, Any]:
        """
        Preview generated DDL for target KaiwuDB.

        Args:
            target_config: Target DataSource request dict (must be KAIWUDB)
            source_db: Complete Database object from read_metadata response
                Structure: {
                    "type": "MYSQL",
                    "name": "source_db",
                    "encoding": "UTF-8",
                    "tableMap": { "tableName": { ... Table object ... } },
                    "viewMap": { "viewName": { ... View object ... } }
                }
            metadata: Optional MetaData config dict (same as read_metadata):
                {
                    "primaryKey": True,
                    "constraint": True,
                    "comment": True,
                    "index": True,
                    "view": False
                }
            is_time_series: If True, request time series table DDL (default: False).
                The request field is "isTimeSeries".
                For time-series DDL to be generated, the source Database columns must
                carry tag marks: "isTag" and the time column must be marked "isTs": true.
                KDTS then generates CREATE TS DATABASE + CREATE TABLE ... TAGS (...) PRIMARY TAGS (...).
                Tables WITHOUT any tag-marked column are SKIPPED (no DDL emitted).

        Returns:
            Response with data containing DdlScript:
                {
                    "dbName": "SOURCE_DB",
                    "createDb": "CREATE TS DATABASE ...",  (is_time_series=True)
                    "table": { "tableName": "CREATE TABLE xxx" },
                    "view": { "viewName": "CREATE VIEW xxx" }
                }
        """
        # Default metadata if not provided
        default_metadata = {
            "primaryKey": True,
            "constraint": True,
            "comment": True,
            "index": True,
            "view": False
        }

        request = {
            "target": target_config,
            "sourceDb": source_db,
            "metadata": metadata or default_metadata,
            "isTimeSeries": is_time_series
        }
        return self._request('POST', '/metadata/preview', data=request)

    def execute_ddl(self, target_config: Dict, ddl_script: Dict, auto_ddl: bool = True) -> Dict[str, Any]:
        """
        Execute DDL on target KaiwuDB.

        Args:
            target_config: Target DataSource request dict
            ddl_script: DdlScript from preview_ddl response data
                Structure: {
                    "dbName": "SOURCE_DB",
                    "createDb": "CREATE DATABASE ...",
                    "table": { "tableName": "CREATE TABLE xxx" },
                    "view": { "viewName": "CREATE VIEW xxx" }
                }
            auto_ddl: If True, auto-create database and tables (default: True)

        Returns:
            Response with data containing absolute path of SQL execution log file.
        """
        request = {
            "target": target_config,
            "ddlScript": ddl_script,
            "autoDdl": auto_ddl
        }
        return self._request('POST', '/metadata/execute', data=request)

    # ==================== DataX API ====================

    # Default DataX configuration for data migration
    DEFAULT_DATAX_CONFIG = {
        "batchSize": 1000,
        "core": {
            "transport": {
                "channel": {
                    "speed": {
                        "byte": 1048576,
                        "record": 1000
                    }
                }
            }
        },
        "enable": True,
        "fetchSize": 1000,
        "setting": {
            "errorLimit": {
                "percentage": 0.02
            },
            "speed": {
                "channel": 4
            }
        }
    }

    def build_migration(self, source: Dict, target: Dict,
                        tables: Optional[List[Dict]] = None,
                        data_config: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Build DataX migration script.

        Args:
            source: Source DataSource request dict
            target: Target DataSource request dict (type must be KAIWUDB)
            tables: Optional list of TableMapping dicts.
                Empty or None = auto-discover all tables (full migration)
                Each mapping has 'source' and 'target' keys.
            data_config: Optional data migration settings dict.
                If not provided, uses DEFAULT_DATAX_CONFIG with:
                - enable (bool): Enable data migration (default: True)
                - fetchSize (int): Rows per fetch from source (default: 1000)
                - batchSize (int): Rows per batch to target (default: 1000)
                - core.transport.channel.speed.byte: Bytes per second (default: 1048576 = 1MB)
                - core.transport.channel.speed.record: Records per second (default: 1000)
                - setting.speed.channel: Number of parallel channels (default: 4)
                - setting.errorLimit.percentage: Error tolerance percentage (default: 0.02 = 2%)

        Returns:
            Response with data containing list of generated script file names.

        Note: The complete data config structure is required for successful DataX execution.
        Missing core or setting fields will cause migration failures.
        """
        request = {
            "source": source,
            "target": target,
            "tables": tables or [],
            "data": data_config or self.DEFAULT_DATAX_CONFIG
        }
        
        # Validate the configuration before sending
        errors = self.validate_migration_config(request)
        if errors:
            raise ValueError(f"Invalid migration configuration: {'; '.join(errors)}")
        
        return self._request('POST', '/datax/build', data=request)
    
    @classmethod
    def validate_migration_config(cls, config: Dict[str, Any]) -> List[str]:
        """
        Validate migration configuration for common errors.
        
        Args:
            config: Full migration request configuration with source, target, tables, data fields
            
        Returns:
            List of error messages (empty if configuration is valid)
            
        Common validation checks:
        - DataX speed configuration constraints (based on DataX official documentation)
        - Mutual exclusion of where and querySql
        - Mutual exclusion of column and columns
        - Recommended: splitPk should not be used with querySql
        - Required fields in data configuration (core and setting)
        
        DataX Speed Configuration Rules:
        1. core.transport.channel.speed (single channel level):
           - Can have 'byte' and/or 'record' (not mutually exclusive!)
           - Should NOT have 'channel' (only in setting.speed)
        
        2. setting.speed (global level):
           - 'byte' and 'record' can be configured simultaneously
           - If 'byte' is configured, core.transport.channel.speed.byte MUST be configured
           - If 'record' is configured, core.transport.channel.speed.record MUST be configured
           - If 'byte' or 'record' is configured, 'channel' is IGNORED (auto-calculated)
           - If only 'channel' is configured, it's used directly
        """
        errors = []
        
        # Validate data configuration
        data = config.get('data', {})
        if not data:
            errors.append("Missing 'data' configuration")
            return errors
        
        # Check enable field
        if 'enable' not in data:
            errors.append("Missing 'data.enable' field")
        
        # Check core configuration (REQUIRED)
        core = data.get('core', {})
        if not core:
            errors.append("Missing 'data.core' configuration (REQUIRED for DataX)")
            return errors
        
        # Check core.transport.channel.speed
        transport = core.get('transport', {})
        channel = transport.get('channel', {})
        core_speed = channel.get('speed', {})
        
        if not core_speed:
            errors.append("Missing 'data.core.transport.channel.speed' configuration")
        else:
            # core.transport.channel.speed can have 'byte' and/or 'record' (not mutually exclusive)
            # But should NOT have 'channel' parameter
            if 'channel' in core_speed:
                errors.append(
                    "'core.transport.channel.speed' should NOT have 'channel' parameter. "
                    "'channel' should only be configured in 'setting.speed'."
                )
        
        # Check setting configuration (REQUIRED)
        setting = data.get('setting', {})
        if not setting:
            errors.append("Missing 'data.setting' configuration (REQUIRED for DataX)")
            return errors
        
        setting_speed = setting.get('speed', {})
        
        if setting_speed:
            # Get core speed values for cross-validation
            core_byte = core_speed.get('byte') if core_speed else None
            core_record = core_speed.get('record') if core_speed else None
            
            setting_byte = setting_speed.get('byte')
            setting_record = setting_speed.get('record')
            setting_channel = setting_speed.get('channel')
            
            # Validate: if setting.speed.byte is configured, core.transport.channel.speed.byte MUST be configured
            if setting_byte is not None:
                if core_byte is None:
                    errors.append(
                        "If 'setting.speed.byte' is configured, 'core.transport.channel.speed.byte' "
                        "MUST also be configured (required for channel count calculation)."
                    )
                elif core_byte <= 0:
                    errors.append(
                        "'core.transport.channel.speed.byte' must be > 0 when 'setting.speed.byte' is configured."
                    )
            
            # Validate: if setting.speed.record is configured, core.transport.channel.speed.record MUST be configured
            if setting_record is not None:
                if core_record is None:
                    errors.append(
                        "If 'setting.speed.record' is configured, 'core.transport.channel.speed.record' "
                        "MUST also be configured (required for channel count calculation)."
                    )
                elif core_record <= 0:
                    errors.append(
                        "'core.transport.channel.speed.record' must be > 0 when 'setting.speed.record' is configured."
                    )
            
            # Validate: if channel is auto-calculated from byte/record, warn about 'channel' being ignored
            if (setting_byte is not None or setting_record is not None) and setting_channel is not None:
                errors.append(
                    "'setting.speed.channel' will be IGNORED when 'setting.speed.byte' or 'setting.speed.record' "
                    "is configured. Channel count is auto-calculated. Remove 'setting.speed.channel' to avoid confusion."
                )
        
        # Validate table configurations
        tables = config.get('tables', [])
        for i, table in enumerate(tables):
            source_table = table.get('source', {})
            if source_table:
                # Validate mutual exclusion of where and querySql
                has_where = 'where' in source_table and source_table.get('where')
                has_query_sql = 'querySql' in source_table and source_table.get('querySql')
                
                if has_where and has_query_sql:
                    errors.append(
                        f"Table {i + 1}: 'where' and 'querySql' are MUTUALLY EXCLUSIVE - "
                        f"use only one"
                    )
                
                # Validate mutual exclusion of column and columns
                has_column = 'column' in source_table and source_table.get('column')
                has_columns = 'columns' in source_table and source_table.get('columns')
                
                if has_column and has_columns:
                    errors.append(
                        f"Table {i + 1}: 'column' and 'columns' are MUTUALLY EXCLUSIVE - "
                        f"use only one"
                    )
                
                # Validate splitPk should not be used with querySql (warning)
                has_split_pk = 'splitPk' in source_table and source_table.get('splitPk')
                if has_split_pk and has_query_sql:
                    errors.append(
                        f"Table {i + 1}: 'splitPk' and 'querySql' should not be used together "
                        f"(splitPk requires table structure which querySql may not have)"
                    )
        
        return errors
    
    @classmethod
    def validate_data_config(cls, data_config: Dict[str, Any]) -> List[str]:
        """
        Validate only the data configuration section.
        
        Args:
            data_config: The 'data' section of migration configuration
            
        Returns:
            List of error messages (empty if valid)
        """
        return cls.validate_migration_config({'data': data_config})

    def execute_migration(self, script_names: List[str]) -> Dict[str, Any]:
        """
        Execute built migration scripts.

        Args:
            script_names: List of script file names (from build_migration response)

        Returns:
            Response with data containing list of log file paths.

        Note: KDTS API expects the request body to be a direct list of strings,
        not an object with a scriptNames field.
        """
        # Directly send the list as request body (KDTS expects List<String>)
        return self._request('POST', '/datax/execute', data=script_names)

    def query_status(self, script_name: str) -> Dict[str, Any]:
        """
        Query migration task status.

        Args:
            script_name: Migration script file name

        Returns:
            Response with data containing JobStatusResponse:
                - status: JobStatus enum (SUBMITTED, RUNNING, SUCCEEDED, FAILED, KILLED, UNKNOWN)
                - progress: Progress percentage (0-100)
                - message: Status message
        """
        return self._request('GET', '/datax/status', params={'scriptName': script_name})

    def control_task(self, script_name: str, action: str = "KILL") -> Dict[str, Any]:
        """
        Control running migration task.

        Args:
            script_name: Migration script file name
            action: Control action:
                - "QUERY": Query current status
                - "KILL": Kill running task (use with caution!)

        Returns:
            Response with data containing JobStatus after control action.
        """
        request = {
            "scriptName": script_name,
            "action": action
        }
        return self._request('POST', '/datax/control', data=request)


def build_source_config(source_type: str,
                        host: str, port: int,
                        username: str, password: str,
                        engine: str,
                        db_name: Optional[str] = None,
                        url: Optional[str] = None) -> Dict[str, Any]:
    """
    Helper function to build DataSource request dict.
    
    Note: engine is REQUIRED for all source configs per KDTS API specification.
    Use SourceType.get_engine(source_type) to determine the correct engine value.

    Args:
        source_type: Source type (MYSQL, ORACLE, KAIWUDB, etc.)
        host: Hostname or IP
        port: Port number
        username: Database username
        password: Database password
        engine: REQUIRED - Engine type (RELATIONAL or TIMESERIES)
        db_name: Optional database name
        url: Optional full JDBC URL (overrides host:port)

    Returns:
        DataSource request dict ready for API calls.

    Raises:
        ValueError: If engine is not 'RELATIONAL' or 'TIMESERIES'
    """
    # Validate engine value
    if engine not in ('RELATIONAL', 'TIMESERIES'):
        raise ValueError(f"engine must be 'RELATIONAL' or 'TIMESERIES', got '{engine}'")
    
    config = {
        "engine": engine,
        "type": source_type,
        "host": host,
        "port": port,
        "username": username,
        "password": password
    }

    if url:
        config["url"] = url
    if db_name:
        config["dbName"] = db_name

    return config


def build_target_config(engine: str,
                        host: str, port: int = 26257,
                        username: str = "root", password: str = "",
                        db_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Helper function to build KAIWUDB target config.
    
    Note: engine is REQUIRED for target config (RELATIONAL or TIMESERIES).

    Args:
        engine: Required engine type (RELATIONAL or TIMESERIES)
        host: KAIWUDB host
        port: KAIWUDB port (default: 26257)
        username: KAIWUDB username (default: root)
        password: KAIWUDB password
        db_name: Target database name

    Returns:
        Target DataSource request dict ready for API calls.
    """
    config = {
        "engine": engine,
        "type": "KAIWUDB",
        "host": host,
        "port": port,
        "username": username,
        "password": password,
        "isTarget": True
    }

    if db_name:
        config["dbName"] = db_name

    return config


def build_table_mapping(source_type: str, source_table: str,
                        target_table: Optional[str] = None,
                        columns: Optional[str] = None,
                        write_mode: str = "insert",
                        source_source_type: Optional[str] = None,
                        where: Optional[str] = None,
                        pre_sql: Optional[List[str]] = None,
                        post_sql: Optional[List[str]] = None,
                        target_columns: Optional[str] = None) -> Dict[str, Any]:
    """
    Helper function to build table mapping for migration.

    Args:
        source_type: KDTS source type (for determining sourceSourceType)
        source_table: Source table name (for INFLUXDB this is the measurement name,
            for MONGODB the collection name)
        target_table: Target table name (default: same as source)
        columns: Source column selection string (e.g., "col1,col2,col3").
            SQL expressions are allowed for RDBMS sources, e.g. "...,1 as t1" — when
            using expressions, pass the real target column names via target_columns
        write_mode: Write mode for target KaiwuDB (insert, replace, etc.)
        source_source_type: Override sourceSourceType (auto-detected if None)
        where: WHERE filter for table-based sources (RDBMS/KAIWUDB/TDENGINE/OPENTSDB),
            e.g. "ts >= '2025-04-01 00:00:00' and ts <= '2025-06-01 00:00:00'".
            Ignored for INFLUXDB (use time range) / MONGODB
        pre_sql: SQL statements executed on the target before writing (e.g. drop/create table)
        post_sql: SQL statements executed on the target after writing
        target_columns: Target column names (default: same as `columns`). REQUIRED
            when source `columns` contain SQL expressions — the target must use the
            real column names (e.g. source "...,1 as t1" → target "...,t1"),
            otherwise DataX cannot find the target column

    Returns:
        TableMapping dict ready for build_migration.

    Note: the source table identifier field differs per source type
    — `table` for RDBMS/KAIWUDB/TDENGINE/OPENTSDB, `measurement` for INFLUXDB,
    `collectionName` for MONGODB. Using the wrong field (e.g. `table` for InfluxDB)
    leaves the field null on the server and the migration fails at execution.
    FTP/HDFS are file sources (path-based, no table) — not supported here.
    """
    # Auto-detect sourceSourceType from KDTS source type
    if not source_source_type:
        source_source_type_map = {
            "MYSQL": "RDBMS", "ORACLE": "RDBMS", "POSTGRESQL": "RDBMS",
            "SQLSERVER": "RDBMS", "CLICKHOUSE": "RDBMS",
            "KAIWUDB": "KAIWUDB",
            "TDENGINE2X": "TDENGINE", "TDENGINE3X": "TDENGINE",
            "INFLUXDB1X": "INFLUXDB", "INFLUXDB2X": "INFLUXDB",
            "OPENTSDB": "OPENTSDB",
            "MONGODB": "MONGODB",
            "FTP": "FTP", "SFTP": "FTP",
            "HDFS": "HDFS"
        }
        source_source_type = source_source_type_map.get(source_type.upper(), "RDBMS")

    # Source table identifier field per source type (from KDTS source DTOs)
    source_field_map = {
        "RDBMS": "table",
        "KAIWUDB": "table",
        "TDENGINE": "table",
        "OPENTSDB": "table",
        "INFLUXDB": "measurement",
        "MONGODB": "collectionName",
    }
    source_field = source_field_map.get(source_source_type)
    if source_field is None:
        raise ValueError(
            f"Source type '{source_type}' is a file-based source (FTP/HDFS) with no table "
            f"identifier — build its mapping manually (path-based) instead of using "
            f"build_table_mapping()."
        )

    # where filter is supported by table-based sources (RDBMS/KAIWUDB/TDENGINE/OPENTSDB),
    # NOT by INFLUXDB (time range) or MONGODB (query)
    source_map = {
        "sourceType": source_source_type,
        source_field: source_table,
        "column": columns or "*"
    }
    if where is not None and source_source_type in ("RDBMS", "KAIWUDB", "TDENGINE", "OPENTSDB"):
        source_map["where"] = where

    target_map = {
        "sourceType": "KAIWUDB",
        "table": target_table or source_table,
        "column": target_columns or columns or "*",
        "writeMode": write_mode
    }
    if pre_sql is not None:
        target_map["preSql"] = pre_sql if isinstance(pre_sql, list) else [pre_sql]
    if post_sql is not None:
        target_map["postSql"] = post_sql if isinstance(post_sql, list) else [post_sql]

    return {"source": source_map, "target": target_map}


def build_manual_metadata(source_type: str, db_name: str, table_name: str,
                          columns: List[Dict[str, Any]],
                          schema_name: str = "default") -> Dict[str, Any]:
    """
    Build a Database object MANUALLY for sources without KDTS metadata support.

    KDTS `preview_ddl` generates DDL from the passed-in Database object, NOT from
    the source connection — so a table-based source with a known structure can
    still get DDL generated this way.

    **IMPORTANT — the table structure MUST come from the USER** (source CREATE
    TABLE DDL or a column list the user provides).
    NEVER guess the structure — production schemas are arbitrary.

    Args:
        source_type: KDTS source type
        db_name: Database name (used as the DDL database name)
        table_name: Table name
        columns: List of column dicts from the USER-PROVIDED structure, each with
            at least: {"columnName": str, "sourceColumnType": str}
            (optional: sourceColumnName, nullAble, comment, ...)
        schema_name: Source schema (default: "default")

    Returns:
        Database object ready for preview_ddl() / execute_ddl().
    """
    cols = []
    for i, c in enumerate(columns, 1):
        cols.append({
            "dbType": source_type, "schemaName": schema_name, "tableName": table_name,
            "sourceColumnName": c.get("sourceColumnName", c["columnName"]),
            "columnName": c["columnName"],
            "sourceColumnType": c.get("sourceColumnType", ""),
            "columnType": c.get("sourceColumnType", ""),
            "columnOrder": i, "strLength": None, "precision": None, "scale": None,
            "nullAble": c.get("nullAble", True), "comment": c.get("comment", ""),
            "extra": "", "columnKey": "", "finalConvertDataType": None,
            "isChecked": True, "isTs": False, "isTag": False, "isPrimaryTag": False,
        })
    return {
        "type": source_type, "name": db_name, "encoding": "UTF-8",
        "interval": None, "retentions": None, "comment": None,
        "tableMap": {
            table_name: {
                "schemaName": schema_name, "sourceTableName": table_name,
                "tableName": table_name, "tableCollation": None, "tableComment": None,
                "columns": cols, "primaryKey": None, "constraint": [],
                "indexes": [], "source": None,
            }
        },
        "viewMap": {},
    }


def build_added_column(column_name: str, default_value: Any,
                       source_type: str = "MYSQL",
                       is_tag: bool = False,
                       is_primary_tag: bool = False) -> Dict[str, Any]:
    """
    Build a NEW column definition to append to a source Database table, for sources
    that lack the column (e.g. adding a `t1` primary tag to an Oracle table).
    Applies to ALL source types (RDBMS, TDengine, InfluxDB, KaiwuDB).

    The KaiwuDB type is derived from the DEFAULT VALUE:
    - int default      → INT4 (INT8 for InfluxDB)   (eligible for PRIMARY TAG)
    - str default      → VARCHAR (eligible for PRIMARY TAG)
    - float default    → FLOAT4/FLOAT8 (ordinary TAG ONLY — float types are demoted
      by KDTS and CANNOT be primary tags; error 3006 if no eligible primary tag remains)
    - bool default     → BOOL   (eligible for PRIMARY TAG)

    IMPORTANT: the source column type must have an EXACT KDTS mapping for the source
    type (e.g. Oracle `NUMBER(10,0)` → INT4, NOT `NUMBER(1,0)` which falls back to
    `NUMBER` → FLOAT and demotes the primary tag). Selected automatically per source.
    NOTE: KAIWUDB has no type-mapping rules in KDTS — the type may be rewritten by
    applyColumnTypeMapping; verify the generated DDL.

    Args:
        column_name: New column name (e.g. "t1")
        default_value: Default value used in the SQL expression column
            (e.g. `1 as t1` in the mapping's source columns)
        source_type: KDTS source type (MYSQL, ORACLE, POSTGRESQL, SQLSERVER,
            CLICKHOUSE, TDENGINE2X/3X, INFLUXDB1X/2X, KAIWUDB)
        is_tag: Mark as tag (isTag=true)
        is_primary_tag: Mark as primary tag (isPrimaryTag=true) — requires an
            int/str/bool default; float defaults are FORCED to ordinary tags

    Returns:
        Column dict ready to append to table["columns"].
    """
    if is_primary_tag and isinstance(default_value, float):
        is_primary_tag = False
        is_tag = True   # float can only be an ordinary tag

    # Source column types with EXACT KDTS mappings per source type
    int_src_map = {
        "MYSQL": "INT", "ORACLE": "NUMBER(10,0)", "POSTGRESQL": "INTEGER",
        "SQLSERVER": "INT", "CLICKHOUSE": "INT32",
        "TDENGINE2X": "INT", "TDENGINE3X": "INT",
        "INFLUXDB1X": "INTEGER", "INFLUXDB2X": "INTEGER",
        "KAIWUDB": "INT4",
    }
    src_upper = (source_type or "").upper()

    if isinstance(default_value, bool):
        mapped, src_type = "BOOL", "BOOLEAN"
    elif isinstance(default_value, int):
        # InfluxDB INTEGER maps to INT8 (no INT4 in its mapping rules)
        mapped = "INT8" if src_upper.startswith("INFLUXDB") else "INT4"
        src_type = int_src_map.get(src_upper, "INT")
    elif isinstance(default_value, float):
        mapped, src_type = "FLOAT4", "FLOAT"
    else:
        mapped, src_type = "VARCHAR", "VARCHAR"

    return {
        "dbType": "RDBMS", "schemaName": "", "tableName": "",
        "sourceColumnName": column_name, "columnName": column_name,
        "sourceColumnType": src_type, "columnType": mapped,
        "columnOrder": 999, "strLength": None, "precision": None, "scale": None,
        "nullAble": not is_primary_tag,   # primary tags must be NOT NULL
        "comment": "", "extra": "", "columnKey": "",
        "finalConvertDataType": mapped, "isChecked": True,
        "isTs": False, "isTag": is_tag, "isPrimaryTag": is_primary_tag,
    }


def build_influxdb_mapping(source_db: Dict, measurement: str,
                           target_table: Optional[str] = None,
                           write_mode: str = "insert",
                           begin_datetime: Optional[str] = None,
                           end_datetime: Optional[str] = None,
                           split_interval_s: int = 86400,
                           read_timeout: int = 0,
                           connect_timeout: int = 0) -> Dict[str, Any]:
    """
    Build a table mapping for an InfluxDB source (measurement-level).

    Uses the SOURCE column names from the metadata (sourceColumnName) for the
    reader side: the InfluxDB time column is "_time" in queries, while the
    metadata columnName is the target name ("ts") — passing columnName to the
    plugin fails the query. The target side uses the KaiwuDB column names (columnName).

    Time-range parameters are REQUIRED and have NO defaults:
    the influxdb reader plugin splits the query into windows of splitIntervalS
    seconds across [begin_datetime, end_datetime]; a null range fails the migration,
    and a too-wide range (e.g. 1970~2099) causes memory overflow in the reader.
    ALWAYS ask the user for the actual data time range.

    Args:
        source_db: Database object from read_metadata() response
        measurement: InfluxDB measurement name (= source table name)
        target_table: Target KaiwuDB table name (default: same as measurement)
        write_mode: Target write mode (default: insert)
        begin_datetime: REQUIRED data start time "YYYY-MM-DD HH:MM:SS" (user input)
        end_datetime: REQUIRED data end time "YYYY-MM-DD HH:MM:SS" (user input)
        split_interval_s: Time window split in seconds for concurrent fetch (default: 86400 = 1 day)
        read_timeout: InfluxDB read timeout in seconds (0 = plugin default; KDTS tests use 60)
        connect_timeout: InfluxDB connect timeout in seconds (0 = plugin default; KDTS tests use 60)

    Returns:
        TableMapping dict with measurement + correct column lists + time range.
    """
    if not begin_datetime or not end_datetime:
        raise ValueError(
            "begin_datetime and end_datetime are REQUIRED for InfluxDB mapping — "
            "ask the user for the actual data time range (no defaults; a null or "
            "too-wide range fails/overflows the migration)."
        )
    tables = source_db.get("tableMap") or {}
    if measurement not in tables:
        raise ValueError(f"Measurement '{measurement}' not found in source_db tableMap")
    cols = tables[measurement].get("columns", [])
    source_cols = ",".join(c.get("sourceColumnName") or c.get("columnName") for c in cols)
    target_cols = ",".join(c.get("columnName") for c in cols)
    source = {
        "sourceType": "INFLUXDB",
        "measurement": measurement,
        "column": source_cols,
        "splitIntervalS": split_interval_s,
        "beginDateTime": begin_datetime,
        "endDateTime": end_datetime,
    }
    # Timeouts are optional (0 = plugin default); KDTS tests pass 60/60
    if read_timeout > 0:
        source["readTimeout"] = read_timeout
    if connect_timeout > 0:
        source["connectTimeout"] = connect_timeout
    return {
        "source": source,
        "target": {
            "sourceType": "KAIWUDB",
            "table": target_table or measurement,
            "column": target_cols,
            "writeMode": write_mode,
        }
    }


def mark_time_series_columns(source_db: Dict, table_name: str,
                             time_column: Optional[str] = None,
                             primary_tags: Optional[List[str]] = None,
                             tags: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Mark column roles on a source Database object for time-series DDL generation.

    Sets the column marks expected by KDTS (`Column.java` field names, declared
    explicitly via @JsonProperty): "isTs" (time column), "isTag" (tag column),
    "isPrimaryTag" (primary tag). KDTS generates time-series DDL from these marks.

    Args:
        source_db: Database object from read_metadata() response (mutated in place)
        table_name: Table name within the database to mark
        time_column: Column name to mark as the time series column (isTs=true)
        primary_tags: List of column names to mark as primary tags (isTag+isPrimaryTag=true)
        tags: List of column names to mark as ordinary tags (isTag=true)

    Returns:
        The same source_db object with marks applied.

    Notes:
        - PRIMARY TAG columns are automatically set to nullAble=false: KDTS demotes
          nullable primary tags to ordinary tags (verified: 3006 if none remain).
          Only pass columns whose SOURCE DATA is NULL-free as primary tags —
          otherwise the write fails on NOT NULL violation.
        - Tables without any isTag=true column are SKIPPED by KDTS (no DDL emitted)
    """
    tables = source_db.get("tableMap") or {}
    if table_name not in tables:
        raise ValueError(f"Table '{table_name}' not found in source_db tableMap")

    primary_tags = primary_tags or []
    tags = tags or []

    for col in tables[table_name].get("columns", []):
        name = col.get("columnName") or col.get("sourceColumnName")
        col["isTs"] = name == time_column
        col["isTag"] = name in primary_tags or name in tags
        col["isPrimaryTag"] = name in primary_tags
        if col["isPrimaryTag"]:
            col["nullAble"] = False   # PRIMARY TAGS must be NOT NULL (KDTS requirement)
    return source_db


# ==================== CLI Entry Point ====================

def main():
    """
    CLI entry point for quick testing and automation.

    Parses command line arguments and executes the specified action.
    """
    if len(sys.argv) < 2:
        print("Usage: python api_client.py <action> [options]")
        print("\nActions:")
        print("  test_connection     Test data source connectivity")
        print("  list_databases      List databases on source")
        print("  read_metadata       Read source metadata")
        print("  preview_ddl         Preview DDL for target")
        print("  execute_ddl         Execute DDL on target")
        print("  build_migration     Build migration script")
        print("  execute_migration   Execute migration")
        print("  query_status        Query task status")
        print("  control_task        Kill/control task")
        sys.exit(1)

    action = sys.argv[1]

    # Quick example usage
    if action == "test_connection":
        client = KDTSClient(base_url="http://localhost:8989")
        # engine is REQUIRED for all source configs per KDTS API
        source = build_source_config(
            source_type="MYSQL",
            host="127.0.0.1", port=3306,
            username="root", password="123456",
            engine="RELATIONAL"
        )
        result = client.test_connection(source)
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
