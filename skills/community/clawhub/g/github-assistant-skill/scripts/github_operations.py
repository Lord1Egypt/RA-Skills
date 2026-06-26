#!/usr/bin/env python3
"""
GitHub Operations - 完整的 GitHub 操作工具集
支持双模式：
1. API Mode - 使用 Personal Access Token（快速、headless）
2. Browser Mode - 使用浏览器自动化（可视化、无需 Token）

操作类别：
- 仓库操作：Star/Fork/Watch
- Issues：创建、列出、关闭、重新打开、评论
- Pull Requests：列出、合并、审查、评论
- 代码内容：获取文件、创建/更新文件
- 评论：Issue/PR 评论
- 仓库内容：浏览目录、获取 README
- 用户活动：获取用户信息、列出 starred 仓库

权限要求（Fine-grained PAT）：
- Contents: Read and Write（代码内容操作）
- Issues: Read and Write（Issues 操作）
- Pull requests: Read and Write（PR 操作）
- Metadata: Read（基础仓库信息）
- Commit statuses: Read（提交状态）
- Actions: Read（工作流运行）
- Administration: Read（仓库管理信息）
- Checks: Read（检查运行）
- Dependabot alerts: Read（安全警报）
- Deployments: Read（部署信息）
- Discussions: Read and Write（讨论区）
- Environments: Read（环境信息）
- Packages: Read（包信息）
- Pages: Read（GitHub Pages）
- Repository security advisories: Read（安全公告）
- Secret scanning alerts: Read（密钥扫描警报）
- Workflows: Read（工作流）
"""

import json
import sys
import os
import requests
import time
import base64

# Import centralized configuration
from config import (
    get_stored_token,
    get_auth_state_file,
    has_token,
    has_browser_session
)


def _get_token():
    """Get stored token from centralized config"""
    token = get_stored_token()
    if token:
        return token
    return os.environ.get("GITHUB_TOKEN", "")


def _has_browser_session():
    """Check if browser session exists"""
    return has_browser_session()


def _use_browser_mode():
    """
    Determine if we should use browser mode.
    Returns True if no token but has browser session.
    """
    return not _get_token() and _has_browser_session()


def _get_browser_context():
    """Get browser context from saved session"""
    try:
        from playwright.sync_api import sync_playwright
        
        auth_file = get_auth_state_file()
        if not os.path.exists(auth_file):
            return None, None, None
        
        p = sync_playwright().start()
        browser = p.chromium.launch(headless=False)  # Visible for user
        context = browser.new_context(storage_state=auth_file)
        return browser, context, p
    except Exception as e:
        print(f"Browser mode error: {e}")
        return None, None, None


def _github_api(endpoint, method="GET", data=None, params=None):
    """Call GitHub API with authentication"""
    token = _get_token()
    if not token:
        return {"success": False, "error": "Not logged in. Please run GitHub login first."}
    
    url = f"https://api.github.com{endpoint}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    try:
        if method == "GET":
            resp = requests.get(url, headers=headers, params=params, timeout=30)
        elif method == "PUT":
            resp = requests.put(url, headers=headers, json=data or {}, timeout=30)
        elif method == "POST":
            resp = requests.post(url, headers=headers, json=data or {}, timeout=30)
        elif method == "PATCH":
            resp = requests.patch(url, headers=headers, json=data or {}, timeout=30)
        elif method == "DELETE":
            resp = requests.delete(url, headers=headers, timeout=30)
        else:
            return {"success": False, "error": f"Unsupported method: {method}"}
        
        if resp.status_code in (200, 201, 202, 204):
            try:
                return {"success": True, "status": resp.status_code, "data": resp.json()}
            except Exception:
                return {"success": True, "status": resp.status_code}
        else:
            try:
                err = resp.json()
                msg = err.get("message", resp.text) if isinstance(err, dict) else str(err)
            except Exception:
                msg = resp.text
            return {"success": False, "status": resp.status_code, "error": msg}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ==================== 仓库操作 ====================

def _browser_star_repo(owner, repo):
    """Star a repo using browser automation"""
    browser, context, p = _get_browser_context()
    if not browser or not context:
        return {"success": False, "error": "No browser session available"}
    
    try:
        page = context.new_page()
        page.goto(f"https://github.com/{owner}/{repo}", timeout=30000)
        
        page.wait_for_selector('button[data-testid="star-button"], button[aria-label*="star"], .btn-sm.btn-primary, [data-ga-click*="star"]', timeout=10000)
        
        star_button = page.locator('button[data-testid="star-button"]').first
        if not star_button.is_visible():
            star_button = page.locator('button:has-text("Star")').first
        
        if star_button.is_visible():
            star_button.click()
            time.sleep(2)
            
            if page.locator('button:has-text("Unstar")').is_visible() or page.locator('button[data-testid="unstar-button"]').is_visible():
                return {"success": True, "method": "browser", "action": "star", "repo": f"{owner}/{repo}"}
        
        return {"success": False, "error": "Could not find or click star button"}
    except Exception as e:
        return {"success": False, "error": f"Browser automation failed: {str(e)}"}
    finally:
        if context:
            context.close()
        if browser:
            browser.close()
        if p:
            p.stop()


def _browser_unstar_repo(owner, repo):
    """Unstar a repo using browser automation"""
    browser, context, p = _get_browser_context()
    if not browser or not context:
        return {"success": False, "error": "No browser session available"}
    
    try:
        page = context.new_page()
        page.goto(f"https://github.com/{owner}/{repo}", timeout=30000)
        
        page.wait_for_selector('button[data-testid="unstar-button"], button:has-text("Unstar")', timeout=10000)
        
        unstar_button = page.locator('button[data-testid="unstar-button"]').first
        if not unstar_button.is_visible():
            unstar_button = page.locator('button:has-text("Unstar")').first
        
        if unstar_button.is_visible():
            unstar_button.click()
            time.sleep(2)
            return {"success": True, "method": "browser", "action": "unstar", "repo": f"{owner}/{repo}"}
        
        return {"success": False, "error": "Could not find or click unstar button"}
    except Exception as e:
        return {"success": False, "error": f"Browser automation failed: {str(e)}"}
    finally:
        if context:
            context.close()
        if browser:
            browser.close()
        if p:
            p.stop()


