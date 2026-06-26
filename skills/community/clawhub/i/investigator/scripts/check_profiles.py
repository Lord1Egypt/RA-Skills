#!/usr/bin/env python3
import json
import re
import sys
import requests
from urllib.parse import quote, urlparse

PLATFORMS = {
    "github": "https://github.com/{u}",
    "reddit": "https://www.reddit.com/user/{u}",
    "tiktok": "https://www.tiktok.com/@{u}",
    "x": "https://x.com/{u}",
    "instagram": "https://www.instagram.com/{u}/",
    "gitlab": "https://gitlab.com/{u}",
    "youtube": "https://www.youtube.com/@{u}",
    "twitch": "https://www.twitch.tv/{u}",
    "pinterest": "https://www.pinterest.com/{u}/",
    "keybase": "https://keybase.io/{u}",
    "hackernews": "https://news.ycombinator.com/user?id={u}",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; OpenClaw username-email-investigator/1.0)"
}


def path_of(url):
    try:
        return urlparse(url).path.rstrip('/')
    except Exception:
        return ''


def extract_title(html):
    m = re.search(r'<title[^>]*>(.*?)</title>', html, re.I | re.S)
    if not m:
        return ''
    return re.sub(r'\s+', ' ', m.group(1)).strip()


def extract_profile_image(html):
    patterns = [
        r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']',
        r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\']+)["\']',
        r'<meta[^>]+property=["\']twitter:image["\'][^>]+content=["\']([^"\']+)["\']',
    ]
    for p in patterns:
        m = re.search(p, html, re.I)
        if m:
            return m.group(1)
    return None


def validate(platform, username, requested_url, final_url, status, title, body):
    title_l = (title or '').lower()
    body_l = (body or '').lower()
    final_path = path_of(final_url)
    u = username.lower()

    if status != 200:
        return 'no_result', ['non_200_status']

    if platform == 'github':
        if final_path == f'/{u}' and (u in title_l or 'github' in title_l) and 'not found' not in body_l:
            return 'exact', ['exact_username_match', 'final_url_match']
        return 'weak', ['ambiguous_profile_page']

    if platform == 'reddit':
        if final_path == f'/user/{u}' and ('reddit' in title_l or f'u/{u}' in body_l or f'user/{u}' in body_l):
            return 'exact', ['exact_username_match', 'final_url_match']
        return 'weak', ['ambiguous_profile_page']

    if platform == 'hackernews':
        if f'profile: {u}' in title_l or f'user: {u}' in body_l or f'id={u}' in final_url.lower():
            return 'exact', ['exact_username_match', 'profile_marker']
        return 'weak', ['ambiguous_profile_page']

    if platform in ('gitlab', 'keybase'):
        if final_path == f'/{u}' and u in (title_l + body_l):
            return 'exact', ['exact_username_match', 'final_url_match']
        return 'weak', ['ambiguous_profile_page']

    if platform == 'youtube':
        if 'consent.youtube.com' in final_url:
            return 'not_verifiable', ['consent_wall']
        if final_path.lower() == f'/@{u}' and u in (title_l + body_l):
            return 'likely', ['final_url_match']
        return 'weak', ['ambiguous_profile_page']

    if platform in ('tiktok', 'x', 'instagram', 'twitch', 'pinterest'):
        expected = {
            'tiktok': f'/@{u}',
            'x': f'/{u}',
            'instagram': f'/{u}',
            'twitch': f'/{u}',
            'pinterest': f'/{u}',
        }[platform]
        if final_path.lower() == expected and u in (title_l + body_l):
            return 'likely', ['final_url_match']
        if final_path.lower() == expected:
            return 'weak', ['final_url_match_only']
        return 'no_result', ['redirect_or_missing']

    return 'weak', ['unknown_validation_rule']


def check_url(platform, username, url: str):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10, allow_redirects=True)
        status = r.status_code
        html = r.text[:20000]
        title = extract_title(html)
        profile_image = extract_profile_image(html)
        match_type, signals = validate(platform, username, url, r.url, status, title, html[:8000])
        if profile_image:
            signals = signals + ['public_profile_image_found']
        exists = match_type in ('exact', 'likely')
        return {
            'status_code': status,
            'exists': exists,
            'final_url': r.url,
            'title': title,
            'profile_image': profile_image,
            'match_type': match_type,
            'signals': signals,
        }
    except Exception as e:
        return {
            'status_code': None,
            'exists': False,
            'error': str(e),
            'final_url': url,
            'title': '',
            'profile_image': None,
            'match_type': 'not_verifiable',
            'signals': ['request_failed'],
        }


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "usage: check_profiles.py <username>"}))
        return
    username = sys.argv[1].strip()
    out = {"input": username, "results": []}
    for name, template in PLATFORMS.items():
        url = template.format(u=quote(username))
        result = check_url(name, username, url)
        out['results'].append({
            'platform': name,
            'url': url,
            **result,
        })
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
