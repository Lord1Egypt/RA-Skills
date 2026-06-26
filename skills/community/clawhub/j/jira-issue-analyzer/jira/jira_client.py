"""Jira API client with Bearer token authentication."""

import requests
from typing import Dict, List, Optional, Any
from config import config


class JiraClient:
    """Jira API client using Bearer token authentication."""

    def __init__(self):
        self.base_url = config.jira_base_url
        self.api_base = config.api_base
        self.session = requests.Session()
        self.session.trust_env = False  # Disable environment proxy settings
        self.session.headers.update({
            'Authorization': f'Bearer {config.jira_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        })

    def test_connection(self) -> bool:
        """Test the connection to Jira server."""
        try:
            response = self.session.get(f"{self.api_base}/myself")
            if response.status_code == 200:
                user = response.json()
                print(f"Connected as: {user.get('displayName', 'Unknown')}")
                return True
            else:
                print(f"Connection failed: {response.status_code} - {response.text}")
                return False
        except requests.RequestException as e:
            print(f"Connection error: {e}")
            return False

    def search_issues(
        self,
        jql: str,
        fields: Optional[List[str]] = None,
        max_results: int = 100,
        start_at: int = 0
    ) -> Dict[str, Any]:
        params = {
            'jql': jql,
            'maxResults': max_results,
            'startAt': start_at,
        }
        if fields:
            params['fields'] = ','.join(fields)

        response = self.session.get(
            f"{self.api_base}/search",
            params=params
        )
        response.raise_for_status()
        return response.json()

    def get_issues_by_assignee(
        self,
        assignee: str,
        max_results: int = 100
    ) -> List[Dict[str, Any]]:
        jql = f'assignee = "{assignee}"'
        fields = [
            'summary', 'status', 'priority', 'assignee',
            'created', 'updated', 'issuetype', 'project'
        ]

        result = self.search_issues(jql=jql, fields=fields, max_results=max_results)

        issues = []
        for issue in result.get('issues', []):
            fields = issue.get('fields', {})
            issues.append({
                'key': issue.get('key'),
                'summary': fields.get('summary'),
                'status': fields.get('status', {}).get('name'),
                'priority': fields.get('priority', {}).get('name', 'None'),
                'assignee': fields.get('assignee', {}).get('displayName', 'Unassigned'),
                'assignee_email': fields.get('assignee', {}).get('emailAddress', ''),
                'created': fields.get('created'),
                'updated': fields.get('updated'),
                'issuetype': fields.get('issuetype', {}).get('name', ''),
                'project': fields.get('project', {}).get('name', ''),
                'url': f"{self.base_url}/browse/{issue.get('key')}",
            })

        return issues

    def get_issue(self, issue_key: str) -> Dict[str, Any]:
        response = self.session.get(
            f"{self.api_base}/issue/{issue_key}",
            params={'expand': 'attachments,comments'}
        )
        response.raise_for_status()
        return response.json()

    def get_issue_info(self, issue_key: str) -> Dict[str, Any]:
        issue = self.get_issue(issue_key)
        fields = issue.get('fields', {})

        return {
            'key': issue.get('key'),
            'id': issue.get('id'),
            'summary': fields.get('summary'),
            'description': fields.get('description'),
            'status': fields.get('status', {}).get('name'),
            'priority': fields.get('priority', {}).get('name', 'None'),
            'issuetype': fields.get('issuetype', {}).get('name', ''),
            'project': fields.get('project', {}).get('name', ''),
            'project_key': fields.get('project', {}).get('key', ''),
            'assignee': fields.get('assignee', {}).get('displayName', 'Unassigned'),
            'assignee_email': fields.get('assignee', {}).get('emailAddress', ''),
            'reporter': fields.get('reporter', {}).get('displayName', ''),
            'reporter_email': fields.get('reporter', {}).get('emailAddress', ''),
            'created': fields.get('created'),
            'updated': fields.get('updated'),
            'resolutiondate': fields.get('resolutiondate'),
            'duedate': fields.get('duedate'),
            'components': [c.get('name') for c in fields.get('components', [])],
            'labels': fields.get('labels', []),
            'url': f"{self.base_url}/browse/{issue.get('key')}",
            'attachments': [
                {
                    'id': a.get('id'),
                    'filename': a.get('filename'),
                    'size': a.get('size'),
                    'mimeType': a.get('mimeType'),
                    'content': a.get('content'),
                    'author': a.get('author', {}).get('displayName', ''),
                    'created': a.get('created'),
                }
                for a in fields.get('attachment', [])
            ],
            'comments': [
                {
                    'id': c.get('id'),
                    'author': c.get('author', {}).get('displayName', ''),
                    'body': c.get('body'),
                    'created': c.get('created'),
                    'updated': c.get('updated'),
                }
                for c in fields.get('comment', {}).get('comments', [])
            ],
            'raw_fields': fields,
        }

    def download_attachment(self, content_url: str, filename: str, dest_dir: str = '.') -> str:
        import os
        os.makedirs(dest_dir, exist_ok=True)
        filepath = os.path.join(dest_dir, filename)

        response = self.session.get(content_url, stream=True)
        response.raise_for_status()

        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return filepath

    def download_issue_attachments(self, issue_key: str, dest_dir: str = None) -> List[str]:
        import os
        if dest_dir is None:
            dest_dir = os.path.join('attachments', issue_key)

        issue = self.get_issue_info(issue_key)
        downloaded = []

        for att in issue.get('attachments', []):
            print(f"Downloading: {att['filename']}...")
            filepath = self.download_attachment(
                att['content'],
                att['filename'],
                dest_dir
            )
            downloaded.append(filepath)
            print(f"  Saved: {filepath} ({os.path.getsize(filepath):,} bytes)")

        return downloaded
