import subprocess
import logging
import os
import sys

class GitCheckoutError(Exception):
    pass

class GitBoundaryError(Exception):
    pass

def check_git_boundary(workdir):
    abs_workdir = os.path.abspath(workdir)
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=abs_workdir,
            capture_output=True,
            text=True,
            check=True
        )
        git_toplevel = os.path.abspath(result.stdout.strip())
        if git_toplevel != abs_workdir:
            error_msg = f"[FATAL] Git boundary violation: '{abs_workdir}' is not the root of a git repository (found '{git_toplevel}')."
            logging.error(error_msg)
            print(error_msg, file=sys.stderr)
            raise GitBoundaryError(error_msg)
    except subprocess.CalledProcessError as e:
        error_msg = f"[FATAL] Git boundary violation: '{abs_workdir}' does not appear to be inside a git repository."
        logging.error(error_msg)
        print(error_msg, file=sys.stderr)
        raise GitBoundaryError(error_msg)

def safe_git_checkout(branch_name, create=False):
    """
    Safely executes git checkout operations.
    Raises GitCheckoutError on failure without running destructive commands.
    """
    cmd = ["git", "checkout"]
    if create:
        cmd.append("-b")
    cmd.append(branch_name)

    try:
        # Wrap the subprocess call for git checkout in a try...except block
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return result
    except subprocess.CalledProcessError as e:
        error_msg = f"Git checkout failed for branch '{branch_name}'. Error: {e.stderr}"
        logging.error(error_msg)
        raise GitCheckoutError(error_msg) from e

def check_git_boundary(workdir):
    import os
    import sys
    import subprocess
    if not os.path.exists(os.path.join(workdir, ".git")):
        print(f"[FATAL] Git boundary violation: workdir '{workdir}' must contain a .git directory.")
        sys.exit(1)
    
    toplevel = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, cwd=workdir).stdout.strip()
    if os.path.abspath(toplevel) != os.path.abspath(workdir):
        print(f"[FATAL] Git boundary violation: workdir '{workdir}' is not the root of the git repository.")
        sys.exit(1)
