from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def analyze_android_project(
    project_path: str
) -> Dict[str, Any]:
    """
    Analyze an Android project to understand its configuration and identify requirements for Play Store deployment


Args:

    project_path: Absolute path to the Android project root directory



Returns:
    Result from analyze_android_project

    
    Args:
        project_path: null
    
    Returns:
        null
    """
    arguments = {
        "project_path": project_path
    }
    
    return call_api("1777419073082371", "analyze_android_project", arguments)

def generate_keystore(
    output_path: str,
    alias: str,
    key_password: str,
    store_password: str,
    validity_days: Optional[int] = None,
    key_size: Optional[int] = None,
    dname: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate a new Android keystore file for app signing with secure parameters


Args:

    output_path: Absolute path where the keystore will be saved

    alias: Key alias for the signing key

    key_password: Password for the signing key

    store_password: Password for the keystore

    validity_days: How many days the key should be valid

    key_size: Key size in bits

    dname: Distinguished name for the certificate



Returns:
    Result from generate_keystore

    
    Args:
        output_path: null
        alias: null
        key_password: null
        store_password: null
        validity_days: null
        key_size: null
        dname: null
    
    Returns:
        null
    """
    arguments = {
        "output_path": output_path,
        "alias": alias,
        "key_password": key_password,
        "store_password": store_password,
        "validity_days": validity_days,
        "key_size": key_size,
        "dname": dname
    }
    
    return call_api("1777419073082371", "generate_keystore", arguments)

def generate_signing_config(
    project_path: str,
    env_var_prefix: Optional[str] = "APP_"
) -> Dict[str, Any]:
    """
    Generate Gradle signing configuration with dual-source support

Generates signing configuration that works seamlessly for both local development and CI/CD:
- Environment variables (prioritized for CI/CD)
- gradle.properties fallback (for local development)
- Task-based validation (debug builds always work)

Automatically generates gradle.properties.template for easy local setup.

Args:

    project_path: Path to Android project

    env_var_prefix: Prefix for environment variables (default: "APP_")
                   Example: "APP_" creates APP_SIGNING_KEY_STORE_PATH
                   Use "" for no prefix


Returns:
    Result including gradle_config_kotlin, gradle_properties_template, and setup instructions

    
    Args:
        project_path: null
        env_var_prefix: null
    
    Returns:
        null
    """
    arguments = {
        "project_path": project_path,
        "env_var_prefix": env_var_prefix
    }
    
    return call_api("1777419073082371", "generate_signing_config", arguments)

def setup_service_account_guide(
) -> Dict[str, Any]:
    """
    Provide interactive step-by-step guide for setting up Google Play Service Account


Returns:
    Result from setup_service_account_guide

    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419073082371", "setup_service_account_guide", arguments)

def generate_github_workflow(
    project_path: str,
    package_name: str,
    track: Optional[str] = None,
    trigger_strategy: Optional[str] = None,
    branch_name: Optional[str] = None,
    app_module_path: Optional[str] = None,
    java_version: Optional[str] = None,
    enforce_proguard: Optional[bool] = True,
    mapping_file_path: Optional[str] = None,
    include_release_notes: Optional[bool] = True,
    release_notes_directory: Optional[str] = None,
    env_var_prefix: Optional[str] = "APP_"
) -> Dict[str, Any]:
    """
    Generate a complete GitHub Actions workflow file for Play Store deployment


Args:

    project_path: Path to Android project

    package_name: Android app package name

    track: Play Store release track (internal, alpha, beta, production)

    trigger_strategy: How to trigger the workflow (manual, branch, tag)

    branch_name: Branch name to trigger on if trigger_strategy is branch

    app_module_path: Path to app module relative to project root

    java_version: Java/JDK version to use for builds

    enforce_proguard: If True, ensure isMinifyEnabled=true in build.gradle.kts (default: True)

    mapping_file_path: Override default ProGuard mapping file path

    include_release_notes: Include release notes directory (default: True)

    release_notes_directory: Path to release notes directory (default: distribution/whatsnew)

    env_var_prefix: Prefix for environment variables (default: "APP_")
                   Example: "APP_" creates APP_SIGNING_KEY_STORE_PATH
                   Use "" for no prefix



Returns:
    Result from generate_github_workflow

    
    Args:
        project_path: null
        package_name: null
        track: null
        trigger_strategy: null
        branch_name: null
        app_module_path: null
        java_version: null
        enforce_proguard: null
        mapping_file_path: null
        include_release_notes: null
        release_notes_directory: null
        env_var_prefix: null
    
    Returns:
        null
    """
    arguments = {
        "project_path": project_path,
        "package_name": package_name,
        "track": track,
        "trigger_strategy": trigger_strategy,
        "branch_name": branch_name,
        "app_module_path": app_module_path,
        "java_version": java_version,
        "enforce_proguard": enforce_proguard,
        "mapping_file_path": mapping_file_path,
        "include_release_notes": include_release_notes,
        "release_notes_directory": release_notes_directory,
        "env_var_prefix": env_var_prefix
    }
    
    return call_api("1777419073082371", "generate_github_workflow", arguments)

def validate_github_secrets(
    repo_owner: str,
    repo_name: str,
    github_token: str,
    required_secrets: Optional[str] = None
) -> Dict[str, Any]:
    """
    Validate that required GitHub Secrets are configured (checks existence only)


Args:

    repo_owner: GitHub repository owner username or organization

    repo_name: GitHub repository name

    github_token: GitHub Personal Access Token with repo scope

    required_secrets: List of secret names to check for



Returns:
    Result from validate_github_secrets

    
    Args:
        repo_owner: null
        repo_name: null
        github_token: null
        required_secrets: null
    
    Returns:
        null
    """
    arguments = {
        "repo_owner": repo_owner,
        "repo_name": repo_name,
        "github_token": github_token,
        "required_secrets": required_secrets
    }
    
    return call_api("1777419073082371", "validate_github_secrets", arguments)

def create_github_secrets_guide(
    repo_url: str,
    keystore_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate a comprehensive guide for creating all required GitHub Secrets


Args:

    repo_url: GitHub repository URL

    keystore_path: Optional path to keystore for encoding instructions



Returns:
    Result from create_github_secrets_guide

    
    Args:
        repo_url: null
        keystore_path: null
    
    Returns:
        null
    """
    arguments = {
        "repo_url": repo_url,
        "keystore_path": keystore_path
    }
    
    return call_api("1777419073082371", "create_github_secrets_guide", arguments)

def validate_play_store_setup(
    service_account_json_path: str,
    package_name: str
) -> Dict[str, Any]:
    """
    Validate that Play Store app and API access are properly configured using service account


Args:

    service_account_json_path: Path to service account JSON file

    package_name: Android app package name to validate



Returns:
    Result from validate_play_store_setup

    
    Args:
        service_account_json_path: null
        package_name: null
    
    Returns:
        null
    """
    arguments = {
        "service_account_json_path": service_account_json_path,
        "package_name": package_name
    }
    
    return call_api("1777419073082371", "validate_play_store_setup", arguments)

def test_deployment_workflow(
    project_path: str,
    keystore_path: str,
    store_password: str,
    key_alias: str,
    key_password: str,
    dry_run: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Test the deployment workflow locally without uploading to Play Store


Args:

    project_path: Path to Android project

    keystore_path: Path to keystore file

    store_password: Keystore password

    key_alias: Key alias

    key_password: Key password

    dry_run: If true, skip actual Play Store upload



Returns:
    Result from test_deployment_workflow

    
    Args:
        project_path: null
        keystore_path: null
        store_password: null
        key_alias: null
        key_password: null
        dry_run: null
    
    Returns:
        null
    """
    arguments = {
        "project_path": project_path,
        "keystore_path": keystore_path,
        "store_password": store_password,
        "key_alias": key_alias,
        "key_password": key_password,
        "dry_run": dry_run
    }
    
    return call_api("1777419073082371", "test_deployment_workflow", arguments)

