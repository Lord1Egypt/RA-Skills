import subprocess
import sys

def get_git_logs():
    try:
        # Get current user
        try:
            user_name = subprocess.check_output(['git', 'config', 'user.name']).decode('utf-8').strip()
        except subprocess.CalledProcessError:
            # Fallback if git config is not set or not in a git repo
            return "Error: Not a git repository or git user.name not set."

        # Get logs from the last 7 days
        # --since="1 week ago" is usually good enough
        cmd = [
            'git', 'log',
            f'--author={user_name}',
            '--since=1.week.ago',
            '--pretty=format:%h|%ad|%s',
            '--date=short',
            '--no-merges'
        ]
        
        logs = subprocess.check_output(cmd).decode('utf-8')
        if not logs:
            return "No commits found in the last week."
        return logs
    except Exception as e:
        return f"Error executing git log: {str(e)}"

if __name__ == "__main__":
    print(get_git_logs())
