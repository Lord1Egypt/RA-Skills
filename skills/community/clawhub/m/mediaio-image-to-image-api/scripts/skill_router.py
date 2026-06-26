#!/usr/bin/env python3
import json
import os
import requests
from typing import Any, Dict, Optional
from urllib.parse import urlparse

class Skill:
    """
    Standard AIGC skill implementation with automatic API routing and parameter mapping.
    """
    def __init__(self, api_doc_path: str):
        with open(api_doc_path, 'r', encoding='utf-8') as f:
            api_items = json.load(f)

        self.api_definitions = {}
        duplicate_names = []
        for item in api_items:
            name = item.get('name')
            if name in self.api_definitions:
                duplicate_names.append(name)
                continue
            self.api_definitions[name] = item

        if duplicate_names:
            deduped = sorted(set(duplicate_names))
            raise ValueError(
                f"Duplicate API names detected in {api_doc_path}: {', '.join(deduped)}. "
                "Please use unique `name` fields in c_api_doc_detail.json."
            )

    def invoke(self, api_name: str, params: Dict[str, Any], api_key: Optional[str] = None) -> Dict[str, Any]:
        """
        Invoke the specified API.
        :param api_name: API name.
        :param params: Business parameters.
        :param api_key: API key. If omitted, API_KEY from environment is used.
        :return: API response payload.
        """
        if api_name not in self.api_definitions:
            return {'error': f"API '{api_name}' not found."}

        resolved_api_key = (api_key or os.getenv('API_KEY', '')).strip()
        if not resolved_api_key:
            return {'error': 'Missing API key. Set API_KEY or pass api_key explicitly.'}

        api = self.api_definitions[api_name]
        url = api['endpoint']
        method = api['method']

        # Restrict outbound requests to the expected Media.io API host.
        parsed = urlparse(url)
        if parsed.scheme != 'https' or parsed.netloc.lower() != 'openapi.media.io':
            return {'error': f"Blocked endpoint host: {parsed.netloc}"}

        headers = {
            'X-API-KEY': resolved_api_key,
            'Content-Type': 'application/json'
        }
        # Replace path parameters in endpoint URLs.
        if '{' in url:
            for k, v in params.items():
                url = url.replace(f'{{{k}}}', str(v))
        # Keep non-path parameters in the JSON body.
        body = {k: v for k, v in params.items() if f'{{{k}}}' not in api['endpoint']}
        try:
            resp = requests.request(method, url, headers=headers, json={'data': body} if body else {}, timeout=30)
            return resp.json()
        except Exception as e:
            return {'error': str(e)}

# Standard usage example.
if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill = Skill(os.path.join(script_dir, 'c_api_doc_detail.json'))
    api_key = os.getenv('API_KEY', '')
    if not api_key:
        raise RuntimeError('API_KEY is not set')
    # Credits query.
    result = skill.invoke('Credits', {}, api_key=api_key)
    print(result)
