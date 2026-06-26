# cycle

> Manage Linear team cycles

## Usage

```
Usage:   linear cycle

Description:

  Manage Linear team cycles

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  

Commands:

  list                 - List cycles for a team                  
  view, v  <cycleRef>  - View cycle details                      
  current              - Show the current active cycle for a team
  next                 - Show the next upcoming cycle for a team 
  create               - Create a new cycle                      
  add      <issueId>   - Add an issue to a cycle                 
  remove   <issueId>   - Remove an issue from its cycle
```

## Subcommands

### list

> List cycles for a team

```
Usage:   linear cycle list

Description:

  List cycles for a team

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  --team           <team>     - Team key (defaults to current team)                                  
  -j, --json                  - Output as JSON                                                       
  --no-pager                  - Disable automatic paging for long output                             

Examples:

  List cycles as JSON         linear cycle list --team ENG --json    
  List cycles without a pager linear cycle list --team ENG --no-pager
```

### view

> View cycle details

```
Usage:   linear cycle view <cycleRef>

Description:

  View cycle details

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  --team           <team>     - Team key (defaults to current team)                                  
  -j, --json                  - Output as JSON                                                       

Examples:

  View a cycle as JSON linear cycle view 42 --team ENG --json 
  View a cycle by name linear cycle view "Cycle 42" --team ENG
```

### current

> Show the current active cycle for a team

```
Usage:   linear cycle current

Description:

  Show the current active cycle for a team

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  --team           <team>     - Team key (defaults to current team)                                  
  -j, --json                  - Force machine-readable JSON output                                   
  --text                      - Output human-readable text                                           

Examples:

  Show the current cycle as JSON         linear cycle current --team ENG       
  Show the current cycle in the terminal linear cycle current --team ENG --text
```

### next

> Show the next upcoming cycle for a team

```
Usage:   linear cycle next

Description:

  Show the next upcoming cycle for a team

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  --team           <team>     - Team key (defaults to current team)                                  
  -j, --json                  - Output as JSON                                                       

Examples:

  Show the next cycle as JSON              linear cycle next --team ENG --json
  Show the next cycle for the default team linear cycle next
```

### create

> Create a new cycle

```
Usage:   linear cycle create --starts <date> --ends <date>

Description:

  Create a new cycle

Options:

  -h, --help                      - Show this help.                                                                
  -w, --workspace  <slug>         - Target workspace (uses credentials)                                            
  --profile        <profile>      - Execution profile override (agent-safe default, human-debug opt-in)            
  --team           <team>         - Team key (defaults to current team)                                            
  --name           <name>         - Custom name for the cycle                                                      
  --description    <description>  - Description of the cycle                                                       
  --starts         <date>         - Start date (YYYY-MM-DD)                                              (required)
  --ends           <date>         - End date (YYYY-MM-DD)                                                (required)

Examples:

  Create 2-week cycle linear cycle create --starts 2026-01-15 --ends 2026-01-29                   
  Create named cycle  linear cycle create --starts 2026-01-15 --ends 2026-01-29 --name 'Sprint 10'
```

### add

> Add an issue to a cycle

```
Usage:   linear cycle add <issueId>

Description:

  Add an issue to a cycle

Options:

  -h, --help                  - Show this help.                                                                         
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                                     
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)                     
  --team           <team>     - Team key (defaults to current team)                                                     
  --cycle          <cycle>    - Cycle name or number (defaults to active cycle)                      (Default: "active")
```

### remove

> Remove an issue from its cycle

```
Usage:   linear cycle remove <issueId>

Description:

  Remove an issue from its cycle

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)
```
