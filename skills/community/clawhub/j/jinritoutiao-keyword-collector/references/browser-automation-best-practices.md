# Browser Automation Best Practices

## Waiting Strategies

### Fixed Wait

Suitable for operations with known delays:

```
action: act
kind: wait
timeMs: 2000
```

### Conditional Wait

Wait for a specific element to appear or disappear:

```
action: act
kind: wait
textGone: Loading...
```

## Element Location

### Using ARIA References

```
action: snapshot
refs: aria
```

Advantages:
- More stable element identification
- Not affected by page structure changes
- Supports accessibility for elements

### Using Role References (Default)

```
action: snapshot
refs: role
```

Suitable for standard HTML elements.

## Input Optimization

### Slow Typing

Triggers autocomplete and dynamic loading:

```
action: act
kind: type
text: keyword
slowly: true
```

### Clear Input Field

Clear before re-entering:

```
action: act
ref: <input-ref>
kind: fill
fields: []
```

## Performance Optimization

### Maintain Session

Reuse the browser session for multiple operations:

1. Launch the browser for the first time
2. Use the same `targetId` for subsequent operations
3. Close all at the end

### Delay Requests

Avoid triggering anti-scraping mechanisms:

- Interval for single operations: 2-3 seconds
- Interval for batch operations: 5-10 seconds
- Avoid high-frequency access during peak hours

## Error Handling

### Timeout Settings

Increase timeout for long operations:

```
action: navigate
targetUrl: https://www.toutiao.com
timeoutMs: 30000
```

### Retry Strategy

Retry 2-3 times after failure:

1. Wait for 3 seconds
2. Refresh the page
3. Re-execute the operation

## Debugging Tips

### Screenshot Assistance

Take a screenshot when encountering problems:

```
action: screenshot
fullPage: true
```

### Console Logs

Check for page errors:

```
action: console
```