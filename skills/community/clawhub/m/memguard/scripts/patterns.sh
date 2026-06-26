#!/usr/bin/env bash
# MemGuard -- Resource Leak Detection Pattern Definitions
# Each pattern: REGEX|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION
#
# Severity levels:
#   critical -- Resource leaks that can crash production systems or exhaust OS resources
#   high     -- Leaks that degrade performance significantly over time
#   medium   -- Potential leaks that may accumulate under sustained load
#   low      -- Informational, minor resource hygiene issues
#
# IMPORTANT: All regexes must use POSIX ERE syntax (grep -E compatible).
# - Use [[:space:]] instead of \s
# - Use [[:alnum:]] instead of \w
# - Avoid Perl-only features (\d, \w, etc.)
#
# Categories:
#   FH -- File Handles (FH-001 to FH-015)
#   EL -- Event Listeners (EL-001 to EL-015)
#   CR -- Circular References (CR-001 to CR-015)
#   UC -- Unbounded Caches (UC-001 to UC-015)
#   RC -- React Cleanup (RC-001 to RC-015)
#   TM -- Timers & Streams (TM-001 to TM-015)

set -euo pipefail

# ============================================================================
# 1. FILE HANDLES (FH-001 through FH-015)
# ============================================================================

declare -a MEMGUARD_FH_PATTERNS=()

MEMGUARD_FH_PATTERNS+=(
  # --- Python open() without with statement ---
  '[^#][[:space:]]*[[:alnum:]_]+[[:space:]]*=[[:space:]]*open[[:space:]]*\(|critical|FH-001|Python open() call not using context manager (with statement)|Use "with open(...) as f:" to ensure the file is automatically closed'

  # --- Java FileInputStream without try-with-resources ---
  'new[[:space:]]+File(Input|Output)Stream[[:space:]]*\(|critical|FH-002|Java FileInputStream/FileOutputStream created without try-with-resources|Wrap in try-with-resources: try (var fis = new FileInputStream(...)) { ... }'

  # --- Node.js fs.open without corresponding close ---
  'fs\.(open|openSync)[[:space:]]*\(|high|FH-003|Node.js fs.open() call -- ensure matching fs.close() exists|Always call fs.close(fd) in a finally block or use fs.promises with try/finally'

  # --- Node.js fs.createReadStream without close/destroy ---
  'fs\.create(Read|Write)Stream[[:space:]]*\(|high|FH-004|Node.js fs.createReadStream/WriteStream -- ensure stream is closed or destroyed|Listen for the close event or call stream.destroy() in error handlers'

  # --- Python cursor without close ---
  '\.cursor[[:space:]]*\([[:space:]]*\)|high|FH-005|Database cursor created -- ensure it is closed after use|Use "with connection.cursor() as cur:" or explicitly call cursor.close() in finally'

  # --- Java JDBC Connection without close ---
  'DriverManager\.getConnection[[:space:]]*\(|critical|FH-006|JDBC Connection.getConnection() -- must be closed after use|Wrap in try-with-resources or use a connection pool that manages lifecycle'

  # --- Java PreparedStatement without close ---
  '\.prepareStatement[[:space:]]*\(|high|FH-007|JDBC PreparedStatement created -- ensure it is closed|Wrap in try-with-resources: try (var ps = conn.prepareStatement(...)) { ... }'

  # --- C# FileStream without using statement ---
  'new[[:space:]]+FileStream[[:space:]]*\(|high|FH-008|C# FileStream created -- ensure using statement or Dispose() is called|Wrap in using statement: using (var fs = new FileStream(...)) { ... }'

  # --- C# StreamReader/StreamWriter without using ---
  'new[[:space:]]+Stream(Reader|Writer)[[:space:]]*\(|high|FH-009|C# StreamReader/StreamWriter created without using statement|Wrap in using statement to ensure proper disposal'

  # --- Go os.Open without defer Close ---
  'os\.(Open|Create)[[:space:]]*\(|high|FH-010|Go os.Open()/os.Create() -- ensure defer file.Close() follows|Add "defer f.Close()" immediately after error check'

  # --- Python tempfile without cleanup ---
  'tempfile\.(mktemp|NamedTemporaryFile|mkdtemp)[[:space:]]*\(|medium|FH-011|Python tempfile creation -- ensure cleanup occurs|Use tempfile as context manager or ensure os.remove() / shutil.rmtree() in finally'

  # --- Java BufferedReader/Writer without close ---
  'new[[:space:]]+Buffered(Reader|Writer)[[:space:]]*\(|high|FH-012|Java BufferedReader/Writer created -- ensure it is closed|Wrap in try-with-resources to ensure automatic closing'

  # --- Rust File::open without proper handling ---
  'File::open[[:space:]]*\(|medium|FH-013|Rust File::open() -- ensure file handle is properly dropped or closed|Let the File go out of scope to auto-close, or explicitly call drop(file)'

  # --- Python sqlite3.connect without close ---
  'sqlite3\.connect[[:space:]]*\(|high|FH-014|Python sqlite3 connection created -- ensure it is closed|Use "with sqlite3.connect(...) as conn:" or call conn.close() in finally'

  # --- Generic database connection without close ---
  '\.(connect|createConnection|getConnection|createPool)[[:space:]]*\(|high|FH-015|Database connection/pool created -- ensure proper cleanup|Close connections in finally blocks or use connection pooling with proper lifecycle'
)

