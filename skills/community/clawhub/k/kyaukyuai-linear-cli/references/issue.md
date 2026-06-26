# issue

> Manage Linear issues

## Usage

```
Usage:   linear issue

Description:

  Manage Linear issues

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  

Commands:

  id                                      - Print the issue based on the current git branch                    
  list                                    - List issues assigned to you (use -A/--all-assignees to include all)
  search            <query>               - Deprecated: use `issue list` or `api` for issue filtering          
  title             [issueId]             - Print the issue title                                              
  start             [issueId]             - Start working on an issue                                          
  view, v           [issueId]             - View issue details (default) or open in browser/app                
  url               [issueId]             - Print the issue URL                                                
  describe          [issueId]             - Print the issue title and Linear-issue trailer                     
  commits           [issueId]             - Show all commits for a Linear issue (jj only)                      
  pull-request, pr  [issueId]             - Create a GitHub pull request with issue details                    
  delete, d         [issueId]             - Delete an issue                                                    
  create                                  - Create a linear issue                                              
  create-batch                            - Create a parent issue and child issues from a JSON file            
  update            [issueId]             - Update a linear issue                                              
  move              <issueId> <state>     - Move an issue to a different workflow state                        
  assign            <issueId> [assignee]  - Assign an issue to a user                                          
  priority          <issueId> <priority>  - Set the priority of an issue                                       
  estimate          <issueId> [points]    - Set the estimate (points) of an issue                              
  parent            [issueId]             - Show the parent issue for an issue                                 
  children          [issueId]             - List child issues for an issue                                     
  label                                   - Manage issue labels                                                
  comment                                 - Manage issue comments                                              
  attach            <issueId> <filepath>  - Attach a file to an issue                                          
  relation                                - Manage issue relations (dependencies)
```

## Subcommands

### id

> Print the issue based on the current git branch

```
Usage:   linear issue id

Description:

  Print the issue based on the current git branch

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)
```

### list

> List issues assigned to you (use -A/--all-assignees to include all)

```
Usage:   linear issue list

Description:

  List issues assigned to you (use -A/--all-assignees to include all)

Options:

  -h, --help                            - Show this help.                                                                                                
  -w, --workspace      <slug>           - Target workspace (uses credentials)                                                                            
  --profile            <profile>        - Execution profile override (agent-safe default, human-debug opt-in)                                            
  -s, --state          <state>          - Filter by issue state (triage, backlog, unstarted|todo, started, completed,      (Default: [ "unstarted" ])    
                                          canceled). May be repeated.                                                                                    
  --all-states                          - Show issues from all states                                                                                    
  --all                                 - Shortcut for --all-states --all-assignees --limit 0 (explicit --state overrides                                
                                          all-states)                                                                                                    
  --assignee           <assignee>       - Filter by assignee (username)                                                                                  
  -A, --all-assignees                   - Show issues for all assignees                                                                                  
  -U, --unassigned                      - Show only unassigned issues                                                                                    
  --sort               <sort>           - Sort order (can also be set via LINEAR_ISSUE_SORT)                               (Values: "manual", "priority")
  --team               <team>           - Team to list issues for (if not your default team)                                                             
  --project            <project>        - Filter by project name                                                                                         
  --cycle              <cycle>          - Filter by cycle name, number, or 'active'                                                                      
  --milestone          <milestone>      - Filter by project milestone name (requires --project)                                                          
  --query              <query>          - Filter by title or description substring                                                                       
  --parent             <parent>         - Filter by parent issue identifier                                                                              
  --priority           <priority>       - Filter by priority (0-4 or none/urgent/high/medium/low)                                                        
  --updated-before     <updatedBefore>  - Filter issues updated before an ISO date or datetime                                                           
  --due-before         <dueBefore>      - Filter issues due before a date (YYYY-MM-DD)                                                                   
  --limit              <limit>          - Maximum number of issues to fetch (default: 50, use 0 for unlimited)             (Default: 50)                 
  -j, --json                            - Force machine-readable JSON output                                                                             
  --text                                - Output human-readable text                                                                                     
  -w, --web                             - Open in web browser                                                                                            
  -a, --app                             - Open in Linear.app                                                                                             
  --no-pager                            - Disable automatic paging for long output                                                                       

Examples:

  List all issues as JSON                             linear issue list --all                                              
  List issues in the terminal                         linear issue list --all --text                                       
  List todo issues for a project across all assignees linear issue list --state todo --project auth-refresh --all-assignees
```

