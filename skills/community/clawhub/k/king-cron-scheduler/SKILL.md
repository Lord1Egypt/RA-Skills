# Cron Scheduler

Enterprise cron job management with monitoring, logging, and failure alerts.

## Features
- Visual cron expression builder
- Job execution logging
- Failure alert configuration (Telegram, Email, Webhook)
- Job dependency management
- Execution time statistics
- Pause/resume individual jobs

## Usage
```bash
clawdhub install king-cron-scheduler
python3 main.py add "0 */6 * * *" backup.sh
python3 main.py list
python3 main.py logs backup-job
```
