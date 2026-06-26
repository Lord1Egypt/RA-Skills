---
name: ln-tool
description: Create hard and symbolic links between files. Use for file referencing, shortcuts, and directory organization.
---
# Ln - Link Creation Utility

Create links between files. Supports hard links (same inode, same data) and symbolic links (reference to target path). Essential for file organization and shared resources.

## Usage

```bash
ln-tool [options] <target> <link_name>
```

## Link Types

- Hard links: Direct reference to file data (same inode)
- Symbolic links: Path reference (can cross filesystems)

## Options

- `-s`: Create symbolic link (default is hard link)
- `-f`: Force creation (remove existing destination)
- `-n`: Treat destination as normal file

## Examples

```bash
# Hard link
ln-tool original.txt link.txt

# Symbolic link
ln-tool -s /usr/bin/python3 ./python

# Force replace existing link
ln-tool -sf /usr/bin/python3 ./python
```