### search

> Deprecated: use `issue list` or `api` for issue filtering

```
Usage:   linear issue search <query>

Description:

  Deprecated: use `issue list` or `api` for issue filtering

Options:

  -h, --help                         - Show this help.                                                                   
  -w, --workspace         <slug>     - Target workspace (uses credentials)                                               
  --profile               <profile>  - Execution profile override (agent-safe default, human-debug opt-in)               
  -j, --json                         - Output as JSON                                                                    
  -n, --limit             <limit>    - Maximum number of results                                            (Default: 20)
  -a, --include-archived             - Include archived issues in results
```

### title

> Print the issue title

```
Usage:   linear issue title [issueId]

Description:

  Print the issue title

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)
```

### start

> Start working on an issue

```
Usage:   linear issue start [issueId]

Description:

  Start working on an issue

Options:

  -h, --help                      - Show this help.                                                      
  -w, --workspace      <slug>     - Target workspace (uses credentials)                                  
  --profile            <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  -A, --all-assignees             - Show issues for all assignees                                        
  -U, --unassigned                - Show only unassigned issues                                          
  -f, --from-ref       <fromRef>  - Git ref to create new branch from                                    
  -b, --branch         <branch>   - Custom branch name to use instead of the issue identifier            
  -i, --interactive               - Enable interactive issue selection                                   
  --dry-run                       - Preview the branch and state transition without making changes       

Examples:

  Preview the branch and state transition linear issue start ENG-123 --dry-run
  Pick from all unstarted issues          linear issue start --all-assignees
```

### view

> View issue details (default) or open in browser/app

```
Usage:   linear issue view [issueId]

Description:

  View issue details (default) or open in browser/app

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  -w, --web                   - Open in web browser                                                  
  -a, --app                   - Open in Linear.app                                                   
  --no-comments               - Exclude comments from the output                                     
  --no-pager                  - Disable automatic paging for long output                             
  -j, --json                  - Force machine-readable JSON output                                   
  --text                      - Output human-readable text                                           
  --no-download               - Keep remote URLs instead of downloading files                        

Examples:

  View issue as JSON          linear issue view ENG-123 --json                  
  View issue in the terminal  linear issue view ENG-123 --text                  
  View issue without comments linear issue view ENG-123 --no-comments --no-pager
```

### url

> Print the issue URL

```
Usage:   linear issue url [issueId]

Description:

  Print the issue URL

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)
```

### describe

> Print the issue title and Linear-issue trailer

```
Usage:   linear issue describe [issueId]

Description:

  Print the issue title and Linear-issue trailer

Options:

  -h, --help                          - Show this help.                                                      
  -w, --workspace          <slug>     - Target workspace (uses credentials)                                  
  --profile                <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  -r, --references, --ref             - Use 'References' instead of 'Fixes' for the Linear issue link
```

### commits

> Show all commits for a Linear issue (jj only)

```
Usage:   linear issue commits [issueId]

Description:

  Show all commits for a Linear issue (jj only)

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)
```

### pull-request

> Create a GitHub pull request with issue details

```
Usage:   linear issue pull-request [issueId]

Description:

  Create a GitHub pull request with issue details

Options:

  -h, --help                  - Show this help.                                                         
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                     
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)     
  --base           <branch>   - The branch into which you want your code merged                         
  --draft                     - Create the pull request as a draft                                      
  -t, --title      <title>    - Optional title for the pull request (Linear issue ID will be prefixed)  
  --web                       - Open the pull request in the browser after creating it                  
  --head           <branch>   - The branch that contains commits for your pull request
```

