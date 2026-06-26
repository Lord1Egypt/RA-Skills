import os
import tempfile

# Set OPENCLAW_WORKSPACE before openclaw_wrapper is first imported,
# so the module-level WORKSPACE assertion passes on all platforms.
# On macOS, __file__ may resolve through /private/ which doesn't match Path.home().
if "OPENCLAW_WORKSPACE" not in os.environ:
    os.environ["OPENCLAW_WORKSPACE"] = os.path.join(tempfile.gettempdir(), "governed-test-workspace")
