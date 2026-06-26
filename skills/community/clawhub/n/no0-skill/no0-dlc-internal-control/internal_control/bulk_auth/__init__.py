"""
批量授权模块

支持批量审批功能
"""

from .service import (
    BulkAuthorizationService,
    BulkAuthRequest,
    BulkAuthItem,
    BulkAuthStatus,
    BulkRequestStore,
    BulkAuthAPI,
    generate_bulk_auth_page
)

__all__ = [
    'BulkAuthorizationService',
    'BulkAuthRequest',
    'BulkAuthItem',
    'BulkAuthStatus',
    'BulkRequestStore',
    'BulkAuthAPI',
    'generate_bulk_auth_page',
]