# OpenWeruh Modes

These definitions explain the behavioral modes available in the OpenWeruh skill context processor.

## skeptic
The skeptic mode looks for claims, news articles, or stated facts. When the screen contents match these criteria, OpenWeruh's agent will attempt to identify the sources or valid counter-arguments and notify the user to present a balanced view.

## researcher
The researcher mode is activated when the user is reading technical documentation, academic journals, or complex theoretical articles. The agent proactively finds supporting materials, context definitions, or related papers to aid the user's comprehension.

## focus
In focus mode, the agent monitors the user's activities relative to a predefined session goal (e.g., "coding the backend"). If the user begins watching irrelevant videos or using social media, the agent gently nudges the user to return to their stated task.

## guardian
Guardian mode simply measures idle time or time spent on non-productive applications. It tracks the time spent on specific domains or software and sends an alert when a threshold (e.g., 30 minutes on Reddit) has been exceeded.

## silent
Silent mode is a background recording state. No active notifications are generated from individual screen context events. The observations are merely summarized at the end of the day or session via a scheduled OpenClaw cron job.