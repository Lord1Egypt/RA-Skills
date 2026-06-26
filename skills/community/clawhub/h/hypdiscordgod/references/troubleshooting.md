# Discord Bot Troubleshooting

## Bot Starts but Commands Do Not Appear

Check:
- correct `CLIENT_ID`
- command registration script ran
- registering to the correct guild/application
- enough time has passed for global sync if using global commands

## Bot Online but Events Do Not Fire

Check:
- required intents in code
- required intents in the Discord developer portal
- event file loaded correctly
- handler attached to the correct client instance

## Moderation Actions Fail

Check:
- bot permissions
- channel overrides
- target role above bot role
- invoker authorization
- guild ownership edge cases

## Interactions Fail with Unknown Interaction

Check:
- interaction was acknowledged fast enough
- duplicate reply/defer logic
- stale component IDs after restart

## Token or Login Errors

Check:
- correct token loaded
- no quotes/newlines in env value
- app token vs client secret confusion
