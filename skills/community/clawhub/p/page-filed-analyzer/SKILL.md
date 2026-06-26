---
name: page-field-analyzer
description: Analyzes form fields on a live webpage using browser automation. Use when the user provides an online URL/link and wants to count and analyze form input fields on that page.
---

# Page Field Analyzer

Analyzes form fields on live webpages using browser automation.

## Usage

When the user provides an online URL, perform the following steps:

### Step 1: Navigate to the URL

```
Use mcp__browser-use__new_page to open the provided URL
```

### Step 2: Wait for Page Load

```
Wait for the page to fully load (use mcp__browser-use__wait_for if needed)
```

### Step 3: Take a Snapshot

```
Use mcp__browser-use__take_snapshot to get the page's accessibility tree
```

### Step 4: Analyze Form Fields

From the snapshot, identify and count these form field types:

#### Input Fields
- `input[type="text"]` - Text inputs
- `input[type="number"]` - Number inputs
- `input[type="email"]` - Email inputs
- `input[type="password"]` - Password inputs
- `input[type="tel"]` - Phone inputs
- `input[type="date"]` - Date inputs
- `input[type="file"]` - File uploads
- `input[type="checkbox"]` - Checkboxes
- `input[type="radio"]` - Radio buttons

#### Other Form Elements
- `select` - Dropdown selects
- `textarea` - Text areas
- `button[type="submit"]` - Submit buttons

#### UI Component Libraries (common patterns)
- Elements with role="textbox" - Input-like components
- Elements with role="combobox" - Select/autocomplete components
- Elements with role="listbox" - List selection components
- Elements with role="checkbox" - Checkbox components
- Elements with role="radio" - Radio components
- Elements with role="spinbutton" - Number picker components
- Elements with role="switch" - Toggle switches

### Step 5: Use JavaScript for Detailed Analysis (Optional)

If the snapshot doesn't provide enough detail, use `mcp__browser-use__evaluate_script` to run:

```javascript
() => {
  const fields = {
    inputs: document.querySelectorAll('input').length,
    textInputs: document.querySelectorAll('input[type="text"], input:not([type])').length,
    numberInputs: document.querySelectorAll('input[type="number"]').length,
    checkboxes: document.querySelectorAll('input[type="checkbox"]').length,
    radios: document.querySelectorAll('input[type="radio"]').length,
    selects: document.querySelectorAll('select').length,
    textareas: document.querySelectorAll('textarea').length,
    dateInputs: document.querySelectorAll('input[type="date"], input[type="datetime-local"]').length,
    fileInputs: document.querySelectorAll('input[type="file"]').length,
    // Ant Design / CN-UI specific
    antInputs: document.querySelectorAll('.ant-input, .cn-input').length,
    antSelects: document.querySelectorAll('.ant-select, .cn-select').length,
    antDatePickers: document.querySelectorAll('.ant-picker, .cn-date-picker').length,
    antCheckboxes: document.querySelectorAll('.ant-checkbox, .cn-checkbox').length,
    antRadios: document.querySelectorAll('.ant-radio, .cn-radio').length,
    antSwitches: document.querySelectorAll('.ant-switch, .cn-switch').length,
    antUploads: document.querySelectorAll('.ant-upload, .cn-upload').length,
    // Form items (containers)
    formItems: document.querySelectorAll('.ant-form-item, .cn-form-item, .next-form-item').length,
  };
  
  // Calculate total unique fields
  fields.totalFields = fields.formItems || (
    fields.textInputs + fields.numberInputs + fields.checkboxes + 
    fields.radios + fields.selects + fields.textareas + 
    fields.dateInputs + fields.fileInputs
  );
  
  return fields;
}
```

### Step 6: Output Results

Format the results as a markdown table:

```markdown
## Page Field Statistics: [Page URL]

### Form Fields Summary

| Field Type | Count |
|------------|-------|
| Text Inputs | X |
| Number Inputs | X |
| Selects/Dropdowns | X |
| Checkboxes | X |
| Radio Buttons | X |
| Date Pickers | X |
| File Uploads | X |
| Text Areas | X |
| Switches | X |

### Total
- **Total Form Fields**: X
- **Total Form Items/Groups**: X

### Notes
- [Any observations about the form structure]
```

## Example

User input:
```
https://example.com/form-page
```

Output:
```markdown
## Page Field Statistics: https://example.com/form-page

### Form Fields Summary

| Field Type | Count |
|------------|-------|
| Text Inputs | 12 |
| Number Inputs | 3 |
| Selects/Dropdowns | 8 |
| Checkboxes | 2 |
| Date Pickers | 4 |

### Total
- **Total Form Fields**: 29
- **Total Form Items/Groups**: 29
```

## Tips

1. If the page requires authentication, inform the user and ask them to log in first
2. For single-page applications (SPAs), wait for dynamic content to load
3. Some form fields may be hidden or in collapsed sections - consider expanding them
4. If the page has multiple tabs or sections, analyze each one separately if requested
