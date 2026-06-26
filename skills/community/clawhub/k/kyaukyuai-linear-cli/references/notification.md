# notification

> Manage Linear notifications

## Usage

```
Usage:   linear notification

Description:

  Manage Linear notifications

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  

Commands:

  list                       - List notifications            
  count                      - Show unread notification count
  read     <notificationId>  - Mark a notification as read   
  archive  <notificationId>  - Archive a notification
```

## Subcommands

### list

> List notifications

```
Usage:   linear notification list

Description:

  List notifications

Options:

  -h, --help                     - Show this help.                                                                   
  -w, --workspace     <slug>     - Target workspace (uses credentials)                                               
  --profile           <profile>  - Execution profile override (agent-safe default, human-debug opt-in)               
  -n, --limit         <limit>    - Maximum number of notifications                                      (Default: 20)
  --include-archived             - Include archived notifications                                                    
  --unread                       - Show only unread notifications                                                    
  -j, --json                     - Force machine-readable JSON output                                                
  --text                         - Output human-readable text                                                        
  --no-pager                     - Disable automatic paging for long output                                          

Examples:

  List notifications as JSON         linear notification list       
  List notifications in the terminal linear notification list --text
```

### count

> Show unread notification count

```
Usage:   linear notification count

Description:

  Show unread notification count

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  -j, --json                  - Output as JSON
```

### read

> Mark a notification as read

```
Usage:   linear notification read <notificationId>

Description:

  Mark a notification as read

Options:

  -h, --help                    - Show this help.                                                      
  -w, --workspace  <slug>       - Target workspace (uses credentials)                                  
  --profile        <profile>    - Execution profile override (agent-safe default, human-debug opt-in)  
  -j, --json                    - Output as JSON                                                       
  --timeout-ms     <timeoutMs>  - Timeout for write confirmation in milliseconds
```

### archive

> Archive a notification

```
Usage:   linear notification archive <notificationId>

Description:

  Archive a notification

Options:

  -h, --help                    - Show this help.                                                      
  -w, --workspace  <slug>       - Target workspace (uses credentials)                                  
  --profile        <profile>    - Execution profile override (agent-safe default, human-debug opt-in)  
  -j, --json                    - Output as JSON                                                       
  --timeout-ms     <timeoutMs>  - Timeout for write confirmation in milliseconds
```
