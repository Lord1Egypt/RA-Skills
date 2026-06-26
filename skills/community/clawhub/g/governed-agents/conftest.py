import os
import tempfile

# Set OPENCLAW_WORKSPACE before openclaw_wrapper is first imported,
# so the module-level WORKSPACE assertion passes on all platforms.
# Uses system tempdir to handle macOS /private/var/folders/... paths.
if "OPENCLAW_WORKSPACE" not in os.environ:
    os.environ["OPENCLAW_WORKSPACE"] = os.path.join(tempfile.gettempdir(), "governed-test-workspace")
