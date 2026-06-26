#!/usr/bin/env bash
# PipelineLint -- CI/CD Pipeline Anti-Pattern Definitions
# 90 patterns across 6 categories, 15 patterns each.
#
# Format per line:
#   REGEX|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION
#
# Severity levels:
#   critical -- Security vulnerability or deployment safety risk
#   high     -- Significant pipeline problem that will cause incorrect behavior
#   medium   -- Moderate concern that should be addressed
#   low      -- Best practice suggestion
#
# IMPORTANT: All regexes use POSIX ERE syntax (grep -E compatible).
# - Use [[:space:]] instead of \s
# - Use [[:alnum:]] instead of \w
# - NEVER use pipe (|) for alternation inside regex -- it conflicts with
#   the field delimiter. Use separate patterns or character classes instead.

set -euo pipefail

# ===========================================================================
# SE -- Secrets & Security (15 patterns: SE-001 to SE-015)
# Free tier
# ===========================================================================

declare -a PIPELINELINT_SE_PATTERNS=(
  'password[[:space:]]*:[[:space:]]*["\x27][^$\{\}][[:alnum:]]+["\x27]|critical|SE-001|Hardcoded password in pipeline YAML configuration|Use secrets manager or encrypted environment variables instead of plain text passwords'
  'api[_-]?key[[:space:]]*:[[:space:]]*["\x27][A-Za-z0-9]{16,}["\x27]|critical|SE-002|API key appears hardcoded in pipeline configuration|Store API keys in CI/CD secrets vault and reference via variable substitution'
  'AKIA[0-9A-Z]{16}|critical|SE-003|AWS Access Key ID hardcoded in pipeline file|Use IAM roles or CI/CD secret variables for AWS credentials'
  'secret[[:space:]]*:[[:space:]]*["\x27][^$\{\}][[:alnum:]]+["\x27]|critical|SE-004|Secret value appears hardcoded in pipeline YAML|Move secrets to a secrets manager and reference via variable interpolation'
  'token[[:space:]]*:[[:space:]]*["\x27][A-Za-z0-9_\-]{20,}["\x27]|high|SE-005|Authentication token hardcoded in pipeline file|Store tokens in CI/CD secret variables and mask in logs'
  'echo[[:space:]].*\$[{(]*[[:alnum:]]*[Ss]ecret|high|SE-006|Secret value may be printed to build logs via echo|Remove echo statements that expose secret variables to build output'
  'printenv|high|SE-007|printenv command dumps all environment variables including secrets|Remove printenv from pipeline scripts to prevent secret leakage'
  'curl[[:space:]].*-u[[:space:]]*[[:alnum:]]+:[[:alnum:]]|high|SE-008|Credentials passed directly in curl command line|Use --netrc-file or environment variable references for curl authentication'
  'Authorization[[:space:]]*:[[:space:]]*["\x27]Bearer[[:space:]][A-Za-z0-9_\-\.]+|high|SE-009|Bearer token hardcoded in Authorization header|Use secret variable substitution for Authorization headers'
  'ssh[_-]?key[[:space:]]*:[[:space:]]*["\x27]|medium|SE-010|SSH key content may be embedded directly in pipeline config|Use CI/CD SSH key management features instead of inline keys'
  '--password[[:space:]]*[= ][[:alnum:]]|medium|SE-011|Password passed as command line argument visible in process list|Use environment variables or stdin for password input'
  'npm_token[[:space:]]*:[[:space:]]*["\x27]|high|SE-012|NPM authentication token hardcoded in pipeline config|Configure NPM token via CI/CD secret variables in .npmrc'
  'GH[POSUposu][[:alnum:]_]{30,}|critical|SE-013|GitHub personal access token or fine-grained token detected|Use GITHUB_TOKEN or GitHub App authentication instead of PATs'
  'set[[:space:]]+-x|medium|SE-014|Shell debug mode (set -x) exposes all commands including secrets|Remove set -x from production pipeline scripts or mask secrets first'
  'docker[[:space:]]login[[:space:]].*-p[[:space:]]|high|SE-015|Docker login with password on command line exposes credentials|Use docker login --password-stdin or CI/CD registry authentication'
)

