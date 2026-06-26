import sys
import os
from pathlib import Path

# Add the root of the skill to sys.path so we can import `tools.*`
CURRENT_DIR = Path(__file__).parent.resolve()
SKILL_ROOT = CURRENT_DIR.parent
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

# Mock environment variables so unit tests don't hit live instances by default
os.environ["RADARR_URL"] = "http://mock-radarr:7878/api/v3"
os.environ["RADARR_API_KEY"] = "mock_radarr_key"
os.environ["QBIT_URL"] = "http://mock-qbit:8080"
os.environ["QBIT_USERNAME"] = "mock_admin"
os.environ["QBIT_PASSWORD"] = "mock_pass"
os.environ["PLEX_URL"] = "http://mock-plex:32400"
os.environ["PLEX_TOKEN"] = "mock_plex_token"
