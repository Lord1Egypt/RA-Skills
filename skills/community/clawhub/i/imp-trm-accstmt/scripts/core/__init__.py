"""
Core module for BIPPI-imp-trm-accstmt
Re-exports data structures for backwards compatibility
"""

from .data_structures import (
    BankStatementData,
    BankStatementHeader,
    BalanceInfo,
    TransactionRecord,
    MappedRecord,
    MappingResult,
    ValidationResult,
    OutputConfig,
    BIPV5_FIELDS,
    get_required_fields,
    get_all_fields,
)

__all__ = [
    'BankStatementData',
    'BankStatementHeader',
    'BalanceInfo',
    'TransactionRecord',
    'MappedRecord',
    'MappingResult',
    'ValidationResult',
    'OutputConfig',
    'BIPV5_FIELDS',
    'get_required_fields',
    'get_all_fields',
]
