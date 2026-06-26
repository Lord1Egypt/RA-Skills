#!/usr/bin/env node
// linear-native-node/scripts/linear.mjs
// Direct Linear GraphQL helper - native Node.js, zero dependencies.
// Requires Node 18+ for global fetch. Reads LINEAR_API_KEY from the process environment only.

const ENDPOINT = "https://api.linear.app/graphql";
const PRIORITIES = new Map([
  ["none", 0],
  ["urgent", 1],
  ["high", 2],
  ["medium", 3],
  ["low", 4],
]);
const PRIORITY_LABELS = new Map([...PRIORITIES.entries()].map(([k, v]) => [v, k]));

function die(message, code = 1) {
  process.stderr.write(`error: ${message}\n`);
  process.exit(code);
}

function setupMessage() {
  return [
    "LINEAR_API_KEY is not set.",
    "Create a Linear API key at: https://linear.app/settings/api",
    "Then add it for this shell session:",
    "  PowerShell: $env:LINEAR_API_KEY = \"<your-linear-key>\"",
    "  bash/zsh:    export LINEAR_API_KEY=\"<your-linear-key>\"",
    "Optional default team:",
    "  PowerShell: $env:LINEAR_DEFAULT_TEAM = \"TEAM\"",
    "  bash/zsh:    export LINEAR_DEFAULT_TEAM=\"TEAM\"",
  ].join("\n");
}

function getEnv(key) {
  return (process.env[key] || "").trim();
}

function requireApiKey() {
  const key = getEnv("LINEAR_API_KEY");
  if (!key) die(setupMessage());
  return key;
}

function parseGlobal(argv) {
  const out = { json: false, execute: false, args: [] };
  for (const arg of argv) {
    if (arg === "--json") out.json = true;
    else if (arg === "--execute") out.execute = true;
    else out.args.push(arg);
  }
  return out;
}

const WRITE_COMMANDS = new Set(["project-create", "create", "comment", "status", "priority"]);

function dieNoExecute(command) {
  // Safety gate: Linear write commands are disabled by default. Use --execute
  // only after explicit operator approval for the specific external mutation.
  die(`write command "${command}" is blocked by default. Re-run with --execute only after explicit approval.`);
}

function takeFlag(args, name, fallback = null) {
  const i = args.indexOf(name);
  if (i < 0) return fallback;
  const value = args[i + 1];
  if (value === undefined || value.startsWith("--")) die(`flag ${name} needs a value`);
  args.splice(i, 2);
  return value;
}

function takeBool(args, name) {
  const i = args.indexOf(name);
  if (i < 0) return false;
  args.splice(i, 1);
  return true;
}

function takeLimit(args, fallback) {
  const limit = Number(takeFlag(args, "--limit", String(fallback)));
  if (!Number.isInteger(limit) || limit < 1 || limit > 100) die("--limit must be an integer from 1 to 100");
  return limit;
}

function priorityValue(name) {
  const key = String(name || "").toLowerCase();
  if (!PRIORITIES.has(key)) die(`invalid priority: ${name}. Use urgent, high, medium, low, or none.`);
  return PRIORITIES.get(key);
}

function requireExactArgs(command, args, count, usage) {
  if (args.length < count) die(`${command} requires ${usage}`);
  if (args.length > count) die(`unknown extra args for ${command}: ${args.slice(count).join(" ")}`);
  return args.slice(0, count);
}

async function graphql(query, variables = {}) {
  const apiKey = requireApiKey();
  let response;
  try {
    response = await fetch(ENDPOINT, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: apiKey,
      },
      body: JSON.stringify({ query, variables }),
    });
  } catch (err) {
    die(`network error contacting Linear: ${err.message || err}`);
  }

  const text = await response.text();
  let payload = null;
  try { payload = text ? JSON.parse(text) : {}; } catch { /* handled below */ }

  if (response.status === 401 || response.status === 403) {
    const denyReason = response.headers?.get?.("x-deny-reason") ? " If this is running behind an egress proxy or sandbox, the proxy may be blocking api.linear.app before Linear sees the request." : "";
    die(`Linear authentication failed or endpoint access was denied (HTTP ${response.status}). Check LINEAR_API_KEY permissions.${denyReason} The key was not printed.`);
  }
  if (!response.ok) {
    const detail = payload?.errors?.map(e => e.message).join("; ") || payload?.message || text || response.statusText;
    die(`Linear HTTP ${response.status}: ${String(detail).slice(0, 700)}`);
  }
  if (!payload) die(`Linear returned non-JSON response: ${text.slice(0, 300)}`);
  if (payload.errors?.length) {
    die(`Linear GraphQL error: ${payload.errors.map(e => e.message).join("; ")}`);
  }
  return payload.data;
}

