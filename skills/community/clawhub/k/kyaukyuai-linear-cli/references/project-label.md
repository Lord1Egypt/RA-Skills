# project-label

> Manage Linear project labels

## Usage

```
Usage:   linear project-label

Description:

  Manage Linear project labels

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  

Commands:

  list  - List project labels
```

## Subcommands

### list

> List project labels

```
Usage:   linear project-label list

Description:

  List project labels

Options:

  -h, --help                     - Show this help.                                                                   
  -w, --workspace     <slug>     - Target workspace (uses credentials)                                               
  --profile           <profile>  - Execution profile override (agent-safe default, human-debug opt-in)               
  -n, --limit         <limit>    - Maximum number of project labels                                     (Default: 50)
  --include-archived             - Include archived project labels                                                   
  -j, --json                     - Output as JSON                                                                    
  --no-pager                     - Disable automatic paging for long output                                          

Examples:

  List project labels as JSON linear project-label list --json
```
