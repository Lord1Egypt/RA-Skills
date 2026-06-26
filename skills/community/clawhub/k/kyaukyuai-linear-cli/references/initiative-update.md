# initiative-update

> Manage initiative status updates (timeline posts)

## Usage

```
Usage:   linear initiative-update

Description:

  Manage initiative status updates (timeline posts)

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  

Commands:

  create, c    <initiativeId>  - Create a new status update for an initiative
  list, l, ls  <initiativeId>  - List status updates for an initiative
```

## Subcommands

### create

> Create a new status update for an initiative

```
Usage:   linear initiative-update create <initiativeId>

Description:

  Create a new status update for an initiative

Options:

  -h, --help                    - Show this help.                                                      
  -w, --workspace    <slug>     - Target workspace (uses credentials)                                  
  --profile          <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  --body             <body>     - Update content (markdown)                                            
  --body-file        <path>     - Read content from file                                               
  --health           <health>   - Health status (onTrack, atRisk, offTrack)                            
  -i, --interactive             - Interactive mode with prompts
```

### list

> List status updates for an initiative

```
Usage:   linear initiative-update list <initiativeId>

Description:

  List status updates for an initiative

Options:

  -h, --help                  - Show this help.                                                                   
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                               
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)               
  -j, --json                  - Output as JSON                                                                    
  --limit          <limit>    - Limit results                                                        (Default: 10)
  --no-pager                  - Disable automatic paging for long output                                          

Examples:

  List initiative updates as JSON linear initiative-update list initiative-slug --json
```
