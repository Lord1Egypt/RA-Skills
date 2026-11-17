"""
error_handler.py - Unified Error Handling for KWDB Data Migration

Maps all KDTS Server error codes to human-readable messages and actionable fix suggestions.
Covers 18 error codes across 6 categories: parameter, connection, metadata, DataX, resource, system.

Error categories:
- 1xxx: Parameter validation errors
- 2xxx: Connection errors
- 3xxx: Metadata/DDL errors
- 4xxx: DataX execution errors
- 5xxx: Resource/availability errors
- 9xxx: System/internal errors
"""

from typing import Dict, Optional, Any
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


# Complete error code mapping with user-friendly messages and fix suggestions
ERROR_CODE_MAP = {
    # ==================== Parameter Errors (1xxx) ====================
    1001: {
        "category": "parameter",
        "name": "PARAM_INVALID",
        "title": "Invalid Request Parameters",
        "description": "The request contains invalid or missing parameters.",
        "common_causes": [
            "Required field is empty or missing",
            "Field value has incorrect format",
            "Enum value is not in allowed range"
        ],
        "fix_suggestions": [
            "Check all required fields: type, host, port, username, password",
            "Note: 'engine' is only required for TARGET config (KAIWUDB), not for source",
            "Ensure field values match expected types (numbers for port, strings for text)",
            "Verify enum values are correct (e.g., 'MYSQL' not 'mysql', 'RELATIONAL' not 'relational')",
            "If using URL, ensure JDBC URL format is correct: jdbc:mysql://host:port/dbname"
        ]
    },
    1002: {
        "category": "parameter",
        "name": "PARAM_SOURCE_TYPE_INVALID",
        "title": "Unsupported Source Database Type",
        "description": "The specified source database type is not supported by KDTS.",
        "common_causes": [
            "Typo in source type name",
            "Source type not implemented in current KDTS version",
            "Using target-only type as source"
        ],
        "fix_suggestions": [
            "Check spelling of source type (e.g., MYSQL, ORACLE, POSTGRESQL, KAIWUDB)",
            "See supported types list: MYSQL, ORACLE, POSTGRESQL, SQLSERVER, CLICKHOUSE, KAIWUDB, TDENGINE2X, TDENGINE3X, INFLUXDB1X, INFLUXDB2X, OPENTSDB, MONGODB, FTP, HDFS",
            "For KWDB-to-KWDB migration, type should be KAIWUDB",
            "Contact KDTS admin if you need a new source type added"
        ]
    },
    1003: {
        "category": "parameter",
        "name": "PARAM_TARGET_TYPE_INVALID",
        "title": "Invalid Target Database Type",
        "description": "Target must be KAIWUDB. KDTS only supports KaiwuDB as migration target.",
        "common_causes": [
            "Using non-KaiwuDB type as target",
            "Copying source config to target without changing type"
        ],
        "fix_suggestions": [
            "Set target type to KAIWUDB",
            "Set target engine to RELATIONAL (for SQL migration) or TIMESERIES (for time-series)",
            "Ensure target has dbName specified",
            "If you need to migrate to another database system, use a different tool (e.g., native database tools)"
        ]
    },
    1004: {
        "category": "parameter",
        "name": "PARAM_TABLE_MAPPING_MISMATCH",
        "title": "Table Mapping Configuration Error",
        "description": "Source and target table mappings have mismatched structures.",
        "common_causes": [
            "Number of source and target mappings differ",
            "Column count mismatch between source and target",
            "Empty tables field when table-level migration required"
        ],
        "fix_suggestions": [
            "Ensure each source mapping has a corresponding target mapping",
            "Check column lists match between source and target",
            "For full migration (all tables), leave tables as empty array: []",
            "For table-level migration, explicitly list each table mapping with source and target"
        ]
    },
    1005: {
        "category": "parameter",
        "name": "JSON_PARSE_ERROR",
        "title": "JSON Parse Error",
        "description": "Request body is not valid JSON.",
        "common_causes": [
            "Malformed JSON syntax",
            "Trailing commas in JSON",
            "Single quotes instead of double quotes",
            "Special characters not escaped"
        ],
        "fix_suggestions": [
            "Validate JSON syntax with a JSON validator tool",
            "Use double quotes for all keys and string values",
            "Remove trailing commas from arrays and objects",
            "Escape special characters: \\n, \\t, \", etc."
        ]
    },

    # ==================== Connection Errors (2xxx) ====================
    2001: {
        "category": "connection",
        "name": "CONNECTION_FAILED",
        "title": "Database Connection Failed",
        "description": "KDTS cannot establish connection to the specified database.",
        "common_causes": [
            "Database server is not running",
            "Incorrect host or port",
            "Firewall blocking connection",
            "Invalid username or password",
            "Database does not exist",
            "Connection pool exhausted"
        ],
        "fix_suggestions": [
            "Verify database server is running and accessible",
            "Check host and port are correct (MySQL default: 3306, PostgreSQL: 5432, Oracle: 1521)",
            "Test network connectivity: ping <host>, telnet <host> <port>",
            "Verify username and password are correct",
            "Ensure target database exists or create it first",
            "Check firewall rules allow KDTS server IP to connect",
            "For JDBC URL users: verify URL format (e.g., jdbc:mysql://host:3306/dbname)"
        ]
    },

    # ==================== Metadata Errors (3xxx) ====================
    3001: {
        "category": "metadata",
        "name": "METADATA_PARSE_FAILED",
        "title": "Metadata Reading Failed",
        "description": "KDTS cannot read source database metadata (tables, columns, etc.).",
        "common_causes": [
            "Source type does not support metadata feature",
            "Insufficient database privileges",
            "Database objects corrupted",
            "Unsupported database version"
        ],
        "fix_suggestions": [
            "Check source type supports metadata (see capabilities: MYSQL, ORACLE, POSTGRESQL, KAIWUDB, SQLSERVER, TDENGINE3X, INFLUXDB1X, INFLUXDB2X)",
            "Ensure database user has SELECT privilege on system catalog tables",
            "Verify source database is not corrupted",
            "Check KDTS version compatibility with source database version",
            "For unsupported metadata sources (TDENGINE2X, OPENTSDB, etc.), use table-level migration with manual column specification"
        ]
    },
    3002: {
        "category": "metadata",
        "name": "METADATA_DDL_BUILD_FAILED",
        "title": "DDL Generation Failed",
        "description": "KDTS cannot generate DDL from source metadata.",
        "common_causes": [
            "Unsupported column type in source",
            "Complex constraint that cannot be translated",
            "Type mapping not available"
        ],
        "fix_suggestions": [
            "Check if source has any unusual column types",
            "Review type mapping documentation for unsupported types",
            "Try migrating simpler tables first (without complex types)",
            "Consider manual DDL creation for problematic tables",
            "Use data-only migration if target table already exists"
        ]
    },
    3003: {
        "category": "metadata",
        "name": "METADATA_EXECUTE_FAILED",
        "title": "DDL Execution Failed",
        "description": "KDTS cannot execute generated DDL on target KaiwuDB.",
        "common_causes": [
            "Table already exists and conflict with DDL",
            "Insufficient target privileges",
            "KaiwuDB version incompatibility",
            "Invalid DDL syntax for KaiwuDB"
        ],
        "fix_suggestions": [
            "Check if target tables already exist; consider using DROP TABLE first (with backup!)",
            "Verify target user has CREATE, ALTER privileges",
            "Check KaiwuDB version compatibility with KDTS",
            "Enable auto_ddl=true for automatic type creation",
            "If using data-only migration, ensure target tables exist and skip DDL step"
        ]
    },
    3004: {
        "category": "metadata",
        "name": "METADATA_TAG_LIMIT_EXCEEDED",
        "title": "Tag Column Limit Exceeded",
        "description": "Time-series migration has too many tag columns (max 128 columns total, 4 primary tags).",
        "common_causes": [
            "Source table has more than 128 columns",
            "More than 4 tag columns designated as primary tags",
            "Mixing time-series and relational columns incorrectly"
        ],
        "fix_suggestions": [
            "Reduce number of columns to 128 or fewer",
            "Ensure only 4 primary tags maximum",
            "Split migration into multiple batches if table has many columns",
            "For time-series data: keep tags in Tag column (max 128) and metrics in Value column",
            "Review KaiwuDB time-series schema design best practices"
        ]
    },
    3005: {
        "category": "metadata",
        "name": "METADATA_TAG_NAME_TOO_LONG",
        "title": "Tag/Column Name Too Long",
        "description": "Tag or column name exceeds 128-byte limit.",
        "common_causes": [
            "Column name is very long in source database",
            "Multi-byte characters in name",
            "Generated name exceeds limit after translation"
        ],
        "fix_suggestions": [
            "Rename long columns in source database first",
            "Use column alias mapping in migration config",
            "For Chinese/Japanese names, consider shorter ASCII alternatives",
            "Split very long column names if possible"
        ]
    },
    3006: {
        "category": "metadata",
        "name": "METADATA_NO_PRIMARY_TAG",
        "title": "No Valid Primary Tag Found",
        "description": "Time-series migration requires at least one valid primary tag.",
        "common_causes": [
            "Source table has no suitable ID column for primary tag",
            "All candidate columns have null values",
            "Primary tag selection is ambiguous"
        ],
        "fix_suggestions": [
            "Identify a unique, non-null column to use as primary tag",
            "Add a primary key column to source table before migration",
            "For time-series data: primary tag should be device/sensor identifier",
            "Ensure primary tag has no duplicate values across the dataset"
        ]
    },

    # ==================== DataX Errors (4xxx) ====================
    4001: {
        "category": "datax",
        "name": "DATAX_BUILD_SCRIPT_FAILED",
        "title": "Migration Script Build Failed",
        "description": "KDTS cannot generate DataX migration script.",
        "common_causes": [
            "Invalid table mapping configuration",
            "Source/target type mapping not supported",
            "DataX template not found on KDTS server",
            "Missing sourceType in table mapping"
        ],
        "fix_suggestions": [
            "Verify table mapping has correct source and target sections",
            "Ensure sourceType is set correctly (RDBMS, KAIWUDB, TDENGINE, INFLUXDB, MONGODB, etc.)",
            "Check target sourceType must be KAIWUDB",
            "Verify KDTS server has DataX templates installed",
            "For full migration, leave tables as empty array; for table-level, list all mappings"
        ]
    },
    4002: {
        "category": "datax",
        "name": "DATAX_PROCESS_LAUNCH_FAILED",
        "title": "DataX Process Launch Failed",
        "description": "KDTS cannot start DataX subprocess for migration.",
        "common_causes": [
            "Python 3 not found on KDTS server",
            "DataX installation corrupted",
            "Insufficient system resources",
            "Security policy blocking process execution"
        ],
        "fix_suggestions": [
            "Check Python 3 installation on KDTS server: which python3, python3 --version",
            "Verify DataX home directory is correctly configured: datax.home.path",
            "Check KDTS server disk space and memory",
            "Review KDTS logs for specific launch error details",
            "Try running DataX manually: cd /path/to/datax && python3 bin/datax.py job.json"
        ]
    },
    4003: {
        "category": "datax",
        "name": "DATAX_PROCESS_TIMEOUT",
        "title": "Migration Process Timeout",
        "description": "Migration execution exceeded timeout limit.",
        "common_causes": [
            "Large dataset takes too long to migrate",
            "Network latency between source and target",
            "DataX running too slowly",
            "Server resource contention"
        ],
        "fix_suggestions": [
            "Increase KDTS timeout configuration (datax.timeout in application.yml)",
            "Reduce data volume: add WHERE clause filter, migrate in batches",
            "Increase DataX channel count for parallel migration: speed.channel = 4 or more",
            "Check source database performance: slow queries, lock contention",
            "Check target database performance: index overhead, disk I/O",
            "Monitor KDTS server CPU and memory during migration"
        ]
    },

    # ==================== Resource Errors (5xxx) ====================
    5001: {
        "category": "resource",
        "name": "RESOURCE_THREAD_POOL_FULL",
        "title": "Service Thread Pool Exhausted",
        "description": "KDTS has reached maximum concurrent requests limit. Server returns HTTP 503.",
        "common_causes": [
            "Too many concurrent migration requests",
            "Long-running tasks holding threads",
            "Thread pool size too small"
        ],
        "fix_suggestions": [
            "Wait and retry after the specified Retry-After seconds (usually 60)",
            "Reduce concurrent migration requests",
            "Increase thread pool size in KDTS configuration",
            "Kill any stuck migration tasks that are no longer needed",
            "Monitor KDTS server load and scale if necessary"
        ]
    },
    5002: {
        "category": "resource",
        "name": "RESOURCE_PYTHON_NOT_FOUND",
        "title": "Python 3 Not Available",
        "description": "KDTS server cannot find Python 3 executable.",
        "common_causes": [
            "Python 3 not installed on KDTS server",
            "Python installed in non-standard path",
            "PATH environment variable not set correctly"
        ],
        "fix_suggestions": [
            "Install Python 3 on KDTS server: sudo apt-get install python3 or sudo yum install python3",
            "Configure Python path in KDTS application.yml: datax.python.path",
            "Verify Python is accessible: which python3 && python3 --version",
            "Restart KDTS server after configuration change"
        ]
    },

    # ==================== System Errors (9xxx) ====================
    9999: {
        "category": "system",
        "name": "SYSTEM_INTERNAL_ERROR",
        "title": "KDTS Internal Error",
        "description": "Unexpected internal error in KDTS server.",
        "common_causes": [
            "Bug in KDTS code",
            "Unexpected null pointer",
            "Third-party library crash",
            "Configuration issue"
        ],
        "fix_suggestions": [
            "Check KDTS server logs for full stack trace",
            "Restart KDTS server and retry",
            "Check KDTS version and update if needed",
            "Report the issue to KDTS development team with logs",
            "Try simpler migration first to isolate the problem"
        ]
    }
}


