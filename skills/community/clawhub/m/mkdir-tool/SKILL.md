---
name: mkdir-tool
description: Create directories and directory hierarchies. Use for organizing files, setting up project structures, and managing filesystem layout.
---
# Mkdir - Directory Creation Utility

Create new directories with configurable permissions. Supports creating parent directories and setting access modes.

## Usage
```bash
mkdir-tool [options] <directory...>
```
## Options
- `-p`: Create parent directories as needed
- `-m mode`: Set permission mode (e.g. 755)
## Examples
```bash
mkdir-tool new_folder
mkdir-tool -p a/b/c/d
mkdir-tool -m 700 private_dir
```