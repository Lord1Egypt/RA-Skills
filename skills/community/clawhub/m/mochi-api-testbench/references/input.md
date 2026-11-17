# Action contract

validate:cases1..25 with id,url,method defaultGET,headers,headerEnv header-name->environment-variable, bearerEnv optional, json/body optional, assert object. Assertions:status int/list,jsonEquals pointer->expected,jsonExists pointer list,bodyContains string list,headers name->value,maxMilliseconds. JSON pointers use /items/0/id. run executes suite; credentials from environment only, no response bodies saved. HTTPS required; allowPrivateHosts exact hostname list explicitly opts into private/local endpoints and local HTTP. No redirects followed in testbench. Write verbs require allowMutations:true AND actual user authorization. compare:before/after saved report.json paths. Network errors are case failures, not successful checks.

Reports remain local. Use the current model to interpret results; the executable tool performs the documented data operations.
