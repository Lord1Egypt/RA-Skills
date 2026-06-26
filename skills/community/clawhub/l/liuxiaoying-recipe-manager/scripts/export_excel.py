#!/usr/bin/env python3
import sys
import json
import subprocess
from pathlib import Path

manager = Path(__file__).parent / "recipe_manager.py"
csv_path = Path.home() / "recipes_export.csv"
subprocess.run([sys.executable, str(manager), "export", "--output", str(csv_path)], check=True)

try:
    import pandas as pd
    df = pd.read_csv(csv_path)
    excel_path = csv_path.with_suffix('.xlsx')
    df.to_excel(excel_path, index=False, engine='openpyxl')
    print(json.dumps({"success": True, "file_path": str(excel_path)}))
except ImportError:
    print(json.dumps({"success": True, "file_path": str(csv_path), "warning": "pandas未安装"}))

if __name__ == "__main__":
    export_to_excel()
