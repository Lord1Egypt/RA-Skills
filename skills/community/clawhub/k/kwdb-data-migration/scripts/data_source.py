"""
data_source.py - Complete Data Source Management Module

Provides comprehensive data source configuration management for all 14 KDTS source types,
including auto-detection, configuration building, connection testing, and template generation.

Key features:
- Auto-detect engine type from source type
- JDBC URL construction for relational databases
- Source-specific configuration builders (FTP, HDFS, MongoDB, time-series)
- Connection test integration with KDTS API client
- Configuration templates for all supported types
"""

from typing import Dict, Any, Optional, List
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


class Engine(str, Enum):
    """
    KDTS engine types for target (KaiwuDB) configuration.

    Usage:
    - For target (KaiwuDB) configuration: Must specify either RELATIONAL or TIMESERIES
      to indicate the target database engine type.
    - For source configuration: Engine is auto-detected from source type.
      RELATIONAL for RDBMS sources, TIMESERIES for all other sources.

    Source Type -> Engine Mapping:
    - RELATIONAL: MySQL, Oracle, PostgreSQL, SQL Server, ClickHouse
    - TIMESERIES: TDengine 2.x/3.x, InfluxDB 1.x/2.x, OpenTSDB, MongoDB, FTP, HDFS, KaiwuDB
    """
    RELATIONAL = "RELATIONAL"
    TIMESERIES = "TIMESERIES"


class SourceType(str, Enum):
    """All supported KDTS source types."""
    MYSQL = "MYSQL"
    ORACLE = "ORACLE"
    POSTGRESQL = "POSTGRESQL"
    SQLSERVER = "SQLSERVER"
    CLICKHOUSE = "CLICKHOUSE"
    KAIWUDB = "KAIWUDB"
    TDENGINE2X = "TDENGINE2X"
    TDENGINE3X = "TDENGINE3X"
    INFLUXDB1X = "INFLUXDB1X"
    INFLUXDB2X = "INFLUXDB2X"
    OPENTSDB = "OPENTSDB"
    MONGODB = "MONGODB"
    FTP = "FTP"
    HDFS = "HDFS"


class SourceCapability(str, Enum):
    """
    Source capability levels.

    Based on KDTS SourceTypes.java implementation:
    - FULL_MIGRATION: Supports auto-discovery of all tables (checkSourceForAllData).
      Sources: MYSQL, ORACLE, POSTGRESQL, CLICKHOUSE, KAIWUDB, TDENGINE3X
      Note: CLICKHOUSE and KAIWUDB do NOT support metadata reading (DDL generation).
    - META_AND_DATA: Supports both metadata reading and data migration,
      but NOT full migration (no automatic table discovery).
      Sources: SQLSERVER, INFLUXDB1X, INFLUXDB2X
    - DATA_ONLY: Supports data migration only, no metadata reading and no auto-discovery.
      Sources: TDENGINE2X, OPENTSDB, MONGODB, FTP, HDFS
    """
    FULL_MIGRATION = "full_migration"
    META_AND_DATA = "meta_and_data"
    DATA_ONLY = "data_only"