# ============================================================================
# 2. EVENT LISTENERS (EL-001 through EL-015)
# ============================================================================

declare -a MEMGUARD_EL_PATTERNS=()

MEMGUARD_EL_PATTERNS+=(
  # --- addEventListener without removeEventListener ---
  '\.addEventListener[[:space:]]*\(|high|EL-001|addEventListener() called -- ensure matching removeEventListener() exists|Store the handler reference and call removeEventListener() in cleanup/unmount'

  # --- jQuery/Node .on() event binding ---
  '\.(on)[[:space:]]*\([[:space:]]*['"'"'"][[:alnum:]]+['"'"'"]|high|EL-002|Event listener bound with .on() -- ensure matching .off() exists|Call .off() with the same event name and handler in cleanup code'

  # --- window/document event listener ---
  '(window|document)\.addEventListener[[:space:]]*\(|high|EL-003|Global window/document event listener -- must be removed on cleanup|Always remove global event listeners in componentWillUnmount, useEffect cleanup, or destroy lifecycle'

  # --- Python signal.connect (Qt/Django signals) ---
  '\.connect[[:space:]]*\([[:space:]]*self\.|medium|EL-004|Signal.connect() with self reference -- ensure disconnect on cleanup|Call signal.disconnect() in cleanup/destructor to prevent retained references'

  # --- Node.js EventEmitter .on without .removeListener ---
  'emitter\.(on|addListener)[[:space:]]*\(|high|EL-005|EventEmitter listener added -- ensure .removeListener() or .off() in cleanup|Remove the listener when the subscriber is done to prevent emitter memory leaks'

  # --- Java addPropertyChangeListener ---
  'add(Property|Change|Action|Mouse|Key|Focus|Window)Listener[[:space:]]*\(|medium|EL-006|Java event listener added -- ensure corresponding removeListener exists|Call remove*Listener() in dispose or cleanup method'

  # --- C# event += subscription ---
  '[[:alnum:]_]+[[:space:]]*\+=[[:space:]]*[[:alnum:]_]+|medium|EL-007|C# event subscription with += -- ensure -= unsubscribe in Dispose|Implement IDisposable and unsubscribe with -= in Dispose() method'

  # --- RxJS subscribe without unsubscribe ---
  '\.subscribe[[:space:]]*\(|high|EL-008|RxJS/Observable subscribe() -- ensure unsubscribe in cleanup|Store subscription and call .unsubscribe() in ngOnDestroy or useEffect cleanup'

  # --- Vue.js $on without $off ---
  '\$on[[:space:]]*\(|high|EL-009|Vue.js $on event binding -- ensure matching $off exists|Call this.$off() in beforeDestroy or beforeUnmount lifecycle hook'

  # --- Angular Renderer2 listen without unlisten ---
  'renderer[[:alnum:]]*\.listen[[:space:]]*\(|high|EL-010|Angular Renderer.listen() -- store and call unlisten function|Store the return value and call it in ngOnDestroy to remove the listener'

  # --- MutationObserver without disconnect ---
  'new[[:space:]]+MutationObserver[[:space:]]*\(|high|EL-011|MutationObserver created -- ensure .disconnect() is called on cleanup|Call observer.disconnect() in cleanup/unmount to stop observing'

  # --- IntersectionObserver without disconnect ---
  'new[[:space:]]+IntersectionObserver[[:space:]]*\(|high|EL-012|IntersectionObserver created -- ensure .disconnect() is called|Call observer.disconnect() in cleanup to prevent retained DOM references'

  # --- ResizeObserver without disconnect ---
  'new[[:space:]]+ResizeObserver[[:space:]]*\(|high|EL-013|ResizeObserver created -- ensure .disconnect() is called|Call observer.disconnect() in cleanup to free observed elements'

  # --- PerformanceObserver without disconnect ---
  'new[[:space:]]+PerformanceObserver[[:space:]]*\(|medium|EL-014|PerformanceObserver created -- ensure .disconnect() is called|Call observer.disconnect() when monitoring is no longer needed'

  # --- WebSocket onmessage without close ---
  'new[[:space:]]+WebSocket[[:space:]]*\(|high|EL-015|WebSocket created -- ensure .close() is called on cleanup|Call ws.close() in cleanup/unmount to properly close the connection'
)

