# label

> Manage Linear issue labels

## Usage

```
Usage:   linear label

Description:

  Manage Linear issue labels

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  

Commands:

  list                - List issue labels       
  create              - Create a new issue label
  delete  <nameOrId>  - Delete an issue label
```

## Subcommands

### list

> List issue labels

```
Usage:   linear label list

Description:

  List issue labels

Options:

  -h, --help              - Show this help.                                                      
  --profile    <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  --team       <teamKey>  - Filter by team (e.g., TC). Shows team-specific labels only.          
  --workspace             - Show only workspace-level labels (not team-specific)                 
  --all                   - Show all labels (both workspace and team)                            
  -j, --json              - Output as JSON                                                       
  --no-pager              - Disable automatic paging for long output                             

Examples:

  List issue labels as JSON linear label list --json
```

### create

> Create a new issue label

```
Usage:   linear label create

Description:

  Create a new issue label

Options:

  -h, --help                        - Show this help.                                                      
  -w, --workspace    <slug>         - Target workspace (uses credentials)                                  
  --profile          <profile>      - Execution profile override (agent-safe default, human-debug opt-in)  
  -n, --name         <name>         - Label name (required)                                                
  -c, --color        <color>        - Color hex code (e.g., #EB5757)                                       
  -d, --description  <description>  - Label description                                                    
  -t, --team         <teamKey>      - Team key for team-specific label (omit for workspace label)          
  -i, --interactive                 - Enable interactive prompts
```

### delete

> Delete an issue label

```
Usage:   linear label delete <nameOrId>

Description:

  Delete an issue label

Options:

  -h, --help                    - Show this help.                                                      
  -w, --workspace    <slug>     - Target workspace (uses credentials)                                  
  --profile          <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  -i, --interactive             - Enable interactive selection and confirmation                        
  -t, --team         <teamKey>  - Team key to disambiguate labels with same name                       
  -y, --yes                     - Skip confirmation prompt                                             
  -f, --force                   - Deprecated alias for --yes
```
