# GitHub Push - Security Notice

This tool implements enterprise-grade safety mechanisms following GitHub's automation guidelines.

## Security Features

- Rate limiting: 3-5 second delays between operations
- Commit batching: Single commit for multiple files
- File validation: Pre-push checks for sensitive files
- Auto-exclusion: .git/, .DS_Store, SSH keys, large files

## Best Practices

1. Always use `--dry-run` before production push
2. Monitor push frequency (max 50/hour)
3. Use meaningful commit messages
4. Configure SSH keys properly
5. Clean sensitive files regularly

## Report Security Issues

Contact security@openclaw.ai for security vulnerabilities.

## License

MIT - OpenClaw Skill Standard