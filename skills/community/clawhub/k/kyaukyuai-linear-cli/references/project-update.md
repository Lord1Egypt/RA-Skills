# project-update

> Manage project status updates

## Usage

```
Usage:   linear project-update

Description:

  Manage project status updates

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  

Commands:

  create, c  <projectId>  - Create a new status update for a project
  list, l    <projectId>  - List status updates for a project
```

## Subcommands

### create

> Create a new status update for a project

```
Usage:   linear project-update create <projectId>

Description:

  Create a new status update for a project

Options:

  -h, --help                    - Show this help.                                                      
  -w, --workspace    <slug>     - Target workspace (uses credentials)                                  
  --profile          <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  --body             <body>     - Update content (inline)                                              
  --body-file        <path>     - Read content from file                                               
  --health           <health>   - Project health status (onTrack, atRisk, offTrack)                    
  -i, --interactive             - Interactive mode with prompts
```

### list

> List status updates for a project

```
Usage:   linear project-update list <projectId>

Description:

  List status updates for a project

Options:

  -h, --help                  - Show this help.                                                                   
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                               
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)               
  --json                      - Output as JSON                                                                    
  --limit          <limit>    - Limit results                                                        (Default: 10)
  --no-pager                  - Disable automatic paging for long output                                          

Examples:

  List project updates as JSON linear project-update list project-slug --json
```
