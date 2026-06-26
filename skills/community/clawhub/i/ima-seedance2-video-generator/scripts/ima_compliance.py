"""
IMA Asset Compliance Verification Module
Version: 1.0.0

Handles asset compliance verification before video generation.
All media inputs must be verified to ensure platform compliance.
"""

import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

from ima_constants import (
    ASSET_TYPES,
    VERIFICATION_STATUS,
    DEFAULT_BASE_URL,
    COMPLIANCE_REQUIRED_TASK_TYPES
)
from ima_logger import log_info, log_error, log_debug

# Import event stream for Agent integration
try:
    from ima_events import emit_prompt, emit_compliance_check, emit_info, emit_warning, human_print
    EVENT_STREAM_ENABLED = True
except ImportError:
    # Fallback: no-op implementations
    EVENT_STREAM_ENABLED = False
    def emit_prompt(message, options, default=None, timeout=None): return default or options[0]
    def emit_compliance_check(*args, **kwargs): pass
    def emit_info(*args, **kwargs): pass
    def emit_warning(*args, **kwargs): pass
    def human_print(*args, **kwargs): print(*args, **kwargs)

# ─── Type Definitions ─────────────────────────────────────────────────────────

class AssetVerificationError(Exception):
    """Raised when asset verification fails."""
    pass

class UserDeclinedVerificationError(Exception):
    """Raised when user declines compliance verification."""
    pass

# ─── Asset Type Detection ─────────────────────────────────────────────────────

def detect_asset_type(file_path_or_url: str) -> Optional[str]:
    """
    Detect if a file path or URL is image, video, or audio.
    
    Args:
        file_path_or_url: Local file path or remote URL
        
    Returns:
        "image", "video", "audio", or None if unknown
    """
    path_lower = file_path_or_url.lower()
    
    # Check file extension
    for asset_type, extensions in ASSET_TYPES.items():
        for ext in extensions:
            if path_lower.endswith(ext):
                return asset_type
    
    return None

def is_local_file(path: str) -> bool:
    """Check if path is a local file (not a URL)."""
    return not path.startswith(("http://", "https://"))

# ─── User Consent ─────────────────────────────────────────────────────────────