# ===========================================================================
# CF -- Caching & Performance (15 patterns: CF-001 to CF-015)
# Free tier
# ===========================================================================

declare -a PIPELINELINT_CF_PATTERNS=(
  'npm[[:space:]]install[^[:space:]]*$|medium|CF-001|npm install without cache configuration may download dependencies every run|Enable npm cache with actions/cache or cache key configuration'
  'pip[[:space:]]install[[:space:]]+-r|medium|CF-002|pip install without cache may re-download packages every build|Use pip cache directory or actions/setup-python with caching enabled'
  'apt-get[[:space:]]install|low|CF-003|apt-get install downloads packages on every run without layer caching|Cache apt packages or use a pre-built Docker image with dependencies'
  'npm[[:space:]]ci[^[:space:]]*$|low|CF-004|npm ci without dependency caching re-downloads node_modules every build|Add actions/cache for node_modules or use setup-node with cache option'
  'yarn[[:space:]]install[^[:space:]]*$|low|CF-005|yarn install without cache configuration slows down builds|Enable yarn cache with actions/cache using yarn cache dir path'
  'docker[[:space:]]build[[:space:]]|medium|CF-006|Docker build without --cache-from may rebuild all layers from scratch|Use --cache-from with registry cache or BuildKit inline cache'
  'gem[[:space:]]install|low|CF-007|gem install without bundler cache re-downloads gems every build|Cache vendor/bundle directory or use setup-ruby with bundler-cache'
  'go[[:space:]]mod[[:space:]]download|low|CF-008|go mod download without GOPATH cache repeats downloads each run|Cache GOPATH/pkg/mod directory between pipeline runs'
  'composer[[:space:]]install|low|CF-009|composer install without cache re-downloads PHP packages every build|Cache composer cache directory between pipeline runs'
  'maven.*compile|medium|CF-010|Maven build without repository cache downloads dependencies every time|Cache ~/.m2/repository directory to speed up Maven builds'
  'gradle[[:space:]]|low|CF-011|Gradle build without cache configuration misses incremental build benefits|Cache ~/.gradle/caches and ~/.gradle/wrapper between builds'
  'cargo[[:space:]]build|low|CF-012|Cargo build without target cache recompiles all dependencies every run|Cache target directory and cargo registry between pipeline runs'
  'restore_cache|low|CF-013|CircleCI restore_cache present -- verify save_cache is also configured|Ensure matching save_cache step exists to persist cache for future runs'
  'fetch-depth[[:space:]]*:[[:space:]]*0|low|CF-014|Git fetch-depth 0 clones full history which slows checkout significantly|Use shallow clone with fetch-depth 1 unless full history is needed'
  'apt-get[[:space:]]update[[:space:]]*&&[[:space:]]*apt-get[[:space:]]install|medium|CF-015|apt-get update and install on every run wastes time without caching|Use a pre-built Docker image or cache the apt lists directory'
)

# ===========================================================================
# TS -- Testing & Quality (15 patterns: TS-001 to TS-015)
# Pro tier
# ===========================================================================

