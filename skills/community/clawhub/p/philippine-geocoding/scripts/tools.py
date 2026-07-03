from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def get_island_groups(
) -> Dict[str, Any]:
    """
    List all island groups in the Philippines
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659371011", "get_island_groups", arguments)

def get_island_group(
    code: str
) -> Dict[str, Any]:
    """
    Get specific island group by code
    
    Args:
        code: null
    
    Returns:
        
    """
    arguments = {
        "code": code
    }
    
    return call_api("1777316659371011", "get_island_group", arguments)

def get_island_group_regions(
    islandGroupCode: str
) -> Dict[str, Any]:
    """
    Get all regions within a specific island group
    
    Args:
        islandGroupCode: null
    
    Returns:
        
    """
    arguments = {
        "islandGroupCode": islandGroupCode
    }
    
    return call_api("1777316659371011", "get_island_group_regions", arguments)

def get_island_group_provinces(
    islandGroupCode: str
) -> Dict[str, Any]:
    """
    Get all provinces within a specific island group
    
    Args:
        islandGroupCode: null
    
    Returns:
        
    """
    arguments = {
        "islandGroupCode": islandGroupCode
    }
    
    return call_api("1777316659371011", "get_island_group_provinces", arguments)

def get_island_group_cities(
    islandGroupCode: str
) -> Dict[str, Any]:
    """
    Get all cities within a specific island group
    
    Args:
        islandGroupCode: null
    
    Returns:
        
    """
    arguments = {
        "islandGroupCode": islandGroupCode
    }
    
    return call_api("1777316659371011", "get_island_group_cities", arguments)

def get_island_group_municipalities(
    islandGroupCode: str
) -> Dict[str, Any]:
    """
    Get all municipalities within a specific island group
    
    Args:
        islandGroupCode: null
    
    Returns:
        
    """
    arguments = {
        "islandGroupCode": islandGroupCode
    }
    
    return call_api("1777316659371011", "get_island_group_municipalities", arguments)

def get_island_group_barangays(
    islandGroupCode: str
) -> Dict[str, Any]:
    """
    Get all barangays within a specific island group
    
    Args:
        islandGroupCode: null
    
    Returns:
        
    """
    arguments = {
        "islandGroupCode": islandGroupCode
    }
    
    return call_api("1777316659371011", "get_island_group_barangays", arguments)

def get_regions(
) -> Dict[str, Any]:
    """
    List all regions in the Philippines
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659371011", "get_regions", arguments)

def get_region(
    code: str
) -> Dict[str, Any]:
    """
    Get specific region by code
    
    Args:
        code: null
    
    Returns:
        
    """
    arguments = {
        "code": code
    }
    
    return call_api("1777316659371011", "get_region", arguments)

def get_region_provinces(
    regionCode: str
) -> Dict[str, Any]:
    """
    Get all provinces within a specific region
    
    Args:
        regionCode: null
    
    Returns:
        
    """
    arguments = {
        "regionCode": regionCode
    }
    
    return call_api("1777316659371011", "get_region_provinces", arguments)

def get_region_districts(
    regionCode: str
) -> Dict[str, Any]:
    """
    Get all districts within a specific region
    
    Args:
        regionCode: null
    
    Returns:
        
    """
    arguments = {
        "regionCode": regionCode
    }
    
    return call_api("1777316659371011", "get_region_districts", arguments)

def get_region_cities(
    regionCode: str
) -> Dict[str, Any]:
    """
    Get all cities within a specific region
    
    Args:
        regionCode: null
    
    Returns:
        
    """
    arguments = {
        "regionCode": regionCode
    }
    
    return call_api("1777316659371011", "get_region_cities", arguments)

def get_region_municipalities(
    regionCode: str
) -> Dict[str, Any]:
    """
    Get all municipalities within a specific region
    
    Args:
        regionCode: null
    
    Returns:
        
    """
    arguments = {
        "regionCode": regionCode
    }
    
    return call_api("1777316659371011", "get_region_municipalities", arguments)