function print(data, json, formatter) {
  if (json) process.stdout.write(JSON.stringify(data, null, 2) + "\n");
  else process.stdout.write(formatter(data) + "\n");
}

function fmtIssue(issue) {
  const priority = issue.priorityLabel || PRIORITY_LABELS.get(issue.priority) || "none";
  const state = issue.state?.name || "no state";
  const assignee = issue.assignee?.name ? ` @${issue.assignee.name}` : " unassigned";
  const project = issue.project?.name ? ` - ${issue.project.name}` : "";
  return `${issue.identifier} [${state}/${priority}]${assignee}${project} - ${issue.title}`;
}

function fmtIssueDetails(issue) {
  const lines = [
    fmtIssue(issue),
    issue.url,
  ];
  if (issue.description) lines.push("", issue.description);
  return lines.join("\n");
}

function fmtIssueList(data) {
  const nodes = data.issues?.nodes || data.nodes || [];
  if (!nodes.length) return "No issues found.";
  return nodes.map(fmtIssue).join("\n");
}

async function resolveIssue(identifier) {
  const data = await graphql(`
    query Issue($id: String!) {
      issue(id: $id) {
        id identifier title description url priority priorityLabel updatedAt
        state { id name type }
        assignee { id name email }
        team { id key name }
        project { id name }
      }
    }`, { id: identifier });
  if (!data.issue) die(`issue not found: ${identifier}`);
  return data.issue;
}

async function resolveTeam(teamKey) {
  if (!teamKey) die("team key is required. Pass one explicitly or set LINEAR_DEFAULT_TEAM.");
  const data = await graphql(`
    query Team($key: String!) {
      teams(filter: { key: { eq: $key } }, first: 1) {
        nodes { id key name states { nodes { id name type position } } }
      }
    }`, { key: teamKey });
  const team = data.teams.nodes[0];
  if (!team) die(`team not found: ${teamKey}`);
  return team;
}

function findState(team, stateName) {
  const wanted = stateName.toLowerCase();
  const state = team.states.nodes.find(s => s.name.toLowerCase() === wanted);
  if (!state) {
    const names = team.states.nodes.map(s => s.name).join(", ");
    die(`state not found on ${team.key}: ${stateName}. Available states: ${names}`);
  }
  return state;
}

async function cmdViewer(json) {
  const data = await graphql(`query { viewer { id name email displayName } }`);
  print(data.viewer, json, v => `${v.name || v.displayName} <${v.email || "no email"}>`);
}

async function cmdOrganization(json) {
  const data = await graphql(`query { organization { id name urlKey createdAt } }`);
  print(data.organization, json, o => `${o.name} (${o.urlKey})`);
}

async function cmdTeams(json) {
  const data = await graphql(`query { teams(first: 100) { nodes { id key name description } } }`);
  print(data.teams.nodes, json, teams => teams.map(t => `${t.key} - ${t.name}`).join("\n") || "No teams found.");
}

function fmtProject(project) {
  const teams = project.teams?.nodes?.map(t => t.key).join(",") || "no-team";
  const state = project.state || "unknown";
  const target = project.targetDate ? ` - target ${project.targetDate}` : "";
  return `${project.name} [${state}] (${teams})${target} - ${project.url || project.id}`;
}

function fmtProjectList(projects) {
  if (!projects.length) return "No projects found.";
  return projects.map(fmtProject).join("\n");
}

async function cmdProjects(args, json) {
  const teamKey = takeFlag(args, "--team", getEnv("LINEAR_DEFAULT_TEAM") || null);
  const limit = takeLimit(args, 25);
  if (args.length) die(`unknown args for projects: ${args.join(" ")}`);

  if (teamKey) {
    const data = await graphql(`
      query TeamProjects($key: String!, $limit: Int!) {
        teams(filter: { key: { eq: $key } }, first: 1) {
          nodes {
            key name
            projects(first: $limit) {
              nodes { id name description url state startDate targetDate updatedAt teams { nodes { key name } } }
            }
          }
        }
      }`, { key: teamKey, limit });
    const team = data.teams.nodes[0];
    if (!team) die(`team not found: ${teamKey}`);
    return print(team.projects.nodes, json, fmtProjectList);
  }

  const data = await graphql(`
    query Projects($limit: Int!) {
      projects(first: $limit) {
        nodes { id name description url state startDate targetDate updatedAt teams { nodes { key name } } }
      }
    }`, { limit });
  print(data.projects.nodes, json, fmtProjectList);
}

