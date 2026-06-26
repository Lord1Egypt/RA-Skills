# Test Document

This is a test markdown file with some issues.

## Missing Image Alt Text

![](https://example.com/image.png)

## Line Length

This line is way too long and should trigger the line length warning because it exceeds the default 80 characters limit by quite a bit.

## Trailing Whitespace

This line has trailing spaces.   

## Inconsistent List

- Item 1
* Item 2
- Item 3

## Code Block Without Language

```
print("hello")
```

## Empty Link

[Empty URL]()
[Empty text](https://example.com)

## Duplicate Header

# Test Document

## Internal Link

[Link to non-existent anchor](#nonexistent)

## External Link

[Good link](https://httpbin.org/status/200)
[Bad link](https://httpbin.org/status/404)