class ErrorHandler:
    """
    Unified error handler for KDTS migration.
    Converts error codes to user-friendly messages and actionable suggestions.
    """

    @staticmethod
    def get_error_info(code: int) -> Optional[Dict[str, Any]]:
        """
        Get detailed error information by code.

        Args:
            code: KDTS error code

        Returns:
            Error info dict or None if code not found:
                {category, name, title, description, common_causes, fix_suggestions}
        """
        return ERROR_CODE_MAP.get(code)

    @staticmethod
    def get_error_hint(code: int) -> str:
        """
        Get concise user-friendly error hint.

        Args:
            code: KDTS error code

        Returns:
            Formatted error hint string with fix suggestions.
        """
        error_info = ERROR_CODE_MAP.get(code)
        if not error_info:
            return f"Unknown error code: {code}"

        lines = [
            f"**{error_info['title']}** ({error_info['name']})",
            f"Category: {error_info['category']}",
            f"Description: {error_info['description']}"
        ]

        if error_info['common_causes']:
            lines.append("\n**Common Causes:**")
            for cause in error_info['common_causes'][:3]:
                lines.append(f"  - {cause}")

        if error_info['fix_suggestions']:
            lines.append("\n**Fix Suggestions:**")
            for i, suggestion in enumerate(error_info['fix_suggestions'][:4], 1):
                lines.append(f"  {i}. {suggestion}")

        return "\n".join(lines)

    @staticmethod
    def format_response_error(response: Dict[str, Any]) -> str:
        """
        Format full error output from API response.

        Args:
            response: API response dict with code and message

        Returns:
            Formatted error string ready for display
        """
        code = response.get("code", 9999)
        message = response.get("message", "Unknown error")

        if code == 0:
            return "Success"

        hint = ErrorHandler.get_error_hint(code)

        return f"""
================================================================================
ERROR CODE: {code}
================================================================================
API Message: {message}

{hint}
================================================================================
"""

    @staticmethod
    def get_category_errors(category: str) -> Dict[int, Dict[str, Any]]:
        """
        Get all error codes in a category.

        Args:
            category: Category name (parameter, connection, metadata, datax, resource, system)

        Returns:
            Dict of error codes to error info
        """
        return {
            code: info for code, info in ERROR_CODE_MAP.items()
            if info['category'] == category
        }

    @staticmethod
    def search_errors(keyword: str) -> Dict[int, Dict[str, Any]]:
        """
        Search error codes by keyword.

        Args:
            keyword: Search keyword (case-insensitive)

        Returns:
            Dict of matching error codes to error info
        """
        keyword_lower = keyword.lower()
        results = {}

        for code, info in ERROR_CODE_MAP.items():
            search_text = " ".join([
                info.get("name", ""),
                info.get("title", ""),
                info.get("description", ""),
                *info.get("common_causes", []),
                *info.get("fix_suggestions", [])
            ]).lower()

            if keyword_lower in search_text:
                results[code] = info

        return results

    @staticmethod
    def get_all_categories() -> list:
        """
        Get list of all error categories.

        Returns:
            List of category strings
        """
        return sorted(set(info['category'] for info in ERROR_CODE_MAP.values()))


# Convenience functions
def format_api_error(api_response: Dict) -> str:
    """
    Convenience wrapper for ErrorHandler.format_response_error.

    Args:
        api_response: API response dict

    Returns:
        Formatted error string
    """
    return ErrorHandler.format_response_error(api_response)


def quick_error_lookup(code: int) -> str:
    """
    Quick error lookup returning concise hint.

    Args:
        code: Error code

    Returns:
        Error hint string
    """
    return ErrorHandler.get_error_hint(code)


if __name__ == "__main__":
    # Demo
    print("=== Error Code Demo ===\n")

    demo_codes = [1001, 1002, 1003, 2001, 3004, 4001, 4002, 4003, 5001, 5002, 9999]

    for code in demo_codes:
        hint = quick_error_lookup(code)
        print(hint)
        print("-" * 60)

    print("\n=== Category Summary ===")
    for category in ErrorHandler.get_all_categories():
        errors = ErrorHandler.get_category_errors(category)
        codes = ", ".join(str(c) for c in sorted(errors.keys()))
        print(f"  {category}: [{codes}]")