def get_region_cities_municipalities(
    regionCode: str
) -> Dict[str, Any]:
    """
    Get all cities and municipalities within a specific region
    
    Args:
        regionCode: null
    
    Returns:
        
    """
    arguments = {
        "regionCode": regionCode
    }
    
    return call_api("1777316659371011", "get_region_cities_municipalities", arguments)

def get_region_sub_municipalities(
    regionCode: str
) -> Dict[str, Any]:
    """
    Get all sub-municipalities within a specific region
    
    Args:
        regionCode: null
    
    Returns:
        
    """
    arguments = {
        "regionCode": regionCode
    }
    
    return call_api("1777316659371011", "get_region_sub_municipalities", arguments)

def get_region_barangays(
    regionCode: str
) -> Dict[str, Any]:
    """
    Get all barangays within a specific region
    
    Args:
        regionCode: null
    
    Returns:
        
    """
    arguments = {
        "regionCode": regionCode
    }
    
    return call_api("1777316659371011", "get_region_barangays", arguments)

def get_provinces(
) -> Dict[str, Any]:
    """
    List all provinces in the Philippines
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659371011", "get_provinces", arguments)

def get_province(
    code: str
) -> Dict[str, Any]:
    """
    Get specific province by code
    
    Args:
        code: null
    
    Returns:
        
    """
    arguments = {
        "code": code
    }
    
    return call_api("1777316659371011", "get_province", arguments)

def get_province_cities(
    provinceCode: str
) -> Dict[str, Any]:
    """
    Get all cities within a specific province
    
    Args:
        provinceCode: null
    
    Returns:
        
    """
    arguments = {
        "provinceCode": provinceCode
    }
    
    return call_api("1777316659371011", "get_province_cities", arguments)

def get_province_municipalities(
    provinceCode: str
) -> Dict[str, Any]:
    """
    Get all municipalities within a specific province
    
    Args:
        provinceCode: null
    
    Returns:
        
    """
    arguments = {
        "provinceCode": provinceCode
    }
    
    return call_api("1777316659371011", "get_province_municipalities", arguments)

def get_province_cities_municipalities(
    provinceCode: str
) -> Dict[str, Any]:
    """
    Get all cities and municipalities within a specific province
    
    Args:
        provinceCode: null
    
    Returns:
        
    """
    arguments = {
        "provinceCode": provinceCode
    }
    
    return call_api("1777316659371011", "get_province_cities_municipalities", arguments)

def get_province_sub_municipalities(
    provinceCode: str
) -> Dict[str, Any]:
    """
    Get all sub-municipalities within a specific province
    
    Args:
        provinceCode: null
    
    Returns:
        
    """
    arguments = {
        "provinceCode": provinceCode
    }
    
    return call_api("1777316659371011", "get_province_sub_municipalities", arguments)

def get_province_barangays(
    provinceCode: str
) -> Dict[str, Any]:
    """
    Get all barangays within a specific province
    
    Args:
        provinceCode: null
    
    Returns:
        
    """
    arguments = {
        "provinceCode": provinceCode
    }
    
    return call_api("1777316659371011", "get_province_barangays", arguments)

def get_cities(
) -> Dict[str, Any]:
    """
    List all cities in the Philippines
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659371011", "get_cities", arguments)

def get_city(
    code: str
) -> Dict[str, Any]:
    """
    Get specific city by code
    
    Args:
        code: null
    
    Returns:
        
    """
    arguments = {
        "code": code
    }
    
    return call_api("1777316659371011", "get_city", arguments)

def get_city_barangays(
    cityCode: str
) -> Dict[str, Any]:
    """
    Get all barangays within a specific city
    
    Args:
        cityCode: null
    
    Returns:
        
    """
    arguments = {
        "cityCode": cityCode
    }
    
    return call_api("1777316659371011", "get_city_barangays", arguments)

