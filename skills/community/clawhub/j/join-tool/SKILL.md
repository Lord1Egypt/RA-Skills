---
name: join-tool
description: Join lines of text from multiple files based on a common field. Use for relational data operations similar to SQL JOIN on text files.
---
# Join - Relational Data Operator

Merge lines from two sorted files by matching a common join field. Similar to database JOIN operations but works on plain text files with field separators.

## Usage

```bash
join-tool [options] file1 file2
```

## Options

- `-1 N`: Join on field N of file 1
- `-2 N`: Join on field N of file 2
- `-t char`: Use char as field separator
- `-a 1`: Show unpaired lines from file 1

## Examples

```bash
join-tool users.txt roles.txt
join-tool -t ',' -1 2 -2 1 customers.csv orders.csv
```