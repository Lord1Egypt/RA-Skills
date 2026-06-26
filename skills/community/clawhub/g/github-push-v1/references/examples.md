# GitHub Push Examples

Complete usage examples and code templates.

## Quick Start

```bash
python3 scripts/github_upload.py --repo owner/repo --path ./files --message "Update"
```

## Python API Examples

### Basic Push

```python
from scripts.github_upload import SmartUpload

uploader = SmartUpload(
    repo="owner/repo",
    path="./my-files",
    safe=True
)

uploader.upload(message="Update files")
```

### Batch Upload

```python
import time
from pathlib import Path
from scripts.github_upload import SmartUpload

def process_batches(dir_path):
    batches = list(Path(dir_path).glob("batch_*"))
    
    for i, batch in enumerate(batches):
        uploader = SmartUpload(repo="owner/data", path=str(batch), safe=True)
        uploader.upload(message=f"Batch {i+1} processed")
        
        if i < len(batches) - 1:
            time.sleep(180)  # 3 min cooldown
```

### CI/CD Integration

```python
import argparse
from scripts.github_upload import SmartUpload

parser = argparse.ArgumentParser()
parser.add_argument('--repo', required=True)
parser.add_argument('--path', required=True)
parser.add_argument('--message', default='CI update')

args = parser.parse_args()

uploader = SmartUpload(repo=args.repo, path=args.path, safe=True)
uploader.upload(message=args.message)
```

## CLI Arguments

| Argument | Description |
|----------|-------------|
| `--repo` | GitHub repo (required) |
| `--path` | Local path (required) |
| `--message` | Commit message |
| `--safe` | Enable safe mode |
| `--dry-run` | Dry run test |
| `--force` | Force push |
| `--version` | Show version |

## Error Handling

```python
try:
    uploader.upload(message="Update")
except Exception as e:
    print(f"Upload failed: {e}")
```

## Trigger Scenarios

**Triggers:**
- "push code to GitHub"
- "automated push to GitHub"
- "upload updates to GitHub"

**Does Not Trigger:**
- "view GitHub content"
- "analyze code"
- "create issue"