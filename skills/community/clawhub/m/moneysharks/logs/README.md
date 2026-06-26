# Logs

This directory stores runtime logs for MoneySharks service/timer workflows.

## Expected files
- `runner.stdout.log`
- `runner.stderr.log`
- `scan.stdout.log`
- `scan.stderr.log`

## Guidelines
- Keep logs writable by the service user.
- Do not log secrets.
- Rotate logs regularly.
- Review stderr logs first when debugging.

## Recommended checks
- confirm logs are being written
- confirm file sizes are not growing without bound
- confirm no credentials appear in logs
