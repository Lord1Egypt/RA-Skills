import os
import sys
import pytest
from unittest.mock import patch

# Add scripts directory to path to allow import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "skills", "pm-skill", "scripts")))

import init_prd

def test_init_prd_guardrail(capsys):
    with patch.object(sys, "argv", ["init_prd.py", "--project", "test_project", "--title", "test_title"]):
        with pytest.raises(SystemExit) as e:
            init_prd.main()
        
        assert e.value.code == 1
        captured = capsys.readouterr()
        assert "Startup validation failed" in captured.out
