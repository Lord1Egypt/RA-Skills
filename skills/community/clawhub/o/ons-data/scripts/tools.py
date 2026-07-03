from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def list_datasets(
    limit: Optional[float] = 20.0,
    offset: Optional[float] = 0.0
) -> Dict[str, Any]:
    """
    List available ONS datasets with metadata
    
    Args:
        limit: Maximum number of datasets to return
        offset: Offset for pagination
    
    Returns:
        
    """
    arguments = {
        "limit": limit,
        "offset": offset
    }
    
    return call_api("1777316659346435", "list_datasets", arguments)

def get_dataset(
    dataset_id: str
) -> Dict[str, Any]:
    """
    Get detailed information about a specific dataset
    
    Args:
        dataset_id: The ID of the dataset to retrieve
    
    Returns:
        
    """
    arguments = {
        "dataset_id": dataset_id
    }
    
    return call_api("1777316659346435", "get_dataset", arguments)

def search_datasets(
    query: str,
    limit: Optional[float] = 10.0
) -> Dict[str, Any]:
    """
    Search for datasets by name or description
    
    Args:
        query: Search query for datasets
        limit: Maximum number of results
    
    Returns:
        
    """
    arguments = {
        "query": query,
        "limit": limit
    }
    
    return call_api("1777316659346435", "search_datasets", arguments)

def get_observation(
    dataset_id: str,
    edition: Optional[str] = "time-series",
    version: Optional[str] = "latest",
    dimensions: null
) -> Dict[str, Any]:
    """
    Get specific data observations with dimension filters
    
    Args:
        dataset_id: The ID of the dataset
        edition: Dataset edition
        version: Dataset version
        dimensions: Dimension filters as key-value pairs (e.g., {"geography": "K02000001", "time": "2023"})
    
    Returns:
        
    """
    arguments = {
        "dataset_id": dataset_id,
        "edition": edition,
        "version": version,
        "dimensions": dimensions
    }
    
    return call_api("1777316659346435", "get_observation", arguments)

def get_latest_data(
    dataset_id: str,
    geography: Optional[str] = None,
    time_period: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get the latest available data for a dataset with optional filters
    
    Args:
        dataset_id: The ID of the dataset
        geography: Geographic filter (e.g., K02000001 for UK)
        time_period: Time period filter (e.g., 2023, Q1-2023)
    
    Returns:
        
    """
    arguments = {
        "dataset_id": dataset_id,
        "geography": geography,
        "time_period": time_period
    }
    
    return call_api("1777316659346435", "get_latest_data", arguments)

