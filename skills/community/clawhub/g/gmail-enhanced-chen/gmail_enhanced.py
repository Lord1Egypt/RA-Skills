"""
Gmail Enhanced - Advanced Gmail integration with automation features
"""
import os
import re
import json
import base64
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import Dict, List, Optional, Union
from datetime import datetime, timedelta

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class GmailClient:
    """Enhanced Gmail client with advanced features"""
    
    SCOPES = [
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/gmail.send',
        'https://www.googleapis.com/auth/gmail.labels',
        'https://www.googleapis.com/auth/gmail.modify',
    ]
    
    def __init__(
        self,
        credentials_path: str = None,
        token_path: str = None
    ):
        self.credentials_path = credentials_path or os.getenv(
            "GMAIL_CREDENTIALS_PATH",
            "~/.credentials/gmail-credentials.json"
        )
        self.token_path = token_path or os.getenv(
            "GMAIL_TOKEN_PATH",
            "~/.credentials/gmail-token.json"
        )
        
        # Expand paths
        self.credentials_path = os.path.expanduser(self.credentials_path)
        self.token_path = os.path.expanduser(self.token_path)
        
        self._service = None
        self._labels_cache = None
    
    def _get_service(self):
        """Build Gmail service"""
        if self._service:
            return self._service
        
        creds = None
        
        # Load token
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)
        
        # Check if valid
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # Need to authenticate
                if not os.path.exists(self.credentials_path):
                    raise FileNotFoundError(
                        f"Credentials not found at {self.credentials_path}. "
                        "Download from Google Cloud Console."
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # Save token
            Path(self.token_path).parent.mkdir(parents=True, exist_ok=True)
            with open(self.token_path, 'w') as f:
                f.write(creds.to_json())
        
        self._service = build('gmail', 'v1', credentials=creds)
        return self._service
    
    # ==================== Core Email Operations ====================
    
    def send(
        self,
        to: str,
        subject: str,
        body: str,
        attachments: List[str] = None,
        cc: str = None,
        bcc: str = None,
        html: bool = False,
        from_name: str = None
    ) -> Dict:
        """Send email"""
        service = self._get_service()
        
        msg = MIMEMultipart('mixed')
        msg['To'] = to
        msg['Subject'] = subject
        
        if cc:
            msg['Cc'] = cc
        if bcc:
            msg['Bcc'] = bcc
        
        if from_name:
            msg['From'] = f"{from_name} <me>"
        else:
            msg['From'] = 'me'
        
        # Body
        if html:
            msg.attach(MIMEText(body, 'html'))
        else:
            msg.attach(MIMEText(body, 'plain'))
        
        # Attachments
        for file_path in attachments or []:
            self._add_attachment(msg, file_path)
        
        # Encode and send
        encoded = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        
        result = service.users().messages().send(
            userId='me',
            body={'raw': encoded}
        ).execute()
        
        return result
    
    def _add_attachment(self, msg, file_path: str):
        """Add attachment to message"""
        filename = os.path.basename(file_path)
        
        with open(file_path, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
        
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {filename}'
        )
        msg.attach(part)
    
    def search(
        self,
        query: str = "",
        max_results: int = 10,
        label: str = None,
        after: str = None,
        before: str = None,
        has_attachments: bool = False
    ) -> List[Dict]:
        """Search emails"""
        service = self._get_service()
        
        # Build query
        parts = [query]
        
        if label:
            parts.append(f"label:{label}")
        if after:
            parts.append(f"after:{after}")
        if before:
            parts.append(f"before:{before}")
        if has_attachments:
            parts.append("has:attachment")
        
        full_query = " ".join(parts)
        
        results = service.users().messages().list(
            userId='me',
            q=full_query,
            maxResults=max_results
        ).execute()
        
        messages = results.get('messages', [])
        return [self.get_message(m['id']) for m in messages]
    
    def search_or(self, queries: List[str], max_results: int = 10) -> List[Dict]:
        """Search with OR logic"""
        all_results = {}
        
        for query in queries:
            results = self.search(query, max_results)
            for msg in results:
                all_results[msg['id']] = msg
        
        return list(all_results.values())
    
    def get_message(
        self,
        msg_id: str,
        format: str = "full"
    ) -> Dict:
        """Get message details"""
        service = self._get_service()
        
        msg = service.users().messages().get(
            userId='me',
            id=msg_id,
            format=format
        ).execute()
        
        return msg
    
    def get_message_simple(self, msg_id: str) -> Dict:
        """Get message in simple format"""
        msg = self.get_message(msg_id, format="metadata")
        
        # Parse headers
        headers = {h['name']: h['value'] for h in msg.get('payload', {}).get('headers', [])}
        
        return {
            'id': msg['id'],
            'threadId': msg['threadId'],
            'subject': headers.get('Subject', ''),
            'from': headers.get('From', ''),
            'to': headers.get('To', ''),
            'date': headers.get('Date', ''),
            'snippet': msg.get('snippet', ''),
            'labelIds': msg.get('labelIds', []),
            'internalDate': msg.get('internalDate')
        }
    
    def delete_message(self, msg_id: str) -> Dict:
        """Move message to trash"""
        service = self._get_service()
        return service.users().messages().trash(
            userId='me',
            id=msg_id
        ).execute()
    
    def archive_message(self, msg_id: str) -> Dict:
        """Archive message (remove from INBOX)"""
        service = self._get_service()
        
        # Remove INBOX label
        return service.users().messages().modify(
            userId='me',
            id=msg_id,
            body={'removeLabelIds': ['INBOX']}
        ).execute()
    
    def add_labels(self, label_names: List[str], msg_ids: List[str]) -> Dict:
        """Add labels to messages"""
        service = self._get_service()
        
        # Get label IDs
        labels = self.get_labels()
        label_ids = []
        
        for name in label_names:
            for label in labels:
                if label['name'] == name:
                    label_ids.append(label['id'])
                    break
        
        if not label_ids:
            raise ValueError(f"Labels not found: {label_names}")
        
        result = {'modified': 0}
        for msg_id in msg_ids:
            service.users().messages().modify(
                userId='me',
                id=msg_id,
                body={'addLabelIds': label_ids}
            ).execute()
            result['modified'] += 1
        
        return result
    
    # ==================== Label Management ====================
    
    def get_labels(self) -> List[Dict]:
        """Get all labels"""
        if self._labels_cache:
            return self._labels_cache
        
        service = self._get_service()
        
        results = service.users().labels().list(userId='me').execute()
        self._labels_cache = results.get('labels', [])
        return self._labels_cache
    
    def create_label(
        self,
        name: str,
        label_list_visibility: str = "labelShow",
        message_list_visibility: str = "show",
        color: str = None
    ) -> Dict:
        """Create label"""
        service = self._get_service()
        
        body = {
            'name': name,
            'labelListVisibility': label_list_visibility,
            'messageListVisibility': message_list_visibility
        }
        
        if color:
            # Parse hex color
            if color.startswith('#'):
                color = color[1:]
            # Gmail uses specific color indices
            # Map to available colors
            colors = {
                "#4A90E2": {"backgroundColor": "#8AB5F8", "textColor": "#0C3576"},
                "#E25C5C": {"backgroundColor": "#F5A5A5", "textColor": "#751818"},
                "#5CB85C": {"backgroundColor": "#A5D6A7", "textColor": "#1B5E20"},
                "#F0AD4E": {"backgroundColor": "#FFE0B2", "textColor": "#E65100"},
            }
            body['color'] = colors.get(color, colors["#4A90E2"])
        
        result = service.users().labels().create(
            userId='me',
            body=body
        ).execute()
        
        # Clear cache
        self._labels_cache = None
        return result
    
    def rename_label(self, old_name: str, new_name: str) -> Dict:
        """Rename label"""
        labels = self.get_labels()
        
        label_id = None
        for label in labels:
            if label['name'] == old_name:
                label_id = label['id']
                break
        
        if not label_id:
            raise ValueError(f"Label not found: {old_name}")
        
        service = self._get_service()
        result = service.users().labels().patch(
            userId='me',
            id=label_id,
            body={'name': new_name}
        ).execute()
        
        self._labels_cache = None
        return result
    
    def delete_label(self, name: str) -> Dict:
        """Delete label"""
        labels = self.get_labels()
        
        label_id = None
        for label in labels:
            if label['name'] == name:
                label_id = label['id']
                break
        
        if not label_id:
            raise ValueError(f"Label not found: {name}")
        
        service = self._get_service()
        result = service.users().labels().delete(
            userId='me',
            id=label_id
        ).execute()
        
        self._labels_cache = None
        return result
    
    def get_label_stats(self, label_name: str) -> Dict:
        """Get label statistics"""
        labels = self.get_labels()
        
        label_id = None
        for label in labels:
            if label['name'] == label_name:
                label_id = label['id']
                break
        
        if not label_id:
            raise ValueError(f"Label not found: {label_name}")
        
        service = self._get_service()
        
        # Get messages with this label
        results = service.users().messages().list(
            userId='me',
            q=f"label:{label_name}",
            maxResults=1
        ).execute()
        
        total = results.get('resultSizeEstimate', 0)
        
        # Get unread count
        results = service.users().messages().list(
            userId='me',
            q=f"label:{label_name} is:unread",
            maxResults=1
        ).execute()
        
        unread = results.get('resultSizeEstimate', 0)
        
        return {
            'name': label_name,
            'total': total,
            'unread': unread,
            'read': total - unread
        }
    
    # ==================== Attachment Handling ====================
    
    def get_attachment_info(self, msg_id: str) -> List[Dict]:
        """Get attachment info from message"""
        msg = self.get_message(msg_id, format="full")
        
        attachments = []
        
        def find_attachments(part):
            if part.get('filename'):
                attachments.append({
                    'filename': part['filename'],
                    'mimeType': part['mimeType'],
                    'size': part.get('body', {}).get('size', 0),
                    'attachmentId': part.get('body', {}).get('attachmentId')
                })
            
            if 'parts' in part:
                for p in part['parts']:
                    find_attachments(p)
        
        find_attachments(msg['payload'])
        return attachments
    
    def download_attachment(
        self,
        msg_id: str,
        attachment_id: str,
        save_path: str
    ) -> Dict:
        """Download attachment"""
        service = self._get_service()
        
        attachment = service.users().messages().attachments().get(
            userId='me',
            messageId=msg_id,
            id=attachment_id
        ).execute()
        
        # Decode
        data = base64.urlsafe_b64decode(attachment['data'])
        
        # Save
        with open(save_path, 'wb') as f:
            f.write(data)
        
        return {'saved_to': save_path, 'size': len(data)}
    
    def search_attachments(
        self,
        query: str,
        save_dir: str = "./downloads"
    ) -> List[Dict]:
        """Search and download attachments"""
        os.makedirs(save_dir, exist_ok=True)
        
        messages = self.search(query, max_results=20, has_attachments=True)
        
        downloaded = []
        
        for msg in messages:
            attachments = self.get_attachment_info(msg['id'])
            
            for att in attachments:
                if att['attachmentId']:
                    save_path = os.path.join(save_dir, att['filename'])
                    self.download_attachment(
                        msg['id'],
                        att['attachmentId'],
                        save_path
                    )
                    downloaded.append({
                        'message_id': msg['id'],
                        'filename': att['filename'],
                        'saved_to': save_path
                    })
        
        return downloaded
    
    # ==================== Automation ====================
    
    def add_rule(
        self,
        name: str,
        query: str,
        add_labels: List[str] = None,
        mark_read: bool = False,
        archive: bool = False,
        auto_reply: str = None
    ):
        """Add processing rule"""
        rules_path = os.path.expanduser("~/.gmail_rules.json")
        
        rules = []
        if os.path.exists(rules_path):
            with open(rules_path, 'r') as f:
                rules = json.load(f)
        
        rules.append({
            'name': name,
            'query': query,
            'add_labels': add_labels or [],
            'mark_read': mark_read,
            'archive': archive,
            'auto_reply': auto_reply
        })
        
        with open(rules_path, 'w') as f:
            json.dump(rules, f, indent=2)
    
    def process_rules(self) -> Dict:
        """Process all rules"""
        rules_path = os.path.expanduser("~/.gmail_rules.json")
        
        if not os.path.exists(rules_path):
            return {'processed': 0, 'actions': 0}
        
        with open(rules_path, 'r') as f:
            rules = json.load(f)
        
        result = {'processed': 0, 'actions': 0}
        
        for rule in rules:
            messages = self.search(rule['query'], max_results=50)
            
            for msg in messages:
                # Add labels
                if rule.get('add_labels'):
                    self.add_labels(rule['add_labels'], [msg['id']])
                    result['actions'] += 1
                
                # Mark read
                if rule.get('mark_read'):
                    service = self._get_service()
                    service.users().messages().modify(
                        userId='me',
                        id=msg['id'],
                        body={'removeLabelIds': ['UNREAD']}
                    ).execute()
                    result['actions'] += 1
                
                # Archive
                if rule.get('archive'):
                    self.archive_message(msg['id'])
                    result['actions'] += 1
                
                # Auto reply
                if rule.get('auto_reply'):
                    headers = {h['name']: h['value'] for h in msg.get('payload', {}).get('headers', [])}
                    self.send(
                        to=headers.get('From', ''),
                        subject=f"Re: {headers.get('Subject', '')}",
                        body=rule['auto_reply']
                    )
                    result['actions'] += 1
            
            result['processed'] += 1
        
        return result
    
    # ==================== Parsing ====================
    
    def parse_email(self, msg_id: str) -> Dict:
        """Extract structured data from email"""
        msg = self.get_message(msg_id, format="full")
        
        # Get headers
        headers = {h['name']: h['value'] for h in msg['payload']['headers']}
        
        # Get body
        body = self._get_body(msg['payload'])
        
        # Extract email addresses
        emails = re.findall(r'[\w\.-]+@[\w\.-]+', body)
        
        # Extract URLs
        urls = re.findall(r'https?://[^\s]+', body)
        
        return {
            'subject': headers.get('Subject', ''),
            'from': headers.get('From', ''),
            'to': headers.get('To', ''),
            'date': headers.get('Date', ''),
            'body': body[:1000],  # First 1000 chars
            'emails_found': list(set(emails)),
            'urls_found': urls[:10],
            'has_attachments': bool(msg.get('payload', {}).get('filename'))
        }
    
    def _get_body(self, payload: Dict) -> str:
        """Extract body from payload"""
        if 'body' in payload and payload['body'].get('data'):
            return base64.urlsafe_b64decode(
                payload['body']['data']
            ).decode('utf-8', errors='ignore')
        
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    return base64.urlsafe_b64decode(
                        part['body']['data']
                    ).decode('utf-8', errors='ignore')
                elif part['mimeType'] == 'text/html':
                    return base64.urlsafe_b64decode(
                        part['body']['data']
                    ).decode('utf-8', errors='ignore')
        
        return ""
    
    def extract_invoice(self, msg_id: str) -> Dict:
        """Extract invoice data"""
        data = self.parse_email(msg_id)
        
        # Simple regex patterns for common invoice fields
        invoice_num = re.search(r'(?:Invoice|Bill|订单)[:\s#]*([A-Z0-9-]+)', data['body'], re.I)
        amount = re.search(r'[$¥€]?\s*(\d+\.?\d*)', data['body'])
        date = re.search(r'(\d{4}[-/]\d{2}[-/]\d{2})', data['body'])
        
        return {
            'invoice_number': invoice_num.group(1) if invoice_num else None,
            'amount': amount.group(1) if amount else None,
            'date': date.group(1) if date else None,
            **data
        }
    
    def extract_contacts(self, msg_id: str) -> List[Dict]:
        """Extract contacts from email"""
        msg = self.get_message(msg_id)
        headers = {h['name']: h['value'] for h in msg['payload']['headers']}
        
        contacts = []
        
        # From
        from_match = re.match(r'(.+?)\s<(.+?)>', headers.get('From', ''))
        if from_match:
            contacts.append({
                'name': from_match.group(1),
                'email': from_match.group(2),
                'role': 'from'
            })
        
        # All mentioned emails
        body = self._get_body(msg['payload'])
        emails = re.findall(r'[\w\.-]+@[\w\.-]+', body)
        
        for email in set(emails):
            if email not in [c.get('email') for c in contacts]:
                contacts.append({
                    'email': email,
                    'role': 'mentioned'
                })
        
        return contacts


def main():
    """Demo usage"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python gmail_enhanced.py <command> [args...]")
        sys.exit(1)
    
    client = GmailClient()
    cmd = sys.argv[1]
    
    if cmd == "search" and len(sys.argv) >= 3:
        results = client.search(sys.argv[2])
        for msg in results:
            print(f"- {msg.get('subject', 'No subject')}")
    elif cmd == "labels":
        labels = client.get_labels()
        for label in labels:
            print(f"- {label['name']}")
    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