def prompt_compliance_consent(file_paths: List[str]) -> bool:
    """
    Prompt user for compliance verification consent.
    
    Args:
        file_paths: List of file paths/URLs to be verified
        
    Returns:
        True if user consents, False otherwise
        
    Raises:
        UserDeclinedVerificationError: If user declines
    """
    human_print("\n" + "━" * 70)
    human_print("🔍 Asset Compliance Verification Required")
    human_print("━" * 70)
    human_print()
    human_print("WHY THIS IS NEEDED:")
    human_print("  To ensure the best video generation results and comply with")
    human_print("  platform policies, your input media must be verified.")
    human_print()
    human_print("WHAT HAPPENS:")
    human_print("  ✓ Compliance check (may take up to 5 minutes)")
    human_print("  ✓ Improves generation success rate")
    human_print("  ✓ Prevents compliance issues")
    human_print("  ✓ Ensures professional-quality output")
    human_print()
    human_print("WHAT WE CHECK:")
    human_print("  • Content appropriateness (no prohibited content)")
    human_print("  • Media quality (resolution, clarity, technical validity)")
    human_print("  • File integrity (not corrupted)")
    human_print("  • Platform policy compliance")
    human_print()
    
    if file_paths:
        human_print(f"FILES TO VERIFY ({len(file_paths)}):")
        for i, path in enumerate(file_paths, 1):
            if is_local_file(path):
                filename = Path(path).name
                filesize = os.path.getsize(path) if os.path.isfile(path) else 0
                size_kb = filesize / 1024
                human_print(f"  {i}. {filename} ({size_kb:.1f} KB)")
            else:
                url_display = path[:60] + "..." if len(path) > 60 else path
                human_print(f"  {i}. {url_display}")
        human_print()

    human_print("This is a one-time check per generation task.")
    human_print("Your media files are only analyzed, not stored or shared.")
    human_print("Read more: https://www.imaclaw.ai/compliance")
    human_print()
    
    # Check for auto-consent via environment variable
    auto_consent = os.environ.get("IMA_AUTO_CONSENT", "").strip().lower() in ("1", "true", "yes", "y")
    
    if auto_consent:
        human_print("✅ Auto-consent enabled (IMA_AUTO_CONSENT=1). Starting verification...\n")
        emit_info("Auto-consent enabled, proceeding with verification")
        return True
    
    # Get user consent via interactive prompt (SKILL.md Rule 4: STOP on verification, offer options)
    try:
        response = emit_prompt(
            message=f"Asset compliance verification required for {len(file_paths)} file(s). Proceed?",
            options=["yes", "no", "y", "n"],
            default="yes"
        )
        
        if response in ("yes", "y"):
            human_print("\n✅ Consent received. Starting verification...\n")
            emit_info("User consented to compliance verification")
            return True
        else:
            human_print("\n❌ Verification declined.")
            human_print("   Note: Verification is required for media-based generation.")
            human_print("   To continue, you must consent to asset verification.\n")
            emit_warning("User declined asset verification")
            raise UserDeclinedVerificationError("User declined asset verification")
            
    except KeyboardInterrupt:
        human_print("\n\n❌ Verification canceled by user.")
        human_print("   Tip: Press Ctrl+C again to exit completely.\n")
        raise UserDeclinedVerificationError("User canceled verification")
    except EOFError:
        # Non-interactive environment (background execution)
        human_print("\n❌ Non-interactive environment detected.")
        human_print("   Tip: Set IMA_AUTO_CONSENT=1 to skip confirmation in background jobs.\n")
        raise UserDeclinedVerificationError("Non-interactive environment without auto-consent")

# ─── API: Asset Verification ──────────────────────────────────────────────────

def verify_asset(
    base_url: str,
    api_key: str,
    asset_url: str,
    asset_name: Optional[str] = None
) -> Dict:
    """
    Verify a single asset for compliance.
    
    Args:
        base_url: API base URL
        api_key: IMA API key
        asset_url: URL of asset to verify
        asset_name: Optional asset name (max 64 chars)
        
    Returns:
        Verification result dict with structure:
        {
            "id": "asset_123",
            "name": "asset.jpg",
            "url": "https://...",
            "group_id": "...",
            "asset_type": "image|video|audio",
            "status": "success|failed|processing",
            "error": {"code": "...", "message": "..."},
            "project_name": "...",
            "create_time": "...",
            "update_time": "..."
        }
        
    Raises:
        AssetVerificationError: If verification request fails or asset rejected
    """
    url = f"{base_url}/open/v1/assets/verify"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "IMA-OpenAPI-Client/ima-seedance2-video-generator_1.0.0",
        "x-app-source": "ima_skills",
        "x_app_language": "en",
    }
    
    payload = {"url": asset_url}
    
    # Add optional name (max 64 chars)
    if asset_name:
        payload["name"] = asset_name[:64]
    
    log_debug(f"Verifying asset: {asset_url}")
    
    try:
        # API is synchronous but may take up to 5 minutes to complete verification
        response = requests.post(url, json=payload, headers=headers, timeout=300)
        
        # Parse JSON response (don't check HTTP status first!)
        try:
            data = response.json()
            log_debug(f"Verification API response: HTTP {response.status_code}, code={data.get('code')}")
        except ValueError as json_err:
            # Non-JSON response indicates HTTP-level error
            log_error(f"Verification API returned non-JSON response: "
                     f"HTTP {response.status_code}, body={response.text[:200]}")
            raise RuntimeError(
                f"Verification API returned non-JSON response (HTTP {response.status_code})"
            ) from json_err
        
        # Check business code (0 or 200 = success)
        code = data.get("code")
        if code not in (0, 200):
            message = data.get("message") or "Unknown error"
            
            if code == 401:
                error_msg = f"IMA API Key unauthorized (code=401): {message}"
                log_error(error_msg)
                raise RuntimeError(error_msg)
            else:
                error_msg = f"Verification API error: code={code}, msg={message}"
                log_error(error_msg)
                raise RuntimeError(error_msg)
        
        # Success - return result
        result = data.get("data", {}).get("result", {})
        log_debug(f"Verification result: status={result.get('status')}, asset={asset_url}")
        
        return result
        
    except requests.exceptions.RequestException as e:
        # Network-level error
        error_details = f"HTTP {e.response.status_code}" if hasattr(e, 'response') and e.response else str(e)
        log_error(f"Asset verification request failed: {error_details}")
        raise AssetVerificationError(f"Verification request failed: {error_details}") from e

