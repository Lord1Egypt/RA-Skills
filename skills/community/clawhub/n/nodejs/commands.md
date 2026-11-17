# Commands — The Node Diagnostic Toolkit

Flags and one-liners that answer a question. Nothing here is a tutorial command; each one replaces a guess with a fact.

## Ask The Process What It Is Doing

```bash
node -p "process.version + ' ' + process.platform + '/' + process.arch"   # runtime identity
node -p "process.execArgv"                                                # flags actually applied
node -p "process.config.variables.node_shared_openssl"                    # build-level facts
node -e "setInterval(()=>console.log(process.getActiveResourcesInfo()),1000)"  # what keeps the loop alive
```

`NODE_OPTIONS` in the environment applies to every child process too — a forgotten `--max-old-space-size` there explains inexplicable memory behavior in tooling.

## Profiling CPU

```bash
node --cpu-prof --cpu-prof-dir=./prof app.js     # writes .cpuprofile on exit; open in DevTools or VS Code
node --prof app.js && node --prof-process isolate-*.log > profile.txt   # no GUI needed, ticks by function
node --inspect app.js                            # attach DevTools live; use --inspect-brk to pause at line 1
```

Read self time, not total time: the widest self-time frame is the code actually running, while the deepest stack is usually a framework's plumbing. Profile under real load for at least 30 s — a cold profile shows module loading.

## Profiling Memory

```bash
node --heap-prof app.js                          # allocation sampling, .heapprofile on exit
node --heapsnapshot-signal=SIGUSR2 app.js        # then: kill -USR2 <pid> for a snapshot on demand
node --trace-gc app.js                           # sawtooth = healthy churn, staircase = leak
node --max-old-space-size=1536 app.js            # heap ceiling in MB (SKILL.md rule 8)
```

Compare two snapshots by retained-size delta per constructor; a single snapshot only tells you what is big, never what is growing.

## Watching The Event Loop

```js
import { monitorEventLoopDelay, performance } from 'node:perf_hooks';
const h = monitorEventLoopDelay({ resolution: 10 });
h.enable();
setInterval(() => console.log({ p50: h.percentile(50) / 1e6, p99: h.percentile(99) / 1e6 }), 5000).unref();
```

Milliseconds after the `/1e6` (the histogram is in nanoseconds). p99 above the 10 ms budget (SKILL.md rule 1) is a blocked loop; export it as a metric and it becomes the earliest saturation signal you have.

## Tracing What Node Is Doing

```bash
node --trace-warnings app.js        # stack for every process warning, including MaxListeners
node --trace-deprecation app.js     # who calls the deprecated API, not just that it happened
node --trace-uncaught app.js        # throw site for non-Error throws
node --trace-exit app.js            # stack for every process.exit() call, including a dependency's
node --trace-sync-io app.js         # sync I/O after the first tick — finds blocking calls in hot paths
node --trace-event-categories node.async_hooks app.js   # trace file for Chrome's tracing viewer
```

## Diagnostic Reports (the crash dump you can read)

```bash
node --report-on-fatalerror --report-on-signal --report-directory=/var/log/node app.js
kill -USR2 <pid>            # write a report from a healthy process
```

The JSON report holds the JS and native stacks, resource usage, libuv handles, environment, and shared libraries at the moment of failure — the only artifact that survives an OOM abort with useful content. Turn it on in production before you need it.

## Runtime Behavior Without Editing Code

```bash
node --env-file=.env app.js               # node >=20.6, no dotenv dependency
node --watch app.js                       # restart on change (node >=22 stable)
node --run build                          # run a package.json script without the package-manager wrapper
UV_THREADPOOL_SIZE=16 node app.js         # libuv pool (SKILL.md rule 3); must be set before the process starts
node --title="api-worker" app.js          # names the process in ps output
```

## Inspecting The Dependency Tree

```bash
npm ls <pkg>                # every path that pulled it; two paths = two module instances
npm ls --depth=0            # what this package directly declares
npm explain <pkg>           # why it is installed at all
npm outdated                # current vs wanted vs latest, per dependency
npm pack --dry-run          # exactly what a publish would ship
```

## Inspecting A Running Container Or Host

```bash
lsof -p <pid> | wc -l                       # open descriptors — compare against ulimit -n (rule 4)
lsof -iTCP:3000 -sTCP:LISTEN -n -P          # who holds the port (EADDRINUSE)
kill -USR1 <pid>                            # opens the inspector on a running process (then --inspect port)
ps -o pid,ppid,rss,etime,command -p <pid>   # RSS and uptime without an APM
```

`kill -USR1` exposes a debugger port: use it on production only through a local tunnel, never on a published port.
