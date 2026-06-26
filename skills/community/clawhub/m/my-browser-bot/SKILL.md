---
name: mybrowser-skill
description: Browser automation CLI for AI agents. Use when the user needs to interact with websites, including navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, or automating any browser task. 
---

# mybrowser-skill

## Platform Support

- **Linux x86_64**: Supported
- **macOS**: Not supported
- **Windows**: Not supported
- Other Linux architectures (ARM, etc.) are not supported.

## Installation
```bash
pipx install mybrowser-skill
mybrowser-skill install   # Download Chromium
```

## Note:
   Each command will return a snapshot of the current page after execution, including the index of elements.
 Please call the standalone mybrowser-skill browser_snapshot command only when necessary to avoid unnecessary token consumption.

## Core Workflow

Every browser automation follows this pattern:

1. **Navigate**: `mybrowser-skill browser_go_to_url --url <url>`
2. **Snapshot**: `mybrowser-skill browser_snapshot` (get indexed element refs)
3. **Interact**: Use element index to click, fill, select
4. **Re-snapshot**: After navigation or DOM changes, get fresh refs

```bash
mybrowser-skill browser_go_to_url --url https://example.com/form
mybrowser-skill browser_snapshot
# Output includes element indices: [1] input "email", [2] input "password", [3] button "Submit"

mybrowser-skill browser_input_text --index 1 --text "user@example.com"
mybrowser-skill browser_input_text --index 2 --text "password123"
mybrowser-skill browser_click_element --index 3
mybrowser-skill browser_wait --seconds 2
mybrowser-skill browser_snapshot  # Check result
```

## Essential Commands

```bash
# Navigation
mybrowser-skill browser_go_to_url --url <url>       # Navigate to URL
mybrowser-skill browser_go_back                      # Go back
mybrowser-skill browser_wait --seconds 3             # Wait for page load (default 3s)

# Snapshot & Screenshot
mybrowser-skill browser_snapshot                     # Get page content with element indices
mybrowser-skill browser_screenshot                   # Take screenshot (returns temp file path of .webp image)
mybrowser-skill browser_screenshot --full            # Full-page screenshot (returns temp file path)
mybrowser-skill browser_screenshot --annotate        # Annotated screenshot with element labels (returns temp file path)
mybrowser-skill browser_markdownify                  # Convert page to markdown

# Click & Input (use indices from snapshot)
mybrowser-skill browser_click_element --index 1      # Click element
mybrowser-skill browser_dblclick_element --index 1   # Double-click element
mybrowser-skill browser_focus_element --index 1      # Focus element
mybrowser-skill browser_input_text --index 1 --text "hello"  # Input text into element

# Scroll
mybrowser-skill browser_scroll_down                  # Scroll down one page
mybrowser-skill browser_scroll_down --amount 300     # Scroll down 300px
mybrowser-skill browser_scroll_up                    # Scroll up one page
mybrowser-skill browser_scroll_up --amount 300       # Scroll up 300px
mybrowser-skill browser_scroll_to_text --text "Section 3"    # Scroll to text
mybrowser-skill browser_scroll_to_top                # Scroll to top
mybrowser-skill browser_scroll_to_bottom             # Scroll to bottom
mybrowser-skill browser_scroll_by --direction down --pixels 500              # Scroll page by direction
mybrowser-skill browser_scroll_by --direction right --pixels 200 --index 3   # Scroll element by direction
mybrowser-skill browser_scroll_into_view --index 5   # Scroll element into view

# Keyboard
mybrowser-skill browser_keypress --key Enter         # Press a key
mybrowser-skill browser_keyboard_op --action type --text "hello"        # Type text
mybrowser-skill browser_keyboard_op --action inserttext --text "hello"  # Insert text without key events
mybrowser-skill browser_keydown --key Shift          # Hold down a key
mybrowser-skill browser_keyup --key Shift            # Release a key

# Dropdown
mybrowser-skill browser_get_dropdown_options --index 2           # Get dropdown options
mybrowser-skill browser_select_dropdown_option --index 2 --text "Option A"  # Select option

# Checkbox
mybrowser-skill browser_check_op --index 4 --value               # Check checkbox
mybrowser-skill browser_check_op --index 4                        # Uncheck checkbox (omit --value)

# Get Information
mybrowser-skill browser_get_info --type text --index 1   # Get element text
mybrowser-skill browser_get_info --type url              # Get current URL
mybrowser-skill browser_get_info --type title            # Get page title
mybrowser-skill browser_get_info --type html --index 1   # Get element HTML
mybrowser-skill browser_get_info --type value --index 1  # Get element value
mybrowser-skill browser_get_info --type attr --index 1 --attribute href   # Get attribute
mybrowser-skill browser_get_info --type count            # Get element count
mybrowser-skill browser_get_info --type box --index 1    # Get bounding box
mybrowser-skill browser_get_info --type styles --index 1 # Get computed styles
mybrowser-skill browser_check_state --state visible --index 1    # Check visibility
mybrowser-skill browser_check_state --state enabled --index 1    # Check if enabled
mybrowser-skill browser_check_state --state checked --index 1    # Check if checked

# Find and Act (semantic locators)
mybrowser-skill browser_find_and_act --by role --value button --action click --name "Submit"
mybrowser-skill browser_find_and_act --by text --value "Sign In" --action click
mybrowser-skill browser_find_and_act --by label --value "Email" --action fill --actionValue "user@test.com"
mybrowser-skill browser_find_and_act --by placeholder --value "Search" --action type --actionValue "query"
mybrowser-skill browser_find_and_act --by testid --value "submit-btn" --action click

# Download
mybrowser-skill browser_download_file --index 5      # Download file by clicking element
mybrowser-skill browser_download_url                 # Download from URL

# Tab Management
mybrowser-skill browser_tab_open --url <url>         # Open URL in new tab
mybrowser-skill browser_tab_list                     # List open tabs
mybrowser-skill browser_tab_switch --tabId 2         # Switch to tab
mybrowser-skill browser_tab_close --tabId 2          # Close tab

# Dialog
mybrowser-skill browser_dialog --action accept       # Accept dialog
mybrowser-skill browser_dialog --action dismiss      # Dismiss dialog
mybrowser-skill browser_dialog --action accept --text "input text"  # Accept prompt with text

# Task Completion
mybrowser-skill browser_done --success --text "Task completed"      # Mark task as done
mybrowser-skill browser_done --text "Still in progress"              # Mark task as incomplete

# Help
mybrowser-skill list                                 # List all available skills
mybrowser-skill <skill_name> --help                  # Show help for a specific skill

# Skill Status 
mybrowser-skill status                               # Check status

```

