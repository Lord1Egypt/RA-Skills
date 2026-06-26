# workflow-state

> Manage Linear workflow states

## Usage

```
Usage:   linear workflow-state

Description:

  Manage Linear workflow states

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  

Commands:

  list                     - List workflow states for a team
  view  <workflowStateId>  - View a workflow state
```

## Subcommands

### list

> List workflow states for a team

```
Usage:   linear workflow-state list

Description:

  List workflow states for a team

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  --team           <teamKey>  - Team key (defaults to current team)                                  
  -j, --json                  - Output as JSON                                                       
  --no-pager                  - Disable automatic paging for long output                             

Examples:

  List workflow states as JSON linear workflow-state list --team ENG --json
```

### view

> View a workflow state

```
Usage:   linear workflow-state view <workflowStateId>

Description:

  View a workflow state

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  -j, --json                  - Output as JSON                                                       

Examples:

  View a workflow state as JSON linear workflow-state view state-123 --json
```
