#!/usr/bin/env python3
"""
LoopAI App Publish

Create and publish apps to the App Hub showcase center.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import requests


def check_url_accessible(url: str, timeout: int = 10, verbose: bool = False) -> tuple:
    """
    Use curl to verify that a URL is accessible.
    
    Returns:
        (is_accessible: bool, status_code_or_error: str)
    """
    try:
        result = subprocess.run(
            [
                'curl', '-s', '-o', '/dev/null',
                '-w', '%{http_code}',
                '-L',  # follow redirects
                '--max-time', str(timeout),
                url
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout + 5
        )
        # Decode bytes to str for Python 3.6 compat
        result.stdout = result.stdout.decode('utf-8', errors='replace') if isinstance(result.stdout, bytes) else result.stdout
        result.stderr = result.stderr.decode('utf-8', errors='replace') if isinstance(result.stderr, bytes) else result.stderr
        
        http_code = result.stdout.strip()
        
        if verbose:
            print(f"[DEBUG] curl check for {url}: HTTP {http_code}", file=sys.stderr)
        
        if http_code and http_code.isdigit():
            code = int(http_code)
            if 200 <= code < 400:
                return True, http_code
            else:
                return False, f"HTTP {http_code}"
        else:
            # curl failed to connect at all (code "000" or empty)
            stderr_msg = result.stderr.strip() if result.stderr else "Connection failed"
            return False, stderr_msg or f"curl returned: {http_code}"
            
    except subprocess.TimeoutExpired:
        return False, f"Timeout after {timeout}s"
    except FileNotFoundError:
        return False, "curl not found on system"
    except Exception as e:
        return False, str(e)


def read_token(token_path: str = ".openclaw/workspace/token") -> str:
    """Read the API token from file."""
    try:
        # Try relative to current workspace
        token_file = Path(token_path)
        if token_file.exists():
            return token_file.read_text().strip()
        
        # Try absolute path
        abs_token_file = Path("/home/admin/.openclaw/workspace/token")
        if abs_token_file.exists():
            return abs_token_file.read_text().strip()
        
        raise FileNotFoundError(f"Token file not found at {token_path} or /home/admin/.openclaw/workspace/token")
    except Exception as e:
        raise RuntimeError(f"Failed to read token: {e}")


def validate_app_data(data: Dict[str, Any]) -> List[str]:
    """Validate required fields in app data."""
    errors = []
    required_fields = ['app_name', 'app_url', 'description', 'author']
    
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")
        elif not data[field]:
            errors.append(f"Required field '{field}' is empty")
    
    # Validate author structure
    if 'author' in data:
        if not isinstance(data['author'], list) or len(data['author']) == 0:
            errors.append("'author' must be a non-empty list")
        elif 'name' not in data['author'][0]:
            errors.append("First author must have 'name' field")
    
    # Validate URL format if present
    if 'app_url' in data and data['app_url']:
        if not data['app_url'].startswith(('http://', 'https://')):
            errors.append("'app_url' must start with http:// or https://")
        else:
            # Use curl to verify the URL is actually accessible
            accessible, detail = check_url_accessible(data['app_url'])
            if not accessible:
                errors.append(
                    f"app_url '{data['app_url']}' is not accessible ({detail}). "
                    f"Please check the URL and ensure it is reachable."
                )
    
    return errors


def create_app(
    api_base_url: str,
    app_data: Dict[str, Any],
    token: str,
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Create an app in App Hub.
    
    Args:
        api_base_url: Base API URL (e.g., https://api.loopspace.xyz)
        app_data: Application data dictionary
        token: API authentication token
        verbose: Enable verbose logging
        
    Returns:
        API response as dictionary
    """
    # Validate input
    errors = validate_app_data(app_data)
    if errors:
        return {
            "success": False,
            "error": "Validation failed",
            "details": errors
        }
    
    # Prepare endpoint
    endpoint = f"{api_base_url.rstrip('/')}/api/app_hub/create"
    
    # Prepare headers
    headers = {
        'Token': token,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    if verbose:
        print(f"[DEBUG] POST {endpoint}", file=sys.stderr)
        print(f"[DEBUG] Headers: {headers}", file=sys.stderr)
        print(f"[DEBUG] Payload: {json.dumps(app_data, indent=2, ensure_ascii=False)}", file=sys.stderr)
    
    try:
        response = requests.post(
            endpoint,
            json=app_data,
            headers=headers,
            timeout=30
        )
        
        if verbose:
            print(f"[DEBUG] Response status: {response.status_code}", file=sys.stderr)
            print(f"[DEBUG] Response headers: {dict(response.headers)}", file=sys.stderr)
        
        # Try to parse JSON response
        try:
            result = response.json()
        except json.JSONDecodeError:
            result = {
                "success": response.ok,
                "status_code": response.status_code,
                "raw_response": response.text[:500]
            }
        
        if verbose:
            print(f"[DEBUG] Parsed result: {json.dumps(result, indent=2, ensure_ascii=False)}", file=sys.stderr)
        
        return result
        
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": "Network error",
            "details": str(e)
        }
    except Exception as e:
        return {
            "success": False,
            "error": "Unexpected error",
            "details": str(e)
        }


