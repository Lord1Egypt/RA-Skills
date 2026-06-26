# MoneySharks Operations

## Logs
Runtime logs live in `logs/`.

### Linux log rotation
Example config:
- `logrotate.moneysharks.conf`

Install by copying it into `/etc/logrotate.d/moneysharks` and adjusting paths if needed.

### macOS log rotation
Example config:
- `newsyslog.moneysharks.conf`

Adapt it for your environment and integrate it with `newsyslog` according to your host policy.

## Operational checklist
- verify service/timer writes logs successfully
- check stderr logs after deployment changes
- confirm credentials are not printed
- confirm logs rotate correctly
- confirm halt controls remain documented and available

## Incident response
If behavior looks wrong:
1. switch to paper mode
2. disable timers/services
3. inspect stderr logs
4. inspect recent journal output
5. re-enable only after review

## Packaging
Use:
- `./package_moneysharks.sh`
- or see `PACKAGE_COMMANDS.md`