# ============================================================================
# 3. CIRCULAR REFERENCES (CR-001 through CR-015)
# ============================================================================

declare -a MEMGUARD_CR_PATTERNS=()

MEMGUARD_CR_PATTERNS+=(
  # --- Parent-child circular reference (this.parent = parent) ---
  'this\.parent[[:space:]]*=[[:space:]]|high|CR-001|Parent reference stored on child object -- potential circular reference|Use WeakRef for parent references or restructure to avoid bidirectional ownership'

  # --- Self-referencing object (this.self / this.instance) ---
  'this\.(self|instance|ref|me)[[:space:]]*=[[:space:]]*this|high|CR-002|Self-referencing object pattern detected -- circular reference|Remove the self-reference or use a WeakRef if the reference is truly needed'

  # --- Circular class attribute references in Python ---
  'self\.[[:alnum:]_]+[[:space:]]*=[[:space:]]*[[:alnum:]_]+[[:space:]]*$|medium|CR-003|Python self attribute assignment -- check for mutual references between objects|Use weakref.ref() for back-references between objects to allow garbage collection'

  # --- Closure capturing this/self into child ---
  'child\.[[:alnum:]_]*parent|medium|CR-004|Child object storing parent reference -- potential circular reference chain|Use WeakRef or event-based communication instead of direct parent references'

  # --- Map/Set storing objects with potential back-references ---
  '\.set[[:space:]]*\([[:space:]]*[[:alnum:]_]+[[:space:]]*,[[:space:]]*this|medium|CR-005|Map.set() storing this as value -- potential circular reference|Ensure the Map does not create a reference cycle; consider using WeakMap'

  # --- Global singleton with instance reference ---
  'static[[:space:]]+instance[[:space:]]*=|medium|CR-006|Static instance pattern -- verify no circular dependencies with contained objects|Ensure singleton does not hold references that create cycles with its consumers'

  # --- Mutual field references between classes ---
  '\.owner[[:space:]]*=[[:space:]]|medium|CR-007|Owner reference pattern -- bidirectional ownership may cause circular references|Use WeakRef for back-references or decouple with an event/observer pattern'

  # --- Python __del__ with reference cycle ---
  'def[[:space:]]+__del__[[:space:]]*\([[:space:]]*self|high|CR-008|Python __del__ destructor defined -- reference cycles prevent __del__ from running|Avoid __del__ in classes that may be part of reference cycles; use weakref.finalize()'

  # --- Node/DOM element with data pointing back to component ---
  '\.(dataset|data)[[:space:]]*\.[[:alnum:]_]+[[:space:]]*=[[:space:]]*this|medium|CR-009|DOM element data attribute referencing component -- DOM-JS circular reference|Use a WeakMap keyed by the element instead of storing references on the element'

  # --- React ref storing component reference ---
  'ref\.current[[:space:]]*=[[:space:]]|medium|CR-010|React ref.current assignment -- ensure ref is cleared on unmount|Set ref.current = null in useEffect cleanup to prevent retained component references'

  # --- Prototype chain circular reference ---
  '\.prototype\.[[:alnum:]_]+[[:space:]]*=[[:space:]]*new|medium|CR-011|Prototype property assigned new object -- verify no circular prototype chain|Ensure prototype assignments do not create circular inheritance chains'

  # --- Bidirectional list (prev/next with mutual refs) ---
  '\.(prev|previous)[[:space:]]*=[[:space:]]|low|CR-012|Doubly-linked list pattern (prev assignment) -- inherent circular reference|This is expected for linked lists but ensure proper cleanup when removing nodes'

  # --- Cache storing computed result that references source ---
  'cache\.(set|put)[[:space:]]*\(.*this|medium|CR-013|Cache storing reference to this -- may prevent garbage collection|Use WeakMap for caches that key or value-reference their owners'

  # --- Python circular import detection ---
  'from[[:space:]]+\.[[:alnum:]_]+[[:space:]]+import|low|CR-014|Relative import pattern -- circular imports can cause issues in Python|Restructure modules to avoid circular imports; use lazy imports if needed'

  # --- Closure referencing outer function scope ---
  'function[[:space:]]*\([^)]*\)[[:space:]]*\{[^}]*function[[:space:]]*\(|medium|CR-015|Nested function closure -- inner function retains reference to outer scope|Be aware of closure scope retention; nullify large outer variables if no longer needed'
)

