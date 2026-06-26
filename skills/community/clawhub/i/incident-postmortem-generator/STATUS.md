# incident-postmortem — Status

**Status:** Ready
**Price:** $59
**Built:** 2026-03-30

## Features
- Log parsing (syslog, JSON, Apache/Nginx, Python tracebacks, Docker, generic)
- Timeline reconstruction from logs + JSON events
- Blame-free language checker with suggestions
- Severity classification (P0-P3)
- 3 output formats (markdown, HTML, JSON)
- CI-friendly exit codes
- Template sections: summary, impact, timeline, root cause, detection, resolution, lessons, actions

## Tested
- Basic generation (--title --severity)
- Full JSON incident file (--from)
- Log parsing with event extraction
- HTML output with styled template
- JSON structured output
- Blame language checker
- Multiple log formats

## Next Steps
- Publish to ClawHub after April 10
