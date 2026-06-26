import argparse
import os
import sys
import re

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--issue-id', required=True)
    parser.add_argument('--status', required=True)
    args = parser.parse_args()

    # Determine workspace root (parent of scripts/)
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    if os.environ.get('SDLC_TEST_MODE') == 'true':
        log_dir = "tests"
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, 'tool_calls.log')
        with open(log_file, 'a') as f:
            f.write(str({'tool': 'update_issue', 'args': {'issue_id': args.issue_id, 'status': args.status}}) + '\n')
        print('{"status": "mock_success", "action": "update_issue"}')
        sys.exit(0)

    # Production Mode
    issue_file = os.path.join(workspace_root, '.issues', f'{args.issue_id}.md')
    if not os.path.exists(issue_file):
        print(f"Error: Issue file {issue_file} does not exist.")
        sys.exit(1)

    with open(issue_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = re.sub(r'^status:.*$', f'status: {args.status}', content, flags=re.MULTILINE)
    
    with open(issue_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Success: Updated {args.issue_id} to {args.status}")

if __name__ == '__main__':
    main()