### delete

> Delete an issue

```
Usage:   linear issue delete [issueId]

Description:

  Delete an issue

Options:

  -h, --help                    - Show this help.                                                      
  -w, --workspace    <slug>     - Target workspace (uses credentials)                                  
  --profile          <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  -i, --interactive             - Enable interactive confirmation                                      
  -y, --yes                     - Skip confirmation prompt                                             
  --confirm                     - Deprecated alias for --yes                                           
  --bulk             <ids...>   - Delete multiple issues by identifier (e.g., TC-123 TC-124)           
  --bulk-file        <file>     - Read issue identifiers from a file (one per line)                    
  --bulk-stdin                  - Read issue identifiers from stdin
```

### create

> Create a linear issue

```
Usage:   linear issue create

Description:

  Create a linear issue

Options:

  -h, --help                                - Show this help.                                                                   
  -w, --workspace            <slug>         - Target workspace (uses credentials)                                               
  --profile                  <profile>      - Execution profile override (agent-safe default, human-debug opt-in)               
  --start                                   - Start the issue after creation                                                    
  -a, --assignee             <assignee>     - Assign the issue to 'self' or someone (by username or name)                       
  --due-date                 <dueDate>      - Due date of the issue                                                             
  --parent                   <parent>       - Parent issue (if any) as a team_number code                                       
  -p, --priority             <priority>     - Priority of the issue (1-4, descending priority)                                  
  --estimate                 <estimate>     - Points estimate of the issue                                                      
  -d, --description          <description>  - Description of the issue (prefer --description-file for markdown)                 
  --description-file         <path>         - Read description from a file (preferred for markdown content)                     
  --context-file             <path>         - Read a normalized external context JSON envelope from a file.                     
  --apply-triage                            - Apply deterministic triage hints from --context-file when routing fields are      
                                              omitted.                                                                          
  --autonomy-policy          <policy>       - Gate source-adjacent intake to suggest-only, preview-required, or apply-allowed.  
  -l, --label                <label>        - Issue label associated with the issue. May be repeated.                           
  --team                     <team>         - Team associated with the issue (if not your default team)                         
  --project                  <project>      - Name or slug ID of the project with the issue                                     
  -s, --state                <state>        - Workflow state for the issue (by name or type)                                    
  --milestone                <milestone>    - Name of the project milestone                                                     
  --cycle                    <cycle>        - Cycle name, number, or 'active'                                                   
  -j, --json                                - Force machine-readable JSON output                                                
  --text                                    - Output human-readable text                                                        
  --dry-run                                 - Preview the created issue without creating it                                     
  --timeout-ms               <timeoutMs>    - Timeout for write confirmation in milliseconds                                    
  --no-pager                                - Accepted for compatibility; issue create does not use a pager                     
  --no-use-default-template                 - Do not use default template for the issue                                         
  -i, --interactive                         - Enable interactive prompts and editor flow                                        
  --no-interactive                          - Accepted for compatibility; issue create is non-interactive by default            
  -t, --title                <title>        - Title of the issue                                                                

Examples:

  Create an issue as JSON                                   linear issue create --title "Fix auth expiry bug" --team ENG                                        
  Create an issue with a piped description                  cat description.md | linear issue create --title "Fix auth expiry bug" --team ENG                   
  Create an issue from a normalized source context file     linear issue create --team ENG --context-file slack-thread.json --dry-run --json                    
  Apply deterministic triage from normalized source context linear issue create --context-file slack-thread.json --apply-triage --dry-run --json                
  Preview source-intake suggestions without applying them   linear issue create --context-file slack-thread.json --autonomy-policy suggest-only --dry-run --json
  Create an issue with human-readable output                linear issue create --title "Fix auth expiry bug" --team ENG --text                                 
  Preview issue creation                                    linear issue create --title "Fix auth expiry bug" --team ENG --state started --dry-run
```

