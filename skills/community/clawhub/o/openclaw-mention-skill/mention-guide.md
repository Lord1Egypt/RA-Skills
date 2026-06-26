# WhatsApp @Mention Guide

## How to @mention group members

When you need to @mention someone in a WhatsApp group, use their **LID** (WhatsApp internal ID).

### Format
```
@LID_NUMBER
```

Example: `@123456789012345` will create a blue clickable mention.

### DO NOT use:
- `@Name` (won't be blue)
- `@PhoneNumber` (won't be blue)

### Finding LIDs

Check the LID cache file for known members:
```
/home/openclaw/.openclaw/workspace/LID_CACHE.json
```

The `_names` section maps LID → display name.
The `_aliases` section maps alias → LID.

### Rules
1. Always use `@LID` format for mentions
2. The system automatically converts `@Name` to `@LID`, but direct LID is most reliable
3. If you don't know someone's LID, check the LID cache file
4. New members are auto-discovered when they send messages in a group