async function cmdProjectCreate(args, json) {
  const defaultTeam = getEnv("LINEAR_DEFAULT_TEAM");
  let teamKey;
  let name;
  let description = "";
  if (args.length >= 2) {
    teamKey = args.shift();
    name = args.shift();
    description = args.shift() || "";
  } else if (args.length === 1 && defaultTeam) {
    teamKey = defaultTeam;
    name = args.shift();
  } else {
    die('project-create requires TEAM_KEY "Name" ["Description"] (or set LINEAR_DEFAULT_TEAM and pass "Name")');
  }
  if (args.length) die(`unknown extra args for project-create: ${args.join(" ")}`);
  const team = await resolveTeam(teamKey);
  const data = await graphql(`
    mutation CreateProject($input: ProjectCreateInput!) {
      projectCreate(input: $input) {
        success
        project { id name description url state startDate targetDate updatedAt teams { nodes { key name } } }
      }
    }`, { input: { name, description, teamIds: [team.id] } });
  if (!data.projectCreate.success) die("Linear did not create the project.");
  print(data.projectCreate.project, json, p => `created project ${fmtProject(p)}`);
}

async function cmdStates(args, json) {
  const [teamKey] = requireExactArgs("states", args, 1, "<TEAM_KEY>");
  const team = await resolveTeam(teamKey);
  print(team.states.nodes, json, states => states.sort((a, b) => a.position - b.position).map(s => `${s.name} (${s.type})`).join("\n") || `No states found for ${team.key}.`);
}

async function getViewerIdIfMine(mine) {
  if (!mine) return null;
  const data = await graphql(`query { viewer { id } }`);
  return data.viewer.id;
}

function buildIssueQuery({ team, mineId, state, stateTypes, urgent }) {
  if (state && stateTypes?.length) die("state name and state type filters are mutually exclusive");
  const filterParts = [];
  const variableDefs = ["$limit: Int!"];
  const variables = {};

  if (team) {
    variableDefs.push("$team: String!");
    filterParts.push(`team: { key: { eq: $team } }`);
    variables.team = team;
  }
  if (mineId) {
    variableDefs.push("$mineId: ID!");
    filterParts.push(`assignee: { id: { eq: $mineId } }`);
    variables.mineId = mineId;
  }
  if (state) {
    variableDefs.push("$state: String!");
    filterParts.push(`state: { name: { eq: $state } }`);
    variables.state = state;
  }
  if (stateTypes?.length) {
    variableDefs.push("$stateTypes: [String!]!");
    filterParts.push(`state: { type: { in: $stateTypes } }`);
    variables.stateTypes = stateTypes;
  }
  if (urgent) filterParts.push(`priority: { eq: 1 }`);

  const filter = filterParts.length ? `filter: { ${filterParts.join(", ")} },` : "";
  return {
    query: `
    query Issues(${variableDefs.join(", ")}) {
      issues(${filter} first: $limit, orderBy: updatedAt) {
        nodes {
          id identifier title url priority priorityLabel updatedAt
          state { id name type }
          assignee { id name email }
          team { id key name }
          project { id name }
        }
      }
    }`,
    variables
  };
}

async function queryIssues(opts) {
  const { query, variables } = buildIssueQuery(opts);
  return graphql(query, { ...variables, limit: opts.limit });
}

async function cmdIssues(args, json) {
  const team = takeFlag(args, "--team", getEnv("LINEAR_DEFAULT_TEAM") || null);
  const state = takeFlag(args, "--state", null);
  const limit = takeLimit(args, 25);
  const mine = takeBool(args, "--mine");
  if (args.length) die(`unknown args for issues: ${args.join(" ")}`);
  const mineId = await getViewerIdIfMine(mine);
  const data = await queryIssues({ team, state, limit, mineId });
  print(data, json, fmtIssueList);
}

async function cmdMyIssues(args, json) {
  const team = takeFlag(args, "--team", getEnv("LINEAR_DEFAULT_TEAM") || null);
  const state = takeFlag(args, "--state", null);
  const limit = takeLimit(args, 25);
  if (args.length) die(`unknown args for my-issues: ${args.join(" ")}`);
  const mineId = await getViewerIdIfMine(true);
  const data = await queryIssues({ team, state, limit, mineId });
  print(data, json, fmtIssueList);
}

async function cmdMyTodos(args, json) {
  const team = takeFlag(args, "--team", getEnv("LINEAR_DEFAULT_TEAM") || null);
  const limit = takeLimit(args, 25);
  if (args.length) die(`unknown args for my-todos: ${args.join(" ")}`);
  const mineId = await getViewerIdIfMine(true);
  const data = await queryIssues({ team, limit, mineId, stateTypes: ["unstarted", "started"] });
  print(data, json, fmtIssueList);
}

