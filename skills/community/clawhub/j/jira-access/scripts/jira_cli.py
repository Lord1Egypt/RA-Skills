#!/usr/bin/env python3
"""Simple Jira CLI wrapper used by the jira-access skill.

It expects three environment variables to be set:
  JIRA_DOMAIN   – e.g. "omeshkshatriya.atlassian.net"
  JIRA_EMAIL    – the account email
  JIRA_API_TOKEN – a personal API token (generated in Atlassian account)

Usage:
  jira list "JQL query"
  jira create <ISSUE_TYPE> "SUMMARY" "DESCRIPTION"
  jira transition <ISSUE-KEY> <STATUS>
  jira comment <ISSUE-KEY> "COMMENT TEXT"

The script prints JSON results to stdout for the assistant to consume.
"""
import os, sys, json, argparse, requests

BASE_URL = f"https://{os.getenv('JIRA_DOMAIN')}/rest/api/3"
AUTH = (os.getenv('JIRA_EMAIL'), os.getenv('JIRA_API_TOKEN'))

if not all([os.getenv('JIRA_DOMAIN'), os.getenv('JIRA_EMAIL'), os.getenv('JIRA_API_TOKEN')]):
    sys.stderr.write('Missing required JIRA environment variables.\n')
    sys.exit(1)

def jira_request(method, path, **kwargs):
    url = f"{BASE_URL}{path}"
    resp = requests.request(method, url, auth=AUTH, headers={'Accept': 'application/json'}, **kwargs)
    resp.raise_for_status()
    return resp.json()

def cmd_list(args):
    jql = args.jql
    data = jira_request('GET', f'/search?jql={requests.utils.quote(jql)}')
    print(json.dumps(data, indent=2))

def cmd_create(args):
    issue_type, summary, description = args.type, args.summary, args.description
    payload = {
        "fields": {
            "project": {"key": os.getenv('JIRA_PROJECT_KEY', 'DEFAULT')},
            "summary": summary,
            "description": description,
            "issuetype": {"name": issue_type}
        }
    }
    data = jira_request('POST', '/issue', json=payload)
    print(json.dumps(data, indent=2))

def cmd_transition(args):
    issue_key, status = args.key, args.status
    # Find transition id for the desired status
    transitions = jira_request('GET', f'/issue/{issue_key}/transitions')
    tid = None
    for t in transitions.get('transitions', []):
        if t.get('name').lower() == status.lower():
            tid = t['id']
            break
    if not tid:
        sys.stderr.write(f'No transition named "{status}" for {issue_key}\n')
        sys.exit(1)
    jira_request('POST', f'/issue/{issue_key}/transitions', json={"transition": {"id": tid}})
    print(json.dumps({"issue": issue_key, "newStatus": status}, indent=2))

def cmd_comment(args):
    issue_key, comment = args.key, args.comment
    payload = {"body": comment}
    data = jira_request('POST', f'/issue/{issue_key}/comment', json=payload)
    print(json.dumps(data, indent=2))

def main():
    parser = argparse.ArgumentParser(prog='jira')
    sub = parser.add_subparsers(dest='command')
    # list
    p_list = sub.add_parser('list', help='List issues with JQL')
    p_list.add_argument('jql')
    p_list.set_defaults(func=cmd_list)
    # create
    p_create = sub.add_parser('create', help='Create an issue')
    p_create.add_argument('type')
    p_create.add_argument('summary')
    p_create.add_argument('description')
    p_create.set_defaults(func=cmd_create)
    # transition
    p_trans = sub.add_parser('transition', help='Transition issue')
    p_trans.add_argument('key')
    p_trans.add_argument('status')
    p_trans.set_defaults(func=cmd_transition)
    # comment
    p_comm = sub.add_parser('comment', help='Add comment')
    p_comm.add_argument('key')
    p_comm.add_argument('comment')
    p_comm.set_defaults(func=cmd_comment)
    args = parser.parse_args()
    if not hasattr(args, 'func'):
        parser.print_help()
        sys.exit(1)
    args.func(args)

if __name__ == '__main__':
    main()
