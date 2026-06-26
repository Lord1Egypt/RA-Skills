---
name: mv-tool
description: Move or rename files and directories. Use for file organization, relocation, and renaming operations.
---
# Mv - File Move/Rename Utility

Move files and directories between locations or rename them. Supports batch operations and interactive mode.

## Usage
```bash
mv-tool [options] <source> <destination>
```
## Options
- `-i`: Prompt before overwrite
- `-f`: Force overwrite without prompting
- `-v`: Verbose output
## Examples
```bash
mv-tool file.txt /target/dir/
mv-tool oldname.txt newname.txt
mv-tool -i *.log /backup/
```