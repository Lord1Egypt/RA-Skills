
import os
import subprocess
import signal
import time
import sys

def run_isolated_child():
    return subprocess.Popen([sys.executable, "-c", "import time; time.sleep(10)"], start_new_session=True)

proc = None
try:
    proc = run_isolated_child()
    print(f"CHILD_PID:{proc.pid}")
    sys.stdout.flush()
    raise KeyboardInterrupt
finally:
    if proc is not None and proc.poll() is None:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        except OSError:
            pass