# ============================================================================
# 4. UNBOUNDED CACHES (UC-001 through UC-015)
# ============================================================================

declare -a MEMGUARD_UC_PATTERNS=()

MEMGUARD_UC_PATTERNS+=(
  # --- Module-level Map without cleanup ---
  '^(const|let|var)[[:space:]]+[[:alnum:]_]+[[:space:]]*=[[:space:]]*new[[:space:]]+Map[[:space:]]*\(|high|UC-001|Module-level Map created without eviction policy -- unbounded growth risk|Add a max size limit or TTL-based eviction strategy to prevent unbounded growth'

  # --- Module-level Set without cleanup ---
  '^(const|let|var)[[:space:]]+[[:alnum:]_]+[[:space:]]*=[[:space:]]*new[[:space:]]+Set[[:space:]]*\(|high|UC-002|Module-level Set created without eviction policy -- unbounded growth risk|Add a max size limit or periodic cleanup to prevent unbounded growth'

  # --- Python global dict used as cache ---
  '^[[:alnum:]_]+[[:space:]]*=[[:space:]]*\{\}[[:space:]]*#.*cache|high|UC-003|Python global dict used as cache -- unbounded growth risk|Use functools.lru_cache or cachetools.TTLCache with a max size'

  # --- In-memory cache object without TTL ---
  '(cache|CACHE|Cache)[[:space:]]*=[[:space:]]*\{|medium|UC-004|In-memory cache object initialized -- verify TTL or max size is enforced|Implement eviction policy (LRU, TTL) or use a library with built-in limits'

  # --- Array push in loop pattern ---
  '\.(push|append|add)[[:space:]]*\([^)]+\)[[:space:]]*;?[[:space:]]*$|medium|UC-005|Collection append pattern -- verify this is not inside an unbounded loop|Ensure array/list growth is bounded; add a max size check or periodic trimming'

  # --- Memoization without size limit ---
  'memoize[[:space:]]*\(|medium|UC-006|Memoization function called -- verify cache has a max size limit|Use memoization libraries with size limits (lodash.memoize with resolver, lru-cache)'

  # --- localStorage/sessionStorage setItem accumulating ---
  'localStorage\.setItem[[:space:]]*\(|medium|UC-007|localStorage.setItem() -- verify storage is periodically cleaned up|Implement a storage cleanup strategy; localStorage has a ~5MB limit per origin'

  # --- Global array accumulating data ---
  '^(const|let|var|)[[:space:]]*[[:alnum:]_]*(log|history|events|queue|buffer|items|list|records)[[:space:]]*=[[:space:]]*\[\]|high|UC-008|Global array for accumulating data -- unbounded growth risk|Add max size limits, periodic trimming, or use a circular buffer'

  # --- Python @lru_cache without maxsize ---
  '@lru_cache[[:space:]]*$|medium|UC-009|Python @lru_cache without maxsize parameter -- unbounded cache|Specify maxsize: @lru_cache(maxsize=128) to limit memory usage'

  # --- @lru_cache(maxsize=None) -- explicitly unbounded ---
  '@lru_cache[[:space:]]*\([[:space:]]*maxsize[[:space:]]*=[[:space:]]*None|high|UC-010|Python @lru_cache with maxsize=None -- explicitly unbounded cache|Set a finite maxsize to prevent unbounded memory growth'

  # --- Node.js require-level object accumulating ---
  'module\.(exports\.)?[[:alnum:]_]*(cache|store|registry|pool)[[:space:]]*=[[:space:]]*\{|medium|UC-011|Module-exported cache/store object -- verify eviction strategy exists|Implement TTL or LRU eviction to prevent unbounded module-level caches'

  # --- Java static HashMap/ConcurrentHashMap without eviction ---
  'static[[:space:]]+(final[[:space:]]+)?[[:alnum:]<>,[:space:]]*(Map|HashMap|ConcurrentHashMap|HashSet)[[:space:]]*[<>[:alnum:][:space:],]*[[:alnum:]_]+[[:space:]]*=|high|UC-012|Java static Map/Set -- unbounded growth risk without eviction|Use Caffeine, Guava Cache, or ConcurrentHashMap with size-bounded eviction'

  # --- C# static Dictionary without eviction ---
  'static[[:space:]]+(readonly[[:space:]]+)?Dictionary[[:space:]]*<|high|UC-013|C# static Dictionary -- unbounded growth risk|Use MemoryCache with expiration policies instead of static dictionaries'

  # --- Go map at package level without cleanup ---
  '^var[[:space:]]+[[:alnum:]_]+[[:space:]]*=[[:space:]]*map\[|high|UC-014|Go package-level map -- unbounded growth risk|Add periodic cleanup or use a bounded cache implementation (groupcache, ristretto)'

  # --- Redis/Memcached set without TTL ---
  '\.(set|hset|sadd)[[:space:]]*\([^,)]+,[[:space:]]*[^,)]+\)[[:space:]]*$|medium|UC-015|Cache set/write without TTL -- entries may accumulate indefinitely|Always specify a TTL when writing to Redis/Memcached to prevent unbounded growth'
)

