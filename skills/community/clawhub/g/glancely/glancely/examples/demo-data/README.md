# Demo Data

Reproduces the README screenshot in 30 seconds with no Google OAuth setup.

```bash
GLANCE_HOME=$PWD/examples/demo-data python3 examples/demo-data/seed.py
GLANCE_HOME=$PWD/examples/demo-data python3 glancely/dashboard/build.py
open glancely/dashboard/index.html
```

The diary panel will show `error` because diary_logger requires real Calendar
access. Mood, reminders, and MIT will all show real-looking populated panels.
