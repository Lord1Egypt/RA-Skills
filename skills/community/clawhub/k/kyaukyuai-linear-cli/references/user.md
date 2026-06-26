# user

> Manage Linear users

## Usage

```
Usage:   linear user

Description:

  Manage Linear users

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  

Commands:

  list            - List users in the workspace
  view  <userId>  - View a user
```

## Subcommands

### list

> List users in the workspace

```
Usage:   linear user list

Description:

  List users in the workspace

Options:

  -h, --help                  - Show this help.                                                                   
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                               
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)               
  -n, --limit      <limit>    - Maximum number of users                                              (Default: 50)
  -a, --all                   - Include disabled users                                                            
  -j, --json                  - Output as JSON                                                                    
  --no-pager                  - Disable automatic paging for long output                                          

Examples:

  List users as JSON linear user list --json
```

### view

> View a user

```
Usage:   linear user view <userId>

Description:

  View a user

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  -j, --json                  - Output as JSON                                                       

Examples:

  View a user as JSON linear user view user-123 --json
```
