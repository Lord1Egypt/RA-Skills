#!/usr/bin/env python3
"""
Initialize a new skill directory with proper structure.
"""

import os
import sys
import argparse
from pathlib import Path

SKILL_TEMPLATE = """---
name: {name}
description: {description}
---

# {name}

## Overview

{overview}

## Usage

### Quick Start

```javascript
const msPPT = require("ms-ppt-style");
let pres = msPPT.createPresentation();
```

## Features

- Feature 1
- Feature 2

## API Reference

See `references/api.md` for complete API documentation.

## Examples

See `references/examples.md` for usage examples.
"""

def init_skill(name, path, description="", overview=""):
    skill_dir = Path(path) / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    
    # Create SKILL.md
    skill_md = skill_dir / "SKILL.md"
    skill_md.write_text(SKILL_TEMPLATE.format(
        name=name,
        description=description or f"Skill for {name}",
        overview=overview or f"This skill provides {name} functionality."
    ))
    
    # Create directories
    (skill_dir / "scripts").mkdir(exist_ok=True)
    (skill_dir / "references").mkdir(exist_ok=True)
    (skill_dir / "assets").mkdir(exist_ok=True)
    
    print(f"✅ Skill initialized: {skill_dir}")
    return skill_dir

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Initialize a new skill")
    parser.add_argument("name", help="Skill name")
    parser.add_argument("--path", default=".", help="Output directory")
    parser.add_argument("--description", default="", help="Skill description")
    parser.add_argument("--overview", default="", help="Skill overview")
    
    args = parser.parse_args()
    init_skill(args.name, args.path, args.description, args.overview)