def _browser_fork_repo(owner, repo):
    """Fork a repo using browser automation"""
    browser, context, p = _get_browser_context()
    if not browser or not context:
        return {"success": False, "error": "No browser session available"}
    
    try:
        page = context.new_page()
        page.goto(f"https://github.com/{owner}/{repo}", timeout=30000)
        
        page.wait_for_selector('button[data-testid="fork-button"], button:has-text("Fork")', timeout=10000)
        
        fork_button = page.locator('button[data-testid="fork-button"]').first
        if not fork_button.is_visible():
            fork_button = page.locator('button:has-text("Fork")').first
        
        if fork_button.is_visible():
            fork_button.click()
            time.sleep(3)
            
            if f"/{repo}" in page.url and "fork" not in page.url.lower():
                new_owner = page.url.split("/")[-2]
                return {"success": True, "method": "browser", "action": "fork", "repo": f"{owner}/{repo}", "forked_to": f"{new_owner}/{repo}"}
        
        return {"success": False, "error": "Could not complete fork action"}
    except Exception as e:
        return {"success": False, "error": f"Browser automation failed: {str(e)}"}
    finally:
        if context:
            context.close()
        if browser:
            browser.close()
        if p:
            p.stop()


def star_repo(owner, repo):
    """Star a repo"""
    if _use_browser_mode():
        print(f"Using browser mode to star {owner}/{repo}...")
        return _browser_star_repo(owner, repo)
    return _github_api(f"/user/starred/{owner}/{repo}", method="PUT")


def unstar_repo(owner, repo):
    """Unstar a repo"""
    if _use_browser_mode():
        print(f"Using browser mode to unstar {owner}/{repo}...")
        return _browser_unstar_repo(owner, repo)
    return _github_api(f"/user/starred/{owner}/{repo}", method="DELETE")


def fork_repo(owner, repo):
    """Fork a repo"""
    if _use_browser_mode():
        print(f"Using browser mode to fork {owner}/{repo}...")
        return _browser_fork_repo(owner, repo)
    return _github_api(f"/repos/{owner}/{repo}/forks", method="POST")


def watch_repo(owner, repo):
    """Watch a repo"""
    if _use_browser_mode():
        return {"success": False, "error": "Watch operation requires API token. Please login with token: python github_login.py token <TOKEN>"}
    return _github_api(
        f"/repos/{owner}/{repo}/subscription",
        method="PUT",
        data={"subscribed": True}
    )


def unwatch_repo(owner, repo):
    """Unwatch a repo"""
    if _use_browser_mode():
        return {"success": False, "error": "Unwatch operation requires API token. Please login with token: python github_login.py token <TOKEN>"}
    return _github_api(f"/repos/{owner}/{repo}/subscription", method="DELETE")


def get_repo_info(owner, repo):
    """Get repository information"""
    return _github_api(f"/repos/{owner}/{repo}")


# ==================== Issues 操作 ====================

def list_issues(owner, repo, state="open", per_page=30):
    """
    List issues in a repository
    state: open, closed, all
    """
    params = {"state": state, "per_page": per_page}
    return _github_api(f"/repos/{owner}/{repo}/issues", params=params)


def get_issue(owner, repo, issue_number):
    """Get a specific issue"""
    return _github_api(f"/repos/{owner}/{repo}/issues/{issue_number}")


def create_issue(owner, repo, title, body=None, labels=None, assignees=None):
    """
    Create a new issue
    Required permission: Issues (Write)
    """
    data = {"title": title}
    if body:
        data["body"] = body
    if labels:
        data["labels"] = labels if isinstance(labels, list) else [labels]
    if assignees:
        data["assignees"] = assignees if isinstance(assignees, list) else [assignees]
    
    return _github_api(f"/repos/{owner}/{repo}/issues", method="POST", data=data)


def update_issue(owner, repo, issue_number, title=None, body=None, state=None, labels=None):
    """
    Update an issue
    state: open, closed
    """
    data = {}
    if title:
        data["title"] = title
    if body:
        data["body"] = body
    if state:
        data["state"] = state
    if labels:
        data["labels"] = labels
    
    return _github_api(f"/repos/{owner}/{repo}/issues/{issue_number}", method="PATCH", data=data)


def close_issue(owner, repo, issue_number):
    """Close an issue"""
    return update_issue(owner, repo, issue_number, state="closed")


def reopen_issue(owner, repo, issue_number):
    """Reopen an issue"""
    return update_issue(owner, repo, issue_number, state="open")


# ==================== Pull Requests 操作 ====================

def list_pull_requests(owner, repo, state="open", per_page=30):
    """
    List pull requests
    state: open, closed, all
    """
    params = {"state": state, "per_page": per_page}
    return _github_api(f"/repos/{owner}/{repo}/pulls", params=params)


def get_pull_request(owner, repo, pr_number):
    """Get a specific pull request"""
    return _github_api(f"/repos/{owner}/{repo}/pulls/{pr_number}")


def create_pull_request(owner, repo, title, head, base, body=None, draft=False, maintainer_can_modify=True):
    """
    Create a new pull request
    Required permission: Pull requests (Write)
    
    owner: repository owner
    repo: repository name
    title: PR title
    head: source branch (e.g., "feature-branch" or "username:branch")
    base: target branch (e.g., "main")
    body: PR description (optional)
    draft: create as draft PR (default: False)
    maintainer_can_modify: allow maintainers to edit the PR (default: True)
    """
    data = {
        "title": title,
        "head": head,
        "base": base,
        "draft": draft,
        "maintainer_can_modify": maintainer_can_modify
    }
    if body:
        data["body"] = body
    
    return _github_api(f"/repos/{owner}/{repo}/pulls", method="POST", data=data)


def update_pull_request(owner, repo, pr_number, title=None, body=None, state=None, base=None, maintainer_can_modify=None):
    """
    Update a pull request
    state: open, closed
    """
    data = {}
    if title:
        data["title"] = title
    if body:
        data["body"] = body
    if state:
        data["state"] = state
    if base:
        data["base"] = base
    if maintainer_can_modify is not None:
        data["maintainer_can_modify"] = maintainer_can_modify
    
    return _github_api(f"/repos/{owner}/{repo}/pulls/{pr_number}", method="PATCH", data=data)


def close_pull_request(owner, repo, pr_number):
    """Close a pull request without merging"""
    return update_pull_request(owner, repo, pr_number, state="closed")


def reopen_pull_request(owner, repo, pr_number):
    """Reopen a closed pull request"""
    return update_pull_request(owner, repo, pr_number, state="open")


def list_pr_files(owner, repo, pr_number):
    """List files changed in a pull request"""
    return _github_api(f"/repos/{owner}/{repo}/pulls/{pr_number}/files")


def list_pr_commits(owner, repo, pr_number):
    """List commits in a pull request"""
    return _github_api(f"/repos/{owner}/{repo}/pulls/{pr_number}/commits")


