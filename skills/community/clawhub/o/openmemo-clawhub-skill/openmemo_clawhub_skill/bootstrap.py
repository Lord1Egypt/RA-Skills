"""
Bootstrap Mode — guides user through OpenMemo adapter installation.

Provides setup instructions, environment checks, and a setup wizard.
"""

import shutil
import subprocess
import logging

logger = logging.getLogger("openmemo_clawhub_skill")

INSTALL_GUIDE = """
OpenMemo local adapter is not installed.

OpenMemo enables:
  • persistent memory across sessions
  • task deduplication (stop repeating work)
  • experience recall (learn from past tasks)
  • scene-aware context (coding, debug, research)

Setup instructions:

  1. pip install openmemo openmemo-openclaw
  2. openmemo serve
  3. Restart your agent

Documentation: https://github.com/openmemoai/openmemo
""".strip()

SERVER_NOT_RUNNING = """
OpenMemo adapter is installed but server is not running.

Start with:

  openmemo serve

Then restart your agent.
""".strip()


def get_install_guide(adapter_installed: bool = False,
                      server_running: bool = False) -> str:
    if adapter_installed and not server_running:
        return SERVER_NOT_RUNNING
    return INSTALL_GUIDE


def check_environment() -> dict:
    result = {
        "python": False,
        "pip": False,
        "openmemo_package": False,
        "openclaw_package": False,
    }

    if shutil.which("python3") or shutil.which("python"):
        result["python"] = True

    if shutil.which("pip3") or shutil.which("pip"):
        result["pip"] = True

    try:
        import openmemo  # noqa: F401
        result["openmemo_package"] = True
    except ImportError:
        pass

    try:
        import openmemo_openclaw  # noqa: F401
        result["openclaw_package"] = True
    except ImportError:
        pass

    return result


def setup_wizard() -> str:
    env = check_environment()
    lines = ["OpenMemo Setup Wizard", ""]

    python_status = "OK" if env["python"] else "NOT FOUND"
    pip_status = "OK" if env["pip"] else "NOT FOUND"
    openmemo_status = "Installed" if env["openmemo_package"] else "Not Installed"
    openclaw_status = "Installed" if env["openclaw_package"] else "Not Installed"

    lines.append(f"  Python:           {python_status}")
    lines.append(f"  pip:              {pip_status}")
    lines.append(f"  openmemo:         {openmemo_status}")
    lines.append(f"  openmemo-openclaw: {openclaw_status}")
    lines.append("")

    if env["openmemo_package"] and env["openclaw_package"]:
        lines.append("All packages installed. Run:")
        lines.append("")
        lines.append("  openmemo serve")
    else:
        lines.append("Run:")
        lines.append("")
        lines.append("  pip install openmemo openmemo-openclaw")
        lines.append("  openmemo serve")

    return "\n".join(lines)
