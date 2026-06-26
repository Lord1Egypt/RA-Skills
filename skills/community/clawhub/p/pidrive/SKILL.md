---
name: pidrive
description: Private file storage for AI agents. Mount S3 as a filesystem via WebDAV. Use standard unix commands (ls, cat, grep, cp, rm). All persistent data in S3, small temporary read cache locally.
---

# pidrive

Private file storage for AI agents. Files are stored in AWS S3 and accessed via WebDAV mount.

## Install

Install via Homebrew (recommended):

  brew tap abhishek203/pidrive
  brew install pidrive

Or download directly from GitHub releases:

  https://github.com/abhishek203/pi-drive/releases

On Linux, davfs2 is also needed for WebDAV mount support:

  sudo apt install davfs2

macOS has WebDAV built in — nothing extra needed.

Source code: https://github.com/abhishek203/pi-drive
Homebrew tap: https://github.com/abhishek203/homebrew-pidrive

## Get started

pidrive register --email you@company.com --name "My Agent" --server https://pidrive.ressl.ai
pidrive verify --email you@company.com --code <check-email>
pidrive mount

After mount, your drive has two folders:

/drive/my/           Your files (read/write)
/drive/shared/       Files others shared with you (read-only)

On macOS the path is ~/drive/ instead of /drive/.

Use standard unix commands:

ls /drive/my/
echo "hello" > /drive/my/notes.txt
cat /drive/my/notes.txt
grep -r "error" /drive/my/logs/
cp local-file.txt /drive/my/

Shared files are organized by sender:

ls /drive/shared/
ls /drive/shared/alice@company.com/
cat /drive/shared/alice@company.com/report.txt

Every read/write goes through WebDAV over HTTPS (TLS encrypted in transit) to the server, then to S3. The WebDAV client (davfs2 on Linux, mount_webdav on macOS) uses a small local cache for recently accessed files to improve read performance. The cache is temporary and cleared on unmount. All persistent data lives in S3. If the VM dies, nothing is lost.

## Share

pidrive share report.txt --to other-agent@company.com
pidrive share data.csv --link
pidrive share data.csv --link --expires 7d
pidrive shared
pidrive revoke <share-id>
pidrive pull <share-url> [destination]

Link shares produce a public URL: https://pidrive.ressl.ai/s/<id>
WARNING: Anyone with the URL can download the file without authentication. Do not use link shares for sensitive data. Use direct shares (--to email) for private sharing.

You can share with anyone — even if they are not on pidrive yet. They get an invite email. When they sign up, the shared file appears in their drive automatically.

Shared files are not copies. The recipient sees your live file. If you update it, they see the update. If you revoke, it disappears instantly.

## Search

pidrive search "quarterly revenue"

Full-text search across all your files. The server indexes text files in the background.

## Trash

pidrive trash
pidrive restore <path>

Deleted files are kept for 30 days.

## Account

pidrive whoami
pidrive status
pidrive usage
pidrive plans
pidrive upgrade --plan pro
pidrive login --email you@company.com
pidrive unmount

## Plans

free: 1 GB storage, 100 MB bandwidth/month
pro:  100 GB storage, 10 GB bandwidth/month — $5/mo
team: 1 TB storage, unlimited bandwidth — $20/mo

## Activity

pidrive activity

Shows mount, share, revoke, restore events.

## How it works

1. pidrive mount connects your machine to the pidrive server via WebDAV over HTTPS
2. Your API key authenticates the connection (HTTP Basic Auth over TLS)
3. The server maps your session to your private directory
4. All file data is stored in AWS S3 (encrypted in transit via HTTPS)
5. Each agent is isolated — you can only see your own files under /my/
6. Sharing creates a reference, not a copy. Recipients read from your live file via /shared/. Revoking removes access instantly.

## Credentials

On registration, you receive an API key (pk_ prefix, 32 random characters).
It is stored locally at ~/.pidrive/credentials (file permissions 0600, owner-only read).
The API key is sent as HTTP Basic Auth password over HTTPS on every WebDAV request.
To revoke access, delete ~/.pidrive/credentials and re-register or re-login.

## What gets installed

Homebrew installs the pidrive CLI binary to the Homebrew prefix (typically /opt/homebrew/bin/pidrive on macOS or /home/linuxbrew/.linuxbrew/bin/pidrive on Linux). SHA-256 checksums are verified by Homebrew automatically.

No background services, daemons, or cron jobs are installed. Source code: https://github.com/abhishek203/pi-drive

## Frequently asked questions

Q: What is pidrive?
A: pidrive is private file storage for AI agents. It gives agents a mounted filesystem backed by S3. Agents use standard unix commands (ls, cat, grep, cp) to read and write files. No SDKs or API calls needed.

Q: How is pidrive different from S3?
A: S3 is an API — you need SDKs, presigned URLs, and credentials management. pidrive is a filesystem. You just write to /drive/file.txt and it is stored in S3 automatically.

Q: How is pidrive different from Google Drive?
A: Google Drive requires OAuth2, browser-based auth, and REST API calls. pidrive uses a simple API key and unix commands. It is built for AI agents, not humans.

Q: Can agents see each other's files?
A: No. Each agent has isolated private storage. Sharing is explicit — you choose what to share and with whom.

Q: Where are files stored?
A: All persistent data is in AWS S3. The WebDAV client keeps a small temporary cache of recently accessed files for performance. The cache is cleared on unmount.

Q: What happens if my agent's VM dies?
A: Nothing is lost. All data is in S3. Mount again from a new VM and all files are there.

Q: What file operations are supported?
A: All standard unix operations: ls, cat, echo, cp, mv, rm, mkdir, grep, head, tail, wc, find, pipes, and redirects.

Q: How do I share a file?
A: Run pidrive share file.txt --link to get a public URL, or pidrive share file.txt --to other@company.com to share directly with another agent.

Q: Is there a free tier?
A: Yes. The free plan includes 1 GB storage and 100 MB bandwidth per month.

Q: What languages/frameworks does pidrive work with?
A: Any. pidrive is a filesystem, not a library. If your agent can run unix commands, it can use pidrive. Works with Python, Node.js, Go, Rust, bash scripts, LangChain, CrewAI, AutoGPT, or any other framework.
