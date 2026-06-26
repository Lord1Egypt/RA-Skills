---
name: mouse-keyboard
description: Control mouse and keyboard on Mac using cliclick. Use when you need to automate clicking, typing, or controlling the mouse cursor.
---

# Mouse & Keyboard Control

Use `cliclick` tool for mouse/keyboard automation on Mac.

## Tools

### exec

Use `exec` to run cliclick commands.

## Available Commands

- `c:X,Y` - Click at coordinates X,Y
- `c:~100,~200` - Click at relative position
- `w:500` - Wait 500ms
- `t:hello` - Type "hello"
- `kd:cmd` - Key down command
- `ku:cmd` - Key up command
- `p:return` - Press return/enter
- `p:space` - Press space
- `p:tab` - Press tab
- `m:X,Y` - Move mouse to X,Y
- `dp` - Double click
- `rc:X,Y` - Right click at X,Y

## Common Workflows

### Click at position
```bash
cliclick c:500,300
```

### Type text
```bash
cliclick t:Hello World
```

### Click and type
```bash
cliclick c:500,300 && cliclick t:username
```

### Keyboard shortcut
```bash
cliclick kd:cmd ku:cmd  # Press cmd
```

### Move and click
```bash
cliclick m:100,100 && cliclick c:100,100
```

## Getting Coordinates

Use `cliclick p` to print current mouse position, or use macOS screenshot tool (Shift+Cmd+4) to get coordinates.

## Notes

- Coordinates are screen-based (0,0 is top-left)
- Use `osascript` for more complex keyboard operations
- Combine with `sleep` for timing
