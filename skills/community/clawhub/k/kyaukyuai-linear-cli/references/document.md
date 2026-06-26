# document

> Manage Linear documents

## Usage

```
Usage:   linear document

Description:

  Manage Linear documents

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  

Commands:

  list, l                  - List documents                    
  view, v    <id>          - View a document's content         
  create, c                - Create a new document             
  update, u  <documentId>  - Update an existing document       
  delete, d  [documentId]  - Delete a document (moves to trash)
```

## Subcommands

### list

> List documents

```
Usage:   linear document list

Description:

  List documents

Options:

  -h, --help                  - Show this help.                                                                   
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                               
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)               
  --project        <project>  - Filter by project (slug or name)                                                  
  --issue          <issue>    - Filter by issue (identifier like TC-123)                                          
  --json                      - Force machine-readable JSON output                                                
  --text                      - Output human-readable text                                                        
  --limit          <limit>    - Limit results                                                        (Default: 50)
  --no-pager                  - Disable automatic paging for long output                                          

Examples:

  List documents as JSON         linear document list --project platform-refresh       
  List documents in the terminal linear document list --project platform-refresh --text
```

### view

> View a document's content

```
Usage:   linear document view <id>

Description:

  View a document's content

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  --raw                       - Output raw markdown without rendering                                
  -w, --web                   - Open document in browser                                             
  --json                      - Output full document as JSON                                         

Examples:

  View a document as JSON linear document view d4b93e3b2695 --json
```

### create

> Create a new document

```
Usage:   linear document create

Description:

  Create a new document

Options:

  -h, --help                     - Show this help.                                                      
  -w, --workspace     <slug>     - Target workspace (uses credentials)                                  
  --profile           <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  -t, --title         <title>    - Document title (required)                                            
  -c, --content       <content>  - Markdown content (inline)                                            
  -f, --content-file  <path>     - Read content from file                                               
  --project           <project>  - Attach to project (slug or ID)                                       
  --issue             <issue>    - Attach to issue (identifier like TC-123)                             
  --icon              <icon>     - Document icon (emoji)                                                
  -i, --interactive              - Interactive mode with prompts                                        
  --dry-run                      - Preview the document without creating it
```

### update

> Update an existing document

```
Usage:   linear document update <documentId>

Description:

  Update an existing document

Options:

  -h, --help                     - Show this help.                                                      
  -w, --workspace     <slug>     - Target workspace (uses credentials)                                  
  --profile           <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  -t, --title         <title>    - New title for the document                                           
  -c, --content       <content>  - New markdown content (inline)                                        
  -f, --content-file  <path>     - Read new content from file                                           
  --icon              <icon>     - New icon (emoji)                                                     
  -e, --edit                     - Open current content in $EDITOR for editing                          
  --dry-run                      - Preview the update without mutating the document
```

### delete

> Delete a document (moves to trash)

```
Usage:   linear document delete [documentId]

Description:

  Delete a document (moves to trash)

Options:

  -h, --help                    - Show this help.                                                      
  -w, --workspace    <slug>     - Target workspace (uses credentials)                                  
  --profile          <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  -i, --interactive             - Enable interactive confirmation                                      
  -y, --yes                     - Skip confirmation prompt                                             
  --bulk             <ids...>   - Delete multiple documents by slug or ID                              
  --bulk-file        <file>     - Read document slugs/IDs from a file (one per line)                   
  --bulk-stdin                  - Read document slugs/IDs from stdin                                   
  --dry-run                     - Preview the deletion without mutating documents
```