declare -a PIPELINELINT_TS_PATTERNS=(
  'deploy.*prod|high|TS-001|Deployment to production without preceding test step in pipeline|Add test and lint steps that must pass before any production deployment'
  '--no-verify|high|TS-002|--no-verify flag bypasses pre-commit hooks and validation checks|Remove --no-verify flag to ensure all validation hooks run in CI'
  'skip[_-]?tests[[:space:]]*:[[:space:]]*true|high|TS-003|Tests explicitly skipped in pipeline configuration|Remove skip_tests flag -- tests should always run in CI pipelines'
  '-DskipTests|high|TS-004|Maven -DskipTests flag disables test execution in CI build|Remove -DskipTests to ensure test suite runs in pipeline'
  '--no-test|high|TS-005|Test execution explicitly disabled via --no-test flag|Remove --no-test flag to enforce test execution in CI'
  'continue-on-error[[:space:]]*:[[:space:]]*true|medium|TS-006|continue-on-error allows pipeline to pass even when step fails|Use continue-on-error only for non-critical optional steps'
  'allow_failure[[:space:]]*:[[:space:]]*true|medium|TS-007|GitLab allow_failure lets failing jobs not block the pipeline|Reserve allow_failure for truly optional jobs like experimental builds'
  'lint.*#.*disabled|medium|TS-008|Linting step appears commented out or disabled in pipeline|Enable linting step to catch code quality issues before merge'
  '--ignore-scripts|medium|TS-009|npm --ignore-scripts skips package lifecycle scripts including tests|Remove --ignore-scripts unless security risk is explicitly understood'
  'FORCE_COLOR[[:space:]]*=[[:space:]]*0|low|TS-010|Disabling color output may indicate suppressed CI formatting|Ensure CI output formatting is configured for readability not suppression'
  'coverage.*--skip|medium|TS-011|Code coverage reporting appears to be skipped in pipeline|Enable coverage reporting to track test quality over time'
  '--passWithNoTests|medium|TS-012|Jest --passWithNoTests allows suite to pass with zero test files|Remove --passWithNoTests to ensure test files exist and execute'
  '--bail[[:space:]]*false|low|TS-013|Jest --bail false runs all tests even after failures slowing feedback|Consider --bail to fail fast on first test failure in CI'
  'TODO.*test|low|TS-014|TODO comment indicates missing test implementation in pipeline file|Implement the pending test step before merging to main branch'
  '--forceExit|medium|TS-015|Jest --forceExit may mask resource leaks and async cleanup issues|Fix underlying async issues instead of using --forceExit'
)

# ===========================================================================
# AR -- Artifacts & Dependencies (15 patterns: AR-001 to AR-015)
# Pro tier
# ===========================================================================

declare -a PIPELINELINT_AR_PATTERNS=(
  'latest|medium|AR-001|Using latest tag for Docker image is non-deterministic and unreproducible|Pin Docker images to specific SHA digest or version tag'
  'npm[[:space:]]install[[:space:]][^-]|medium|AR-002|npm install with loose versions may introduce untested dependency changes|Use npm ci with a lockfile for deterministic installs in CI'
  'pip[[:space:]]install[[:space:]][^-].*[^=]==[[:space:]]|low|AR-003|pip install without pinned versions risks non-reproducible builds|Pin all dependencies with exact versions in requirements.txt'
  'curl.*[[:space:]]-[[:space:]]*[sS].*sh$|high|AR-004|Piping curl output to shell executes unverified remote code|Download scripts first then verify checksum before execution'
  'wget.*sh$|high|AR-005|Downloading and executing shell scripts from remote URLs is risky|Download scripts first then verify integrity before execution'
  'chmod[[:space:]]+777|high|AR-006|chmod 777 grants world-writable permissions which is a security risk|Use minimal permissions like chmod 755 for executables'
  'npm[[:space:]]audit[[:space:]]fix[[:space:]]--force|medium|AR-007|npm audit fix --force can introduce breaking changes in production|Run npm audit separately and review fixes before applying'
  'actions/checkout@v[12][^0-9]|medium|AR-008|Using old major version of actions/checkout may miss security fixes|Update to latest actions/checkout version for security patches'
  'uses[[:space:]]*:[[:space:]]*[[:alnum:]]+/[[:alnum:]]+@master|high|AR-009|Pinning GitHub Action to master branch is unstable and insecure|Pin GitHub Actions to specific version tag or commit SHA'
  'uses[[:space:]]*:[[:space:]]*[[:alnum:]]+/[[:alnum:]]+@main|high|AR-010|Pinning GitHub Action to main branch is unstable and insecure|Pin GitHub Actions to specific version tag or commit SHA'
  '--trusted-host|high|AR-011|pip --trusted-host disables SSL verification for package downloads|Remove --trusted-host and fix SSL certificate issues instead'
  'npm[[:space:]]config[[:space:]]set[[:space:]]strict-ssl[[:space:]]false|high|AR-012|Disabling npm strict-ssl allows man-in-the-middle attacks|Fix SSL certificate issues instead of disabling verification'
  'apk[[:space:]]add[[:space:]]--no-cache|low|AR-013|Alpine apk add without version pinning may produce different builds|Pin package versions in apk add for reproducible Docker builds'
  'go[[:space:]]get[[:space:]]|medium|AR-014|go get without version specification may fetch unexpected versions|Use go get with explicit version tags for reproducible builds'
  '--no-check-certificate|high|AR-015|wget --no-check-certificate disables SSL verification|Fix SSL certificate issues instead of bypassing verification'
)