# ============================================================================
# 5. REACT CLEANUP (RC-001 through RC-015)
# ============================================================================

declare -a MEMGUARD_RC_PATTERNS=()

MEMGUARD_RC_PATTERNS+=(
  # --- useEffect without cleanup return ---
  'useEffect[[:space:]]*\([[:space:]]*\([[:space:]]*\)[[:space:]]*=>[[:space:]]*\{|medium|RC-001|useEffect callback -- verify it returns a cleanup function if it creates subscriptions|Add a return () => { cleanup } statement to useEffect for proper resource cleanup'

  # --- setInterval inside useEffect ---
  'useEffect.*setInterval|critical|RC-002|setInterval inside useEffect -- must have clearInterval in cleanup|Return a cleanup function: return () => clearInterval(intervalId)'

  # --- setTimeout inside useEffect ---
  'useEffect.*setTimeout|high|RC-003|setTimeout inside useEffect -- should have clearTimeout in cleanup|Return a cleanup function: return () => clearTimeout(timeoutId)'

  # --- addEventListener inside useEffect ---
  'useEffect.*addEventListener|high|RC-004|addEventListener inside useEffect -- must have removeEventListener in cleanup|Return: () => element.removeEventListener(event, handler)'

  # --- subscribe inside useEffect ---
  'useEffect.*\.subscribe|high|RC-005|Subscription created inside useEffect -- must unsubscribe in cleanup|Return: () => subscription.unsubscribe()'

  # --- WebSocket inside useEffect ---
  'useEffect.*new[[:space:]]+WebSocket|high|RC-006|WebSocket created inside useEffect -- must close in cleanup|Return: () => ws.close() to properly close the WebSocket connection'

  # --- fetch/XHR inside useEffect without abort ---
  'useEffect.*fetch[[:space:]]*\(|medium|RC-007|fetch() inside useEffect -- use AbortController for cancellation|Create AbortController, pass signal to fetch, abort in cleanup return'

  # --- setState outside mount check ---
  'setState[[:space:]]*\(.*\)[[:space:]]*;?[[:space:]]*$|medium|RC-008|setState call -- verify component is still mounted before updating state|Use an isMounted flag or AbortController to prevent state updates after unmount'

  # --- EventSource inside useEffect ---
  'useEffect.*new[[:space:]]+EventSource|high|RC-009|EventSource (SSE) created inside useEffect -- must close in cleanup|Return: () => eventSource.close() to stop receiving server-sent events'

  # --- ResizeObserver in useEffect ---
  'useEffect.*ResizeObserver|high|RC-010|ResizeObserver inside useEffect -- must disconnect in cleanup|Return: () => observer.disconnect() to stop observing element sizes'

  # --- MutationObserver in useEffect ---
  'useEffect.*MutationObserver|high|RC-011|MutationObserver inside useEffect -- must disconnect in cleanup|Return: () => observer.disconnect() to stop observing DOM mutations'

  # --- setInterval in class componentDidMount ---
  'componentDidMount.*setInterval|critical|RC-012|setInterval in componentDidMount -- must clearInterval in componentWillUnmount|Store interval ID and call clearInterval(this.intervalId) in componentWillUnmount'

  # --- addEventListener in componentDidMount ---
  'componentDidMount.*addEventListener|high|RC-013|addEventListener in componentDidMount -- must remove in componentWillUnmount|Call removeEventListener with same handler in componentWillUnmount'

  # --- useRef holding external resource ---
  'useRef[[:space:]]*\([[:space:]]*new[[:space:]]|medium|RC-014|useRef initialized with new object -- ensure cleanup in useEffect|If ref holds a resource (WebSocket, Worker, etc.), clean it up in useEffect return'

  # --- requestAnimationFrame in useEffect ---
  'useEffect.*requestAnimationFrame|high|RC-015|requestAnimationFrame inside useEffect -- must cancel in cleanup|Return: () => cancelAnimationFrame(rafId) to stop the animation loop'
)

