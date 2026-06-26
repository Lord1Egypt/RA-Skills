# webhook

> Manage Linear webhooks

## Usage

```
Usage:   linear webhook

Description:

  Manage Linear webhooks

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  

Commands:

  list                 - List webhooks   
  view    <webhookId>  - View a webhook  
  create               - Create a webhook
  update  <webhookId>  - Update a webhook
  delete  <webhookId>  - Delete a webhook
```

## Subcommands

### list

> List webhooks

```
Usage:   linear webhook list

Description:

  List webhooks

Options:

  -h, --help                     - Show this help.                                                                   
  -w, --workspace     <slug>     - Target workspace (uses credentials)                                               
  --profile           <profile>  - Execution profile override (agent-safe default, human-debug opt-in)               
  -n, --limit         <limit>    - Maximum number of webhooks                                           (Default: 20)
  --team              <teamKey>  - Filter by team key                                                                
  --include-archived             - Include archived webhooks                                                         
  -j, --json                     - Output as JSON                                                                    
  --no-pager                     - Disable automatic paging for long output                                          

Examples:

  List team webhooks as JSON linear webhook list --team ENG --json            
  List archived webhooks     linear webhook list --include-archived --limit 50
```

### view

> View a webhook

```
Usage:   linear webhook view <webhookId>

Description:

  View a webhook

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  -j, --json                  - Force machine-readable JSON output                                   
  --text                      - Output human-readable text                                           

Examples:

  View a webhook as JSON         linear webhook view webhook_123       
  View a webhook in the terminal linear webhook view webhook_123 --text
```

### create

> Create a webhook

```
Usage:   linear webhook create

Description:

  Create a webhook

Options:

  -h, --help                             - Show this help.                                                      
  -w, --workspace       <slug>           - Target workspace (uses credentials)                                  
  --profile             <profile>        - Execution profile override (agent-safe default, human-debug opt-in)  
  -u, --url             <url>            - Webhook URL (required)                                               
  -r, --resource-types  <resourceTypes>  - Comma-separated resource types (e.g. Issue,Comment)                  
  -l, --label           <label>          - Webhook label                                                        
  -t, --team            <teamKey>        - Team key (defaults to current team)                                  
  --all-public-teams                     - Enable the webhook for all public teams instead of a specific team   
  --secret              <secret>         - Secret used to sign webhook payloads                                 
  --disabled                             - Create the webhook disabled                                          
  -j, --json                             - Output as JSON                                                       
  --dry-run                              - Preview the webhook without creating it                              

Examples:

  Preview creating a team webhook            linear webhook create --url https://example.com/hooks/linear --resource-types Issue,Comment --team ENG --dry-run
  Create an all-public-teams webhook as JSON linear webhook create --url https://example.com/hooks/linear --resource-types Issue --all-public-teams --json
```

### update

> Update a webhook

```
Usage:   linear webhook update <webhookId>

Description:

  Update a webhook

Options:

  -h, --help                             - Show this help.                                                      
  -w, --workspace       <slug>           - Target workspace (uses credentials)                                  
  --profile             <profile>        - Execution profile override (agent-safe default, human-debug opt-in)  
  -u, --url             <url>            - New webhook URL                                                      
  -r, --resource-types  <resourceTypes>  - New comma-separated resource types                                   
  -l, --label           <label>          - New webhook label                                                    
  --secret              <secret>         - New secret used to sign payloads                                     
  --enabled                              - Enable the webhook                                                   
  --disabled                             - Disable the webhook                                                  
  -j, --json                             - Output as JSON                                                       
  --dry-run                              - Preview the update without mutating the webhook                      

Examples:

  Preview a webhook update  linear webhook update webhook_123 --label "Primary webhook" --resource-types Issue,Comment --dry-run
  Disable a webhook as JSON linear webhook update webhook_123 --disabled --json
```

### delete

> Delete a webhook

```
Usage:   linear webhook delete <webhookId>

Description:

  Delete a webhook

Options:

  -h, --help                    - Show this help.                                                      
  -w, --workspace    <slug>     - Target workspace (uses credentials)                                  
  --profile          <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  -i, --interactive             - Enable interactive confirmation                                      
  -y, --yes                     - Skip confirmation prompt                                             
  -j, --json                    - Output as JSON                                                       
  --dry-run                     - Preview the deletion without mutating the webhook                    

Examples:

  Preview deleting a webhook         linear webhook delete webhook_123 --dry-run   
  Delete a webhook without prompting linear webhook delete webhook_123 --yes --json
```