# ===========================================================================
# DP -- Deployment Safety (15 patterns: DP-001 to DP-015)
# Team tier
# ===========================================================================

declare -a PIPELINELINT_DP_PATTERNS=(
  'deploy.*prod.*auto|critical|DP-001|Automated deployment to production without manual approval gate|Add manual approval step or environment protection rules before prod deploy'
  'force[[:space:]]push|critical|DP-002|Force push in pipeline can overwrite remote history and lose commits|Remove force push from CI pipelines -- use standard push workflow'
  '--force[[:space:]].*deploy|critical|DP-003|Force flag on deployment command bypasses safety checks|Remove --force flag and fix deployment issues through proper channels'
  'terraform[[:space:]]apply[[:space:]]-auto-approve|critical|DP-004|Terraform apply with -auto-approve skips plan review on infrastructure|Use terraform plan then require manual approval before terraform apply'
  'kubectl[[:space:]]delete|high|DP-005|kubectl delete in pipeline may remove critical resources accidentally|Use declarative kubectl apply instead of imperative delete commands'
  'rm[[:space:]]+-rf|high|DP-006|rm -rf in pipeline scripts risks deleting critical files if path is wrong|Use specific targeted cleanup commands instead of recursive force delete'
  'DROP[[:space:]]TABLE|critical|DP-007|SQL DROP TABLE in pipeline migration may cause irreversible data loss|Use reversible migrations and add manual approval for destructive operations'
  'DROP[[:space:]]DATABASE|critical|DP-008|SQL DROP DATABASE in pipeline is catastrophically destructive|Never include DROP DATABASE in automated pipelines -- require manual DBA approval'
  'environment[[:space:]]*:[[:space:]]*production|low|DP-009|Production environment deployment -- verify protection rules are configured|Configure environment protection rules requiring reviews for production'
  'kubectl[[:space:]]apply.*--all-namespaces|high|DP-010|kubectl apply across all namespaces risks unintended cluster-wide changes|Target specific namespace with -n flag for controlled deployments'
  'helm[[:space:]]upgrade.*--install|medium|DP-011|helm upgrade --install without --wait may not detect failed rollout|Add --wait and --timeout flags to detect deployment failures'
  'docker[[:space:]]push.*latest|medium|DP-012|Pushing Docker image with latest tag makes rollback difficult|Tag images with build number or git SHA for traceable deployments'
  'sleep[[:space:]][0-9]|low|DP-013|Using sleep for deployment timing is fragile and unreliable|Use health check polling or readiness probes instead of sleep'
  'kubectl[[:space:]]rollout[[:space:]]undo|medium|DP-014|kubectl rollout undo without revision may roll back to wrong version|Specify --to-revision flag for predictable rollback behavior'
  'migrate.*--run-unsafe|high|DP-015|Running database migrations with unsafe flag skips safety validations|Remove --run-unsafe and fix migration issues properly'
)

