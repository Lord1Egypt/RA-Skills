#!/usr/bin/env python3
import os
import sys
import json
import urllib.parse
import urllib.request
import argparse

def load_env_file(path):
    if not os.path.exists(path):
        return
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and not os.getenv(key):
                os.environ[key] = value

def _resolve_credentials():
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    load_env_file(os.path.join(skill_dir, '.env'))
    load_env_file(os.path.join(os.path.expanduser('~'), '.openclaw', 'credentials', 'naver-shopping.env'))

    client_id = (
        os.getenv('NAVER_Client_ID')
        or os.getenv('NAVER_CLIENT_ID')
        or os.getenv('NAVER_SHOPPING_CLIENT_ID')
    )
    client_secret = (
        os.getenv('NAVER_Client_Secret')
        or os.getenv('NAVER_CLIENT_SECRET')
        or os.getenv('NAVER_SHOPPING_CLIENT_SECRET')
    )
    return client_id, client_secret


def search_shopping(query, display=5, sort='sim'):
    client_id, client_secret = _resolve_credentials()

    if not client_id or not client_secret:
        return {
            "error": (
                "네이버 쇼핑 API 자격증명을 찾지 못했습니다. "
                "NAVER_Client_ID / NAVER_Client_Secret 또는 NAVER_CLIENT_ID / NAVER_CLIENT_SECRET 을 설정해 주세요."
            )
        }

    display = max(1, min(int(display), 100))
    encText = urllib.parse.quote(query)
    url = f"https://openapi.naver.com/v1/search/shop.json?query={encText}&display={display}&sort={sort}"
    
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id.strip())
    request.add_header("X-Naver-Client-Secret", client_secret.strip())
    
    # Debug: print headers (excluding secret)
    # print(f"ID: {client_id.strip()}", file=sys.stderr)
    
    try:
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if rescode == 200:
            response_body = response.read()
            return json.loads(response_body.decode('utf-8'))
        else:
            return {"error": f"Error Code: {rescode}"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Naver Shopping Search')
    parser.add_argument('query', help='Search query')
    parser.add_argument('--display', type=int, default=5, help='Number of results (1-100)')
    parser.add_argument('--sort', default='sim', choices=['sim', 'date', 'asc', 'dsc'], help='Sort order')
    
    args = parser.parse_args()
    
    results = search_shopping(args.query, args.display, args.sort)
    
    if "error" in results:
        print(json.dumps(results, indent=2, ensure_ascii=False))
        sys.exit(1)
        
    print(json.dumps(results, indent=2, ensure_ascii=False))
