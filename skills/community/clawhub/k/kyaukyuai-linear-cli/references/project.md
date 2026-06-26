# project

> Manage Linear projects

## Usage

```
Usage:   linear project

Description:

  Manage Linear projects

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  

Commands:

  list                        - List projects                     
  view, v  <projectIdOrSlug>  - View project details              
  create                      - Create a new Linear project       
  update   <projectId>        - Update a Linear project           
  delete   <projectId>        - Delete (trash) a Linear project   
  label                       - Manage project labels on a project
```

## Subcommands

### list

> List projects

```
Usage:   linear project list

Description:

  List projects

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  --team           <team>     - Filter by team key                                                   
  --all-teams                 - Show projects from all teams                                         
  --status         <status>   - Filter by status name                                                
  -w, --web                   - Open in web browser                                                  
  -a, --app                   - Open in Linear.app                                                   
  -j, --json                  - Output as JSON                                                       
  --no-pager                  - Disable automatic paging for long output                             

Examples:

  List all projects as JSON        linear project list --all-teams --json         
  List started projects for a team linear project list --team ENG --status started
```

### view

> View project details

```
Usage:   linear project view <projectIdOrSlug>

Description:

  View project details

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  -w, --web                   - Open in web browser                                                  
  -a, --app                   - Open in Linear.app                                                   
  -j, --json                  - Force machine-readable JSON output                                   
  --text                      - Output human-readable text                                           

Examples:

  View a project as JSON         linear project view auth-refresh       
  View a project in the terminal linear project view auth-refresh --text
  Open a project in the browser  linear project view auth-refresh --web
```

### create

> Create a new Linear project

```
Usage:   linear project create

Description:

  Create a new Linear project

Options:

  -h, --help                        - Show this help.                                                          
  -w, --workspace    <slug>         - Target workspace (uses credentials)                                      
  --profile          <profile>      - Execution profile override (agent-safe default, human-debug opt-in)      
  -n, --name         <name>         - Project name (required)                                                  
  -d, --description  <description>  - Project description                                                      
  -t, --team         <team>         - Team key (required, can be repeated for multiple teams)                  
  -l, --lead         <lead>         - Project lead (username, email, or @me)                                   
  -s, --status       <status>       - Project status (planned, started, paused, completed, canceled, backlog)  
  --start-date       <startDate>    - Start date (YYYY-MM-DD)                                                  
  --target-date      <targetDate>   - Target completion date (YYYY-MM-DD)                                      
  --initiative       <initiative>   - Add to initiative immediately (ID, slug, or name)                        
  -i, --interactive                 - Enable interactive prompts                                               
  -j, --json                        - Output created project as JSON                                           
  --dry-run                         - Preview the project without creating it                                  

Examples:

  Create a project as JSON linear project create --name "Auth refresh" --team ENG --json                    
  Preview project creation linear project create --name "Auth refresh" --team ENG --status planned --dry-run
```

### update

> Update a Linear project

```
Usage:   linear project update <projectId>

Description:

  Update a Linear project

Options:

  -h, --help                        - Show this help.                                                      
  -w, --workspace    <slug>         - Target workspace (uses credentials)                                  
  --profile          <profile>      - Execution profile override (agent-safe default, human-debug opt-in)  
  -n, --name         <name>         - Project name                                                         
  -d, --description  <description>  - Project description                                                  
  -s, --status       <status>       - Status (planned, started, paused, completed, canceled, backlog)      
  -l, --lead         <lead>         - Project lead (username, email, or @me)                               
  --start-date       <startDate>    - Start date (YYYY-MM-DD)                                              
  --target-date      <targetDate>   - Target date (YYYY-MM-DD)                                             
  -t, --team         <team>         - Team key (can be repeated for multiple teams)                        
  --dry-run                         - Preview the update without mutating the project                      

Examples:

  Update status and target date linear project update auth-refresh --status started --target-date 2026-04-30
  Preview team changes          linear project update auth-refresh --team ENG --team PLATFORM --dry-run
```

### delete

> Delete (trash) a Linear project

```
Usage:   linear project delete <projectId>

Description:

  Delete (trash) a Linear project

Options:

  -h, --help                    - Show this help.                                                      
  -w, --workspace    <slug>     - Target workspace (uses credentials)                                  
  --profile          <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  -i, --interactive             - Enable interactive confirmation                                      
  -y, --yes                     - Skip confirmation prompt                                             
  -f, --force                   - Deprecated alias for --yes                                           
  --dry-run                     - Preview the deletion without mutating the project                    

Examples:

  Preview deleting a project         linear project delete auth-refresh --dry-run
  Delete a project without prompting linear project delete auth-refresh --yes
```

### label

> Manage project labels on a project

```
Usage:   linear project label

Description:

  Manage project labels on a project

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  

Commands:

  add     <projectId> <label>  - Add a label to a project     
  remove  <projectId> <label>  - Remove a label from a project
```

#### label subcommands

##### add

```
Usage:   linear project label add <projectId> <label>

Description:

  Add a label to a project

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  -j, --json                  - Output as JSON                                                       

Examples:

  Add a project label linear project label add auth-redesign bug
```

##### remove

```
Usage:   linear project label remove <projectId> <label>

Description:

  Remove a label from a project

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  -j, --json                  - Output as JSON                                                       

Examples:

  Remove a project label linear project label remove auth-redesign bug
```
