# File Organization Patterns

## Directory Structure Templates

### Standard Project
```
project-name/
├── src/              # Source code
│   ├── components/
│   ├── utils/
│   └── index.js
├── tests/            # Test files
│   ├── unit/
│   └── integration/
├── docs/             # Documentation
│   └── api/
├── assets/           # Static files
│   ├── images/
│   ├── fonts/
│   └── styles/
├── scripts/          # Build/automation
├── config/           # Configuration
└── dist/             # Build output (gitignore)
```

### Documentation Site
```
docs/
├── guides/           # User guides
├── api/              # API reference
├── tutorials/        # Step-by-step
├── examples/         # Code samples
└── images/           # Documentation assets
```

### Research/Data
```
research/
├── data/             # Raw data
├── processed/        # Cleaned data
├── analysis/         # Scripts, notebooks
├── outputs/          # Charts, reports
└── literature/       # Papers, notes
```

## Batch Rename Patterns

### Sequential Numbering
```bash
# Add prefix with numbering
i=1; for f in *.txt; do mv "$f" "doc_$(printf "%03d" $i).$f"; ((i++)); done

# Rename with date
for f in *.md; do mv "$f" "$(date +%Y-%m-%d)_$f"; done
```

### Extension-Based Organization
```bash
# Group by type
mkdir -p images docs code
find . -maxdepth 1 -name "*.png" -o -name "*.jpg" -o -name "*.gif" | xargs -I {} mv {} images/
find . -maxdepth 1 -name "*.md" -o -name "*.txt" -o -name "*.pdf" | xargs -I {} mv {} docs/
find . -maxdepth 1 -name "*.py" -o -name "*.js" -o -name "*.ts" | xargs -I {} mv {} code/
```

### Date-Based Organization
```bash
# Organize by modification date
for f in *; do
  if [ -f "$f" ]; then
    date=$(stat -c %y "$f" | cut -d' ' -f1)
    mkdir -p "$date"
    mv "$f" "$date/"
  fi
done
```

## Find Commands

### By Extension
```bash
find . -type f -name "*.py"              # Python files
find . -type f -name "*.md"              # Markdown files
find . -type f \( -name "*.jpg" -o -name "*.png" \)  # Multiple extensions
```

### By Modification Time
```bash
find . -type f -mtime -7                 # Modified in last 7 days
find . -type f -mtime +30                # Modified over 30 days ago
find . -type f -mmin -60                 # Modified in last hour
```

### By Size
```bash
find . -type f -size +100M               # Files > 100MB
find . -type f -size -1K                 # Files < 1KB
find . -type f -size +10M -size -50M     # Files 10-50MB
```

### By Depth
```bash
find . -maxdepth 1 -type f               # Files in current dir only
find . -mindepth 2 -type f               # Files nested 2+ levels
```

## Project Scaffolding

### Create Structure
```bash
mkdir -p project-name/{src,tests,docs,assets,scripts,config}
cd project-name
touch README.md
touch src/index.js
touch tests/index.test.js
```

### Initialize Git
```bash
git init
cat > .gitignore << EOF
node_modules/
dist/
.env
*.log
.DS_Store
EOF
git add -A
git commit -m "chore: initialize project structure"
```

### Copy Template
```bash
# From template directory
cp -r /path/to/template/* project-name/
# Or use tar for selective copy
tar -cf - --include='*.md' --include='*.js' /template | (cd project-name && tar -xf -)
```

## Safety Patterns

### Dry Run Pattern
```bash
# Always preview first
echo "Would move these files:"
find . -name "*.txt"
# Review output, then execute
find . -name "*.txt" -exec mv {} dest/ \;
```

### Backup Before Restructure
```bash
# Snapshot current state
tar -czf backup_$(date +%Y%m%d_%H%M%S).tar.gz target-directory/
# Or use git commit
git add -A
git commit -m "backup: pre-restructure snapshot"
```

### Safe Move with Error Handling
```bash
for f in *.txt; do
  if [ -f "$f" ]; then
    mv "$f" dest/ && echo "Moved: $f" || echo "Failed: $f"
  fi
done
```

### Avoid Overwriting
```bash
# Check if destination exists
for f in *.txt; do
  dest="target/$f"
  if [ -e "$dest" ]; then
    echo "Skip: $dest exists"
  else
    mv "$f" "$dest"
  fi
done
```

## Common Operations

### Flatten Nested Directories
```bash
# Move all files from subdirs to parent
find . -type f -exec mv {} . \;
# Remove empty dirs
find . -type d -empty -delete
```

### Remove Empty Files
```bash
find . -type f -empty -delete
```

### Find Duplicates (by name)
```bash
find . -type f -name "*.txt" | sort | uniq -d
```

### Organize Git Repo
```bash
# Move untracked files into proper structure
mkdir -p src docs tests
git status --short | grep '^??' | awk '{print $2}' | while read f; do
  case "$f" in
    *.md) mv "$f" docs/ ;;
    *.test.*) mv "$f" tests/ ;;
    *) mv "$f" src/ ;;
  esac
done
```