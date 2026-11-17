"""确保 Skill 根目录在 sys.path 上，使 `from core ...` 等绝对导入在 pytest 下可用。"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
