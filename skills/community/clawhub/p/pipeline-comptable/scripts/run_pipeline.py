import sys, runpy
sys.argv = [
    "pipeline.py",
    "--inbox", "/root/.openclaw/workspace/inbox-mails",
    "--clients-root", "/root/.openclaw/workspace/clients",
]
runpy.run_path("pipeline.py", run_name="__main__")