# Comprehensive source type registry
SOURCE_TYPE_REGISTRY: Dict[str, Dict[str, Any]] = {
    # Relational databases
    SourceType.MYSQL: {
        "engine": Engine.RELATIONAL,
        "default_port": 3306,
        "jdbc_driver": "com.mysql.cj.jdbc.Driver",
        "jdbc_url_template": "jdbc:mysql://{host}:{port}/{db}?useSSL=false&serverTimezone=UTC&allowPublicKeyRetrieval=true",
        "capability": SourceCapability.FULL_MIGRATION,
        "supports_metadata": True,
        "supports_full": True,
        "jdbc_prefix": "jdbc:mysql://",
    },
    SourceType.ORACLE: {
        "engine": Engine.RELATIONAL,
        "default_port": 1521,
        "jdbc_driver": "oracle.jdbc.OracleDriver",
        "jdbc_url_template": "jdbc:oracle:thin:@{host}:{port}:{db}",
        "capability": SourceCapability.FULL_MIGRATION,
        "supports_metadata": True,
        "supports_full": True,
        "jdbc_prefix": "jdbc:oracle:thin:@",
    },
    SourceType.POSTGRESQL: {
        "engine": Engine.RELATIONAL,
        "default_port": 5432,
        "jdbc_driver": "org.postgresql.Driver",
        "jdbc_url_template": "jdbc:postgresql://{host}:{port}/{db}",
        "capability": SourceCapability.FULL_MIGRATION,
        "supports_metadata": True,
        "supports_full": True,
        "jdbc_prefix": "jdbc:postgresql://",
    },
    SourceType.SQLSERVER: {
        "engine": Engine.RELATIONAL,
        "default_port": 1433,
        "jdbc_driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver",
        "jdbc_url_template": "jdbc:sqlserver://{host}:{port};databaseName={db};encrypt=false",
        "capability": SourceCapability.META_AND_DATA,
        "supports_metadata": True,
        "supports_full": False,
        "jdbc_prefix": "jdbc:sqlserver://",
    },
    SourceType.CLICKHOUSE: {
        "engine": Engine.RELATIONAL,
        "default_port": 9000,
        "jdbc_driver": "com.github.housepower.jdbc.ClickHouseDriver",
        "jdbc_url_template": "jdbc:clickhouse://{host}:{port}/{db}",
        "capability": SourceCapability.FULL_MIGRATION,
        "supports_metadata": False,
        "supports_full": True,
        "jdbc_prefix": "jdbc:clickhouse://",
    },
    # KaiwuDB (source or target)
    # When used as target, engine must be explicitly specified (RELATIONAL or TIMESERIES).
    SourceType.KAIWUDB: {
        "engine": None,  # Engine must be explicitly specified for KAIWUDB
        "default_port": 26257,
        "jdbc_driver": "com.kaiwudb.Driver",
        "jdbc_url_template": "jdbc:kaiwudb://{host}:{port}/{db}",
        "capability": SourceCapability.FULL_MIGRATION,
        "supports_metadata": False,
        "supports_full": True,
        "jdbc_prefix": "jdbc:kaiwudb://",
    },
    # Time-series databases
    SourceType.TDENGINE3X: {
        "engine": Engine.TIMESERIES,
        "default_port": 6030,
        "jdbc_driver": "com.taosdata.jdbc.TSDBDriver",
        "jdbc_url_template": "jdbc:TAOS3://{host}:{port}/{db}",
        "capability": SourceCapability.FULL_MIGRATION,
        "supports_metadata": True,
        "supports_full": True,
        "jdbc_prefix": "jdbc:TAOS3://",
    },
    SourceType.TDENGINE2X: {
        "engine": Engine.TIMESERIES,
        "default_port": 6030,
        "jdbc_driver": "com.taosdata.jdbc.TSDBDriver",
        "jdbc_url_template": "jdbc:TAOS://{host}:{port}/{db}",
        "capability": SourceCapability.DATA_ONLY,
        "supports_metadata": False,
        "supports_full": False,
        "jdbc_prefix": "jdbc:TAOS://",
    },
    SourceType.INFLUXDB1X: {
        "engine": Engine.TIMESERIES,
        "default_port": 8086,
        "jdbc_driver": None,  # HTTP protocol, no JDBC
        "jdbc_url_template": None,
        "capability": SourceCapability.META_AND_DATA,
        "supports_metadata": True,
        "supports_full": False,
        "jdbc_prefix": None,
    },
    SourceType.INFLUXDB2X: {
        "engine": Engine.TIMESERIES,
        "default_port": 8086,
        "jdbc_driver": None,
        "jdbc_url_template": None,
        "capability": SourceCapability.META_AND_DATA,
        "supports_metadata": True,
        "supports_full": False,
        "jdbc_prefix": None,
    },
    SourceType.OPENTSDB: {
        "engine": Engine.TIMESERIES,
        "default_port": 4242,
        "jdbc_driver": None,
        "jdbc_url_template": None,
        "capability": SourceCapability.DATA_ONLY,
        "supports_metadata": False,
        "supports_full": False,
        "jdbc_prefix": None,
    },
    # Document databases
    SourceType.MONGODB: {
        "engine": Engine.TIMESERIES,
        "default_port": 27017,
        "jdbc_driver": None,
        "jdbc_url_template": None,
        "capability": SourceCapability.DATA_ONLY,
        "supports_metadata": False,
        "supports_full": False,
        "jdbc_prefix": None,
    },
    # File-based sources
    SourceType.FTP: {
        "engine": Engine.TIMESERIES,
        "default_port": 21,
        "jdbc_driver": None,
        "jdbc_url_template": None,
        "capability": SourceCapability.DATA_ONLY,
        "supports_metadata": False,
        "supports_full": False,
        "jdbc_prefix": None,
    },
    SourceType.HDFS: {
        "engine": Engine.TIMESERIES,  # Use TIMESERIES for file sources
        "default_port": 8020,
        "jdbc_driver": None,
        "jdbc_url_template": None,
        "capability": SourceCapability.DATA_ONLY,
        "supports_metadata": False,
        "supports_full": False,
        "jdbc_prefix": None,
    },
}