### create-batch

> Create a parent issue and child issues from a JSON file

```
Usage:   linear issue create-batch

Description:

  Create a parent issue and child issues from a JSON file

Options:

  -h, --help                    - Show this help.                                                      
  -w, --workspace  <slug>       - Target workspace (uses credentials)                                  
  --profile        <profile>    - Execution profile override (agent-safe default, human-debug opt-in)  
  --file           <path>       - Path to a JSON file describing the issue batch                       
  --team           <team>       - Team key override for the batch file                                 
  --project        <project>    - Project name override for the batch file                             
  -j, --json                    - Output as JSON                                                       
  --dry-run                     - Preview the batch without creating issues                            
  --timeout-ms     <timeoutMs>  - Timeout for write confirmation in milliseconds                       

Examples:

  Preview a parent and child issue batch linear issue create-batch --file rollout.json --dry-run
  Create a batch and return JSON         linear issue create-batch --file rollout.json --json
```

### update

> Update a linear issue

```
Usage:   linear issue update [issueId]

Description:

  Update a linear issue

Options:

  -h, --help                         - Show this help.                                                                   
  -w, --workspace     <slug>         - Target workspace (uses credentials)                                               
  --profile           <profile>      - Execution profile override (agent-safe default, human-debug opt-in)               
  -a, --assignee      <assignee>     - Assign the issue to 'self' or someone (by username or name)                       
  --due-date          <dueDate>      - Due date of the issue                                                             
  --clear-due-date                   - Clear the due date on the issue                                                   
  --parent            <parent>       - Parent issue (if any) as a team_number code                                       
  -p, --priority      <priority>     - Priority of the issue (1-4, descending priority)                                  
  --estimate          <estimate>     - Points estimate of the issue                                                      
  -d, --description   <description>  - Description of the issue (prefer --description-file for markdown)                 
  --comment           <comment>      - Add a comment after successfully updating the issue                               
  --description-file  <path>         - Read description from a file (preferred for markdown content)                     
  --context-file      <path>         - Read a normalized external context JSON envelope from a file.                     
  --context-target    <target>       - Map --context-file into description or comment (default: comment).                
  --apply-triage                     - Apply deterministic triage hints from --context-file when routing fields are      
                                       omitted.                                                                          
  --autonomy-policy   <policy>       - Gate source-adjacent intake to suggest-only, preview-required, or apply-allowed.  
  -l, --label         <label>        - Issue label associated with the issue. May be repeated.                           
  --team              <team>         - Team associated with the issue (if not your default team)                         
  --project           <project>      - Name or slug ID of the project with the issue                                     
  -s, --state         <state>        - Workflow state for the issue (by name or type)                                    
  --milestone         <milestone>    - Name of the project milestone                                                     
  --cycle             <cycle>        - Cycle name, number, or 'active'                                                   
  --no-interactive                   - Accepted for compatibility; issue update is always non-interactive                
  -j, --json                         - Force machine-readable JSON output                                                
  --text                             - Output human-readable text                                                        
  --dry-run                          - Preview the update without mutating the issue                                     
  --timeout-ms        <timeoutMs>    - Timeout for write confirmation in milliseconds                                    
  -t, --title         <title>        - Title of the issue                                                                

Examples:

  Update state and assignee                                 linear issue update ENG-123 --state started --assignee self                                                 
  Preview an update with a comment                          linear issue update ENG-123 --state completed --comment "Ready for review" --dry-run                        
  Pipe a description into an update                         cat description.md | linear issue update ENG-123 --state started --dry-run --json                           
  Preview an update with normalized source context          linear issue update ENG-123 --state triage --context-file slack-thread.json --dry-run --json                
  Apply deterministic triage from normalized source context linear issue update ENG-123 --context-file slack-thread.json --apply-triage --dry-run --json                
  Preview source-intake suggestions without applying them   linear issue update ENG-123 --context-file slack-thread.json --autonomy-policy suggest-only --dry-run --json
  Return the updated issue as JSON                          linear issue update ENG-123 --title "Fix auth timeout edge case"                                            
  Return human-readable terminal output                     linear issue update ENG-123 --title "Fix auth timeout edge case" --text
```

