#!/usr/bin/env python3
"""
API Wrapper Generator - Generate OpenClaw skills from REST APIs

Usage:
    python generator.py generate --spec https://api.example.com/openapi.json --name my-api
    python generator.py validate --spec ./openapi.yaml
    python generator.py test --skill ./my-api --endpoint <operationId>
"""

import os
import sys
import json
import yaml
import hashlib
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class APIEndpoint:
    """Represents an API endpoint."""
    
    operation_id: str
    method: str
    path: str
    summary: str = ""
    description: str = ""
    parameters: List[Dict] = field(default_factory=list)
    request_body: Optional[Dict] = None
    responses: Dict[str, Dict] = field(default_factory=dict)
    auth_required: bool = False
    tags: List[str] = field(default_factory=list)


@dataclass
class APISpec:
    """Represents an API specification."""
    
    title: str
    version: str
    base_url: str
    description: str = ""
    endpoints: List[APIEndpoint] = field(default_factory=list)
    auth_type: str = "none"
    auth_config: Dict = field(default_factory=dict)


class APIWrapperGenerator:
    """Generate OpenClaw skills from OpenAPI specs."""
    
    def __init__(self, output_dir: str = "."):
        self.output_dir = Path(output_dir)
    
    def parse_openapi(self, spec_url: str) -> APISpec:
        """Parse OpenAPI specification from URL or file."""
        
        # Load spec
        if spec_url.startswith(('http://', 'https://')):
            content = self._fetch_url(spec_url)
        else:
            content = Path(spec_url).read_text()
        
        # Parse YAML or JSON
        if spec_url.endswith(('.yaml', '.yml')) or content.strip().startswith(('openapi:', 'swagger:')):
            spec_data = yaml.safe_load(content)
        else:
            spec_data = json.loads(content)
        
        # Extract API info
        info = spec_data.get('info', {})
        servers = spec_data.get('servers', [{}])
        
        base_url = ""
        if servers:
            server = servers[0]
            base_url = server.get('url', '')
            if server.get('variables'):
                for var_name, var_info in server['variables'].items():
                    base_url = base_url.replace(f'{{{var_name}}}', var_info.get('default', ''))
        
        # Detect auth
        auth_type, auth_config = self._detect_auth(spec_data)
        
        # Parse endpoints
        endpoints = []
        paths = spec_data.get('paths', {})
        
        for path, methods in paths.items():
            for method, operation in methods.items():
                if method.upper() not in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD']:
                    continue
                
                endpoint = APIEndpoint(
                    operation_id=operation.get('operationId', f"{method}_{path}").replace('/', '_').replace('{', '').replace('}', ''),
                    method=method.upper(),
                    path=path,
                    summary=operation.get('summary', ''),
                    description=operation.get('description', ''),
                    parameters=operation.get('parameters', []),
                    request_body=operation.get('requestBody'),
                    responses=operation.get('responses', {}),
                    auth_required=bool(spec_data.get('security', [])),
                    tags=operation.get('tags', []),
                )
                
                endpoints.append(endpoint)
        
        return APISpec(
            title=info.get('title', 'API').replace(' ', '-').lower(),
            version=info.get('version', '1.0.0'),
            base_url=base_url,
            description=info.get('description', ''),
            endpoints=endpoints,
            auth_type=auth_type,
            auth_config=auth_config,
        )
    
    def _fetch_url(self, url: str) -> str:
        """Fetch content from URL."""
        try:
            req = urllib.request.Request(url, headers={'Accept': 'application/json, application/yaml'})
            response = urllib.request.urlopen(req, timeout=30)
            return response.read().decode('utf-8')
        except urllib.error.HTTPError as e:
            raise Exception(f"Failed to fetch {url}: {e.code}")
    
    def _detect_auth(self, spec_data: Dict) -> tuple:
        """Detect authentication type from spec."""
        
        security_schemes = spec_data.get('components', {}).get('securitySchemes', {})
        security = spec_data.get('security', [])
        
        if not security_schemes:
            return "none", {}
        
        # Get first security scheme
        for name, scheme in security_schemes.items():
            auth_type = scheme.get('type', '').lower()
            
            if auth_type == 'apikey':
                location = scheme.get('in', 'header')
                key_name = scheme.get('name', 'X-API-Key')
                return "api_key", {"location": location, "name": key_name}
            
            elif auth_type == 'http':
                scheme_name = scheme.get('scheme', '').lower()
                if scheme_name == 'bearer':
                    return "bearer", {}
                elif scheme_name == 'basic':
                    return "basic", {}
            
            elif auth_type == 'oauth2':
                flows = scheme.get('flows', {})
                return "oauth2", {"flows": flows}
        
        return "none", {}
    
    def generate_skill(self, spec: APISpec, name: Optional[str] = None) -> Path:
        """Generate OpenClaw skill from API spec."""
        
        skill_name = name or spec.title
        skill_dir = self.output_dir / skill_name
        skill_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate SKILL.md
        skill_md = self._generate_skill_md(spec, skill_name)
        (skill_dir / "SKILL.md").write_text(skill_md)
        
        # Generate claw.json
        claw_json = self._generate_claw_json(spec, skill_name)
        (skill_dir / "claw.json").write_text(claw_json)
        
        # Generate API client
        api_script = self._generate_api_client(spec, skill_name)
        scripts_dir = skill_dir / "scripts"
        scripts_dir.mkdir(exist_ok=True)
        (scripts_dir / "api.py").write_text(api_script)
        
        # Generate references
        refs_dir = skill_dir / "references"
        refs_dir.mkdir(exist_ok=True)
        (refs_dir / "endpoints.md").write_text(self._generate_endpoints_md(spec))
        
        print(f"✓ Generated skill: {skill_name}")
        print(f"  Output: {skill_dir}")
        print(f"  Endpoints: {len(spec.endpoints)}")
        
        return skill_dir
    
    def _generate_skill_md(self, spec: APISpec, name: str) -> str:
        """Generate SKILL.md content."""
        
        endpoints_list = "\n".join([
            f"- `{e.operation_id}` — {e.summary or e.method + ' ' + e.path}"
            for e in spec.endpoints[:20]  # Limit to first 20
        ])
        
        return f"""---
name: {name}
version: 1.0.0
description: {spec.description[:200] if spec.description else f"OpenClaw skill for {spec.title} API"}. Auto-generated from OpenAPI spec.
---

# {spec.title} API

{spec.description or f"Interact with {spec.title} API from OpenClaw."}

**Base URL:** `{spec.base_url}`

**Version:** {spec.version}

## Quick Start

```bash
# List available operations
{name} list

# Call an endpoint
{name} {spec.endpoints[0].operation_id if spec.endpoints else 'call'} --param value

# Get help for specific operation
{name} {spec.endpoints[0].operation_id if spec.endpoints else 'call'} --help
```

## Authentication

This API uses **{spec.auth_type.upper()}** authentication.

```bash
# Configure authentication
{name} config set auth.api_key YOUR_API_KEY
# or for Bearer token
{name} config set auth.bearer_token YOUR_TOKEN
```

## Available Operations

{endpoints_list}

{'' if len(spec.endpoints) <= 20 else f'_... and {len(spec.endpoints) - 20} more operations_'}

## Usage Examples

```bash
# Example: {spec.endpoints[0].operation_id if spec.endpoints else 'call'}
{name} {spec.endpoints[0].operation_id if spec.endpoints else 'call'} \\
  --param1 value1 \\
  --param2 value2
```

## Error Handling

The skill will return error details for:
- Authentication failures (401)
- Permission denied (403)
- Not found (404)
- Rate limiting (429)
- Server errors (5xx)

## See Also

- `references/endpoints.md` — Complete endpoint reference
- `scripts/api.py` — API client implementation
"""
    
    def _generate_claw_json(self, spec: APISpec, name: str) -> str:
        """Generate claw.json content."""
        
        return json.dumps({
            "name": name,
            "version": "1.0.0",
            "description": f"OpenClaw skill for {spec.title} API. Auto-generated from OpenAPI spec.",
            "author": "Neckr0ik",
            "license": "MIT",
            "keywords": ["api", spec.title.lower().replace(' ', '-'), "rest", "openapi"],
            "dependencies": {
                "requests": ">=2.28.0"
            }
        }, indent=2)
    
    def _generate_api_client(self, spec: APISpec, name: str) -> str:
        """Generate API client script."""
        
        endpoint_methods = []
        
        for endpoint in spec.endpoints:
            params = []
            param_docs = []
            
            # Path parameters
            for param in endpoint.parameters:
                if param.get('in') == 'path':
                    params.append(f"'{param['name']}'")
                    param_docs.append(f"        {param['name']}: {param.get('schema', {}).get('type', 'str')}")
            
            # Query parameters
            for param in endpoint.parameters:
                if param.get('in') == 'query':
                    params.append(f"{param['name']}=None")
                    param_docs.append(f"        {param['name']}: {param.get('schema', {}).get('type', 'str')} (optional)")
            
            param_str = ", ".join(params) if params else ""
            
            method_code = f'''
    def {endpoint.operation_id}(self, {param_str}):
        """
        {endpoint.summary or endpoint.method + ' ' + endpoint.path}
        
        Method: {endpoint.method}
        Path: {endpoint.path}
{chr(10).join(param_docs) if param_docs else '        '}
        Returns:
            dict: API response
        """
        path = "{endpoint.path}"
{self._generate_path_params_code(endpoint)}
{self._generate_query_params_code(endpoint)}
        
        return self._request("{endpoint.method}", path){self._generate_body_code(endpoint)}
'''
            endpoint_methods.append(method_code)
        
        return f'''#!/usr/bin/env python3
"""
{name} API Client

Auto-generated from OpenAPI specification.
"""

import os
import json
import urllib.request
import urllib.error
from typing import Dict, Optional, Any


class {name.replace('-', '').replace('_', '').title()}Client:
    """Client for {spec.title} API."""
    
    def __init__(self, base_url: str = "{spec.base_url}", api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key or os.environ.get('{name.replace('-', '_').upper()}_API_KEY')
        self.timeout = 30
    
    def _request(self, method: str, path: str, params: Optional[Dict] = None, 
                  data: Optional[Dict] = None) -> Dict:
        """Make HTTP request to API."""
        
        url = self.base_url + path
        
        # Add query parameters
        if params:
            query = '&'.join(f'{k}={v}' for k, v in params.items() if v is not None)
            if query:
                url += '?' + query
        
        headers = {{
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }}
        
        # Add authentication
        if self.api_key:
{self._generate_auth_code(spec)}
        
        # Build request
        req_data = json.dumps(data).encode() if data else None
        req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
        
        try:
            response = urllib.request.urlopen(req, timeout=self.timeout)
            return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if e.fp else ''
            return {{
                'error': True,
                'status': e.code,
                'message': str(e),
                'body': error_body
            }}
{''.join(endpoint_methods)}


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="{spec.title} API Client")
    parser.add_argument('operation', help='Operation to perform')
    parser.add_argument('--base-url', default="{spec.base_url}", help='API base URL')
    parser.add_argument('--api-key', help='API key')
    
    # Parse known args for operation-specific help
    args, remaining = parser.parse_known_args()
    
    client = {name.replace('-', '').replace('_', '').title()}Client(
        base_url=args.base_url,
        api_key=args.api_key
    )
    
    if args.operation == 'list':
        print("Available operations:")
        for op in [{', '.join([f"'{e.operation_id}'" for e in spec.endpoints[:10]])}]:
            print(f"  - {{op}}")
    elif hasattr(client, args.operation):
        print(f"Calling {{args.operation}}...")
        # In real implementation, would parse remaining args
        print("See --help for operation-specific options")
    else:
        print(f"Unknown operation: {{args.operation}}")
        print("Use 'list' to see available operations")


if __name__ == "__main__":
    main()
'''
    
    def _generate_path_params_code(self, endpoint: APIEndpoint) -> str:
        """Generate code for path parameter substitution."""
        
        path_params = [p for p in endpoint.parameters if p.get('in') == 'path']
        
        if not path_params:
            return "        # No path parameters"
        
        lines = []
        for param in path_params:
            lines.append(f'        path = path.replace("{{{param["name"]}}}", str({param["name"]}))')
        
        return '\n'.join(lines)
    
    def _generate_query_params_code(self, endpoint: APIEndpoint) -> str:
        """Generate code for query parameters."""
        
        query_params = [p for p in endpoint.parameters if p.get('in') == 'query']
        
        if not query_params:
            return "        params = {}"
        
        lines = ["        params = {"]
        for param in query_params:
            lines.append(f'            "{param["name"]}": {param["name"]},')
        lines.append("        }")
        
        return '\n'.join(lines)
    
    def _generate_body_code(self, endpoint: APIEndpoint) -> str:
        """Generate code for request body."""
        
        if not endpoint.request_body:
            return ""
        
        return ", data=data"
    
    def _generate_auth_code(self, spec: APISpec) -> str:
        """Generate authentication code."""
        
        if spec.auth_type == "api_key":
            location = spec.auth_config.get('location', 'header')
            name = spec.auth_config.get('name', 'X-API-Key')
            
            if location == 'header':
                return f"            headers['{name}'] = self.api_key"
            else:  # query
                return "            params['api_key'] = self.api_key"
        
        elif spec.auth_type == "bearer":
            return "            headers['Authorization'] = f'Bearer {self.api_key}'"
        
        elif spec.auth_type == "basic":
            return "            headers['Authorization'] = f'Basic {self.api_key}'"
        
        return ""
    
    def _generate_endpoints_md(self, spec: APISpec) -> str:
        """Generate endpoints reference markdown."""
        
        sections = [f"# {spec.title} API Endpoints\n"]
        
        for endpoint in spec.endpoints:
            sections.append(f"\n## {endpoint.operation_id}\n")
            sections.append(f"**Method:** `{endpoint.method}`\n")
            sections.append(f"**Path:** `{endpoint.path}`\n")
            
            if endpoint.summary:
                sections.append(f"\n{endpoint.summary}\n")
            
            if endpoint.parameters:
                sections.append("\n### Parameters\n")
                for param in endpoint.parameters:
                    sections.append(f"- `{param['name']}` ({param.get('in', 'unknown')}): {param.get('description', '')}\n")
            
            if endpoint.request_body:
                sections.append("\n### Request Body\n")
                content = endpoint.request_body.get('content', {})
                for content_type, schema in content.items():
                    sections.append(f"Content-Type: `{content_type}`\n")
            
            sections.append("\n---\n")
        
        return ''.join(sections)
    
    def validate_spec(self, spec_url: str) -> bool:
        """Validate OpenAPI specification."""
        
        try:
            spec = self.parse_openapi(spec_url)
            print(f"✓ Valid OpenAPI specification")
            print(f"  Title: {spec.title}")
            print(f"  Version: {spec.version}")
            print(f"  Endpoints: {len(spec.endpoints)}")
            return True
        except Exception as e:
            print(f"✗ Invalid specification: {e}")
            return False


def main():
    """CLI entry point."""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="API Wrapper Generator")
    subparsers = parser.add_subparsers(dest='command', help='Command')
    
    # generate command
    gen_parser = subparsers.add_parser('generate', help='Generate skill from API spec')
    gen_parser.add_argument('--spec', required=True, help='OpenAPI spec URL or file')
    gen_parser.add_argument('--name', help='Skill name')
    gen_parser.add_argument('--output', default='.', help='Output directory')
    
    # validate command
    val_parser = subparsers.add_parser('validate', help='Validate OpenAPI spec')
    val_parser.add_argument('--spec', required=True, help='OpenAPI spec URL or file')
    
    args = parser.parse_args()
    
    generator = APIWrapperGenerator(output_dir=args.output if hasattr(args, 'output') else '.')
    
    if args.command == 'generate':
        spec = generator.parse_openapi(args.spec)
        generator.generate_skill(spec, name=args.name)
    
    elif args.command == 'validate':
        generator.validate_spec(args.spec)
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()