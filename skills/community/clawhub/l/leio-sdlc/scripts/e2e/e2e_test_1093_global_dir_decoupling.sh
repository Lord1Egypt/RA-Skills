#!/bin/bash
set -e

# Setup mock directories
TEST_DIR=$(mktemp -d)
mkdir -p "$TEST_DIR/fake_global_dir"
mkdir -p "$TEST_DIR/fake_workdir"
mkdir -p "$TEST_DIR/fake_workdir/.sdlc_runs"

# Interceptor setup
mkdir -p "$TEST_DIR/bin"
cat << 'EOF' > "$TEST_DIR/bin/openclaw"
#!/bin/bash
echo "$@" > /tmp/intercepted_prompt.log
EOF
chmod +x "$TEST_DIR/bin/openclaw"

# Execution
export PATH="$TEST_DIR/bin:$PATH"

echo "dummy" > "$TEST_DIR/fake_workdir/dummy.md"
echo "dummy prd" > "$TEST_DIR/fake_workdir/dummy_prd.md"

# Test spawn_coder
python3 scripts/spawn_coder.py --workdir "$TEST_DIR/fake_workdir" --global-dir "$TEST_DIR/fake_global_dir" --pr-file "$TEST_DIR/fake_workdir/dummy.md" --prd-file "$TEST_DIR/fake_workdir/dummy_prd.md" || true
if grep -q "You are an autonomous" /tmp/intercepted_prompt.log; then
  echo "PASS: Coder Playbook successfully injected despite fake global-dir."
else
  echo "FAIL: Coder Playbook was empty or not injected."
  cat /tmp/intercepted_prompt.log
  exit 1
fi

rm /tmp/intercepted_prompt.log

# Test spawn_planner
python3 scripts/spawn_planner.py --workdir "$TEST_DIR/fake_workdir" --global-dir "$TEST_DIR/fake_global_dir" --prd-file "$TEST_DIR/fake_workdir/dummy_prd.md" || true
if grep -i -q "objective\|scope" "/tmp/sdlc_prompt"* || grep -i -q "objective\|scope" /tmp/intercepted_prompt.log || cat "/tmp/sdlc_prompt"* | grep -q "You are a senior Software Architect"; then
  echo "PASS: Planner Playbook successfully injected despite fake global-dir."
else
  echo "FAIL: Planner Playbook was empty or not injected."
  cat /tmp/intercepted_prompt.log
  cat "/tmp/sdlc_prompt"*
  exit 1
fi

rm /tmp/intercepted_prompt.log

# Test spawn_reviewer
python3 scripts/spawn_reviewer.py --workdir "$TEST_DIR/fake_workdir" --global-dir "$TEST_DIR/fake_global_dir" --pr-file "$TEST_DIR/fake_workdir/dummy.md" --diff-target "HEAD" --override-diff-file "dummy.diff" || true
if grep -i -q "review" "/tmp/sdlc_prompt"* || grep -i -q "review" /tmp/intercepted_prompt.log || cat "/tmp/sdlc_prompt"* | grep -q "You are a strict, senior Technical Reviewer"; then
  echo "PASS: Reviewer Playbook successfully injected despite fake global-dir."
else
  echo "FAIL: Reviewer Playbook was empty or not injected."
  cat /tmp/intercepted_prompt.log
  exit 1
fi

echo "All E2E checks passed."
