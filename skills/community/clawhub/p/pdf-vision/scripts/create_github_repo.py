#!/usr/bin/env python3
"""
Create GitHub repository using GitHub API and your token
"""

import os
import sys
import json
import requests

def create_github_repo(repo_name, description="", private=False):
    """Create a new GitHub repository"""
    
    # Get GitHub token from environment
    github_token = os.environ.get('GITHUB_TOKEN')
    if not github_token:
        # Try to read from .bashrc
        try:
            with open(os.path.expanduser('~/.bashrc'), 'r') as f:
                for line in f:
                    if 'GITHUB_TOKEN' in line:
                        # Extract token from export line
                        if '"' in line:
                            token = line.split('"')[1]
                        elif "'" in line:
                            token = line.split("'")[1]
                        else:
                            token = line.split('=')[1].strip()
                        github_token = token
                        break
        except FileNotFoundError:
            pass
    
    if not github_token:
        print("Error: GITHUB_TOKEN not found in environment or ~/.bashrc")
        return False
    
    # GitHub API endpoint
    url = "https://api.github.com/user/repos"
    
    # Repository data
    data = {
        "name": repo_name,
        "description": description,
        "private": private,
        "auto_init": True,
        "gitignore_template": "Python"
    }
    
    # Headers
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 201:
            repo_info = response.json()
            print(f"✅ Repository created successfully!")
            print(f"Repository URL: {repo_info['html_url']}")
            print(f"Clone URL: {repo_info['clone_url']}")
            return repo_info['clone_url']
        else:
            print(f"❌ Error creating repository: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 create_github_repo.py <repo_name> [description] [private]")
        sys.exit(1)
    
    repo_name = sys.argv[1]
    description = sys.argv[2] if len(sys.argv) > 2 else "PDF Vision skill for OpenClaw"
    private = sys.argv[3].lower() == 'true' if len(sys.argv) > 3 else False
    
    clone_url = create_github_repo(repo_name, description, private)
    
    if clone_url:
        print(f"\nNext steps:")
        print(f"1. Navigate to your skill directory:")
        print(f"   cd /home/lpq/.openclaw/workspace/skills/pdf-vision")
        print(f"2. Add the remote repository:")
        print(f"   git remote add origin {clone_url}")
        print(f"3. Push your code:")
        print(f"   git branch -M main")
        print(f"   git push -u origin main")
    else:
        print("\nFailed to create repository. Please check your GITHUB_TOKEN.")

if __name__ == "__main__":
    main()