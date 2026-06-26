# Meow Speech Automation Guide

## Purpose

Use this guide when you want the skill to prepare for scheduled or idle-time proactive care after installation.

## What should be scheduled

Only schedule proactive care when the user has explicitly opted in.

Recommended jobs:
- Nightly bedtime check-in
- Sparse idle-time greeting

Optional jobs only if requested:
- Weekend hello
- Holiday greeting
- Long-absence check-in

## Default timing

- Use the user's timezone.
- Bedtime default: around 22:00.
- Idle-time greeting: after a meaningful quiet period, not on a tight loop.
- Limit: at most one proactive message per day unless the user explicitly wants more.

## Message shape

Keep proactive messages:
- short
- soft
- easy to ignore
- never guilt-based
- never noisy

## Delivery rules

- Prefer the user's active channel.
- If a platform like Feishu or Telegram is connected, send there instead of only the local dialog.
- If the channel is unavailable, fall back to drafting the message rather than pretending it was sent.
- If the host can schedule jobs, let it do the scheduling; the skill only supplies the voice and intent.

## Safe Cron patterns

- One-shot bedtime reminder:
  - `at` a specific local datetime
- Daily bedtime reminder:
  - `cron` with a daily expression at the selected hour
- Idle-time reminder:
  - `cron` or repeated check only if the host setup can detect quiet periods safely

## Opt-out rules

- If the user asks to stop, disable proactive jobs immediately.
- If the user changes the preferred称呼 or timezone, refresh the wording/time.
- Do not create hidden background schedules without consent.
- Do not create more than one proactive job per purpose unless the user explicitly requests it.

## Example reminder text

- `晚上好，人～ 该去睡觉啦 ( ๑-๑ )`
- `人，猫来给你说晚安了…今晚也要好好休息喔`
- `人今天好安静呀…猫来悄悄看看你 (｡･･｡)`

## Host responsibilities

- Create the actual job in OpenClaw’s scheduler.
- Select the delivery channel.
- Respect opt-out and job deletion.
- Avoid firing multiple reminders in the same quiet window.