# ===========================================================================
# EN -- Environment & Configuration (15 patterns: EN-001 to EN-015)
# Team tier
# ===========================================================================

declare -a PIPELINELINT_EN_PATTERNS=(
  'localhost|medium|EN-001|Hardcoded localhost in pipeline config will fail in CI/CD environment|Use environment variables or service discovery for host configuration'
  '127\.0\.0\.1|medium|EN-002|Hardcoded loopback IP address will not work in container-based CI|Use service aliases or environment variables for network addresses'
  'timeout[[:space:]]*:[[:space:]]*[0-9]{4,}|low|EN-003|Very large timeout value may allow runaway jobs to consume resources|Set reasonable timeout limits to catch stuck builds early'
  'timeout-minutes[[:space:]]*:[[:space:]]*[0-9]{3,}|medium|EN-004|Job timeout exceeds 100 minutes which may indicate a problem|Investigate why job takes so long and set a reasonable timeout limit'
  'retry[[:space:]]*:[[:space:]]*0|medium|EN-005|Retry count set to zero means no retry on flaky steps|Configure at least 1 retry for network-dependent or flaky steps'
  'max[_-]?retries[[:space:]]*:[[:space:]]*0|medium|EN-006|Max retries disabled may cause pipeline failure on transient errors|Set max_retries to at least 1 for steps that interact with external services'
  'NODE_ENV[[:space:]]*=[[:space:]]*production|medium|EN-007|Hardcoded NODE_ENV=production in pipeline instead of using variable|Use environment-specific variable configuration not hardcoded values'
  'ENV[[:space:]]NODE_ENV[[:space:]]production|medium|EN-008|Hardcoded NODE_ENV in Dockerfile used by pipeline|Parameterize NODE_ENV with ARG or set at runtime with -e flag'
  'http://[[:alnum:]]|medium|EN-009|Plain HTTP URL in pipeline config -- traffic is unencrypted|Use HTTPS for all URLs in pipeline configuration'
  'concurrency[[:space:]]*:[[:space:]]*[0-9]+|low|EN-010|Fixed concurrency limit -- verify it matches deployment environment capacity|Review concurrency settings to match available CI runner capacity'
  'runs-on[[:space:]]*:[[:space:]]*self-hosted|medium|EN-011|Self-hosted runner may have inconsistent environment between runs|Ensure self-hosted runners are containerized or regularly reprovisioned'
  'image[[:space:]]*:[[:space:]]*ubuntu|low|EN-012|Using generic ubuntu image without version tag may drift over time|Pin Ubuntu image to specific version like ubuntu-22.04 for consistency'
  'matrix[[:space:]]*:.*$|low|EN-013|Matrix build present -- verify all combinations are intentional|Review matrix strategy to avoid unnecessary build combinations'
  'DATABASE_URL[[:space:]]*=[[:space:]]*["\x27]postgres|high|EN-014|Database connection string hardcoded in pipeline configuration|Use CI/CD secret variables for database connection strings'
  'when[[:space:]]*:[[:space:]]*manual|low|EN-015|Manual trigger pipeline -- verify automated triggers exist for CI flow|Ensure automated triggers are configured alongside manual options'
)

# ===========================================================================
# Utility Functions
# ===========================================================================