async function cmdUrgent(args, json) {
  const team = takeFlag(args, "--team", getEnv("LINEAR_DEFAULT_TEAM") || null);
  const mine = takeBool(args, "--mine");
  const limit = takeLimit(args, 25);
  if (args.length) die(`unknown args for urgent: ${args.join(" ")}`);
  const mineId = await getViewerIdIfMine(mine);
  const data = await queryIssues({ team, limit, mineId, urgent: true });
  print(data, json, fmtIssueList);
}

async function cmdIssue(args, json) {
  const [identifier] = requireExactArgs("issue", args, 1, "<IDENTIFIER>, e.g. ENG-123");
  const issue = await resolveIssue(identifier);
  print(issue, json, fmtIssueDetails);
}

async function cmdCreate(args, json) {
  const priorityName = takeFlag(args, "--priority", "none");
  const priority = priorityValue(priorityName);
  const defaultTeam = getEnv("LINEAR_DEFAULT_TEAM");
  let teamKey;
  let title;
  let description = "";
  if (args.length >= 2) {
    teamKey = args.shift();
    title = args.shift();
    description = args.shift() || "";
  } else if (args.length === 1 && defaultTeam) {
    teamKey = defaultTeam;
    title = args.shift();
  } else {
    die('create requires TEAM_KEY and "Title" (or set LINEAR_DEFAULT_TEAM and pass "Title")');
  }
  if (args.length) die(`unknown extra args for create: ${args.join(" ")}`);
  const team = await resolveTeam(teamKey);
  const data = await graphql(`
    mutation CreateIssue($input: IssueCreateInput!) {
      issueCreate(input: $input) {
        success
        issue { id identifier title url priority priorityLabel state { name type } assignee { name } team { key name } project { name } }
      }
    }`, { input: { teamId: team.id, title, description, priority } });
  if (!data.issueCreate.success) die("Linear did not create the issue.");
  print(data.issueCreate.issue, json, i => `created ${fmtIssue(i)}\n${i.url}`);
}

async function cmdComment(args, json) {
  const [identifier, body] = requireExactArgs("comment", args, 2, '<IDENTIFIER> "Comment"');
  const issue = await resolveIssue(identifier);
  const data = await graphql(`
    mutation Comment($input: CommentCreateInput!) {
      commentCreate(input: $input) { success comment { id url body createdAt } }
    }`, { input: { issueId: issue.id, body } });
  if (!data.commentCreate.success) die("Linear did not create the comment.");
  print(data.commentCreate.comment, json, c => `commented on ${issue.identifier} - ${c.url || "no url"}`);
}

async function cmdStatus(args, json) {
  const [identifier, stateName] = requireExactArgs("status", args, 2, "<IDENTIFIER> <state-name>");
  const issue = await resolveIssue(identifier);
  const team = await resolveTeam(issue.team.key);
  const state = findState(team, stateName);
  const data = await graphql(`
    mutation UpdateIssue($id: String!, $input: IssueUpdateInput!) {
      issueUpdate(id: $id, input: $input) { success issue { id identifier title url priority priorityLabel state { name type } assignee { name } team { key name } project { name } } }
    }`, { id: issue.id, input: { stateId: state.id } });
  if (!data.issueUpdate.success) die("Linear did not update the issue status.");
  print(data.issueUpdate.issue, json, i => `updated ${i.identifier} status -> ${i.state.name}`);
}

async function cmdPriority(args, json) {
  const [identifier, priorityName] = requireExactArgs("priority", args, 2, "<IDENTIFIER> <urgent|high|medium|low|none>");
  const priority = priorityValue(priorityName);
  const issue = await resolveIssue(identifier);
  const data = await graphql(`
    mutation UpdateIssue($id: String!, $input: IssueUpdateInput!) {
      issueUpdate(id: $id, input: $input) { success issue { id identifier title url priority priorityLabel state { name type } assignee { name } team { key name } project { name } } }
    }`, { id: issue.id, input: { priority } });
  if (!data.issueUpdate.success) die("Linear did not update the issue priority.");
  print(data.issueUpdate.issue, json, i => `updated ${i.identifier} priority -> ${i.priorityLabel || PRIORITY_LABELS.get(i.priority)}`);
}

function slugify(text) {
  return String(text || "")
    .toLowerCase()
    .replace(/['']/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 70)
    .replace(/-+$/g, "");
}

