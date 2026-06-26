# Version Update: 1.0.0 → 1.0.1

## Update Summary
This document outlines the changes made to upgrade the pptx-master skill from version 1.0.0 to 1.0.1.

## Changes Made

### 1. Project Initialization Behavior
- **Changed**: Source content handling from MOVE to COPY
- **Previous**: Files were moved (`--move`) from original location to `sources/` directory
- **New**: Files are copied (`--copy`) to `sources/` directory, preserving original files
- **Impact**: Original source files now remain in their original location after import

### 2. Template Library Expansion
- **Added**: Two new layout templates - HUAWEI and red grey
- **Enhanced**: Template selection step to include new options
- **Updated**: Template recommendation flow to mention new options

### 3. Version Identification
- **Updated**: Description to reflect version 1.0.1
- **Added**: Reference to enhanced template options and source content handling

## Implementation Details

### Modified Sections
1. Step 2: Project Initialization - Updated file handling instruction
2. Step 3: Template Selection - Enhanced template recommendation flow
3. Header: Updated description to reflect version and enhancements

## Backward Compatibility
The changes maintain full backward compatibility:
- Existing workflows continue to function as before
- Only the source file handling behavior has changed (copy vs move)
- All existing templates remain available
- New templates are additional options

## Testing Recommendations
- Verify source files remain in original location after project initialization
- Test new HUAWEI and red grey template options
- Confirm all existing functionality remains intact