# ============================================================================
# 6. TIMERS & STREAMS (TM-001 through TM-015)
# ============================================================================

declare -a MEMGUARD_TM_PATTERNS=()

MEMGUARD_TM_PATTERNS+=(
  # --- setInterval without clearInterval ---
  'setInterval[[:space:]]*\(|critical|TM-001|setInterval() called -- ensure matching clearInterval() exists|Store the interval ID and call clearInterval() in cleanup/destroy/unmount'

  # --- setTimeout in loop ---
  '(for|while)[[:space:]]*\(.*setTimeout|high|TM-002|setTimeout inside a loop -- potential timer accumulation|Use a single setTimeout with recursion or ensure proper cancellation on each iteration'

  # --- Stream pipe without error handling ---
  '\.pipe[[:space:]]*\([^)]+\)[[:space:]]*;?[[:space:]]*$|high|TM-003|Stream .pipe() without error event handler -- can cause unhandled stream leak|Add .on("error") handler on both source and destination streams'

  # --- Go goroutine without done/context ---
  'go[[:space:]]+func[[:space:]]*\(|high|TM-004|Go goroutine launched -- ensure done channel or context.Context for lifecycle|Pass a context.Context or done channel to allow goroutine cancellation'

  # --- Go goroutine with anonymous function ---
  'go[[:space:]]+[[:alnum:]_]+[[:space:]]*\(|medium|TM-005|Go goroutine launched (named function) -- ensure proper lifecycle management|Use context.WithCancel or sync.WaitGroup for goroutine coordination'

  # --- Node.js readable stream not destroyed ---
  'new[[:space:]]+Readable[[:space:]]*\(|high|TM-006|Node.js Readable stream created -- ensure .destroy() on error or done|Call stream.destroy() in error handlers to prevent resource leaks'

  # --- Missing stream.end() call ---
  'new[[:space:]]+Writable[[:space:]]*\(|high|TM-007|Node.js Writable stream created -- ensure .end() is called|Call stream.end() when done writing to flush buffers and release resources'

  # --- Python thread without join ---
  'threading\.Thread[[:space:]]*\(|high|TM-008|Python Thread created -- ensure .join() is called for cleanup|Call thread.join() or use daemon=True for threads that should not outlive the process'

  # --- Python subprocess without close/kill ---
  'subprocess\.(Popen|run|call)[[:space:]]*\(|high|TM-009|Python subprocess created -- ensure proper cleanup and resource release|Use context manager or ensure process.kill() and process.wait() in finally block'

  # --- Java ExecutorService without shutdown ---
  '(Executors|ThreadPoolExecutor)\.(new[[:alnum:]]+|fixed|cached|scheduled)[[:space:][:alnum:]]*\(|critical|TM-010|Java ExecutorService created -- must be shut down to release threads|Call executor.shutdown() or executor.shutdownNow() in finally block or @PreDestroy'

  # --- Web Worker without terminate ---
  'new[[:space:]]+Worker[[:space:]]*\(|high|TM-011|Web Worker created -- ensure .terminate() is called on cleanup|Call worker.terminate() when the worker is no longer needed'

  # --- SharedWorker without explicit close ---
  'new[[:space:]]+SharedWorker[[:space:]]*\(|high|TM-012|SharedWorker created -- ensure port.close() on cleanup|Call worker.port.close() when the shared worker connection is no longer needed'

  # --- Python asyncio task without await/cancel ---
  'asyncio\.(create_task|ensure_future)[[:space:]]*\(|high|TM-013|Python asyncio task created -- ensure it is awaited or cancelled|Await the task or call task.cancel() in cleanup to prevent orphaned coroutines'

  # --- Rust spawn without JoinHandle usage ---
  'thread::spawn[[:space:]]*\(|medium|TM-014|Rust thread::spawn() -- ensure JoinHandle is used or thread is detached|Store the JoinHandle and call .join() for cleanup, or explicitly detach'

  # --- C# Timer without Dispose ---
  'new[[:space:]]+Timer[[:space:]]*\(|high|TM-015|C# Timer created -- ensure Dispose() is called on cleanup|Wrap in using statement or call timer.Dispose() in the Dispose pattern'
)

