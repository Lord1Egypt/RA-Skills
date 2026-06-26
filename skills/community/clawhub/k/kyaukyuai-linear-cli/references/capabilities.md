# capabilities

> Describe the agent-facing command surface

## Usage

```
Usage:   linear capabilities

Description:

  Describe the agent-facing command surface

Options:

  -h, --help                  - Show this help.                                                      
  -w, --workspace  <slug>     - Target workspace (uses credentials)                                  
  --profile        <profile>  - Execution profile override (agent-safe default, human-debug opt-in)  
  -j, --json                  - Force machine-readable JSON output                                   
  --text                      - Output a human-readable summary                                      
  --compat         <version>  - Select the machine-readable capabilities schema version (v1, v2).    

Examples:

  Describe agent-facing capabilities as JSON  linear capabilities                                               
  Request the legacy v1 compatibility shape   linear capabilities --compat v1                                   
  Pin the richer v2 metadata shape explicitly linear capabilities --compat v2                                   
  Show the human-readable summary             linear capabilities --text                                        
  Find commands that support dry-run          linear capabilities | jq '.commands[] | select(.dryRun.supported)'
```
