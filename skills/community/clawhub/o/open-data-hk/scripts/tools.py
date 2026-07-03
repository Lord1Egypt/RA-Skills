from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def list_datasets(
    limit: Optional[null] = None,
    offset: Optional[null] = None,
    language: Optional[str] = "en"
) -> Dict[str, Any]:
    """
    Get a list of dataset IDs from data.gov.hk

Args:
    limit: Maximum number of datasets to return (default: 1000)
    offset: Offset of the first dataset to return
    language: Language code (en, tc, sc)
    
    Args:
        limit: null
        offset: null
        language: null
    
    Returns:
        null
    """
    arguments = {
        "limit": limit,
        "offset": offset,
        "language": language
    }
    
    return call_api("1777419076890627", "list_datasets", arguments)

def get_dataset_details(
    dataset_id: str,
    language: Optional[str] = "en",
    include_tracking: Optional[bool] = False
) -> Dict[str, Any]:
    """
    Get detailed information about a specific dataset

Args:
    dataset_id: The ID or name of the dataset to retrieve
    language: Language code (en, tc, sc)
    include_tracking: Add tracking information to dataset and resources
    
    Args:
        dataset_id: null
        language: null
        include_tracking: null
    
    Returns:
        null
    """
    arguments = {
        "dataset_id": dataset_id,
        "language": language,
        "include_tracking": include_tracking
    }
    
    return call_api("1777419076890627", "get_dataset_details", arguments)

def list_categories(
    order_by: Optional[str] = "name",
    sort: Optional[str] = "title asc",
    limit: Optional[null] = None,
    offset: Optional[null] = None,
    all_fields: Optional[bool] = False,
    language: Optional[str] = "en"
) -> Dict[str, Any]:
    """
    Get a list of data categories (groups)

Args:
    order_by: Field to sort by ('name' or 'packages') - deprecated, use sort instead
    sort: Sorting of results ('name asc', 'package_count desc', etc.)
    limit: Maximum number of categories to return
    offset: Offset for pagination
    all_fields: Return full group dictionaries instead of just names
    language: Language code (en, tc, sc)
    
    Args:
        order_by: null
        sort: null
        limit: null
        offset: null
        all_fields: null
        language: null
    
    Returns:
        
    """
    arguments = {
        "order_by": order_by,
        "sort": sort,
        "limit": limit,
        "offset": offset,
        "all_fields": all_fields,
        "language": language
    }
    
    return call_api("1777419076890627", "list_categories", arguments)

def get_category_details(
    category_id: str,
    include_datasets: Optional[bool] = False,
    include_dataset_count: Optional[bool] = True,
    include_extras: Optional[bool] = True,
    include_users: Optional[bool] = True,
    include_groups: Optional[bool] = True,
    include_tags: Optional[bool] = True,
    include_followers: Optional[bool] = True,
    language: Optional[str] = "en"
) -> Dict[str, Any]:
    """
    Get detailed information about a specific category (group)

Args:
    category_id: The ID or name of the category to retrieve
    include_datasets: Include a truncated list of the category's datasets
    include_dataset_count: Include the full package count
    include_extras: Include the category's extra fields
    include_users: Include the category's users
    include_groups: Include the category's sub groups
    include_tags: Include the category's tags
    include_followers: Include the category's number of followers
    language: Language code (en, tc, sc)
    
    Args:
        category_id: null
        include_datasets: null
        include_dataset_count: null
        include_extras: null
        include_users: null
        include_groups: null
        include_tags: null
        include_followers: null
        language: null
    
    Returns:
        null
    """
    arguments = {
        "category_id": category_id,
        "include_datasets": include_datasets,
        "include_dataset_count": include_dataset_count,
        "include_extras": include_extras,
        "include_users": include_users,
        "include_groups": include_groups,
        "include_tags": include_tags,
        "include_followers": include_followers,
        "language": language
    }
    
    return call_api("1777419076890627", "get_category_details", arguments)

def search_datasets(
    query: Optional[str] = "*:*",
    limit: Optional[int] = 10.0,
    offset: Optional[int] = 0.0,
    language: Optional[str] = "en"
) -> Dict[str, Any]:
    """
    Search for datasets by query term using the package_search API.

This function searches across dataset titles, descriptions, and other metadata
to find datasets matching the query term.

Args:
    query: The solr query string (e.g., "transport", "weather", "*:*" for all)
    limit: Maximum number of datasets to return (default: 10, max: 1000)
    offset: Offset for pagination
    language: Language code (en, tc, sc)

Returns:
    A dictionary containing:
    - count: Total number of matching datasets
    - results: List of matching datasets (up to limit)
    - has_more: Boolean indicating if there are more results available
    
    Args:
        query: null
        limit: null
        offset: null
        language: null
    
    Returns:
        null
    """
    arguments = {
        "query": query,
        "limit": limit,
        "offset": offset,
        "language": language
    }
    
    return call_api("1777419076890627", "search_datasets", arguments)

def get_supported_formats(
) -> Dict[str, Any]:
    """
    Get a list of file formats supported by data.gov.hk

Returns:
    A list of supported file formats
    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419076890627", "get_supported_formats", arguments)

def search_datasets_with_facets(
    query: Optional[str] = "*:*",
    language: Optional[str] = "en"
) -> Dict[str, Any]:
    """
    Search for datasets and return faceted results for better data exploration.

Args:
    query: The solr query string
    language: Language code (en, tc, sc)

Returns:
    A dictionary containing:
    - count: Total number of matching datasets
    - search_facets: Faceted information about the results
    - sample_results: First 3 matching datasets
    
    Args:
        query: null
        language: null
    
    Returns:
        null
    """
    arguments = {
        "query": query,
        "language": language
    }
    
    return call_api("1777419076890627", "search_datasets_with_facets", arguments)

def get_datasets_by_format(
    file_format: str,
    limit: Optional[int] = 10.0,
    language: Optional[str] = "en"
) -> Dict[str, Any]:
    """
    Get datasets that have resources in a specific file format.

Args:
    file_format: The file format to filter by (e.g., "CSV", "JSON", "GeoJSON")
    limit: Maximum number of datasets to return
    language: Language code (en, tc, sc)

Returns:
    A dictionary containing:
    - count: Total number of matching datasets
    - results: List of matching datasets
    
    Args:
        file_format: null
        limit: null
        language: null
    
    Returns:
        null
    """
    arguments = {
        "file_format": file_format,
        "limit": limit,
        "language": language
    }
    
    return call_api("1777419076890627", "get_datasets_by_format", arguments)