# ============================================================================
# Utility Functions
# ============================================================================

# Get total pattern count across all categories
memguard_pattern_count() {
  local count=0
  count=$((count + ${#MEMGUARD_FH_PATTERNS[@]}))
  count=$((count + ${#MEMGUARD_EL_PATTERNS[@]}))
  count=$((count + ${#MEMGUARD_CR_PATTERNS[@]}))
  count=$((count + ${#MEMGUARD_UC_PATTERNS[@]}))
  count=$((count + ${#MEMGUARD_RC_PATTERNS[@]}))
  count=$((count + ${#MEMGUARD_TM_PATTERNS[@]}))
  echo "$count"
}

# List patterns by category
memguard_list_patterns() {
  local filter_type="${1:-all}"
  local -n _patterns_ref

  case "$filter_type" in
    FH) _patterns_ref=MEMGUARD_FH_PATTERNS ;;
    EL) _patterns_ref=MEMGUARD_EL_PATTERNS ;;
    CR) _patterns_ref=MEMGUARD_CR_PATTERNS ;;
    UC) _patterns_ref=MEMGUARD_UC_PATTERNS ;;
    RC) _patterns_ref=MEMGUARD_RC_PATTERNS ;;
    TM) _patterns_ref=MEMGUARD_TM_PATTERNS ;;
    all)
      memguard_list_patterns "FH"
      memguard_list_patterns "EL"
      memguard_list_patterns "CR"
      memguard_list_patterns "UC"
      memguard_list_patterns "RC"
      memguard_list_patterns "TM"
      return
      ;;
    *)
      echo "Unknown category: $filter_type"
      return 1
      ;;
  esac

  for entry in "${_patterns_ref[@]}"; do
    IFS='|' read -r regex severity check_id description recommendation <<< "$entry"
    printf "%-12s %-8s %s\n" "$check_id" "$severity" "$description"
  done
}

# Get patterns array name for a category
get_memguard_patterns_for_category() {
  local category="$1"
  case "$category" in
    fh) echo "MEMGUARD_FH_PATTERNS" ;;
    el) echo "MEMGUARD_EL_PATTERNS" ;;
    cr) echo "MEMGUARD_CR_PATTERNS" ;;
    uc) echo "MEMGUARD_UC_PATTERNS" ;;
    rc) echo "MEMGUARD_RC_PATTERNS" ;;
    tm) echo "MEMGUARD_TM_PATTERNS" ;;
    *)  echo "" ;;
  esac
}

# All category names for iteration
get_all_memguard_categories() {
  echo "fh el cr uc rc tm"
}

# Category ID to human-readable label
category_to_label() {
  case "$1" in
    FH|fh) echo "File Handles" ;;
    EL|el) echo "Event Listeners" ;;
    CR|cr) echo "Circular References" ;;
    UC|uc) echo "Unbounded Caches" ;;
    RC|rc) echo "React Cleanup" ;;
    TM|tm) echo "Timers & Streams" ;;
    *)     echo "$1" ;;
  esac
}

# Severity to numeric points for scoring
severity_to_points() {
  case "$1" in
    critical) echo 25 ;;
    high)     echo 15 ;;
    medium)   echo 8 ;;
    low)      echo 3 ;;
    *)        echo 0 ;;
  esac
}