def check_pr_mergeable(owner, repo, pr_number):
    """Check if a pull request can be merged"""
    return _github_api(f"/repos/{owner}/{repo}/pulls/{pr_number}/merge")


def list_pr_reviews(owner, repo, pr_number):
    """List reviews on a pull request"""
    return _github_api(f"/repos/{owner}/{repo}/pulls/{pr_number}/reviews")


def request_reviewers(owner, repo, pr_number, reviewers=None, team_reviewers=None):
    """
    Request reviewers for a pull request
    reviewers: list of usernames
    team_reviewers: list of team slugs
    """
    data = {}
    if reviewers:
        data["reviewers"] = reviewers if isinstance(reviewers, list) else [reviewers]
    if team_reviewers:
        data["team_reviewers"] = team_reviewers if isinstance(team_reviewers, list) else [team_reviewers]
    
    return _github_api(
        f"/repos/{owner}/{repo}/pulls/{pr_number}/requested_reviewers",
        method="POST",
        data=data
    )


def merge_pull_request(owner, repo, pr_number, commit_title=None, commit_message=None, sha=None):
    """
    Merge a pull request
    Required permission: Pull requests (Write)
    """
    data = {}
    if commit_title:
        data["commit_title"] = commit_title
    if commit_message:
        data["commit_message"] = commit_message
    if sha:
        data["sha"] = sha
    
    return _github_api(f"/repos/{owner}/{repo}/pulls/{pr_number}/merge", method="PUT", data=data)


def create_pull_request_review(owner, repo, pr_number, body=None, event=None, comments=None):
    """
    Create a review on a pull request
    event: APPROVE, REQUEST_CHANGES, COMMENT
    """
    data = {}
    if body:
        data["body"] = body
    if event:
        data["event"] = event
    if comments:
        data["comments"] = comments
    
    return _github_api(f"/repos/{owner}/{repo}/pulls/{pr_number}/reviews", method="POST", data=data)


def approve_pull_request(owner, repo, pr_number, body=None):
    """Approve a pull request"""
    return create_pull_request_review(owner, repo, pr_number, body=body, event="APPROVE")


def request_changes_pull_request(owner, repo, pr_number, body):
    """Request changes on a pull request"""
    return create_pull_request_review(owner, repo, pr_number, body=body, event="REQUEST_CHANGES")


# ==================== 代码内容操作 ====================

def get_file_content(owner, repo, path, ref=None):
    """
    Get the contents of a file or directory
    Required permission: Contents (Read)
    """
    params = {}
    if ref:
        params["ref"] = ref
    
    result = _github_api(f"/repos/{owner}/{repo}/contents/{path}", params=params)
    if result["success"] and "data" in result:
        data = result["data"]
        # If it's a file, decode the content
        if isinstance(data, dict) and data.get("type") == "file" and "content" in data:
            try:
                content = base64.b64decode(data["content"]).decode("utf-8")
                data["decoded_content"] = content
            except Exception:
                pass
        result["data"] = data
    
    return result


def get_readme(owner, repo, ref=None):
    """Get the README of a repository"""
    params = {}
    if ref:
        params["ref"] = ref
    
    result = _github_api(f"/repos/{owner}/{repo}/readme", params=params)
    if result["success"] and "data" in result:
        data = result["data"]
        if "content" in data:
            try:
                content = base64.b64decode(data["content"]).decode("utf-8")
                data["decoded_content"] = content
            except Exception:
                pass
        result["data"] = data
    
    return result


def create_or_update_file(owner, repo, path, message, content, sha=None, branch=None):
    """
    Create or update a file in the repository
    Required permission: Contents (Write)
    
    content: string content (will be base64 encoded)
    sha: required if updating an existing file
    branch: target branch (default: default branch)
    """
    data = {
        "message": message,
        "content": base64.b64encode(content.encode("utf-8")).decode("utf-8")
    }
    if sha:
        data["sha"] = sha
    if branch:
        data["branch"] = branch
    
    return _github_api(f"/repos/{owner}/{repo}/contents/{path}", method="PUT", data=data)


def delete_file(owner, repo, path, message, sha, branch=None):
    """
    Delete a file from the repository
    Required permission: Contents (Write)
    """
    data = {
        "message": message,
        "sha": sha
    }
    if branch:
        data["branch"] = branch
    
    return _github_api(f"/repos/{owner}/{repo}/contents/{path}", method="DELETE", data=data)


def list_directory(owner, repo, path="", ref=None):
    """
    List contents of a directory
    """
    return get_file_content(owner, repo, path or "", ref=ref)


# ==================== 评论操作 ====================

def list_issue_comments(owner, repo, issue_number):
    """List comments on an issue"""
    return _github_api(f"/repos/{owner}/{repo}/issues/{issue_number}/comments")


def create_issue_comment(owner, repo, issue_number, body):
    """
    Create a comment on an issue
    Required permission: Issues (Write)
    """
    return _github_api(
        f"/repos/{owner}/{repo}/issues/{issue_number}/comments",
        method="POST",
        data={"body": body}
    )


def list_pr_comments(owner, repo, pr_number):
    """List review comments on a pull request"""
    return _github_api(f"/repos/{owner}/{repo}/pulls/{pr_number}/comments")


def create_pr_review_comment(owner, repo, pr_number, body, commit_id, path, position):
    """
    Create a review comment on a specific line of a pull request
    Required permission: Pull requests (Write)
    """
    data = {
        "body": body,
        "commit_id": commit_id,
        "path": path,
        "position": position
    }
    return _github_api(f"/repos/{owner}/{repo}/pulls/{pr_number}/comments", method="POST", data=data)


# ==================== 用户操作 ====================

def get_user(username=None):
    """
    Get user information
    If username is None, gets the authenticated user
    """
    if username:
        return _github_api(f"/users/{username}")
    return _github_api("/user")


def get_user_repos(username=None, type="owner", sort="updated", per_page=30):
    """
    List repositories for a user
    If username is None, lists authenticated user's repos
    
    type: all, owner, member (default: owner)
    sort: created, updated, pushed, full_name (default: updated)
    """
    params = {"type": type, "sort": sort, "per_page": per_page}
    if username:
        return _github_api(f"/users/{username}/repos", params=params)
    return _github_api("/user/repos", params=params)


def get_my_repos(type="owner", sort="updated", per_page=30):
    """List authenticated user's repositories"""
    return get_user_repos(username=None, type=type, sort=sort, per_page=per_page)


def list_user_starred(username, sort="updated", direction="desc", per_page=30):
    """List repositories starred by a user"""
    params = {"sort": sort, "direction": direction, "per_page": per_page}
    return _github_api(f"/users/{username}/starred", params=params)


