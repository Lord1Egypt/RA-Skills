---
name: message-in-a-bottle
description: Randomly retrieve a message in a bottle (drift bottle) containing life insights, small stories, wishes, or inspirational quotes. Use when the user asks for a drift bottle, message in a bottle, random message, or needs inspiration/wisdom. Trigger words: 漂流瓶, message in a bottle, drift bottle, 随机消息, 瓶中信.
---

# Message in a Bottle

Get a random message in a bottle containing life insights, stories, wishes, or inspirational thoughts.

## Usage

When triggered, run the script to randomly select and return a drift bottle message:

```bash
python3 scripts/get_bottle.py
```

The script will randomly return one of the pre-written drift bottle messages.

## Message Types

The drift bottles may contain:

- Life insights and wisdom
- Short stories or anecdotes
- Wishes and blessings
- Inspirational quotes
- Thoughtful reflections

## Extending Messages

To add new drift bottle messages, edit `scripts/get_bottle.py` and add new entries to the `messages` list.

Each message should be concise, meaningful, and capable of standing alone.
