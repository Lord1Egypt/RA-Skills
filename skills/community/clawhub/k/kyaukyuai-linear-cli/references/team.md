# team

> Manage Linear teams

## Usage

```
Usage:   linear team

Description:

  Manage Linear teams

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  

Commands:

  create                - Create a linear team                                                         
  delete     <teamKey>  - Delete a Linear team                                                         
  list                  - List teams                                                                   
  view       [teamKey]  - View a team                                                                  
  id                    - Print the configured team id                                                 
  autolinks             - Configure GitHub repository autolinks for Linear issues with this team prefix
  members    [teamKey]  - List team members
```

## Subcommands

### create

> Create a linear team

```
Usage:   linear team create

Description:

  Create a linear team

Options:

  -h, --help                        - Show this help.                                                        
  -w, --workspace    <slug>         - Target workspace (uses credentials)                                    
  --profile          <profile>      - Execution profile override (agent-safe default, human-debug opt-in)    
  -n, --name         <name>         - Name of the team                                                       
  -d, --description  <description>  - Description of the team                                                
  -i, --interactive                 - Enable interactive prompts                                             
  -k, --key          <key>          - Team key (if not provided, will be generated from name)                
  --private                         - Make the team private                                                  
  --no-interactive                  - Accepted for compatibility; team create is non-interactive by default
```

### delete

> Delete a Linear team

```
Usage:   linear team delete <teamKey>

Description:

  Delete a Linear team

Options:

  -h, --help                       - Show this help.                                                      
  -w, --workspace    <slug>        - Target workspace (uses credentials)                                  
  --profile          <profile>     - Execution profile override (agent-safe default, human-debug opt-in)  
  -i, --interactive                - Enable interactive selection and confirmation                        
  --move-issues      <targetTeam>  - Move all issues to another team before deletion                      
  -y, --yes                        - Skip confirmation prompt                                             
  --force                          - Deprecated alias for --yes
```

### list

> List teams

```
Usage:   linear team list

Description:

  List teams

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  -j, --json                  - Output as JSON                                                       
  -w, --web                   - Open in web browser                                                  
  -a, --app                   - Open in Linear.app                                                   
  --no-pager                  - Disable automatic paging for long output                             

Examples:

  List teams as JSON linear team list --json
```

### view

> View a team

```
Usage:   linear team view [teamKey]

Description:

  View a team

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  -j, --json                  - Output as JSON                                                       

Examples:

  View a team as JSON linear team view ENG --json
```

### id

> Print the configured team id

```
Usage:   linear team id

Description:

  Print the configured team id

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)
```

### autolinks

> Configure GitHub repository autolinks for Linear issues with this team prefix

```
Usage:   linear team autolinks

Description:

  Configure GitHub repository autolinks for Linear issues with this team prefix

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)
```

### members

> List team members

```
Usage:   linear team members [teamKey]

Description:

  List team members

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  -a, --all                   - Include inactive members                                             
  -j, --json                  - Output as JSON
```
