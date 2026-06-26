# Human-like Reply Skill - Technical Reference

## Architecture

The `human-like-reply` skill consists of three main components:

1. **ReplyState Manager**: Tracks conversation state per session
2. **ReplyFormatter**: Processes AI-generated text
3. **Topic Detector**: Identifies when the conversation topic changes

## Data Flow

```
User Message → AI generates reply → ReplyFormatter processes → Send to user
```

The formatter works in two stages:

1. **Pre-processing**: Remove unnecessary greetings if we decide not to use one
2. **Post-processing**: Apply casual replacements, trim whitespace, add greeting if needed

## State Storage

State is stored in `memory/reply_state.json`:

```json
{
  "conversations": {
    "session_key_1": {
      "rounds": 5,
      "last_message_time": "2026-03-10T14:30:00",
      "last_used_greeting": true,
      "current_topic": "weather",
      "greeting_count": 3
    }
  }
}
```

## Configuration

Default configuration (in `SKILL.md`):

```yaml
human_like_reply:
  enabled: true
  greeting_threshold: 3
  topic_change_threshold: 5
  silence_minutes: 30
  use_smileys: true
  formal_level: 0.3
```

## Greeting Decision Algorithm

```python
def should_use_greeting(conv, config, is_new_topic):
    rounds = conv["rounds"]

    # 1. Check silence gap
    if silence > config["silence_minutes"] * 60:
        return True, greeting()

    # 2. New topic early in conversation
    if is_new_topic and rounds < config["topic_change_threshold"]:
        return True, greeting()

    # 3. Early rounds with probability decay
    if rounds < config["greeting_threshold"]:
        prob = 1.0 - (rounds / config["greeting_threshold"])
        return random() < prob

    # 4. Late rounds only on topic change
    if is_new_topic and random() < 0.3:
        return True, greeting()

    return False, ""
```

## Topic Change Detection

Simple keyword overlap approach:

- Extract Chinese 2+ character words from new message
- Compare with last 3 messages' keywords
- If overlap < 2, consider it a new topic

## Integration Points

In OpenClaw, this skill should be hooked into:

1. **Before sending**: `message(action="send")` pre-hook
2. **Session state**: Access session key for per-conversation tracking
3. **Configuration**: Read from OpenClaw config

## Example Transformations

| Before | After |
|--------|-------|
| `老板，明天天气怎么样？` | `明天天气怎么样？` |
| `好的，我马上处理。` | `马上处理。` |
| `老板，那个事情已经好了。` | `那个事情已经好了。` |
| `老板，还有其他事吗？` | `还有别的事吗？` |

## Limitations

- Greeting detection is regex-based and may miss edge cases
- Topic change detection is heuristic, not perfect
- State is not shared across sessions
- No support for languages other than Chinese yet

## Future Improvements

- Use embedding similarity for topic detection
- Learn user preferences for greeting frequency
- Support multi-language
- Add tone adaptation (professional vs casual)