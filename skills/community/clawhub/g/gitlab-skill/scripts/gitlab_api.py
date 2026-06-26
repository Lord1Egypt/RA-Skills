#!/usr/bin/env python3
"""
GitLab API helper script for Claude Code GitLab skill
Supports multiple GitLab operations: listing repos, issues, MRs, branches, etc.
"""

import json
import urllib.request
import urllib.error
import urllib.parse
import ssl
import sys
import subprocess
import re
from pathlib import Path
from typing import Dict, List, Any, Optional


class GitLabAPI:
    """GitLab API client"""

    def __init__(self, config_path: Optional[Path] = None, insecure: bool = False,
                 allow_prompt: bool = False):
        """Initialize GitLab API client with secure credential loading

        Args:
            config_path: [DEPRECATED] Path to config.json file. Use environment variables or ~/.claude/gitlab_config.json instead.
            insecure: If True, bypass SSL certificate verification (useful for internal GitLab instances with self-signed certs)
            allow_prompt: If True, allow interactive credential prompting if credentials not found
        """
        # Warn if using deprecated config_path parameter
        if config_path is not None:
            print("⚠️  Warning: config_path parameter is deprecated")
            print("   Credentials now loaded from environment variables or")
            print("   user config file (~/.claude/gitlab_config.json)")
            print("   See SKILL.md for more information\n")

        # Import credential loader
        try:
            from credential_loader import CredentialManager
        except ImportError:
            print("Error: credential_loader.py not found")
            print("Please ensure credential_loader.py is in the same directory")
            sys.exit(1)

        # Load credentials securely
        try:
            self._credential_manager = CredentialManager(allow_prompt=allow_prompt)
            creds = self._credential_manager.load_credentials()
            self.host = creds["host"]
            self.token = creds["access_token"]
            self._credential_source = self._credential_manager.get_credential_source()
        except SystemExit:
            sys.exit(1)

        self.insecure = insecure

        # SSL context for internal GitLab instances with self-signed certificates
        self.ssl_context = ssl._create_unverified_context()

    def get_credential_source(self) -> str:
        """Return the source of loaded credentials for debugging

        Returns:
            String describing where credentials were loaded from
            (e.g., "environment_variables", "user_config_file", "legacy_config_file")
        """
        return getattr(self, '_credential_source', 'unknown')

    def create_project(self, name: str, description: Optional[str] = None,
                      visibility: str = "private", namespace_id: Optional[int] = None,
                      initialize_with_readme: bool = False, default_branch: str = "main",
                      wiki_enabled: bool = True, issues_enabled: bool = True,
                      merge_requests_enabled: bool = True, jobs_enabled: bool = True,
                      path: Optional[str] = None) -> Dict:
        """Create a new GitLab project

        Args:
            name: Project name (required)
            description: Project description
            visibility: Visibility level (public/private/internal)
            namespace_id: Namespace ID for the project (defaults to user's personal namespace)
            initialize_with_readme: Create repository with initial README
            default_branch: Default branch name (defaults to "main")
            wiki_enabled: Enable wiki
            issues_enabled: Enable issues
            merge_requests_enabled: Enable merge requests
            jobs_enabled: Enable CI/CD pipelines
            path: Project path (slug, defaults to name)

        Returns:
            Dict with created project information
        """
        data = {
            "name": name,
            "visibility": visibility,
            "initialize_with_readme": initialize_with_readme,
            "wiki_enabled": wiki_enabled,
            "issues_enabled": issues_enabled,
            "merge_requests_enabled": merge_requests_enabled,
            "jobs_enabled": jobs_enabled
        }

        if description:
            data["description"] = description
        if default_branch:
            data["default_branch"] = default_branch
        if path:
            data["path"] = path
        if namespace_id:
            data["namespace_id"] = namespace_id

        return self._make_request("projects", method="POST", data=data)

    def clone_repo(self, repo_url: str, target_dir: Optional[Path] = None) -> Dict:
        """Clone a GitLab repository to the specified directory

        Args:
            repo_url: GitLab repository URL (HTTPS or SSH)
            target_dir: Directory to clone to (defaults to repo name in current directory)

        Returns:
            Dict with success status, clone path, and repo info
        """
        # Parse the repository URL
        parsed = urllib.parse.urlparse(repo_url)
        host = parsed.netloc or parsed.path.split('/')[0]

        # Extract project path from URL
        # Handles both https://host/group/project and git@host:group/project.git
        if "://" in repo_url:
            # HTTPS URL
            path_parts = parsed.path.strip('/').rstrip('.git').split('/')
            project_path = '/'.join(path_parts)
            project_name = path_parts[-1] if path_parts else 'repo'
        else:
            # SSH URL format: git@host:group/project.git
            match = re.match(r'[^@]+@([^:]+):(.+\.git)', repo_url)
            if match:
                host = match.group(1)
                project_path = match.group(2).rstrip('.git')
                project_name = project_path.split('/')[-1]
            else:
                return {"success": False, "error": "Invalid SSH URL format"}

        # Determine target directory
        if target_dir is None:
            target_dir = Path.cwd() / project_name

        # Check if directory already exists
        if target_dir.exists():
            return {"success": False, "error": f"Directory already exists: {target_dir}"}

        # Check if we need to add authentication for HTTPS
        clone_url = repo_url
        if repo_url.startswith('https://') and self.token:
            # Insert token for authentication if needed
            # Format: https://oauth2:TOKEN@host/project.git
            if '@' not in repo_url:
                auth_url = repo_url.replace('https://', f'https://oauth2:{self.token}@')
                clone_url = auth_url

        # Perform git clone
        try:
            result = subprocess.run(
                ['git', 'clone', clone_url, str(target_dir)],
                capture_output=True,
                text=True,
                check=True
            )

            # Get basic repo info after cloning
            repo_info = self._get_clone_info(target_dir)

            return {
                "success": True,
                "clone_path": str(target_dir),
                "project_name": project_name,
                "project_path": project_path,
                "host": host,
                "repo_info": repo_info
            }

        except subprocess.CalledProcessError as e:
            return {
                "success": False,
                "error": f"Git clone failed: {e.stderr}",
                "details": e.stderr
            }
        except FileNotFoundError:
            return {
                "success": False,
                "error": "Git not found. Please install git to clone repositories."
            }

    def _get_clone_info(self, repo_path: Path) -> Dict:
        """Get basic information about a cloned repository"""
        info = {"branch": "unknown", "remote": "unknown", "commit": "unknown"}

        try:
            # Get current branch
            result = subprocess.run(
                ['git', 'branch', '--show-current'],
                cwd=repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            info["branch"] = result.stdout.strip()

            # Get remote URL
            result = subprocess.run(
                ['git', 'remote', 'get-url', 'origin'],
                cwd=repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            info["remote"] = result.stdout.strip()

            # Get latest commit
            result = subprocess.run(
                ['git', 'log', '-1', '--format=%h %s'],
                cwd=repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            info["commit"] = result.stdout.strip()

        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

        return info

    def _make_request_curl(self, endpoint: str, method: str = "GET", data: Optional[Dict] = None) -> Dict:
        """Make an authenticated request to the GitLab API using curl subprocess

        This method is useful as a fallback when Python's SSL handling fails with self-signed certificates.

        Args:
            endpoint: API endpoint (e.g., "projects" or "projects/123/issues")
            method: HTTP method (GET, POST, PUT, DELETE)
            data: Optional data payload for POST/PUT requests

        Returns:
            Dict with parsed JSON response
        """
        url = f"{self.host}/api/v4/{endpoint}"

        # Build curl command
        curl_cmd = ['curl', '-s']
        if self.insecure:
            curl_cmd.append('-k')

        curl_cmd.extend(['--request', method])

        # Add headers
        curl_cmd.extend(['--header', f'PRIVATE-TOKEN: {self.token}'])
        if data:
            curl_cmd.extend(['--header', 'Content-Type: application/json'])
            curl_cmd.extend(['--data', json.dumps(data)])

        curl_cmd.append(url)

        try:
            result = subprocess.run(
                curl_cmd,
                capture_output=True,
                text=True,
                check=True
            )

            if result.stdout:
                return json.loads(result.stdout)
            return {}

        except subprocess.CalledProcessError as e:
            error_msg = e.stderr if e.stderr else e.stdout
            # Provide user-friendly error messages
            if '401' in str(e.returncode) or '401' in error_msg:
                print("❌ Error: Authentication failed (check token)")
            elif '404' in str(e.returncode) or '404' in error_msg:
                print("❌ Error: Resource not found")
            elif '403' in str(e.returncode) or '403' in error_msg:
                print("❌ Error: Access denied (check token permissions)")
            else:
                print(f"API Error: {error_msg}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON response: {e}")
            print(f"Response: {result.stdout[:500] if result.stdout else 'Empty'}")
            sys.exit(1)

    def _make_request(self, endpoint: str, method: str = "GET", data: Optional[Dict] = None, use_curl: bool = False) -> Dict:
        """Make an authenticated request to the GitLab API"""
        # Use curl if requested or if insecure mode is enabled
        if use_curl or self.insecure:
            return self._make_request_curl(endpoint, method, data)

        url = f"{self.host}/api/v4/{endpoint}"
        headers = {"PRIVATE-TOKEN": self.token}

        if data:
            headers["Content-Type"] = "application/json"

        req = urllib.request.Request(url, headers=headers, method=method)

        if data:
            req.data = json.dumps(data).encode("utf-8")

        try:
            with urllib.request.urlopen(req, context=self.ssl_context) as resp:
                body = resp.read().decode("utf-8")
                if body:
                    return json.loads(body)
                return {}
        except urllib.error.HTTPError as e:
            error_body = e.file.read().decode("utf-8")

            # Provide user-friendly error messages
            if e.code == 400 and "Branch already exists" in error_body:
                print("❌ Error: Branch already exists")
                sys.exit(1)
            elif e.code == 400 and "Invalid branch name" in error_body:
                print("❌ Error: Invalid branch name")
                sys.exit(1)
            elif e.code == 404:
                print("❌ Error: Resource not found (check project ID and issue/branch name)")
                sys.exit(1)
            elif e.code == 403:
                print("❌ Error: Access denied (check token permissions)")
                sys.exit(1)
            else:
                print(f"API Error ({e.code}): {error_body}")
                sys.exit(1)
        except urllib.error.URLError as e:
            print(f"Network Error: {e.reason}")
            sys.exit(1)

    def _paginate(self, endpoint: str, params: str = "") -> List[Dict]:
        """Handle paginated API responses"""
        all_items = []
        page = 1
        per_page = 100

        while True:
            url = f"{endpoint}?per_page={per_page}&page={page}"
            if params:
                url += f"&{params}"

            try:
                items = self._make_request(url)
                if not items:
                    break

                if isinstance(items, list):
                    all_items.extend(items)
                    if len(items) < per_page:
                        break
                else:
                    # Single item response
                    all_items.append(items)
                    break

                page += 1
            except Exception as e:
                print(f"Error fetching page {page}: {e}")
                break

        return all_items

    def list_projects(self, search: Optional[str] = None, visibility: Optional[str] = None) -> List[Dict]:
        """List all projects accessible to the user"""
        params = "membership=true&order_by=updated_at&sort=desc"

        if search:
            params += f"&search={urllib.parse.quote(search)}"

        if visibility and visibility in ["public", "private", "internal"]:
            params += f"&visibility={visibility}"

        return self._paginate("projects", params)

    def get_project(self, project_id: str) -> Dict:
        """Get details of a specific project"""
        return self._make_request(f"projects/{urllib.parse.quote(project_id, safe='')}")

    def list_issues(self, project_id: Optional[str] = None, state: str = "opened") -> List[Dict]:
        """List issues from a project or all projects"""
        if project_id:
            endpoint = f"projects/{urllib.parse.quote(project_id, safe='')}/issues"
        else:
            endpoint = "issues"

        return self._paginate(endpoint, f"state={state}")

    def get_issue(self, project_id: str, issue_iid: int) -> Dict:
        """Get details of a specific issue by its IID"""
        return self._make_request(
            f"projects/{urllib.parse.quote(project_id, safe='')}/issues/{issue_iid}"
        )

    def create_issue(self, project_id: str, title: str, description: Optional[str] = None,
                    labels: Optional[str] = None) -> Dict:
        """Create a new issue"""
        data = {"title": title}
        if description:
            data["description"] = description
        if labels:
            data["labels"] = labels

        return self._make_request(
            f"projects/{urllib.parse.quote(project_id, safe='')}/issues",
            method="POST",
            data=data
        )

    def list_merge_requests(self, project_id: Optional[str] = None, state: str = "opened") -> List[Dict]:
        """List merge requests from a project or all projects"""
        if project_id:
            endpoint = f"projects/{urllib.parse.quote(project_id, safe='')}/merge_requests"
        else:
            endpoint = "merge_requests"

        return self._paginate(endpoint, f"state={state}")

    def create_merge_request(self, project_id: str, source_branch: str, target_branch: str,
                           title: str, description: Optional[str] = None) -> Dict:
        """Create a new merge request"""
        data = {
            "source_branch": source_branch,
            "target_branch": target_branch,
            "title": title
        }
        if description:
            data["description"] = description

        return self._make_request(
            f"projects/{urllib.parse.quote(project_id, safe='')}/merge_requests",
            method="POST",
            data=data
        )

    def list_branches(self, project_id: str) -> List[Dict]:
        """List branches in a project"""
        return self._paginate(f"projects/{urllib.parse.quote(project_id, safe='')}/repository/branches")

    def create_branch(self, project_id: str, branch: str, ref: str) -> Dict:
        """Create a new branch from a reference (branch or commit)"""
        data = {
            "branch": branch,
            "ref": ref
        }

        return self._make_request(
            f"projects/{urllib.parse.quote(project_id, safe='')}/repository/branches",
            method="POST",
            data=data
        )

    def list_commits(self, project_id: str, ref_name: Optional[str] = None) -> List[Dict]:
        """List commits in a project"""
        params = ""
        if ref_name:
            params = f"ref_name={urllib.parse.quote(ref_name, safe='')}"

        return self._paginate(f"projects/{urllib.parse.quote(project_id, safe='')}/repository/commits", params)

    def list_pipelines(self, project_id: str) -> List[Dict]:
        """List pipelines in a project"""
        return self._paginate(f"projects/{urllib.parse.quote(project_id, safe='')}/pipelines")


def format_markdown_projects(projects: List[Dict]) -> str:
    """Format projects as Markdown table"""
    if not projects:
        return "## No projects found"

    output = [f"## Found {len(projects)} GitLab Projects\n"]
    output.append("| Name | Visibility | Last Updated | URL |")
    output.append("|------|------------|--------------|-----|")

    for p in projects:
        name = p.get("path_with_namespace", p.get("name", "unknown"))
        visibility = p.get("visibility", "unknown")
        updated = p.get("last_activity_at", "unknown")[:10]
        url = p.get("web_url", "")
        name_display = name[:40] + "..." if len(name) > 40 else name

        output.append(f"| {name_display} | {visibility} | {updated} | [View]({url}) |")

    return "\n".join(output)


def format_markdown_issues(issues: List[Dict]) -> str:
    """Format issues as Markdown table"""
    if not issues:
        return "## No issues found"

    output = [f"## Found {len(issues)} Issues\n"]
    output.append("| ID | Title | State | Author | Updated |")
    output.append("|----|-------|-------|--------|--------|")

    for issue in issues:
        iid = issue.get("iid", "N/A")
        title = issue.get("title", "")[:50]
        state = issue.get("state", "unknown")
        author = issue.get("author", {}).get("username", "unknown")
        updated = issue.get("updated_at", "")[:10]
        url = issue.get("web_url", "")

        output.append(f"| {iid} | [{title}]({url}) | {state} | {author} | {updated} |")

    return "\n".join(output)


def format_markdown_mrs(mrs: List[Dict]) -> str:
    """Format merge requests as Markdown table"""
    if not mrs:
        return "## No merge requests found"

    output = [f"## Found {len(mrs)} Merge Requests\n"]
    output.append("| IID | Title | State | Author | Source → Target |")
    output.append("|-----|-------|-------|--------|----------------|")

    for mr in mrs:
        iid = mr.get("iid", "N/A")
        title = mr.get("title", "")[:40]
        state = mr.get("state", "unknown")
        author = mr.get("author", {}).get("username", "unknown")
        source = mr.get("source_branch", "?")
        target = mr.get("target_branch", "?")
        url = mr.get("web_url", "")

        output.append(f"| {iid} | [{title}]({url}) | {state} | {author} | {source} → {target} |")

    return "\n".join(output)


def format_markdown_branch_created(branch_info: Dict) -> str:
    """Format created branch information as Markdown"""
    branch_name = branch_info.get("name", "unknown")
    commit = branch_info.get("commit", {})
    short_id = commit.get("short_id", "N/A")
    message = commit.get("title", "No message").split("\n")[0][:60]
    author = commit.get("author_name", "unknown")
    date = commit.get("authored_date", "")[:10]
    protected = "🔒 Protected" if branch_info.get("protected", False) else "Not protected"
    web_url = branch_info.get("web_url", "")

    output = [
        "## ✅ Branch Created Successfully\n",
        f"**Branch**: `{branch_name}`",
        f"**Status**: {protected}",
        f"**Commit**: `{short_id}` - {message}",
        f"**Author**: {author}",
        f"**Date**: {date}",
        f"**View**: [Branch in GitLab]({web_url})\n"
    ]

    return "\n".join(output)


def format_markdown_project_created(project: Dict) -> str:
    """Format created project information as Markdown"""
    name = project.get("name", "unknown")
    project_id = project.get("id", "N/A")
    visibility = project.get("visibility", "unknown")
    path_with_namespace = project.get("path_with_namespace", "")
    web_url = project.get("web_url", "")
    http_url = project.get("http_url_to_repo", "")
    ssh_url = project.get("ssh_url_to_repo", "")
    description = project.get("description", "No description")

    output = [
        "## ✅ Repository Created Successfully\n",
        f"**Project**: {name}",
        f"**Project ID**: {project_id}",
        f"**Visibility**: {visibility}",
        f"**Path**: {path_with_namespace}",
        f"**Description**: {description}",
        f"**URL**: [View Project]({web_url})",
        f"**Clone (HTTPS)**: `git clone {http_url}`",
        f"**Clone (SSH)**: `git clone {ssh_url}`\n"
    ]

    return "\n".join(output)


def format_markdown_issue_created(issue: Dict) -> str:
    """Format created issue information as Markdown"""
    title = issue.get("title", "unknown")
    iid = issue.get("iid", "N/A")
    state = issue.get("state", "unknown")
    state_icon = "🟢" if state == "opened" else "🔴" if state == "closed" else "⚪"

    author = issue.get("author", {}).get("name", "Unknown")
    created = issue.get("created_at", "")[:10]

    # Handle multiple assignees
    assignees = issue.get("assignees", [])
    if assignees:
        assignee_names = ", ".join([a.get("name", "Unknown") for a in assignees])
    else:
        assignee_names = "Unassigned"

    # Handle labels
    labels = issue.get("labels", [])
    if labels:
        label_str = " ".join([f"`{l}`" for l in labels])
    else:
        label_str = "None"

    web_url = issue.get("web_url", "")

    output = [
        "## ✅ Issue Created Successfully\n",
        f"**Issue #{iid}**: {title} {state_icon}",
        f"**State**: {state}",
        f"**Author**: {author}",
        f"**Created**: {created}",
        f"**Assignees**: {assignee_names}",
        f"**Labels**: {label_str}",
        f"**Link**: [View in GitLab]({web_url})\n"
    ]

    return "\n".join(output)


def format_markdown_issue_details(issue: Dict) -> str:
    """Format issue details as Markdown"""
    title = issue.get("title", "No title")
    iid = issue.get("iid", "N/A")
    state = issue.get("state", "unknown")
    state_icon = "🟢" if state == "opened" else "🔴" if state == "closed" else "⚪"

    author = issue.get("author", {}).get("name", "Unknown")
    created = issue.get("created_at", "")[:10]

    # Handle multiple assignees
    assignees = issue.get("assignees", [])
    if assignees:
        assignee_names = ", ".join([a.get("name", "Unknown") for a in assignees])
    else:
        assignee_names = "Unassigned"

    # Handle labels
    labels = issue.get("labels", [])
    if labels:
        label_str = " ".join([f"`{l}`" for l in labels])
    else:
        label_str = "None"

    milestone = issue.get("milestone", {}).get("title", "None") if issue.get("milestone") else "None"
    description = issue.get("description", "No description") or "No description"
    web_url = issue.get("web_url", "")

    output = [
        f"# Issue #{iid}: {title} {state_icon}\n",
        f"**State**: {state}",
        f"**Author**: {author}",
        f"**Created**: {created}",
        f"**Assignees**: {assignee_names}",
        f"**Labels**: {label_str}",
        f"**Milestone**: {milestone}",
        f"**Link**: [View in GitLab]({web_url})\n",
        "## Description\n",
        description
    ]

    return "\n".join(output)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="GitLab API tool")
    parser.add_argument("operation", choices=["projects", "issues", "mrs", "branches", "commits", "pipelines", "create-branch", "get-issue", "clone", "create-project", "create-issue"],
                       help="Operation to perform")
    parser.add_argument("--project", help="Project ID or path")
    parser.add_argument("--search", help="Search query")
    parser.add_argument("--state", default="opened", help="Filter by state (opened/closed/merged)")
    parser.add_argument("--format", default="markdown", choices=["markdown", "json"], help="Output format")
    parser.add_argument("--branch", help="Branch name to create")
    parser.add_argument("--branch-ref", help="Reference branch/commit for new branch")
    parser.add_argument("--issue-iid", type=int, help="Issue IID to fetch")
    parser.add_argument("--repo-url", help="Repository URL to clone")
    parser.add_argument("--target-dir", help="Target directory for cloning")
    # Create project arguments
    parser.add_argument("--name", help="Project name (required for create-project)")
    parser.add_argument("--description", help="Project description")
    parser.add_argument("--visibility", default="private", choices=["public", "private", "internal"], help="Project visibility")
    parser.add_argument("--namespace-id", type=int, help="Namespace ID for the project")
    parser.add_argument("--init-readme", action="store_true", help="Initialize with README")
    parser.add_argument("--default-branch", default="main", help="Default branch name")
    parser.add_argument("--path", help="Project path (slug)")
    # Create issue arguments
    parser.add_argument("--title", help="Issue title (required for create-issue)")
    parser.add_argument("--labels", help="Comma-separated issue labels")
    # SSL options
    parser.add_argument("--insecure", action="store_true", help="Bypass SSL certificate verification (use -k flag with curl)")
    parser.add_argument("--allow-prompt", action="store_true",
                       help="Allow interactive credential prompting if not found")

    args = parser.parse_args()

    api = GitLabAPI(insecure=args.insecure, allow_prompt=args.allow_prompt)

    if args.operation == "clone":
        if not args.repo_url:
            print("Error: --repo-url is required for cloning")
            sys.exit(1)

        target_dir = Path(args.target_dir) if args.target_dir else None
        result = api.clone_repo(args.repo_url, target_dir)

        if result["success"]:
            info = result["repo_info"]
            output = [
                "## ✅ Repository Cloned Successfully\n",
                f"**Clone Path**: `{result['clone_path']}`",
                f"**Project**: {result['project_name']}",
                f"**Project Path**: {result['project_path']}",
                f"**Host**: {result['host']}",
                f"**Branch**: {info['branch']}",
                f"**Latest Commit**: {info['commit']}",
                f"**Remote**: {info['remote']}\n"
            ]
            print("\n".join(output))
        else:
            print(f"❌ Clone failed: {result['error']}")
            sys.exit(1)

    elif args.operation == "create-project":
        if not args.name:
            print("Error: --name is required for creating a project")
            sys.exit(1)

        result = api.create_project(
            name=args.name,
            description=args.description,
            visibility=args.visibility,
            namespace_id=args.namespace_id,
            initialize_with_readme=args.init_readme,
            default_branch=args.default_branch,
            path=args.path
        )

        if args.format == "markdown":
            print(format_markdown_project_created(result))
        else:
            print(json.dumps(result, indent=2))

    elif args.operation == "create-issue":
        if not args.project:
            print("Error: --project is required for creating issues")
            sys.exit(1)
        if not args.title:
            print("Error: --title is required for creating issues")
            sys.exit(1)

        result = api.create_issue(args.project, args.title, description=args.description, labels=args.labels)
        if args.format == "markdown":
            print(format_markdown_issue_created(result))
        else:
            print(json.dumps(result, indent=2))

    elif args.operation == "projects":
        result = api.list_projects(search=args.search)
        if args.format == "markdown":
            print(format_markdown_projects(result))
        else:
            print(json.dumps(result, indent=2))

    elif args.operation == "issues":
        result = api.list_issues(project_id=args.project, state=args.state)
        if args.format == "markdown":
            print(format_markdown_issues(result))
        else:
            print(json.dumps(result, indent=2))

    elif args.operation == "mrs":
        result = api.list_merge_requests(project_id=args.project, state=args.state)
        if args.format == "markdown":
            print(format_markdown_mrs(result))
        else:
            print(json.dumps(result, indent=2))

    elif args.operation == "branches":
        if not args.project:
            print("Error: --project is required for listing branches")
            sys.exit(1)
        result = api.list_branches(args.project)
        print(json.dumps(result, indent=2))

    elif args.operation == "commits":
        if not args.project:
            print("Error: --project is required for listing commits")
            sys.exit(1)
        result = api.list_commits(args.project)
        print(json.dumps(result, indent=2))

    elif args.operation == "pipelines":
        if not args.project:
            print("Error: --project is required for listing pipelines")
            sys.exit(1)
        result = api.list_pipelines(args.project)
        print(json.dumps(result, indent=2))

    elif args.operation == "create-branch":
        if not args.project:
            print("Error: --project is required for creating branches")
            sys.exit(1)
        if not args.branch:
            print("Error: --branch is required")
            sys.exit(1)
        if not args.branch_ref:
            print("Error: --branch-ref is required")
            sys.exit(1)

        result = api.create_branch(args.project, args.branch, args.branch_ref)
        if args.format == "markdown":
            print(format_markdown_branch_created(result))
        else:
            print(json.dumps(result, indent=2))

    elif args.operation == "get-issue":
        if not args.project:
            print("Error: --project is required for getting issue details")
            sys.exit(1)
        if not args.issue_iid:
            print("Error: --issue-iid is required")
            sys.exit(1)

        result = api.get_issue(args.project, args.issue_iid)
        if args.format == "markdown":
            print(format_markdown_issue_details(result))
        else:
            print(json.dumps(result, indent=2))