def get_user_followers(username=None, per_page=30):
    """List followers of a user (authenticated user if username is None)"""
    params = {"per_page": per_page}
    if username:
        return _github_api(f"/users/{username}/followers", params=params)
    return _github_api("/user/followers", params=params)


def get_user_following(username=None, per_page=30):
    """List users that a user is following (authenticated user if username is None)"""
    params = {"per_page": per_page}
    if username:
        return _github_api(f"/users/{username}/following", params=params)
    return _github_api("/user/following", params=params)


def follow_user(username):
    """Follow a user"""
    return _github_api(f"/user/following/{username}", method="PUT")


def unfollow_user(username):
    """Unfollow a user"""
    return _github_api(f"/user/following/{username}", method="DELETE")


def check_following(username):
    """Check if the authenticated user is following another user"""
    return _github_api(f"/user/following/{username}")


# ==================== 仓库创建/管理 ====================

def create_repo(name, description=None, private=False, auto_init=False, gitignore_template=None, license_template=None):
    """
    Create a new repository for the authenticated user
    
    name: repository name
    description: repository description (optional)
    private: make repository private (default: False)
    auto_init: initialize with README (default: False)
    gitignore_template: .gitignore template (e.g., "Python", "Node")
    license_template: license template (e.g., "mit", "apache-2.0")
    """
    data = {
        "name": name,
        "private": private,
        "auto_init": auto_init
    }
    if description:
        data["description"] = description
    if gitignore_template:
        data["gitignore_template"] = gitignore_template
    if license_template:
        data["license_template"] = license_template
    
    return _github_api("/user/repos", method="POST", data=data)


def update_repo(owner, repo, description=None, homepage=None, private=None, has_issues=None, has_projects=None, has_wiki=None, default_branch=None):
    """Update repository settings"""
    data = {}
    if description is not None:
        data["description"] = description
    if homepage is not None:
        data["homepage"] = homepage
    if private is not None:
        data["private"] = private
    if has_issues is not None:
        data["has_issues"] = has_issues
    if has_projects is not None:
        data["has_projects"] = has_projects
    if has_wiki is not None:
        data["has_wiki"] = has_wiki
    if default_branch is not None:
        data["default_branch"] = default_branch
    
    return _github_api(f"/repos/{owner}/{repo}", method="PATCH", data=data)


def delete_repo(owner, repo):
    """Delete a repository (requires delete_repo scope)"""
    return _github_api(f"/repos/{owner}/{repo}", method="DELETE")


def list_forks(owner, repo, per_page=30):
    """List forks of a repository"""
    return _github_api(f"/repos/{owner}/{repo}/forks", params={"per_page": per_page})


def list_stargazers(owner, repo, per_page=30):
    """List users who have starred a repository"""
    return _github_api(f"/repos/{owner}/{repo}/stargazers", params={"per_page": per_page})


def list_watchers(owner, repo, per_page=30):
    """List users watching a repository"""
    return _github_api(f"/repos/{owner}/{repo}/subscribers", params={"per_page": per_page})


def check_starred(owner, repo):
    """Check if the authenticated user has starred a repository"""
    return _github_api(f"/user/starred/{owner}/{repo}")


# ==================== Issue Labels 操作 ====================

def list_issue_labels(owner, repo, issue_number):
    """List labels for an issue"""
    return _github_api(f"/repos/{owner}/{repo}/issues/{issue_number}/labels")


def add_issue_labels(owner, repo, issue_number, labels):
    """
    Add labels to an issue
    labels: list of label names (strings)
    """
    data = {"labels": labels if isinstance(labels, list) else [labels]}
    return _github_api(f"/repos/{owner}/{repo}/issues/{issue_number}/labels", method="POST", data=data)


def set_issue_labels(owner, repo, issue_number, labels):
    """
    Set (replace) labels for an issue
    labels: list of label names (strings)
    """
    data = {"labels": labels if isinstance(labels, list) else [labels]}
    return _github_api(f"/repos/{owner}/{repo}/issues/{issue_number}/labels", method="PUT", data=data)


def remove_issue_label(owner, repo, issue_number, label_name):
    """Remove a label from an issue"""
    return _github_api(f"/repos/{owner}/{repo}/issues/{issue_number}/labels/{label_name}", method="DELETE")


def clear_issue_labels(owner, repo, issue_number):
    """Remove all labels from an issue"""
    return _github_api(f"/repos/{owner}/{repo}/issues/{issue_number}/labels", method="DELETE")


def list_repo_labels(owner, repo, per_page=30):
    """List all labels for a repository"""
    return _github_api(f"/repos/{owner}/{repo}/labels", params={"per_page": per_page})


def create_label(owner, repo, name, color, description=None):
    """
    Create a label for a repository
    color: hex color code without # (e.g., "ff0000" for red)
    """
    data = {"name": name, "color": color}
    if description:
        data["description"] = description
    return _github_api(f"/repos/{owner}/{repo}/labels", method="POST", data=data)


def update_label(owner, repo, label_name, new_name=None, color=None, description=None):
    """Update a repository label"""
    data = {}
    if new_name:
        data["new_name"] = new_name
    if color:
        data["color"] = color
    if description is not None:
        data["description"] = description
    return _github_api(f"/repos/{owner}/{repo}/labels/{label_name}", method="PATCH", data=data)


def delete_label(owner, repo, label_name):
    """Delete a label from a repository"""
    return _github_api(f"/repos/{owner}/{repo}/labels/{label_name}", method="DELETE")


# ==================== Issue Assignees 操作 ====================

def add_issue_assignees(owner, repo, issue_number, assignees):
    """Add assignees to an issue"""
    data = {"assignees": assignees if isinstance(assignees, list) else [assignees]}
    return _github_api(f"/repos/{owner}/{repo}/issues/{issue_number}/assignees", method="POST", data=data)


def remove_issue_assignee(owner, repo, issue_number, assignee):
    """Remove an assignee from an issue"""
    data = {"assignees": [assignee]}
    return _github_api(f"/repos/{owner}/{repo}/issues/{issue_number}/assignees", method="DELETE", data=data)


# ==================== Issue 锁定操作 ====================

def lock_issue(owner, repo, issue_number, lock_reason=None):
    """
    Lock an issue
    
    lock_reason: off-topic, too heated, resolved, spam (optional)
    """
    data = {}
    if lock_reason:
        data["lock_reason"] = lock_reason
    return _github_api(f"/repos/{owner}/{repo}/issues/{issue_number}/lock", method="PUT", data=data)


def unlock_issue(owner, repo, issue_number):
    """Unlock an issue"""
    return _github_api(f"/repos/{owner}/{repo}/issues/{issue_number}/lock", method="DELETE")


