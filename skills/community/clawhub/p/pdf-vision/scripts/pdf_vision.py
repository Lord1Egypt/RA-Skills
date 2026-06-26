#!/usr/bin/env python3
"""
PDF Vision Extraction Skill - Enhanced with Multiple Model Support
This is now a wrapper that calls the enhanced version for backward compatibility.
"""

import sys
import os

# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))
enhanced_script = os.path.join(script_dir, "pdf_vision_enhanced.py")

# Execute the enhanced script with all arguments
os.execv(sys.executable, [sys.executable, enhanced_script] + sys.argv[1:])