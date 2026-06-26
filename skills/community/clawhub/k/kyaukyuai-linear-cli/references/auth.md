# auth

> Manage Linear authentication

## Usage

```
Usage:   linear auth

Description:

  Manage Linear authentication

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  

Commands:

  login                 - Add a workspace credential                     
  logout   [workspace]  - Remove a workspace credential                  
  list                  - List configured workspaces                     
  default  [workspace]  - Set the default workspace                      
  token                 - Print the configured API token                 
  whoami                - Print information about the authenticated user 
  migrate               - Migrate plaintext credentials to system keyring
```

## Subcommands

### login

> Add a workspace credential

```
Usage:   linear auth login

Description:

  Add a workspace credential

Options:

  -h, --help                    - Show this help.                                                      
  -w, --workspace    <slug>     - Target workspace (uses credentials)                                  
  --profile          <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  -k, --key          <key>      - API key (prompted if not provided)                                   
  -i, --interactive             - Enable interactive prompts                                           
  --plaintext                   - Store API key in credentials file instead of system keyring
```

### logout

> Remove a workspace credential

```
Usage:   linear auth logout [workspace]

Description:

  Remove a workspace credential

Options:

  -h, --help                    - Show this help.                                                      
  -w, --workspace    <slug>     - Target workspace (uses credentials)                                  
  --profile          <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  -i, --interactive             - Enable interactive selection and confirmation                        
  -y, --yes                     - Skip confirmation prompt                                             
  -f, --force                   - Deprecated alias for --yes
```

### list

> List configured workspaces

```
Usage:   linear auth list

Description:

  List configured workspaces

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  --no-pager                  - Disable automatic paging for long output
```

### default

> Set the default workspace

```
Usage:   linear auth default [workspace]

Description:

  Set the default workspace

Options:

  -h, --help                    - Show this help.                                                      
  -w, --workspace    <slug>     - Target workspace (uses credentials)                                  
  --profile          <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  -i, --interactive             - Enable interactive workspace selection
```

### token

> Print the configured API token

```
Usage:   linear auth token

Description:

  Print the configured API token

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)
```

### whoami

> Print information about the authenticated user

```
Usage:   linear auth whoami

Description:

  Print information about the authenticated user

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)
```

### migrate

> Migrate plaintext credentials to system keyring

```
Usage:   linear auth migrate

Description:

  Migrate plaintext credentials to system keyring

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)
```
