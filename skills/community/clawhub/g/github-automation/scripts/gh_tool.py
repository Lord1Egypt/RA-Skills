#!/usr/bin/env python3
"""GitHub CLI automation tool."""
import sys
import os
import json
import urllib.request
import urllib.error
import ssl

GITHUB_API = "https://api.github.com"

def get_token():
    """Get GitHub token from environment."""
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        print("❌ Error: GITHUB_TOKEN environment variable not set")
        print("Set it with: export GITHUB_TOKEN=ghp_your_token_here")
        sys.exit(1)
    return token

def api_request(endpoint, token, method='GET', data=None):
    """Make GitHub API request."""
    url = f"{GITHUB_API}{endpoint}"
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'GitHub-Automation/1.0'
    }
    
    if data:
        headers['Content-Type'] = 'application/json'
        data = json.dumps(data).encode('utf-8')
    
    req = urllib.request.Request(url, headers=headers, method=method, data=data)
    
    try:
        with urllib.request.urlopen(req, timeout=30, context=ctx) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return {'error': f'HTTP {e.code}: {e.reason}'}
    except Exception as e:
        return {'error': str(e)}

def list_issues(owner, repo, token, state='open'):
    """List issues for a repo."""
    endpoint = f"/repos/{owner}/{repo}/issues?state={state}"
    return api_request(endpoint, token)

def create_issue(owner, repo, token, title, body='', labels=None):
    """Create an issue."""
    endpoint = f"/repos/{owner}/{repo}/issues"
    data = {
        'title': title,
        'body': body
    }
    if labels:
        data['labels'] = labels if isinstance(labels, list) else [labels]
    return api_request(endpoint, token, 'POST', data)

def list_prs(owner, repo, token, state='open'):
    """List pull requests."""
    endpoint = f"/repos/{owner}/{repo}/pulls?state={state}"
    return api_request(endpoint, token)

def list_repos(token, username=None):
    """List repositories."""
    if username:
        endpoint = f"/users/{username}/repos"
    else:
        endpoint = "/user/repos"
    return api_request(endpoint, token)

def get_notifications(token):
    """Get user notifications."""
    endpoint = "/notifications"
    return api_request(endpoint, token)

def main():
    if len(sys.argv) < 2:
        print("GitHub Automation Tool")
        print("=" * 50)
        print("Commands:")
        print("  issue list <owner>/<repo> [state]")
        print("  issue create <owner>/<repo> <title> [body] [--labels label1,label2]")
        print("  pr list <owner>/<repo> [state]")
        print("  repo list [username]")
        print("  notifications")
        print("")
        print("Environment: GITHUB_TOKEN required")
        sys.exit(1)
    
    token = get_token()
    command = sys.argv[1]
    
    if command == 'issue':
        subcommand = sys.argv[2] if len(sys.argv) > 2 else None
        
        if subcommand == 'list':
            repo_spec = sys.argv[3]
            state = sys.argv[4] if len(sys.argv) > 4 else 'open'
            owner, repo = repo_spec.split('/')
            issues = list_issues(owner, repo, token, state)
            
            if 'error' in issues:
                print(f"❌ Error: {issues['error']}")
                return
            
            print(f"Issues for {owner}/{repo} ({state}):")
            for issue in issues:
                if 'pull_request' not in issue:  # Skip PRs
                    print(f"  #{issue['number']}: {issue['title']}")
        
        elif subcommand == 'create':
            repo_spec = sys.argv[3]
            title = sys.argv[4]
            body = sys.argv[5] if len(sys.argv) > 5 else ''
            owner, repo = repo_spec.split('/')
            
            result = create_issue(owner, repo, token, title, body)
            
            if 'error' in result:
                print(f"❌ Error: {result['error']}")
            else:
                print(f"✅ Created issue #{result['number']}: {result['title']}")
                print(f"   URL: {result['html_url']}")
    
    elif command == 'pr':
        subcommand = sys.argv[2] if len(sys.argv) > 2 else None
        
        if subcommand == 'list':
            repo_spec = sys.argv[3]
            state = sys.argv[4] if len(sys.argv) > 4 else 'open'
            owner, repo = repo_spec.split('/')
            prs = list_prs(owner, repo, token, state)
            
            if 'error' in prs:
                print(f"❌ Error: {prs['error']}")
                return
            
            print(f"PRs for {owner}/{repo} ({state}):")
            for pr in prs:
                print(f"  #{pr['number']}: {pr['title']} by {pr['user']['login']}")
    
    elif command == 'repo':
        subcommand = sys.argv[2] if len(sys.argv) > 2 else None
        
        if subcommand == 'list':
            username = sys.argv[3] if len(sys.argv) > 3 else None
            repos = list_repos(token, username)
            
            if 'error' in repos:
                print(f"❌ Error: {repos['error']}")
                return
            
            whose = f"{username}'s" if username else "your"
            print(f"Repositories for {whose}:")
            for repo in repos:
                visibility = "🔒" if repo['private'] else "🌐"
                print(f"  {visibility} {repo['full_name']}")
    
    elif command == 'notifications':
        notifs = get_notifications(token)
        
        if 'error' in notifs:
            print(f"❌ Error: {notifs['error']}")
            return
        
        print(f"Notifications ({len(notifs)} unread):")
        for n in notifs[:10]:  # Limit to 10
            print(f"  {n['subject']['type']}: {n['subject']['title']}")
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()