# ==================== 通知操作 ====================

def list_notifications(show_all=False, participating=False, since=None, before=None, per_page=30):
    """
    List notifications for the authenticated user
    
    show_all: show all notifications, not just unread (default: False)
    participating: only show notifications where user is participating (default: False)
    since: only show notifications after this time (ISO 8601 format)
    before: only show notifications before this time (ISO 8601 format)
    """
    params = {"per_page": per_page}
    if show_all:
        params["all"] = "true"
    if participating:
        params["participating"] = "true"
    if since:
        params["since"] = since
    if before:
        params["before"] = before
    
    return _github_api("/notifications", params=params)


def list_repo_notifications(owner, repo, show_all=False, participating=False, since=None, before=None, per_page=30):
    """List notifications for a specific repository"""
    params = {"per_page": per_page}
    if show_all:
        params["all"] = "true"
    if participating:
        params["participating"] = "true"
    if since:
        params["since"] = since
    if before:
        params["before"] = before
    
    return _github_api(f"/repos/{owner}/{repo}/notifications", params=params)


def mark_notification_read(thread_id):
    """Mark a notification as read"""
    return _github_api(f"/notifications/threads/{thread_id}", method="PATCH")


def mark_all_notifications_read(last_read_at=None):
    """Mark all notifications as read"""
    data = {}
    if last_read_at:
        data["last_read_at"] = last_read_at
    return _github_api("/notifications", method="PUT", data=data)


# ==================== 组织操作 ====================

def list_my_orgs(per_page=30):
    """List organizations for the authenticated user"""
    return _github_api("/user/orgs", params={"per_page": per_page})


def get_org(org):
    """Get an organization"""
    return _github_api(f"/orgs/{org}")


def list_org_repos(org, type="all", per_page=30):
    """List repositories for an organization"""
    params = {"type": type, "per_page": per_page}
    return _github_api(f"/orgs/{org}/repos", params=params)


def list_org_members(org, per_page=30):
    """List members of an organization"""
    return _github_api(f"/orgs/{org}/members", params={"per_page": per_page})


# ==================== Gist 操作 ====================

def list_gists(username=None, per_page=30):
    """List gists (authenticated user's if username is None)"""
    params = {"per_page": per_page}
    if username:
        return _github_api(f"/users/{username}/gists", params=params)
    return _github_api("/gists", params=params)


def get_gist(gist_id):
    """Get a specific gist"""
    return _github_api(f"/gists/{gist_id}")


def create_gist(files, description=None, public=False):
    """
    Create a gist
    
    files: dict of filename -> {"content": "..."}
    description: gist description (optional)
    public: make gist public (default: False)
    """
    data = {"files": files, "public": public}
    if description:
        data["description"] = description
    
    return _github_api("/gists", method="POST", data=data)


def update_gist(gist_id, files=None, description=None):
    """Update a gist"""
    data = {}
    if files:
        data["files"] = files
    if description:
        data["description"] = description
    
    return _github_api(f"/gists/{gist_id}", method="PATCH", data=data)


def delete_gist(gist_id):
    """Delete a gist"""
    return _github_api(f"/gists/{gist_id}", method="DELETE")


# ==================== 其他操作 ====================

def get_starred_repos():
    """Get list of starred repositories for current user"""
    result = _github_api("/user/starred")
    if result["success"]:
        repos = []
        for item in result.get("data", []):
            repos.append({
                "name": item.get("full_name", ""),
                "url": item.get("html_url", ""),
                "stars": item.get("stargazers_count", 0),
                "description": item.get("description", "") or "",
            })
        return {"success": True, "count": len(repos), "data": repos}
    return result


def _detect_token_type():
    """Detect if token is Fine-grained or Classic"""
    token = _get_token()
    if not token:
        return "none"
    # Fine-grained tokens start with 'github_pat_'
    if token.startswith('github_pat_'):
        return "fine-grained"
    # Classic tokens start with 'ghp_', 'gho_', 'ghu_', 'ghs_', 'ghr_'
    elif token.startswith(('ghp_', 'gho_', 'ghu_', 'ghs_', 'ghr_')):
        return "classic"
    else:
        return "unknown"


def check_auth():
    """Check if current token is valid and get user info"""
    result = _github_api("/user")
    token_type = _detect_token_type()
    
    if result["success"]:
        user = result.get("data", {})
        return {
            "success": True,
            "username": user.get("login", ""),
            "name": user.get("name", ""),
            "email": user.get("email", ""),
            "avatar": user.get("avatar_url", ""),
            "public_repos": user.get("public_repos", 0),
            "private_repos": user.get("total_private_repos", 0),
            "followers": user.get("followers", 0),
            "following": user.get("following", 0),
            "token_type": token_type,
            "token_type_display": {
                "fine-grained": "Fine-grained PAT",
                "classic": "Classic PAT",
                "none": "Not logged in",
                "unknown": "Unknown token type"
            }.get(token_type, "Unknown")
        }
    else:
        result["token_type"] = token_type
        result["token_type_display"] = {
            "fine-grained": "Fine-grained PAT",
            "classic": "Classic PAT",
            "none": "Not logged in",
            "unknown": "Unknown token type"
        }.get(token_type, "Unknown")
    return result


def get_rate_limit():
    """Get current rate limit status"""
    return _github_api("/rate_limit")


def list_commits(owner, repo, sha=None, path=None, per_page=30):
    """
    List commits in a repository
    """
    params = {"per_page": per_page}
    if sha:
        params["sha"] = sha
    if path:
        params["path"] = path
    
    return _github_api(f"/repos/{owner}/{repo}/commits", params=params)


def get_commit(owner, repo, ref):
    """Get a specific commit"""
    return _github_api(f"/repos/{owner}/{repo}/commits/{ref}")


def list_branches(owner, repo, per_page=30):
    """List branches in a repository"""
    return _github_api(f"/repos/{owner}/{repo}/branches", params={"per_page": per_page})


def get_branch(owner, repo, branch):
    """Get a specific branch"""
    return _github_api(f"/repos/{owner}/{repo}/branches/{branch}")


def create_branch(owner, repo, branch_name, from_branch=None):
    """
    Create a new branch
    from_branch: source branch (default: repository's default branch)
    """
    # First get the default branch if not specified
    if not from_branch:
        repo_info = get_repo_info(owner, repo)
        if not repo_info["success"]:
            return repo_info
        from_branch = repo_info["data"].get("default_branch", "main")
    
    # Get the SHA of the source branch
    ref_result = _github_api(f"/repos/{owner}/{repo}/git/refs/heads/{from_branch}")
    if not ref_result["success"]:
        return ref_result
    
    sha = ref_result["data"]["object"]["sha"]
    
    # Create the new branch
    return _github_api(
        f"/repos/{owner}/{repo}/git/refs",
        method="POST",
        data={
            "ref": f"refs/heads/{branch_name}",
            "sha": sha
        }
    )