### move

> Move an issue to a different workflow state

```
Usage:   linear issue move <issueId> <state>

Description:

  Move an issue to a different workflow state

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  -j, --json                  - Output as JSON                                                       

Examples:

  Move to In Progress linear issue move ENG-123 'In Progress'
  Move to Done        linear issue move ENG-123 Done         
  Move by state type  linear issue move ENG-123 completed
```

### assign

> Assign an issue to a user

```
Usage:   linear issue assign <issueId> [assignee]

Description:

  Assign an issue to a user

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  -j, --json                  - Output as JSON                                                       
  --unassign                  - Remove the current assignee                                          

Examples:

  Assign to self linear issue assign ENG-123 self      
  Assign to user linear issue assign ENG-123 john      
  Unassign       linear issue assign ENG-123 --unassign
```

### priority

> Set the priority of an issue

```
Usage:   linear issue priority <issueId> <priority>

Description:

  Set the priority of an issue

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  -j, --json                  - Output as JSON                                                       

Examples:

  Set urgent     linear issue priority ENG-123 1
  Set high       linear issue priority ENG-123 2
  Set medium     linear issue priority ENG-123 3
  Set low        linear issue priority ENG-123 4
  Clear priority linear issue priority ENG-123 0
```

### estimate

> Set the estimate (points) of an issue

```
Usage:   linear issue estimate <issueId> [points]

Description:

  Set the estimate (points) of an issue

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  -j, --json                  - Output as JSON                                                       
  --clear                     - Clear the estimate                                                   

Examples:

  Set 3 points   linear issue estimate ENG-123 3      
  Set 5 points   linear issue estimate ENG-123 5      
  Clear estimate linear issue estimate ENG-123 --clear
```

### parent

> Show the parent issue for an issue

```
Usage:   linear issue parent [issueId]

Description:

  Show the parent issue for an issue

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  -j, --json                  - Output as JSON
```

### children

> List child issues for an issue

```
Usage:   linear issue children [issueId]

Description:

  List child issues for an issue

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  -j, --json                  - Output as JSON
```

### label

> Manage issue labels

```
Usage:   linear issue label

Description:

  Manage issue labels

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  

Commands:

  add     <issueId> <label>  - Add a label to an issue     
  remove  <issueId> <label>  - Remove a label from an issue
```

#### label subcommands

##### add

```
Usage:   linear issue label add <issueId> <label>

Description:

  Add a label to an issue

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  

Examples:

  Add bug label linear issue label add ENG-123 bug
```

##### remove

```
Usage:   linear issue label remove <issueId> <label>

Description:

  Remove a label from an issue

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  

Examples:

  Remove bug label linear issue label remove ENG-123 bug
```

### comment

> Manage issue comments

```
Usage:   linear issue comment

Description:

  Manage issue comments

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  

Commands:

  add     [issueId] [body]  - Add a comment to an issue or reply to a comment
  delete  <commentId>       - Delete a comment                               
  update  <commentId>       - Update an existing comment                     
  list    [issueId]         - List comments for an issue
```

#### comment subcommands

##### add

```
Usage:   linear issue comment add [issueId] [body]

Description:

  Add a comment to an issue or reply to a comment

Options:

  -h, --help                      - Show this help.                                                      
  -w, --workspace    <slug>       - Target workspace (uses credentials)                                  
  --profile          <profile>    - Execution profile override (agent-safe default, human-debug opt-in)  
  -b, --body         <text>       - Comment body text                                                    
  --body-file        <path>       - Read comment body from a file (preferred for markdown content)       
  -p, --parent       <id>         - Parent comment ID for replies                                        
  -a, --attach       <filepath>   - Attach a file to the comment (can be used multiple times)            
  -i, --interactive               - Enable interactive body prompts                                      
  -j, --json                      - Output as JSON                                                       
  --dry-run                       - Preview the comment without creating it                              
  --timeout-ms       <timeoutMs>  - Timeout for write confirmation in milliseconds                       

Examples:

  Add a comment with a positional body linear issue comment add ENG-123 "Ready for review"                               
  Preview a comment from a file        linear issue comment add ENG-123 --body-file review.md --dry-run                  
  Pipe a comment body from stdin       printf "Ready for review\n" | linear issue comment add ENG-123                    
  Reply to a comment as JSON           linear issue comment add ENG-123 --parent comment_123 --body "Following up" --json
```