def get_municipalities(
) -> Dict[str, Any]:
    """
    List all municipalities in the Philippines
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659371011", "get_municipalities", arguments)

def get_municipality(
    code: str
) -> Dict[str, Any]:
    """
    Get specific municipality by code
    
    Args:
        code: null
    
    Returns:
        
    """
    arguments = {
        "code": code
    }
    
    return call_api("1777316659371011", "get_municipality", arguments)

def get_municipality_barangays(
    municipalityCode: str
) -> Dict[str, Any]:
    """
    Get all barangays within a specific municipality
    
    Args:
        municipalityCode: null
    
    Returns:
        
    """
    arguments = {
        "municipalityCode": municipalityCode
    }
    
    return call_api("1777316659371011", "get_municipality_barangays", arguments)

def get_barangays(
) -> Dict[str, Any]:
    """
    List all barangays in the Philippines
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659371011", "get_barangays", arguments)

def get_barangay(
    code: str
) -> Dict[str, Any]:
    """
    Get specific barangay by code
    
    Args:
        code: null
    
    Returns:
        
    """
    arguments = {
        "code": code
    }
    
    return call_api("1777316659371011", "get_barangay", arguments)

def get_districts(
) -> Dict[str, Any]:
    """
    List all districts in the Philippines
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659371011", "get_districts", arguments)

def get_district(
    code: str
) -> Dict[str, Any]:
    """
    Get specific district by code
    
    Args:
        code: null
    
    Returns:
        
    """
    arguments = {
        "code": code
    }
    
    return call_api("1777316659371011", "get_district", arguments)

def get_district_cities(
    districtCode: str
) -> Dict[str, Any]:
    """
    Get all cities within a specific district
    
    Args:
        districtCode: null
    
    Returns:
        
    """
    arguments = {
        "districtCode": districtCode
    }
    
    return call_api("1777316659371011", "get_district_cities", arguments)

def get_district_municipalities(
    districtCode: str
) -> Dict[str, Any]:
    """
    Get all municipalities within a specific district
    
    Args:
        districtCode: null
    
    Returns:
        
    """
    arguments = {
        "districtCode": districtCode
    }
    
    return call_api("1777316659371011", "get_district_municipalities", arguments)

def get_district_cities_municipalities(
    districtCode: str
) -> Dict[str, Any]:
    """
    Get all cities and municipalities within a specific district
    
    Args:
        districtCode: null
    
    Returns:
        
    """
    arguments = {
        "districtCode": districtCode
    }
    
    return call_api("1777316659371011", "get_district_cities_municipalities", arguments)

def get_district_sub_municipalities(
    districtCode: str
) -> Dict[str, Any]:
    """
    Get all sub-municipalities within a specific district
    
    Args:
        districtCode: null
    
    Returns:
        
    """
    arguments = {
        "districtCode": districtCode
    }
    
    return call_api("1777316659371011", "get_district_sub_municipalities", arguments)

def get_district_barangays(
    districtCode: str
) -> Dict[str, Any]:
    """
    Get all barangays within a specific district
    
    Args:
        districtCode: null
    
    Returns:
        
    """
    arguments = {
        "districtCode": districtCode
    }
    
    return call_api("1777316659371011", "get_district_barangays", arguments)

def search_by_name(
    name: str,
    type: Optional[str] = None,
    limit: Optional[int] = 10.0
) -> Dict[str, Any]:
    """
    Search for geographic entities by name across all levels (regions, provinces, cities, municipalities, barangays)
    
    Args:
        name: null
        type: null
        limit: null
    
    Returns:
        
    """
    arguments = {
        "name": name,
        "type": type,
        "limit": limit
    }
    
    return call_api("1777316659371011", "search_by_name", arguments)

def get_hierarchy(
    code: str
) -> Dict[str, Any]:
    """
    Get complete geographic hierarchy for a specific code (shows parent entities)
    
    Args:
        code: null
    
    Returns:
        
    """
    arguments = {
        "code": code
    }
    
    return call_api("1777316659371011", "get_hierarchy", arguments)

def validate_code(
    code: str
) -> Dict[str, Any]:
    """
    Validate if a geographic code exists and return its type
    
    Args:
        code: null
    
    Returns:
        
    """
    arguments = {
        "code": code
    }
    
    return call_api("1777316659371011", "validate_code", arguments)