async function cmdBranch(args, json) {
  const [identifier] = requireExactArgs("branch", args, 1, "<IDENTIFIER>");
  const issue = await resolveIssue(identifier);
  const branch = `${issue.identifier.toLowerCase()}-${slugify(issue.title)}`;
  print({ branch, issue }, json, x => x.branch);
}

async function cmdStandup(args, json) {
  const team = takeFlag(args, "--team", getEnv("LINEAR_DEFAULT_TEAM") || null);
  const limit = takeLimit(args, 20);
  if (args.length) die(`unknown args for standup: ${args.join(" ")}`);
  const mineId = await getViewerIdIfMine(true);
  const data = await queryIssues({ team, limit, mineId, stateTypes: ["started", "completed"] });
  if (json) return print(data, true, () => "");
  const nodes = data.issues.nodes;
  const active = nodes.filter(i => i.state?.type === "started");
  const completed = nodes.filter(i => i.state?.type === "completed");
  const section = (title, items) => `${title}\n${items.length ? items.map(i => `- ${fmtIssue(i)}`).join("\n") : "- None"}`;
  process.stdout.write([section("Active", active), section("Recently completed", completed)].join("\n\n") + "\n");
}

function printHelp() {
  process.stdout.write(`Linear Native Node helper\n\nUsage:\n  node scripts/linear.mjs <command> [args] [--json]\n\nRead-only commands:\n  viewer                                      Show the authenticated Linear user\n  organization                                Show the workspace organization\n  teams                                       List workspace teams\n  projects [--team TEAM] [--limit N]          List projects, optionally scoped to a team\n  states <TEAM_KEY>                           List workflow states for a team\n  issues [--team TEAM] [--mine] [--state STATE] [--limit N]\n                                              List issues with optional filters\n  my-issues [--team TEAM] [--state STATE] [--limit N]\n                                              List issues assigned to the viewer\n  my-todos [--team TEAM] [--limit N]          List assigned unstarted/started issues\n  urgent [--team TEAM] [--mine] [--limit N]   List urgent issues\n  standup [--team TEAM] [--limit N]           Summarize assigned active/recently completed work\n  issue <IDENTIFIER>                          Show issue details, e.g. TEAM-123\n  branch <IDENTIFIER>                         Print a branch slug from an issue title\n\nWrite commands:\n  project-create [TEAM_KEY] "Name" ["Description"]\n                                              Create a project; TEAM_KEY may come from LINEAR_DEFAULT_TEAM\n  create [TEAM_KEY] "Title" ["Description"] [--priority urgent|high|medium|low|none]\n                                              Create an issue; TEAM_KEY may come from LINEAR_DEFAULT_TEAM\n  comment <IDENTIFIER> "Comment"             Add a comment to an issue\n  status <IDENTIFIER> <state-name>            Move an issue to a workflow state\n  priority <IDENTIFIER> <urgent|high|medium|low|none>\n                                              Update issue priority\n\nGlobal flags:\n  --json                                      Print JSON where supported\n  --execute                                   Required for write commands after explicit approval\n  -h, --help, help                            Show this help\n\nCredentials:\n  LINEAR_API_KEY from process environment\n  Optional LINEAR_DEFAULT_TEAM, e.g. TEAM\n`);
}

async function main() {
  const parsed = parseGlobal(process.argv.slice(2));
  const args = parsed.args;
  const command = (args.shift() || "help").toLowerCase();
  if (WRITE_COMMANDS.has(command) && !parsed.execute) dieNoExecute(command);
  switch (command) {
    case "help":
    case "-h":
    case "--help": return printHelp();
    case "viewer": return cmdViewer(parsed.json);
    case "organization": return cmdOrganization(parsed.json);
    case "teams": return cmdTeams(parsed.json);
    case "projects": return cmdProjects(args, parsed.json);
    case "project-create": return cmdProjectCreate(args, parsed.json);
    case "states": return cmdStates(args, parsed.json);
    case "issues": return cmdIssues(args, parsed.json);
    case "my-issues": return cmdMyIssues(args, parsed.json);
    case "my-todos": return cmdMyTodos(args, parsed.json);
    case "urgent": return cmdUrgent(args, parsed.json);
    case "standup": return cmdStandup(args, parsed.json);
    case "issue": return cmdIssue(args, parsed.json);
    case "create": return cmdCreate(args, parsed.json);
    case "comment": return cmdComment(args, parsed.json);
    case "status": return cmdStatus(args, parsed.json);
    case "priority": return cmdPriority(args, parsed.json);
    case "branch": return cmdBranch(args, parsed.json);
    default: die(`unknown command: ${command}. Try help.`);
  }
}

main().catch(err => die(err?.message || String(err)));