##### delete

```
Usage:   linear issue comment delete <commentId>

Description:

  Delete a comment

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)
```

##### update

```
Usage:   linear issue comment update <commentId>

Description:

  Update an existing comment

Options:

  -h, --help                      - Show this help.                                                      
  -w, --workspace    <slug>       - Target workspace (uses credentials)                                  
  --profile          <profile>    - Execution profile override (agent-safe default, human-debug opt-in)  
  -b, --body         <text>       - New comment body text                                                
  --body-file        <path>       - Read comment body from a file (preferred for markdown content)       
  --timeout-ms       <timeoutMs>  - Timeout for write confirmation in milliseconds                       
  -i, --interactive               - Enable interactive body prompts                                      

Examples:

  Update a comment from stdin printf "Updated comment\n" | linear issue comment update comment_123
```

##### list

```
Usage:   linear issue comment list [issueId]

Description:

  List comments for an issue

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  -j, --json                  - Output as JSON                                                       
  --no-pager                  - Disable automatic paging for long output
```

### attach

> Attach a file to an issue

```
Usage:   linear issue attach <issueId> <filepath>

Description:

  Attach a file to an issue

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  -t, --title      <title>    - Custom title for the attachment                                      
  -c, --comment    <body>     - Add a comment body linked to the attachment
```

### relation

> Manage issue relations (dependencies)

```
Usage:   linear issue relation

Description:

  Manage issue relations (dependencies)

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  

Commands:

  add     <issueId> <relationType> <relatedIssueId>  - Add a relation between two issues   
  delete  <issueId> <relationType> <relatedIssueId>  - Delete a relation between two issues
  list    [issueId]                                  - List relations for an issue
```

#### relation subcommands

##### add

```
Usage:   linear issue relation add <issueId> <relationType> <relatedIssueId>

Description:

  Add a relation between two issues

Options:

  -h, --help                    - Show this help.                                                      
  -w, --workspace  <slug>       - Target workspace (uses credentials)                                  
  --profile        <profile>    - Execution profile override (agent-safe default, human-debug opt-in)  
  -j, --json                    - Output as JSON                                                       
  --dry-run                     - Preview relation creation without mutating Linear                    
  --timeout-ms     <timeoutMs>  - Timeout for write confirmation in milliseconds                       

Examples:

  Mark issue as blocked by another linear issue relation add ENG-123 blocked-by ENG-100
  Mark issue as blocking another   linear issue relation add ENG-123 blocks ENG-456    
  Mark issues as related           linear issue relation add ENG-123 related ENG-456   
  Mark issue as duplicate          linear issue relation add ENG-123 duplicate ENG-100
```

##### delete

```
Usage:   linear issue relation delete <issueId> <relationType> <relatedIssueId>

Description:

  Delete a relation between two issues

Options:

  -h, --help                    - Show this help.                                                      
  -w, --workspace  <slug>       - Target workspace (uses credentials)                                  
  --profile        <profile>    - Execution profile override (agent-safe default, human-debug opt-in)  
  -j, --json                    - Output as JSON                                                       
  --dry-run                     - Preview relation deletion without mutating Linear                    
  --timeout-ms     <timeoutMs>  - Timeout for write confirmation in milliseconds
```

##### list

```
Usage:   linear issue relation list [issueId]

Description:

  List relations for an issue

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  -j, --json                  - Output as JSON
```
