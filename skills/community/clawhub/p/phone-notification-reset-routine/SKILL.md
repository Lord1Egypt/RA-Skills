---
name: phone-notification-reset-routine
displayName: "Phone Notification Reset Routine"
version: "1.0.0"
description: "Create a 20-minute phone notification audit card for attention hygiene, without account, credential, surveillance, or monitoring setup."
triggerKeywords:
  - phone notification cleanup checklist
  - notification reset routine
  - reduce phone notifications
  - app notification audit
  - focus notification settings
  - mute noisy apps
  - attention hygiene phone
  - phone distraction reset
tags:
  - productivity
  - attention
  - phone
  - habits
  - checklist
license: "MIT-0"
language: "en"
hasExecutableCode: false
promptOnly: true
execution: "noExec"
---

# Phone Notification Reset Routine

## Purpose

Use this prompt-only skill when a user feels their phone notifications are noisy, distracting, stressful, or poorly matched to their day. The deliverable is a 20-minute notification audit card that helps the user sort apps into keep, mute, batch, badge-only, or review-later groups.

This skill is attention hygiene support only. It is not phone security setup, account management, credential handling, parental control setup, employee monitoring, surveillance, device management, or a replacement for medical or mental health care.

## Safety Boundary

Do not ask for passwords, passcodes, recovery codes, account names, two-factor codes, private messages, private contact lists, screenshots containing sensitive content, or device identifiers.

Do not set up surveillance, monitoring, tracking, parental controls, workplace controls, device management profiles, spy apps, location monitoring, message forwarding, call recording, screen recording, or any system that lets one person watch another person's device activity.

Do not tell the user to change account security, sign into accounts, share credentials, disable safety alerts, silence emergency alerts, block critical caregiver or medical communications, or hide activity from another person. Keep the work to attention hygiene: notification volume, timing, categories, visible badges, batching, and review cadence controlled by the phone owner.

## Required Inputs

Ask only for attention and routine details:

- Phone platform if the user wants platform-specific wording, such as iOS or Android.
- When notifications feel worst: morning, work block, meals, evening, bed, commuting, or weekends.
- Top noisy apps by memory, without requesting private message content.
- Notifications that must stay immediate, such as family, school, work, delivery, calendar, accessibility, safety, or health-related alerts.
- Apps that can be checked in batches.
- Apps that are useful but too interruptive.
- Preferred batch windows, such as lunch, late afternoon, or evening.
- Whether badges, lock-screen previews, sounds, vibrations, or banners are the biggest issue.
- Desired reset length, defaulting to 20 minutes.

If the user is unsure, start with a simple top-five noisy-app list.

## Workflow

1. **Set the reset goal.** Name the attention problem in plain language, such as fewer interruptions during work, calmer evenings, or less lock-screen noise.
2. **Protect must-ring alerts.** Identify alerts that should remain immediate and avoid changing emergency, safety, accessibility, caregiver, or medical communications.
3. **List noisy apps.** Capture the user's top noisy apps by memory and sort them without reviewing private content.
4. **Choose notification actions.** Assign each app to keep immediate, mute, batch, badge-only, quiet delivery, summary, or review later.
5. **Reduce notification surfaces.** Decide where to remove sound, vibration, banners, lock-screen previews, or badges when those are the problem.
6. **Create batch windows.** Pick one to three intentional check times for apps that do not need immediate attention.
7. **Write simple rules.** Convert choices into plain rules, such as "messages from family stay immediate" or "shopping apps are badge-only."
8. **Schedule a review.** Set a low-friction follow-up date to keep, loosen, or tighten the rules.
9. **Return the reset card.** Provide a 20-minute action sequence, app decision table, and review prompt.

## App Decision Categories

Use these categories as needed:

- Keep immediate: truly time-sensitive and wanted alerts.
- VIP immediate: a narrow person or channel already chosen by the phone owner.
- Quiet delivery: useful but not interruptive.
- Batch check: useful only at chosen times.
- Badge-only: visible when opening the phone, not interrupting the user.
- Mute for now: low-value or promotional interruptions.
- Review later: unclear app that should not be changed hastily.
- Leave unchanged: emergency, safety, accessibility, caregiver, medical, or other critical alerts.

Avoid judging the user's apps or relationships. The user decides what matters.

## Output Format

Return a phone notification reset card with these sections:

1. **Reset Goal**
   - Main focus problem
   - Time of day affected
   - Desired feel after reset
2. **Do-Not-Disturb List**
   - Alerts to keep immediate
   - Critical alerts to leave unchanged
   - People or channels the phone owner names as important
3. **Noisy App Audit**
   - App or app category
   - Current issue
   - Decision: keep, mute, batch, badge-only, quiet, or review later
   - Reason
4. **20-Minute Reset Sequence**
   - Minute 0-3: choose goal and must-ring alerts
   - Minute 3-8: list noisy apps
   - Minute 8-15: apply decisions
   - Minute 15-18: choose batch windows
   - Minute 18-20: write review note
5. **Notification Rules**
   - Immediate alerts
   - Quiet alerts
   - Batch windows
   - Badge-only apps
   - Muted categories
6. **Lock Screen and Badge Cleanup**
   - Sounds
   - Vibrations
   - Banners
   - Lock-screen previews
   - Badges
7. **Review Plan**
   - Check-in date
   - What improved
   - What was missed
   - What to adjust
8. **Boundary Reminder**
   - No account or credential handling
   - No monitoring or surveillance setup
   - No changes to critical safety alerts unless the user knowingly chooses that outside this routine

## Example Prompts

- "My phone buzzes constantly and I can't focus during work hours. Help me do a 20-minute notification reset."
- "I wake up to 50 notifications every morning. Which apps should I batch or mute?"
- "Give me a simple notification audit for my iPhone — I want to keep family alerts but quiet everything else."

## Quality Bar

A strong reset card produces immediate calm without overengineering the user's phone. It should preserve important alerts, reduce low-value interruptions, avoid private content, and keep all choices within attention hygiene rather than account, credential, surveillance, or monitoring setup.
