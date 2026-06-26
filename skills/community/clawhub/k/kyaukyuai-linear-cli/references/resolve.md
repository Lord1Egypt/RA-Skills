# resolve

> Resolve references without mutating Linear

## Usage

```
Usage:   linear resolve

Description:

  Resolve references without mutating Linear

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  

Commands:

  issue           [issue]  - Resolve an issue reference without mutating Linear         
  team            [team]   - Resolve a team reference without mutating Linear           
  workflow-state  <state>  - Resolve a workflow state reference without mutating Linear 
  user            <user>   - Resolve a user reference without mutating Linear           
  pack                     - Resolve a multi-entity context pack without mutating Linear
  label           <label>  - Resolve an issue label reference without mutating Linear
```

## Subcommands

### issue

> Resolve an issue reference without mutating Linear

```
Usage:   linear resolve issue [issue]

Description:

  Resolve an issue reference without mutating Linear

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  -j, --json                  - Force machine-readable JSON output                                   
  --text                      - Output human-readable text                                           

Examples:

  Resolve an explicit issue identifier       linear resolve issue ENG-123
  Resolve the current issue from VCS context linear resolve issue
```

### team

> Resolve a team reference without mutating Linear

```
Usage:   linear resolve team [team]

Description:

  Resolve a team reference without mutating Linear

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  -j, --json                  - Force machine-readable JSON output                                   
  --text                      - Output human-readable text                                           

Examples:

  Resolve an explicit team key        linear resolve team ENG
  Resolve the configured current team linear resolve team
```

### workflow-state

> Resolve a workflow state reference without mutating Linear

```
Usage:   linear resolve workflow-state <state>

Description:

  Resolve a workflow state reference without mutating Linear

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  --team           <team>     - Team key for team-scoped resolution                                  
  -j, --json                  - Force machine-readable JSON output                                   
  --text                      - Output human-readable text                                           

Examples:

  Resolve a workflow state by exact name linear resolve workflow-state Done --team ENG   
  Resolve a workflow state by type       linear resolve workflow-state started --team ENG
```

### user

> Resolve a user reference without mutating Linear

```
Usage:   linear resolve user <user>

Description:

  Resolve a user reference without mutating Linear

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  -j, --json                  - Force machine-readable JSON output                                   
  --text                      - Output human-readable text                                           

Examples:

  Resolve the current authenticated user      linear resolve user self             
  Resolve a teammate by email or display name linear resolve user alice@example.com
```

### pack

> Resolve a multi-entity context pack without mutating Linear

```
Usage:   linear resolve pack

Description:

  Resolve a multi-entity context pack without mutating Linear

Options:

  -h, --help                   - Show this help.                                                      
  -w, --workspace   <slug>     - Target workspace (uses credentials)                                  
  --profile         <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  --issue           <issue>    - Issue identifier or numeric issue ref                                
  --team            <team>     - Team key for explicit team context                                   
  --workflow-state  <state>    - Workflow state name, type, or ID within the active team context      
  --user            <user>     - User email, display name, or self                                    
  --project         <project>  - Project ID or slug                                                   
  --label           <label>    - Issue label name. May be repeated.                                   
  -j, --json                   - Force machine-readable JSON output                                   
  --text                       - Output human-readable text                                           

Examples:

  Resolve an issue-scoped pack for triage planning linear resolve pack --issue ENG-123 --workflow-state started --label Bug --json
  Resolve a user and project pack                  linear resolve pack --user self --project auth-refresh --json
```

### label

> Resolve an issue label reference without mutating Linear

```
Usage:   linear resolve label <label>

Description:

  Resolve an issue label reference without mutating Linear

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  --team           <team>     - Team key for team-scoped resolution                                  
  -j, --json                  - Force machine-readable JSON output                                   
  --text                      - Output human-readable text                                           

Examples:

  Resolve a label within a team context linear resolve label Bug --team ENG
```
