# Today's Headlines Page Structure Description

## Homepage Elements

### Search Box

- **Location**: Top navigation bar of the page
- **Features**:
  - input element
  - placeholder contains the word "search"
  - usually accompanied by a search icon
- **ARIA Label**: may include keywords like "search" or "搜索"

### Search Suggestion Box

- **Trigger Condition**: After entering text in the search box
- **Location**: Directly below the search box
- **Element Type**:
  - div container
  - contains multiple li or div items
  - each item includes a suggested keyword
- **Delay**: Appears about 200-500ms after input

## Common Element Selectors

### Search Box Identification

Check in snapshot for:
- role: "searchbox"
- role: "textbox"
- name contains "搜索"
- placeholder contains "搜索"

### Suggestion Item Identification

Check in snapshot for:
- list items located below the search box
- role: "option" or role: "listitem"
- clickable elements containing text content

## Page Loading Characteristics

### First Screen Load

- Navigation bar: 1-2 seconds
- Recommended content: 2-4 seconds
- Fully loaded: 5-8 seconds

### Dynamic Loading

- Search suggestions: 200-500ms after input
- Search results: 1-3 seconds after submission
- Infinite scroll: 1-2 seconds after scrolling

## Anti-Scraping Mechanism

### Detection Features

- High-frequency requests
- Abnormal input speed
- No mouse movement traces

### Avoidance Suggestions

- Input using `slowly: true`
- 2-5 seconds intervals between operations
- Avoid a large number of requests in a short time
- Use a normal browser configuration profile

## Update Log

### Common Structure in 2024

```
Search box: input[aria-label*="搜索"]
Suggestion box: div.suggestion-list
Suggestion item: div.suggestion-item
```

**Note**: Page structure may update at any time; rely on real-time snapshots for actual operations.