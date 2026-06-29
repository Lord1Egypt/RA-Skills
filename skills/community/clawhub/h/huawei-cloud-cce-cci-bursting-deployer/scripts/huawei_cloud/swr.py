"""SWR basic edition helpers used by CCE to CCI bursting workflows."""

from __future__ import annotations

import json
from typing import Any, Dict, Iterable, Optional
from urllib.parse import quote

import requests
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.sdk_request import SdkRequest
from huaweicloudsdkcore.signer.signer import Signer

from .common import get_credentials_with_region


def _records(payload: Any, *keys: str) -> list[Dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if not isinstance(payload, dict):
        return []
    for key in keys:
        value = payload.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    return []


def _signed_swr_get(
    region: str,
    resource_path: str,
    query_params: Optional[Iterable[tuple[str, str]]],
    ak: str,
    sk: str,
    project_id: str,
) -> Any:
    host = f"swr-api.{region}.myhuaweicloud.com"
    request = SdkRequest(
        method="GET",
        schema="https",
        host=host,
        resource_path=resource_path,
        query_params=list(query_params or []),
        header_params={
            "Content-Type": "application/json",
            "X-Project-Id": project_id,
        },
    )
    signed = Signer(BasicCredentials(ak, sk, project_id)).sign(request)
    response = requests.get(
        f"{signed.schema}://{signed.host}{signed.uri}",
        headers=signed.header_params,
        timeout=30,
    )
    if response.status_code < 200 or response.status_code >= 300:
        raise RuntimeError(f"SWR API HTTP {response.status_code}: {response.text[:500]}")
    if not response.text:
        return {}
    return response.json()


def discover_swr_smoke_images(
    region: str,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
    max_namespaces: int = 20,
    max_repositories: int = 20,
    max_tags_per_repository: int = 5,
) -> Dict[str, Any]:
    """Discover tenant-owned SWR basic edition images for CCI smoke tests.

    The lookup deliberately follows the basic edition API sequence:
    namespaces -> repos filtered by namespace -> tags for each repository.
    """
    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
    if not access_key or not secret_key:
        return {
            "success": False,
            "error": "Credentials not provided. Set HUAWEI_AK and HUAWEI_SK environment variables or pass as parameters.",
        }
    if not proj_id:
        return {
            "success": False,
            "error": "Project ID not found. Pass project_id or ensure the account can access the region.",
        }

    try:
        namespaces_payload = _signed_swr_get(
            region,
            "/v2/manage/namespaces",
            None,
            access_key,
            secret_key,
            proj_id,
        )
        namespace_items = _records(namespaces_payload, "namespaces")
        namespaces = []
        for item in namespace_items:
            name = item.get("name") or item.get("namespace")
            if name and str(name) not in namespaces:
                namespaces.append(str(name))
        namespaces = namespaces[: max(1, max_namespaces)]

        candidates = []
        repositories = []
        for namespace in namespaces:
            repos_payload = _signed_swr_get(
                region,
                "/v2/manage/repos",
                [("namespace", namespace), ("limit", str(max(1, max_repositories)))],
                access_key,
                secret_key,
                proj_id,
            )
            repo_items = _records(repos_payload, "repositories", "repos")
            for repo in repo_items[: max(1, max_repositories)]:
                repository = repo.get("name") or repo.get("repository") or repo.get("repo_name")
                if not repository:
                    continue
                repository = str(repository)
                tags_payload = _signed_swr_get(
                    region,
                    f"/v2/manage/namespaces/{quote(namespace, safe='')}/repos/{quote(repository, safe='')}/tags",
                    [("limit", str(max(1, max_tags_per_repository)))],
                    access_key,
                    secret_key,
                    proj_id,
                )
                tag_items = _records(tags_payload, "tags")
                tags = []
                for tag_item in tag_items:
                    tag = tag_item.get("tag") or tag_item.get("name")
                    if tag:
                        tags.append(str(tag))
                repositories.append(
                    {
                        "namespace": namespace,
                        "repository": repository,
                        "tags": tags,
                    }
                )
                for tag in tags:
                    candidates.append(
                        {
                            "namespace": namespace,
                            "repository": repository,
                            "tag": tag,
                            "image": f"swr.{region}.myhuaweicloud.com/{namespace}/{repository}:{tag}",
                            "source": "tenant-owned-swr-basic",
                        }
                    )

        return {
            "success": True,
            "action": "discover_swr_smoke_images",
            "region": region,
            "project_id": proj_id,
            "lookup_sequence": [
                "ListNamespaces",
                "ListReposDetails(namespace=<tenant-namespace>)",
                "ListRepositoryTags(namespace=<tenant-namespace>, repository=<repository>)",
            ],
            "namespace_count": len(namespaces),
            "namespaces": namespaces,
            "repository_count": len(repositories),
            "repositories": repositories,
            "candidate_count": len(candidates),
            "candidates": candidates,
        }
    except requests.RequestException as exc:
        return {"success": False, "error": str(exc), "error_type": type(exc).__name__}
    except json.JSONDecodeError as exc:
        return {"success": False, "error": f"Invalid SWR response JSON: {exc}"}
    except Exception as exc:
        return {"success": False, "error": str(exc), "error_type": type(exc).__name__}