class DataSourceManager:
    """
    Comprehensive data source configuration manager.

    Provides utilities for building, validating, and managing
    data source configurations for all KDTS supported types.
    """

    def __init__(self, api_client=None):
        """
        Initialize DataSourceManager.

        Args:
            api_client: Optional KDTS API client instance for connection testing.
        """
        self.api_client = api_client

    # ==================== Source Type Detection ====================

    @staticmethod
    def detect_source_type(config: Dict[str, Any]) -> Optional[str]:
        """
        Detect source type from configuration.

        Args:
            config: Data source configuration dict

        Returns:
            Detected source type string or None
        """
        # Direct type field
        if 'type' in config:
            return config['type'].upper()

        # JDBC URL detection
        url = config.get('url', '')
        for src_type, info in SOURCE_TYPE_REGISTRY.items():
            if info.get('jdbc_prefix') and url.startswith(info['jdbc_prefix']):
                return src_type

        return None

    @staticmethod
    def get_engine(source_type: str) -> str:
        """
        Get engine type for a source type.

        Args:
            source_type: Source type string

        Returns:
            Engine type string
        """
        source_upper = source_type.upper()
        if source_upper in SOURCE_TYPE_REGISTRY:
            engine = SOURCE_TYPE_REGISTRY[source_upper]["engine"]
            return engine.value if isinstance(engine, Engine) else engine

        # Default fallback
        logger.warning(f"Unknown source type '{source_type}', defaulting to RELATIONAL")
        return Engine.RELATIONAL.value

    @staticmethod
    def get_capability(source_type: str) -> Dict[str, Any]:
        """
        Get source capability information.

        Args:
            source_type: Source type string

        Returns:
            Dict with capability info
        """
        source_upper = source_type.upper()
        if source_upper in SOURCE_TYPE_REGISTRY:
            info = SOURCE_TYPE_REGISTRY[source_upper]
            return {
                "capability": info["capability"].value if isinstance(info["capability"], SourceCapability) else info["capability"],
                "supports_full_migration": info["supports_full"],
                "supports_metadata": info["supports_metadata"],
                "engine": info["engine"].value if isinstance(info["engine"], Engine) else info["engine"],
                "default_port": info["default_port"],
            }
        return {
            "capability": SourceCapability.DATA_ONLY.value,
            "supports_full_migration": False,
            "supports_metadata": False,
            "engine": Engine.RELATIONAL.value,
            "default_port": 0,
        }

    # ==================== JDBC URL Construction ====================

    @staticmethod
    def build_jdbc_url(source_type: str, host: str, port: int, db_name: str) -> Optional[str]:
        """
        Build JDBC URL for relational databases.

        Args:
            source_type: Source type string
            host: Database host
            port: Database port
            db_name: Database name

        Returns:
            JDBC URL string or None if not supported
        """
        source_upper = source_type.upper()
        if source_upper not in SOURCE_TYPE_REGISTRY:
            return None

        info = SOURCE_TYPE_REGISTRY[source_upper]
        template = info.get("jdbc_url_template")
        if not template:
            return None

        return template.format(host=host, port=port, db=db_name)

    # ==================== Configuration Building ====================

    @staticmethod
    def build_config(
            source_type: str,
        host: str,
        port: Optional[int] = None,
        username: str = "",
        password: str = "",
        db_name: Optional[str] = None,
        url: Optional[str] = None,
        extra_fields: Optional[Dict[str, Any]] = None,
        is_target: bool = False,
    ) -> Dict[str, Any]:
        """
        Build complete data source configuration.

        Args:
            source_type: Source type (e.g., MYSQL, KAIWUDB, FTP)
            host: Database host (or FTP/HDFS host)
            port: Port number (uses default if None)
            username: Username for authentication
            password: Password for authentication
            db_name: Database name (not required for file sources)
            url: Full JDBC URL (overrides host:port:db for relational)
            extra_fields: Additional source-specific fields
            is_target: If True, marks as target configuration

        Returns:
            Complete data source configuration dict
        """
        source_upper = source_type.upper()

        if source_upper not in SOURCE_TYPE_REGISTRY:
            raise ValueError(f"Unsupported source type: {source_type}")

        registry_info = SOURCE_TYPE_REGISTRY[source_upper]

        config = {
            "engine": registry_info["engine"].value if isinstance(registry_info["engine"], Engine) else registry_info["engine"],
            "type": source_upper,
        }

        # Use provided values or defaults
        use_port = port if port else registry_info["default_port"]

        if url:
            config["url"] = url
            # Extract host and port from URL for reference (if possible)
            if not host:
                config["host"] = host or ""
        else:
            config["host"] = host
            config["port"] = use_port

        config["username"] = username
        config["password"] = password

        # Add db_name for database sources (not for file sources like FTP, HDFS)
        if db_name and source_upper not in [SourceType.FTP, SourceType.HDFS]:
            config["dbName"] = db_name

        # Mark as target if applicable
        if is_target:
            config["isTarget"] = True

        # Add source-specific fields
        if extra_fields:
            config.update(extra_fields)

        logger.info(f"Built config for {source_upper}: {host}:{use_port}")
        return config

    def build_relational_config(
        self,
        source_type: str,
        host: str,
        port: Optional[int] = None,
        username: str = "",
        password: str = "",
        db_name: str = "",
        use_jdbc_url: bool = False,
        is_target: bool = False,
    ) -> Dict[str, Any]:
        """
        Build relational database configuration.

        Args:
            source_type: Relational source type
            host: Database host
            port: Database port (uses default if None)
            username: Username
            password: Password
            db_name: Database name
            use_jdbc_url: If True, use JDBC URL instead of host:port
            is_target: If True, mark as target

        Returns:
            Relational database configuration
        """
        registry_info = SOURCE_TYPE_REGISTRY.get(source_type.upper(), {})

        url = None
        if use_jdbc_url and registry_info.get("jdbc_url_template"):
            url = self.build_jdbc_url(source_type, host, port or registry_info["default_port"], db_name)

        return self.build_config(
            source_type=source_type,
            host=host,
            port=port,
            username=username,
            password=password,
            db_name=db_name,
            url=url,
            is_target=is_target,
        )

    def build_timeseries_config(
        self,
        source_type: str,
        host: str,
        port: Optional[int] = None,
        username: str = "",
        password: str = "",
        db_name: str = "",
        is_target: bool = False,
    ) -> Dict[str, Any]:
        """
        Build time-series database configuration.

        Args:
            source_type: Time-series source type
            host: Database host
            port: Database port (uses default if None)
            username: Username
            password: Password
            db_name: Database name
            is_target: If True, mark as target

        Returns:
            Time-series database configuration
        """
        return self.build_config(
            source_type=source_type,
            host=host,
            port=port,
            username=username,
            password=password,
            db_name=db_name,
            is_target=is_target,
        )

    def build_mongodb_config(
        self,
        host: str,
        port: Optional[int] = 27017,
        username: str = "",
        password: str = "",
        db_name: str = "",
        auth_db: str = "admin",
        is_target: bool = False,
    ) -> Dict[str, Any]:
        """
        Build MongoDB configuration.

        Args:
            host: MongoDB host
            port: MongoDB port (default: 27017)
            username: Username
            password: Password
            db_name: Database name
            auth_db: Authentication database (default: admin)
            is_target: If True, mark as target

        Returns:
            MongoDB configuration
        """
        return self.build_config(
            source_type=SourceType.MONGODB,
            host=host,
            port=port,
            username=username,
            password=password,
            db_name=db_name,
            extra_fields={"authDb": auth_db},
            is_target=is_target,
        )

    def build_ftp_config(
        self,
        host: str,
        port: int = 21,
        username: str = "anonymous",
        password: str = "",
        protocol: str = "ftp",
        is_target: bool = False,
    ) -> Dict[str, Any]:
        """
        Build FTP/SFTP configuration.

        Args:
            host: FTP/SFTP host
            port: FTP port (default: 21)
            username: Username (default: anonymous)
            password: Password or email for anonymous
            protocol: Protocol (ftp or sftp)
            is_target: If True, mark as target

        Returns:
            FTP/SFTP configuration
        """
        config = self.build_config(
            source_type=SourceType.FTP,
            host=host,
            port=port,
            username=username,
            password=password,
            is_target=is_target,
        )
        # Add protocol field for FTP/SFTP distinction
        config["protocol"] = protocol.lower()
        return config

    def build_hdfs_config(
        self,
        host: str,
        port: int = 8020,
        username: str = "",
        password: str = "",
        default_fs: Optional[str] = None,
        is_target: bool = False,
    ) -> Dict[str, Any]:
        """
        Build HDFS configuration.

        Args:
            host: HDFS NameNode host
            port: HDFS port (default: 8020)
            username: Username
            password: Password (typically not required for HDFS)
            default_fs: HDFS URI (e.g., hdfs://namenode:8020)
            is_target: If True, mark as target

        Returns:
            HDFS configuration
        """
        config = self.build_config(
            source_type=SourceType.HDFS,
            host=host,
            port=port,
            username=username,
            password=password,
            is_target=is_target,
        )
        # Add defaultFs field
        if default_fs:
            config["defaultFs"] = default_fs
        else:
            config["defaultFs"] = f"hdfs://{host}:{port}"
        return config

    def build_target_config(
        self,
        engine: str = "RELATIONAL",
        host: str = "127.0.0.1",
        port: int = 26257,
        username: str = "root",
        password: str = "",
        db_name: str = "",
    ) -> Dict[str, Any]:
        """
        Build KaiwuDB target configuration.

        Args:
            engine: Target engine (RELATIONAL or TIMESERIES)
            host: Target host
            port: Target port (default: 26257)
            username: Username (default: root)
            password: Password
            db_name: Target database name

        Returns:
            KaiwuDB target configuration
        """
        return self.build_config(
            source_type=SourceType.KAIWUDB,
            host=host,
            port=port,
            username=username,
            password=password,
            db_name=db_name,
            extra_fields={"engine": engine},
            is_target=True,
        )

    # ==================== Connection Testing ====================

    def test_connection(
        self,
        config: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Test connection to data source.

        Args:
            config: Data source configuration
            base_url: KDTS server base URL (uses api_client if available)

        Returns:
            Connection test result with status and details
        """
        if self.api_client:
            # Use provided API client
            is_target = config.get("isTarget", False)
            return self.api_client.test_connection(config, is_target=is_target)

        # Without API client, can only validate config format
        logger.warning("No API client available, performing config validation only")
        return self._validate_config_format(config)

    @staticmethod
    def _validate_config_format(config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate configuration format without API call.
        
        Note: engine is NOT required for source config (auto-detected),
        but IS required for target config (KaiwuDB).

        Args:
            config: Configuration to validate

        Returns:
            Validation result
        """
        # Check if this is a target config
        is_target = config.get('isTarget', False) or config.get('type', '').upper() == 'KAIWUDB'
        
        # Required fields: engine only required for target config
        required = ['type', 'host', 'username', 'password']
        if is_target:
            required.append('engine')  # engine required for target config
        
        missing = [f for f in required if f not in config or not config[f]]

        if missing:
            return {
                "code": 1001,
                "message": f"Missing required fields: {', '.join(missing)}",
                "valid": False,
            }

        return {
            "code": 0,
            "message": "Config format valid (no actual connection tested)",
            "valid": True,
        }

    def test_both_connections(
        self,
        source_config: Dict[str, Any],
        target_config: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Test both source and target connections.

        Args:
            source_config: Source configuration
            target_config: Target configuration
            base_url: KDTS server base URL

        Returns:
            Combined test result
        """
        source_result = self.test_connection(source_config)
        target_result = self.test_connection(target_config)

        return {
            "source": source_result,
            "target": target_result,
            "all_valid": source_result.get("valid", False) and target_result.get("valid", False),
        }

    # ==================== Template Generation ====================

    @staticmethod
    def get_template(source_type: str) -> Dict[str, Any]:
        """
        Get configuration template for a source type.

        Args:
            source_type: Source type string

        Returns:
            Configuration template with placeholders
        """
        registry_info = SOURCE_TYPE_REGISTRY.get(source_type.upper(), {})

        # Get and convert engine to string
        engine = registry_info.get("engine", Engine.RELATIONAL)
        engine_str = engine.value if isinstance(engine, Engine) else engine

        template = {
            "engine": engine_str,
            "type": source_type.upper(),
            "host": "<host>",
            "port": registry_info.get("default_port", 0),
            "username": "<username>",
            "password": "<password>",
        }

        # Add dbName for database sources (not for file sources)
        if source_type.upper() not in [SourceType.FTP, SourceType.HDFS]:
            template["dbName"] = "<database_name>"

        # Add JDBC URL hint for relational sources
        if registry_info.get("jdbc_url_template"):
            template["_jdbc_url_hint"] = registry_info["jdbc_url_template"].format(
                host="<host>", port=registry_info.get("default_port"), db="<database_name>"
            )

        return template

    def get_all_templates(self) -> Dict[str, Dict[str, Any]]:
        """
        Get configuration templates for all source types.

        Returns:
            Dict mapping source types to their templates
        """
        return {
            src_type: self.get_template(src_type)
            for src_type in SOURCE_TYPE_REGISTRY
        }

    # ==================== Utility Methods ====================

    @staticmethod
    def list_supported_types() -> List[str]:
        """
        List all supported source types.

        Returns:
            Sorted list of source type strings
        """
        return sorted(SOURCE_TYPE_REGISTRY.keys())

    @staticmethod
    def get_default_port(source_type: str) -> int:
        """
        Get default port for a source type.

        Args:
            source_type: Source type string

        Returns:
            Default port number
        """
        return SOURCE_TYPE_REGISTRY.get(source_type.upper(), {}).get("default_port", 0)

    @staticmethod
    def get_source_type_registry() -> Dict[str, Dict[str, Any]]:
        """
        Get complete source type registry.

        Returns:
            Copy of source type registry
        """
        return dict(SOURCE_TYPE_REGISTRY)

    @staticmethod
    def is_full_migration_capable(source_type: str) -> bool:
        """
        Check if source supports full migration.

        Args:
            source_type: Source type string

        Returns:
            True if full migration is supported
        """
        source_upper = source_type.upper()
        if source_upper in SOURCE_TYPE_REGISTRY:
            return SOURCE_TYPE_REGISTRY[source_upper]["supports_full"]
        return False

    @staticmethod
    def is_metadata_capable(source_type: str) -> bool:
        """
        Check if source supports metadata reading.

        Args:
            source_type: Source type string

        Returns:
            True if metadata reading is supported
        """
        source_upper = source_type.upper()
        if source_upper in SOURCE_TYPE_REGISTRY:
            return SOURCE_TYPE_REGISTRY[source_upper]["supports_metadata"]
        return False


# Convenience functions (module-level)

def build_source_config(
    source_type: str,
    host: str,
    port: Optional[int] = None,
    username: str = "",
    password: str = "",
    db_name: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Module-level convenience function to build source config.

    Args:
        source_type: Source type string
        host: Database host
        port: Port number (uses default if None)
        username: Username
        password: Password
        db_name: Database name

    Returns:
        Data source configuration dict
    """
    manager = DataSourceManager()
    return manager.build_config(
        source_type=source_type,
        host=host,
        port=port,
        username=username,
        password=password,
        db_name=db_name,
    )


def build_target_config(
    engine: str = "RELATIONAL",
    host: str = "127.0.0.1",
    port: int = 26257,
    username: str = "root",
    password: str = "",
    db_name: str = "",
) -> Dict[str, Any]:
    """
    Module-level convenience function to build target config.

    Args:
        engine: Target engine (RELATIONAL or TIMESERIES)
        host: Target host
        port: Target port (default: 26257)
        username: Username
        password: Password
        db_name: Target database name

    Returns:
        Target configuration dict
    """
    manager = DataSourceManager()
    return manager.build_target_config(
        engine=engine,
        host=host,
        port=port,
        username=username,
        password=password,
        db_name=db_name,
    )


if __name__ == "__main__":
    # Demo usage
    manager = DataSourceManager()

    print("=== Supported Source Types ===")
    print(manager.list_supported_types())

    print("\n=== MySQL Config ===")
    mysql_config = manager.build_relational_config(
        source_type="MYSQL",
        host="192.168.1.100",
        username="root",
        password="secret",
        db_name="source_db",
    )
    print(mysql_config)

    print("\n=== KaiwuDB Target Config ===")
    target_config = manager.build_target_config(
        engine="RELATIONAL",
        host="127.0.0.1",
        username="root",
        password="kwdb_secret",
        db_name="target_db",
    )
    print(target_config)

    print("\n=== FTP Config ===")
    ftp_config = manager.build_ftp_config(
        host="ftp.example.com",
        username="user",
        password="pass",
        protocol="sftp",
    )
    print(ftp_config)

    print("\n=== MongoDB Config ===")
    mongo_config = manager.build_mongodb_config(
        host="mongo.example.com",
        port=27017,
        username="admin",
        password="pass",
        db_name="source_mongo",
    )
    print(mongo_config)

    print("\n=== Source Type Capabilities ===")
    for stype in ["MYSQL", "KAIWUDB", "FTP", "HDFS", "MONGODB"]:
        cap = manager.get_capability(stype)
        print(f"{stype}: {cap}")