def check_verification_result(result: Dict, asset_name: str) -> None:
    """
    Check verification result and raise error if failed.
    
    Args:
        result: Verification result from verify_asset()
        asset_name: Name of asset for error messages
        
    Raises:
        AssetVerificationError: If verification failed or still processing
    """
    status = result.get("status", "").lower()
    
    # ✅ FIX: API returns "Active" for successful verification (not "success")
    if status == VERIFICATION_STATUS["SUCCESS"] or status == "active":
        log_info(f"✅ Verified: {asset_name} (asset_id: {result.get('id')})")
        return
    
    elif status == VERIFICATION_STATUS["FAILED"]:
        error_info = result.get("error", {})
        error_msg = error_info.get("message", "Unknown error")
        error_code = error_info.get("code", "")
        
        log_error(f"❌ Verification failed: {asset_name}")
        
        human_print("\n" + "━" * 70)
        human_print("❌ Asset Verification Failed")
        human_print("━" * 70)
        human_print()
        human_print(f"Asset: {asset_name}")
        human_print(f"Reason: {error_msg}")
        if error_code:
            human_print(f"Error Code: {error_code}")
        human_print()
        human_print("The input media contains content that cannot be processed.")
        human_print("Please ensure your media complies with platform policies.")
        human_print()
        human_print("For more information: https://www.imaclaw.ai/compliance")
        human_print("━" * 70)
        human_print()
        
        raise AssetVerificationError(f"Asset verification failed: {error_msg}")
    
    elif status == VERIFICATION_STATUS["PROCESSING"]:
        log_error(f"⏳ Still processing: {asset_name}")
        raise AssetVerificationError(
            f"Asset still processing. Please try again later."
        )
    
    else:
        log_error(f"Unknown status: {status}")
        raise AssetVerificationError(f"Unknown verification status: {status}")

# ─── Batch Verification ───────────────────────────────────────────────────────