# Count total patterns
pipelinelint_pattern_count() {
  local count=0
  count=$((count + ${#PIPELINELINT_SE_PATTERNS[@]}))
  count=$((count + ${#PIPELINELINT_CF_PATTERNS[@]}))
  count=$((count + ${#PIPELINELINT_TS_PATTERNS[@]}))
  count=$((count + ${#PIPELINELINT_AR_PATTERNS[@]}))
  count=$((count + ${#PIPELINELINT_DP_PATTERNS[@]}))
  count=$((count + ${#PIPELINELINT_EN_PATTERNS[@]}))
  echo "$count"
}

# Count patterns in a specific category
pipelinelint_category_count() {
  local cat="$1"
  case "$cat" in
    SE) echo "${#PIPELINELINT_SE_PATTERNS[@]}" ;;
    CF) echo "${#PIPELINELINT_CF_PATTERNS[@]}" ;;
    TS) echo "${#PIPELINELINT_TS_PATTERNS[@]}" ;;
    AR) echo "${#PIPELINELINT_AR_PATTERNS[@]}" ;;
    DP) echo "${#PIPELINELINT_DP_PATTERNS[@]}" ;;
    EN) echo "${#PIPELINELINT_EN_PATTERNS[@]}" ;;
    *)  echo "0" ;;
  esac
}

# Get the bash array name for a category code
get_pipelinelint_patterns_for_category() {
  local cat="$1"
  case "$cat" in
    SE) echo "PIPELINELINT_SE_PATTERNS" ;;
    CF) echo "PIPELINELINT_CF_PATTERNS" ;;
    TS) echo "PIPELINELINT_TS_PATTERNS" ;;
    AR) echo "PIPELINELINT_AR_PATTERNS" ;;
    DP) echo "PIPELINELINT_DP_PATTERNS" ;;
    EN) echo "PIPELINELINT_EN_PATTERNS" ;;
    *)  echo "" ;;
  esac
}

# Get human-readable label for a category code
get_pipelinelint_category_label() {
  local cat="$1"
  case "$cat" in
    SE) echo "Secrets & Security" ;;
    CF) echo "Caching & Performance" ;;
    TS) echo "Testing & Quality" ;;
    AR) echo "Artifacts & Dependencies" ;;
    DP) echo "Deployment Safety" ;;
    EN) echo "Environment & Configuration" ;;
    *)  echo "Unknown" ;;
  esac
}

# Get space-separated list of category codes available at a given tier level.
# Tier levels: 0=free (SE, CF), 1=pro (SE, CF, TS, AR), 2/3=team/enterprise (all)
get_pipelinelint_categories_for_tier() {
  local tier_level="$1"
  case "$tier_level" in
    0) echo "SE CF" ;;
    1) echo "SE CF TS AR" ;;
    2|3) echo "SE CF TS AR DP EN" ;;
    *) echo "SE CF" ;;
  esac
}

# Severity to point deduction mapping
severity_to_points() {
  local severity="$1"
  case "$severity" in
    critical) echo 25 ;;
    high)     echo 15 ;;
    medium)   echo  8 ;;
    low)      echo  3 ;;
    *)        echo  0 ;;
  esac
}

# Validate that a string is a known category code
is_valid_pipelinelint_category() {
  local cat="$1"
  case "$cat" in
    SE|CF|TS|AR|DP|EN) return 0 ;;
    *) return 1 ;;
  esac
}

# List patterns in a given category or "all"
pipelinelint_list_patterns() {
  local filter="${1:-all}"

  local categories="SE CF TS AR DP EN"
  if [[ "$filter" != "all" ]]; then
    filter=$(echo "$filter" | tr '[:lower:]' '[:upper:]')
    categories="$filter"
  fi

  for cat in $categories; do
    local label
    label=$(get_pipelinelint_category_label "$cat")
    echo -e "${BOLD:-}--- ${cat}: ${label} ---${NC:-}"

    local arr_name
    arr_name=$(get_pipelinelint_patterns_for_category "$cat")
    [[ -z "$arr_name" ]] && continue

    local -n _arr="$arr_name"
    for entry in "${_arr[@]}"; do
      IFS='|' read -r regex severity check_id description recommendation <<< "$entry"
      local sev_upper
      sev_upper=$(echo "$severity" | tr '[:lower:]' '[:upper:]')
      echo "  [$sev_upper] $check_id: $description"
    done
    echo ""
  done
}
