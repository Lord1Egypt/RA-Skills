from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def search_dataflows(
    query: str,
    limit: Optional[float] = 20.0
) -> Dict[str, Any]:
    """
    Search for OECD datasets (dataflows) by keyword. Returns matching datasets with their IDs, names, and descriptions.
    
    Args:
        query: Search query to find relevant datasets
        limit: Maximum number of results to return (default: 20)
    
    Returns:
        
    """
    arguments = {
        "query": query,
        "limit": limit
    }
    
    return call_api("1777316659351555", "search_dataflows", arguments)

def list_dataflows(
    category: Optional[str] = None,
    limit: Optional[float] = 50.0
) -> Dict[str, Any]:
    """
    List available OECD dataflows (datasets), optionally filtered by category. Use this to browse datasets by topic area.
    
    Args:
        category: Optional category filter: ECO, HEA, EDU, ENV, TRD, JOB, NRG, AGR, GOV, SOC, DEV, STI, TAX, FIN, TRA, IND, REG
        limit: Maximum number of results (default: 50)
    
    Returns:
        
    """
    arguments = {
        "category": category,
        "limit": limit
    }
    
    return call_api("1777316659351555", "list_dataflows", arguments)

def get_data_structure(
    dataflow_id: str
) -> Dict[str, Any]:
    """
    Get the metadata and structure of a specific OECD dataset. Returns dimensions, attributes, and valid values for querying data.
    
    Args:
        dataflow_id: Dataflow ID (e.g., "QNA", "MEI", "HEALTH_STAT")
    
    Returns:
        
    """
    arguments = {
        "dataflow_id": dataflow_id
    }
    
    return call_api("1777316659351555", "get_data_structure", arguments)

def query_data(
    dataflow_id: str,
    filter: Optional[str] = None,
    start_period: Optional[str] = None,
    end_period: Optional[str] = None,
    last_n_observations: Optional[float] = None
) -> Dict[str, Any]:
    """
    Query actual statistical data from an OECD dataset. ⚠️ IMPORTANT: Defaults to last 100 observations (max 1000) to protect context window. Use filters, time periods, or last_n_observations to control data size. Large datasets (e.g. SOCX_AGG) can have 70,000+ observations - always specify limits!
    
    Args:
        dataflow_id: Dataflow ID to query
        filter: Dimension filter (e.g., "USA.GDP.." for US GDP). Use "*" or "all" for all values. Get structure first to see valid dimensions.
        start_period: Start period (e.g., "2020-Q1", "2020-01")
        end_period: End period (e.g., "2023-Q4", "2023-12")
        last_n_observations: Get only the last N observations (default: 100, max: 1000 to protect against context overflow)
    
    Returns:
        
    """
    arguments = {
        "dataflow_id": dataflow_id,
        "filter": filter,
        "start_period": start_period,
        "end_period": end_period,
        "last_n_observations": last_n_observations
    }
    
    return call_api("1777316659351555", "query_data", arguments)

def get_categories(
) -> Dict[str, Any]:
    """
    Get all available OECD data categories (17 categories covering all topics: Economy, Health, Education, Environment, etc.)
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659351555", "get_categories", arguments)

def get_popular_datasets(
) -> Dict[str, Any]:
    """
    Get a curated list of commonly used OECD datasets across all categories.
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659351555", "get_popular_datasets", arguments)

def search_indicators(
    indicator: str,
    category: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search for specific economic or social indicators by keyword (e.g., "inflation", "unemployment", "GDP").
    
    Args:
        indicator: Indicator to search for
        category: Optional category filter
    
    Returns:
        
    """
    arguments = {
        "indicator": indicator,
        "category": category
    }
    
    return call_api("1777316659351555", "search_indicators", arguments)

def get_dataflow_url(
    dataflow_id: str,
    filter: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate an OECD Data Explorer URL for a dataset. Use this to provide users with a direct link to explore data visually in their browser.
    
    Args:
        dataflow_id: Dataflow ID
        filter: Optional dimension filter
    
    Returns:
        
    """
    arguments = {
        "dataflow_id": dataflow_id,
        "filter": filter
    }
    
    return call_api("1777316659351555", "get_dataflow_url", arguments)

def list_categories_detailed(
) -> Dict[str, Any]:
    """
    Get all OECD data categories with example datasets for each category. Returns comprehensive information about all 17 categories.
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659351555", "list_categories_detailed", arguments)