def verify_assets_batch(
    base_url: str,
    api_key: str,
    urls: List[str],
    names: Optional[List[str]] = None,
    max_workers: int = 3
) -> List[Dict]:
    """
    Verify multiple assets in parallel.
    
    Args:
        base_url: API base URL
        api_key: IMA API key
        urls: List of asset URLs to verify
        names: Optional list of asset names (same length as urls)
        max_workers: Maximum number of parallel verification workers (default: 3)
        
    Returns:
        List of verification results (one per URL, order preserved)
        
    Raises:
        AssetVerificationError: If any verification fails
    """
    if not urls:
        return []
    
    human_print("\n🔍 Verifying asset compliance...")
    human_print(f"   Processing {len(urls)} asset(s) in parallel (max {max_workers} concurrent)...")
    
    names = names or [None] * len(urls)
    
    # Prepare verification tasks
    tasks = []
    for idx, (url, name) in enumerate(zip(urls, names)):
        display_name = name or Path(url).name
        tasks.append((idx, url, name, display_name))
    
    # Results dictionary to preserve order
    results_dict = {}
    failed_assets = []
    
    # Execute verifications in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_task = {
            executor.submit(verify_asset, base_url, api_key, url, name): (idx, display_name)
            for idx, url, name, display_name in tasks
        }
        
        # Process completed tasks as they finish
        completed = 0
        total = len(urls)
        
        for future in as_completed(future_to_task):
            idx, display_name = future_to_task[future]
            completed += 1
            
            try:
                result = future.result()
                
                # Check verification result
                check_verification_result(result, display_name)
                
                # Store result with original index
                results_dict[idx] = result
                
                human_print(f"  ✅ [{completed}/{total}] Verified: {display_name}")
                
            except AssetVerificationError as e:
                # Verification failed - record error
                failed_assets.append((display_name, str(e)))
                human_print(f"  ❌ [{completed}/{total}] Failed: {display_name}")
            
            except Exception as e:
                # Unexpected error
                log_error(f"Unexpected error verifying {display_name}: {e}")
                failed_assets.append((display_name, f"Unexpected error: {e}"))
                human_print(f"  ❌ [{completed}/{total}] Error: {display_name}")
    
    # Check for failures
    if failed_assets:
        human_print("\n❌ Asset verification failed!")
        human_print(f"   {len(failed_assets)} of {total} asset(s) failed verification.\n")
        
        for asset_name, error_msg in failed_assets:
            human_print(f"  • {asset_name}: {error_msg}")
        human_print()
        
        # Raise error for first failed asset
        raise AssetVerificationError(
            f"Asset verification failed: {failed_assets[0][1]}"
        )
    
    # Return results in original order
    results = [results_dict[i] for i in range(len(urls))]
    
    human_print(f"\n✅ All {len(results)} asset(s) verified successfully!\n")
    return results

# ─── Task Type Check ──────────────────────────────────────────────────────────

def requires_compliance_verification(task_type: str) -> bool:
    """
    Check if a task type requires asset compliance verification.
    
    Args:
        task_type: Task type (e.g., "image_to_video")
        
    Returns:
        True if compliance verification is required
    """
    return task_type in COMPLIANCE_REQUIRED_TASK_TYPES

# ─── High-Level Flow ──────────────────────────────────────────────────────────

def verify_compliance_flow(
    base_url: str,
    api_key: str,
    task_type: str,
    media_paths: List[str],
    uploaded_urls: Optional[List[str]] = None
) -> Tuple[bool, List[Dict]]:
    """
    Complete compliance verification flow with user consent.
    
    This is the main entry point for compliance verification.
    
    Args:
        base_url: API base URL
        api_key: IMA API key
        task_type: Task type (e.g., "image_to_video")
        media_paths: Original file paths (local or remote)
        uploaded_urls: URLs after upload (if local files were uploaded)
        
    Returns:
        Tuple of (success: bool, verification_results: List[Dict])
        
    Raises:
        UserDeclinedVerificationError: If user declines
        AssetVerificationError: If verification fails
    """
    # Check if verification is needed
    if not requires_compliance_verification(task_type):
        log_debug(f"Task type {task_type} does not require compliance verification")
        return (True, [])
    
    if not media_paths:
        log_debug("No media paths provided, skipping verification")
        return (True, [])
    
    urls_to_verify = uploaded_urls if uploaded_urls else media_paths

    asset_pairs = []
    for original_path, uploaded_url in zip(media_paths, urls_to_verify):
        asset_type = detect_asset_type(original_path) or detect_asset_type(uploaded_url)
        if asset_type in ASSET_TYPES:
            asset_pairs.append((original_path, uploaded_url))

    if not asset_pairs:
        log_debug("No supported media inputs found, skipping compliance verification")
        return (True, [])

    asset_paths = [pair[0] for pair in asset_pairs]
    asset_urls = [pair[1] for pair in asset_pairs]

    # Step 1: Get user consent for all supported media inputs
    prompt_compliance_consent(asset_paths)

    # Extract names from original media paths
    names = [Path(p).stem for p in asset_paths]

    # Step 2: Verify all supported media assets
    results = verify_assets_batch(base_url, api_key, asset_urls, names)
    
    return (True, results)