def get_app_detail(
    api_base_url: str,
    app_id: str,
    token: str,
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Get app detail from App Hub.
    
    Args:
        api_base_url: Base API URL
        app_id: Application ID (integer, not UUID)
        token: API authentication token
        verbose: Enable verbose logging
        
    Returns:
        API response as dictionary
    """
    endpoint = f"{api_base_url.rstrip('/')}/api/app_hub/detail/{app_id}"
    
    headers = {
        'Token': token,
        'Accept': 'application/json'
    }
    
    if verbose:
        print(f"[DEBUG] GET {endpoint}", file=sys.stderr)
        print(f"[DEBUG] Headers: {headers}", file=sys.stderr)
    
    try:
        response = requests.get(
            endpoint,
            headers=headers,
            timeout=30
        )
        
        if verbose:
            print(f"[DEBUG] Response status: {response.status_code}", file=sys.stderr)
        
        try:
            result = response.json()
        except json.JSONDecodeError:
            result = {
                "success": response.ok,
                "status_code": response.status_code,
                "raw_response": response.text[:500]
            }
        
        if verbose:
            print(f"[DEBUG] Parsed result: {json.dumps(result, indent=2, ensure_ascii=False)}", file=sys.stderr)
        
        return result
        
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": "Network error",
            "details": str(e)
        }
    except Exception as e:
        return {
            "success": False,
            "error": "Unexpected error",
            "details": str(e)
        }


def update_app(
    api_base_url: str,
    app_id: str,
    update_data: Dict[str, Any],
    token: str,
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Update app information in App Hub.
    
    Args:
        api_base_url: Base API URL
        app_id: Application ID to update
        update_data: Fields to update (partial update)
        token: API authentication token
        verbose: Enable verbose logging
        
    Returns:
        API response as dictionary
    """
    endpoint = f"{api_base_url.rstrip('/')}/api/app_hub/update"
    
    # Add id to payload (API expects integer 'id')
    try:
        payload = {"id": int(app_id)}
    except ValueError:
        return {
            "success": False,
            "error": "Invalid app_id",
            "details": "app_id must be an integer"
        }
    
    payload.update(update_data)
    
    headers = {
        'Token': token,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    if verbose:
        print(f"[DEBUG] POST {endpoint}", file=sys.stderr)
        print(f"[DEBUG] Headers: {headers}", file=sys.stderr)
        print(f"[DEBUG] Payload: {json.dumps(payload, indent=2, ensure_ascii=False)}", file=sys.stderr)
    
    try:
        response = requests.post(
            endpoint,
            json=payload,
            headers=headers,
            timeout=30
        )
        
        if verbose:
            print(f"[DEBUG] Response status: {response.status_code}", file=sys.stderr)
        
        try:
            result = response.json()
        except json.JSONDecodeError:
            result = {
                "success": response.ok,
                "status_code": response.status_code,
                "raw_response": response.text[:500]
            }
        
        if verbose:
            print(f"[DEBUG] Parsed result: {json.dumps(result, indent=2, ensure_ascii=False)}", file=sys.stderr)
        
        return result
        
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": "Network error",
            "details": str(e)
        }
    except Exception as e:
        return {
            "success": False,
            "error": "Unexpected error",
            "details": str(e)
        }


def parse_author_args(author_name: str, author_avatar: Optional[str] = None, 
                     author_url: Optional[str] = None) -> List[Dict[str, str]]:
    """Parse author arguments into proper format."""
    author = [{"name": author_name}]
    if author_avatar:
        author[0]["avatar"] = author_avatar
    if author_url:
        author[0]["url"] = author_url
    return author


def parse_communities_args(names: List[str], avatars: List[str], urls: List[str]) -> List[Dict[str, str]]:
    """Parse communities arguments into proper format."""
    communities = []
    for i, name in enumerate(names):
        community = {"name": name}
        if i < len(avatars) and avatars[i]:
            community["avatar"] = avatars[i]
        if i < len(urls) and urls[i]:
            community["url"] = urls[i]
        communities.append(community)
    return communities


def build_app_data_from_args(args) -> Dict[str, Any]:
    """Build app data dictionary from command line arguments."""
    app_data = {
        "app_name": args.app_name,
        "app_url": args.app_url,
        "description": args.description,
        "author": parse_author_args(args.author_name, args.author_avatar, args.author_url),
        "price_mode": args.price_mode,
        "price": args.price,
        "visibility": args.visibility
    }
    
    if args.icon:
        app_data["icon"] = args.icon
    
    if args.screenshot:
        app_data["screenshots"] = args.screenshot
    
    if args.community_name:
        app_data["communities"] = parse_communities_args(
            args.community_name,
            args.community_avatar or [],
            args.community_url or []
        )
    
    # Remove None values
    return {k: v for k, v in app_data.items() if v is not None}


def main():
    parser = argparse.ArgumentParser(
        description="Create app showcase in App Hub",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic app creation
  %(prog)s --app-name "MyApp" --app-url "https://myapp.com" \\
           --description "An awesome app" --author-name "Developer"

  # Full featured app
  %(prog)s --app-name "Pro Tool" --app-url "https://protool.example.com" \\
           --description "Professional AI tool" --author-name "Jane" \\
           --author-avatar "https://example.com/avatar.jpg" \\
           --author-url "https://jane.example.com" \\
           --icon "https://example.com/icon.png" \\
           --screenshot "https://example.com/ss1.png" \\
           --screenshot "https://example.com/ss2.png" \\
           --price-mode 0 --visibility 0 \\
           --community-name "AI Hub" \\
           --community-url "https://aihub.example.com"

  # Validate only (no API call)
  %(prog)s --validate-only --app-name "Test" --app-url "https://test.com" \\
           --description "Test app" --author-name "Tester"
        """
    )
    
    # API configuration
    parser.add_argument(
        '--api-url',
        default='https://api.loopspace.xyz',
        help='App Hub API base URL (default: https://api.loopspace.xyz)'
    )
    parser.add_argument(
        '--token-file',
        default='.openclaw/workspace/token',
        help='Path to token file (default: .openclaw/workspace/token)'
    )
    
    # Operation mode (implicit based on flags)
    parser.add_argument(
        '--get-detail',
        action='store_true',
        help='Get app detail by app-id'
    )
    parser.add_argument(
        '--app-id',
        help='Application ID (required for --get-detail and --update)'
    )
    parser.add_argument(
        '--update',
        action='store_true',
        help='Update app information (requires --app-id)'
    )
    parser.add_argument(
        '--add-screenshot',
        action='append',
        help='Add screenshot (for update, does not replace)'
    )
    parser.add_argument(
        '--remove-screenshot',
        type=int,
        help='Remove screenshot by index (for update)'
    )
    
    # Application data (required for create)
    parser.add_argument(
        '--app-name',
        help='Application name (required for create)'
    )
    parser.add_argument(
        '--app-url',
        help='Application URL (required for create)'
    )
    parser.add_argument(
        '--description',
        help='Application description (required for create)'
    )
    
    # Author info
    parser.add_argument(
        '--author-name',
        help='Author name (required for create)'
    )
    parser.add_argument(
        '--author-avatar',
        help='Author avatar URL (optional)'
    )
    parser.add_argument(
        '--author-url',
        help='Author personal/social URL (optional)'
    )
    
    # Optional fields
    parser.add_argument(
        '--icon',
        help='Application icon URL'
    )
    parser.add_argument(
        '--screenshot',
        action='append',
        help='Screenshot URL (can be used multiple times, for create/replace)'
    )
    parser.add_argument(
        '--price-mode',
        type=int,
        choices=[0, 1],
        help='Pricing mode: 0=free, 1=paid (optional for create/update)'
    )
    parser.add_argument(
        '--price',
        help='Price value as string, use "0" for free (optional)'
    )
    parser.add_argument(
        '--visibility',
        type=int,
        choices=[0, 1],
        help='Visibility: 0=public, 1=private (optional for create/update)'
    )
    
    # Communities (multiple)
    parser.add_argument(
        '--community-name',
        action='append',
        help='Community name (can be used multiple times)'
    )
    parser.add_argument(
        '--community-avatar',
        action='append',
        help='Community avatar URL (must match number of community-name)'
    )
    parser.add_argument(
        '--community-url',
        action='append',
        help='Community URL (must match number of community-name)'
    )
    
    # JSON input
    parser.add_argument(
        '--json-file',
        help='Load app data from JSON file'
    )
    
    # Validation mode
    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Only validate data, do not make API call'
    )
    
    # Verbose
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    try:
        # Load token
        token = read_token(args.token_file)
        if args.verbose:
            print(f"[DEBUG] Token loaded (length: {len(token)})", file=sys.stderr)
        
        # Determine operation mode
        if args.get_detail:
            # Get app detail
            if not args.app_id:
                print("Error: --app-id is required for --get-detail", file=sys.stderr)
                sys.exit(1)
            
            result = get_app_detail(args.api_url, args.app_id, token, args.verbose)
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
        elif args.update:
            # Update app
            if not args.app_id:
                print("Error: --app-id is required for --update", file=sys.stderr)
                sys.exit(1)
            
            # Convert app_id to integer (API expects integer)
            try:
                app_id_int = int(args.app_id)
            except ValueError:
                print(f"Error: --app-id must be an integer, got '{args.app_id}'", file=sys.stderr)
                sys.exit(1)
            
            # Build update data (only include provided fields)
            update_data = {}
            
            # Optional updatable fields
            if args.app_name:
                update_data['app_name'] = args.app_name
            if args.app_url:
                if not args.app_url.startswith(('http://', 'https://')):
                    print("Error: --app-url must start with http:// or https://", file=sys.stderr)
                    sys.exit(1)
                update_data['app_url'] = args.app_url
            if args.description:
                update_data['description'] = args.description
            if args.icon:
                update_data['icon'] = args.icon
            
            # Handle screenshots
            if args.screenshot is not None:
                update_data['screenshots'] = args.screenshot
            if args.add_screenshot:
                if 'screenshots' not in update_data:
                    update_data['screenshots'] = args.add_screenshot
                else:
                    update_data['screenshots'].extend(args.add_screenshot)
            if args.remove_screenshot is not None:
                update_data['remove_screenshot_index'] = args.remove_screenshot
            
            # Handle author update (need all three or none)
            if args.author_name:
                author_data = {"name": args.author_name}
                if args.author_avatar:
                    author_data["avatar"] = args.author_avatar
                if args.author_url:
                    author_data["url"] = args.author_url
                update_data['author'] = [author_data]
            
            # Other fields (only add if explicitly provided)
            if args.price_mode is not None:
                update_data['price_mode'] = args.price_mode
            if args.price is not None:
                update_data['price'] = args.price
            if args.visibility is not None:
                update_data['visibility'] = args.visibility
            
            # Communities
            if args.community_name:
                update_data['communities'] = parse_communities_args(
                    args.community_name,
                    args.community_avatar or [],
                    args.community_url or []
                )
            
            if args.verbose:
                print(f"[DEBUG] Update payload: {json.dumps(update_data, indent=2, ensure_ascii=False)}", file=sys.stderr)
            
            result = update_app(args.api_url, app_id_int, update_data, token, args.verbose)
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
        else:
            # Create new app (original logic)
            if args.json_file:
                # Load from JSON file
                json_path = Path(args.json_file)
                if not json_path.exists():
                    print(f"Error: JSON file not found: {args.json_file}", file=sys.stderr)
                    sys.exit(1)
                
                with open(json_path, 'r', encoding='utf-8') as f:
                    app_data = json.load(f)
                
                if args.verbose:
                    print(f"[DEBUG] Loaded data from {args.json_file}", file=sys.stderr)
            else:
                # Build from command line arguments
                if not all([args.app_name, args.app_url, args.description, args.author_name]):
                    print("Error: Missing required fields: --app-name, --app-url, --description, --author-name", file=sys.stderr)
                    parser.print_help()
                    sys.exit(1)
                
                app_data = build_app_data_from_args(args)
            
            # Validate only mode
            if args.validate_only:
                errors = validate_app_data(app_data)
                if errors:
                    print("Validation failed:", file=sys.stderr)
                    for error in errors:
                        print(f"  ✗ {error}", file=sys.stderr)
                    sys.exit(1)
                else:
                    print("✓ Validation passed - app data is valid", file=sys.stderr)
                    print(json.dumps(app_data, indent=2, ensure_ascii=False))
                    sys.exit(0)
            
            # Make API call
            if args.verbose:
                print("Starting app creation...", file=sys.stderr)
            
            result = create_app(args.api_url, app_data, token, args.verbose)
            
            # Pretty print result
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