def delete_branch(owner, repo, branch):
    """Delete a branch"""
    return _github_api(f"/repos/{owner}/{repo}/git/refs/heads/{branch}", method="DELETE")


def list_releases(owner, repo, per_page=30):
    """List releases in a repository"""
    return _github_api(f"/repos/{owner}/{repo}/releases", params={"per_page": per_page})


def get_release(owner, repo, release_id):
    """Get a specific release"""
    return _github_api(f"/repos/{owner}/{repo}/releases/{release_id}")


def get_release_by_tag(owner, repo, tag):
    """Get a release by tag name"""
    return _github_api(f"/repos/{owner}/{repo}/releases/tags/{tag}")


def create_release(owner, repo, tag_name, name=None, body=None, draft=False, prerelease=False, target_commitish=None):
    """
    Create a new release
    Required permission: Contents (Write)
    
    tag_name: tag name for the release
    name: release title (optional, defaults to tag_name)
    body: release description (optional)
    draft: create as draft (default: False)
    prerelease: mark as prerelease (default: False)
    target_commitish: commitish for the tag (optional)
    """
    data = {
        "tag_name": tag_name,
        "draft": draft,
        "prerelease": prerelease
    }
    if name:
        data["name"] = name
    if body:
        data["body"] = body
    if target_commitish:
        data["target_commitish"] = target_commitish
    
    return _github_api(f"/repos/{owner}/{repo}/releases", method="POST", data=data)


def update_release(owner, repo, release_id, tag_name=None, name=None, body=None, draft=None, prerelease=None):
    """Update a release"""
    data = {}
    if tag_name:
        data["tag_name"] = tag_name
    if name:
        data["name"] = name
    if body:
        data["body"] = body
    if draft is not None:
        data["draft"] = draft
    if prerelease is not None:
        data["prerelease"] = prerelease
    
    return _github_api(f"/repos/{owner}/{repo}/releases/{release_id}", method="PATCH", data=data)


def delete_release(owner, repo, release_id):
    """Delete a release"""
    return _github_api(f"/repos/{owner}/{repo}/releases/{release_id}", method="DELETE")


def get_workflow_runs(owner, repo, per_page=30):
    """
    List workflow runs (Actions)
    Required permission: Actions (Read)
    """
    return _github_api(f"/repos/{owner}/{repo}/actions/runs", params={"per_page": per_page})


def get_workflow(owner, repo, workflow_id):
    """Get a specific workflow"""
    return _github_api(f"/repos/{owner}/{repo}/actions/workflows/{workflow_id}")


def trigger_workflow(owner, repo, workflow_id, ref="main", inputs=None):
    """
    Trigger a workflow dispatch event
    Required permission: Contents (Read/Write) for the repository
    
    workflow_id: workflow filename or ID
    ref: branch or tag reference (default: main)
    inputs: workflow inputs (optional)
    """
    data = {"ref": ref}
    if inputs:
        data["inputs"] = inputs
    
    return _github_api(
        f"/repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches",
        method="POST",
        data=data
    )


def cancel_workflow_run(owner, repo, run_id):
    """Cancel a workflow run"""
    return _github_api(f"/repos/{owner}/{repo}/actions/runs/{run_id}/cancel", method="POST")


def rerun_workflow(owner, repo, run_id):
    """Re-run a workflow"""
    return _github_api(f"/repos/{owner}/{repo}/actions/runs/{run_id}/rerun", method="POST")


# ==================== 主程序 ====================

