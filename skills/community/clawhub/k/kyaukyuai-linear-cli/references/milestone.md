# milestone

> Manage Linear project milestones

## Usage

```
Usage:   linear milestone

Description:

  Manage Linear project milestones

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  

Commands:

  list                    - List milestones for a project       
  view, v  <milestoneId>  - View milestone details              
  create                  - Create a new project milestone      
  update   <id>           - Update an existing project milestone
  delete   <id>           - Delete a project milestone
```

## Subcommands

### list

> List milestones for a project

```
Usage:   linear milestone list --project <projectId>

Description:

  List milestones for a project

Options:

  -h, --help                    - Show this help.                                                                
  -w, --workspace  <slug>       - Target workspace (uses credentials)                                            
  --profile        <profile>    - Execution profile override (agent-safe default, human-debug opt-in)            
  --project        <projectId>  - Project ID                                                           (required)
  -j, --json                    - Output as JSON                                                                 
  --no-pager                    - Disable automatic paging for long output                                       

Examples:

  List milestones as JSON         linear milestone list --project auth-refresh --json    
  List milestones without a pager linear milestone list --project auth-refresh --no-pager
```

### view

> View milestone details

```
Usage:   linear milestone view <milestoneId>

Description:

  View milestone details

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  -j, --json                  - Output as JSON                                                       

Examples:

  View a milestone as JSON         linear milestone view milestone-123 --json
  View a milestone in the terminal linear milestone view milestone-123
```

### create

> Create a new project milestone

```
Usage:   linear milestone create --project <projectId> --name <name>

Description:

  Create a new project milestone

Options:

  -h, --help                      - Show this help.                                                                
  -w, --workspace  <slug>         - Target workspace (uses credentials)                                            
  --profile        <profile>      - Execution profile override (agent-safe default, human-debug opt-in)            
  --project        <projectId>    - Project ID                                                           (required)
  --name           <name>         - Milestone name                                                       (required)
  --description    <description>  - Milestone description                                                          
  --target-date    <date>         - Target date (YYYY-MM-DD)                                                       
  --dry-run                       - Preview the milestone without creating it                                      

Examples:

  Create a milestone         linear milestone create --project auth-refresh --name "Beta launch"                                   
  Preview milestone creation linear milestone create --project auth-refresh --name "Beta launch" --target-date 2026-05-01 --dry-run
```

### update

> Update an existing project milestone

```
Usage:   linear milestone update <id>

Description:

  Update an existing project milestone

Options:

  -h, --help                      - Show this help.                                                      
  -w, --workspace  <slug>         - Target workspace (uses credentials)                                  
  --profile        <profile>      - Execution profile override (agent-safe default, human-debug opt-in)  
  --name           <name>         - Milestone name                                                       
  --description    <description>  - Milestone description                                                
  --target-date    <date>         - Target date (YYYY-MM-DD)                                             
  --sort-order     <value>        - Sort order relative to other milestones                              
  --project        <projectId>    - Move to a different project                                          
  --dry-run                       - Preview the update without mutating the milestone                    

Examples:

  Rename a milestone              linear milestone update milestone-123 --name "GA launch"                
  Preview a milestone date change linear milestone update milestone-123 --target-date 2026-05-15 --dry-run
```

### delete

> Delete a project milestone

```
Usage:   linear milestone delete <id>

Description:

  Delete a project milestone

Options:

  -h, --help                    - Show this help.                                                      
  -w, --workspace    <slug>     - Target workspace (uses credentials)                                  
  --profile          <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  -i, --interactive             - Enable interactive confirmation                                      
  -y, --yes                     - Skip confirmation prompt                                             
  -f, --force                   - Deprecated alias for --yes                                           
  --dry-run                     - Preview the deletion without mutating the milestone                  

Examples:

  Preview deleting a milestone         linear milestone delete milestone-123 --dry-run
  Delete a milestone without prompting linear milestone delete milestone-123 --yes
```
