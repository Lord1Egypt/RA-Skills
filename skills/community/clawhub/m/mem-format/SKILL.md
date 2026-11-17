---
name: mem-format
description: Memory Bank Template Compliance Cleaner Workflow Use when the user invokes $mem-format or asks for this workflow by name.
---

# mem-format

This skill is a Codex conversion of a personal Windsurf global workflow. Follow the workflow below, adapting Windsurf-specific slash-command wording to Codex skill invocation. If the workflow mentions running `/mem-format`, treat that as explicit invocation of `$mem-format`.

The mem-format workflow scans memory bank files and revises them to conform to established templates. This ensures consistency across all memory bank documentation and maintains proper formatting standards.

## Usage

Run this workflow to:
1. Clean specific files: `/mem-format [file1.md] [file2.md]`
2. Clean entire memory bank: `/mem-format all`
3. Clean by category: `/mem-format tasks` or `/mem-format sessions`

## Workflow Steps

### Step 1: Scan Target Files
// turbo
Identify files to be processed based on user input:
- Specific files provided as arguments
- Entire memory bank if "all" specified
- Category-based filtering (tasks, sessions, etc.)

### Step 2: Template Matching
// turbo
For each file, determine the appropriate template:
- Task files (T*.md in tasks/ directory) → task-template.md
- Session files (YYYY-MM-DD-*.md in sessions/ directory) → session-template.md
- Core registry files (tasks.md, session_cache.md) → corresponding templates
- Edit history files → edit_history.md template
- Implementation details → flexible template matching

### Step 3: Compliance Analysis
// turbo
Analyze each file against its template:
- Check required sections presence
- Validate section order and formatting
- Verify timestamp formats (YYYY-MM-DD HH:MM:SS TZ)
- Check for proper markdown structure
- Identify missing or malformed content

### Step 4: Content Extraction
// turbo
Extract existing content from files:
- Preserve actual data and information
- Identify template placeholders vs real content
- Extract task metadata (ID, status, dates, etc.)
- Preserve implementation details and progress notes
- Maintain relationships and dependencies

### Step 5: Template Application
// turbo
Reconstruct files using proper templates:
- Apply correct template structure
- Insert extracted content into appropriate sections
- Ensure proper section ordering
- Fix formatting and markdown issues
- Standardize timestamp formats
- Add missing required sections

### Step 6: Validation
// turbo
Validate revised files:
- Check all required sections present
- Verify markdown syntax correctness
- Ensure internal consistency
- Validate links and references
- Check for template remnants (placeholders)

### Step 7: Report Generation
// turbo
Generate comprehensive report:
- List of files processed
- Issues found and fixed
- Template compliance status
- Any manual review needed
- Summary statistics

## Template Mapping

| File Pattern | Template | Target Directory |
|-------------|----------|------------------|
| tasks/T*.md | task-template.md | tasks/ |
| sessions/YYYY-MM-DD-*.md | session-template.md | sessions/ |
| tasks.md | tasks.md | memory-bank/ |
| session_cache.md | session_cache.md | memory-bank/ |
| edit_history.md | edit_history.md | memory-bank/ |
| activeContext.md | activeContext.md | memory-bank/ |
| errorLog.md | errorLog.md | memory-bank/ |
| progress.md | progress.md | memory-bank/ |

## Common Issues Fixed

### 1. Missing Required Sections
- Add missing template sections
- Preserve existing content structure
- Use proper section headers (##, ###)

### 2. Incorrect Timestamp Formats
- Convert to YYYY-MM-DD HH:MM:SS TZ format
- Include timezone information
- Ensure consistency across all timestamps

### 3. Malformed Task Metadata
- Standardize task ID formats (T1, T2, etc.)
- Fix status icons (🔄, ⏸️, ✅)
- Ensure priority levels (HIGH, MEDIUM, LOW)

### 4. Section Order Issues
- Reorder sections to match template
- Maintain content integrity
- Preserve logical flow

### 5. Markdown Formatting
- Fix header levels
- Correct list formatting
- Ensure proper table structure

## Safety Measures

### 1. Backup Creation
// turbo
Before modifying files, create backups:
- Copy original files to backup location
- Timestamp backup directories
- Maintain change history

### 2. Content Preservation
// turbo
Ensure no content loss:
- Extract all existing data before restructuring
- Verify content integrity after revision
- Manual review for complex cases

### 3. Progressive Application
// turbo
Apply changes incrementally:
- Process one file at a time
- Validate each change
- Rollback capability for errors

## Implementation Notes

### Template Detection Algorithm
```typescript
function detectTemplate(filePath: string): string {
  if (filePath.includes('tasks/T') && filePath.endsWith('.md')) {
    return 'task-template.md';
  }
  if (filePath.includes('sessions/') && /^\d{4}-\d{2}-\d{2}/.test(filePath)) {
    return 'session-template.md';
  }
  // ... other patterns
  return 'default-template.md';
}
```

### Content Extraction Strategy
```typescript
function extractContent(fileContent: string, template: string): Record<string, string> {
  const sections = parseTemplateSections(template);
  const extracted = {};
  
  sections.forEach(section => {
    extracted[section] = findSectionContent(fileContent, section);
  });
  
  return extracted;
}
```

### Template Application Process
```typescript
function applyTemplate(template: string, extractedContent: Record<string, string>): string {
  let result = template;
  
  Object.entries(extractedContent).forEach(([section, content]) => {
    result = result.replace(`[${section.toUpperCase()}]`, content || '');
  });
  
  return result;
}
```

## Quality Assurance

### Automated Checks
- Markdown syntax validation
- Required section presence
- Timestamp format verification
- Link integrity checking

### Manual Review Triggers
- Complex content structures
- Large file size (>50KB)
- Multiple template conflicts
- Unusual file patterns

### Success Criteria
- All files match their respective templates
- No content loss during restructuring
- Proper formatting throughout
- Consistent metadata presentation

## Troubleshooting

### Common Issues
1. **Template Not Found**: Use default template for unknown file types
2. **Content Loss**: Restore from backup and retry with manual review
3. **Format Conflicts**: Prioritize existing content over strict template compliance
4. **Large Files**: Process in chunks to avoid memory issues

### Error Handling
- Graceful degradation for template mismatches
- Detailed logging of all transformations
- Rollback capability for failed operations
- Manual intervention flags for complex cases

## Maintenance

### Regular Updates
- Update template mappings as new templates are added
- Refine detection algorithms based on usage patterns
- Enhance content extraction logic for edge cases

### Template Evolution
- Version templates for backward compatibility
- Migration paths for template changes
- Documentation of template modifications

This workflow ensures memory bank files maintain consistent structure and formatting while preserving all valuable content and implementation details.