def print_usage():
    print("""GitHub Operations - 完整的 GitHub 操作工具集

用法: python github_operations.py <操作> [参数...]

用户操作:
  user [username]                获取用户信息（不提供用户名则获取当前用户）
  my-repos [type]                列出当前用户的仓库 (type: all/owner/member)
  user-repos <username> [type]   列出指定用户的仓库
  followers [username]           列出粉丝（不提供用户名则列出当前用户粉丝）
  following [username]           列出关注的人
  follow <username>              关注用户
  unfollow <username>            取消关注用户

仓库操作:
  star <owner/repo>              Star 仓库
  unstar <owner/repo>            Unstar 仓库
  fork <owner/repo>              Fork 仓库
  watch <owner/repo>             Watch 仓库
  unwatch <owner/repo>           Unwatch 仓库
  info <owner/repo>              获取仓库信息
  create-repo <name> [desc]      创建新仓库
  forks <owner/repo>             列出仓库的 Forks
  stargazers <owner/repo>        列出 Stargazers

分支操作:
  branches <owner/repo>          列出分支
  branch <owner/repo> <name>     获取分支信息
  create-branch <owner/repo> <branch> [from]  创建分支

Issues 操作:
  issues <owner/repo> [state]    列出 Issues (state: open/closed/all)
  issue <owner/repo> <number>    获取指定 Issue
  create-issue <owner/repo> <title> [body]  创建 Issue
  close-issue <owner/repo> <number>         关闭 Issue
  reopen-issue <owner/repo> <number>        重新打开 Issue
  labels <owner/repo> <issue_num>           列出 Issue 标签
  add-labels <owner/repo> <issue_num> <labels...>  添加标签
  lock-issue <owner/repo> <number> [reason] 锁定 Issue
  unlock-issue <owner/repo> <number>        解锁 Issue

Pull Requests 操作:
  prs <owner/repo> [state]       列出 PRs (state: open/closed/all)
  pr <owner/repo> <number>       获取指定 PR
  create-pr <owner/repo> <title> <head> <base> [body]  创建 PR
  close-pr <owner/repo> <number> 关闭 PR
  reopen-pr <owner/repo> <number> 重新打开 PR
  merge-pr <owner/repo> <number> [title]    合并 PR
  approve-pr <owner/repo> <number> [body]   批准 PR
  pr-files <owner/repo> <number> 列出 PR 修改的文件
  pr-commits <owner/repo> <number> 列出 PR 的提交
  pr-reviews <owner/repo> <number> 列出 PR 审查

代码内容操作:
  file <owner/repo> <path> [ref]            获取文件内容
  readme <owner/repo> [ref]                 获取 README
  ls <owner/repo> [path] [ref]              列出目录内容
  create-file <owner/repo> <path> <message> <content>  创建/更新文件

Releases 操作:
  releases <owner/repo>          列出 Releases
  release <owner/repo> <id>      获取指定 Release
  create-release <owner/repo> <tag> [name] [body]  创建 Release

Actions 操作:
  workflows <owner/repo>         列出工作流运行
  workflow <owner/repo> <id>     获取指定工作流
  trigger-workflow <owner/repo> <workflow_id> [ref]  触发工作流

评论操作:
  comments <owner/repo> <issue_number>      列出 Issue 评论
  comment <owner/repo> <issue_number> <body>  创建 Issue 评论

通知操作:
  notifications [--all]          列出通知（--all 显示已读）
  repo-notifications <owner/repo> [--all]  列出仓库通知
  mark-read <thread_id>          标记通知已读

组织操作:
  orgs                           列出当前用户的组织
  org <org_name>                 获取组织信息
  org-repos <org_name>           列出组织仓库
  org-members <org_name>         列出组织成员

其他操作:
  starred                        列出当前用户 Starred 仓库
  check                          检查登录状态
  rate-limit                     查看 API 限流状态
  commits <owner/repo> [path]    列出提交

示例:
  python github_operations.py user torvalds
  python github_operations.py my-repos owner
  python github_operations.py star facebook/react
  python github_operations.py create-repo my-new-repo "Description here"
  python github_operations.py create-pr owner/repo "Fix bug" feature-branch main
  python github_operations.py issues microsoft/vscode open
  python github_operations.py file torvalds/linux README.md
  python github_operations.py notifications --all
""")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    action = sys.argv[1]
    
    # 简单操作（无需 owner/repo）
    simple_actions = {
        "starred": get_starred_repos,
        "check": check_auth,
        "rate-limit": get_rate_limit,
        "my-repos": lambda: get_my_repos(),
        "orgs": list_my_orgs,
        "notifications": lambda: list_notifications(show_all="--all" in sys.argv),
    }
    
    if action in simple_actions:
        print(json.dumps(simple_actions[action](), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    # 用户操作
    if action == "user":
        username = sys.argv[2] if len(sys.argv) > 2 else None
        print(json.dumps(get_user(username), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "user-repos":
        if len(sys.argv) < 3:
            print("请提供用户名")
            sys.exit(1)
        print(json.dumps(get_user_repos(sys.argv[2]), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "followers":
        username = sys.argv[2] if len(sys.argv) > 2 else None
        print(json.dumps(get_user_followers(username), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "following":
        username = sys.argv[2] if len(sys.argv) > 2 else None
        print(json.dumps(get_user_following(username), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "follow":
        if len(sys.argv) < 3:
            print("请提供用户名")
            sys.exit(1)
        print(json.dumps(follow_user(sys.argv[2]), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "unfollow":
        if len(sys.argv) < 3:
            print("请提供用户名")
            sys.exit(1)
        print(json.dumps(unfollow_user(sys.argv[2]), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "create-repo":
        if len(sys.argv) < 3:
            print("请提供仓库名称")
            sys.exit(1)
        name = sys.argv[2]
        description = sys.argv[3] if len(sys.argv) > 3 else None
        print(json.dumps(create_repo(name, description), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    # 组织操作
    if action == "org":
        if len(sys.argv) < 3:
            print("请提供组织名称")
            sys.exit(1)
        print(json.dumps(get_org(sys.argv[2]), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "org-repos":
        if len(sys.argv) < 3:
            print("请提供组织名称")
            sys.exit(1)
        print(json.dumps(list_org_repos(sys.argv[2]), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "org-members":
        if len(sys.argv) < 3:
            print("请提供组织名称")
            sys.exit(1)
        print(json.dumps(list_org_members(sys.argv[2]), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    # 需要 owner/repo 的操作
    if len(sys.argv) < 3:
        print(f"操作 '{action}' 需要 owner/repo 参数")
        print_usage()
        sys.exit(1)
    
    repo_path = sys.argv[2]
    if "/" not in repo_path:
        print("请使用 owner/repo 格式，例如: octocat/claude-code")
        sys.exit(1)
    
    owner, repo = repo_path.split("/", 1)
    
    # 仓库操作
    repo_actions = {
        "star": lambda: star_repo(owner, repo),
        "unstar": lambda: unstar_repo(owner, repo),
        "fork": lambda: fork_repo(owner, repo),
        "watch": lambda: watch_repo(owner, repo),
        "unwatch": lambda: unwatch_repo(owner, repo),
        "info": lambda: get_repo_info(owner, repo),
        "branches": lambda: list_branches(owner, repo),
        "releases": lambda: list_releases(owner, repo),
        "workflows": lambda: get_workflow_runs(owner, repo),
        "forks": lambda: list_forks(owner, repo),
        "stargazers": lambda: list_stargazers(owner, repo),
        "watchers": lambda: list_watchers(owner, repo),
    }
    
    if action in repo_actions:
        result = repo_actions[action]()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)
    
    # Issues 操作
    if action == "issues":
        state = sys.argv[3] if len(sys.argv) > 3 else "open"
        print(json.dumps(list_issues(owner, repo, state), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "issue":
        if len(sys.argv) < 4:
            print("请提供 Issue 编号")
            sys.exit(1)
        print(json.dumps(get_issue(owner, repo, int(sys.argv[3])), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "create-issue":
        if len(sys.argv) < 4:
            print("请提供 Issue 标题")
            sys.exit(1)
        title = sys.argv[3]
        body = sys.argv[4] if len(sys.argv) > 4 else None
        print(json.dumps(create_issue(owner, repo, title, body), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "close-issue":
        if len(sys.argv) < 4:
            print("请提供 Issue 编号")
            sys.exit(1)
        print(json.dumps(close_issue(owner, repo, int(sys.argv[3])), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "reopen-issue":
        if len(sys.argv) < 4:
            print("请提供 Issue 编号")
            sys.exit(1)
        print(json.dumps(reopen_issue(owner, repo, int(sys.argv[3])), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    # PR 操作
    if action == "prs":
        state = sys.argv[3] if len(sys.argv) > 3 else "open"
        print(json.dumps(list_pull_requests(owner, repo, state), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "pr":
        if len(sys.argv) < 4:
            print("请提供 PR 编号")
            sys.exit(1)
        print(json.dumps(get_pull_request(owner, repo, int(sys.argv[3])), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "merge-pr":
        if len(sys.argv) < 4:
            print("请提供 PR 编号")
            sys.exit(1)
        title = sys.argv[4] if len(sys.argv) > 4 else None
        print(json.dumps(merge_pull_request(owner, repo, int(sys.argv[3]), title), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "approve-pr":
        if len(sys.argv) < 4:
            print("请提供 PR 编号")
            sys.exit(1)
        body = sys.argv[4] if len(sys.argv) > 4 else None
        print(json.dumps(approve_pull_request(owner, repo, int(sys.argv[3]), body), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "create-pr":
        if len(sys.argv) < 6:
            print("用法: create-pr <owner/repo> <title> <head> <base> [body]")
            sys.exit(1)
        title = sys.argv[3]
        head = sys.argv[4]
        base = sys.argv[5]
        body = sys.argv[6] if len(sys.argv) > 6 else None
        print(json.dumps(create_pull_request(owner, repo, title, head, base, body), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "close-pr":
        if len(sys.argv) < 4:
            print("请提供 PR 编号")
            sys.exit(1)
        print(json.dumps(close_pull_request(owner, repo, int(sys.argv[3])), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "reopen-pr":
        if len(sys.argv) < 4:
            print("请提供 PR 编号")
            sys.exit(1)
        print(json.dumps(reopen_pull_request(owner, repo, int(sys.argv[3])), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "pr-files":
        if len(sys.argv) < 4:
            print("请提供 PR 编号")
            sys.exit(1)
        print(json.dumps(list_pr_files(owner, repo, int(sys.argv[3])), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "pr-commits":
        if len(sys.argv) < 4:
            print("请提供 PR 编号")
            sys.exit(1)
        print(json.dumps(list_pr_commits(owner, repo, int(sys.argv[3])), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "pr-reviews":
        if len(sys.argv) < 4:
            print("请提供 PR 编号")
            sys.exit(1)
        print(json.dumps(list_pr_reviews(owner, repo, int(sys.argv[3])), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    # 分支操作
    if action == "branch":
        if len(sys.argv) < 4:
            print("请提供分支名称")
            sys.exit(1)
        print(json.dumps(get_branch(owner, repo, sys.argv[3]), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "create-branch":
        if len(sys.argv) < 4:
            print("用法: create-branch <owner/repo> <branch_name> [from_branch]")
            sys.exit(1)
        branch_name = sys.argv[3]
        from_branch = sys.argv[4] if len(sys.argv) > 4 else None
        print(json.dumps(create_branch(owner, repo, branch_name, from_branch), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    # Release 操作
    if action == "release":
        if len(sys.argv) < 4:
            print("请提供 Release ID")
            sys.exit(1)
        print(json.dumps(get_release(owner, repo, sys.argv[3]), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "create-release":
        if len(sys.argv) < 4:
            print("用法: create-release <owner/repo> <tag> [name] [body]")
            sys.exit(1)
        tag = sys.argv[3]
        name = sys.argv[4] if len(sys.argv) > 4 else None
        body = sys.argv[5] if len(sys.argv) > 5 else None
        print(json.dumps(create_release(owner, repo, tag, name, body), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    # Workflow 操作
    if action == "workflow":
        if len(sys.argv) < 4:
            print("请提供 Workflow ID")
            sys.exit(1)
        print(json.dumps(get_workflow(owner, repo, sys.argv[3]), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "trigger-workflow":
        if len(sys.argv) < 4:
            print("用法: trigger-workflow <owner/repo> <workflow_id> [ref]")
            sys.exit(1)
        workflow_id = sys.argv[3]
        ref = sys.argv[4] if len(sys.argv) > 4 else "main"
        print(json.dumps(trigger_workflow(owner, repo, workflow_id, ref), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    # Issue Labels 操作
    if action == "labels":
        if len(sys.argv) < 4:
            print("请提供 Issue 编号")
            sys.exit(1)
        print(json.dumps(list_issue_labels(owner, repo, int(sys.argv[3])), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "add-labels":
        if len(sys.argv) < 5:
            print("用法: add-labels <owner/repo> <issue_number> <label1> [label2...]")
            sys.exit(1)
        issue_number = int(sys.argv[3])
        labels = sys.argv[4:]
        print(json.dumps(add_issue_labels(owner, repo, issue_number, labels), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    # Issue 锁定操作
    if action == "lock-issue":
        if len(sys.argv) < 4:
            print("用法: lock-issue <owner/repo> <issue_number> [reason]")
            sys.exit(1)
        reason = sys.argv[4] if len(sys.argv) > 4 else None
        print(json.dumps(lock_issue(owner, repo, int(sys.argv[3]), reason), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "unlock-issue":
        if len(sys.argv) < 4:
            print("请提供 Issue 编号")
            sys.exit(1)
        print(json.dumps(unlock_issue(owner, repo, int(sys.argv[3])), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    # 通知操作
    if action == "repo-notifications":
        show_all_flag = "--all" in sys.argv
        print(json.dumps(list_repo_notifications(owner, repo, show_all=show_all_flag), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "mark-read":
        if len(sys.argv) < 3:
            print("请提供 Thread ID")
            sys.exit(1)
        print(json.dumps(mark_notification_read(sys.argv[2]), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    # 代码内容操作
    if action == "file":
        if len(sys.argv) < 4:
            print("请提供文件路径")
            sys.exit(1)
        path = sys.argv[3]
        ref = sys.argv[4] if len(sys.argv) > 4 else None
        print(json.dumps(get_file_content(owner, repo, path, ref), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "readme":
        ref = sys.argv[3] if len(sys.argv) > 3 else None
        print(json.dumps(get_readme(owner, repo, ref), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "ls":
        path = sys.argv[3] if len(sys.argv) > 3 else ""
        ref = sys.argv[4] if len(sys.argv) > 4 else None
        print(json.dumps(list_directory(owner, repo, path, ref), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "create-file":
        if len(sys.argv) < 6:
            print("用法: create-file <owner/repo> <path> <message> <content>")
            sys.exit(1)
        path = sys.argv[3]
        message = sys.argv[4]
        content = sys.argv[5]
        print(json.dumps(create_or_update_file(owner, repo, path, message, content), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    # 评论操作
    if action == "comments":
        if len(sys.argv) < 4:
            print("请提供 Issue 编号")
            sys.exit(1)
        print(json.dumps(list_issue_comments(owner, repo, int(sys.argv[3])), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "comment":
        if len(sys.argv) < 5:
            print("请提供 Issue 编号和评论内容")
            sys.exit(1)
        print(json.dumps(create_issue_comment(owner, repo, int(sys.argv[3]), sys.argv[4]), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    # Commits
    if action == "commits":
        path = sys.argv[3] if len(sys.argv) > 3 else None
        print(json.dumps(list_commits(owner, repo, path=path), ensure_ascii=False, indent=2))
        sys.exit(0)
    
    print(f"未知操作: {action}")
    print_usage()
    sys.exit(1)
