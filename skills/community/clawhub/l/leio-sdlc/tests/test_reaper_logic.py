import os
import subprocess
import signal
import time
import sys

def test_reaper():
    test_script = os.path.join(os.getcwd(), 'tests', 'reaper_dummy.py')
    with open(test_script, 'w') as f:
        f.write("""
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
""")

    proc = subprocess.Popen([sys.executable, test_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = proc.communicate()
    
    child_pid = None
    for line in out.splitlines():
        if "CHILD_PID:" in line:
            child_pid = int(line.split(":")[1])
    
    if child_pid:
        time.sleep(0.5)
        try:
            os.kill(child_pid, 0)
            print(f"FAILURE: Child process {child_pid} still alive.")
            sys.exit(1)
        except OSError:
            print(f"SUCCESS: Child process {child_pid} reaped.")
    else:
        print("FAILURE: Could not determine child PID.")
        sys.exit(1)

if __name__ == '__main__':
    test_reaper()
