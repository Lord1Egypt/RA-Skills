def run(issue_title: str, issue_description: str):
    """
    Generate a simple fix plan for a GitHub issue
    """

    plan = f"""
Issue: {issue_title}

Fix Plan:

1. Read and understand the issue description.
2. Identify the component related to the bug.
3. Reproduce the problem locally.
4. Locate the problematic code.
5. Implement a fix.
6. Add tests if necessary.
7. Submit pull request.

Issue Details:
{issue_description}
"""

    return {
        "fix_plan": plan
    }