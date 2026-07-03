from .common import *

def list_supported_regions() -> Dict[str, Any]:
    """List all supported Huawei Cloud regions
    
    Returns:
        Dict with success status and list of supported regions
    """
    regions = []
    
    # 中国大陆区域
    china_regions = []
    for region_id, info in SUPPORTED_REGIONS.items():
        if region_id.startswith("cn-"):
            china_regions.append({
                "region_id": region_id,
                "name": info["name"],
                "description": info["description"]
            })
    
    # 国际区域
    international_regions = []
    for region_id, info in SUPPORTED_REGIONS.items():
        if not region_id.startswith("cn-"):
            international_regions.append({
                "region_id": region_id,
                "name": info["name"],
                "description": info["description"]
            })
    
    return {
        "success": True,
        "action": "list_supported_regions",
        "total_count": len(SUPPORTED_REGIONS),
        "china_mainland": {
            "count": len(china_regions),
            "regions": china_regions
        },
        "international": {
            "count": len(international_regions),
            "regions": international_regions
        }
    }

def list_projects(ak: Optional[str] = None, sk: Optional[str] = None, domain_id: Optional[str] = None, region: Optional[str] = None) -> Dict[str, Any]:
    """List all projects (tenants) available for the account using IAM API

    This function queries IAM to get all project information associated with the account.
    You can optionally filter by domain_id or specific region name.

    Args:
        ak: Access Key ID (optional, will use HUAWEI_AK env var if not provided)
        sk: Secret Access Key (optional, will use HUAWEI_SK env var if not provided)
        domain_id: Filter by domain ID (optional)
        region: Filter by region name (e.g., 'cn-north-4'). If provided, will return project for this region.

    Returns:
        Dictionary with project information including project_id, name, region, etc.
    """
    from huaweicloudsdkiam.v3 import KeystoneListProjectsRequest

    access_key, secret_key, _ = get_credentials(ak, sk, None)

    if not access_key or not secret_key:
        return {
            "success": False,
            "error": "Credentials not provided. Set HUAWEI_AK and HUAWEI_SK environment variables or pass as parameters."
        }

    if not SDK_AVAILABLE:
        return {
            "success": False,
            "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"
        }

    try:
        client = create_iam_client(access_key, secret_key)

        # Build the request - use keystone API for listing projects
        request = KeystoneListProjectsRequest()
        if domain_id:
            request.domain_id = domain_id

        # Execute the request - keystone API uses keystone_list_projects
        response = client.keystone_list_projects(request)

        projects = []
        # Keystone API returns projects in a different format
        if hasattr(response, 'projects') and response.projects:
            for project in response.projects:
                project_info = {
                    "id": project.id,
                    "name": project.name,
                    "domain_id": getattr(project, 'domain_id', None),
                    "enabled": getattr(project, 'enabled', None),
                    "description": getattr(project, 'description', None),
                }

                # Extract region from project name (e.g., "cn-north-4" -> region)
                if project.name:
                    # Project names typically match region IDs in Huawei Cloud
                    project_info["region"] = project.name

                projects.append(project_info)
        elif hasattr(response, 'keystone_projects') and response.keystone_projects:
            # Alternative attribute name
            for project in response.keystone_projects:
                project_info = {
                    "id": project.id,
                    "name": project.name,
                    "domain_id": getattr(project, 'domain_id', None),
                    "enabled": getattr(project, 'enabled', None),
                    "description": getattr(project, 'description', None),
                }

                if project.name:
                    project_info["region"] = project.name

                projects.append(project_info)

        # If region parameter provided, filter results
        if region:
            projects = [p for p in projects if p.get('name') == region or p.get('region') == region]

        # Build result with region to project ID mapping
        region_to_project = {}
        for p in projects:
            if p.get('name'):
                region_to_project[p['name']] = p['id']

        return {
            "success": True,
            "action": "list_projects",
            "domain_id": domain_id,
            "region_filter": region,
            "count": len(projects),
            "projects": projects,
            "region_to_project_mapping": region_to_project
        }

    except ClientRequestException as e:
        return {
            "success": False,
            "error": f"{e.error_code} - {e.error_msg}",
            "request_id": getattr(e, 'request_id', None)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }

def get_project_by_region(region: str, ak: Optional[str] = None, sk: Optional[str] = None) -> Dict[str, Any]:
    """Get project ID for a specific region

    This is a convenience function that queries IAM and returns the project ID
    for the specified region name.

    Args:
        region: Region name (e.g., 'cn-north-4', 'cn-east-3', etc.)
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)

    Returns:
        Dictionary with project_id for the specified region

    Example:
        >>> get_project_by_region("cn-north-4")
        {"success": True, "region": "cn-north-4", "project_id": "xxx...xxx"}
    """
    access_key, secret_key, _ = get_credentials(ak, sk, None)

    if not access_key or not secret_key:
        return {
            "success": False,
            "error": "Credentials not provided. Set HUAWEI_AK and HUAWEI_SK environment variables or pass as parameters."
        }

    if not region:
        return {
            "success": False,
            "error": "region is required"
        }

    # Get all projects and filter
    result = list_projects(ak, sk, region=region)

    if result.get('success') and result.get('count', 0) > 0:
        project = result['projects'][0]
        return {
            "success": True,
            "action": "get_project_by_region",
            "region": region,
            "project_id": project['id'],
            "project_name": project.get('name'),
            "domain_id": project.get('domain_id'),
            "enabled": project.get('enabled')
        }
    else:
        return {
            "success": False,
            "error": f"No project found for region: {region}",
            "available_regions": list(result.get('region_to_project_mapping', {}).keys()) if result.get('success') else None
        }