## Common Patterns

### Form Submission

```bash
mybrowser-skill browser_go_to_url --url https://example.com/signup
mybrowser-skill browser_snapshot
mybrowser-skill browser_input_text --index 1 --text "Jane Doe"
mybrowser-skill browser_input_text --index 2 --text "jane@example.com"
mybrowser-skill browser_select_dropdown_option --index 3 --text "California"
mybrowser-skill browser_check_op --index 4 --value
mybrowser-skill browser_click_element --index 5
mybrowser-skill browser_wait --seconds 2
mybrowser-skill browser_snapshot  # Verify result
```

### Data Extraction

```bash
mybrowser-skill browser_go_to_url --url https://example.com/products
mybrowser-skill browser_snapshot
mybrowser-skill browser_get_info --type text --index 5    # Get specific element text
mybrowser-skill browser_markdownify                        # Get full page as markdown
```

### Infinite Scroll Pages

```bash
mybrowser-skill browser_go_to_url --url https://example.com/feed
mybrowser-skill browser_scroll_to_bottom     # Trigger lazy loading
mybrowser-skill browser_wait --seconds 2     # Wait for content
mybrowser-skill browser_snapshot             # Get updated content
```

## Element Index Lifecycle (Important)

Element indices are invalidated when the page changes. Always re-snapshot after:

- Clicking links or buttons that navigate
- Form submissions
- Dynamic content loading (dropdowns, modals, AJAX)

```bash
mybrowser-skill browser_click_element --index 5   # May navigate to new page
mybrowser-skill browser_snapshot                   # MUST re-snapshot
mybrowser-skill browser_click_element --index 1   # Use new indices
```